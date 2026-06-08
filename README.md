# Doclira Website

Static Astro product site for **Doclira PDF**. It contains:

- English landing page at `/`
- Chinese landing page at `/zh/`
- English user guide at `/guide/`
- Chinese user guide at `/zh/guide/`
- Product effect images under `public/assets/`

## Local Development

```powershell
npm install
npm run dev
```

## Build

```powershell
npm run build
```

Deploy the generated Astro site to Vercel after replacing the launch fields in `src/brand.js`:

- `purchaseUrl`: Gumroad product checkout link
- `supportEmail`: customer support email address

The public website intentionally states the product limitations: Doclira PDF handles common local PDF work and lightweight text changes, but it is not advertised as full Word-style editing for every complex or scanned PDF.
