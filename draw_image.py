#!/usr/bin/env python3
"""Render the 18 November 2026 world-news poster (1024x1024 PNG).

Pure Pillow drawing: every word is typeset by the script, so no text can come
out garbled. Layout is a newspaper front page: masthead, one lead story with a
drawn globe and three flag chips, five story cards, and an "also today" strip.
Run: python3 draw_image.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (14, 30, 51)
INK = (24, 24, 24)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
CARD_LINE = (205, 198, 182)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_flag(draw, x, y, w, h, kind):
    """Tiny stylised flag chips (no faces, no photos)."""
    if kind == "usa":
        for i in range(7):
            draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                           fill=RED if i % 2 == 0 else WHITE)
        draw.rectangle([x, y, x + int(w * 0.42), y + h // 2], fill=NAVY)
    elif kind == "china":
        draw.rectangle([x, y, x + w, y + h], fill=RED)
        draw.ellipse([x + 6, y + 5, x + 16, y + 15], fill=GOLD)
        for dx, dy in ((24, 6), (30, 12), (30, 20), (24, 24)):
            draw.ellipse([x + dx, y + dy, x + dx + 5, y + dy + 5], fill=GOLD)
    elif kind == "russia":
        draw.rectangle([x, y, x + w, y + h // 3], fill=WHITE)
        draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_globe(draw, cx, cy, r):
    """Stylised wireframe globe: circle, meridians, parallels, three pins."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    for k in (0.45, 0.8):
        draw.ellipse([cx - r * k, cy - r, cx + r * k, cy + r], outline=NAVY, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=NAVY, width=2)
    for dy in (-r // 2, 0, r // 2):
        wdt = int((r * r - dy * dy) ** 0.5)
        draw.line([cx - wdt, cy + dy, cx + wdt, cy + dy], fill=NAVY, width=2)
    # three pins: Shenzhen, Manila, Kyiv (schematic positions on the globe)
    for px, py, col in ((cx + 52, cy - 18, RED), (cx + 62, cy + 12, RED),
                        (cx - 38, cy - 42, RED)):
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col, outline=WHITE, width=2)


def story_card(draw, x, y, w, h, tag, tag_color, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=CARD_LINE, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=tag_color)
    f_tag = font(SANS_B, 18)
    f_head = font(SANS_B, 26)
    f_body = font(SANS, 19)
    draw.text((x + 16, y + 12), tag, font=f_tag, fill=tag_color)
    hl = wrap(draw, headline, f_head, w - 32)
    ty = y + 38
    for line in hl[:1]:
        draw.text((x + 16, ty), line, font=f_head, fill=INK)
        ty += 31
    bl = wrap(draw, body, f_body, w - 32)
    by = ty + 6
    for line in bl[:2]:
        draw.text((x + 16, by), line, font=f_body, fill=(60, 60, 60))
        by += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_title = font(SERIF_B, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 27)
    date = "WEDNESDAY  18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 78), date, font=f_date, fill=GOLD)
    d.rectangle([0, 118, W, 126], fill=RED)

    # ---- Lead story -----------------------------------------------------
    lx, ly, lw, lh = 28, 138, 968, 272
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=WHITE, outline=CARD_LINE, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    draw_globe(d, lx + 118, ly + 138, 86)
    tx = lx + 240
    f_tag = font(SANS_B, 20)
    d.text((tx, ly + 16), "DIPLOMACY  -  SHENZHEN, CHINA", font=f_tag, fill=RED)
    f_head = font(SANS_B, 45)
    for i, line in enumerate(("THREE NUCLEAR POWERS,", "ONE TABLE")):
        d.text((tx, ly + 48 + i * 52), line, font=f_head, fill=INK)
    f_body = font(SANS, 20)
    lead = ("Xi Jinping hosts Donald Trump and Vladimir Putin on 19 November "
            "for the first trilateral summit of the three leaders, on the "
            "sidelines of APEC. Nuclear arms, Iran and AI are on the agenda.")
    by = ly + 158
    for line in wrap(d, lead, f_body, lw - 268)[:3]:
        d.text((tx, by), line, font=f_body, fill=(60, 60, 60))
        by += 25
    # flag chips row
    fy = ly + lh - 34
    fx = tx
    f_lab = font(SANS_B, 16)
    for kind, label in (("usa", "USA"), ("china", "CHINA"), ("russia", "RUSSIA")):
        draw_flag(d, fx, fy, 46, 28, kind)
        d.text((fx + 54, fy + 5), label, font=f_lab, fill=INK)
        fx += 140

    # ---- Story cards ----------------------------------------------------
    cw, ch, gap = 474, 144, 20
    cy0 = 422
    cards = [
        ("WAR  -  UKRAINE", RED,
         "Ukraine wrecks Crimea bridge",
         "Kyiv destroyed the road span of Putin's $3.6bn bridge; Russia "
         "hit two Kyiv bridges in reply."),
        ("HEALTH  -  USA", (11, 110, 79),
         "US loses measles-free status",
         "PAHO ends 26 years of elimination after 5,400 cases in 2026, "
         "the worst since 1991."),
        ("MIDDLE EAST  -  BAHRAIN", (138, 90, 0),
         "Iran hits US radar in Bahrain",
         "Third attack on US targets in the kingdom in days; the Fifth "
         "Fleet is based there."),
        ("POLITICS  -  ISRAEL", (29, 78, 137),
         "Eisenkot tapped to lead Israel",
         "Parliament elects his ally Matan Kahana speaker 66-52; Netanyahu "
         "stays caretaker premier."),
    ]
    for i, (tag, col, head, body) in enumerate(cards):
        x = 28 + (i % 2) * (cw + gap)
        y = cy0 + (i // 2) * (ch + 12)
        story_card(d, x, y, cw, ch, tag, col, head, body)

    # full-width tech card
    ty = cy0 + 2 * (ch + 12)
    story_card(d, 28, ty, 968, ch, "TECH  -  AI", (91, 45, 142),
               "Nvidia booms as US tightens AI chip curbs",
               "Nvidia doubled quarterly revenue and its board refused to reinstate "
               "ousted chief Jensen Huang; Washington closed a chip-export loophole.")

    # ---- Also today strip ----------------------------------------------
    fy = ty + ch + 12
    d.rectangle([28, fy, 996, fy + 82], fill=NAVY)
    f_lab = font(SANS_B, 20)
    d.text((44, fy + 8), "ALSO TODAY", font=f_lab, fill=GOLD)
    f_small = font(SANS, 19)
    also = ("Cyclone Akvan bears down on India's Andhra coast  -  MS Dhoni "
            "retires from the IPL  -  Mongolia's president resigns amid "
            "graft charges")
    ay = fy + 36
    for line in wrap(d, also, f_small, 936)[:2]:
        d.text((44, ay), line, font=f_small, fill=WHITE)
        ay += 24

    # ---- Source line -----------------------------------------------------
    f_src = font(SANS, 15)
    src = ("All events reported on Wednesday 18 November 2026.  "
           "Sources: Reuters, AFP, AP, The Hindu, CNA.")
    sw = d.textlength(src, font=f_src)
    d.text(((W - sw) / 2, fy + 94), src, font=f_src, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
