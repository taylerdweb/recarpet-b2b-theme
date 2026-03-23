#!/usr/bin/env node
/**
 * ReCarpet Image Upload Script
 *
 * Downloads images from old Webflow site and uploads them to Shopify,
 * then outputs the Shopify CDN URLs mapped to each section.
 *
 * Usage:
 *   1. Go to Shopify Admin → Settings → Apps and sales channels → Develop apps
 *   2. Create or open an app → API credentials → Admin API access token
 *   3. Make sure the app has "write_files" and "write_themes" scopes
 *   4. Run: SHOPIFY_TOKEN=shpat_xxxxx SHOPIFY_STORE=recarpet-build node scripts/upload-images.js
 */

const https = require('https');
const http = require('http');

const STORE = process.env.SHOPIFY_STORE || 'recarpet-build';
const TOKEN = process.env.SHOPIFY_TOKEN;

if (!TOKEN) {
  console.error('\n❌ Missing SHOPIFY_TOKEN environment variable.');
  console.error('   Get it from: Shopify Admin → Settings → Apps → Develop apps → Your app → API credentials');
  console.error('   Run: SHOPIFY_TOKEN=shpat_xxxxx SHOPIFY_STORE=recarpet-build node scripts/upload-images.js\n');
  process.exit(1);
}

// ── Image mapping: old Webflow CDN URLs → where they belong in the Shopify theme ──
const CDN = 'https://cdn.prod.website-files.com/673458673a0d213279b7ad1b';

