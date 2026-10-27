"""Daily money card: USD/ILS from Bank of Israel -> HTML design -> PNG (headless Chrome/Edge).
Usage: python money_card.py [out.png]"""
import csv
import io
import math
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from string import Template

import requests

BRAND = "כסף בפשטות"
URL = ("https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/"
       "?c%5BDATA_TYPE%5D=OF00&c%5BBASE_CURRENCY%5D=USD&lastNObservations=30&format=csv")

BROWSERS = [
    "chrome", "google-chrome", "chromium", "chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def fetch_series():
    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    return [(x["TIME_PERIOD"], float(x["OBS_VALUE"])) for x in rows]


def guilloche(cx, cy, R, r, d, color, op, width=0.7):
    pts = []
    k = (R - r) / r
    for i in range(0, 3600):
        t = i * math.pi / 180 * 0.5
        x = (R - r) * math.cos(t) + d * math.cos(k * t)
        y = (R - r) * math.sin(t) - d * math.sin(k * t)
        pts.append(f"{cx + x:.1f},{cy + y:.1f}")
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" opacity="{op}"/>')


def chart_svg(values, w=1080, h=250):
    lo, hi = min(values), max(values)
    pad = (hi - lo) * 0.12 or 0.01
    lo, hi = lo - pad, hi + pad
    n = len(values)
    xs = [i / (n - 1) * w for i in range(n)]
    ys = [h - (v - lo) / (hi - lo) * h for v in values]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area = f"0,{h} {line} {w},{h}"
    lx, ly = xs[-1] - 26, ys[-1]
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2E7F78" stop-opacity=".75"/><stop offset="1" stop-color="#0B1F24" stop-opacity="0"/>
  </linearGradient></defs>
  <polygon points="{area}" fill="url(#g)"/>
  <polyline points="{line}" fill="none" stroke="#E6F2E4" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
  <line x1="{lx:.1f}" y1="0" x2="{lx:.1f}" y2="{ly:.1f}" stroke="#FF5A3C" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/>
  <circle cx="{lx:.1f}" cy="{ly:.1f}" r="26" fill="#FF5A3C" opacity=".22"/>
  <circle cx="{lx:.1f}" cy="{ly:.1f}" r="12" fill="#FF5A3C"/>
</svg>'''


def meaning(change_pct, rate):
    if change_pct <= -0.05:
        return ("הדולר נחלש מול השקל.",
                "כל מה ששולמים בדולרים נעשה זול יותר: טיסות, אתרים בחו״ל, ציוד מיובא. "
                "מי שמרוויח בדולרים, יצואנים ועובדי הייטק, מקבל פחות שקלים על אותו שכר.")
    if change_pct >= 0.05:
        return ("הדולר התחזק מול השקל.",
                "קניות בחו״ל וחופשות יקרות יותר. מי שמרוויח בדולרים מקבל יותר שקלים, "
                "ויבואנים עשויים להעלות מחירים בהמשך.")
    return ("השער כמעט לא זז.",
            "יום יציב. כשהשער רגוע, קל יותר לתכנן טיסה או קנייה מחו״ל בלי הפתעות.")


HTML = Template("""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@700;900&family=Heebo:wght@400;500;800&display=swap');
:root{--ink:#0B1F24;--line:#1D4B4E;--paper:#E6F2E4;--coral:#FF5A3C;--mute:#8FB0AA}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:var(--ink);color:var(--paper);font-family:'Heebo',sans-serif;position:relative;overflow:hidden}
.rosettes{position:absolute;inset:0}
.chart{position:absolute;left:0;bottom:380px;width:1080px;height:250px}
.unitrow{display:flex;justify-content:space-between;align-items:center;margin-top:8px}
.top{position:absolute;top:72px;right:72px;left:72px;display:flex;justify-content:space-between;align-items:baseline}
.brand{font-weight:800;font-size:38px;letter-spacing:.5px}
.issue{font-family:'Frank Ruhl Libre',serif;font-weight:700;font-size:30px;color:var(--mute);direction:ltr}
.hero{position:absolute;top:170px;right:72px;left:72px}
.label{font-size:40px;font-weight:500;color:var(--mute);margin-bottom:6px}
.num{font-family:'Frank Ruhl Libre',serif;font-weight:900;font-size:330px;line-height:.95;direction:ltr;text-align:right;letter-spacing:-6px}
.unit{font-size:44px;font-weight:500}
.pill{display:inline-block;font-weight:800;font-size:40px;color:var(--ink);background:var(--coral);padding:8px 26px 10px;border-radius:60px;direction:ltr}
.pill small{font-weight:500;font-size:30px;margin-inline-start:10px}
.range{position:absolute;right:72px;left:72px;top:712px;display:flex;justify-content:space-between;font-size:30px;color:var(--mute);direction:ltr}
.range b{font-family:'Frank Ruhl Libre',serif;font-weight:700;color:var(--paper);font-size:34px}
.card{position:absolute;right:0;left:0;bottom:0;height:380px;background:var(--paper);color:var(--ink);padding:56px 72px 0}
.card h2{font-weight:800;font-size:54px;line-height:1.15;margin-bottom:18px}
.card p{font-size:36px;line-height:1.38;font-weight:400;max-width:900px}
.src{position:absolute;bottom:34px;right:72px;left:72px;font-size:26px;color:#3F6661;display:flex;justify-content:space-between}
</style></head><body>
<svg class="rosettes" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg">$rosettes</svg>
<div class="chart">$chart</div>
<div class="top"><div class="brand">$brand</div><div class="issue">$issue</div></div>
<div class="hero">
  <div class="label">שער הדולר היום</div>
  <div class="num">$rate</div>
  <div class="unitrow"><div class="unit">שקלים לכל דולר</div>
  <div class="pill">$arrow $change% <small>מאתמול</small></div></div>
</div>
<div class="range"><span>הגבוה ב־30 יום <b>$hi</b></span><span>הנמוך <b>$lo</b></span></div>
<div class="card"><h2>$head</h2><p>$body</p>
  <div class="src"><span>מקור: בנק ישראל, שער יציג</span><span>הסבר כללי, לא ייעוץ השקעות</span></div></div>
</body></html>""")


def find_browser():
    for b in BROWSERS:
        p = shutil.which(b) or (b if os.path.exists(b) else None)
        if p:
            return p
    raise FileNotFoundError("No Chrome/Edge found for rendering")


def build_html(series):
    vals = [v for _, v in series]
    rate, prev = vals[-1], vals[-2]
    change = (rate / prev - 1) * 100
    head, body = meaning(change, rate)
    ros = (guilloche(150, 180, 420, 11, 330, "#1D4B4E", 0.9)
           + guilloche(980, 1000, 380, 9, 300, "#1D4B4E", 0.7))
    d = date.fromisoformat(series[-1][0])
    return HTML.substitute(
        rosettes=ros, chart=chart_svg(vals), brand=BRAND,
        issue=f"No. {d.strftime('%d.%m.%y')}", rate=f"{rate:.3f}",
        arrow="▼" if change < 0 else "▲", change=f"{abs(change):.2f}",
        hi=f"{max(vals):.3f}", lo=f"{min(vals):.3f}", head=head, body=body)


def render(html, out):
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "card.html")
        open(f, "w", encoding="utf-8").write(html)
        subprocess.run([find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1350", "--virtual-time-budget=10000",
                        f"--screenshot={os.path.abspath(out)}", "file:///" + f.replace("\\", "/")],
                       check=True, timeout=120, capture_output=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out/money_card.png"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    render(build_html(fetch_series()), out)
    print("saved", out)
