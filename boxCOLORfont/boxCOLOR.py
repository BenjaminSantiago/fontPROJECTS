from fontParts.world import NewFont

# --- config ---
EM = 1000

glyph_colors = {
    "A":  "#00FFFF",
    "S":  "#FF00FF",
    "D":  "#FFFF00",
    "F":  "#FF0000",
    "J":  "#00FF00",
    "K":  "#0000FF",
    "L":  "#FFFFFF",
    "semicolon": "#000000",
}

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

# --- make font ---
f = NewFont()
f.info.unitsPerEm = EM
f.info.ascender = EM
f.info.descender = 0

# --- draw box glyphs ---
for char, gname in char_map.items():
    g = f.newGlyph(gname)
    g.width = EM

    # base layer (required, but empty is OK)
    g.clear()

    # color layer
    layer_name = f"color.{gname}"
    layer = f.newLayer(layer_name)

    cg = layer.newGlyph(gname)
    pen = cg.getPen()
    pen.moveTo((0, 0))
    pen.lineTo((EM, 0))
    pen.lineTo((EM, EM))
    pen.lineTo((0, EM))
    pen.closePath()

    # map Unicode
    g.unicode = ord(char)

# save UFO
f.save("BoxColor.ufo")
