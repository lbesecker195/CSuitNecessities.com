# C-Suit Necessities — layout & content guide

A Hugo site built to do two things at once:

1. **Maximize CTR on images and anchor text** (every product image is an affiliate link).
2. **Keep readers on the page** long enough to click something.

50 articles ship with it: 40 single product reviews + 10 head-to-head comparisons,
across 10 categories. All products are on Amazon.

---

## 1. Swapping the affiliate ID — one line

```toml
# hugo.toml
[params]
  amazonTag = "loganbesecker-20"      # ← change this. That's the whole job.
```

Every button, text link, product image, comparison-table cell, sidebar card and
sticky bar builds its URL through [`layouts/partials/amzn.html`](layouts/partials/amzn.html),
which reads `amazonTag`. Nothing else references a tag. Even a bare
`https://www.amazon.com/...` link pasted into markdown gets the tag appended
automatically by the link render hook.

**One exception:** an `amzn.to` SiteStripe short link (as used by the landing page in
[§10](#10-landing-pages)) has its tag baked in by Amazon, so `amazonTag` does not touch it.
Change those by editing the link itself.

## 2. Products: `data/offers.yaml`

56 entries (40 reviewed products + 16 comparison-only contenders). Each looks like:

```yaml
saddleback-briefcase:
  name: Saddleback Leather Thin Front Pocket Briefcase
  brand: Saddleback Leather Co.
  domain: amazon.com
  asin: ""                                  # ← see below
  search: Saddleback Leather Thin Front Pocket Briefcase
  rating: "4.8"
  tagline: Full-grain boot leather, zero zippers to break
  cta: Check Price on Amazon
  image: /img/products/saddleback-briefcase.svg
  bullets: [ ... ]                          # shown in the in-content offer card
  compare: { Best for: ..., Weight: ..., ... }   # rows in comparison tables
  deal: 100-year leather — often ships with a free hobo bag
  reviewRef: /reviews/saddleback-briefcase
```

**ASIN vs search.** Every product currently has `asin: ""`, so links resolve to a
*tagged Amazon search* for the `search:` string. That works and tracks right now,
with zero risk of pointing at the wrong item. As you confirm each product's ASIN,
paste it into `asin:` and that product's links switch to the direct product page
(better conversion). No other change needed.

## 3. Where the clicks come from

Every **single review** page carries, automatically:

| Surface | Count | Source |
|---|---|---|
| Clickable product images → Amazon | 5 | hero, in-content offer card, in-content figure, sidebar, sticky bar |
| Affiliate text links in prose | 4 | `{{< buy >}}` shortcodes, first one auto-highlighted amber |
| Affiliate buttons | 5 | verdict box, offer card, inline CTA, final CTA, sidebar + sticky |
| Internal links (dwell) | 6+ | related cards, prev/next, category, breadcrumbs |

Every **comparison** page adds 4 clickable product thumbnails in the table header,
4 product-name links, and 4 per-column buy buttons.

### How images become links
`layouts/_default/_markup/render-image.html` wraps *every* in-content image in the
page's product link, adds a hover cue pill ("Check price on Amazon →"), zoom-on-hover
and a `data-cta` slot for analytics. You never have to write the link.

### How anchor text becomes a money link
`layouts/_default/_markup/render-link.html` rewrites outbound links: any `amazon.*`
host gets `rel="sponsored nofollow noopener"`, a new tab, the affiliate tag, an
external-link icon, and `data-affiliate`/`data-cta` attributes. The **first** money
link on the page also gets an amber highlight (`params.firstLinkEmphasis`).

## 4. Dwell-time features

Reading-progress bar · scroll-spy sticky TOC · sidebar product card · "Executives who
read this also compared…" related grid · prev/next in section · FAQ accordions ·
category cross-links · back-to-top. All automatic.

Money links open in a **new tab** (`params.affiliateNewTab`), so a click doesn't end
the session.

## 5. Writing a new review

```bash
hugo new reviews/my-product.md --kind review
```

Add the product to `data/offers.yaml` first, then set `offer = "my-product"` in the
front matter — that single key drives the hero link, sidebar, sticky bar, final CTA
and every unlinked image on the page.

Shortcodes:

| Shortcode | What it does |
|---|---|
| `{{< key-takeaways offer="key" >}}…{{< /key-takeaways >}}` | verdict box + early buy button |
| `{{< buy "key" >}}anchor text{{< /buy >}}` | inline affiliate text link |
| `{{< offer-card "key" >}}` | big clickable image + bullets + button |
| `{{< cta "key" >}}` | button + deal note |
| `{{< img-link offer="key" caption="…" >}}` | clickable product photo (image pulled from `offers.yaml`; add `src="…"` to override) |
| `{{< comparison offers="a,b,c" rows="Best for,Weight,…" >}}` | comparison table, everything linked |
| `{{< pros-cons >}}` … `vs` … `{{< /pros-cons >}}` | two-column pros/cons |
| `{{< callout type="tip\|deal\|warn" >}}…{{< /callout >}}` | highlighted aside |

Plain markdown images work too — `![alt](url "Caption")` auto-links to the page's product.

**Dates must be in the past** or Hugo will hide the page as future content.

## 6. Analytics

`assets/js/engagement.js` fires to GA4 / GTM / Plausible / PostHog:

- `affiliate_click` — with `affiliate`, `slot` (hero-image, side, sticky, cmp-button, in-content…), `surface` (`image` vs `text`) and `anchor_text`
- `image_click`, `scroll_depth`, `read_complete`, `time_on_page`

That `surface` field is how you A/B whether images or anchor text are earning the clicks.

## 7. Images

Every product's lead photo lives in **one place**: the `image` field in
`data/offers.yaml`. `layouts/partials/page-photo.html` resolves it for the hero,
the in-content `img-link`, cards, the sidebar, the sticky bar and `og:image` — so
changing one line updates every surface.

**Current photos are editorial stock from Unsplash**, not product shots. Each carries
the photographer + Unsplash credit the API licence requires (rendered by
`partials/photo-credit.html`). They're contextual — a leather-briefcase scene on the
Saddleback review, not the Saddleback itself.

- `tools/fetch_unsplash.py` — pulls a photo per product. Needs `UNSPLASH_ACCESS_KEY`
  (env var, never committed). Resumable: skips products that already have a `photoId`;
  `--force` re-fetches. De-dupes so no two products share an image. Edit the `QUERY`
  dict to change what a product searches for, blank its `photoId` in `offers.yaml`,
  and re-run just that key: `python3 tools/fetch_unsplash.py sony-xm5`.
- `tools/fetch_unsplash_all.sh` — runs the above in passes, sleeping out the
  50-req/hour demo-app rate limit. A registered production app raises that ceiling.

**To use real product photos instead:** generate image links from Amazon SiteStripe
(Associates dashboard → the product → Get Link → Image), paste the URL into that
product's `image:` in `offers.yaml`, and blank its `photoId`/`photoCredit` so no
Unsplash credit renders. Or use the Product Advertising API once you qualify.
`static/img/products/*.svg` remain as the fallback if `image:` is ever empty.

## 8. Run

```bash
hugo server --source site
```

## 9. Seed scripts

`tools/gen_products.py` and `tools/gen_content.py` generated `data/offers.yaml`, the
fallback SVGs and all 50 articles. The markdown and YAML are the source of truth now —
**re-running overwrites them**, though `gen_products.py` preserves `asin`, `image` and
the `photo*` fields so a re-run won't wipe your fetched photos. Kept as a template for
bulk-adding a category.

## 10. Landing pages

A chrome-free, single-goal page: no site header or footer nav, so nothing competes with the
click. Live example: [`content/mcp-server-optimization-book.md`](content/mcp-server-optimization-book.md)
→ `/mcp-server-optimization-book/`.

**To make another one:** copy that file, change the front matter, done. Nothing to add to
the layout. Set `layout = "landing"` and:

| front matter | what it does |
|---|---|
| `affiliateUrl` | **The one link** behind every button, image and text link. An `amzn.to` short link works as-is. Delete it to fall back to `amazon.com/dp/<asin>?tag=<amazonTag>` |
| `asin` | Used only for that fallback |
| `image`, `imageAlt`, `imageWidth/Height` | The clickable hero + final-CTA image, the sticky-bar thumbnail, and `og:image`. Put the file in `static/img/` |
| `eyebrow`, `headline`, `subhead`, `ctaText`, `ctaNote` | Hero copy and the button label |
| `problemTitle`, `problemBody`, `pillars[]` (`icon` = `search`\|`shield`\|`bolt`), `inlineLead`, `inlineCta` | The three-card section and the highlighted text link under it |
| `audienceTitle`, `audience[]` | Checklist section (has its own button) |
| `faqTitle`, `faq[]` | Accordion; also emits FAQ schema |
| `finalTitle`, `finalText`, `stickyTagline` | Bottom CTA block and the sticky bar |
| `pageTitle` | Overrides the `<title>`/`og:title` (otherwise `Title · <site name>`) |

Markdown under the front matter is rendered as an extra free-form section (empty = skipped).

**Promoting it elsewhere (links go STRAIGHT to Amazon, not to the landing page):**

- **Homepage "This month's picks":** in `content/_index.md`, add the page path to `topPicks`
  (`"/mcp-server-optimization-book"`). A plain key is a product from `offers.yaml`; a `/path` is a
  landing page. The card's image and button both use the page's `affiliateUrl`.
- **Top menu:** in `hugo.toml`, a `[[menus.main]]` entry with `pageRef = "<page path>"` and
  `[menus.main.params] affiliate = true` shows the entry's `name` as the anchor text but links
  to that page's `affiliateUrl` (new tab, `sponsored`). The nav is hidden below 960px by the
  site's responsive CSS, so on phones only the homepage card is visible.
- Both are resolved by `layouts/partials/page-affiliate.html`, so **changing `affiliateUrl` in the
  landing page's front matter updates the landing page, the card and the menu at once.**
- Card tuning in the landing front matter: `pickTagline`, `pickImagePosition` (CSS
  `object-position` for the 16:10 crop), `pickHideCue = true` (drops the "…on Amazon →" pill,
  which is always visible on touch screens and would otherwise cover text baked into the image).

**Tracking:** each link carries a `data-cta` slot (`lp-hero-image`, `lp-hero-button`,
`lp-inline-link`, `lp-audience-button`, `lp-final-image`, `lp-final-button`, `lp-sticky-image`,
`lp-sticky`), so `affiliate_click` events say which one earned the click and whether it was an
`image` or `text` surface.

**Compliance:** the exact Amazon statement ("As an Amazon Associate I earn from qualifying
purchases.") sits directly under the hero and final buttons and in the footer. Override the
wording site-wide with `[params].associateStatement`.

**Gotcha (this bit us):** the layout drops the site header via a `{{ define "header" }}` override,
and Go silently ignores an *empty* `define`, so the override must contain something (it holds an
HTML comment). Mind this if you add more overridable blocks to `baseof.html`.
