from fontParts.world import NewFont

EM = 1000

glyph_colors = {
    "A": ("#00FFFF", 0),
    "S": ("#FF00FF", 1),
    "D": ("#FFFF00", 2),
    "F": ("#FF0000", 3),
    "J": ("#00FF00", 4),
    "K": ("#0000FF", 5),
    "L": ("#FFFFFF", 6),
    "semicolon": ("#000000", 7),
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

f = NewFont()
f.info.unitsPerEm = EM
f.info.ascender = EM
f.info.descender = 0

# --- CPAL palette ---
palette = []
for char, gname in char_map.items():
    _, palette_index = glyph_colors[gname]

    # base glyph (empty, but REQUIRED)
    g = f.newGlyph(gname)
    g.clear()
    g.width = EM
    g.unicode = ord(char)

    # color layer glyph (REAL glyph, not UFO layer)
    layer_glyph_name = f"{gname}.color0"
    lg = f.newGlyph(layer_glyph_name)
    lg.width = EM

    pen = lg.getPen()
    pen.moveTo((0, 0))
    pen.lineTo((EM, 0))
    pen.lineTo((EM, EM))
    pen.lineTo((0, EM))
    pen.closePath()

    # map base glyph → layer glyph
    g.lib["public.colorLayerMapping"] = [
        (layer_glyph_name, palette_index)
    ]


f.save("BoxColor.ufo")
