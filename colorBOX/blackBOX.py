from fontParts.world import NewFont

EM = 1000

# Only these glyphs
char_map = {
    "A": "A",
    "S": "S",
    "D": "D",
    "F": "F",
    "J": "J",
    "K": "K",
    "L": "L",
    ";": "semicolon",
}

f = NewFont()

# Font info
f.info.familyName = "blackbox"
f.info.styleName = "Regular"
f.info.unitsPerEm = EM
f.info.ascender = EM
f.info.descender = 0

# Optional but nice-to-have naming bits
f.info.postscriptFontName = "blackbox-Regular"
f.info.postscriptFullName = "blackbox Regular"

for char, gname in char_map.items():
    g = f.newGlyph(gname)
    g.clear()

    # 0 sidebearings because the box spans exactly 0..EM and width is EM
    g.width = EM

    # Map unicode (semicolon gets its codepoint too)
    g.unicode = ord(char)

    # Draw full EM-square box (touches both sidebearings)
    pen = g.getPen()
    pen.moveTo((0, 0))
    pen.lineTo((EM, 0))
    pen.lineTo((EM, EM))
    pen.lineTo((0, EM))
    pen.closePath()

# Save UFO
f.save("blackbox-Regular.ufo")
print("Wrote blackbox-Regular.ufo")
