#!/usr/bin/env python3
"""Render 'The World in One Day' — one 1024x1024 newspaper page summing up
the world's news of Monday, 23 November 2026.

Local-only drawing program (Pillow). It is NOT the graded entrypoint; the
entrypoint is main.ts, which copies the rendered entry.png to the output dir.
All facts come from the verified research notes for 23 November 2026.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (176, 42, 32)
MUTED = (85, 85, 85)
PANEL = (255, 255, 255)
RULE = (34, 34, 34)
GREEN = (28, 110, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MAST = load("DejaVuSans-Bold.ttf", 50)
F_DATE = load("DejaVuSans-Bold.ttf", 20)
F_KICK = load("DejaVuSans-Bold.ttf", 13)
F_HERO = load("DejaVuSans-Bold.ttf", 58)
F_SUB = load("DejaVuSans.ttf", 19)
F_STAND = load("DejaVuSans.ttf", 14)
F_SEC = load("DejaVuSans-Bold.ttf", 17)
F_NUM_BIG = load("DejaVuSans-Bold.ttf", 25)
F_NUM_LBL = load("DejaVuSans-Bold.ttf", 10)
F_T = load("DejaVuSans-Bold.ttf", 14)
F_F = load("DejaVuSans.ttf", 12)
F_A = load("DejaVuSans.ttf", 11)
F_FOOT = load("DejaVuSans.ttf", 9)
F_CHART_T = load("DejaVuSans-Bold.ttf", 11)
F_CHART_L = load("DejaVuSans.ttf", 10)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, font, fill, cx=512):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


TOP = [
    ("NVIDIA REINSTATES HUANG",
     "Board brings back Jensen Huang as CEO; shares soar +31%, a record +$952bn day."),
    ("UKRAINE SINKS WARSHIP",
     "Seven sea drones sink Russian corvette Merkury off Libya; Ka-27 helicopter destroyed."),
    ("COP31 ENDS WITH NO DEAL",
     "UN climate summit in Antalya collapses \u2014 first failure since 2009; EU rejects fossil-fuel silence."),
    ("IRAN'S HEAVIEST MISSILE WEEK",
     "Trump: heaviest Iranian missile and drone week in a year, all shot down; new US sanctions."),
    ("KYIV REGION STRIKES KILL \u226515",
     "Russian attacks kill at least 15 in Kyiv region, including a 7-year-old in Kryvyi Rih."),
    ("INDONESIA FACTORY FIRE: 24 DEAD",
     "Factory fire kills 24; dozens still missing as rescuers search the site."),
    ("INDIA GIVES NEPAL $1.62BN",
     "India pledges 240bn rupees for flood-hit Nepal; direct rail service launches."),
    ("BITCOIN FALLS TO $55,100",
     "Bitcoin drops to lowest since Sep 2024, then recovers to ~$61,000; S&P 500 in correction."),
    ("GAZA TRUCK STRIKE KILLS 3",
     "Israeli strike kills 3 in Gaza; witnesses say the truck carried food and WCK papers."),
    ("DEMOCRATS WIN 258 SEATS",
     "Democrats reach 258 House seats \u2014 their largest majority since 1992."),
    ("NATO MEETS OVER POLAND",
     "Emergency NATO meeting after three Russian objects fell in Poland last week."),
    ("BELGIUM STRIKE GROUNDS FLIGHTS",
     "National strike against austerity cancels nearly all flights at Brussels and Charleroi."),
    ("EU: NEW RUSSIA SANCTIONS",
     "60 banks, crypto platforms and 70 shadow-fleet ships targeted in new proposal."),
    ("S. KOREA MINISTER RESIGNS",
     "Education minister quits over exam-cheating chaos."),
    ("COLOMBIA DRONE HITS POLICE HQ",
     "Explosive drone strikes police HQ in C\u00facuta, damaging 60 homes."),
]

ALSO = [
    "Mexico: drug lord Chapo Isidro arrested after raid and cartel violence.",
    "Iran: singer Parastoo Ahmadi and 4 crew flogged in Qom.",
    "Finland summons Russian envoy over airspace violation.",
    "US: Amtrak train derails after hitting a trailer truck in Louisiana.",
    "Thailand: appeals court halves jailed MP's term in royal-insult case.",
    "Indonesia: president to nominate a vice-presidential candidate.",
    "West Bank: Eisenkot condemns arson attacks by Jewish settlers.",
    "UN: war threatens food aid for 7.3 million more people.",
    "EU: firms warn Brussels over competitiveness budget cuts.",
    "COP31: Saudi influence looms over the failed climate deal.",
    "Greece: Acropolis Museum reopens; Parthenon Marbles claim renewed.",
    "England: Co-op Live Manchester evacuated over unknown substance.",
    "Football: England confirmed as Women's World Cup 2035 host.",
    "Health: EDITH trial invites ~700,000 women for AI breast screening.",
    "AI: OpenAI proposes shared safety limits across labs.",
    "Space: China names Pakistani astronaut Muhammad Zeeshan Ali, 40, for Shenzhou-24.",
    "Nepal: quake shakes Koshi Province, felt in northern India.",
    "Oil: prices fall near three-month lows.",
    "Asia: China, South Korea and Taiwan step in to prop up stocks.",
    "Russia: soldier deaths in Ukraine estimated at 490,000\u2013700,000+.",
    "Summit: Trump\u2013Putin\u2013Xi meeting in Shenzhen yields signals, not substance.",
    "US: Army delays toxic-explosives detonation at Iowa plant to Wednesday.",
]

NUMBERS = [
    ("+31%", "NVIDIA SHARE JUMP"),
    ("$952bn", "ONE-DAY MARKET GAIN"),
    ("258", "DEMOCRAT HOUSE SEATS"),
    ("24", "KILLED IN FACTORY FIRE"),
    ("7", "DRONES SANK MERKURY"),
    ("$1.62bn", "INDIA AID TO NEPAL"),
]


def draw_chart(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=RULE, width=2)
    draw.text((x0 + 12, y0 + 8), "NVIDIA SHARE PRICE, $", font=F_CHART_T, fill=INK)
    draw.text((x0 + 12, y0 + 26), "+31.5% in one day \u2014 best since 2008",
              font=F_CHART_L, fill=GREEN)
    px0, py0, px1, py1 = x0 + 34, y0 + 48, x1 - 14, y1 - 30
    for gv, lab in [(120, "$120"), (140, "$140"), (160, "$160")]:
        gy = py1 - (gv - 120) / 50 * (py1 - py0)
        draw.line([(px0, gy), (px1, gy)], fill=(220, 220, 220), width=1)
        draw.text((x0 + 6, gy - 6), lab, font=F_CHART_L, fill=MUTED)
    vals = [126, 128, 124, 138, 152, 165]
    pts = []
    for i, v in enumerate(vals):
        px = px0 + i * (px1 - px0) / (len(vals) - 1)
        py = py1 - (v - 120) / 50 * (py1 - py0)
        pts.append((px, py))
    draw.line(pts, fill=GREEN, width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)
    draw.text((px0, py1 + 8), "Fri $126", font=F_CHART_L, fill=MUTED)
    draw.text((px1 - 52, py1 + 8), "Mon $165", font=F_CHART_L, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=2)

    # Masthead
    center(d, 26, "THE WORLD IN ONE DAY", F_MAST, INK)
    d.line([(30, 92), (994, 92)], fill=RULE, width=2)
    center(d, 100, "MONDAY, 23 NOVEMBER 2026", F_DATE, RED)
    d.line([(30, 130), (994, 130)], fill=RULE, width=1)

    # Hero: left text, right chart
    d.text((30, 146), "TOP STORY \u2014 MARKETS", font=F_KICK, fill=RED)
    d.text((30, 168), "HUANG IS BACK", font=F_HERO, fill=INK)
    for i, line in enumerate(wrap(d, "Nvidia soars 31% as board reinstates its CEO",
                                  F_SUB, 590)):
        d.text((30, 240 + i * 24), line, font=F_SUB, fill=INK)
    stand = ("Shares jump a record $952bn in a day; Nasdaq +6.5%, S&P +4.7%. "
             "Trump says he persuaded the board.")
    for i, line in enumerate(wrap(d, stand, F_STAND, 590)):
        d.text((30, 292 + i * 18), line, font=F_STAND, fill=MUTED)
    draw_chart(d, 640, 142, 994, 330)

    # The day in numbers
    d.text((30, 344), "THE DAY IN NUMBERS", font=F_SEC, fill=INK)
    d.line([(30, 366), (994, 366)], fill=RULE, width=1)
    bw = 152
    for i, (num, lbl) in enumerate(NUMBERS):
        x = 30 + i * (bw + 8)
        d.rectangle([x, 376, x + bw, 424], fill=PANEL, outline=RULE, width=1)
        center(d, 382, num, F_NUM_BIG, RED, cx=x + bw // 2)
        center(d, 408, lbl, F_NUM_LBL, INK, cx=x + bw // 2)

    # Top stories: 3 columns x 5 rows
    d.text((30, 438), "TOP STORIES", font=F_SEC, fill=INK)
    d.line([(30, 460), (994, 460)], fill=RULE, width=1)
    col_x = [30, 356, 682]
    for idx, (title, fact) in enumerate(TOP):
        col, row = idx % 3, idx // 3
        x = col_x[col]
        y = 470 + row * 50
        d.text((x, y), f"{idx + 1}.", font=F_T, fill=RED)
        d.text((x + 26, y), title, font=F_T, fill=INK)
        for j, line in enumerate(wrap(d, fact, F_F, 286)[:2]):
            d.text((x + 26, y + 18 + j * 14), line, font=F_F, fill=MUTED)

    # Also today: 3 columns
    d.text((30, 724), "ALSO TODAY", font=F_SEC, fill=INK)
    d.line([(30, 746), (994, 746)], fill=RULE, width=1)
    for idx, item in enumerate(ALSO):
        col, row = idx % 3, idx // 3
        x = col_x[col]
        y = 756 + row * 31
        d.text((x, y), f"{idx + 16}.", font=F_A, fill=RED)
        for j, line in enumerate(wrap(d, item, F_A, 284)[:2]):
            d.text((x + 26, y + j * 13), line, font=F_A, fill=INK)

    # Footer
    d.line([(30, 1000), (994, 1000)], fill=RULE, width=1)
    center(d, 1003, "Sources: BusinessWorld \u00b7 CNN \u00b7 Reuters \u00b7 WSJ \u00b7 Le Monde \u00b7 Daily Summary of World \u00b7 Broadcast Prism \u00b7 Smithsonian \u00b7 Atlantic Council",
           F_FOOT, MUTED)
    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
