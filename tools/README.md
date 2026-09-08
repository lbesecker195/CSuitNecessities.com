# One-time seed scripts

These generated `data/offers.yaml`, the placeholder SVGs in `static/img/products/`,
and all 50 articles in `content/reviews/` + `content/compare/`.

**The markdown and YAML are now the source of truth. Re-running these overwrites
your edits.** They're kept only as a template if you want to bulk-add a category.

`gen_content.py` reads `catalog.json`, which `gen_products.py` writes to a temp path —
update that path before re-running.
