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
