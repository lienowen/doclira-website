# Doclira Website Launch Checklist

## Before Publishing

1. Confirm the Gumroad checkout URL opens correctly: `https://taixianglumark.gumroad.com/l/doclira-pdf`.
2. Confirm support mail can receive customer questions: `lienowen@outlook.com`.
3. Confirm `src/brand.js` still contains the final purchase URL and support email.
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
