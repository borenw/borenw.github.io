# CLAUDE.md — borenw.github.io

> **If the user mentioned `borenw.github.io` — in any form ("the site", "my page", "the
> curriculum", or a pasted URL) — read this whole file before your first edit.** The same
> reminder is repeated as a comment at the top of `index.html`, because it kept being missed.
> Every rule below marked REQUIRED is a rule the user has already had to repeat.

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

## Tool-repo install rule (REQUIRED)

**Every single-file tool repo in this account installs the same way: save one ZIP, paste one
command, paste one more to run it.** The user should never have to correct this again — apply it
without being asked, in the tool's own repo, whenever you create or change one.

The README must open with this three-step block, adapted only in the repo name and script name:

- **0 · Download** — the user clicks `Code ▾ → Download ZIP` (or the `<repo>-main.zip` link in the
  README) and it lands in `~/Downloads`. No renaming, no unpacking by hand.
- **1 · Paste this** — unpacks into `~/bin` and prints the version, so the paste proves itself:

  ```bash
  mkdir -p ~/bin && unzip -jo "`ls -t ~/Downloads/<repo>-main*.zip | head -1`" "*/<script>.py" -d ~/bin && chmod +x ~/bin/<script>.py && python3 ~/bin/<script>.py -V
  ```

- **2 · Paste this** — the run command with the user's own path:

  ```bash
  python3 ~/bin/<script>.py <their file> --open
  ```

Why each piece, so it does not get "simplified" away:

- `ls -t … | head -1` picks the newest download, so `…main (1).zip` still works and **re-pasting
  step 1 is how you update**.
- `unzip -jo` flattens and overwrites — no nested folder, no stale copy.
- The backtick-in-double-quotes form runs unchanged in **bash, zsh and tcsh/csh**. The EDA servers
  here default to tcsh; a `$(...)` form would break there.
- Ending on `-V` makes the install its own test, so **every tool script must accept `-V` /
  `--version`**.
- Nothing outside `~/bin` is touched, so `rm ~/bin/<script>.py` uninstalls it.

Do **not** offer a different install as the main route — no `git clone`, no `pip install`, no
`setup.py`, no installer script. The `curl` one-liner (public repos) and the `scp`-to-server note
belong underneath as `<sub>` sub-points. **Verify the paste end-to-end against the live archive URL
before claiming it works** (download the real ZIP, run the real command).

The reader-facing copy of this convention lives in `index.html` under `#install`
("📦 Tool Install Convention"); keep the two in sync when either changes.

## Long-running CLI rule — status every 5 seconds (REQUIRED)

**A tool in this account must never look hung.** The user has sat through a 500-second parse
with nothing on screen, unable to tell a slow run from a stuck one. Any CLI you write or touch
here reports progress, without being asked.

Any phase that can run longer than a few seconds prints **one line to stderr every 5 seconds**,
carrying all four of:

1. **Which phase, and how far through it** — a real percentage against a real total (stream
   bytes, records, cells, shapes, output bytes). Never invent one: if the total is genuinely
   unknowable, print what has been done so far and the elapsed time and *no* percentage.
2. **The rate and the ETA for that phase.**
3. **The overall percentage and ETA for the whole run**, weighted across phases and anchored to
   **what previous runs actually took on this machine** — keep a small timing cache under
   `~/.cache/<tool>/` (honour `XDG_CACHE_HOME`), predict an exact repeat from its own last run
   and anything else from the median seconds-per-input-byte, correct it as the run goes, and say
   plainly when there is no baseline yet.
4. **For a phase writing a file: that file's size and timestamp on disk** as it grows, so "is it
   still writing?" is answered by looking at the line.

Mechanics that are part of the rule, because getting them wrong is how it fails quietly:

- Measure the 5 s **from the start of the run, not the start of the phase** — otherwise a long
  run made of short phases goes silent at every phase boundary.
- Print nothing until the first 5 s are up, so short runs stay silent.
- **stderr only.** stdout stays the pasteable summary, so `> report.txt` and `| mail` are
  unaffected. Rewrite in place on a tty; append whole lines when redirected to a log.
- Offer `--no-progress` (keep the summary, drop the heartbeat) and `-q` (drop both).

Copy the shape from a tool that already does it rather than inventing another:
`borenw/gds-dashboard` (`gds_dashboard.py` — `Progress` / `Run` / `RunHistory`) or
`borenw/chip-review-report` (`chip_review.py` — `Progress`).

**And if it is slow, profile it before explaining it away.** On gds-dashboard that was worth
2.4x on a 4.2-million-record parse: read the stream in blocks rather than per record, no
throwaway string formatting per record (`RT.get(t, "UNKNOWN_%02X" % t)` formats one for every
record, found or not), a fast path for the shape that dominates real layouts (axis-aligned
rectangles), and `-j` to put one file on each core. Report the before and after honestly.

The reader-facing summary of this and the install rule lives in `index.html` — the install one
under `#install`, this one only in the comment at the top of the file. Keep all three in sync.

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
