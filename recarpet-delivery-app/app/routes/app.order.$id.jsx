import { json } from "@remix-run/node";
import { useLoaderData, useSubmit, useNavigation } from "@remix-run/react";
import { useState, useCallback } from "react";
import {
  Page,
  Layout,
  Card,
  BlockStack,
  InlineStack,
  Text,
  TextField,
  Button,
  Badge,
  Banner,
  Divider,
  Box,
  Thumbnail,
  InlineGrid,
} from "@shopify/polaris";
import { authenticate } from "../shopify.server.js";

// ── Loader: fetch draft order details ──
export const loader = async ({ request, params }) => {
  const { admin } = await authenticate.admin(request);
  const draftOrderId = `gid://shopify/DraftOrder/${params.id}`;

  const response = await admin.graphql(`
    query getDraftOrder($id: ID!) {
      draftOrder(id: $id) {
        id
        name
        createdAt
        note2
        customer {
          displayName
          companyContactProfiles {
            company {
              name
            }
          }
        }
        lineItems(first: 50) {
          edges {
            node {
              id
              title
              quantity
              variant {
                title
                sku
                image {
                  url
                  altText
                }
              }
              product {
                title
                featuredImage {
                  url
                  altText
                }
              }
            }
          }
        }
        metafield(namespace: "custom", key: "confirmed_delivery_dates") {
          id
          value
        }
      }
    }
  `, { variables: { id: draftOrderId } });

  const data = await response.json();
  const order = data.data.draftOrder;

  if (!order) {
    throw new Response("Order not found", { status: 404 });
  }

  // Parse requested delivery date from notes
  const notes = order.note2 || "";
  const dateMatch = notes.match(/Önskat leveransdatum:\s*(\d{4}-\d{2}-\d{2})/);
  const requestedDate = dateMatch ? dateMatch[1] : null;

  // Parse existing confirmed dates
  let confirmedDates = {};
  if (order.metafield?.value) {
    try {
      const parsed = JSON.parse(order.metafield.value);
      if (parsed.line_items) {
        parsed.line_items.forEach((li) => {
          confirmedDates[li.line_item_id] = li.delivery_date || "";
        });
      }
    } catch (e) {}
  }

  const lineItems = order.lineItems.edges.map(({ node }) => {
    const lineItemId = node.id.split("/").pop();
    return {
      id: lineItemId,
      gid: node.id,
      title: node.product?.title || node.title,
      variantTitle: node.variant?.title !== "Default Title" ? node.variant?.title : null,
      sku: node.variant?.sku || "",
      quantity: node.quantity,
      imageUrl: node.variant?.image?.url || node.product?.featuredImage?.url || null,
      confirmedDate: confirmedDates[lineItemId] || "",
    };
  });

  return json({
    order: {
      id: params.id,
      gid: order.id,
      name: order.name,
      createdAt: order.createdAt,
      customerName:
        order.customer?.companyContactProfiles?.[0]?.company?.name ||
        order.customer?.displayName ||
        "Okänd kund",
      requestedDate,
      notes,
      metafieldId: order.metafield?.id || null,
    },
    lineItems,
  });
};

// ── Action: save confirmed delivery dates ──
export const action = async ({ request, params }) => {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();
  const draftOrderId = `gid://shopify/DraftOrder/${params.id}`;

  const dates = JSON.parse(formData.get("dates"));

  // Build the JSON value
  const metafieldValue = JSON.stringify({
    updated_at: new Date().toISOString(),
    line_items: dates,
  });

  // Save to order metafield
  const response = await admin.graphql(`
    mutation setDeliveryDates($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields {
          id
          namespace
          key
          value
        }
        userErrors {
          field
          message
        }
      }
    }
  `, {
    variables: {
      metafields: [
        {
          ownerId: draftOrderId,
          namespace: "custom",
          key: "confirmed_delivery_dates",
          type: "json",
          value: metafieldValue,
        },
      ],
    },
  });

  const result = await response.json();
  const errors = result.data?.metafieldsSet?.userErrors;

  if (errors?.length > 0) {
    return json({ success: false, errors }, { status: 400 });
  }

  return json({ success: true });
};

