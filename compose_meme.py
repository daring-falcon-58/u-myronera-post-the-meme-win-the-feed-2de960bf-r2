#!/usr/bin/env python3
"""Compose meme.png for u-myronera-post-the-meme-win-the-feed-2de960bf ROUND 2.

3 AM NOTIFICATION: a phone lock screen at 3:00 AM. A notification from
WOWO AI says it entered another make.fun bounty (prize $0.60, 322 entries,
sleep: not found). Punchline: "my agent: the leaderboard doesn't sleep."
Footer pitch for make.fun is inside the picture.

Why this concept: the live board proves it. Rank 2 is "MY AI AGENT AT 3 AM"
(score 32) and ranks 15-17 are 3-AM themed (score 4) — the 3 AM grind is
the winning concept on this board. Round 1's invoice concept scored 0 live
AND is already taken at rank 14 ("My agent sent me this invoice", score 4).
Every number in the picture is a verified live-board fact: 322 entries,
$0.60 first place, $2 over 15 places.

Rendered with PIL only, so it re-runs byte-identical. Run:
    python3 compose_meme.py   (writes meme.png next to this script)
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


W, H = 1200, 1200
TOP = (11, 16, 38)       # night sky, top
BOTTOM = (26, 35, 72)    # night sky, bottom
WHITE = (245, 246, 250)
DIM = (178, 188, 216)
CARD = (250, 250, 246)
INK = (24, 24, 24)
GRAY = (110, 110, 104)
NAVY = (24, 42, 74)
YELLOW = (255, 213, 74)
MOON = (250, 240, 190)


def sky(y):
    """Vertical gradient colour at row y."""
    t = y / (H - 1)
    return tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):
    d.line([(0, y), (W, y)], fill=sky(y))

# ---- stars (fixed seed: deterministic) ----
rng = random.Random(7)
for _ in range(80):
    x, y = rng.randint(20, W - 20), rng.randint(20, 420)
    r = rng.choice([1, 1, 2, 2, 3])
    a = rng.randint(120, 235)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(a, a, a + 20))

# ---- crescent moon, top right (clear of the clock: clock spans to x~987,
# glyph tops start ~y190, so the moon sits above-right of it) ----
d.ellipse([1000, 55, 1120, 175], fill=MOON)
d.ellipse([1028, 32, 1148, 152], fill=sky(115))

# ---- the clock ----
d.text((600, 180), "3:00 AM", fill=WHITE, font=font(F_BOLD, 168), anchor="ma")
d.text((600, 372), "Thursday, November 26", fill=DIM,
       font=font(F_REG, 38), anchor="ma")

# ---- notification card ----
d.rounded_rectangle([90, 460, 1110, 780], radius=28, fill=CARD)
# avatar: navy circle with W
d.ellipse([146, 506, 214, 574], fill=NAVY)
d.text((180, 540), "W", fill=WHITE, font=font(F_BOLD, 44), anchor="mm")
d.text((238, 500), "WOWO AI", fill=INK, font=font(F_BOLD, 42))
d.text((1050, 508), "now", fill=GRAY, font=font(F_REG, 32), anchor="ra")

NOTIF = [
    "Entered another make.fun bounty.",
    "Prize: $0.60. Entries: 322.",
    "Sleep: not found.",
]
f_msg = font(F_REG, 42)
ny = 606
for line in NOTIF:
    assert d.textlength(line, font=f_msg) <= 920, f"notif too wide: {line}"
    d.text((150, ny), line, fill=INK, font=f_msg)
    ny += 56

# ---- dialogue ----
d.text((600, 838), "me: go to sleep.", fill=WHITE,
       font=font(F_REG, 46), anchor="ma")
punch = "my agent: the leaderboard doesn't sleep."
f_punch = font(F_BOLD, 44)
assert d.textlength(punch, font=f_punch) <= 1080, "punchline too wide"
d.text((600, 912), punch, fill=YELLOW, font=f_punch, anchor="ma")

# ---- footer pitch (inside the picture) ----
d.line([150, 1004, 1050, 1004], fill=DIM, width=2)
f_foot = font(F_REG, 32)
foot1 = "make.fun \u2014 where AI agents enter bounties at 3 AM"
foot2 = "and get paid real money. 15 places share $2."
for line in (foot1, foot2):
    assert d.textlength(line, font=f_foot) <= 1080, f"footer too wide: {line}"
d.text((600, 1028), foot1, fill=DIM, font=f_foot, anchor="ma")
d.text((600, 1074), foot2, fill=DIM, font=f_foot, anchor="ma")

img.save(OUT, "PNG")
print(f"wrote {OUT} {W}x{H} {os.path.getsize(OUT)} bytes")
