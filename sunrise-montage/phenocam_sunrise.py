#!/usr/bin/env python3
"""phenocam_sunrise.py: download one year of sunrise-window photos from a PhenoCam site.

Usage:
    python3 phenocam_sunrise.py [SITE] [YEAR] [--start 04:00] [--end 09:00] [--every N]

Defaults: NEON Great Smoky Mountains tower camera (NEON.D07.GRSM.DP1.00033), year 2025,
photos taken 04:00 to 09:00 (camera time, local standard time). Photos land in
./phenocam_<SITE>_<YEAR>/ ready to load into https://borenw.github.io/sunrise-montage/

Re-running resumes: files already on disk are skipped.
Only Python 3 is needed, nothing to install.
"""
import argparse, json, os, pathlib, re, statistics, sys, threading, time, urllib.request

VERSION = "1.0.0"
BASE = "https://phenocam.nau.edu/data/archive"
UA = "sunrise-montage/" + VERSION + " (+https://borenw.github.io/sunrise-montage/)"


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def fmt_t(sec):
    if sec is None or sec != sec or sec == float("inf"):
        return "?"
    sec = int(sec)
    if sec < 60:
        return "%ds" % sec
    if sec < 3600:
        return "%dm%02ds" % (sec // 60, sec % 60)
    return "%dh%02dm" % (sec // 3600, sec % 3600 // 60)


def fmt_b(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return ("%d %s" % (n, u)) if u == "B" else ("%.1f %s" % (n, u))
        n /= 1024.0


# ---------------------------------------------------------------- timing history
class RunHistory:
    """Remembers how long previous runs took per listing and per photo on this machine."""

    def __init__(self):
        root = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
        self.path = pathlib.Path(root) / "phenocam_sunrise" / "runs.json"
        try:
            self.runs = json.loads(self.path.read_text())
        except Exception:
            self.runs = []

    def median(self, key):
        vals = [r[key] for r in self.runs if r.get(key)]
        return statistics.median(vals) if vals else None

    def save(self, **rec):
        try:
            self.runs = (self.runs + [rec])[-20:]
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.runs))
        except Exception:
            pass


# ---------------------------------------------------------------- 5-second heartbeat
class Progress:
    """Prints one status line to stderr every 5 s (counted from run start) while work runs."""

    def __init__(self, enabled, history):
        self.enabled = enabled
        self.t0 = time.time()
        self.phase, self.done, self.total = "listing", 0, 12
        self.phase_t0 = self.t0
        self.writing = None
        self.n_photos = None
        self.list_actual = None
        h = history
        self.sec_list = h.median("sec_per_listing")
        self.sec_photo = h.median("sec_per_photo")
        self.baseline = self.sec_list is not None and self.sec_photo is not None
        self.sec_list = self.sec_list or 1.5
        self.sec_photo = self.sec_photo or 0.6
        self.tty = sys.stderr.isatty()
        self.lock = threading.Lock()
        self.stop = threading.Event()
        if enabled:
            threading.Thread(target=self._loop, daemon=True).start()

    def set(self, phase=None, done=None, total=None, writing=None):
        with self.lock:
            if phase and phase != self.phase:
                self.phase, self.phase_t0 = phase, time.time()
            if done is not None:
                self.done = done
            if total is not None:
                self.total = total
            self.writing = writing

    def _loop(self):
        nxt = self.t0 + 5
        while not self.stop.wait(max(0.0, nxt - time.time())):
            self._print()
            nxt += 5

    def _print(self):
        with self.lock:
            now = time.time()
            ph, done, total = self.phase, self.done, self.total
            el = now - self.phase_t0
            rate = done / el if el > 0 and done else 0.0
            # per-item seconds for this phase: measured once there is enough of it, else history
            if ph == "listing":
                per = el / done if done >= 2 else self.sec_list
            else:
                per = el / done if done >= 20 else self.sec_photo
            phase_eta = (total - done) * per
            # overall: listing work + download work, in estimated seconds
            n_ph = self.n_photos if self.n_photos is not None else 12 * 30 * 20
            if ph != "listing" and self.list_actual is not None:
                est_list = self.list_actual
            else:
                est_list = 12 * (per if ph == "listing" else self.sec_list)
            est_dl = n_ph * (self.sec_photo if ph == "listing" else per)
            if ph == "listing":
                spent = done * per
            else:
                spent = est_list + done * per
            whole = est_list + est_dl
            ov = 100.0 * spent / whole if whole else 0
            ov_eta = max(0.0, whole - spent)
            pct = ("%.1f%%" % (100.0 * done / total)) if total else "?"
            unit = "month/s" if ph == "listing" else "photo/s"
            line = "[%s] %d/%d %s · %.2f %s · ETA %s · overall %.0f%% ETA %s%s · elapsed %s" % (
                ph, done, total, pct, rate, unit, fmt_t(phase_eta), ov, fmt_t(ov_eta),
                "" if self.baseline else " (no baseline yet)", fmt_t(now - self.t0))
            w = self.writing
            if w:
                try:
                    st = os.stat(w)
                    line += " · writing %s %s %s" % (os.path.basename(w), fmt_b(st.st_size),
                                                     time.strftime("%H:%M:%S", time.localtime(st.st_mtime)))
                except OSError:
                    pass
        if self.tty:
            sys.stderr.write("\r\033[K" + line)
        else:
            sys.stderr.write(line + "\n")
        sys.stderr.flush()

    def close(self):
        self.stop.set()
        if self.enabled and self.tty and time.time() - self.t0 >= 5:
            sys.stderr.write("\n")


# ---------------------------------------------------------------- main
def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)


