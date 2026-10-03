# Quest Hauling website

Static, SEO-focused site for Quest Hauling's 16-yard dumpster rental ($550 / 7 days / 1.5 tons) in Orange County and Los Angeles County.

## Build

```
python3 build.py
```

This writes the finished site to `public/`. Upload `public/` to any static host (Netlify, Cloudflare Pages, Vercel, GitHub Pages). No dependencies are needed beyond Python 3.

## Before going live

Edit the `BUSINESS` block at the top of `build.py`, then rebuild:

- `domain`: the real domain. It's used for canonical URLs, the sitemap and structured data.
- `phone`: the real phone number. It's currently the placeholder `555-555-5555`.
- `form_action`: quote requests go to questhauling1@gmail.com through FormSubmit. The first submission sends a one-time activation email to that inbox, which you must confirm.

## Pages

- `/`: home page
- `/dumpster-rental/orange-county/`, `/dumpster-rental/los-angeles-county/`: county pages
- `/dumpster-rental/<city>/`: Huntington Beach, Newport Beach, Costa Mesa, Fountain Valley, Irvine, Santa Ana, Anaheim, Long Beach

To add a city, add an entry to `CITIES` in `build.py` with its own intro, local tip, neighborhoods and ZIP codes. Keep each city's text unique so the pages aren't treated as duplicates.

## SEO built in

- A unique title, meta description and canonical URL on every page
- Open Graph and Twitter tags with a 1200×630 share image
- JSON-LD structured data: LocalBusiness (with service area and a $550 Offer), FAQPage, BreadcrumbList, WebSite and WebPage
- One H1 per page, semantic sections, and internal links between city and county pages
- `sitemap.xml` and `robots.txt`
- Inline CSS and SVG graphics instead of photos, for fast loading
- A mobile tap-to-call bar, labelled form fields and keyboard focus styles
