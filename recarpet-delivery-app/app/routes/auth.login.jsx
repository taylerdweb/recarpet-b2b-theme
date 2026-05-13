import { json } from "@remix-run/node";
import { Form, useLoaderData } from "@remix-run/react";
import {
  AppProvider,
  Card,
  Page,
  Text,
  TextField,
  Button,
  BlockStack,
} from "@shopify/polaris";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";
import { login } from "../shopify.server.js";
import { useState } from "react";

export const links = () => [{ rel: "stylesheet", href: polarisStyles }];

export const loader = async ({ request }) => {
  const url = new URL(request.url);
  const errors = {};

  if (url.searchParams.get("shop")?.endsWith(".myshopify.com")) {
    throw await login(request);
  }

  return json({ errors, polarisTranslations: require("@shopify/polaris/locales/en.json") });
};

export const action = async ({ request }) => {
  const errors = {};
  const formData = await request.formData();
  const shop = formData.get("shop");

  if (!shop) {
    errors.shop = "Ange butikens URL";
    return json({ errors });
  }

  throw await login(request);
};

export default function Auth() {
  const { errors } = useLoaderData();
  const [shop, setShop] = useState("");

  return (
    <AppProvider i18n={{}}>
      <Page>
        <Card>
          <Form method="post">
            <BlockStack gap="400">
              <Text variant="headingMd" as="h2">Logga in</Text>
              <TextField
                type="text"
                name="shop"
                label="Butikens URL"
                value={shop}
                onChange={setShop}
                autoComplete="on"
                placeholder="recarpet-b2b.myshopify.com"
                error={errors?.shop}
              />
              <Button submit variant="primary">Logga in</Button>
            </BlockStack>
          </Form>
        </Card>
      </Page>
    </AppProvider>
  );
}
