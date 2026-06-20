"""Reference generator for the neon-glass repo logo.

Produces a matched pair, ``logo-light.png`` and ``logo-dark.png`` (1590x1098),
in one run::

    uv run python make_logo.py            # writes both variants

The BRAND FRAME below (badge geometry, glass treatment, neon border, gloss,
glow, colors, typography, layout) is meant to stay identical across repos so
every project's logo is recognizably part of the same family. Only two things
should change per repo:

  1. TITLE            - the repo name printed under the badge.
  2. draw_hero(...)   - the neon-green glyph drawn inside the badge.

Everything a hero draws (in NEON) automatically picks up the glow treatment,
so a hero only needs to draw flat NEON shapes/text inside the given frame box.

Fonts (Open Font License) are expected next to this script in ``fonts/``::

    Jost[wght].ttf          # geometric variable display face
    SpaceMono-Regular.ttf   # retro mono for labels/metadata

Download them from Google Fonts if missing:
    https://github.com/google/fonts/raw/main/ofl/jost/Jost%5Bwght%5D.ttf
    https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Regular.ttf
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ==== PER-REPO SETTINGS (change these) ====================================
TITLE = 'template-uv-project'   # repo name, printed under the badge


def draw_hero(md, box, neon):
    """Draw this repo's neon glyph inside the badge.

    Parameters
    ----------
    md : PIL.ImageDraw.ImageDraw
        Draw onto this (a transparent layer); the glow is added afterwards.
    box : tuple of int
        ``(x0, y0, x1, y1)`` inner frame the glyph should fit within.
    neon : tuple of int
        The signature neon green RGB to draw with.

    Notes
    -----
    Draw only flat ``neon`` shapes/text -- the caller blurs a copy of this
    layer to make the glow, so no glow handling is needed here. This default
    is the ``template-uv-project`` hero: a viewfinder/template frame (four
    corner brackets) around a lowercase ``uv`` monogram. Replace the body for
    other repos; keep the fill color ``neon``.
    """
    fx0, fy0, fx1, fy1 = box
    arm, th, cr = int(96 * SS), int(26 * SS), int(8 * SS)

    def box_sorted(x0, y0, x1, y1):
        return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]

    def bracket(x, y, dx, dy):  # L bracket with its corner at (x, y)
        md.rounded_rectangle(box_sorted(x, y, x + dx * arm, y + dy * th), cr, fill=neon)
        md.rounded_rectangle(box_sorted(x, y, x + dx * th, y + dy * arm), cr, fill=neon)

    bracket(fx0, fy0, +1, +1)
    bracket(fx1, fy0, -1, +1)
    bracket(fx0, fy1, +1, -1)
    bracket(fx1, fy1, -1, -1)

    font = jost(int(196 * SS), weight=600)
    txt = 'uv'
    tb = md.textbbox((0, 0), txt, font=font)
    cx, cy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    md.text((cx - (tb[2] - tb[0]) // 2 - tb[0], cy - (tb[3] - tb[1]) // 2 - tb[1]),
            txt, font=font, fill=neon)


# ==== BRAND FRAME (keep identical across repos) ===========================
SS = 2                          # supersampling factor for crisp edges
W, H = 1590 * SS, 1098 * SS

# palette
BG_TOP, BG_BOT = (12, 13, 16), (6, 6, 8)            # dark canvas gradient
LIGHT_TOP, LIGHT_BOT = (251, 251, 253), (231, 232, 236)  # light canvas gradient
GLASS_TOP, GLASS_BOT = (34, 37, 46), (9, 10, 13)    # dark-glass badge gradient
NEON = (134, 239, 172)          # #86efac signature neon green (hero + dark title)
NEON_BRIGHT = (190, 250, 213)   # lighter core that sells the glow
DEEP_GREEN = (21, 128, 61)      # #15803d title color for the light variant

# badge geometry -- FIXED brand frame; identical for every repo. The central
# glass rectangle never resizes; the hero scales to fit BADGE_INNER, the badge
# never grows to fit the hero.
BADGE_SIZE = 600 * SS                       # side length of the glass square
BADGE_TOP = 165 * SS                        # distance from canvas top
BADGE_RADIUS = 132 * SS                     # corner radius
BADGE_X0 = W // 2 - BADGE_SIZE // 2         # centered horizontally
BADGE_Y0 = BADGE_TOP
BADGE_X1 = BADGE_X0 + BADGE_SIZE
BADGE_Y1 = BADGE_Y0 + BADGE_SIZE
BADGE_BOX = [BADGE_X0, BADGE_Y0, BADGE_X1, BADGE_Y1]
HERO_MARGIN = 118 * SS                       # inset of the hero frame from edge
HERO_BOX = (BADGE_X0 + HERO_MARGIN, BADGE_Y0 + HERO_MARGIN,
            BADGE_X1 - HERO_MARGIN, BADGE_Y1 - HERO_MARGIN)

_HERE = os.path.dirname(os.path.abspath(__file__))
FONT_JOST = os.path.join(_HERE, 'fonts', 'Jost[wght].ttf')
FONT_MONO = os.path.join(_HERE, 'fonts', 'SpaceMono-Regular.ttf')


def jost(size, weight=400):
    f = ImageFont.truetype(FONT_JOST, size)
    f.set_variation_by_axes([weight])
    return f


def vgrad(top, bot):
    """Full-canvas vertical gradient."""
    g = Image.new('RGB', (1, H))
    for y in range(H):
        t = y / (H - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g.resize((W, H))


def render(theme):
    """Render one variant; ``theme`` is ``'light'`` or ``'dark'``."""
    # --- canvas ---
    if theme == 'light':
        img = vgrad(LIGHT_TOP, LIGHT_BOT).convert('RGBA')
    else:
        img = vgrad(BG_TOP, BG_BOT).convert('RGBA')
        lift_mask = Image.new('L', (W, H), 0)            # soft radial pool of light
        ImageDraw.Draw(lift_mask).ellipse(
            [W // 2 - 520 * SS, int(H * 0.42) - 380 * SS,
             W // 2 + 520 * SS, int(H * 0.42) + 380 * SS], fill=70)
        lift_mask = lift_mask.filter(ImageFilter.GaussianBlur(220 * SS))
        img.paste(Image.new('RGBA', (W, H), (26, 40, 32, 255)), (0, 0), lift_mask)

    draw = ImageDraw.Draw(img)

    # The badge uses the FIXED module-level geometry (BADGE_BOX) in every
    # variant, so the central glass rectangle is the exact same size and
    # position regardless of theme, hero, or title.

    # --- depth behind the badge: shadow (light) or neon halo (dark) ---
    if theme == 'light':
        shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            [BADGE_X0, BADGE_Y0 + 16 * SS, BADGE_X1, BADGE_Y1 + 16 * SS],
            BADGE_RADIUS, fill=(20, 24, 30, 90))
        img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(46 * SS)))
    else:
        halo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(halo).rounded_rectangle(BADGE_BOX, BADGE_RADIUS, fill=(*NEON, 90))
        img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(55 * SS)))

    # --- glass body (dark in BOTH themes) ---
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(BADGE_BOX, BADGE_RADIUS, fill=255)
    img.paste(vgrad(GLASS_TOP, GLASS_BOT).convert('RGBA'), (0, 0), mask)

    # --- top gloss sheen ---
    gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gloss).rounded_rectangle(
        [BADGE_X0, BADGE_Y0, BADGE_X1, BADGE_Y0 + int(BADGE_SIZE * 0.46)],
        BADGE_RADIUS, fill=(255, 255, 255, 26))
    gloss = gloss.filter(ImageFilter.GaussianBlur(26 * SS))
    img.paste(gloss, (0, 0),
              Image.composite(gloss.getchannel('A'), Image.new('L', (W, H), 0), mask))

    # --- neon hairline border ---
    draw.rounded_rectangle(BADGE_BOX, BADGE_RADIUS, outline=(*NEON, 70), width=2 * SS)

    # --- hero glyph + glow (drawn inside the fixed HERO_BOX) ---
    mark = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_hero(ImageDraw.Draw(mark), HERO_BOX, NEON)
    for blur, alpha in [(34 * SS, 150), (16 * SS, 150), (6 * SS, 120)]:
        g = mark.filter(ImageFilter.GaussianBlur(blur))
        g.putalpha(g.getchannel('A').point(lambda a: min(255, a * alpha // 255)))
        img.alpha_composite(g)
    core = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # bright inner core
    core.paste(Image.new('RGBA', (W, H), (*NEON_BRIGHT, 255)), (0, 0), mark.getchannel('A'))
    img.alpha_composite(core.filter(ImageFilter.GaussianBlur(3 * SS)))
    img.alpha_composite(mark)

    # --- title under the badge (auto-fit width) ---
    size = int(118 * SS)
    font = jost(size, weight=500)
    while draw.textlength(TITLE, font=font) > int(1010 * SS) and size > 40:
        size -= 2 * SS
        font = jost(size, weight=500)
    ty = BADGE_Y1 + int(108 * SS)
    tx = W // 2 - draw.textlength(TITLE, font=font) / 2
    if theme == 'light':
        draw.text((tx, ty), TITLE, font=font, fill=DEEP_GREEN)
    else:
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).text((tx, ty), TITLE, font=font, fill=(*NEON, 200))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14 * SS)))
        draw.text((tx, ty), TITLE, font=font, fill=NEON)

    out = img.convert('RGB').resize((1590, 1098), Image.LANCZOS)
    path = f'logo-{theme}.png'
    out.save(path)
    print('saved', path)


if __name__ == '__main__':
    render('light')
    render('dark')
