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


def inflation(rate, hook_title, sub, amount=100):
    rows = [(f"בעוד {y} שנים", money(amount / (1 + rate) ** y)) for y in (10, 20, 30)]
    return [
        hook(hook_title, sub),
        numbers(f"כוח הקנייה של {amount:,} שקלים", f"אם המחירים עולים {rate * 100:.0f}% בשנה", rows,
                note=f"כמה סל קניות שעולה היום {money(amount)} עולה בעתיד, בערך."),
        lesson("מה זה אומר?", [
            "מחירים עולים לאורך זמן, ולכן אותו סכום קונה פחות.",
            "כסף שרק עומד מאבד כוח קנייה בשקט.",
            f"{rate * 100:.0f}% בשנה היא הנחה לדוגמה. האינפלציה האמיתית משתנה משנה לשנה."]),
    ]


def monthly(pmt, rate, hook_title, sub):
    rows = [(f"אחרי {y} שנים", money(fv_monthly(pmt, rate, y))) for y in (10, 20, 30)]
    total = pmt * 12 * 30
    return [
        hook(hook_title, sub),
        numbers("ככה זה מצטבר", f"הפקדה של {money(pmt)} בחודש, בתשואה לדוגמה של {rate * 100:.0f}% בשנה", rows,
                note="הפקדה חודשית קבועה, והתשואה נצברת מדי חודש."),
        lesson("כמה מזה הגיע מהפקדות?", [
            f"ב־30 שנה הפקדת בסך הכול {money(total)}.",
            f"את ההפרש עשו הזמן והריבית: {money(fv_monthly(pmt, rate, 30) - total)}.",
            "ככל שמתחילים מוקדם יותר, הזמן עובד בשבילך."], big=("אחרי 30 שנה", money(fv_monthly(pmt, rate, 30)))),
    ]


def start_early(pmt, rate, age1, age2, hook_title, sub, retire=65):
    a, b = fv_monthly(pmt, rate, retire - age1), fv_monthly(pmt, rate, retire - age2)
    return [
        hook(hook_title, sub),
        numbers("אותה הפקדה, התחלה שונה", f"{money(pmt)} בחודש עד גיל {retire}, תשואה לדוגמה של {rate * 100:.0f}%", [
            (f"מתחילים בגיל {age2}", money(b)), (f"מתחילים בגיל {age1}", money(a))]),
        lesson("מה עלתה ההמתנה?", [
            f"המתנה של {age2 - age1} שנים עולה בערך {money(a - b)} בסוף הדרך.",
            f"בגיל {age1} הפקדת {money(pmt * 12 * (retire - age1))}, ובגיל {age2} {money(pmt * 12 * (retire - age2))}.",
            "ההבדל הגדול נוצר בשנים הראשונות."], big=("ההפרש", money(a - b))),
    ]


def fees(principal, gross, years, hook_title, sub):
    levels = (0.005, 0.01, 0.02)
    vals = [principal * (1 + gross - f) ** years for f in levels]
    return [
        hook(hook_title, sub),
        numbers("אותה השקעה, עמלה שונה", f"{money(principal)}, תשואה של {gross * 100:.0f}% לפני עמלה, {years} שנה",
                [(f"עמלה של {f * 100:.1f}%", money(v)) for f, v in zip(levels, vals)]),
        lesson("מה זה אומר?", [
            "עמלה קטנה נראית כלום בשנה אחת.",
            "אבל היא נגרעת מהתשואה כל שנה, ולכן הפער גדל עם הזמן.",
            "שווה לבדוק כמה אתה משלם."], big=("הפער בין 0.5% ל־2%", money(vals[0] - vals[2]))),
    ]


def simple_vs_compound(amount, rate, years, hook_title, sub):
    simple, comp = amount * (1 + rate * years), amount * (1 + rate) ** years
    return [
        hook(hook_title, sub),
        numbers("שתי דרכים לחשב ריבית", f"{money(amount)}, ריבית של {rate * 100:.0f}% בשנה, {years} שנה",
                [("ריבית פשוטה", money(simple)), ("ריבית דריבית", money(comp))]),
        lesson("מה ההבדל?", [
            "ריבית פשוטה: הריבית מחושבת רק על הסכום המקורי.",
            "ריבית דריבית: הריבית נוספת לקרן, ואז גם עליה מקבלים ריבית.",
            f"אחרי {years} שנה ההפרש הוא {money(comp - simple)}."], big=("ההפרש", money(comp - simple))),
    ]


