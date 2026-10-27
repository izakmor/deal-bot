"""Daily USD/ILS carousel (3 slides, 1080x1350) from Bank of Israel data.
Slide 1: the rate + weekly candlestick chart. Slide 2: what it means in shekels.
Slide 3: what the data says. Usage: python money_cards.py [out_dir]"""
import csv
import io
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from string import Template

import requests

URL = ("https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/"
       "?c%5BDATA_TYPE%5D=OF00&c%5BBASE_CURRENCY%5D=USD&lastNObservations=70&format=csv")
BROWSERS = [
    "chrome", "google-chrome", "chromium", "chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
DAYS = ["שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]
MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר",
          "נובמבר", "דצמבר"]
MONTHS_SHORT = ["ינו׳", "פבר׳", "מרץ", "אפר׳", "מאי", "יוני", "יולי", "אוג׳", "ספט׳", "אוק׳", "נוב׳", "דצמ׳"]
INK, PAPER, COBALT, SUN, MUTE, GRID, WARN = "#101A3A", "#EEF2F8", "#2F4BFF", "#FFD23F", "#6B7699", "#D3DAEA", "#D9381E"


def fetch():
    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    return [(date.fromisoformat(x["TIME_PERIOD"]), float(x["OBS_VALUE"])) for x in rows]


def value_on_or_before(series, d):
    best = series[0]
    for item in series:
        if item[0] <= d:
            best = item
    return best


def weekly_candles(series):
    weeks = {}
    for d, v in series:
        weeks.setdefault(d.isocalendar()[:2], []).append((d, v))
    out = []
    for key in sorted(weeks):
        w = weeks[key]
        vals = [v for _, v in w]
        # FX convention: a week opens where the previous one closed
        op = out[-1]["close"] if out else vals[0]
        out.append({"start": w[0][0], "open": op, "close": vals[-1],
                    "hi": max(vals + [op]), "lo": min(vals + [op])})
    return out


def candles_svg(candles, w=936, h=540):
    gutter, bottom, top_m = 104, 50, 22
    pw, ph = w - gutter, h - bottom - top_m
    lo = min(c["lo"] for c in candles)
    hi = max(c["hi"] for c in candles)
    pad = (hi - lo) * 0.1
    lo, hi = lo - pad, hi + pad
    y = lambda v: top_m + ph - (v - lo) / (hi - lo) * ph
    n = len(candles)
    slot = pw / n
    parts = [f'<rect x="{slot * (n - 1):.1f}" y="0" width="{slot:.1f}" height="{h - bottom}" rx="10" fill="{COBALT}" opacity=".09"/>']
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        parts.append(f'<line x1="0" x2="{pw}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{GRID}" stroke-width="2" stroke-dasharray="4 8"/>')
        parts.append(f'<text x="{pw + 16}" y="{y(v) + 9:.1f}" fill="{MUTE}" font-size="26" font-family="Heebo">{v:.2f}</text>')
    last_month = None
    for i, c in enumerate(candles):
        cx = slot * (i + 0.5)
        bw = slot * 0.52
        last = i == n - 1
        col = COBALT if last else INK
        up = c["close"] >= c["open"]
        top, bot = y(max(c["open"], c["close"])), y(min(c["open"], c["close"]))
        bot = max(bot, top + 5)
        fill = col if up else PAPER
        parts.append(f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{y(c["hi"]):.1f}" y2="{y(c["lo"]):.1f}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
        parts.append(f'<rect x="{cx - bw / 2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bot - top:.1f}" rx="3" fill="{fill}" stroke="{col}" stroke-width="4"/>')
        m = c["start"].month
        if m != last_month:
            parts.append(f'<text x="{cx:.1f}" y="{h - 10}" fill="{MUTE}" font-size="26" font-family="Heebo" text-anchor="middle">{MONTHS_SHORT[m - 1]}</text>')
            last_month = m
    lc = candles[-1]
    ly = y(lc["close"])
    lx = slot * (n - 0.5)
    parts.append(f'<line x1="{lx:.1f}" x2="{pw}" y1="{ly:.1f}" y2="{ly:.1f}" stroke="{COBALT}" stroke-width="2.5" stroke-dasharray="3 7"/>')
    parts.append(f'<rect x="{pw + 4}" y="{ly - 20:.1f}" width="{gutter - 4}" height="40" rx="8" fill="{COBALT}"/>')
    parts.append(f'<text x="{pw + 4 + (gutter - 4) / 2}" y="{ly + 9:.1f}" fill="#fff" font-size="26" font-weight="700" font-family="Heebo" text-anchor="middle">{lc["close"]:.3f}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Secular+One&family=Heebo:wght@400;500;700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;background:{PAPER};color:{INK};font-family:'Heebo',sans-serif;position:relative;overflow:hidden}}
.abs{{position:absolute}}
h1{{font-family:'Secular One',sans-serif;font-weight:400;font-size:88px;line-height:1.05}}
.sub{{font-size:36px;color:{MUTE};font-weight:500}}
.dots{{position:absolute;bottom:52px;left:0;right:0;display:flex;justify-content:center;gap:14px}}
.dots i{{display:block;width:16px;height:16px;border-radius:8px;background:{GRID}}}
.dots i.on{{width:48px;background:{COBALT}}}
.ltr{{direction:ltr}}
"""


def page(body, step):
    dots = "".join(f'<i class="{"on" if i == step else ""}"></i>' for i in range(3))
    return f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}<div class="dots">{dots}</div></body></html>'


def slide1(series, candles):
    d, rate = series[-1]
    prev = series[-2][1]
    ch = (rate / prev - 1) * 100
    arrow = "▼" if ch < 0 else "▲"
    word = "ירד" if ch < 0 else "עלה"
    date_txt = f"יום {DAYS[d.weekday()]}, {d.day} ב{MONTHS[d.month - 1]}"
    return page(f"""
<div class="abs sub" style="top:72px;right:72px">{date_txt}</div>
<h1 class="abs" style="top:132px;right:72px">כמה עולה דולר?</h1>
<div class="abs ltr" style="top:262px;right:72px;display:flex;align-items:baseline;gap:18px;font-weight:800">
  <span style="font-size:132px;line-height:1;letter-spacing:-2px">{rate:.3f}</span><span style="font-size:64px;color:{COBALT}">₪</span></div>
<div class="abs" style="top:430px;right:72px;display:flex;align-items:center;gap:18px">
  <span class="ltr" style="background:{SUN};font-weight:800;font-size:40px;padding:6px 24px 8px;border-radius:40px">{arrow} {abs(ch):.2f}%</span>
  <span style="font-size:36px;font-weight:500">{word} מאתמול</span></div>
<div class="abs" style="top:572px;right:72px;left:72px;display:flex;justify-content:space-between;font-size:30px;color:{MUTE};font-weight:500">
  <span>נרות שבועיים, כשלושה חודשים</span><span>מלא: עלה. ריק: ירד.</span></div>
<div class="abs ltr" style="top:640px;left:72px">{candles_svg(candles)}</div>
<div class="abs" style="top:1322px;display:none"></div>""", 0)


def slide2(series):
    d, rate = series[-1]
    _, old = value_on_or_before(series, d - timedelta(days=30))
    rows = [("קנייה באתר זר", 100, "buy"), ("טיסה וחופשה", 1000, "buy"), ("משכורת בדולרים", 5000, "earn")]
    out = []
    for title, usd, kind in rows:
        now_v, old_v = usd * rate, usd * old
        diff = now_v - old_v
        cheaper = diff < 0
        good = cheaper if kind == "buy" else not cheaper
        if abs(diff) < 0.5:
            line, color = "כמעט בלי שינוי לעומת לפני חודש", MUTE
        else:
            verb = ("זול" if cheaper else "יקר") if kind == "buy" else ("מקבלים פחות" if cheaper else "מקבלים יותר")
            line = (f"{verb} ב־₪{abs(diff):,.0f} לעומת לפני חודש" if kind == "buy"
                    else f"{verb} ב־₪{abs(diff):,.0f} לעומת לפני חודש")
            color = COBALT if good else WARN
        out.append(f"""<div style="padding:34px 0;border-top:3px solid {GRID}">
  <div style="display:flex;justify-content:space-between;align-items:baseline">
    <div><div style="font-size:46px;font-weight:700">{title}</div><div style="font-size:32px;color:{MUTE};font-weight:500">{usd:,} דולר</div></div>
    <div class="ltr" style="font-size:72px;font-weight:800;line-height:1">₪{now_v:,.0f}</div></div>
  <div style="margin-top:12px;font-size:34px;font-weight:700;color:{color}">{line}</div></div>""")
    return page(f"""
<h1 class="abs" style="top:100px;right:72px;left:72px">מה זה אומר לכיס שלך?</h1>
<div class="abs sub" style="top:214px;right:72px">אותו סכום בדולרים, בשקלים</div>
<div class="abs" style="top:330px;right:72px;left:72px">{''.join(out)}</div>
<div class="abs" style="bottom:120px;right:72px;left:72px;font-size:26px;color:{MUTE}">חישוב לפי השער היציג של בנק ישראל. הסבר כללי, לא ייעוץ.</div>""", 1)


def slide3(series, candles):
    d, rate = series[-1]
    vals = [v for _, v in series]
    lo, hi = min(vals), max(vals)
    pos = (rate - lo) / (hi - lo)
    where = "קרוב לתחתית" if pos < 0.25 else "קרוב לראש" if pos > 0.75 else "באמצע"
    d30, v30 = value_on_or_before(series, d - timedelta(days=30))
    ch30 = (rate / v30 - 1) * 100
    moves = [abs(b / a - 1) * 100 for (_, a), (_, b) in zip(series, series[1:])]
    avg = sum(moves) / len(moves)
    today = moves[-1]
    ratio = today / avg if avg else 1
    today_txt = (f"התנועה של היום, {today:.2f}%, חזקה פי {ratio:.1f} מהרגיל." if ratio >= 1.5
                 else f"התנועה של היום, {today:.2f}%, בטווח הרגיל." if ratio >= 0.5
                 else f"היום השער כמעט לא זז, {today:.2f}%.")
    marker = (1 - pos) * 100
    return page(f"""
<h1 class="abs" style="top:100px;right:72px;left:72px">מה הנתונים אומרים?</h1>
<div class="abs" style="top:250px;right:72px;left:72px">
  <div style="font-size:44px;font-weight:700">השער נמצא {where} של הטווח</div>
  <div style="font-size:32px;color:{MUTE};font-weight:500;margin-top:4px">בכשלושה חודשים האחרונים</div>
  <div style="position:relative;height:16px;border-radius:8px;background:{GRID};margin:44px 0 12px">
    <div style="position:absolute;top:-12px;right:calc({marker:.1f}% - 20px);width:40px;height:40px;border-radius:20px;background:{COBALT};border:6px solid {PAPER}"></div></div>
  <div class="ltr" style="display:flex;justify-content:space-between;font-size:32px;font-weight:700"><span>{lo:.3f}</span><span>{hi:.3f}</span></div></div>
<div class="abs" style="top:560px;right:72px;left:72px;border-top:3px solid {GRID};padding-top:34px">
  <div style="font-size:44px;font-weight:700">{'ירד' if ch30 < 0 else 'עלה'} {abs(ch30):.1f}% בחודש האחרון</div>
  <div style="font-size:34px;margin-top:8px;font-weight:500">{today_txt}</div></div>
<div class="abs" style="top:800px;right:72px;left:72px;border-top:3px solid {GRID};padding-top:34px">
  <div style="font-size:44px;font-weight:700">ולמה זה זז?</div>
  <div style="font-size:34px;line-height:1.42;margin-top:8px;font-weight:500">את הסיבה המדויקת ליום אחד אי אפשר לדעת. בדרך כלל משפיעים: הריבית בישראל ובארה״ב, כסף שנכנס ויוצא מהארץ, והמצב הכלכלי והביטחוני.</div></div>
<div class="abs" style="bottom:120px;right:72px;left:72px;font-size:26px;color:{MUTE}">מקור: בנק ישראל. הסבר כללי, לא ייעוץ השקעות.</div>""", 2)


def find_browser():
    for b in BROWSERS:
        p = shutil.which(b) or (b if os.path.exists(b) else None)
        if p:
            return p
    raise FileNotFoundError("No Chrome/Edge found")


def render(html, out):
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "s.html")
        open(f, "w", encoding="utf-8").write(html)
        subprocess.run([find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1350", "--virtual-time-budget=10000",
                        f"--screenshot={os.path.abspath(out)}", "file:///" + f.replace("\\", "/")],
                       check=True, timeout=120, capture_output=True)


def build(out_dir="out", series=None):
    """Renders the 3 slides named by data date; returns (paths, series)."""
    os.makedirs(out_dir, exist_ok=True)
    series = series or fetch()
    candles = weekly_candles(series)
    tag = series[-1][0].isoformat()
    paths = []
    for i, html in enumerate([slide1(series, candles), slide2(series), slide3(series, candles)], 1):
        p = os.path.join(out_dir, f"money_{tag}_{i}.png")
        render(html, p)
        paths.append(p)
    return paths, series


def caption(series):
    d, rate = series[-1]
    ch = (rate / series[-2][1] - 1) * 100
    arrow = "▼" if ch < 0 else "▲"
    return (f"הדולר עומד על {rate:.3f} ₪ ({arrow} {abs(ch):.2f}% מאתמול).\n\n"
            "גוללים הצידה: מה זה אומר לכיס שלך, ומה הנתונים אומרים.\n\n"
            "מקור: בנק ישראל, שער יציג. הסבר כללי, לא ייעוץ השקעות.\n\n"
            "#דולר #שערהדולר #כסף #חיסכון #כלכלה")


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "out")[0])