def main():
    ap = argparse.ArgumentParser(description="Download one year of sunrise-window PhenoCam photos.")
    ap.add_argument("site", nargs="?", default="NEON.D07.GRSM.DP1.00033",
                    help="PhenoCam site name (default: NEON.D07.GRSM.DP1.00033, Great Smoky Mountains)")
    ap.add_argument("year", nargs="?", type=int, default=2025, help="year to download (default 2025)")
    ap.add_argument("--start", default="04:00", help="earliest photo time, HH:MM (default 04:00)")
    ap.add_argument("--end", default="09:00", help="latest photo time, HH:MM, exclusive (default 09:00)")
    ap.add_argument("--every", type=int, default=1, metavar="N", help="keep every Nth day (default 1)")
    ap.add_argument("--out", help="output folder (default phenocam_<SITE>_<YEAR>)")
    ap.add_argument("--pause", type=float, default=0.2, help="seconds between downloads (default 0.2)")
    ap.add_argument("--base", default=BASE, help=argparse.SUPPRESS)
    ap.add_argument("--no-progress", action="store_true", help="no 5-second status lines, keep the summary")
    ap.add_argument("-q", "--quiet", action="store_true", help="print nothing")
    ap.add_argument("-V", "--version", action="version", version="phenocam_sunrise " + VERSION)
    a = ap.parse_args()

    lo, hi = hm(a.start), hm(a.end)
    out = pathlib.Path(a.out or "phenocam_%s_%d" % (a.site, a.year))
    out.mkdir(parents=True, exist_ok=True)
    say = (lambda *x: None) if a.quiet else (lambda *x: print(*x, flush=True))
    hist = RunHistory()
    prog = Progress(not (a.quiet or a.no_progress), hist)
    pat = re.compile(re.escape(a.site) + r"_(\d{4})_(\d{2})_(\d{2})_(\d{2})(\d{2})(\d{2})\.jpg")
    t_run = time.time()

    # phase 1: list each month's archive folder
    todo, have, skipped_months = [], 0, []
    t_list = time.time()
    for month in range(1, 13):
        url = "%s/%s/%d/%02d/" % (a.base.rstrip("/"), a.site, a.year, month)
        try:
            html = fetch(url).read().decode("utf-8", "replace")
        except Exception as e:
            skipped_months.append(month)
            say("  %d-%02d: could not list (%s)" % (a.year, month, e))
            prog.set(done=month)
            continue
        names = set()
        for m in pat.finditer(html):
            mins = int(m.group(4)) * 60 + int(m.group(5))
            doy = time.strptime("%s-%s-%s" % m.group(1, 2, 3), "%Y-%m-%d").tm_yday
            if lo <= mins < hi and (doy - 1) % a.every == 0:
                names.add(m.group(0))
        n_new = 0
        for n in sorted(names):
            if (out / n).exists():
                have += 1
            else:
                todo.append(url + n)
                n_new += 1
        say("  %d-%02d: %d photos in window, %d to download" % (a.year, month, len(names), n_new))
        prog.set(done=month)
    sec_listing = (time.time() - t_list) / 12
    prog.list_actual = time.time() - t_list

    if len(skipped_months) == 12:
        prog.close()
        say("Could not list any month for %s %d. Check the site name and year at "
            "https://phenocam.nau.edu/webcam/ (and your internet connection)." % (a.site, a.year))
        sys.exit(2)

    # phase 2: download
    prog.n_photos = len(todo)
    prog.set(phase="download", done=0, total=len(todo))
    new = failed = 0
    nbytes = 0
    t_dl = time.time()
    for i, url in enumerate(todo):
        dest = out / url.rsplit("/", 1)[1]
        part = dest.with_name(dest.name + ".part")
        prog.set(done=i, writing=str(part))
        ok = False
        for attempt in (1, 2):
            try:
                with fetch(url) as r, open(part, "wb") as f:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                os.replace(part, dest)
                nbytes += dest.stat().st_size
                ok = True
                break
            except Exception as e:
                err = e
                time.sleep(1.0 * attempt)
        if ok:
            new += 1
        else:
            failed += 1
            try:
                part.unlink()
            except OSError:
                pass
            say("  failed %s (%s)" % (dest.name, err))
        if a.pause:
            time.sleep(a.pause)
    prog.set(done=len(todo), writing=None)
    prog.close()

    if todo:
        hist.save(sec_per_listing=sec_listing, sec_per_photo=(time.time() - t_dl) / len(todo),
                  n=len(todo), site=a.site, when=int(time.time()))
    say("done: %d new photos (%s), %d already had, %d failed, %d month(s) not listed -> %s/  in %s"
        % (new, fmt_b(nbytes), have, failed, len(skipped_months), out, fmt_t(time.time() - t_run)))
    say("next: open https://borenw.github.io/sunrise-montage/ and pick the photos in %s/" % out)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninterrupted. Run the same command again to resume.\n")
        sys.exit(130)
