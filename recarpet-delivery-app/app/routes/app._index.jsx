import { json } from "@remix-run/node";
import { useLoaderData, useNavigate } from "@remix-run/react";
import {
  Page,
  Layout,
  Card,
  DataTable,
  Badge,
  Text,
  BlockStack,
  Banner,
} from "@shopify/polaris";
import { authenticate } from "../shopify.server.js";

export const loader = async ({ request }) => {
  const { admin } = await authenticate.admin(request);

  // Fetch recent draft orders
  const response = await admin.graphql(`
    query {
      draftOrders(first: 25, sortKey: UPDATED_AT, reverse: true) {
        edges {
          node {
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
                }
              }
            }
            metafield(namespace: "custom", key: "confirmed_delivery_dates") {
              value
            }
          }
        }
      }
    }
  `);

  const data = await response.json();
  const draftOrders = data.data.draftOrders.edges.map(({ node }) => {
    // Parse requested delivery date from notes
    const notes = node.note2 || "";
    const dateMatch = notes.match(/Önskat leveransdatum:\s*(\d{4}-\d{2}-\d{2})/);
    const requestedDate = dateMatch ? dateMatch[1] : null;

    // Parse confirmed dates
    let confirmedDates = null;
    if (node.metafield?.value) {
      try {
        confirmedDates = JSON.parse(node.metafield.value);
      } catch (e) {}
    }

    const totalItems = node.lineItems.edges.length;
    const confirmedItems = confirmedDates?.line_items?.filter((li) => li.delivery_date).length || 0;

    return {
      id: node.id,
      name: node.name,
      createdAt: node.createdAt,
      customerName: node.customer?.companyContactProfiles?.[0]?.company?.name
        || node.customer?.displayName
        || "Okänd kund",
      requestedDate,
      totalItems,
      confirmedItems,
      allConfirmed: totalItems > 0 && confirmedItems === totalItems,
    };
  });

  return json({ draftOrders });
};

export default function Index() {
  const { draftOrders } = useLoaderData();
  const navigate = useNavigate();

  const rows = draftOrders.map((order) => [
    order.name,
    order.customerName,
    order.requestedDate || "—",
    order.allConfirmed ? (
      <Badge tone="success">Alla bekräftade</Badge>
    ) : order.confirmedItems > 0 ? (
      <Badge tone="attention">{order.confirmedItems}/{order.totalItems} bekräftade</Badge>
    ) : (
      <Badge tone="warning">Ej bekräftade</Badge>
    ),
  ]);

  return (
    <Page title="Leveransdatum">
      <BlockStack gap="500">
        <Banner tone="info">
          <Text as="p">
            Här ser du alla orderutkast med kundens önskade leveransdatum.
            Klicka på en order för att bekräfta leveransdatum per artikel.
          </Text>
        </Banner>

        <Layout>
          <Layout.Section>
            <Card padding="0">
              <DataTable
                columnContentTypes={["text", "text", "text", "text"]}
                headings={["Order", "Kund", "Önskat datum", "Status"]}
                rows={rows}
                hoverable
                onRowClick={(index) => {
                  const orderId = draftOrders[index].id.split("/").pop();
                  navigate(`/app/order/${orderId}`);
                }}
              />
            </Card>
          </Layout.Section>
        </Layout>
      </BlockStack>
    </Page>
  );
}
