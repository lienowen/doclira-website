# Doclira Website Launch Checklist

## Before Publishing

1. Create the Gumroad product and obtain the checkout URL.
2. Choose a customer support email address.
3. Edit `src/brand.js` and fill `purchaseUrl` and `supportEmail`.
4. Confirm the English and Chinese pages use the final price and delivery policy.
5. Run `npm run build`.

## Vercel Setup

1. Push the `website` project to a GitHub repository.
2. Import the repository in Vercel.
3. Select Astro if prompted; the build command is `npm run build`.
4. Deploy and connect the final domain.
5. Use the deployed `/zh/guide/` link in Chinese automatic delivery messages.
6. Use the deployed `/guide/` link in Gumroad delivery instructions.

## Pages Included

- `/` English product page
- `/guide/` English user guide
- `/zh/` Chinese product page
- `/zh/guide/` Chinese user guide