def rule72_post(hook_title, sub, rates=(2, 4, 6, 8)):
    return [
        hook(hook_title, sub),
        numbers("כמה זמן עד ההכפלה", "לפי החוק של 72", [(f"ריבית של {r}%", f"כ־{72 / r:.0f} שנים") for r in rates]),
        lesson("איך זה עובד?", [
            "מחלקים 72 בריבית השנתית.",
            "התוצאה היא בערך מספר השנים עד שהכסף מוכפל.",
            "זה קירוב מקובל, לא חישוב מדויק."], note="ההנחה היא ריבית קבועה לאורך כל התקופה. " + DISCLAIMER),
    ]


def emergency(expense, hook_title, sub):
    return [
        hook(hook_title, sub),
        numbers("כמה זה בשקלים", f"הוצאות חודשיות של {money(expense)}", [
            ("חודש אחד", money(expense)), ("שלושה חודשים", money(expense * 3)), ("שישה חודשים", money(expense * 6))]),
        lesson("מה זה קרן חירום?", [
            "כסף זמין לדברים שלא תכננת: אובדן עבודה, תיקון, רופא.",
            "כלל אצבע נפוץ: בין שלושה לשישה חודשי הוצאות.",
            "זה כלל כללי. המצב של כל אחד שונה."], note="כלל אצבע, לא ייעוץ אישי."),
    ]


def budget(income, hook_title, sub):
    return [
        hook(hook_title, sub),
        numbers("ככה זה מתחלק", f"משכורת נטו של {money(income)}", [
            ("50% לצרכים", money(income * 0.5)), ("30% לרצונות", money(income * 0.3)), ("20% לחיסכון", money(income * 0.2))]),
        lesson("מה נכנס לאן?", [
            "צרכים: דיור, חשבונות, אוכל, תחבורה.",
            "רצונות: בילויים, קניות, מה שאפשר בלי.",
            "חיסכון: קרן חירום, השקעות, החזר חובות."], note="כלל אצבע נפוץ, לא חוק. כל אחד מתאים אותו לעצמו."),
    ]


