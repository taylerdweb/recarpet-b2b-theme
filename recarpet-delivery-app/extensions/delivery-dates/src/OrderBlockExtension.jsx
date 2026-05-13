import { reactExtension } from "@shopify/ui-extensions-react/admin";
import { useEffect, useState } from "react";
import {
  useApi,
  AdminBlock,
  BlockStack,
  InlineStack,
  Text,
  Divider,
  Badge,
  Banner,
  ProgressIndicator,
} from "@shopify/ui-extensions-react/admin";

const TARGET = "admin.order-details.block.render";

export default reactExtension(TARGET, () => <DeliveryDatesBlock />);

function DeliveryDatesBlock() {
  const { data, query } = useApi(TARGET);
  const [lineItems, setLineItems] = useState([]);
  const [dates, setDates] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [source, setSource] = useState(null); // Track where data came from
  const [saveStatus, setSaveStatus] = useState(null); // Debug: track save result

  const resourceId = data?.selected?.[0]?.id;

  // Parse delivery dates from notes text
  function parseDatesFromNotes(notes, items) {
    const dateMap = {};
    if (!notes || !notes.includes("Bekräftade leveransdatum:")) return dateMap;

    const section = notes.split("Bekräftade leveransdatum:")[1] || "";
    const lines = section.trim().split("\n").filter((l) => l.trim() && l.includes(": "));

    lines.forEach((line) => {
      const lastColon = line.lastIndexOf(": ");
      if (lastColon === -1) return;
      const itemName = line.substring(0, lastColon).trim();
      const dateVal = line.substring(lastColon + 2).trim();

      if (!/^\d{4}-\d{2}-\d{2}$/.test(dateVal)) return;

      const matchedItem = items.find((item) => {
        const fullName = item.variantTitle ? `${item.title} (${item.variantTitle})` : item.title;
        return fullName === itemName || item.title === itemName;
      });
      if (matchedItem) {
        dateMap[matchedItem.shortId] = dateVal;
      }
    });
    return dateMap;
  }

  // Parse delivery dates from metafield JSON
  function parseDatesFromMetafield(metafieldValue) {
    try {
      const parsed = JSON.parse(metafieldValue);
      const dateMap = {};
      if (parsed.line_items) {
        parsed.line_items.forEach((li) => {
          if (li.delivery_date) {
            dateMap[li.line_item_id] = li.delivery_date;
          }
        });
      }
      return dateMap;
    } catch (e) {
      return {};
    }
  }

  // Save metafield data AND notes to this order (copies from draft or notes)
  async function saveMetafieldToOrder(items, dateMap, currentNotes) {
    if (Object.keys(dateMap).length === 0) return;

    const payload = {
      updated_at: new Date().toISOString(),
      line_items: items.map((item) => ({
        line_item_id: item.shortId,
        title: item.title,
        variant: item.variantTitle || "",
        sku: item.sku,
        quantity: item.quantity,
        delivery_date: dateMap[item.shortId] || "",
      })),
    };

    // Build delivery text for notes
    const deliveryLines = items
      .filter((item) => dateMap[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dateMap[item.shortId]))
      .map((item) => {
        const label = item.variantTitle ? `${item.title} (${item.variantTitle})` : item.title;
        return `${label}: ${dateMap[item.shortId]}`;
      });

    const errors = [];

    try {
      // Step 1: Save metafield
      const metaResult = await query(`
        mutation {
          metafieldsSet(metafields: [{
            ownerId: "${resourceId}",
            namespace: "custom",
            key: "confirmed_delivery_dates",
            type: "json",
            value: ${JSON.stringify(JSON.stringify(payload))}
          }]) {
            metafields { id }
            userErrors { field message }
          }
        }
      `);

      const metaErrors = metaResult?.data?.metafieldsSet?.userErrors;
      if (metaErrors?.length > 0) {
        errors.push("Metafield: " + metaErrors.map((e) => e.message).join(", "));
      }
      if (metaResult?.errors?.length > 0) {
        errors.push("Metafield GQL: " + metaResult.errors.map((e) => e.message).join(", "));
      }
    } catch (e) {
      errors.push("Metafield exception: " + e.message);
    }

    try {
      // Step 2: Update order notes with delivery dates (for email template)
      if (deliveryLines.length > 0) {
        const deliveryText = "Bekräftade leveransdatum:\n" + deliveryLines.join("\n");
        const notes = currentNotes || "";
        const deliverySection = /Bekräftade leveransdatum:\n[\s\S]*?(?=\n\n|$)/;
        let updatedNotes;
        if (deliverySection.test(notes)) {
          updatedNotes = notes.replace(deliverySection, deliveryText);
        } else {
          updatedNotes = notes ? notes + "\n\n" + deliveryText : deliveryText;
        }

        const notesResult = await query(`
          mutation {
            orderUpdate(input: {
              id: "${resourceId}",
              note: ${JSON.stringify(updatedNotes)}
            }) {
              order { id }
              userErrors { field message }
            }
          }
        `);

        const notesErrors = notesResult?.data?.orderUpdate?.userErrors;
        if (notesErrors?.length > 0) {
          errors.push("Notes: " + notesErrors.map((e) => e.message).join(", "));
        }
        if (notesResult?.errors?.length > 0) {
          errors.push("Notes GQL: " + notesResult.errors.map((e) => e.message).join(", "));
        }
      }
    } catch (e) {
      errors.push("Notes exception: " + e.message);
    }

    if (errors.length > 0) {
      setSaveStatus("Fel vid auto-sparning: " + errors.join(" | "));
    } else {
      setSaveStatus("Auto-sparad till metafield + anteckningar");
    }
  }

  // Search for the source draft order and get its delivery dates
  async function fetchFromDraftOrder(orderName) {
    try {
      // Search draft orders matching this order's name pattern
      // Draft order names are like "#D123", order names are like "#1123"
      // We search recent draft orders and match by customer/line items
      const result = await query(`
        query {
          draftOrders(first: 10, sortKey: UPDATED_AT, reverse: true) {
            edges {
              node {
                id
                name
                note2
                metafield(namespace: "custom", key: "confirmed_delivery_dates") {
                  value
                }
              }
            }
          }
        }
      `);

      const draftOrders = result.data?.draftOrders?.edges || [];

      for (const { node: draft } of draftOrders) {
        // Check metafield first
        if (draft.metafield?.value) {
          const dateMap = parseDatesFromMetafield(draft.metafield.value);
          if (Object.keys(dateMap).length > 0) {
            return {
              dateMap,
              rawMetafield: draft.metafield.value,
              source: "draft-metafield",
              draftName: draft.name,
            };
          }
        }

        // Check notes as fallback
        if (draft.note2 && draft.note2.includes("Bekräftade leveransdatum:")) {
          return { notes: draft.note2, source: "draft-notes", draftName: draft.name };
        }
      }

      return null;
    } catch (e) {
      return null;
    }
  }

  useEffect(() => {
    async function fetchData() {
      if (!resourceId) return;

      try {
        const result = await query(`
          query {
            order(id: "${resourceId}") {
              name
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
          }
        `);

        const order = result.data.order;
        if (!order) {
          setError("Kunde inte hämta orderdata");
          setLoading(false);
          return;
        }

        const notes = order.note || "";
        const orderName = order.name || "";

        // Parse line items
        const items = order.lineItems.edges.map(({ node }) => ({
          id: node.id,
          shortId: node.id.split("/").pop(),
          title: node.product?.title || node.title,
          variantTitle: node.variant?.title !== "Default Title" ? node.variant?.title : null,
          sku: node.variant?.sku || "",
          quantity: node.quantity,
        }));
        setLineItems(items);

        // === SOURCE 1: Order metafield ===
        if (order.metafield?.value) {
          const dateMap = parseDatesFromMetafield(order.metafield.value);
          if (Object.values(dateMap).some((d) => d)) {
            setDates(dateMap);
            setSource("metafield");
            setLoading(false);
            return;
          }
        }

        // === SOURCE 2: Order custom attributes (copies from draft automatically) ===
        const deliveryAttr = (order.customAttributes || []).find(
          (a) => a.key === "_confirmed_delivery_dates"
        );
        if (deliveryAttr?.value) {
          const attrDates = parseDatesFromNotes(
            "Bekräftade leveransdatum:\n" + deliveryAttr.value,
            items
          );
          if (Object.keys(attrDates).length > 0) {
            setDates(attrDates);
            setSource("attributes");
            // Save to metafield + notes for customer account extension and re-sent emails
            await saveMetafieldToOrder(items, attrDates, notes);
            setLoading(false);
            return;
          }
        }

        // === SOURCE 3: Order notes ===
        if (notes.includes("Bekräftade leveransdatum:")) {
          const noteDates = parseDatesFromNotes(notes, items);
          if (Object.keys(noteDates).length > 0) {
            setDates(noteDates);
            setSource("notes");
            // Auto-save to metafield for customer account extension
            await saveMetafieldToOrder(items, noteDates, notes);
            setLoading(false);
            return;
          }
        }

        // === SOURCE 3: Look up source draft order ===
        // Shopify doesn't copy metafields from draft → order, so we fetch
        // recent draft orders and match delivery dates by product title.
        const draftData = await fetchFromDraftOrder(orderName);
        if (draftData) {
          let dateMap = {};

          if (draftData.dateMap) {
            // Got dates from draft metafield — re-match to order line items by title
            // (line item IDs differ between draft and order)
            try {
              const parsed = JSON.parse(
                draftData.rawMetafield || "{}"
              );
              if (parsed.line_items) {
                parsed.line_items.forEach((draftItem) => {
                  if (!draftItem.delivery_date) return;
                  const orderItem = items.find((oi) => {
                    const draftLabel = draftItem.variant
                      ? `${draftItem.title} (${draftItem.variant})`
                      : draftItem.title;
                    const orderLabel = oi.variantTitle
                      ? `${oi.title} (${oi.variantTitle})`
                      : oi.title;
                    return orderLabel === draftLabel || oi.title === draftItem.title;
                  });
                  if (orderItem) {
                    dateMap[orderItem.shortId] = draftItem.delivery_date;
                  }
                });
              }
            } catch (e) {}
          } else if (draftData.notes) {
            dateMap = parseDatesFromNotes(draftData.notes, items);
          }

          if (Object.keys(dateMap).length > 0) {
            setDates(dateMap);
            setSource("draft");
            // Save to order metafield + notes so we don't need to look up again
            await saveMetafieldToOrder(items, dateMap, notes);
            setLoading(false);
            return;
          }
        }

        // No data found anywhere
      } catch (e) {
        setError("Fel vid hämtning: " + e.message);
      }
      setLoading(false);
    }
    fetchData();
  }, [resourceId, query]);

  const confirmedCount = lineItems.filter(
    (item) => dates[item.shortId] && /^\d{4}-\d{2}-\d{2}$/.test(dates[item.shortId])
  ).length;

  if (loading) {
    return (
      <AdminBlock title="Leveransdatum">
        <BlockStack gap="base">
          <ProgressIndicator size="small" />
          <Text>Laddar...</Text>
        </BlockStack>
      </AdminBlock>
    );
  }

  if (confirmedCount === 0) {
    return (
      <AdminBlock title="Leveransdatum">
        <Banner status="warning">Inga leveransdatum bekräftade för denna order.</Banner>
      </AdminBlock>
    );
  }

  return (
    <AdminBlock title={`Leveransdatum (${confirmedCount}/${lineItems.length})`}>
      <BlockStack gap="base">
        {error && <Banner status="critical">{error}</Banner>}

        {/* Debug: show auto-save result */}
        {saveStatus && (
          <Banner status={saveStatus.startsWith("Fel") ? "warning" : "info"}>
            {saveStatus}
          </Banner>
        )}
        {source && (
          <Text appearance="subdued" size="small">Källa: {source}</Text>
        )}

        {lineItems.map((item, index) => {
          const date = dates[item.shortId];
          const hasDate = date && /^\d{4}-\d{2}-\d{2}$/.test(date);

          return (
            <BlockStack key={item.id} gap="tight">
              <InlineStack gap="base" blockAlignment="center" inlineAlignment="spaceBetween">
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
                {hasDate ? (
                  <Badge tone="success">{date}</Badge>
                ) : (
                  <Badge tone="warning">Ej satt</Badge>
                )}
              </InlineStack>
              {index < lineItems.length - 1 && <Divider />}
            </BlockStack>
          );
        })}
      </BlockStack>
    </AdminBlock>
  );
}
