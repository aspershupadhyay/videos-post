"""Build the CatchTheError logo set as self-contained SVGs.

The wordmark is outlined from Bricolage Grotesque (wdth 75, wght 800) so the
files render the same everywhere, with no font installed.

    python3 brand/build_logo.py
"""

from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
FONT = ROOT.parent / "videos/case-017-artcraft/assets/fonts/BricolageGrotesque.woff2"
OUT = ROOT / "logo"

PAPER = "#F2E8D5"
INK = "#1B1814"
RUST = "#C2502A"
TEAL = "#0E4A4A"
MUSTARD = "#E2A72E"


def mark(ink=INK, body=RUST, seam=PAPER, glint=MUSTARD, lens=None):
    """The lens-and-bug mark, drawn in a 512 x 512 box."""
    lens_fill = f'<circle cx="214" cy="214" r="134" fill="{lens}"/>' if lens else ""
    legs = [
        ((168, 196), (124, 172)),
        ((164, 228), (112, 228)),
        ((170, 262), (128, 292)),
    ]
    leg_paths = "".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}"/>'
        f'<path d="M{428 - a[0]} {a[1]} L{428 - b[0]} {b[1]}"/>'
        for a, b in legs
    )
    return f"""
  <g id="mark">
    {lens_fill}
    <path d="M318 318 L446 446" stroke="{ink}" stroke-width="62" stroke-linecap="round"/>
    <path d="M300 300 L334 334" stroke="{ink}" stroke-width="82" stroke-linecap="butt"/>
    <circle cx="214" cy="214" r="150" fill="none" stroke="{ink}" stroke-width="34"/>
    <path d="M110 170 A112 112 0 0 1 170 110" fill="none" stroke="{glint}" stroke-width="12" stroke-linecap="round"/>
    <g stroke="{ink}" stroke-width="11" stroke-linecap="round" fill="none">
      {leg_paths}
      <path d="M204 150 L186 116"/>
      <path d="M224 150 L242 116"/>
    </g>
    <ellipse cx="214" cy="236" rx="52" ry="66" fill="{body}"/>
    <path d="M214 178 L214 298" stroke="{seam}" stroke-width="7" stroke-linecap="round"/>
    <circle cx="214" cy="166" r="22" fill="{ink}"/>
  </g>"""


def load_font():
    font = TTFont(FONT)
    return instantiateVariableFont(font, {"wght": 800, "wdth": 75, "opsz": 96}, inplace=False)


def text_path(font, text, size, x, y, tracking=0.0):
    """Outline `text` with its baseline at (x, y); returns (svg path d, advance)."""
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(glyph_set)
    cursor = 0.0
    for ch in text:
        name = cmap[ord(ch)]
        glyph = glyph_set[name]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x + cursor, y)))
        cursor += glyph.width * scale + tracking * size
    return pen.getCommands(), cursor - tracking * size


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f"{rect}{body}</svg>\n"
    )


def main():
    OUT.mkdir(exist_ok=True)
    font = load_font()

    # Mark alone, transparent.
    (OUT / "mark.svg").write_text(svg(512, 512, mark()))
    (OUT / "mark-reversed.svg").write_text(svg(512, 512, mark(ink=PAPER, seam=TEAL)))

    # Profile pictures: platforms crop to a circle, so the mark sits inside 80%.
    def avatar(bg, **kw):
        return svg(
            1080, 1080,
            f'<g transform="translate(540 540) scale(1.72) translate(-262 -262)">{mark(**kw)}</g>',
            bg=bg,
        )

    (OUT / "avatar-paper.svg").write_text(avatar(PAPER))
    (OUT / "avatar-rust.svg").write_text(avatar(RUST, body=INK, seam=RUST, lens=PAPER))
    (OUT / "avatar-teal.svg").write_text(avatar(TEAL, ink=PAPER, seam=TEAL, lens=None))

    # Horizontal lockup: mark + CATCHTHE / ERROR stacked.
    def lockup(ink, accent, seam, bg=None):
        top, top_w = text_path(font, "CATCH THE", 150, 560, 250, tracking=0.01)
        bottom, bottom_w = text_path(font, "ERROR", 236, 556, 450, tracking=0.0)
        width = int(560 + max(top_w, bottom_w) + 60)
        rule_y = 478
        body = (
            f'<g transform="translate(20 20) scale(0.94)">{mark(ink=ink, seam=seam)}</g>'
            f'<path d="{top}" fill="{ink}"/>'
            f'<path d="{bottom}" fill="{accent}"/>'
            f'<rect x="560" y="{rule_y}" width="{bottom_w:.0f}" height="16" fill="{MUSTARD}"/>'
        )
        return svg(width, 512, body, bg=bg)

    (OUT / "lockup.svg").write_text(lockup(INK, RUST, PAPER))
    (OUT / "lockup-on-paper.svg").write_text(lockup(INK, RUST, PAPER, bg=PAPER))
    (OUT / "lockup-reversed.svg").write_text(lockup(PAPER, MUSTARD, TEAL, bg=TEAL))

    # Wordmark only, for the video end card and thin placements.
    word, word_w = text_path(font, "CATCHTHEERROR", 200, 0, 170)
    split, split_w = text_path(font, "CATCHTHE", 200, 0, 170)
    err, _ = text_path(font, "ERROR", 200, split_w, 170)
    (OUT / "wordmark.svg").write_text(
        svg(int(word_w) + 4, 210, f'<path d="{split}" fill="{INK}"/><path d="{err}" fill="{RUST}"/>')
    )
    print("wrote", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
