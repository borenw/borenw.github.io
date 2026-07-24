# CLAUDE.md — borenw.github.io

Guidance for Claude Code when working in this repository (Bo's Engineering Curriculum, the GitHub Pages site at https://borenw.github.io/).

## Page-number rule (REQUIRED)

**Every page on borenw.github.io has a unique, permanent "page number."**

- **Numbering is append-only.** The initial numbers were assigned in curriculum-index reading order (see the Page Registry in `index.html`). A **new page always gets the next unused number** (current max + 1) — never renumber existing pages, even when a new page is inserted earlier in the curriculum. This keeps every footer stable forever.
- **A "page"** = a hosted HTML page on the site (has a `LIVE` badge / a `borenw.github.io/...` URL). GitHub-only repos (notebooks, MATLAB, SKILL tools with no hosted page) are **not** numbered.
- **Two places must show the number, and must stay in sync:**
  1. **The page's own footer** — `Page N · Bo's Engineering Curriculum` (link the text to `https://borenw.github.io/`). For pages that live in their own repo, edit that repo's page.
  2. **The Page Registry** in this repo's `index.html` (the `#pages` section) — one row per page: number, title, link.
- When you **create or add a new page**, allocate the next number, add its footer, and add its Registry row in the same change.

## Revision rule (REQUIRED)

**The site carries a visible revision number: the `rev N` badge in `index.html`'s banner (`<span class="rev" id="siterev">`).**

- **On EVERY change you push to this repo** (editing `index.html`, adding/updating a Registry row, editing `biohacking.html` or any page/asset that lives directly in this repo), **do BOTH in the same commit:**
  1. **Increment the rev** — the `rev N` text in `<span class="rev" id="siterev">` — by exactly 1 (e.g. `rev 60` → `rev 61`). Never skip, reuse, or decrement. It's a plain monotonic counter (not a date, not a git hash). One push touching several files = one bump.
  2. **Refresh the build time** — set `data-built` on `<span class="age" id="siteage" data-built="...">` to the current UTC time in `YYYY-MM-DDTHH:MM:SSZ` form. Get it with `date -u +%Y-%m-%dT%H:%M:%SZ`. This drives both the "built N ago" badge and the live freshness self-check (`#sitecheck`, which compares it to the latest commit via the GitHub API), so the reader can tell a fresh build from a cached copy. If it's stale/wrong, the self-check will falsely nag or reassure.
- If you can't find the badges, they are the pills in the top-right of `<div class="banner">` (`.revbadges`); restore them before pushing.
- Treat this like the page-number rule: a hard requirement, done as part of the change, not an afterthought — it's how the reader (and the next Claude) can tell at a glance which build is live.

## Chart / figure rule (REQUIRED)

**Every chart, plot, or figure on any page must carry a title or a figure number** (e.g. `Figure 3 · First-order constants vs process node`). Number figures per page (Figure 1, 2, 3 …) in reading order, and give each a short descriptive title. This applies to canvas plots, SVG diagrams, embedded images used as figures — anything a reader would call "a figure." Dual-axis charts must label each y-axis with its quantity **and color-match the axis label to its curve**.

## Reply rule (REQUIRED)

**After you finish pushing page work, END the reply by stating the live link and its page number**, e.g.:

> ✅ Live: https://borenw.github.io/gm-id-estimator/ — **Page 9**

If several pages were pushed, list each link + page number.

## Site structure

- `index.html` — the curriculum home (course → chapter tables) and the **Page Registry** (`#pages`).
- `biohacking.html`, `rsa/`, `spike_prime_projects/`, `Buck_explorer_v1.ipynb` — pages/assets that live directly in this repo.
- Most tool pages live in their **own repos** under github.com/borenw and are surfaced here by link. Editing their footer means editing that repo.
- Stats strip (Courses / Live Pages / Repositories) is maintained by the site owner; update the counts when you add a page.
