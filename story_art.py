"""Topic illustrations for the story carousels (flat vector, 1080x440 canvas, same palette).
Icons are drawn standing on y=0 and centred on x=0; scenes place them with cup_g-style transforms."""
import math

from story_cards import COIN, CORAL, GROUND, INK, LEAF, LEAF2, SUN, cup_g, svg440, tree

BROWN, SKY, PAPER = "#C98B4B", "#9FE3F5", "#FFFFFF"


def _g(cx, base, k, inner):
    return f'<g transform="translate({cx},{base}) scale({k})">{inner}</g>'


def _ground(rx=620, ry=90, cy=420):
    return f'<ellipse cx="540" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GROUND}"/>'


# ------------------------------------------------------------------ icons (cx, base, k)
def bag_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="160" ry="22" fill="{GROUND}"/>'
              f'<path d="M-50 -170 C-50 -240 50 -240 50 -170" stroke="#8A5A3B" stroke-width="12" fill="none" stroke-linecap="round"/>'
              f'<path d="M-125 0 L-105 -170 L105 -170 L125 0 Z" fill="{BROWN}"/>'
              f'<path d="M-105 -170 L105 -170 L100 -140 L-100 -140 Z" fill="#B27A3D"/>'
              f'<circle cx="0" cy="-70" r="34" fill="{CORAL}"/><circle cx="0" cy="-70" r="14" fill="{PAPER}"/>')


def lunch_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="170" ry="22" fill="{GROUND}"/>'
              f'<rect x="-135" y="-120" width="270" height="120" rx="22" fill="{CORAL}"/>'
              f'<rect x="-145" y="-160" width="290" height="46" rx="18" fill="#FF8F76"/>'
              f'<rect x="-22" y="-146" width="44" height="22" rx="8" fill="{PAPER}"/>'
              f'<circle cx="-70" cy="-60" r="14" fill="{PAPER}" opacity=".7"/><circle cx="70" cy="-60" r="14" fill="{PAPER}" opacity=".7"/>')


def tv_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="150" ry="18" fill="{GROUND}"/>'
              f'<rect x="-150" y="-190" width="300" height="170" rx="20" fill="{INK}"/>'
              f'<path d="M-32 -150 L-32 -60 L48 -105 Z" fill="{PAPER}"/>'
              f'<rect x="-30" y="-22" width="60" height="16" fill="{INK}"/><rect x="-80" y="-10" width="160" height="10" rx="5" fill="{INK}"/>')


def dumbbell_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="190" ry="20" fill="{GROUND}"/>'
              f'<rect x="-130" y="-92" width="260" height="16" rx="8" fill="{INK}"/>'
              f'<rect x="-175" y="-150" width="36" height="130" rx="10" fill="{INK}"/><rect x="-138" y="-130" width="26" height="90" rx="8" fill="#2C4468"/>'
              f'<rect x="139" y="-150" width="36" height="130" rx="10" fill="{INK}"/><rect x="112" y="-130" width="26" height="90" rx="8" fill="#2C4468"/>')


def taxi_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="200" ry="18" fill="{GROUND}"/>'
              f'<path d="M-95 -95 L-62 -158 L72 -158 L112 -95 Z" fill="{SUN}"/>'
              f'<rect x="-180" y="-100" width="360" height="72" rx="26" fill="{SUN}"/>'
              f'<path d="M-72 -100 L-50 -146 L-6 -146 L-6 -100 Z M6 -100 L6 -146 L58 -146 L88 -100 Z" fill="#DFF3FF"/>'
              f'<rect x="-30" y="-184" width="60" height="28" rx="8" fill="{CORAL}"/>'
              f'<circle cx="-105" cy="-28" r="34" fill="{INK}"/><circle cx="-105" cy="-28" r="13" fill="{PAPER}"/>'
              f'<circle cx="115" cy="-28" r="34" fill="{INK}"/><circle cx="115" cy="-28" r="13" fill="{PAPER}"/>')


def phone_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="130" ry="16" fill="{GROUND}"/>'
              f'<rect x="-85" y="-210" width="170" height="205" rx="30" fill="{INK}"/>'
              f'<rect x="-70" y="-192" width="140" height="165" rx="14" fill="{PAPER}"/>'
              f'<circle cx="0" cy="-120" r="34" fill="{CORAL}"/><rect x="-46" y="-70" width="92" height="14" rx="7" fill="{SUN}"/>'
              f'<rect x="-46" y="-48" width="60" height="10" rx="5" fill="#D3E2DB"/>')


def bottle_g(cx, base, k=1.0):
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="110" ry="16" fill="{GROUND}"/>'
              f'<rect x="-48" y="-190" width="96" height="190" rx="34" fill="{SKY}"/>'
              f'<rect x="-24" y="-218" width="48" height="32" rx="8" fill="{INK}"/>'
              f'<rect x="-48" y="-110" width="96" height="46" fill="{PAPER}" opacity=".75"/>'
              f'<path d="M-30 -160 C-30 -140 -30 -130 -26 -120" stroke="{PAPER}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".8"/>')


