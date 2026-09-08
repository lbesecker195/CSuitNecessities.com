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
  amazonTag = "csuitnec-20"      # ← change this. That's the whole job.
```

Every button, text link, product image, comparison-table cell, sidebar card and
sticky bar builds its URL through [`layouts/partials/amzn.html`](layouts/partials/amzn.html),
which reads `amazonTag`. Nothing else references a tag. Even a bare
`https://www.amazon.com/...` link pasted into markdown gets the tag appended
automatically by the link render hook.

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
| `{{< img-link src="…" offer="key" caption="…" cue="…" >}}` | explicit clickable image |
| `{{< comparison offers="a,b,c" rows="Best for,Weight,…" >}}` | comparison table, everything linked |
| `{{< pros-cons >}}` … `vs` … `{{< /pros-cons >}}` | two-column pros/cons |
| `{{< callout type="tip\|deal\|warn" >}}…{{< /callout >}}` | highlighted aside |

Plain markdown works too — `![alt](/img/products/x.svg "Caption")` auto-links to the
page's product.

**Dates must be in the past** or Hugo will hide the page as future content.

## 6. Analytics

`assets/js/engagement.js` fires to GA4 / GTM / Plausible / PostHog:

- `affiliate_click` — with `affiliate`, `slot` (hero-image, side, sticky, cmp-button, in-content…), `surface` (`image` vs `text`) and `anchor_text`
- `image_click`, `scroll_depth`, `read_complete`, `time_on_page`

That `surface` field is how you A/B whether images or anchor text are earning the clicks.

## 7. Placeholder images

`static/img/products/*.svg` are generated placeholders — brand, product name, tagline
on a category-colored card. **Replace them with real product photography** (same
filenames, or update `image:` in `offers.yaml`). Note Amazon's Associates terms on
product-image usage; use the Product Advertising API or your own photos.

## 8. Run

```bash
hugo server --source site
```

## 9. Seed scripts

`tools/gen_products.py` and `tools/gen_content.py` are the one-time generators that
produced `data/offers.yaml`, the placeholder SVGs and all 50 articles. The markdown
and YAML are now the source of truth — **re-running the scripts overwrites them.**
They're kept only as a template if you want to bulk-add another category.
