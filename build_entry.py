"""news-image-20261122: draw one 1024x1024 PNG summing up world news of
Sunday 22 November 2026, to /output/entry.png.

Deterministic: no network, no randomness, no clock, no environment input.
The stories are embedded below as constants; the program only draws.
Run: python3 build_entry.py  (writes /output/entry.png, creating /output
if needed). Python 3.13 compatible; needs Pillow and DejaVu fonts
(system fonts). Build script only: the submitted entrypoint main.py is
stdlib-only and copies the entry.png this script produces, because the
server runs the entrypoint with no third-party packages installed.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 42, 68)
NAVY_LIGHT = (27, 68, 102)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (20, 28, 36)
MUTED = (90, 100, 112)
RULE = (196, 52, 40)
GOLD = (212, 160, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FALLBACK_DIR = "/usr/share/fonts"


def font(name, size):
    for base in (FONT_DIR, FALLBACK_DIR):
        path = os.path.join(base, name) if base == FONT_DIR else name
        if base == FONT_DIR:
            path = os.path.join(FONT_DIR, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        else:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                pass
    return ImageFont.load_default(size=size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

STORIES = [
    ("JUSTICE", "Mexico captures 'El Chapo Isidro'",
     "Special forces seize the FBI most-wanted cartel boss in Sinaloa; "
     "11 killed in the firefight that followed."),
    ("CLIMATE", "COP31 talks enter Sunday overtime",
     "Talks in Antalya run into a second day past deadline over fossil "
     "fuels; a new draft lands Sunday as states press for a transition "
     "pledge."),
    ("MIDDLE EAST", "Saudi stops missile; Bahrain blames Iran",
     "Saudi-led coalition says it intercepted a Houthi missile headed "
     "for western Saudi Arabia; Bahrain says an Iranian attack hit a "
     "civilian industrial facility."),
    ("EUROPE", "France protests continue",
     "Largely peaceful marches over living costs and student rights "
     "draw smaller crowds than last week, in a sixth weekend of "
     "rallies."),
    ("MARKETS", "Nvidia faces US accounting probe",
     "The chip giant faces a US accounting probe amid deepening turmoil, "
     "media report; Bitcoin falls to a two-year low."),
    ("DISASTER", "6.7 quake hits Peru; Brazil clears rubble",
     "A 6.7-magnitude quake strikes Peru with no deaths reported, as a "
     "Brazilian town clears rubble after a deadly storm."),
]

ALSO = [
    "Rohingyas hail ICJ Myanmar verdict",
    "Bayer's $7.25bn deal wins US approval",
    "India's NSE top five by market value",
]


def wrap(draw, text, fnt, width):
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_card(draw, x, y, w, h, tag, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=(214, 206, 188), width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=RULE)
    tag_f = SANS_B(17)
    draw.text((x + 18, y + 18), tag, font=tag_f, fill=RULE)
    head_f = SANS_B(29)
    lines = wrap(draw, headline, head_f, w - 36)
    ty = y + 48
    for line in lines[:2]:
        draw.text((x + 18, ty), line, font=head_f, fill=INK)
        ty += 34
    body_f = SANS(20)
    blines = wrap(draw, body, body_f, w - 36)
    by = ty + 8
    for line in blines[:4]:
        draw.text((x + 18, by), line, font=body_f, fill=(52, 62, 74))
        by += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 172], fill=NAVY)
    d.rectangle([0, 172, W, 178], fill=GOLD)
    d.text((36, 22), "THE WORLD IN ONE IMAGE", font=SANS_B(20), fill=GOLD)
    d.text((36, 48), "WORLD NEWS", font=SERIF_B(84), fill=(255, 255, 255))
    d.text((36, 138), "SUNDAY 22 NOVEMBER 2026  •  6 STORIES  •  ONE DAY",
           font=SANS_B(22), fill=(196, 214, 232))

    # Story grid: 2 columns x 3 rows
    gx, gy = 24, 198
    cw, ch, gap = 476, 232, 24
    for i, (tag, head, body) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + 14)
        draw_card(d, cx, cy, cw, ch, tag, head, body)

    # Footer (ALSO kept to one short line, never clipped)
    fy = 198 + 3 * 232 + 2 * 14 + 8  # 930
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((36, fy + 8), "ALSO TODAY", font=SANS_B(18), fill=GOLD)
    also_f = SANS(16)
    also_lines = wrap(d, "  •  ".join(ALSO), also_f, W - 72)
    assert len(also_lines) == 1, also_lines
    d.text((36, fy + 34), also_lines[0], font=also_f, fill=(255, 255, 255))
    d.text((36, fy + 64), "Sources: AFP, AP, Reuters, Business Standard, Xinhua  •  22 November 2026",
           font=SANS(15), fill=(150, 170, 190))

    out = "/output/entry.png"
    os.makedirs("/output", exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print("wrote " + out)


if __name__ == "__main__":
    main()