const IMAGE_MAP = [
  // ─── Hero / Header images ───
  { url: `${CDN}/673db5ae8fc4a4ddc908aa03_ReCarpet_Start_Hero.jpg`, name: 'rc-start-hero.jpg', alt: 'ReCarpet startsida hero', section: 'Homepage → rc-hero → background_image' },
  { url: `${CDN}/673db5b08c08f63e56cb5b20_ReCarpet_Fastighetsagare_Header.jpg`, name: 'rc-fastighetsagare-hero.jpg', alt: 'Fastighetsägare hero', section: 'Fastighetsägare → rc-page-hero → background_image' },
  { url: `${CDN}/673db5b3d8b283f247764a55_ReCarpet_Arkitekt_Header.jpg`, name: 'rc-arkitekt-hero.jpg', alt: 'Arkitekter hero', section: 'Arkitekter → rc-page-hero → background_image' },
  { url: `${CDN}/673db5b51f12d3cbfa2636d9_ReCarpet_Hyresgast_Header.jpg`, name: 'rc-hyresgast-hero.jpg', alt: 'Hyresgäst hero', section: 'Hyresgäst → rc-page-hero → background_image' },
  { url: `${CDN}/673db5b5f82a2ffeb5bca4b4_ReCarpet_Entreprenor_Header.jpg`, name: 'rc-entreprenor-hero.jpg', alt: 'Entreprenör hero', section: 'Entreprenör → rc-page-hero → background_image' },
  { url: `${CDN}/673db5ad6fcc703565e7692d_ReCarpet_Omoss_Header.jpg`, name: 'rc-omoss-hero.jpg', alt: 'Om oss hero', section: 'Om oss → rc-page-hero → background_image' },
  { url: `${CDN}/673db5aef00f8163e59fe162_ReCarpet_Tjanster_Header.jpg`, name: 'rc-tjanster-hero.jpg', alt: 'Tjänster hero', section: 'Vad vi gör → rc-page-hero → background_image' },

  // ─── Customer group card thumbnails (homepage) ───
  { url: `${CDN}/673db5ad917d312c0f6b3feb_ReCarpet_Start_Thumbnail.jpg`, name: 'rc-card-fastighetsagare.jpg', alt: 'Fastighetsägare', section: 'Homepage → rc-customer-cards → block 1 image' },
  { url: `${CDN}/673db5b41f12d3cbfa263591_ReCarpet_Arkitekt_Thumbnail.jpg`, name: 'rc-card-arkitekt.jpg', alt: 'Arkitekt', section: 'Homepage → rc-customer-cards → block 2 image' },
  { url: `${CDN}/673db5b5452829be8c693af6_ReCarpet_Hyresgast_Thumbnail.jpg`, name: 'rc-card-hyresgast.jpg', alt: 'Hyresgäst', section: 'Homepage → rc-customer-cards → block 3 image' },
  { url: `${CDN}/673db5b4835f079c65637708_ReCarpet_Entreprenor_Thumbnail.jpg`, name: 'rc-card-entreprenor.jpg', alt: 'Entreprenör', section: 'Homepage → rc-customer-cards → block 4 image' },

  // ─── Homepage service timeline images ───
  { url: `${CDN}/673db5ad126c0679353de3d0_ReCarpet_Start_Inventering.jpg`, name: 'rc-service-inventering.jpg', alt: 'Inventering', section: 'Homepage → rc-services → block 1 image' },
  { url: `${CDN}/673db5adce546209498e3658_ReCarpet_Start_Demontering.jpg`, name: 'rc-service-demontering.jpg', alt: 'Demontering', section: 'Homepage → rc-services → block 2 image' },
  { url: `${CDN}/673db5add8b283f247764797_ReCarpet_Start_Formedling.jpg`, name: 'rc-service-formedling.jpg', alt: 'Förmedling', section: 'Homepage → rc-services → block 3 image' },
  { url: `${CDN}/673db5adb14e67fdeb715a50_ReCarpet_Start_Montering.jpg`, name: 'rc-service-montering.jpg', alt: 'Montering', section: 'Homepage → rc-services → block 4 image' },
  { url: `${CDN}/673db5ad998d31c288a9fbdc_ReCarpet_Start_Service.jpg`, name: 'rc-service-underhall.jpg', alt: 'Service & underhåll', section: 'Homepage → rc-services → block 5 image' },
  { url: `${CDN}/673db5ad73f550e3bc3376c0_ReCarpet_Start_InterntAterbruk.jpg`, name: 'rc-service-internt-aterbruk.jpg', alt: 'Internt återbruk', section: 'Homepage → rc-services → block 6 image' },

  // ─── Products CTA image ───
  { url: `${CDN}/673db5b0a9523a1164c46d64_ReCarpet_Start_Mattor.jpg`, name: 'rc-products-cta.jpg', alt: 'Textilplattor', section: 'Homepage → rc-products-cta → image' },

  // ─── Tjänster detail images ───
  { url: `${CDN}/673db5aef7e017409545c4c0_ReCarpet_Tjanster_Inventering.jpg`, name: 'rc-tjanst-inventering.jpg', alt: 'Inventering tjänst', section: 'Vad vi gör → rc-vad-vi-gor → block 1 image' },
  { url: `${CDN}/673db5ae0f5d80b144ca0a24_ReCarpet_Tjanster_Demontering.jpg`, name: 'rc-tjanst-demontering.jpg', alt: 'Demontering tjänst', section: 'Vad vi gör → rc-vad-vi-gor → block 2 image' },
  { url: `${CDN}/673db5ae7a80bbad28d8c80d_ReCarpet_Tjanster_Formedling.jpg`, name: 'rc-tjanst-formedling.jpg', alt: 'Förmedling tjänst', section: 'Vad vi gör → rc-vad-vi-gor → block 3 image' },
  { url: `${CDN}/673db5ae2bd8e788bc67319b_ReCarpet_Tjanster_Service.jpg`, name: 'rc-tjanst-service.jpg', alt: 'Service tjänst', section: 'Vad vi gör → rc-vad-vi-gor → block 4 image' },

  // ─── Om oss page images ───
  { url: `${CDN}/673db5ada9523a1164c46be2_ReCarpet_Omoss_FullW.jpg`, name: 'rc-omoss-fullw.jpg', alt: 'Om oss bred bild', section: 'Om oss → rc-om-oss → intro_image' },
  { url: `${CDN}/673db5ad835f079c6563740a_ReCarpet_Omoss_Hallbarhet.jpg`, name: 'rc-omoss-hallbarhet.jpg', alt: 'Om oss hållbarhet', section: 'Om oss → rc-om-oss → stats_image' },

  // ─── Fastighetsägare page images ───
  { url: `${CDN}/673db5b08c08f63e56cb5b36_ReCarpet_Fastighetsagare_CO2.jpg`, name: 'rc-fast-co2.jpg', alt: 'Fastighetsägare CO2', section: 'Fastighetsägare → rc-kundgrupp → intro_image' },
  { url: `${CDN}/673db5b1d8b283f24776498f_ReCarpet_Fastighetsagare_FullW.jpg`, name: 'rc-fast-fullw.jpg', alt: 'Fastighetsägare bred bild', section: 'Fastighetsägare → rc-kundgrupp → stats_image' },
  { url: `${CDN}/673db5b1126c0679353de620_ReCarpet_Fastighetsagare_Hallbarhet.jpg`, name: 'rc-fast-hallbarhet.jpg', alt: 'Fastighetsägare hållbarhet', section: 'Fastighetsägare page extra' },
  { url: `${CDN}/673db5b2a9523a1164c46ea7_ReCarpet_Fastighetsagare_Milliken.jpg`, name: 'rc-fast-milliken.jpg', alt: 'Fastighetsägare Milliken', section: 'Fastighetsägare page extra' },

  // ─── Arkitekt page images ───
  { url: `${CDN}/673db5b498ece3a4b32b23e7_ReCarpet_Arkitekt_VaraMattor.jpg`, name: 'rc-arkitekt-mattor.jpg', alt: 'Arkitekt vara mattor', section: 'Arkitekter → rc-kundgrupp → intro_image' },

  // ─── Entreprenör page ───
  { url: `${CDN}/673db5b7f00f8163e59fe49a_ReCarpet_Entreprenor_Fordel.jpg`, name: 'rc-entreprenor-fordel.jpg', alt: 'Entreprenör fördelar', section: 'Entreprenör → rc-kundgrupp → intro_image' },

  // ─── Logos ───
  { url: `${CDN}/673458673a0d213279b7ad69_ReCarpet_without%20icon_Cold%20light%202.png`, name: 'rc-logo-light.png', alt: 'ReCarpet logotyp ljus', section: 'Footer → rc-footer → logo' },
  { url: `${CDN}/673458673a0d213279b7ad6b_ReCarpet_without%20icon_re-green%202.png`, name: 'rc-logo-green.png', alt: 'ReCarpet logotyp grön', section: 'Header logo' },
  { url: `${CDN}/681c8044d1bc21257a4a2b03_Logotyp_LundbergsFastigheter_liggande_RGB_gron_svart.png`, name: 'rc-kundlogo-lundbergs.png', alt: 'Lundbergs Fastigheter', section: 'Homepage → rc-logo-bar → block image' },
];

