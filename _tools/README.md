# _tools — page generators

Helper scripts that write parts of the converter pages. They are not part of the website:
GitHub Pages skips folders whose names start with `_`, so nothing here is published.

Run them from the repo root with Python 3 (no extra packages needed):

```
python _tools/content.py
python _tools/pagebar.py
```

Both scripts are safe to re-run: each one replaces its own marked block in the pages and leaves
everything else alone. Commit the changed `.html` files afterwards as usual.

## content.py — guides, tables and FAQs

Writes the content under each converter, between these markers in each page:

- `<!-- content:start -->` … `<!-- content:end -->` — the guide, tables and FAQ cards
- `<!-- jsonld:start -->` … `<!-- jsonld:end -->` — FAQ structured data in `<head>`

To change text, a table row or an FAQ, edit that page's entry in the `PAGES` dictionary
(for example `PAGES['cooking']`), then re-run the script. Don't hand-edit the HTML between
the markers: the next run overwrites it.

Table values are calculated from conversion factors at the top of each page's section in the
script (for example `LB, OZ, ST` for weight). Keep them in step with the factors in the page's own
converter script so the tables and the converter agree.

## pagebar.py — sticky section bar

Writes the bar under the site nav (page title + section shortcuts) between
`<!-- pagebar:start -->` and `<!-- pagebar:end -->`. It reads the title from each page's `<h1>`.
Run it after adding a new converter page, or after `content.py` if section ids change.

## Adding a new converter page

1. Build the page (follow the existing page pattern, nav, footer, canonical tag).
2. Add a `PAGES['<name>']` entry in `content.py` and run it.
3. Run `pagebar.py`.
4. Add the page to the nav on every page, the homepage grid and `sitemap.xml`.
