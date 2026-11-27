# Keeping search information up to date

SEO means helping search engines understand the website and helping people find useful pages. Moving HTML into smaller files does not hide it from Google: Flask joins those files into a full page before sending it.

## What each page should cover

| Page | Main topic |
| --- | --- |
| Homepage | Visa and study consultants in Sheikhupura |
| `/uk` | UK universities and UK study visa guidance |
| Other destination pages | Study options and study visa guidance for that destination |
| IELTS and PTE pages | Preparation classes in Sheikhupura |

Use the correct spelling, Sheikhupura. Write naturally. Do not repeat keywords or make copies of the same page for different towns. Mention only services the business offers. UK study visa guidance does not mean tourist or work visa services are also offered.

We have not measured keyword search numbers. Use Google Search Console or Keyword Planner when choosing topics based on search demand.

## Where to change things

| Change | File |
| --- | --- |
| Page title and search description | The page's main file in `templates/` |
| Visible page text | The page section in `templates/partials/` |
| Business introduction and service text | `templates/partials/home/about.html` and `templates/partials/home/services.html` |
| Footer contact details | `templates/partials/layout/footer.html` |
| Business details for search engines | `templates/base.html` |
| Pages listed in the sitemap | `backend/data/sitemap.py` |

Keep the business name, address and phone the same on the website and Google Business Profile. Only add real hours, reviews, locations and services.

## When adding or moving a page

1. Give it a clear title and short description.
2. Keep one main URL for it. The `canonical` link tells search engines which URL that is.
3. Add it to the sitemap if it should appear in search.
4. Link to it from a useful existing page.
5. Keep old links working. If a page moves, use a permanent redirect, called a 301.
6. Run `python -m unittest discover -s tests -v`.

The SEO checks open pages and check their titles, descriptions, main URLs, search data and local links. The saved homepage results were updated when local SEO content was added.

## After putting changes online

- Check the live page with Google's Rich Results Test.
- Use Search Console to check whether Google can read the page.
- Submit the sitemap: [visaculture.com/sitemap.xml](https://visaculture.com/sitemap.xml).
- Watch which searches bring people to the site and whether visits lead to enquiries.
- Keep the real Google Business Profile up to date with the correct contact details, hours, photos and genuine reviews.

These online account tasks are separate from editing local code.

## About rankings

No code change can promise a top Google position. Local results depend on how well the business matches a search, how close it is to the person searching, and how well known it is. Repeating “near me” does not change the office location.

Build useful pages and keep business details accurate. Do not invent results, reviews or visa success claims.

Read Google's [local ranking advice](https://support.google.com/business/answer/7091) and [business search-data guide](https://developers.google.com/search/docs/appearance/structured-data/local-business).