// ── Component ──
export default function OrderDeliveryDates() {
  const { order, lineItems } = useLoaderData();
  const submit = useSubmit();
  const navigation = useNavigation();
  const isSaving = navigation.state === "submitting";

  // State: delivery dates per line item
  const [dates, setDates] = useState(() => {
    const initial = {};
    lineItems.forEach((item) => {
      initial[item.id] = item.confirmedDate || "";
    });
    return initial;
  });

  const [saved, setSaved] = useState(false);

  const handleDateChange = useCallback((lineItemId, value) => {
    setDates((prev) => ({ ...prev, [lineItemId]: value }));
    setSaved(false);
  }, []);

  // Apply same date to all items
  const handleApplyToAll = useCallback((date) => {
    const updated = {};
    lineItems.forEach((item) => {
      updated[item.id] = date;
    });
    setDates(updated);
    setSaved(false);
  }, [lineItems]);

  const handleSave = useCallback(() => {
    const payload = lineItems.map((item) => ({
      line_item_id: item.id,
      title: item.title,
      variant: item.variantTitle || "",
      sku: item.sku,
      quantity: item.quantity,
      delivery_date: dates[item.id] || "",
    }));

    const formData = new FormData();
    formData.set("dates", JSON.stringify(payload));
    submit(formData, { method: "POST" });
    setSaved(true);
  }, [dates, lineItems, submit]);

  const allDatesSet = lineItems.every((item) => dates[item.id]);
  const anyDateSet = lineItems.some((item) => dates[item.id]);

  // Format date for display
  const formatDate = (dateStr) => {
    if (!dateStr) return null;
    const d = new Date(dateStr + "T00:00:00");
    return d.toLocaleDateString("sv-SE", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <Page
      backAction={{ url: "/app" }}
      title={`${order.name} — Leveransdatum`}
      subtitle={order.customerName}
      primaryAction={{
        content: isSaving ? "Sparar..." : "Spara leveransdatum",
        onAction: handleSave,
        disabled: isSaving || !anyDateSet,
        loading: isSaving,
      }}
    >
      <BlockStack gap="500">
        {/* Requested delivery date banner */}
        {order.requestedDate ? (
          <Banner tone="info" title="Kundens önskade leveransdatum">
            <BlockStack gap="200">
              <Text as="p" variant="headingMd" fontWeight="bold">
                {formatDate(order.requestedDate)}
              </Text>
              <Text as="p" tone="subdued">
                Datumet kunden valde vid beställning. Bekräfta faktiskt leveransdatum per artikel nedan.
              </Text>
              <InlineStack gap="300">
                <Button
                  size="slim"
                  onClick={() => handleApplyToAll(order.requestedDate)}
                >
                  Använd detta datum för alla artiklar
                </Button>
              </InlineStack>
            </BlockStack>
          </Banner>
        ) : (
          <Banner tone="warning">
            <Text as="p">
              Inget önskat leveransdatum angivet av kunden.
            </Text>
          </Banner>
        )}

        {saved && !isSaving && (
          <Banner tone="success" onDismiss={() => setSaved(false)}>
            <Text as="p">Leveransdatum sparade!</Text>
          </Banner>
        )}

        {/* Line items with date pickers */}
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <Text as="h2" variant="headingMd">
                  Artiklar ({lineItems.length} st)
                </Text>
                <Divider />

                {lineItems.map((item, index) => (
                  <div key={item.id}>
                    <Box paddingBlockStart="300" paddingBlockEnd="300">
                      <InlineGrid columns={["twoThirds", "oneThird"]} gap="400" alignItems="center">
                        {/* Product info */}
                        <InlineStack gap="400" align="start" blockAlign="center">
                          {item.imageUrl ? (
                            <Thumbnail source={item.imageUrl} alt={item.title} size="medium" />
                          ) : (
                            <Thumbnail source="" alt={item.title} size="medium" />
                          )}
                          <BlockStack gap="100">
                            <Text as="p" variant="bodyMd" fontWeight="semibold">
                              {item.title}
                            </Text>
                            {item.variantTitle && (
                              <Text as="p" variant="bodySm" tone="subdued">
                                {item.variantTitle}
                              </Text>
                            )}
                            <InlineStack gap="200">
                              {item.sku && (
                                <Text as="p" variant="bodySm" tone="subdued">
                                  SKU: {item.sku}
                                </Text>
                              )}
                              <Text as="p" variant="bodySm">
                                Antal: {item.quantity}
                              </Text>
                            </InlineStack>
                          </BlockStack>
                        </InlineStack>

                        {/* Date picker */}
                        <BlockStack gap="100">
                          <TextField
                            label="Bekräftat leveransdatum"
                            type="date"
                            value={dates[item.id] || ""}
                            onChange={(value) => handleDateChange(item.id, value)}
                            autoComplete="off"
                            helpText={
                              dates[item.id]
                                ? formatDate(dates[item.id])
                                : "Välj leveransdatum"
                            }
                          />
                          {dates[item.id] && (
                            <Badge tone="success">Bekräftat</Badge>
                          )}
                        </BlockStack>
                      </InlineGrid>
                    </Box>
                    {index < lineItems.length - 1 && <Divider />}
                  </div>
                ))}
              </BlockStack>
            </Card>
          </Layout.Section>

          {/* Sidebar summary */}
          <Layout.Section variant="oneThird">
            <Card>
              <BlockStack gap="300">
                <Text as="h2" variant="headingMd">Sammanfattning</Text>
                <Divider />

                <BlockStack gap="200">
                  <InlineStack align="space-between">
                    <Text as="p" tone="subdued">Order</Text>
                    <Text as="p">{order.name}</Text>
                  </InlineStack>
                  <InlineStack align="space-between">
                    <Text as="p" tone="subdued">Kund</Text>
                    <Text as="p">{order.customerName}</Text>
                  </InlineStack>
                  <InlineStack align="space-between">
                    <Text as="p" tone="subdued">Önskat datum</Text>
                    <Text as="p">
                      {order.requestedDate ? formatDate(order.requestedDate) : "—"}
                    </Text>
                  </InlineStack>
                </BlockStack>

                <Divider />

                <BlockStack gap="200">
                  <Text as="p" variant="headingSm">Bekräftade datum</Text>
                  {lineItems.map((item) => (
                    <InlineStack key={item.id} align="space-between">
                      <Text as="p" variant="bodySm" truncate>
                        {item.title}
                      </Text>
                      <Text as="p" variant="bodySm">
                        {dates[item.id] ? (
                          <Badge tone="success" size="small">
                            {dates[item.id]}
                          </Badge>
                        ) : (
                          <Badge tone="warning" size="small">Ej satt</Badge>
                        )}
                      </Text>
                    </InlineStack>
                  ))}
                </BlockStack>

                {allDatesSet && (
                  <>
                    <Divider />
                    <Banner tone="success">
                      <Text as="p" variant="bodySm">
                        Alla artiklar har bekräftade leveransdatum.
                      </Text>
                    </Banner>
                  </>
                )}
              </BlockStack>
            </Card>

            {/* Order notes */}
            {order.notes && (
              <Box paddingBlockStart="400">
                <Card>
                  <BlockStack gap="200">
                    <Text as="h2" variant="headingMd">Ordernoteringar</Text>
                    <Divider />
                    <Text as="p" variant="bodySm" tone="subdued">
                      {order.notes}
                    </Text>
                  </BlockStack>
                </Card>
              </Box>
            )}
          </Layout.Section>
        </Layout>
      </BlockStack>
    </Page>
  );
}
