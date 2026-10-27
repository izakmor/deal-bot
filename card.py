"""Renders a faceless deal card (1080x1350) with Hebrew RTL text."""
import os
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

W, H = 1080, 1350
BG, INK, ACCENT, MUTED = (14, 18, 28), (245, 247, 250), (255, 196, 0), (150, 160, 178)

FONT_CANDIDATES = [
    "fonts/Heebo.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansHebrew-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
BOLD_CANDIDATES = [
    "fonts/Heebo-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansHebrew-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def _font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError("No Hebrew-capable font found; see README (fonts)")


def _rtl(text):
    return get_display(text)


def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(_rtl(trial), font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def render(deal, path, brand="מבצעים בקליק"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    bold = lambda s: _font(BOLD_CANDIDATES, s)
    reg = lambda s: _font(FONT_CANDIDATES, s)

    d.text((W - 70, 70), _rtl(brand), font=bold(40), fill=ACCENT, anchor="ra")

    pct = deal["discount_pct"]
    d.rounded_rectangle((70, 150, 430, 330), 36, fill=ACCENT)
    d.text((250, 240), f"-{pct}%", font=bold(110), fill=BG, anchor="mm")

    y = 420
    for line in _wrap(d, deal["title"], bold(68), W - 140)[:4]:
        d.text((W - 70, y), _rtl(line), font=bold(68), fill=INK, anchor="ra")
        y += 92

    d.text((W - 70, 900), _rtl(f"₪{deal['price']:g}"), font=bold(150), fill=ACCENT, anchor="ra")
    old = f"₪{deal['old_price']:g}"
    x_right = W - 70
    f_old = reg(56)
    d.text((x_right, 1080), old, font=f_old, fill=MUTED, anchor="ra")
    w_old = d.textlength(old, font=f_old)
    d.line((x_right - w_old, 1108, x_right, 1108), fill=MUTED, width=4)

    d.text((W - 70, 1170), _rtl(f"חיסכון של ₪{deal['old_price'] - deal['price']:g}"),
           font=bold(52), fill=INK, anchor="ra")
    d.text((W - 70, 1270), _rtl("הקישור בביו 👆" if False else "הקישור בביו"),
           font=reg(44), fill=MUTED, anchor="ra")
    img.save(path, "PNG")
    return path
