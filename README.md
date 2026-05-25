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

Deploy the generated Astro site to Vercel. Current launch settings in `src/brand.js`:

- `purchaseUrl`: `https://taixianglumark.gumroad.com/l/doclira-pdf`
- `supportEmail`: `taixianglumark@gmail.com`

The public website intentionally states the product limitations: Doclira PDF handles common local PDF work and lightweight text changes, but it is not advertised as full Word-style editing for every complex or scanned PDF.
