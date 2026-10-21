# 🌅 Sunrise Sine Montage

Live page: https://borenw.github.io/sunrise-montage/ (Page 58)

One year of webcam photos laid out with **days across** and **time of morning down**. Night cells are dark and day cells are lit, so the boundary is the sunrise time, which traces a sine wave over the year (period 365 days, amplitude growing with latitude).

The page runs entirely in the browser, works on a phone, and has a built-in simulated demo for eight locations:

| # | 📍 Preset | 🌄 Scene | ⏱️ Demo rows |
|---|---|---|---|
| 1 | Great Smoky Mountains NP | layered ridges | 7.5 min |
| 2 | Acadia NP | ocean sunrise | 7.5 min |
| 3 | Grand Canyon NP | rim and buttes | 7.5 min |
| 4 | Big Bend NP | desert peaks | 7.5 min |
| 5 | Everglades NP | flat sawgrass and palms (nearly flat wave) | 7.5 min |
| 6 | Denali NP | snow peak with alpenglow (huge wave) | 7.5 min |
| 7 | NEON GRSM tower, Smokies | forest canopy | 15 min (matches camera) |
| 8 | NEON RMNP tower, Rocky Mountain NP | snowy peaks over conifers | 15 min (matches camera) |

## 📥 Download a real year of photos

`phenocam_sunrise.py` downloads one year of morning photos from any [PhenoCam](https://phenocam.nau.edu/webcam/) site. It needs only Python 3, nothing to install.

**One line: install, print the version, then download NEON Great Smoky Mountains for 2025**

```bash
mkdir -p ~/bin && curl -fsSL https://borenw.github.io/sunrise-montage/phenocam_sunrise.py -o ~/bin/phenocam_sunrise.py && chmod +x ~/bin/phenocam_sunrise.py && python3 ~/bin/phenocam_sunrise.py -V && python3 ~/bin/phenocam_sunrise.py NEON.D07.GRSM.DP1.00033 2025
```

**Rocky Mountain NP instead**

```bash
python3 ~/bin/phenocam_sunrise.py NEON.D10.RMNP.DP1.00033 2025
```

**Run again later** (resumes, skips photos already on disk)

```bash
python3 ~/bin/phenocam_sunrise.py NEON.D07.GRSM.DP1.00033 2025
```

Photos land in `phenocam_<SITE>_<YEAR>/`. Then open the live page, choose the matching NEON preset, and use **Pick folder** (computer) or **Pick photos** (phone, from the Files app).

### Options

| ⚙️ Option | 📝 What it does | 🔢 Default |
|---|---|---|
| `SITE` | PhenoCam site name | `NEON.D07.GRSM.DP1.00033` |
| `YEAR` | Calendar year | `2025` |
| `--start`, `--end` | Time window, camera time (local standard time) | `04:00`, `09:00` |
| `--every N` | Keep every Nth day | `1` |
| `--out DIR` | Output folder | `phenocam_SITE_YEAR` |
| `--pause S` | Seconds between downloads | `0.2` |
| `--no-progress` | Hide the 5-second status line, keep the summary | off |
| `-q` | Print nothing | off |
| `-V` | Print the version | |

While it runs, a status line on stderr every 5 seconds shows the phase, count and percent, rate, ETA, overall percent and ETA (anchored to past runs cached in `~/.cache/phenocam_sunrise/`), and the size of the file being written.

### Size and time

A full year at 15 minutes from 04:00 to 09:00 is about 7,000 photos, roughly 1 to 3 GB. Use `--every 2` to halve it; the page's default columns are every 2 days anyway.

## 🛠️ Notes

* File names carry the date and time (`SITE_YYYY_MM_DD_HHMMSS.jpg`); the page reads them, so keep the names.
* Finer rows than the camera (7.5 min with a 15 min camera) are filled from the nearest photo when **Fill gaps** is on.
* The script was tested against a mock of the PhenoCam archive layout. If the first month prints `could not list`, check the site name at https://phenocam.nau.edu/webcam/.