ICONS = {"bag": bag_g, "lunch": lunch_g, "tv": tv_g, "dumbbell": dumbbell_g, "taxi": taxi_g, "phone": phone_g,
         "bottle": bottle_g, "cup": cup_g}


# ------------------------------------------------------------------ generic habit scenes
def scene_hero(icon):
    return svg440(_ground() + ICONS[icon](430, 405, 1.0) + COIN(760, 372, 44) + COIN(760, 372, 24) + COIN(850, 392, 30))


def scene_single(icon):
    return svg440(_ground() + ICONS[icon](470, 405, 0.9) + COIN(720, 376, 42) + COIN(720, 376, 22))


def scene_grid(icon):
    cells = "".join(ICONS[icon](330 + (i % 7) * 70, 150 + (i // 7) * 62, 0.15) for i in range(28))
    return svg440(f'<rect x="250" y="20" width="580" height="400" rx="30" fill="{PAPER}"/>' + cells)


def scene_pyramid(icon):
    out = _ground(cy=425)
    for row, n in enumerate((3, 2, 1)):
        for j in range(n):
            out += ICONS[icon](540 + (j - (n - 1) / 2) * 170, 415 - row * 125, 0.4)
    return svg440(out)


def scene_mountain(icon):
    out = _ground(640, 80, 430)
    for row, n in enumerate(range(9, 0, -1)):
        for j in range(n):
            out += COIN(540 + (j - (n - 1) / 2) * 50, 408 - row * 34, 25)
    return svg440(out + ICONS[icon](540, 408 - 8 * 34 - 14, 0.3))


# ------------------------------------------------------------------ inflation / raise: shopping basket
def basket(n, cx=540, base=410, k=1.0):
    fruit = [(CORAL, -70, -150), (SUN, 0, -165), (LEAF2, 70, -150), (CORAL, -35, -195), (SUN, 35, -195), (LEAF, 0, -225)]
    items = "".join(f'<circle cx="{x}" cy="{y}" r="34" fill="{c}"/><circle cx="{x - 10}" cy="{y - 10}" r="9" fill="#fff" opacity=".45"/>'
                    for c, x, y in fruit[:max(0, n)])
    return _g(cx, base, k, f'<ellipse cx="0" cy="0" rx="200" ry="20" fill="{GROUND}"/>' + items +
              f'<path d="M-150 -140 L-120 -10 L120 -10 L150 -140 Z" fill="{BROWN}"/>'
              f'<path d="M-135 -105 L135 -105 M-128 -70 L128 -70 M-60 -140 L-52 -10 M0 -140 L0 -10 M60 -140 L52 -10" stroke="#8A5A3B" stroke-width="7"/>'
              f'<path d="M-160 -140 L160 -140" stroke="#8A5A3B" stroke-width="16" stroke-linecap="round"/>'
              f'<path d="M-110 -140 C-110 -270 110 -270 110 -140" stroke="#8A5A3B" stroke-width="12" fill="none" stroke-linecap="round"/>')


def scene_basket(ratio):
    return svg440(_ground() + basket(max(1, round(6 * ratio))))


def scene_basket_tag():
    tag = (f'<path d="M760 150 L860 150 L900 190 L860 230 L760 230 Z" fill="{CORAL}"/><circle cx="782" cy="190" r="9" fill="#fff"/>'
           f'<text x="838" y="205" font-family="Heebo" font-weight="800" font-size="40" text-anchor="middle" fill="#fff">+</text>')
    return svg440(_ground() + basket(6, 470, 410, 1.0) + tag)


def scene_raise(nominal_ratio, real_ratio):
    h = min(260, 150 * nominal_ratio)
    slip = (f'<rect x="250" y="{410 - h}" width="230" height="{h}" rx="16" fill="{PAPER}"/>'
            f'<rect x="274" y="{430 - h}" width="140" height="14" rx="7" fill="#D3E2DB"/><rect x="274" y="{458 - h}" width="100" height="14" rx="7" fill="#D3E2DB"/>'
            f'<text x="365" y="{400}" font-family="Heebo" font-weight="800" font-size="46" text-anchor="middle" fill="{INK}">₪</text>')
    return svg440(_ground() + slip + basket(max(1, round(6 * real_ratio)), 740, 410, 0.9))


# ------------------------------------------------------------------ fees: coin with a bite
def coin_bite():
    arrow = (f'<circle cx="700" cy="170" r="62" fill="{CORAL}"/>'
             f'<path d="M700 140 L700 196 M676 174 L700 200 L724 174" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg440(_ground() + COIN(540, 285, 150) + COIN(540, 285, 85) +
                  f'<text x="540" y="322" font-family="Heebo" font-weight="800" font-size="110" text-anchor="middle" fill="{INK}">%</text>' + arrow)


# ------------------------------------------------------------------ emergency: umbrella over coins
def umbrella(level):
    drops = "".join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="14" fill="{SKY}" opacity=".85"/>'
                    for x, y in [(210, 90), (300, 40), (380, 120), (700, 60), (790, 130), (880, 70), (180, 200), (900, 210)])
    canopy = (f'<path d="M340 170 C340 60 740 60 740 170 C710 150 690 150 660 170 C630 150 600 150 570 170 '
              f'C540 150 510 150 480 170 C450 150 430 150 400 170 C380 150 360 150 340 170 Z" fill="{CORAL}"/>'
              f'<path d="M540 78 L540 170 M450 96 L470 170 M630 96 L610 170" stroke="#E0472B" stroke-width="5"/>'
              f'<path d="M540 170 L540 250 C540 275 512 275 512 252" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    out = _ground(cy=425) + drops + canopy
    for x, h in [(420, 2), (480, 4), (540, 5), (600, 4), (660, 2)]:
        for k in range(max(1, round(h * level / 4))):
            out += COIN(x, 405 - k * 20, 26)
    return svg440(out)


# ------------------------------------------------------------------ budget: pie chart
def pie(highlight=None):
    cx, cy, r = 540, 215, 185
    parts = [(0.5, INK), (0.3, CORAL), (0.2, SUN)]
    out, a0 = "", -math.pi / 2
    for i, (share, col) in enumerate(parts):
        a1 = a0 + share * 2 * math.pi
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        op = 1 if highlight in (None, i) else 0.3
        pull = 14 if highlight == i else 0
        mid = (a0 + a1) / 2
        tx, ty = pull * math.cos(mid), pull * math.sin(mid)
        out += (f'<path transform="translate({tx:.1f},{ty:.1f})" d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if share > .5 else 0} 1 {x1:.1f} {y1:.1f} Z" '
                f'fill="{col}" opacity="{op}"/>')
        a0 = a1
    return svg440(out)


# ------------------------------------------------------------------ time: clock
def clock(hours_elapsed, coin=True):
    cx, cy, r = 470, 215, 175
    m_ang = math.radians((hours_elapsed * 60 % 60) * 6 - 90)
    h_ang = math.radians((hours_elapsed % 12) * 30 - 90)
    ticks = "".join(f'<line x1="{cx + 150 * math.cos(math.radians(i * 30))}" y1="{cy + 150 * math.sin(math.radians(i * 30))}" '
                    f'x2="{cx + 165 * math.cos(math.radians(i * 30))}" y2="{cy + 165 * math.sin(math.radians(i * 30))}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                    for i in range(12))
    hands = (f'<line x1="{cx}" y1="{cy}" x2="{cx + 105 * math.cos(h_ang):.1f}" y2="{cy + 105 * math.sin(h_ang):.1f}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx + 145 * math.cos(m_ang):.1f}" y2="{cy + 145 * math.sin(m_ang):.1f}" stroke="{CORAL}" stroke-width="9" stroke-linecap="round"/>'
             f'<circle cx="{cx}" cy="{cy}" r="14" fill="{INK}"/>')
    face = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="12"/>'
    extra = COIN(790, 330, 50) + COIN(790, 330, 28) + COIN(860, 372, 34) if coin else ""
    return svg440(face + ticks + hands + extra)


# ------------------------------------------------------------------ simple vs compound: stairs
def stairs(kind):
    out = f'<rect x="120" y="408" width="840" height="12" rx="6" fill="{GROUND}"/>'
    n, x = 7, 150
    h = 0
    for i in range(n):
        step = 36 if kind == "simple" else 18 + i * 12
        h += step
        col = INK if kind == "simple" else LEAF
        out += f'<rect x="{x + i * 110}" y="{408 - h}" width="92" height="{h}" rx="8" fill="{col}"/>'
    return svg440(out)


# ------------------------------------------------------------------ doubling and piggy bank
def coin_pair():
    return svg440(_ground() + COIN(380, 300, 100) + COIN(380, 300, 56) + COIN(700, 300, 100) + COIN(700, 300, 56) +
                  f'<text x="540" y="320" font-family="Heebo" font-weight="800" font-size="90" text-anchor="middle" fill="{INK}">×2</text>')


def piggy():
    body = (f'<ellipse cx="540" cy="285" rx="190" ry="130" fill="#FF8F76"/>'
            f'<path d="M430 170 L455 105 L505 160 Z" fill="#FF7A5C"/>'
            f'<ellipse cx="716" cy="300" rx="52" ry="42" fill="#FF7A5C"/><circle cx="702" cy="298" r="8" fill="{INK}"/><circle cx="730" cy="298" r="8" fill="{INK}"/>'
            f'<circle cx="650" cy="238" r="12" fill="{INK}"/>'
            f'<rect x="440" y="396" width="52" height="40" rx="14" fill="#FF7A5C"/><rect x="590" y="396" width="52" height="40" rx="14" fill="#FF7A5C"/>'
            f'<rect x="500" y="168" width="90" height="14" rx="7" fill="{INK}"/>')
    return svg440(_ground() + body + COIN(545, 112, 34))


def sprout_pig_scene():
    return piggy()
