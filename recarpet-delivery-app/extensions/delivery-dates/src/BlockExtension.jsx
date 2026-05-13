import { useEffect, useState, useCallback } from "react";
import {
  reactExtension,
  useApi,
  AdminBlock,
  BlockStack,
  InlineStack,
  Text,
  TextField,
  Button,
  Divider,
  Badge,
  Banner,
  ProgressIndicator,
} from "@shopify/ui-extensions-react/admin";

// Register for both draft orders and regular orders
const TARGET = "admin.draft-order-details.block.render";

export default reactExtension(TARGET, () => <DeliveryDatesBlock />);

function DeliveryDatesBlock() {
  const { data, query } = useApi(TARGET);
  const [lineItems, setLineItems] = useState([]);
  const [dates, setDates] = useState({});
  const [requestedDate, setRequestedDate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState(null);

  const [existingNotes, setExistingNotes] = useState("");
  const [notesSynced, setNotesSynced] = useState(false);
  const [existingAttributes, setExistingAttributes] = useState([]);

  // Determine if this is a draft order or regular order
  const resourceId = data?.selected?.[0]?.id;

  // Fetch order data on mount
  useEffect(() => {
    async function fetchData() {
      if (!resourceId) return;

      try {
        const isDraft = resourceId.includes("DraftOrder");

        const queryStr = isDraft
          ? `query {
              draftOrder(id: "${resourceId}") {
                note2
                customAttributes { key value }
                lineItems(first: 50) {
                  edges {
                    node {
                      id
                      title
                      quantity
                      variant { title sku }
                      product { title }
                    }
                  }
                }
                metafield(namespace: "custom", key: "confirmed_delivery_dates") {
                  id
                  value
                }
              }
            }`
          : `query {
              order(id: "${resourceId}") {
                note
                customAttributes { key value }
                lineItems(first: 50) {
                  edges {
                    node {
                      id
                      title
                      quantity
                      variant { title sku }
                      product { title }
                    }
                  }
                }
                metafield(namespace: "custom", key: "confirmed_delivery_dates") {
                  id
                  value
                }
              }
            }`;

        const result = await query(queryStr);
        const resource = isDraft ? result.data.draftOrder : result.data.order;

        if (!resource) {
          setError("Kunde inte hämta orderdata");
          setLoading(false);
          return;
        }

        // Store existing custom attributes (sparkCartId, sparkPaymentType, etc.)
        const attrs = (resource.customAttributes || []).filter(
          (a) => a.key !== "_confirmed_delivery_dates"
        );
        setExistingAttributes(attrs);

        // Parse requested date from notes and store existing notes
        const notes = (isDraft ? resource.note2 : resource.note) || "";
        setExistingNotes(notes);
        const dateMatch = notes.match(/Önskat leveransdatum:\s*(\d{4}-\d{2}-\d{2})/);
        if (dateMatch) setRequestedDate(dateMatch[1]);

        // Parse line items
        const items = resource.lineItems.edges.map(({ node }) => ({
          id: node.id,
          shortId: node.id.split("/").pop(),
          title: node.product?.title || node.title,
          variantTitle: node.variant?.title !== "Default Title" ? node.variant?.title : null,
          sku: node.variant?.sku || "",
          quantity: node.quantity,
        }));
        setLineItems(items);

        // Parse existing confirmed dates
        if (resource.metafield?.value) {
          try {
            const parsed = JSON.parse(resource.metafield.value);
            const dateMap = {};
            if (parsed.line_items) {
              parsed.line_items.forEach((li) => {
                dateMap[li.line_item_id] = li.delivery_date || "";
              });
            }
            setDates(dateMap);
          } catch (e) {}
        }
      } catch (e) {
        setError("Fel vid hämtning: " + e.message);
      }

      setLoading(false);
    }

    fetchData();
  }, [resourceId, query]);

  // Auto-sync: if metafield has dates but notes are missing delivery section,
  // repair notes automatically. This handles the case where Shopify's admin
  // "Spara" button overwrote notes but the metafield survived (metafieldsSet).
  useEffect(() => {
    if (loading || notesSynced || !resourceId || lineItems.length === 0) return;

    const hasConfirmedDates = lineItems.some(
      (item) => dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId])
    );
    if (!hasConfirmedDates) return;

    // If notes already have delivery section, no sync needed
    if (existingNotes.includes("Bekräftade leveransdatum:")) {
      setNotesSynced(true);
      return;
    }

    // Build delivery text from current dates
    const lines = lineItems
      .filter((item) => dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId]))
      .map((item) => {
        const label = item.variantTitle ? `${item.title} (${item.variantTitle})` : item.title;
        return `${label}: ${dates[item.shortId]}`;
      });
    if (lines.length === 0) return;

    const deliveryText = "Bekräftade leveransdatum:\n" + lines.join("\n");
    const updatedNotes = existingNotes
      ? existingNotes + "\n\n" + deliveryText
      : deliveryText;

    const isDraft = resourceId.includes("DraftOrder");
    const notesMutation = isDraft
      ? `mutation { draftOrderUpdate(id: "${resourceId}", input: { note: ${JSON.stringify(updatedNotes)} }) { draftOrder { id } userErrors { field message } } }`
      : `mutation { orderUpdate(input: { id: "${resourceId}", note: ${JSON.stringify(updatedNotes)} }) { order { id } userErrors { field message } } }`;

    setNotesSynced(true);
    query(notesMutation)
      .then(() => setExistingNotes(updatedNotes))
      .catch(() => {});
  }, [loading, notesSynced, resourceId, lineItems, dates, existingNotes, query]);

  // Handle date change for a line item
  const handleDateChange = useCallback((lineItemId, value) => {
    setDates((prev) => ({ ...prev, [lineItemId]: value }));
    setSaved(false);
  }, []);

  // Apply requested date to all items
  const handleApplyAll = useCallback(() => {
    if (!requestedDate) return;
    const updated = {};
    lineItems.forEach((item) => {
      updated[item.shortId] = requestedDate;
    });
    setDates(updated);
    setSaved(false);
  }, [requestedDate, lineItems]);

  // Build delivery dates text for notes
  const buildDeliveryNotesText = useCallback(() => {
    const lines = lineItems
      .filter((item) => dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId]))
      .map((item) => {
        const label = item.variantTitle ? `${item.title} (${item.variantTitle})` : item.title;
        return `${label}: ${dates[item.shortId]}`;
      });
    if (lines.length === 0) return "";
    return "Bekräftade leveransdatum:\n" + lines.join("\n");
  }, [dates, lineItems]);

  // Save confirmed dates to metafield + notes
  const handleSave = useCallback(async () => {
    setSaving(true);
    setError(null);

    const payload = {
      updated_at: new Date().toISOString(),
      line_items: lineItems.map((item) => ({
        line_item_id: item.shortId,
        title: item.title,
        variant: item.variantTitle || "",
        sku: item.sku,
        quantity: item.quantity,
        delivery_date: dates[item.shortId] || "",
      })),
    };

    const isDraft = resourceId.includes("DraftOrder");

    // Build updated notes: keep existing notes but replace/append delivery dates section
    const deliveryText = buildDeliveryNotesText();
    let updatedNotes = existingNotes;
    const deliverySection = /Bekräftade leveransdatum:\n[\s\S]*?(?=\n\n|$)/;
    if (deliverySection.test(updatedNotes)) {
      updatedNotes = updatedNotes.replace(deliverySection, deliveryText);
    } else {
      updatedNotes = updatedNotes ? updatedNotes + "\n\n" + deliveryText : deliveryText;
    }

    try {
      const metafieldValue = JSON.stringify(payload);

      // Step 1: Save metafield via metafieldsSet (independent mutation).
      // This is NOT affected by Shopify's own "Spara" button on the draft
      // order page, which can overwrite draftOrderUpdate changes.
      const metaResult = await query(`
        mutation {
          metafieldsSet(metafields: [{
            ownerId: "${resourceId}",
            namespace: "custom",
            key: "confirmed_delivery_dates",
            type: "json",
            value: ${JSON.stringify(metafieldValue)}
          }]) {
            metafields { id }
            userErrors { field message }
          }
        }
      `);

      const metaErrors = metaResult.data?.metafieldsSet?.userErrors;
      if (metaErrors?.length > 0) {
        setError("Metafield: " + metaErrors.map((e) => e.message).join(", "));
        setSaving(false);
        return;
      }

      // Step 2: Update notes + custom attributes via draftOrderUpdate/orderUpdate.
      // Custom attributes copy from draft → order automatically and survive
      // Shopify's admin "Spara" button (unlike notes which get overwritten).
      const deliveryAttrValue = lineItems
        .filter((item) => dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId]))
        .map((item) => {
          const label = item.variantTitle ? `${item.title} (${item.variantTitle})` : item.title;
          return `${label}: ${dates[item.shortId]}`;
        })
        .join("\n");

      // Merge existing attributes with our delivery dates attribute
      const allAttributes = [
        ...existingAttributes.map((a) => `{ key: ${JSON.stringify(a.key)}, value: ${JSON.stringify(a.value)} }`),
        `{ key: "_confirmed_delivery_dates", value: ${JSON.stringify(deliveryAttrValue)} }`,
      ].join(", ");

      const updateMutation = isDraft
        ? `mutation { draftOrderUpdate(id: "${resourceId}", input: { note: ${JSON.stringify(updatedNotes)}, customAttributes: [${allAttributes}] }) { draftOrder { id } userErrors { field message } } }`
        : `mutation { orderUpdate(input: { id: "${resourceId}", note: ${JSON.stringify(updatedNotes)} }) { order { id } userErrors { field message } } }`;

      const updateResult = await query(updateMutation);
      const updateErrors = isDraft
        ? updateResult.data?.draftOrderUpdate?.userErrors
        : updateResult.data?.orderUpdate?.userErrors;

      if (updateErrors?.length > 0) {
        setSaved(true);
        setExistingNotes(updatedNotes);
        setError("Leveransdatum sparade, men uppdatering misslyckades: " + updateErrors.map((e) => e.message).join(", "));
      } else {
        setSaved(true);
        setExistingNotes(updatedNotes);
      }
    } catch (e) {
      setError("Kunde inte spara: " + e.message);
    }

    setSaving(false);
  }, [dates, lineItems, resourceId, query, existingNotes, buildDeliveryNotesText]);

  // Count confirmed
  const confirmedCount = lineItems.filter((item) => dates[item.shortId]).length;
  const allConfirmed = lineItems.length > 0 && confirmedCount === lineItems.length;

  if (loading) {
    return (
      <AdminBlock title="Leveransdatum">
        <BlockStack gap="base">
          <ProgressIndicator size="small" />
          <Text>Laddar orderdata...</Text>
        </BlockStack>
      </AdminBlock>
    );
  }

  return (
    <AdminBlock
      title={`Leveransdatum (${confirmedCount}/${lineItems.length} bekräftade)`}
    >
      <BlockStack gap="base">
        {/* Requested date banner */}
        {requestedDate && (
          <Banner
            status="info"
            title={`Kunden önskar leverans: ${requestedDate}`}
            action={{
              content: "Applicera på alla",
              onAction: handleApplyAll,
            }}
          />
        )}

        {error && <Banner status="critical">{error}</Banner>}
        {saved && <Banner status="success">Leveransdatum sparade!</Banner>}

        <Divider />

        {/* Line items with date pickers */}
        {lineItems.map((item, index) => (
          <BlockStack key={item.id} gap="tight">
            <InlineStack gap="base" blockAlignment="center">
              <BlockStack gap="none">
                <Text fontWeight="bold">{item.title}</Text>
                <InlineStack gap="tight">
                  {item.variantTitle && (
                    <Text appearance="subdued" size="small">{item.variantTitle}</Text>
                  )}
                  {item.sku && (
                    <Text appearance="subdued" size="small">SKU: {item.sku}</Text>
                  )}
                  <Text size="small">Antal: {item.quantity}</Text>
                </InlineStack>
              </BlockStack>
            </InlineStack>

            <InlineStack gap="base" blockAlignment="center">
              <TextField
                label="Leveransdatum (ÅÅÅÅ-MM-DD)"
                value={dates[item.shortId] || ""}
                placeholder="2026-06-20"
                onChange={(value) => handleDateChange(item.shortId, value)}
              />
              {dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId]) ? (
                <Badge tone="success">Bekräftat</Badge>
              ) : dates[item.shortId] ? (
                <Badge tone="warning">Ogiltigt format</Badge>
              ) : (
                <Badge tone="warning">Ej satt</Badge>
              )}
            </InlineStack>

            {index < lineItems.length - 1 && <Divider />}
          </BlockStack>
        ))}

        <Divider />

        {/* Save button */}
        <InlineStack gap="base" inlineAlignment="end">
          <Button
            variant="primary"
            onPress={handleSave}
            disabled={saving}
            loading={saving}
          >
            {saving ? "Sparar..." : "Spara leveransdatum"}
          </Button>
        </InlineStack>

        {allConfirmed && (
          <Banner status="success">
            Alla artiklar har bekräftade leveransdatum.
          </Banner>
        )}
      </BlockStack>
    </AdminBlock>
  );
}
