import { useEffect, useState } from "react";
import {
  reactExtension,
  useApi,
  useAppMetafields,
  BlockStack,
  InlineStack,
  Text,
  Divider,
  Heading,
} from "@shopify/ui-extensions-react/customer-account";

const TARGET = "customer-account.order-status.block.render";

export default reactExtension(TARGET, () => <DeliveryDatesCustomer />);

function DeliveryDatesCustomer() {
  const api = useApi(TARGET);
  const [deliveryItems, setDeliveryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [debug, setDebug] = useState("");

  // Approach 1: Try useAppMetafields (declared in TOML config)
  let appMetafields = [];
  try {
    appMetafields = useAppMetafields({
      namespace: "custom",
      key: "confirmed_delivery_dates",
    });
  } catch (e) {
    // Hook might not be available
  }

  useEffect(() => {
    async function loadData() {
      // First: check appMetafields from TOML declaration
      if (appMetafields && appMetafields.length > 0) {
        const entry = appMetafields[0];
        const metaValue = entry?.metafield?.value;
        if (metaValue) {
          try {
            const parsed = JSON.parse(metaValue);
            if (parsed.line_items) {
              const items = parsed.line_items.filter((li) => li.delivery_date);
              if (items.length > 0) {
                setDeliveryItems(items);
                setLoading(false);
                return;
              }
            }
          } catch (e) {
            // Parse error, try fallback
          }
        }
      }

      // Fallback: try Storefront API query with node()
      try {
        if (!api.query) {
          setDebug(
            "Ingen query. appMetafields: " + JSON.stringify(appMetafields)
          );
          setLoading(false);
          return;
        }

        // Try to get order ID from the extension API
        const orderData = api.order?.current;
        const orderId = orderData?.id;

        if (!orderId) {
          setDebug(
            "Ingen order-ID. keys: " +
              Object.keys(api).join(",") +
              " | appMeta: " +
              appMetafields.length
          );
          setLoading(false);
          return;
        }

        // Query Storefront API using node() to fetch order metafield
        const result = await api.query(
          `query OrderMetafield($orderId: ID!) {
            node(id: $orderId) {
              ... on Order {
                metafield(key: "confirmed_delivery_dates", namespace: "custom") {
                  value
                }
              }
            }
          }`,
          {
            variables: { orderId },
          }
        );

        if (result?.errors?.length > 0) {
          setDebug(
            "Query-fel: " + result.errors.map((e) => e.message).join(", ")
          );
          setLoading(false);
          return;
        }

        const metaValue = result?.data?.node?.metafield?.value;
        if (metaValue) {
          const parsed = JSON.parse(metaValue);
          if (parsed.line_items) {
            const items = parsed.line_items.filter((li) => li.delivery_date);
            setDeliveryItems(items);
          }
        } else {
          setDebug("Inget metafält via node-query (order: " + orderId + ")");
        }
      } catch (e) {
        setDebug("Fel: " + e.message);
      }
      setLoading(false);
    }
    loadData();
  }, [api, appMetafields.length]);

  if (loading) {
    return (
      <BlockStack padding="base">
        <Text>Laddar leveransdatum...</Text>
      </BlockStack>
    );
  }

  if (deliveryItems.length === 0) {
    if (debug) {
      return (
        <BlockStack padding="base">
          <Text appearance="subdued" size="small">
            Leveransdatum: {debug}
          </Text>
        </BlockStack>
      );
    }
    return null;
  }

  return (
    <BlockStack padding="base">
      <Heading level={3}>Bekräftade leveransdatum</Heading>
      <Divider />
      {deliveryItems.map((item, index) => (
        <BlockStack key={item.line_item_id || index} gap="extraTight">
          <InlineStack blockAlignment="center" inlineAlignment="space-between">
            <Text emphasis="bold">
              {item.title}
              {item.variant ? ` — ${item.variant}` : ""}
            </Text>
            <Text emphasis="bold">{item.delivery_date}</Text>
          </InlineStack>
          {index < deliveryItems.length - 1 && <Divider />}
        </BlockStack>
      ))}
    </BlockStack>
  );
}
