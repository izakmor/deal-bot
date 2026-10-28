"""30+ story carousels (9 slides each) built from parameterised templates.
Every number is computed here. Importing this module registers the stories into
story_cards.STORIES in the final publishing order."""
import story_art as A
import story_cards as sc
from story_cards import bars, cards, chips, money, pile, hero_art

N = 9
TAKE = "<p><b style='font-weight:800'>{a}</b> {a2}</p><p><b style='font-weight:800'>{b}</b> {b2}</p>" \
       "<p><b style='font-weight:800'>שמרו לפוסט</b> ושלחו למי שצריך לשמוע את זה.</p>"


def S(series):
    return lambda *a, **k: sc.slide(*a, series=series, **k)


def tsize(title):
    return 100 if len(title) <= 34 else 88


def bold(t):
    return f"<b style='font-weight:800'>{t}</b>"


# ---------------------------------------------------------------- habits
def habit_story(unit, price, per_year, freq, title, sub, alt_sentence, alt_price, alt_share, alt_foot, rate=0.07, icon="cup"):
    month, year, ten = price * per_year / 12, price * per_year, price * per_year * 10
    grown = sc.fv_monthly(month, rate, 10)
    save = per_year * alt_share * (price - alt_price)
    sl = S("הרגלים קטנים")
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.scene_hero(icon), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "קודם, ההנחות",
           chips(("מחיר", money(price)), ("כמה", freq), ("תקופה", "10 שנים")) +
           "<p>לא נבקש ממך לוותר על כלום. רק להסתכל על המספר.</p><p>כל מספר בהמשך מחושב מהנתונים האלה.</p>",
           foot="הנתונים הם דוגמה. כל אחד ישנה אותם לפי ההרגל שלו.", top=340),
        sl(3, N, "בפעם אחת זה לא מרגיש",
           cards((f"כל {unit}", money(price)), ("בחודש", money(month))) +
           f"<p>{money(month)} בחודש. לא סכום שעוצר אותך באמצע.</p>", A.scene_single(icon), art_bottom=150),
        sl(4, N, "בשנה כבר רואים משהו",
           cards(("בשנה", money(year)), ("בשנתיים", money(year * 2))) +
           f"<p>{money(year)} בשנה, על משהו שהפך להרגל.</p>", A.scene_grid(icon), art_bottom=150),
        sl(5, N, "בשלוש שנים זה סכום",
           cards(("אחרי 3 שנים", money(year * 3)), ("בחודש", money(month))) +
           f"<p>{money(year * 3)}. אותו הרגל, רק עם יותר אפסים.</p>", A.scene_pyramid(icon), art_bottom=150),
        sl(6, N, "בעשר שנים מגיע המספר",
           cards(("אחרי 10 שנים", money(ten)), ("בשנה", money(year))) +
           f"<p>{money(ten)}. זה הסכום שעבר מהכיס שלך, בלי שהרגשת.</p>", A.scene_mountain(icon), art_bottom=130),
        sl(7, N, "ואם הכסף הזה היה עובד?",
           cards(("הפקדת", money(ten)), ("יש לך", money(grown))) +
           f"<p>אם היית מפקיד את אותו סכום כל חודש, בתשואה לדוגמה של {rate * 100:.0f}% בשנה, "
           f"הריבית הייתה מוסיפה {money(grown - ten)}.</p>",
           sc.sprout_coin(), art_bottom=210, foot=f"התשואה היא דוגמה, לא הבטחה. {rate * 100:.0f}% בשנה היא הנחה אופטימית, ובפועל יכולות להיות גם שנים של הפסד."),
        sl(8, N, "אפשר גם בלי לוותר על הכול",
           f"<p>{alt_sentence.format(save=bold(money(save)))}</p>",
           bars(year, year - save, "כמו היום", "אחרי ההחלפה"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="הרגל קטן הוא לא קטן.", a2="הוא רק נראה ככה בפעם אחת.",
                       b="לא צריך לוותר על כלום.", b2="מספיק לדעת כמה זה עולה, ולהחליט."),
           foot=f"המספרים הם דוגמה לפי {money(price)} ל{unit}. {alt_foot} לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- start early
def early_story(pmt, rate, a1, a2, retire=65):
    val = lambda age, start: sc.fv_monthly(pmt, rate, max(0, age - start)) if age > start else 0
    dep = lambda age, start: pmt * 12 * max(0, age - start)
    title = f"מתחילים לחסוך בגיל {a1} או בגיל {a2}? ההבדל גדול"
    sub = f"אותה הפקדה של {pmt} שקלים בחודש, רק התחלה אחרת."
    sl = S("חיסכון לטווח ארוך")
    mid = (a2 + retire) // 2
    e65, l65 = val(retire, a1), val(retire, a2)
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', hero_art(), art_bottom=150, title_size=88),
        sl(2, N, "שני אנשים, אותה הפקדה",
           chips(("הפקדה בחודש", money(pmt)), ("תשואה לדוגמה", f"{rate * 100:.0f}% בשנה"), ("עד גיל", str(retire))) +
           f"<p>אחד מתחיל בגיל {a1}, השני בגיל {a2}. שניהם מפקידים בדיוק אותו סכום.</p>",
           foot="התשואה היא דוגמה. בפועל היא משתנה, ויכולות להיות גם שנים של ירידות.", top=340),
        sl(3, N, f"בגיל {a2} רק אחד מהם התחיל",
           cards(("המקדים: הפקיד", money(dep(a2, a1))), ("המקדים: יש לו", money(val(a2, a1)))) +
           f"<p>המאחר עוד לא הפקיד שקל. למקדים כבר יש {money(val(a2, a1))}.</p>", sc.tree(1), art_bottom=150),
        sl(4, N, f"בגיל {a2 + 10} השני כבר בדרך",
           cards(("המקדים", money(val(a2 + 10, a1))), ("המאחר", money(val(a2 + 10, a2)))) +
           f"<p>המאחר הפקיד {money(dep(a2 + 10, a2))} ויש לו {money(val(a2 + 10, a2))}. המקדים עדיין רחוק קדימה.</p>",
           sc.tree(1), art_bottom=150),
        sl(5, N, f"בגיל {mid} הפער גדל",
           cards(("המקדים", money(val(mid, a1))), ("המאחר", money(val(mid, a2)))) +
           f"<p>ההפרש כבר {money(val(mid, a1) - val(mid, a2))}.</p>", sc.tree(2), art_bottom=150),
        sl(6, N, f"בגיל {retire} מגיע המספר",
           cards(("המקדים", money(e65)), ("המאחר", money(l65))) +
           f"<p>המקדים הפקיד {money(dep(retire, a1))}, המאחר {money(dep(retire, a2))}.</p>", sc.tree(3), art_bottom=150),
        sl(7, N, "ומה עלתה ההמתנה?",
           cards(("ההפרש", money(e65 - l65)), ("שנות המתנה", str(a2 - a1))) +
           f"<p>המתנה של {a2 - a1} שנים עולה בערך {money(e65 - l65)} בסוף הדרך.</p>",
           foot="ההנחה: הפקדה קבועה כל חודש ותשואה קבועה. בפועל זה משתנה."),
        sl(8, N, "בתמונה אחת",
           f"<p>אותה הפקדה. ההבדל היחיד הוא מתי התחלת.</p>",
           bars(e65, l65, f"התחלה בגיל {a1}", f"התחלה בגיל {a2}"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="הזמן הוא החלק החזק.", a2="בדוגמה הזאת, ההתחלה המוקדמת עשתה את רוב ההבדל.",
                       b="לא מאחרים להתחיל.", b2="גם התחלה מאוחרת עדיין עדיפה על לא להתחיל."),
           foot="כל המספרים הם דוגמה בלבד. אין כאן הבטחה, והשקעה כרוכה בסיכון. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- inflation
def inflation_story(rate, amount, title, sub):
    f = lambda y: amount / (1 + rate) ** y
    need = lambda y: amount * (1 + rate) ** y
    sl = S("אינפלציה")
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.scene_basket_tag(), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "קודם, ההנחה",
           chips(("סכום היום", money(amount)), ("אינפלציה לדוגמה", f"{rate * 100:.0f}% בשנה"), ("תקופה", "30 שנה")) +
           "<p>אינפלציה היא עלייה כללית במחירים. אותו סכום קונה פחות עם הזמן.</p>",
           foot="האינפלציה האמיתית משתנה משנה לשנה. כאן היא קבועה, לצורך הדוגמה.", top=340),
        sl(3, N, "אחרי 5 שנים עוד לא מרגישים",
           cards(("היום", money(amount)), ("אחרי 5 שנים", money(f(5)))) +
           f"<p>אותו כסף קונה בערך {money(f(5))} במחירים של היום.</p>", A.scene_basket(f(5) / amount), art_bottom=150),
        sl(4, N, "אחרי 10 שנים זה בולט",
           cards(("היום", money(amount)), ("אחרי 10 שנים", money(f(10)))) +
           f"<p>כוח הקנייה ירד ל־{f(10) / amount * 100:.0f}% ממה שהיה.</p>", A.scene_basket(f(10) / amount), art_bottom=150),
        sl(5, N, "אחרי 20 שנה אפשר לראות את זה בסופר",
           cards(("היום", money(amount)), ("אחרי 20 שנה", money(f(20)))) +
           f"<p>נשארו {f(20) / amount * 100:.0f}% מכוח הקנייה המקורי.</p>", A.scene_basket(f(20) / amount), art_bottom=150),
        sl(6, N, f"אחרי 30 שנה נשאר רק {f(30) / amount * 100:.0f}%",
           cards(("היום", money(amount)), ("אחרי 30 שנה", money(f(30)))) +
           f"<p>במחירים של היום, הסכום הזה שווה רק {money(f(30))}.</p>", A.scene_basket(f(30) / amount), art_bottom=150),
        sl(7, N, "ומה צריך כדי לשמור על הערך?",
           cards(("היום", money(amount)), ("בעוד 20 שנה", money(need(20)))) +
           f"<p>כדי לקנות בעוד 20 שנה את מה שהסכום קונה היום, צריך כ־{money(need(20))}.</p>",
           foot="זה לא המלצה להשקיע. זה רק המחשה של מה שקורה לסכום שעומד."),
        sl(8, N, "בתמונה אחת",
           f"<p>אותו סכום, אחרי 20 שנה, בכוח קנייה של היום.</p>",
           bars(amount, f(20), "היום", "אחרי 20 שנה"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="כסף שעומד לא נשאר אותו דבר.", a2="המחירים עולים, והכסף אותו הדבר.",
                       b="שווה לדעת מה קורה לכסף שלך.", b2="לא כל אחד צריך לעשות משהו, אבל כדאי להבין."),
           foot=f"דוגמה לפי אינפלציה קבועה של {rate * 100:.0f}% בשנה. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- fees
def fees_story(principal, gross, years, title, sub):
    levels = (0.005, 0.01, 0.02)
    v = [principal * (1 + gross - f) ** years for f in levels]
    sl = S("עמלות")
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.coin_bite(), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "קודם, ההנחות",
           chips(("סכום", money(principal)), ("תשואה לפני עמלה", f"{gross * 100:.0f}% בשנה"), ("תקופה", f"{years} שנה")) +
           "<p>אותה השקעה. ההבדל היחיד הוא כמה משלמים כל שנה על ניהול.</p>",
           foot="דמי ניהול משתנים בין מוצרים. כאן הם קבועים, לצורך הדוגמה.", top=340),
        sl(3, N, "עמלה של חצי אחוז",
           cards(("הפקדת", money(principal)), (f"אחרי {years} שנה", money(v[0]))) +
           f"<p>עם עמלה של 0.5% בשנה, הסכום מגיע ל־{money(v[0])}.</p>", sc.tree(3), art_bottom=150),
        sl(4, N, "עמלה של אחוז",
           cards(("הפקדת", money(principal)), (f"אחרי {years} שנה", money(v[1]))) +
           f"<p>עם עמלה של 1% בשנה: {money(v[1])}. כבר {money(v[0] - v[1])} פחות.</p>", sc.tree(2), art_bottom=150),
        sl(5, N, "עמלה של שני אחוזים",
           cards(("הפקדת", money(principal)), (f"אחרי {years} שנה", money(v[2]))) +
           f"<p>עם עמלה של 2% בשנה: {money(v[2])}.</p>", sc.tree(1), art_bottom=150),
        sl(6, N, "ההפרש הכולל",
           cards(("ההפרש", money(v[0] - v[2])), ("באחוז", f"{(1 - v[2] / v[0]) * 100:.0f}%")) +
           f"<p>הפער בין 0.5% ל־2% הוא {money(v[0] - v[2])}, על אותה השקעה בדיוק.</p>"),
        sl(7, N, "למה זה קורה?",
           "<p>העמלה לא נגבית פעם אחת. היא נגרעת מהתשואה כל שנה.</p>"
           "<p>בשנה הבאה היא נגרעת גם ממה שהיה אמור לצמוח על הכסף שכבר נגרע.</p>",
           foot="דמי ניהול קיימים בקופות גמל, בקרנות ובתיקים מנוהלים. כדאי לשאול כמה משלמים.", top=340),
        sl(8, N, "בתמונה אחת",
           f"<p>אותה השקעה. עמלה אחרת.</p>", bars(v[0], v[2], "עמלה 0.5%", "עמלה 2%"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="עמלה קטנה היא לא קטנה.", a2="היא נראית כלום בשנה אחת.",
                       b="שווה לשאול כמה משלמים.", b2="זו שאלה פשוטה, והתשובה שווה כסף."),
           foot="המספרים הם דוגמה. אין כאן המלצה על מוצר. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- emergency fund
def emergency_story(expense, title, sub):
    sl = S("קרן חירום")
    m3, m6 = expense * 3, expense * 6
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.umbrella(2), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "מה זה קרן חירום?",
           "<p>כסף שמחכה בצד לדברים שלא תכננת: אובדן עבודה, תיקון דחוף, הוצאה רפואית.</p>"
           "<p>המטרה היא לא להרוויח ממנו, אלא שלא תהיה חייב ללוות כשזה קורה.</p>",
           foot="הסבר כללי. המצב של כל אחד שונה.", top=340),
        sl(3, N, "קודם, מה ההוצאות שלך",
           chips(("הוצאות בחודש", money(expense)), ("בשנה", money(expense * 12)), ("ביום", money(expense / 30))) +
           "<p>הנתון החשוב הוא ההוצאות, לא ההכנסה. הוא קובע כמה זמן הכסף יחזיק.</p>", top=340),
        sl(4, N, "חודש אחד",
           cards(("הוצאות", money(expense)), ("מספיק ל", "חודש")) +
           "<p>זה מה שצריך כדי לעבור חודש בלי הכנסה.</p>", A.umbrella(1), art_bottom=150),
        sl(5, N, "שלושה חודשים",
           cards(("סכום", money(m3)), ("מספיק ל", "3 חודשים")) +
           "<p>זה הרף התחתון של כלל האצבע הנפוץ.</p>", A.umbrella(2), art_bottom=150),
        sl(6, N, "שישה חודשים",
           cards(("סכום", money(m6)), ("מספיק ל", "6 חודשים")) +
           "<p>זה הרף העליון של אותו כלל, למי שרוצה יותר ביטחון.</p>", A.umbrella(4), art_bottom=150),
        sl(7, N, "איך בונים את זה?",
           cards(("בחודש", money(m3 / 12)), ("אחרי שנה", money(m3))) +
           f"<p>אם מפקידים {money(m3 / 12)} בחודש, אחרי שנה יש שלושה חודשי הוצאות בצד.</p>",
           foot="הדוגמה מניחה שההוצאות לא משתנות."),
        sl(8, N, "בתמונה אחת",
           "<p>שלושה חודשים מול שישה חודשים.</p>", bars(m6, m3, "שישה חודשים", "שלושה חודשים"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="קרן חירום היא ביטוח לשקט.", a2="לא להשקעה.",
                       b="מתחילים מסכום קטן.", b2="כל חודש בצד הוא חודש של ביטחון."),
           foot="כלל אצבע נפוץ, לא ייעוץ אישי ולא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- budget 50/30/20
def budget_story(income, title, sub):
    sl = S("תקציב")
    need, want, sav = income * 0.5, income * 0.3, income * 0.2
    f10 = sc.fv_monthly(sav, 0.05, 10)
    h10 = sc.fv_monthly(income * 0.1, 0.05, 10)
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.pie(), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "הכלל בשורה אחת",
           "<p>חמישים אחוז לצרכים, שלושים אחוז לרצונות ועשרים אחוז לחיסכון.</p>"
           "<p>זה כלל אצבע נפוץ, לא חוק. כל אחד מתאים אותו לעצמו.</p>",
           foot=f"הדוגמה: משכורת נטו של {money(income)}.", top=340),
        sl(3, N, "חמישים אחוז: צרכים",
           cards(("בחודש", money(need)), ("מהמשכורת", "50%")) +
           "<p>דיור, חשבונות, אוכל, תחבורה. מה שחייבים לשלם כדי לחיות.</p>", A.pie(0), art_bottom=150),
        sl(4, N, "שלושים אחוז: רצונות",
           cards(("בחודש", money(want)), ("מהמשכורת", "30%")) +
           "<p>בילויים, קניות, מנויים. מה שאפשר גם בלעדיו, אבל נעים שיש.</p>", A.pie(1), art_bottom=150),
        sl(5, N, "עשרים אחוז: חיסכון",
           cards(("בחודש", money(sav)), ("מהמשכורת", "20%")) +
           "<p>קרן חירום, חיסכון לטווח ארוך, החזר חובות.</p>", A.pie(2), art_bottom=150),
        sl(6, N, "מה זה עושה בעשר שנים?",
           cards(("הפקדת", money(sav * 120)), ("יש לך", money(f10))) +
           f"<p>{money(sav)} בחודש, בתשואה לדוגמה של 5% בשנה, מגיעים ל־{money(f10)}.</p>",
           sc.sprout_coin(), art_bottom=170),
        sl(7, N, "ואם זה לא מסתדר?",
           "<p>לא כולם יכולים עשרים אחוז. זה בסדר.</p>"
           "<p>אפשר להתחיל מעשרה אחוז, ולהעלות כשיש עוד מקום.</p>",
           foot="הכלל הוא נקודת התחלה, לא מבחן.", top=340),
        sl(8, N, "עשרה אחוז מול עשרים אחוז",
           f"<p>אותה משכורת, אחרי עשר שנים.</p>", bars(f10, h10, "20% חיסכון", "10% חיסכון"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="עדיף חיסכון קטן שקורה.", a2="מחיסכון מושלם שנשאר בתכנון.",
                       b="כלל אצבע הוא רק התחלה.", b2="כדאי להתאים אותו לחיים שלך."),
           foot="כלל אצבע נפוץ. התשואה היא דוגמה, לא הבטחה. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- hours of work
def hourly_story(net, title, sub):
    rate = net / 182
    cost = lambda price: price / rate
    fmt = lambda h: f"{h * 60:.0f} דקות" if h < 1 else f"{h:.1f} שעות"
    sl = S("זמן וכסף")
    year_coffee = 18 * 365
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.clock(10 + 10 / 60), art_bottom=150, title_size=tsize(title)),
        sl(2, N, "קודם, מה שווה שעה שלך",
           chips(("משכורת נטו", money(net)), ("שעות בחודש", "182"), ("שעה", money(rate))) +
           "<p>זה חישוב מקורב. הוא נותן דרך אחרת להסתכל על מחירים.</p>",
           foot="182 שעות עבודה בחודש הן הנחה מקובלת. כל אחד ישנה לפי המצב שלו.", top=340),
        sl(3, N, "קפה ומשלוח",
           cards(("קפה, 18 ש\"ח", fmt(cost(18))), ("משלוח, 85 ש\"ח", fmt(cost(85)))) +
           "<p>בדקות עבודה, אלה עדיין דברים קטנים.</p>", A.clock(cost(85)), art_bottom=150),
        sl(4, N, "נעליים וטלפון",
           cards(("נעליים, 400 ש\"ח", fmt(cost(400))), ("טלפון, 3,000 ש\"ח", fmt(cost(3000)))) +
           "<p>כאן כבר מדברים על שעות ועל ימי עבודה.</p>", A.clock(cost(3000)), art_bottom=150),
        sl(5, N, "חופשה",
           cards(("חופשה, 8,000 ש\"ח", f"{cost(8000) / 8:.1f} ימים"), ("בשעות", f"{cost(8000):.0f}")) +
           f"<p>חופשה של 8,000 שקלים שווה בערך {cost(8000) / 8:.1f} ימי עבודה (ביום של 8 שעות).</p>", sc.calendar_art(), art_bottom=150),
        sl(6, N, "ההרגל היומי",
           cards(("קפה כל יום, בשנה", money(year_coffee)), ("בשעות עבודה", f"{cost(year_coffee):.0f}")) +
           f"<p>קפה כל יום לאורך שנה הוא בערך {cost(year_coffee) / 8:.0f} ימי עבודה.</p>", sc.coin_mountain(), art_bottom=130),
        sl(7, N, "למה זה שימושי?",
           "<p>כסף הוא זמן שהשקעת כדי להשיג אותו.</p><p>זה לא אומר להפסיק לקנות. זה עוזר לבחור על מה שווה לעבוד.</p>",
           foot="חישוב מקורב לפי הנחה על שעות עבודה.", top=340),
        sl(8, N, "בתמונה אחת",
           "<p>קפה יומי לאורך שנה, מול החופשה.</p>", bars(year_coffee, 8000, "קפה כל יום, שנה", "חופשה"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="כל קנייה עולה גם זמן.", a2="לפעמים הוא שווה את זה, ולפעמים לא.",
                       b="ההרגלים הקטנים הם הכבדים.", b2="לא כי הם יקרים, אלא כי הם חוזרים."),
           foot=f"דוגמה לפי משכורת נטו של {money(net)}. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- rule 72
def rule72_story():
    title, sub = "כמה זמן לוקח לכסף להכפיל את עצמו?", "יש כלל פשוט אחד שאפשר לעשות בראש."
    sl = S("ריבית דריבית")
    yrs = lambda r: 72 / r
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.coin_pair(), art_bottom=150, title_size=100),
        sl(2, N, "הכלל",
           "<p>מחלקים 72 בריבית השנתית.</p><p>התוצאה היא בערך מספר השנים עד שהכסף מוכפל.</p>",
           foot="קירוב מקובל, לא חישוב מדויק. ההנחה: ריבית קבועה.", top=340),
        sl(3, N, "ריבית של 2%",
           cards(("72 ÷ 2", f"{yrs(2):.0f} שנים"), ("1,000 שקלים", "2,000 שקלים")) +
           "<p>בריבית נמוכה, ההכפלה לוקחת הרבה זמן.</p>", sc.tree(0), art_bottom=150),
        sl(4, N, "ריבית של 4%",
           cards(("72 ÷ 4", f"{yrs(4):.0f} שנים"), ("1,000 שקלים", "2,000 שקלים")) +
           "<p>ריבית כפולה, חצי מהזמן.</p>", sc.tree(1), art_bottom=150),
        sl(5, N, "ריבית של 6%",
           cards(("72 ÷ 6", f"{yrs(6):.0f} שנים"), ("1,000 שקלים", "2,000 שקלים")) +
           "<p>כבר שתי הכפלות בערך ב־24 שנה.</p>", sc.tree(2), art_bottom=150),
        sl(6, N, "ריבית של 8%",
           cards(("72 ÷ 8", f"{yrs(8):.0f} שנים"), ("1,000 שקלים", "2,000 שקלים")) +
           "<p>ריבית גבוהה כזאת היא הנחה אופטימית, אבל היא מראה את ההבדל.</p>", sc.tree(3), art_bottom=150),
        sl(7, N, "וזה עובד גם הפוך",
           cards(("אינפלציה של 3%", f"{yrs(3):.0f} שנים"), ("מחירים", "מוכפלים")) +
           "<p>באינפלציה של 3% בשנה, מחירים מכפילים את עצמם בערך ב־24 שנה.</p>", A.scene_basket(0.5), art_bottom=150),
        sl(8, N, "בתמונה אחת",
           "<p>כמה שנים צריך לכל ריבית.</p>", bars(yrs(2), yrs(8), "ריבית 2%", "ריבית 8%"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="72 לחלק לריבית.", a2="חישוב של שתי שניות.",
                       b="עובד גם על אינפלציה.", b2="אותו כלל, כיוון הפוך."),
           foot="קירוב מקובל, לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- simple vs compound
def simple_story(amount=1000, rate=0.05):
    title, sub = "ריבית פשוטה או ריבית דריבית?", "שתי מילים, והפרש של מאות שקלים."
    sl = S("ריבית דריבית")
    s_ = lambda y: amount * (1 + rate * y)
    c_ = lambda y: amount * (1 + rate) ** y
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', hero_art(), art_bottom=150, title_size=100),
        sl(2, N, "ההנחות",
           chips(("סכום", money(amount)), ("ריבית", f"{rate * 100:.0f}% בשנה"), ("תקופה", "30 שנה")) +
           "<p>נשווה בין שתי שיטות לחשב ריבית על אותו סכום.</p>", top=340),
        sl(3, N, "ריבית פשוטה: איך זה עובד",
           "<p>הריבית מחושבת רק על הסכום המקורי.</p>"
           f"<p>כל שנה מוסיפים {money(amount * rate)}, בלי שינוי.</p>", A.stairs("simple"), art_bottom=150, top=380),
        sl(4, N, "ריבית דריבית: איך זה עובד",
           "<p>הריבית נוספת לקרן, ואז גם עליה מקבלים ריבית.</p>"
           "<p>כל שנה מוסיפים קצת יותר מהשנה שלפניה.</p>", A.stairs("compound"), art_bottom=150, top=380),
        sl(5, N, "אחרי 10 שנים",
           cards(("פשוטה", money(s_(10))), ("דריבית", money(c_(10)))) +
           f"<p>ההפרש עדיין קטן: {money(c_(10) - s_(10))}.</p>", sc.tree(1), art_bottom=150),
        sl(6, N, "אחרי 20 שנה",
           cards(("פשוטה", money(s_(20))), ("דריבית", money(c_(20)))) +
           f"<p>ההפרש כבר {money(c_(20) - s_(20))}.</p>", sc.tree(2), art_bottom=150),
        sl(7, N, "אחרי 30 שנה",
           cards(("פשוטה", money(s_(30))), ("דריבית", money(c_(30)))) +
           f"<p>ההפרש {money(c_(30) - s_(30))}. הדריבית גבוהה ב־{(c_(30) / s_(30) - 1) * 100:.0f}% מהפשוטה.</p>", sc.tree(3), art_bottom=150),
        sl(8, N, "בתמונה אחת",
           "<p>אותו סכום ואותה ריבית. שיטה אחרת.</p>", bars(c_(30), s_(30), "ריבית דריבית", "ריבית פשוטה"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="דריבית מנצחת עם הזמן.", a2="בהתחלה ההבדל קטן, ובסוף הוא גדול.",
                       b="שווה לדעת איזו שיטה חלה עליך.", b2="במוצרים שונים הריבית מחושבת אחרת."),
           foot="הדוגמה מניחה ריבית קבועה לכל התקופה. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- child savings
def child_story(pmt=100, rate=0.05):
    title, sub = f"{pmt} שקלים בחודש מהיום שילד נולד. כמה זה אחרי 18 שנה?", "מה קורה אם משאירים את זה עוד קצת?"
    sl = S("חיסכון לילד")
    f18 = sc.fv_monthly(pmt, rate, 18)
    f40 = f18 * (1 + rate) ** 22
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.piggy(), art_bottom=150, title_size=84),
        sl(2, N, "ההנחות",
           chips(("הפקדה בחודש", money(pmt)), ("תשואה לדוגמה", f"{rate * 100:.0f}% בשנה"), ("עד גיל", "18")) +
           "<p>הפקדה קטנה וקבועה, בלי לגעת.</p>",
           foot="התשואה היא דוגמה. בפועל היא משתנה, ויכולות להיות גם שנים של ירידות.", top=340),
        sl(3, N, "אחרי 5 שנים",
           cards(("הפקדת", money(pmt * 60)), ("יש", money(sc.fv_monthly(pmt, rate, 5)))) +
           "<p>בגיל 5 עוד לא רואים הרבה.</p>", sc.tree(0), art_bottom=150),
        sl(4, N, "אחרי 10 שנים",
           cards(("הפקדת", money(pmt * 120)), ("יש", money(sc.fv_monthly(pmt, rate, 10)))) +
           "<p>הקו מתחיל לעלות.</p>", sc.tree(1), art_bottom=150),
        sl(5, N, "בגיל 18",
           cards(("הפקדת", money(pmt * 216)), ("יש", money(f18))) +
           f"<p>הריבית הוסיפה {money(f18 - pmt * 216)}.</p>", sc.tree(2), art_bottom=150),
        sl(6, N, "ואם לא נוגעים עוד 22 שנה?",
           cards(("בגיל 18", money(f18)), ("בגיל 40", money(f40))) +
           "<p>בלי להפקיד שקל נוסף, רק עם הזמן.</p>", sc.tree(3), art_bottom=150),
        sl(7, N, "עשרים ושתיים שנה בלי להפקיד שקל",
           cards(("ההפרש", money(f40 - f18)), ("בלי הפקדות", "0")) +
           f"<p>{money(f40 - f18)} נוספו רק מהזמן.</p>",
           foot="ההנחה: אין משיכות ואין שינוי בתשואה."),
        sl(8, N, "בתמונה אחת",
           "<p>אותה הפקדה, שני גילאים.</p>", bars(f40, f18, "בגיל 40", "בגיל 18"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="הזמן עושה את העבודה.", a2="גם הפקדה קטנה, כשהיא מתחילה מוקדם.",
                       b="לא חייבים סכום גדול.", b2="חשוב שיהיה קבוע."),
           foot="כל המספרים הם דוגמה. אין כאן הבטחה. לא ייעוץ השקעות.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- salary raise vs inflation
def raise_story(salary=10000, raise_=0.03, infl=0.04):
    title, sub = "קיבלת העלאה של 3% בשנה. האם באמת הרווחת יותר?", "תלוי מה קרה למחירים."
    sl = S("משכורת")
    nom = lambda y: salary * (1 + raise_) ** y
    real = lambda y: salary * ((1 + raise_) / (1 + infl)) ** y
    slides = [
        sl(1, N, title, f'<p style="font-size:46px">{sub}</p>', A.scene_raise(1.34, 0.9), art_bottom=150, title_size=84),
        sl(2, N, "ההנחות",
           chips(("משכורת", money(salary)), ("העלאה בשנה", f"{raise_ * 100:.0f}%"), ("אינפלציה", f"{infl * 100:.0f}% בשנה")) +
           "<p>נשווה בין המספר בתלוש לבין מה שאפשר לקנות איתו.</p>",
           foot="המספרים הם דוגמה. האינפלציה וההעלאות האמיתיות משתנות.", top=340),
        sl(3, N, "אחרי 5 שנים",
           cards(("בתלוש", money(nom(5))), ("בכוח קנייה", money(real(5)))) +
           "<p>בתלוש יש יותר. בסופר, פחות.</p>", A.scene_raise(nom(5) / salary, real(5) / salary), art_bottom=150),
        sl(4, N, "אחרי 10 שנים",
           cards(("בתלוש", money(nom(10))), ("בכוח קנייה", money(real(10)))) +
           f"<p>בתלוש {money(nom(10))}, אבל בכוח קנייה של היום זה {money(real(10))}.</p>", A.scene_raise(nom(10) / salary, real(10) / salary), art_bottom=150),
        sl(5, N, "אחרי 20 שנה",
           cards(("בתלוש", money(nom(20))), ("בכוח קנייה", money(real(20)))) +
           f"<p>הפער בין המספר בתלוש למה שהוא קונה הולך וגדל.</p>", A.scene_raise(nom(20) / salary, real(20) / salary), art_bottom=150),
        sl(6, N, "מה המשמעות?",
           f"<p>כשההעלאה ({raise_ * 100:.0f}%) נמוכה מהאינפלציה ({infl * 100:.0f}%), קונים פחות מדי שנה.</p>"
           "<p>גם אם המספר בתלוש גדל.</p>", top=340),
        sl(7, N, "ואם ההעלאה שווה לאינפלציה?",
           cards(("בתלוש", money(salary * 1.04 ** 10)), ("בכוח קנייה", money(salary))) +
           "<p>אז נשארים באותו מקום. העלאה אמיתית היא מה שמעל האינפלציה.</p>",
           foot="דוגמה: העלאה ואינפלציה של 4% בשנה."),
        sl(8, N, "בתמונה אחת",
           "<p>אותה משכורת, אחרי 10 שנים.</p>", bars(nom(10), real(10), "המספר בתלוש", "מה שהוא קונה"), art_bottom=150),
        sl(9, N, "מה לוקחים מזה?",
           TAKE.format(a="לא רק המספר בתלוש חשוב.", a2="גם מה שהוא קונה.",
                       b="העלאה אמיתית היא מעל האינפלציה.", b2="שווה לבדוק מול מה שקרה למחירים."),
           foot="הדוגמה מניחה שיעורים קבועים. לא ייעוץ אישי.", top=340),
    ]
    return slides, title, sub


# ---------------------------------------------------------------- registration
ICON = {"habit_delivery": "bag", "habit_lunch": "lunch", "habit_streaming": "tv", "habit_gym": "dumbbell",
        "habit_taxi": "taxi", "habit_apps": "phone", "habit_friday": "cup", "habit_water": "bottle"}


def _habit(slug, *a, **k):
    return slug, (lambda: habit_story(*a, icon=ICON[slug], **k))


REG = dict([
    ("story_compound", sc.compound_story),
    ("story_coffee", sc.coffee_story),
    _habit("habit_delivery", "משלוח", 85, 104, "פעמיים בשבוע", "משלוח אוכל פעמיים בשבוע. כמה זה באמת?",
           "85 שקלים למשלוח. נחשב.",
           "אם מחליפים חצי מהמשלוחים בארוחה בבית (בערך ₪40), חוסכים בערך {save} בשנה.", 40, 0.5, "ארוחה בבית: ₪40 (הנחה)."),
    _habit("habit_lunch", "ארוחה", 55, 250, "כל יום עבודה", "ארוחת צהריים בחוץ בכל יום עבודה. כמה זה בשנה?",
           "55 שקלים לארוחה. נראה כלום.",
           "אם מביאים אוכל מהבית ב־40% מהימים (בערך ₪15 לארוחה), חוסכים בערך {save} בשנה.", 15, 0.4, "אוכל מהבית: ₪15 (הנחה)."),
    _habit("habit_streaming", "חודש", 45, 12, "כל חודש", "מנוי שכמעט לא משתמשים בו. כמה הוא עולה בעשור?",
           "45 שקלים בחודש. נשמע כלום.",
           "אם מבטלים את המנוי, חוסכים {save} בשנה.", 0, 1.0, "ביטול המנוי חוסך את מלוא הסכום."),
    _habit("habit_gym", "חודש", 250, 12, "כל חודש", "מנוי חדר כושר שלא הולכים אליו. כמה זה בעשור?",
           "250 שקלים בחודש. כמה פעמים באמת הולכים?",
           "אם עוברים למנוי זול יותר (בערך ₪120 בחודש), חוסכים בערך {save} בשנה.", 120, 1.0, "מנוי חלופי: ₪120 לחודש (הנחה)."),
    _habit("habit_taxi", "נסיעה", 60, 104, "פעמיים בשבוע", "מונית פעמיים בשבוע. כמה זה בשנה?",
           "60 שקלים לנסיעה.",
           "אם מחליפים חצי מהנסיעות בתחבורה ציבורית (בערך ₪10 לנסיעה), חוסכים בערך {save} בשנה.", 10, 0.5, "תחבורה ציבורית: ₪10 (הנחה)."),
    _habit("habit_apps", "הזמנה", 120, 24, "פעמיים בחודש", "קניות ספונטניות באפליקציות. כמה זה בשנה?",
           "120 שקלים בכל פעם.",
           "אם מוותרים על חצי מההזמנות, חוסכים בערך {save} בשנה.", 0, 0.5, "הדוגמה מניחה שמוותרים על חצי מההזמנות."),
    _habit("habit_friday", "יציאה", 60, 52, "כל שישי", "קפה ומאפה בכל שישי. כמה זה בעשור?",
           "60 שקלים בשבוע.",
           "אם מחליפים חצי מהיציאות בקפה בבית (בערך ₪20), חוסכים בערך {save} בשנה.", 20, 0.5, "קפה בבית: ₪20 (הנחה)."),
    _habit("habit_water", "בקבוק", 8, 250, "כל יום עבודה", "בקבוק מים בחנות בכל יום. כמה זה בעשור?",
           "8 שקלים לבקבוק. מי סופר?",
           "אם עוברים לבקבוק רב־פעמי ב־80% מהימים, חוסכים בערך {save} בשנה.", 1, 0.8, "בקבוק רב־פעמי: עלות של כשקל ליום (הנחה)."),
    ("compound_300", lambda: sc.compound_story(300, 0.05)),
    ("compound_1000", lambda: sc.compound_story(1000, 0.05)),
    ("compound_200", lambda: sc.compound_story(200, 0.04)),
    ("compound_800", lambda: sc.compound_story(800, 0.06)),
    ("early_500", lambda: early_story(500, 0.05, 25, 35)),
    ("early_300", lambda: early_story(300, 0.05, 30, 40)),
    ("inflation_1000", lambda: inflation_story(0.03, 1000, "1,000 שקלים של היום. כמה הם יקנו בעוד 20 שנה?", "הכסף נשאר אותו כסף. המחירים לא.")),
    ("inflation_5000", lambda: inflation_story(0.02, 5000, "5,000 שקלים בצד. מה קורה להם בעשרות שנים?", "גם אינפלציה נמוכה עושה עבודה.")),
    ("inflation_10000", lambda: inflation_story(0.04, 10000, "משכורת של 10,000 שקלים שלא עולה. מה היא תקנה בעוד 20 שנה?", "כוח הקנייה לא עומד במקום.")),
    ("fees_100k", lambda: fees_story(100000, 0.05, 30, "עמלה של 2% במקום 0.5%. כמה זה עולה לך?", "על 100,000 שקלים. נשמע קטן.")),
    ("fees_50k", lambda: fees_story(50000, 0.06, 25, "עמלות קטנות, פער גדול. מה קורה אחרי 25 שנה?", "על 50,000 שקלים בתשואה של 6%.")),
    ("emergency_8000", lambda: emergency_story(8000, "כמה כסף צריך להיות בצד ליום לא צפוי?", "אם ההוצאות החודשיות שלך הן 8,000 שקלים.")),
    ("emergency_12000", lambda: emergency_story(12000, "קרן חירום: כמה זה באמת אצלך?", "אם ההוצאות החודשיות הן 12,000 שקלים.")),
    ("budget_8000", lambda: budget_story(8000, "כלל 50/30/20: לאן הולכת המשכורת?", "על משכורת נטו של 8,000 שקלים.")),
    ("budget_15000", lambda: budget_story(15000, "כלל 50/30/20 על משכורת של 15,000", "ככה זה נראה בשקלים.")),
    ("hourly_8000", lambda: hourly_story(8000, "כמה זמן צריך לעבוד בשביל קפה, משלוח ונעליים?", "משכורת נטו של 8,000 שקלים.")),
    ("hourly_12000", lambda: hourly_story(12000, "כמה דקות עבודה עולה הקפה שלך?", "משכורת נטו של 12,000 שקלים.")),
    ("hourly_20000", lambda: hourly_story(20000, "כמה שעות עבודה עולות הרגלים קטנים?", "משכורת נטו של 20,000 שקלים.")),
    ("rule72", rule72_story),
    ("simple_vs_compound", simple_story),
    ("child_savings", child_story),
    ("raise_vs_inflation", raise_story),
])

ORDER = ["story_compound", "story_coffee", "hourly_8000", "inflation_1000", "habit_delivery", "compound_300", "emergency_8000",
         "fees_100k", "habit_lunch", "early_500", "budget_8000", "rule72", "habit_streaming", "inflation_10000",
         "compound_1000", "simple_vs_compound", "hourly_12000", "habit_taxi", "raise_vs_inflation", "fees_50k",
         "habit_gym", "child_savings", "emergency_12000", "habit_apps", "compound_200", "inflation_5000",
         "budget_15000", "habit_friday", "early_300", "hourly_20000", "habit_water", "compound_800"]
assert set(ORDER) == set(REG), set(ORDER) ^ set(REG)
sc.STORIES = {k: REG[k] for k in ORDER}
