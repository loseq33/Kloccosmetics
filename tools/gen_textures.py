"""Generuje tekstury moda kloccosmetics (peleryny + skrzydla).
Uruchom:  python tools/gen_textures.py   (wymaga Pillow)
"""
from PIL import Image, ImageDraw
import random, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources",
                    "assets", "kloccosmetics", "textures")
S = 8  # skala tekstury peleryny (64x32 -> 512x256)

# ---------- prosty czcionka 5x7 w stylu Minecrafta ----------
G = {
 'S': [".###.", "#...#", "#....", ".###.", "....#", "#...#", ".###."],
 'B': ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
 'O': [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 'u': [".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"],
 'p': [".....", ".....", "####.", "#...#", "#...#", "#...#", "####.", "#....", "#...."],
 'r': [".....", ".....", "#.##.", "##...", "#....", "#....", "#...."],
 'e': [".....", ".....", ".###.", "#...#", "#####", "#....", ".###."],
 'm': [".....", ".....", "##.#.", "#.#.#", "#.#.#", "#...#", "#...#"],
 'b': ["#....", "#....", "####.", "#...#", "#...#", "#...#", "####."],
 'l': ["..#..", "..#..", "..##.", "..#..", ".##..", "..#..", "..#.."],  # ł
 'y': [".....", ".....", "#...#", "#...#", "#...#", ".####", "....#", "#...#", ".###."],
}
G['\u0142'] = G['l']  # ł


def text_img(text, color, scale):
    w = len(text) * 6 - 1
    img = Image.new("RGBA", (w, 9), (0, 0, 0, 0))
    px = img.load()
    x = 0
    for ch in text:
        for r, row in enumerate(G[ch]):
            for c, v in enumerate(row):
                if v == '#':
                    px[x + c, r] = color
        x += 6
    return img.resize((w * scale, 9 * scale), Image.NEAREST)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)


def make_cape(name, base, edge, deco):
    img = Image.new("RGBA", (64 * S, 32 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for (x, y, w, h) in [(0, 1, 1, 16), (1, 0, 10, 1), (11, 0, 10, 1),
                         (1, 1, 10, 16), (11, 1, 1, 16)]:
        d.rectangle([x * S, y * S, (x + w) * S - 1, (y + h) * S - 1], fill=base)
    # wnetrze
    d.rectangle([12 * S, 1 * S, 22 * S - 1, 17 * S - 1], fill=shade(base, 0.75))
    # obramowanie zewnetrznej strony
    d.rectangle([1 * S, 1 * S, 11 * S - 1, 17 * S - 1], outline=edge, width=2)
    ox, oy, ow, oh = 1 * S, 1 * S, 10 * S, 16 * S
    if deco:
        kind = deco[0]
        if kind == "supreme":
            txt = text_img("Supreme", (255, 255, 255, 255), 2).rotate(-90, expand=True)
            bw, bh = txt.width + 14, txt.height + 14
            bx, by = ox + (ow - bw) // 2, oy + (oh - bh) // 2
            d.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=(237, 28, 36, 255))
            img.paste(txt, (bx + 7, by + 7), txt)
        elif kind == "vtext":
            txt = text_img(deco[1], deco[2], 2).rotate(-90, expand=True)
            img.paste(txt, (ox + (ow - txt.width) // 2, oy + (oh - txt.height) // 2), txt)
        elif kind == "boss":
            txt = text_img("BOSS", (255, 255, 255, 255), 3)
            img.paste(txt, (ox + (ow - txt.width) // 2, oy + (oh - txt.height) // 2), txt)
    img.save(os.path.join(ROOT, "cape", name + ".png"))


BLACK = (17, 17, 20, 255)
WHITE = (242, 242, 242, 255)
BLUE = (30, 95, 216, 255)
PURPLE = (106, 31, 181, 255)
W_ = (255, 255, 255, 255)
K_ = (10, 10, 10, 255)

make_cape("supreme_black", BLACK, (60, 60, 66, 255), ("supreme",))
make_cape("supreme_white", WHITE, (170, 170, 170, 255), ("supreme",))
make_cape("bulbely_black", BLACK, (60, 60, 66, 255), ("vtext", "bu\u0142be\u0142y", W_))
make_cape("bulbely_white", WHITE, (170, 170, 170, 255), ("vtext", "bu\u0142be\u0142y", K_))
make_cape("bulbely_blue", BLUE, (20, 60, 150, 255), ("vtext", "bu\u0142be\u0142y", W_))
make_cape("purple", PURPLE, (70, 15, 125, 255), None)
make_cape("boss_purple", PURPLE, (70, 15, 125, 255), ("boss",))
make_cape("boss_black", BLACK, (60, 60, 66, 255), ("boss",))

# ---------- skrzydla (polowka 160x200, szczyt skrzydla po lewej, kregoslup po prawej) ----------
WW, WH = 160, 200
SH = (150, 12)   # bark
EL = (75, 10)    # lokiec
TIPS = [(0, 45), (12, 105), (45, 160), (100, 196), (140, 170)]


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def outline(scallop):
    pts = [SH, EL, TIPS[0]]
    for i in range(len(TIPS) - 1):
        m = lerp(TIPS[i], TIPS[i + 1], 0.5)
        m = lerp(m, EL, scallop)
        pts += [m, TIPS[i + 1]]
    return pts


def dragon(name, membrane, bone, line):
    img = Image.new("RGBA", (WW, WH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = outline(0.30)
    d.polygon(pts, fill=membrane)
    d.line(pts + [pts[0]], fill=line, width=3)
    d.line([SH, EL], fill=bone, width=8)
    for t in TIPS:
        d.line([EL, t], fill=bone, width=6)
    d.line([SH, TIPS[-1]], fill=bone, width=5)
    return img


def fire(name):
    rnd = random.Random(7)
    img = Image.new("RGBA", (WW, WH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    base = outline(0.12)
    # poszarpane jezyki ognia
    jag = []
    for i in range(len(base)):
        a, b = base[i], base[(i + 1) % len(base)]
        jag.append(a)
        if i >= 2:  # tylko krawedz zewnetrzna
            n = 4
            dx, dy = a[0] - EL[0], a[1] - EL[1]
            for k in range(1, n):
                p = lerp(a, b, k / n)
                ox, oy = p[0] - EL[0], p[1] - EL[1]
                ln = max(1.0, (ox * ox + oy * oy) ** 0.5)
                amp = (11 if k % 2 else -7) + rnd.randint(-3, 3)
                jag.append((p[0] + ox / ln * amp, p[1] + oy / ln * amp))
    layers = [(1.0, (190, 25, 5, 255)), (0.86, (240, 85, 10, 255)),
              (0.68, (255, 160, 20, 255)), (0.48, (255, 225, 90, 255)),
              (0.28, (255, 250, 200, 255))]
    for k, col in layers:
        poly = [(SH[0] + (x - SH[0]) * k, SH[1] + (y - SH[1]) * k) for x, y in jag]
        d.polygon(poly, fill=col)
    return img


def save_wing(name, right_half):
    tex = Image.new("RGBA", (WW * 2, WH), (0, 0, 0, 0))
    tex.paste(right_half.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
    tex.paste(right_half, (WW, 0))
    tex.save(os.path.join(ROOT, "wings", name + ".png"))


save_wing("dragon_black", dragon("b", (18, 14, 24, 255), (52, 46, 60, 255), (95, 60, 140, 255)))
save_wing("dragon_white", dragon("w", (212, 212, 226, 255), (255, 255, 255, 255), (130, 130, 150, 255)))
save_wing("fire", fire("f"))
print("OK")