def hourly(net_month, hook_title, items=(("קפה", 18), ("משלוח אוכל", 85), ("זוג נעליים", 400))):
    rate = net_month / 182
    rows = []
    for name, price in items:
        mins = price / rate * 60
        rows.append((f"{name} ({money(price)})", f"{mins:.0f} דקות" if mins < 60 else f"{mins / 60:.1f} שעות"))
    return [
        hook(hook_title, f"משכורת נטו של {money(net_month)}, כ־{money(rate)} לשעה."),
        numbers("כמה עבודה זה עולה", "מחיר בדקות ובשעות עבודה", rows, note="לפי 182 שעות עבודה בחודש, בערך."),
        lesson("למה זה שימושי?", [
            "כסף הוא זמן שהשקעת כדי להשיג אותו.",
            "זה לא אומר להפסיק לקנות.",
            "זה עוזר לבחור על מה שווה לעבוד."], note="חישוב מקורב לפי הנחה על שעות עבודה."),
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
add("habit_streaming", habit("חודש", 45, 12, f"מנוי סטרימינג שכמעט לא משתמשים בו. כמה זה {hl('בעשר שנים')}?", "45 שקלים בחודש. נשמע כלום."))
add("habit_taxi", habit("נסיעה", 60, 104, f"מונית פעמיים בשבוע. כמה זה {hl('בשנה')}?", "60 שקלים לנסיעה."))
add("habit_lunch", habit("ארוחה", 55, 250, f"ארוחת צהריים בחוץ בכל יום עבודה. כמה זה {hl('בשנה')}?", "55 שקלים לארוחה."))
add("habit_gym", habit("חודש", 250, 12, f"מנוי חדר כושר שלא הולכים אליו. כמה זה {hl('בעשר שנים')}?", "250 שקלים בחודש."))
add("habit_apps", habit("הזמנה", 120, 24, f"קניות ספונטניות באפליקציות פעמיים בחודש. כמה זה {hl('בשנה')}?", "120 שקלים בכל פעם."))
add("habit_friday", habit("יציאה", 60, 52, f"קפה ומאפה בכל שישי. כמה זה {hl('בעשר שנים')}?", "60 שקלים בשבוע."))
add("monthly_300", monthly(300, 0.04, f"300 שקלים בחודש. כמה יצטברו {hl('ב־30 שנה')}?", "פחות מקפה ביום."))
add("monthly_500", monthly(500, 0.04, f"500 שקלים בחודש. כמה זה {hl('אחרי 30 שנה')}?", "הפקדה קטנה, הרבה זמן."))
add("monthly_1000", monthly(1000, 0.04, f"1,000 שקלים בחודש בצד. כמה זה {hl('אחרי 30 שנה')}?", "בלי להרוויח יותר. רק להתמיד."))
add("monthly_200", monthly(200, 0.05, f"רק 200 שקלים בחודש. כמה זה {hl('אחרי 30 שנה')}?", "סכום שאפשר לא להרגיש."))
add("monthly_400", monthly(400, 0.03, f"400 שקלים בחודש בריבית נמוכה. כמה זה {hl('אחרי 30 שנה')}?", "גם בתשואה צנועה זה גדל."))
add("early_500", start_early(500, 0.04, 25, 35, f"מתחילים לחסוך בגיל 25 או 35? ההבדל {hl('גדול')}", "אותה הפקדה, עשר שנים של פער."))
add("early_300", start_early(300, 0.05, 30, 40, f"עשר שנים של המתנה. כמה הן {hl('עולות לך')}?", "300 שקלים בחודש, התחלה אחרת."))
add("compound_5000", compound(5000, 0.05, f"5,000 שקלים וזמן. כמה זה {hl('אחרי 30 שנה')}?", "בריבית דריבית."))
add("compound_10000", compound(10000, 0.03, f"10,000 שקלים בריבית צנועה. כמה אחרי {hl('30 שנה')}?", "גם 3% בשנה עושה הבדל."))
add("inflation_100_2", inflation(0.02, f"100 שקלים של היום. כמה הם יקנו {hl('בעוד 30 שנה')} באינפלציה של 2%?", "אפילו אינפלציה נמוכה אוכלת כסף."))
add("inflation_100_5", inflation(0.05, f"אינפלציה של 5%. מה קורה ל־100 שקלים {hl('בעוד 20 שנה')}?", "כשהמחירים עולים מהר."))
add("inflation_salary", inflation(0.03, f"משכורת של 10,000 שקלים שלא עולה. מה היא תקנה {hl('בעוד 20 שנה')}?", "כוח הקנייה לא עומד במקום.", amount=10000))
add("rule72", rule72_post(f"כמה זמן לוקח לכסף {hl('להכפיל את עצמו')}?", "יש כלל פשוט אחד."))
add("simple_vs_compound", simple_vs_compound(1000, 0.05, 20, f"ריבית פשוטה או דריבית? ההבדל אחרי {hl('20 שנה')}", "שתי מילים. הפרש גדול."))
add("fees_100k", fees(100000, 0.05, 30, f"עמלה של 2% במקום 0.5%. כמה זה עולה לך {hl('ב־30 שנה')}?", "על 100,000 שקלים. נשמע קטן."))
add("fees_50k", fees(50000, 0.06, 25, f"עמלות קטנות, פער גדול. מה קורה {hl('אחרי 25 שנה')}?", "על 50,000 שקלים בתשואה של 6%."))
add("emergency_8000", emergency(8000, f"כמה כסף צריך להיות בצד ל{hl('יום לא צפוי')}?", "אם ההוצאות החודשיות שלך הן 8,000 שקלים."))
add("emergency_12000", emergency(12000, f"קרן חירום: כמה זה {hl('באמת')} אצלך?", "אם ההוצאות החודשיות הן 12,000 שקלים."))
add("budget_8000", budget(8000, f"כלל 50/30/20: לאן הולכת {hl('המשכורת')}?", "על משכורת נטו של 8,000 שקלים."))
add("budget_15000", budget(15000, f"כלל 50/30/20 על משכורת של {hl('15,000')}", "ככה זה נראה בשקלים."))
add("hourly_8000", hourly(8000, f"כמה זמן אתה צריך {hl('לעבוד')} בשביל קפה, משלוח ונעליים?"))
add("hourly_12000", hourly(12000, f"כמה דקות עבודה עולה {hl('הקפה שלך')}?"))
add("hourly_20000", hourly(20000, f"כמה שעות עבודה עולות {hl('הרגלים קטנים')}?", items=(("קפה", 18), ("ארוחת צהריים", 55), ("מונית", 60))))

ORDER = ["habit_coffee", "compound_1000", "hourly_8000", "habit_delivery", "monthly_500", "inflation_100",
         "early_500", "habit_lunch", "rule72", "fees_100k", "habit_streaming", "budget_8000", "inflation_salary",
         "monthly_300", "habit_taxi", "simple_vs_compound", "emergency_8000", "hourly_12000", "compound_5000",
         "habit_gym", "monthly_1000", "early_300", "habit_apps", "inflation_100_2", "fees_50k", "budget_15000",
         "habit_friday", "monthly_200", "emergency_12000", "compound_10000", "inflation_100_5", "monthly_400",
         "hourly_20000"]
assert set(ORDER) == set(POSTS), set(POSTS) ^ set(ORDER)
POSTS = {k: POSTS[k] for k in ORDER}


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