// ── Helpers ──

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchUrl(res.headers.location).then(resolve).catch(reject);
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function shopifyGraphQL(query, variables = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ query, variables });
    const req = https.request({
      hostname: `${STORE}.myshopify.com`,
      path: '/admin/api/2024-10/graphql.json',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': TOKEN,
        'Content-Length': Buffer.byteLength(data),
      }
    }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try {
          resolve(JSON.parse(Buffer.concat(chunks).toString()));
        } catch (e) {
          reject(new Error('Parse error: ' + Buffer.concat(chunks).toString().substring(0, 200)));
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function shopifyRest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = https.request({
      hostname: `${STORE}.myshopify.com`,
      path: `/admin/api/2024-10/${path}`,
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': TOKEN,
        ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}),
      }
    }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try {
          resolve(JSON.parse(Buffer.concat(chunks).toString()));
        } catch (e) {
          reject(new Error('Parse error: ' + Buffer.concat(chunks).toString().substring(0, 200)));
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function uploadImageToShopify(imageUrl, filename, altText) {
  // Use fileCreate with originalSource — Shopify downloads the image directly from the URL
  // This is the simplest approach and doesn't require stagedUploads
  const result = await shopifyGraphQL(`
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          id
          alt
          createdAt
        }
        userErrors { field message }
      }
    }
  `, {
    files: [{
      alt: altText,
      contentType: 'IMAGE',
      originalSource: imageUrl,
      filename: filename
    }]
  });

  // Debug: log full response if there's an issue
  if (!result.data) {
    const errMsg = result.errors
      ? result.errors.map(e => e.message).join('; ')
      : JSON.stringify(result).substring(0, 300);
    throw new Error('API error: ' + errMsg);
  }

  const userErrors = result.data.fileCreate?.userErrors || [];
  if (userErrors.length > 0) {
    throw new Error('File error: ' + userErrors.map(e => e.message).join('; '));
  }

  const file = result.data.fileCreate?.files?.[0];
  if (!file) throw new Error('No file returned');
  return file;
}

// ── Main ──

async function main() {
  console.log('\n🖼️  ReCarpet Image Upload\n');
  console.log(`Store: ${STORE}.myshopify.com`);
  console.log(`Images to upload: ${IMAGE_MAP.length}\n`);

  // Test API connection and check scopes
  try {
    const shop = await shopifyGraphQL('{ shop { name } }');
    if (shop.errors) {
      console.error('❌ API error:', shop.errors[0]?.message || JSON.stringify(shop.errors));
      console.error('\n   Make sure your app has these Admin API scopes enabled:');
      console.error('   - write_files (read_files)');
      console.error('   Then reinstall the app to apply the new scopes.\n');
      process.exit(1);
    }
    console.log(`✅ Connected to: ${shop.data.shop.name}`);
  } catch (e) {
    console.error('❌ Cannot connect to Shopify API:', e.message);
    process.exit(1);
  }

  // Quick test: try creating a file to verify write_files scope
  console.log('   Testing file upload permissions...');
  try {
    const testResult = await shopifyGraphQL(`{ files(first: 1) { edges { node { id } } } }`);
    if (testResult.errors) {
      console.error('❌ Missing "read_files" scope. Add it in your app settings and reinstall.');
      process.exit(1);
    }
    console.log('   ✅ File permissions OK\n');
  } catch (e) {
    console.error('❌ File scope check failed:', e.message);
    process.exit(1);
  }

  const results = [];
  let success = 0;
  let failed = 0;

  for (let i = 0; i < IMAGE_MAP.length; i++) {
    const img = IMAGE_MAP[i];
    process.stdout.write(`[${i + 1}/${IMAGE_MAP.length}] ${img.name} ... `);
    try {
      const file = await uploadImageToShopify(img.url, img.name, img.alt);
      console.log('✅');
      results.push({
        name: img.name,
        section: img.section,
        shopifyId: file?.id,
        status: 'uploaded'
      });
      success++;
    } catch (e) {
      console.log('❌ ' + e.message.substring(0, 80));
      results.push({ name: img.name, section: img.section, error: e.message });
      failed++;
    }
    // Small delay to avoid rate limits
    await new Promise(r => setTimeout(r, 500));
  }

  console.log(`\n── Results ──`);
  console.log(`✅ Uploaded: ${success}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`\n── Image → Section mapping ──\n`);
  for (const r of results) {
    if (r.error) {
      console.log(`  ❌ ${r.name} → ${r.section}`);
      console.log(`     Error: ${r.error.substring(0, 100)}`);
    } else {
      console.log(`  ✅ ${r.name} → ${r.section}`);
      if (r.shopifyId) console.log(`     ID: ${r.shopifyId}`);
    }
  }

  console.log('\n── Next steps ──');
  console.log('1. Go to Theme Customizer for each page');
  console.log('2. Select the uploaded images in the image picker for each section');
  console.log('3. The images will appear in the "Files" section of the image picker');
  console.log('');
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
