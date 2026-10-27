"""Evergreen carousel posts built from templates + parameters. All numbers are computed here,
so every post is accurate for its stated assumptions.
Usage: python content_cards.py [out_dir]   (renders every post in POSTS as 3 PNG slides)"""
import os
import sys

from money_cards import CSS, INK, PAPER, COBALT, SUN, MUTE, GRID, render

DISCLAIMER = "דוגמה לחישוב בלבד. לא הבטחה ולא ייעוץ השקעות."


def money(v):
    return f"₪{v:,.0f}"


def fv_monthly(pmt, annual, years):
    r, n = annual / 12, years * 12
    return pmt * (((1 + r) ** n - 1) / r)


def doc(body, dark=False):
    bg = f"body{{background:{INK};color:{PAPER}}}" if dark else ""
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}{bg}</style>'
            f'</head><body>{body}</body></html>')


LAST = {}


def hook(title, sub):
    import re
    LAST.update(title=re.sub(r"<[^>]+>", "", title), sub=sub)
    return doc(f"""
<div class="abs" style="inset:0;padding:72px;display:flex;flex-direction:column;justify-content:center">
  <h1 style="font-size:124px;line-height:1.08">{title}</h1>
  <div style="margin-top:44px;font-size:44px;font-weight:500;color:#AEB8D6;line-height:1.35">{sub}</div></div>""",
               dark=True)


def numbers(title, sub, rows, note=""):
    out = []
    for i, (label, value) in enumerate(rows):
        last = i == len(rows) - 1
        color = COBALT if last else INK
        size = 112 if last else 76
        out.append(f"""<div style="flex:1;display:flex;justify-content:space-between;align-items:center;
border-top:3px solid {GRID}">
  <div style="font-size:50px;font-weight:{700 if last else 500}">{label}</div>
  <div class="ltr" style="font-size:{size}px;font-weight:800;color:{color};line-height:1">{value}</div></div>""")
    foot = f'<div class="abs" style="bottom:90px;right:72px;left:72px;font-size:28px;color:{MUTE}">{note}</div>' if note else ""
    return doc(f"""
<h1 class="abs" style="top:100px;right:72px;left:72px;font-size:80px">{title}</h1>
<div class="abs sub" style="top:210px;right:72px;left:72px">{sub}</div>
<div class="abs" style="top:330px;bottom:190px;right:72px;left:72px;display:flex;flex-direction:column">{''.join(out)}</div>{foot}""")


def lesson(title, lines, note=DISCLAIMER, big=None):
    paras = "".join(f'<p style="font-size:46px;line-height:1.4;font-weight:500;margin-bottom:30px">{l}</p>' for l in lines)
    bigblock = ""
    if big:
        bigblock = (f'<div style="margin-bottom:40px"><div style="font-size:44px;font-weight:700;color:{MUTE}">{big[0]}</div>'
                    f'<div class="ltr" style="font-size:150px;font-weight:800;color:{COBALT};line-height:1.05;text-align:right">{big[1]}</div></div>')
    return doc(f"""
<h1 class="abs" style="top:100px;right:72px;left:72px;font-size:84px">{title}</h1>
<div class="abs" style="top:300px;bottom:170px;right:72px;left:72px;display:flex;flex-direction:column;justify-content:center">{bigblock}{paras}</div>
<div class="abs" style="bottom:90px;right:72px;left:72px;font-size:28px;color:{MUTE}">{note}</div>""")


def hl(text):
    return f'<span style="color:{SUN}">{text}</span>'


META = {}


def plain(t):
    import re
    return re.sub(r"<[^>]+>", "", t)


def habit(unit, price, per_year, hook_title, sub, rate=0.04):
    month, year = price * per_year / 12, price * per_year
    ten = year * 10
    grown = fv_monthly(month, rate, 10)
    return [
        hook(hook_title, sub),
        numbers("בואו נחשב", "אותו הרגל, בשקלים", [
            (f"כל {unit}", money(price)), ("בחודש", money(month)), ("בשנה", money(year)),
            ("בעשר שנים", money(ten))]),
        lesson("ואם הכסף הזה היה עובד?", [
            f"אם היית מפקיד את אותו סכום כל חודש, בתשואה לדוגמה של {rate * 100:.0f}% בשנה.",
            f"הפקדת בסך הכול {money(ten)}. ההפרש בא מהריבית.",
            "לא צריך לוותר על כלום. מספיק לדעת כמה זה עולה."], big=("אחרי עשר שנים", money(grown))),
    ]


def compound(amount, rate, hook_title, sub):
    rows = [(f"אחרי {y} שנים", money(amount * (1 + rate) ** y)) for y in (10, 20, 30)]
    double = 72 / (rate * 100)
    return [
        hook(hook_title, sub),
        numbers("ככה זה גדל", f"{money(amount)} בריבית של {rate * 100:.0f}% בשנה, בלי לגעת", rows,
                note="ריבית דריבית: הריבית נצברת גם על הריבית של השנים הקודמות."),
        lesson("החוק של 72", [
            "מחלקים 72 בריבית השנתית, וזה בערך מספר השנים עד שהכסף מוכפל.",
            f"בריבית של {rate * 100:.0f}%: 72 ÷ {rate * 100:.0f} = בערך {double:.0f} שנים.",
            f"בריבית של {rate * 200:.0f}%: בערך {72 / (rate * 200):.0f} שנים."],
               note="קירוב מקובל. " + DISCLAIMER),
    ]


def inflation(rate, hook_title, sub):
    rows = [(f"בעוד {y} שנים", money(100 / (1 + rate) ** y)) for y in (10, 20, 30)]
    return [
        hook(hook_title, sub),
        numbers("כוח הקנייה של 100 שקלים", f"אם המחירים עולים {rate * 100:.0f}% בשנה", rows,
                note="כמה סל קניות שעולה היום 100 ₪ עולה בעתיד, בערך."),
        lesson("מה זה אומר?", [
            "מחירים עולים לאורך זמן, ולכן אותו סכום קונה פחות.",
            "כסף שרק עומד מאבד כוח קנייה בשקט.",
            f"{rate * 100:.0f}% בשנה היא הנחה לדוגמה. האינפלציה האמיתית משתנה משנה לשנה."]),
    ]


POSTS = {}


def add(slug, slides):
    """Register a post; the queue order is the order of add() calls."""
    POSTS[slug] = slides
    META[slug] = dict(LAST)


add("habit_coffee", habit("קפה", 18, 365, f"כמה הקפה של הבוקר עולה לך {hl('בעשר שנים')}?", "18 שקלים ביום. בוא נחשב."))
add("habit_delivery", habit("משלוח", 85, 104, f"משלוח אוכל פעמיים בשבוע. כמה זה {hl('בשנה')}?", "85 שקלים למשלוח. המספר מפתיע."))
add("compound_1000", compound(1000, 0.04, f"מה קורה ל־1,000 שקלים אם לא נוגעים בהם {hl('30 שנה')}?", "בלי טריקים. רק זמן וריבית."))
add("inflation_100", inflation(0.03, f"100 שקלים של היום. כמה הם יקנו {hl('בעוד 10 שנים')}?", "הכסף נשאר אותו כסף. המחירים לא."))


def build_all(out_dir="out/content", only=None):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for slug, slides in POSTS.items():
        if only and slug not in only:
            continue
        for i, html in enumerate(slides, 1):
            p = os.path.join(out_dir, f"{slug}_{i}.png")
            render(html, p)
            paths.append(p)
    return paths


if __name__ == "__main__":
    print(build_all(sys.argv[1] if len(sys.argv) > 1 else "out/content"))
