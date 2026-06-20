---
name: logo
description: Create a logo for this repo. Use when the user asks for a logo specifically for this repository. Produces a matched light/dark pair and wires up theme-aware switching in the README.
---

# Logo

Create a **matched pair** of 1590x1098 PNG logos that succinctly represent this
repository — `logo-light.png` and `logo-dark.png` — and wire the README header
to auto-switch between them by color scheme.

Repeat the repo title at the bottom of the badge, color-coordinated with the
neon hero; otherwise keep text to a minimum.

## The look

An app-icon-style **glossy dark-glass badge** holding a **neon-green hero
glyph** with a soft neon glow, the repo name set beneath. Modern / techy, dark
neon aesthetic, suitable as an app icon / favicon. The dark-glass badge is used
in *both* variants — only the surrounding canvas, the badge's depth treatment,
and the title color change between light and dark.

## What stays the same vs. what changes

This is a **brand family**: the frame and coloring are fixed so every repo's
logo is recognizably related. Only two things change per repo.

**Keep identical (the brand frame):**
- The dark-glass badge: size, corner radius, gradient, neon hairline border,
  top gloss sheen.
- The full color palette (below).
- The neon glow treatment on the hero.
- Typography choices and the layout (badge centered up top, title centered
  beneath).
- The light/dark variant rules and the README auto-switch.

**Change per repo:**
- **Hero glyph** — the neon-green mark inside the badge. Pick something that
  captures the repo's name/theme. Draw it flat in the signature neon green; the
  glow is applied automatically. (This repo's hero is a viewfinder/"template
  frame" of four corner brackets around a lowercase `uv` monogram.)
- **Title** — the repo name, printed under the badge.

## Design system

Signature neon green over tight neutrals; geometric **Jost** for display and
retro **Space Mono** for metadata/labels; glossy dark-glass badge treatment;
minimal-hue philosophy.

### Color palette

| Role | RGB | Hex | Notes |
|------|-----|-----|-------|
| Signature neon green | `134, 239, 172` | `#86efac` | hero glyph, border, dark-mode title |
| Neon bright core | `190, 250, 213` | `#befdd5` | inner glow core |
| Deep green | `21, 128, 61` | `#15803d` | light-mode title (contrast on white) |
| Glass top → bottom | `34,37,46` → `9,10,13` | `#22252e` → `#090a0d` | badge body gradient |
| Dark canvas top → bottom | `12,13,16` → `6,6,8` | `#0c0d10` → `#060608` | dark variant background |
| Light canvas top → bottom | `251,251,253` → `231,232,236` | `#fbfbfd` → `#e7e8ec` | light variant background |

### Geometry (at 1x; render at 2x supersample, then downscale with LANCZOS)

- Canvas `1590 x 1098`.
- **Badge (fixed): `600 x 600` square, centered horizontally, top edge at
  `y = 165`, corner radius `132`.** This central glass rectangle is a constant
  of the brand frame — it is the same size and position in every variant and
  every repo, and must not be resized to fit the hero or title. In
  `make_logo.py` it is the module-level `BADGE_*` constants; the hero scales to
  fit `HERO_BOX`, never the reverse.
- Neon hairline border: `#86efac` at alpha 70, width 2.
- Top gloss: white at alpha ~26 over the upper 46% of the badge, blurred.
- Hero sits inside a `118` px inner margin from the badge edge.
- Title: Jost weight 500, auto-fit to ~`1010` px max width, baseline ~`108` px
  below the badge.

### Hero glow recipe

Draw the hero flat in `#86efac` on a transparent layer, then composite, under
the crisp glyph, three blurred copies of it (blur 34/16/6 px at alpha
150/150/120) plus a small bright-core pass tinted `#befdd5`. This is generic —
any hero shape picks up the same glow.

### Typography

- **Jost** (geometric, variable weight) — hero lettering and the title.
- **Space Mono** — reserved for any mono metadata/labels.
- Fonts (OFL) live in `fonts/` next to the generator. If absent, fetch from
  Google Fonts: `ofl/jost/Jost[wght].ttf` and
  `ofl/spacemono/SpaceMono-Regular.ttf`.

### Light vs. dark variants

| Element | Dark variant | Light variant |
|---------|--------------|---------------|
| Canvas | dark gradient + soft radial green pool | light gradient |
| Badge depth | neon green halo behind badge | soft offset drop shadow |
| Badge & hero | dark glass + neon glyph | **identical** |
| Title | `#86efac` with soft glow | `#15803d`, no glow |

Rationale: the neon halo and glowing title disappear on white, so the light
variant swaps them for a drop shadow and a deeper green that holds contrast;
the badge itself never changes.

## How to build

1. Edit `make_logo.py` (next to this file): set `TITLE` to the repo name and
   replace the body of `draw_hero(...)` with this repo's glyph (keep the fill
   color `neon`).
2. From the repo root, run it with the project's environment:
   ```bash
   uv run python .claude/skills/logo/make_logo.py
   ```
   It writes `logo-light.png` and `logo-dark.png` to the current directory.
3. Review both on light and dark backgrounds before committing.

## README auto theme switching

Use a `<picture>` element so the README serves the matching variant by color
scheme (GitHub honors `prefers-color-scheme`). List the dark `<source>` first
and the light `<img>` as the default fallback:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png" />
  <img src="logo-light.png" align="right" width=200 alt="<repo-name> logo" />
</picture>
```
