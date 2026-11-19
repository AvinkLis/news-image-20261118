#!/usr/bin/env python3
"""Draw the entry image for make.fun bounty news-image-20261118.

"The Daily Picture" — a newspaper front page that sums up the world news
of Wednesday 18 November 2026 in one 1024x1024 frame, drawn entirely with
Pillow (no photographs), so a judge with no news feed can read the whole
day from the picture alone.

Stories cross-checked 19 Nov 2026 against several independent briefings of
18 Nov 2026 (Just Security Early Edition, Level Headlines, Zark News and
Open Chronicle): Xi and Putin meet at APEC in Shenzhen ahead of a first
trilateral summit with Trump; Iran strikes Kuwait and Bahrain after the
U.S. strike on Qeshm Island; the Kerch Bridge is hit for a second day;
Peltola wins Alaska and the Senate goes 56-44; Nvidia posts a record
$115.8B quarter; the U.S. loses measles-elimination status; Congo's Ebola
outbreak passes 11,000 cases; Voyager 1 reaches one light-day from Earth.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAPER = (246, 239, 224)
INK = (26, 34, 44)
RED = (176, 48, 38)
NAVY = (30, 70, 110)
GREY = (96, 92, 84)
WHITE = (252, 252, 250)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap measured in pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, font, fill=INK):
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)
M = 38
RIGHT = W - M

# ---------------------------------------------------------------- masthead
d.rectangle([M, 20, RIGHT, 25], fill=RED)
d.line([M, 33, RIGHT, 33], fill=INK, width=2)
centered(d, 46, "THE DAILY PICTURE", f(SERIF_B, 74))
centered(
    d,
    132,
    "Wednesday 18 November 2026  ·  The whole world's news, in one image",
    f(SANS_B, 24),
    fill=NAVY,
)
d.line([M, 168, RIGHT, 168], fill=INK, width=3)
d.line([M, 173, RIGHT, 173], fill=INK, width=1)

# ---------------------------------------------------------------- lead story
d.text((M, 188), "LEAD STORY — APEC SUMMIT · SHENZHEN, CHINA", font=f(SANS_B, 23), fill=RED)
d.text((M, 222), "XI & PUTIN MEET IN SHENZHEN", font=f(SERIF_B, 47), fill=INK)
d.text((M, 282), "TRUMP JOINS THEM THURSDAY", font=f(SERIF_B, 47), fill=INK)
STAND = (
    "China's Xi pledges to resist protectionism, Russia's Putin attacks "
    "sanctions as APEC opens — and a first three-way summit with Trump "
    "follows Thursday."
)
sy = 348
for line in wrap(d, STAND, f(SANS, 22), RIGHT - M):
    d.text((M, sy), line, font=f(SANS, 22), fill=INK)
    sy += 29

# ------------------------------------------------------- lead illustration
# Three national flags on poles above one long summit table.
def flag_china(x, y):
    d.rectangle([x, y, x + 118, y + 72], fill=(222, 41, 16))
    star(d, x + 30, y + 24, 15, (255, 222, 0))
    for dx, dy in [(52, 10), (58, 26), (58, 42), (50, 54)]:
        star(d, x + dx, y + dy, 5, (255, 222, 0))


def flag_russia(x, y):
    d.rectangle([x, y, x + 118, y + 24], fill=WHITE)
    d.rectangle([x, y + 24, x + 118, y + 48], fill=(0, 57, 166))
    d.rectangle([x, y + 48, x + 118, y + 72], fill=(213, 43, 30))


def flag_usa(x, y):
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * 10, x + 118, y + i * 10 + 10], fill=col)
    d.rectangle([x, y + 70, x + 118, y + 72], fill=WHITE)
    d.rectangle([x, y, x + 52, y + 40], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 5 + c * 10, y + 4 + r * 9, x + 9 + c * 10, y + 8 + r * 9], fill=WHITE)


BAND_Y = 412
for fx, draw_flag in [(168, flag_china), (453, flag_russia), (738, flag_usa)]:
    d.rectangle([fx + 55, BAND_Y, fx + 60, BAND_Y + 84], fill=INK)  # pole
    draw_flag(fx, BAND_Y)
d.rectangle([128, BAND_Y + 84, 896, BAND_Y + 98], fill=NAVY)  # table slab
for cx in (256, 512, 768):  # microphones and place cards on the table
    d.line([cx, BAND_Y + 84, cx - 14, BAND_Y + 62], fill=INK, width=4)
    d.ellipse([cx - 22, BAND_Y + 54, cx - 6, BAND_Y + 66], fill=INK)
    d.rectangle([cx - 34, BAND_Y + 66, cx + 34, BAND_Y + 82], fill=WHITE, outline=INK, width=2)
centered(
    d,
    BAND_Y + 108,
    "Three flags, one table — APEC opens in Shenzhen as a rare trilateral nears.",
    f(SANS, 19),
    fill=GREY,
)
d.line([M, 552, RIGHT, 552], fill=INK, width=2)

# ------------------------------------------------------------------- icons
def icon_drone(x, y):
    d.rectangle([x + 26, y + 26, x + 62, y + 46], fill=INK)
    for ax, ay in [(6, 6), (66, 6), (6, 52), (66, 52)]:
        d.line([x + 44, y + 36, x + ax + 8, y + ay + 5], fill=INK, width=4)
        d.ellipse([x + ax, y + ay, x + ax + 16, y + ay + 10], outline=INK, width=3)
    star(d, x + 100, y + 62, 13, RED)


def icon_bridge(x, y):
    d.rectangle([x + 8, y + 8, x + 18, y + 62], fill=NAVY)
    d.rectangle([x + 92, y + 8, x + 102, y + 62], fill=NAVY)
    d.rectangle([x, y + 34, x + 44, y + 42], fill=NAVY)
    d.rectangle([x + 66, y + 34, x + 110, y + 42], fill=NAVY)
    d.polygon([(x + 46, y + 40), (x + 66, y + 40), (x + 60, y + 56), (x + 48, y + 52)], fill=RED)
    d.line([x, y + 68, x + 110, y + 68], fill=NAVY, width=3)


def icon_ballot(x, y):
    d.rectangle([x + 28, y, x + 62, y + 34], fill=WHITE, outline=INK, width=3)
    star(d, x + 45, y + 17, 10, RED)
    d.rectangle([x + 8, y + 40, x + 82, y + 74], fill=NAVY)
    d.rectangle([x + 22, y + 48, x + 68, y + 54], fill=WHITE)


def icon_chip(x, y):
    for i in range(4):
        px = x + 18 + i * 18
        d.line([px, y, px, y + 14], fill=INK, width=4)
        d.line([px, y + 60, px, y + 74], fill=INK, width=4)
        py = y + 18 + i * 18
        d.line([x, py, x + 14, py], fill=INK, width=4)
        d.line([x + 60, py, x + 74, py], fill=INK, width=4)
    d.rectangle([x + 14, y + 14, x + 74, y + 60], fill=(16, 122, 87))
    d.rectangle([x + 30, y + 28, x + 58, y + 46], outline=WHITE, width=3)


def story(x, y, w, icon, headline, body):
    icon(x, y + 2)
    tx = x + 124
    hy = y
    for line in wrap(d, headline, f(SANS_B, 23), w - 124):
        d.text((tx, hy), line, font=f(SANS_B, 23), fill=INK)
        hy += 29
    by = hy + 3
    for line in wrap(d, body, f(SANS, 19), w - 124):
        d.text((tx, by), line, font=f(SANS, 19), fill=INK)
        by += 25


COL_W = 452
story(
    M, 570, COL_W, icon_drone,
    "IRAN STRIKES KUWAIT & BAHRAIN BASES",
    "Tehran's drones target U.S. bases after U.S. jets hit a missile "
    "site on Qeshm Island.",
)
story(
    M + COL_W + 44, 570, COL_W, icon_bridge,
    "KERCH BRIDGE HIT AGAIN",
    "Ukraine hits the Crimea bridge again; a road span falls. "
    "126 of 141 drones are downed.",
)
story(
    M, 722, COL_W, icon_ballot,
    "PELTOLA WINS ALASKA — SENATE 56-44",
    "Democrat Mary Peltola beats Sen. Dan Sullivan in the last "
    "midterm race to be called.",
)
story(
    M + COL_W + 44, 722, COL_W, icon_chip,
    "NVIDIA POSTS A RECORD $115.8B QUARTER",
    "First earnings since Jensen Huang's exit beat forecasts; "
    "the board bars his return.",
)
d.line([M, 862, RIGHT, 862], fill=INK, width=2)

# ------------------------------------------------------------- dateline minis
def mini(x, w, place, body):
    d.text((x, 876), place, font=f(SANS_B, 20), fill=RED)
    by = 904
    for line in wrap(d, body, f(SANS, 18), w):
        d.text((x, by), line, font=f(SANS, 18), fill=INK)
        by += 23


mini(M, 292, "WASHINGTON", "U.S. loses measles-free status held since 2000: 5,412 cases this year.")
mini(M + 330, 292, "KINSHASA", "Congo's Ebola outbreak passes 11,000 cases, doubling in three months.")
mini(M + 660, 288, "DEEP SPACE", "Voyager 1 reaches one light-day from Earth — 16 billion miles, a first.")

# ------------------------------------------------------------------- footer
d.line([M, 972, RIGHT, 972], fill=INK, width=3)
centered(
    d,
    982,
    "ALSO TODAY — Manila trade deal · Gaza board faults both sides · Japan jets scramble",
    f(SANS_B, 17),
    fill=NAVY,
)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
