import { json } from "@remix-run/node";
import { authenticate } from "../shopify.server.js";

/**
 * App Proxy endpoint — called from the storefront (customer account page)
 * to fetch confirmed delivery dates for a specific order.
 *
 * URL: /apps/delivery-dates/api/proxy/delivery-dates?order_id=123
 */
export const loader = async ({ request }) => {
  const { session, admin } = await authenticate.public.appProxy(request);
  const url = new URL(request.url);
  const orderId = url.searchParams.get("order_id");

  if (!orderId) {
    return json({ error: "order_id required" }, { status: 400 });
  }

  // Try draft order first, then regular order
  const gid = `gid://shopify/DraftOrder/${orderId}`;
  const orderGid = `gid://shopify/Order/${orderId}`;

  let metafieldValue = null;
  let orderName = null;
  let requestedDate = null;

  // Try draft order
  const draftResponse = await admin.graphql(`
    query getDraftOrderDates($id: ID!) {
      draftOrder(id: $id) {
        name
        note2
        metafield(namespace: "custom", key: "confirmed_delivery_dates") {
          value
        }
      }
    }
  `, { variables: { id: gid } });

  const draftData = await draftResponse.json();

  if (draftData.data?.draftOrder) {
    const draft = draftData.data.draftOrder;
    metafieldValue = draft.metafield?.value;
    orderName = draft.name;
    const notes = draft.note2 || "";
    const match = notes.match(/Önskat leveransdatum:\s*(\d{4}-\d{2}-\d{2})/);
    requestedDate = match ? match[1] : null;
  } else {
    // Try regular order
    const orderResponse = await admin.graphql(`
      query getOrderDates($id: ID!) {
        order(id: $id) {
          name
          note
          metafield(namespace: "custom", key: "confirmed_delivery_dates") {
            value
          }
        }
      }
    `, { variables: { id: orderGid } });

    const orderData = await orderResponse.json();
    if (orderData.data?.order) {
      const order = orderData.data.order;
      metafieldValue = order.metafield?.value;
      orderName = order.name;
      const notes = order.note || "";
      const match = notes.match(/Önskat leveransdatum:\s*(\d{4}-\d{2}-\d{2})/);
      requestedDate = match ? match[1] : null;
    }
  }

  if (!metafieldValue) {
    return json({
      order_name: orderName,
      requested_date: requestedDate,
      confirmed_dates: null,
      message: "Inga bekräftade leveransdatum ännu.",
    });
  }

  let confirmed;
  try {
    confirmed = JSON.parse(metafieldValue);
  } catch (e) {
    return json({ error: "Invalid metafield data" }, { status: 500 });
  }

  return json({
    order_name: orderName,
    requested_date: requestedDate,
    confirmed_dates: confirmed,
  });
};
