"""9-slide story carousels: one idea told step by step, with a growing-tree illustration,
number cards and flowing text. All numbers are computed. Usage: python story_cards.py [out_dir]"""
import os
import sys

from content_cards import fv_monthly, money
from money_cards import render

INK, MINT1, MINT2, CARD = "#10213A", "#3CCFAA", "#D4F8EC", "rgba(255,255,255,.72)"
SUN, LEAF, LEAF2, GROUND, CORAL = "#FFC933", "#1F9D6E", "#35B982", "#17795B", "#FF6B4A"
SERIES = "ריבית דריבית"
BRAND = "הכסף היומי"

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Secular+One&family=Heebo:wght@400;500;700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:'Heebo',sans-serif;color:{INK};
background:linear-gradient(165deg,{MINT1} 0%,{MINT2} 100%)}}
.abs{{position:absolute}} .ltr{{direction:ltr}}
.bar{{position:absolute;top:64px;right:72px;left:72px;display:flex;align-items:center;gap:24px;font-weight:700;font-size:30px}}
.bar .line{{flex:1;height:3px;background:rgba(16,33,58,.25)}}
h1{{font-family:'Secular One',sans-serif;font-weight:400;line-height:1.08}}
.card{{background:{CARD};border-radius:34px;padding:30px 36px}}
.card small{{display:block;font-size:30px;font-weight:600;opacity:.75;margin-bottom:6px}}
.card b{{font-size:78px;font-weight:800;line-height:1.05;display:block}}
p{{font-size:42px;line-height:1.5;font-weight:500;margin-bottom:26px}}
.brand{{position:absolute;bottom:52px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px;
font-family:'Secular One',sans-serif;font-size:46px}}
.foot{{position:absolute;bottom:128px;right:72px;left:72px;font-size:26px;opacity:.7}}
"""

COIN = lambda x, y, r=15: (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SUN}" stroke="#D49A00" stroke-width="3"/>'
                           f'<circle cx="{x}" cy="{y}" r="{r * 0.55}" fill="none" stroke="#D49A00" stroke-width="2"/>')


def tree(level):
    """level 0 sprout ... 3 big tree with coins. Drawn on a 1080x440 canvas."""
    ground = f'<ellipse cx="540" cy="420" rx="620" ry="90" fill="{GROUND}"/>'
    if level == 0:
        body = (f'<path d="M540 400 C540 360 540 340 540 310" stroke="{LEAF}" stroke-width="10" fill="none" stroke-linecap="round"/>'
                f'<ellipse cx="505" cy="315" rx="38" ry="20" transform="rotate(-30 505 315)" fill="{LEAF2}"/>'
                f'<ellipse cx="578" cy="300" rx="42" ry="22" transform="rotate(28 578 300)" fill="{LEAF}"/>')
    else:
        s = {1: 0.55, 2: 0.8, 3: 1.1}[level]
        top = 405 - 190 * s
        body = (f'<rect x="{540 - 16 * s}" y="{top + 60 * s}" width="{32 * s}" height="{345 - 60 * s - top + 60 * s}" rx="10" fill="#7A4A2B"/>'
                f'<circle cx="{540 - 70 * s}" cy="{top + 40 * s}" r="{80 * s}" fill="{LEAF2}"/>'
                f'<circle cx="{540 + 70 * s}" cy="{top + 40 * s}" r="{80 * s}" fill="{LEAF2}"/>'
                f'<circle cx="540" cy="{top - 10 * s}" r="{100 * s}" fill="{LEAF}"/>')
        coins = {1: [(520, top), (580, top + 30)],
                 2: [(480, top + 10), (560, top - 30), (610, top + 40), (520, top + 60)],
                 3: [(430, top + 20), (500, top - 40), (580, top - 60), (650, top - 10), (690, top + 50), (470, top + 80),
                     (560, top + 40), (620, top + 90)]}[level]
        body += "".join(COIN(x, y, 16 if level < 3 else 20) for x, y in coins)
        if level == 3:
            body += "".join(COIN(x, 400 - i % 3 * 14, 22) for i, x in enumerate(range(380, 480, 22)))
            body += "".join(COIN(x, 400 - i % 3 * 14, 22) for i, x in enumerate(range(620, 740, 24)))
    return f'<svg viewBox="0 0 1080 440" width="1080" height="440" xmlns="http://www.w3.org/2000/svg">{ground}{body}</svg>'


def hero_art():
    hill = f'<path d="M0 300 C250 170 520 300 1080 120 L1080 440 L0 440 Z" fill="{GROUND}"/>'
    trail = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".7"/>'
                    for x, y, r in [(250, 262, 10), (330, 276, 14), (410, 286, 18)])
    ball = (f'<circle cx="640" cy="228" r="130" fill="#fff"/><circle cx="600" cy="190" r="26" fill="#E7F7F1"/>'
            f'<circle cx="680" cy="262" r="38" fill="#E7F7F1"/><path d="M520 300 C560 340 700 350 760 300" '
            f'stroke="#CDE8DE" stroke-width="10" fill="none" stroke-linecap="round"/>')
    pile = "".join(COIN(x, y, 24) for x, y in [(880, 390), (930, 390), (980, 392), (905, 360), (955, 362), (930, 332)])
    return f'<svg viewBox="0 0 1080 440" width="1080" height="440" xmlns="http://www.w3.org/2000/svg">{hill}{trail}{ball}{pile}</svg>'


def bars(a, b, la, lb):
    m = max(a, b)
    ha, hb = 300 * a / m, 300 * b / m
    return (f'<svg viewBox="0 0 1080 420" width="1080" height="420" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="260" y="{360 - ha}" width="220" height="{ha}" rx="22" fill="{INK}"/>'
            f'<rect x="600" y="{360 - hb}" width="220" height="{hb}" rx="22" fill="{CORAL}"/>'
            f'<text x="370" y="{346 - ha}" font-family="Heebo" font-weight="800" font-size="44" text-anchor="middle" fill="{INK}">{money(a)}</text>'
            f'<text x="710" y="{346 - hb}" font-family="Heebo" font-weight="800" font-size="44" text-anchor="middle" fill="{INK}">{money(b)}</text>'
            f'<text x="370" y="405" font-family="Heebo" font-weight="700" font-size="34" text-anchor="middle" fill="{INK}">{la}</text>'
            f'<text x="710" y="405" font-family="Heebo" font-weight="700" font-size="34" text-anchor="middle" fill="{INK}">{lb}</text></svg>')


def slide(n, total, title, content, art="", art_bottom=170, foot="", title_size=92, top=430, series=SERIES):
    coin = f'<svg width="46" height="46" viewBox="0 0 46 46">{COIN(23, 23, 19)}</svg>'
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="bar"><span>{series}</span><span class="line"></span><span class="ltr">{n}/{total}</span></div>'
            f'<h1 class="abs" style="top:150px;right:72px;left:72px;font-size:{title_size}px">{title}</h1>'
            f'<div class="abs" style="top:{top}px;right:72px;left:72px">{content}</div>'
            f'<div class="abs" style="bottom:{art_bottom}px;left:0;right:0">{art}</div>'
            f'{"<div class=foot>" + foot + "</div>" if foot else ""}'
            f'<div class="brand">{coin}<span>{BRAND}</span></div></body></html>')


def cards(*items):
    return ('<div style="display:flex;gap:22px;margin-bottom:34px">' +
            "".join(f'<div class="card" style="flex:1"><small>{k}</small><b class="ltr" style="text-align:right">{v}</b></div>'
                    for k, v in items) + '</div>')


def chips(*items):
    return ('<div style="display:flex;gap:18px;margin-bottom:40px">' +
            "".join(f'<div class="card" style="flex:1;padding:26px 28px"><small style="font-size:28px">{k}</small>'
                    f'<b style="font-size:52px">{v}</b></div>' for k, v in items) + '</div>')


def compound_story(pmt=500, rate=0.05):
    f = lambda y: fv_monthly(pmt, rate, y)
    dep = lambda y: pmt * 12 * y
    f30, f20, f10, f2 = f(30), f(20), f(10), f(2)
    rm = rate / 12
    stop10 = f10 * (1 + rm) ** (20 * 12)
    N = 9
    title = f"איך {pmt} שקלים בחודש נהיים {f30 / 1000:.0f} אלף שקלים"
    sub = "סיפור ב־9 שקופיות: מה קורה לחיסכון קטן כשנותנים לו זמן."
    slides = [
        slide(1, N, f"איך {pmt} שקלים בחודש נהיים {f30 / 1000:.0f} אלף שקלים",
              f'<p style="font-size:46px">והסוד הוא לא להרוויח יותר. הוא להתחיל, ולהמשיך.</p>', hero_art(), art_bottom=150, title_size=100),
        slide(2, N, "קודם, ההנחות",
              chips(("הפקדה בחודש", money(pmt)), ("תשואה לדוגמה", f"{rate * 100:.0f}% בשנה"), ("תקופה", "30 שנה")) +
              "<p>אין כאן מזל ואין תזמון שוק. אותו סכום, כל חודש, ולא נוגעים בו.</p>"
              "<p>כל מספר בהמשך מחושב מהנתונים האלה.</p>",
              foot="התשואה היא דוגמה. בפועל היא משתנה משנה לשנה, ויכולות להיות גם שנים של ירידות.", top=340),
        slide(3, N, "בשנתיים הראשונות נראה שכלום לא קורה",
              cards(("הפקדת", money(dep(2))), ("יש לך", money(f2))) +
              f"<p>הריבית הוסיפה רק {money(f2 - dep(2))}. זה הרגע שבו הרבה אנשים אומרים \"לא שווה את זה\" ועוצרים.</p>",
              tree(0), art_bottom=150),
        slide(4, N, "אחרי 10 שנים כבר רואים משהו",
              cards(("הפקדת", money(dep(10))), ("יש לך", money(f10))) +
              f"<p>הריבית כבר הוסיפה {money(f10 - dep(10))}. עדיין לא מרגש, אבל הקו התחיל לעלות.</p>",
              tree(1), art_bottom=150),
        slide(5, N, "אחרי 20 שנה הריבית נכנסת לעבודה",
              cards(("הפקדת", money(dep(20))), ("יש לך", money(f20))) +
              f"<p>הריבית כבר גדולה מחצי ממה שהפקדת: {money(f20 - dep(20))} מול {money(dep(20))}.</p>",
              tree(2), art_bottom=150),
        slide(6, N, "אחרי 30 שנה מגיע המספר הגדול",
              cards(("הפקדת", money(dep(30))), ("יש לך", money(f30))) +
              f"<p>{money(f30 - dep(30))} מתוכם הם ריבית. יותר ממה שהפקדת בכלל.</p>",
              tree(3), art_bottom=150),
        slide(7, N, "ומה אם מפסיקים אחרי 10 שנים?",
              cards(("הפקדת", money(dep(10))), ("אחרי 30 שנה", money(stop10))) +
              f"<p>הפסקת להפקיד, אבל השארת את הכסף לעבוד עוד 20 שנה.</p>"
              f"<p>הפקדת {dep(10) / dep(30) * 100:.0f}% מהסכום, והגעת ל־{stop10 / f30 * 100:.0f}% מהתוצאה.</p>",
              foot="הדוגמה מניחה שלא מושכים את הכסף ושהתשואה נשארת קבועה."),
        slide(8, N, "ומה אם מתחילים 10 שנים מאוחר?",
              f"<p>אותה הפקדה, עשר שנים פחות על השעון. ההמתנה עולה בערך <b style='font-weight:800'>{money(f30 - f20)}</b>.</p>"
              f"<p style='font-size:36px;opacity:.8'>לא כי הפקדת פחות, אלא כי הזמן עבד פחות.</p>",
              bars(f30, f20, "מתחילים עכשיו", "מתחילים בעוד 10 שנים"), art_bottom=150),
        slide(9, N, "מה לוקחים מזה?",
              "<p><b style='font-weight:800'>הזמן חשוב יותר מהסכום.</b> בדוגמה הזאת, ההתחלה המוקדמת עשתה את רוב ההבדל.</p>"
              "<p><b style='font-weight:800'>החלק המשעמם הוא החלק שעובד.</b> הפקדה קבועה, בלי דרמה.</p>"
              "<p><b style='font-weight:800'>שמרו לפוסט</b> ושלחו למי שצריך לשמוע את זה.</p>",
              foot=f"כל המספרים הם דוגמה לפי {money(pmt)} בחודש ו־{rate * 100:.0f}% בשנה. אין כאן הבטחה, והשקעה כרוכה בסיכון. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


def cup_art():
    steam = "".join(f'<path d="M{x} 150 C{x - 22} 110 {x + 22} 80 {x} 40" stroke="#fff" stroke-width="10" fill="none" '
                    f'stroke-linecap="round" opacity=".8"/>' for x in (470, 540, 610))
    cup = (f'<ellipse cx="540" cy="395" rx="230" ry="32" fill="{GROUND}"/>'
           f'<path d="M400 170 L680 170 L650 360 Q540 400 430 360 Z" fill="#fff"/>'
           f'<path d="M680 200 C770 190 770 300 660 300" stroke="#fff" stroke-width="26" fill="none" stroke-linecap="round"/>'
           f'<ellipse cx="540" cy="172" rx="140" ry="22" fill="#8A5A3B"/>')
    coins = "".join(COIN(x, y, 22) for x, y in [(860, 380), (910, 380), (960, 382), (885, 350), (935, 352), (910, 322)])
    return f'<svg viewBox="0 0 1080 440" width="1080" height="440" xmlns="http://www.w3.org/2000/svg">{steam}{cup}{coins}</svg>'


def pile(level):
    """Five coin stacks whose height grows with level 1..4."""
    ground = f'<ellipse cx="540" cy="420" rx="620" ry="90" fill="{GROUND}"/>'
    body = ""
    for x, h in [(360, 3), (450, 5), (540, 7), (630, 5), (720, 3)]:
        for k in range(max(1, round(h * level / 4))):
            body += COIN(x, 400 - k * 20, 26)
    return f'<svg viewBox="0 0 1080 440" width="1080" height="440" xmlns="http://www.w3.org/2000/svg">{ground}{body}</svg>'


def coffee_story(price=18, per_year=365, rate=0.04, home=4, home_days_week=3):
    month, year, ten = price * per_year / 12, price * per_year, price * per_year * 10
    grown = fv_monthly(month, rate, 10)
    save = home_days_week * (per_year / 7) * (price - home)
    N = 9
    sl = lambda *a, **k: slide(*a, series="הרגלים קטנים", **k)
    title = "כמה הקפה של הבוקר עולה לך באמת?"
    sub = "סיפור ב־9 שקופיות: מה קורה להרגל של 18 שקלים ביום."
    slides = [
        sl(1, N, title, '<p style="font-size:46px">18 שקלים ביום. נשמע כלום. בוא נראה את המספר המלא.</p>',
           cup_art(), art_bottom=150, title_size=100),
        sl(2, N, "קודם, ההנחות",
           chips(("מחיר קפה", money(price)), ("כמה פעמים", "כל יום"), ("תקופה", "10 שנים")) +
           "<p>לא נבקש ממך לוותר על כלום. רק להסתכל על המספר.</p>"
           "<p>כל מספר בהמשך מחושב מהנתונים האלה.</p>",
           foot="הנתונים הם דוגמה. כל אחד ישנה אותם לפי ההרגל שלו.", top=340),
        sl(3, N, "ביום ובשבוע זה לא מרגיש",
           cards(("ביום", money(price)), ("בשבוע", money(price * 7))) +
           f"<p>{money(price * 7)} בשבוע זה פחות מארוחה אחת במסעדה. אף אחד לא עוצר על זה.</p>",
           pile(1), art_bottom=150),
        sl(4, N, "בחודש כבר מתחילים להרגיש",
           cards(("בחודש", money(month)), ("בשנה", money(year))) +
           f"<p>{money(month)} בחודש. ובשנה כבר {money(year)}, על משהו שאפשר לשתות בלי לחשוב.</p>",
           pile(2), art_bottom=150),
        sl(5, N, "בשלוש שנים זה כבר סכום",
           cards(("אחרי שנה", money(year)), ("אחרי 3 שנים", money(year * 3))) +
           f"<p>{money(year * 3)} על קפה. אותו הרגל, רק עם יותר אפסים.</p>",
           pile(3), art_bottom=150),
        sl(6, N, "בעשר שנים מגיע המספר",
           cards(("אחרי 10 שנים", money(ten)), ("בממוצע בשנה", money(year))) +
           f"<p>{money(ten)}. זה הסכום שעבר מהכיס שלך לבית הקפה, בלי שהרגשת.</p>",
           pile(4), art_bottom=150),
        sl(7, N, "ואם הכסף הזה היה עובד?",
           cards(("הפקדת", money(ten)), ("יש לך", money(grown))) +
           f"<p>אם היית מפקיד את אותו סכום כל חודש, בתשואה לדוגמה של {rate * 100:.0f}% בשנה, "
           f"הריבית הייתה מוסיפה {money(grown - ten)}.</p>",
           foot="התשואה היא דוגמה, לא הבטחה. בפועל היא משתנה, ויכולות להיות גם שנים של הפסד."),
        sl(8, N, "אפשר גם בלי לוותר על הכול",
           f"<p>אם מחליפים רק {home_days_week} ימים בשבוע בקפה בבית שעולה {home} שקלים, חוסכים בערך "
           f"<b style='font-weight:800'>{money(save)}</b> בשנה.</p>"
           f"<p style='font-size:36px;opacity:.8'>ועדיין נשאר קפה בחוץ ארבעה ימים בשבוע.</p>",
           bars(year, year - save, "כל יום בחוץ", f"{home_days_week} ימים בבית"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           "<p><b style='font-weight:800'>הרגל קטן הוא לא קטן.</b> הוא רק נראה ככה ביום אחד.</p>"
           "<p><b style='font-weight:800'>לא צריך לוותר על כלום.</b> מספיק לדעת כמה זה עולה, ולהחליט.</p>"
           "<p><b style='font-weight:800'>שמרו לפוסט</b> ושלחו למי שמזמין קפה כל בוקר.</p>",
           foot=f"המספרים הם דוגמה לפי {money(price)} ליום. קפה בבית: {money(home)} (הנחה). לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


STORIES = {"story_compound": compound_story, "story_coffee": coffee_story}
META = {}


def build(out_dir="out/story", only=None):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for slug, fn in STORIES.items():
        if only and slug not in only:
            continue
        slides, title, sub = fn()
        META[slug] = {"title": title, "sub": sub}
        for i, html in enumerate(slides, 1):
            p = os.path.join(out_dir, f"{slug}_{i}.png")
            render(html, p)
            paths.append(p)
    return paths


def meta(slug):
    slides, title, sub = STORIES[slug]()
    return {"title": title, "sub": sub, "count": len(slides)}


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "out/story"))
