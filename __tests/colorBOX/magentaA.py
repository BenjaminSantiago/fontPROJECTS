from fontParts.world import NewFont

EM = 1000

f = NewFont()
f.info.familyName = "Magenta A"
f.info.unitsPerEm = EM
f.info.ascender = EM
f.info.descender = 0

# --- CPAL: one palette, one color (MAGENTA) ---
f.lib["public.colorPalettes"] = [
    [(1.0, 0.0, 1.0, 1.0)]  # index 0 = magenta
]

# --- base glyph A (empty) ---
g = f.newGlyph("A")
g.width = EM
g.unicode = ord("A")
g.clear()

# --- color layer glyph A.color0 ---
lg = f.newLayer("A.color0", (1,0,1,1))

cg = lg.newGlyph("A")
pen = cg.getPen()
pen.moveTo((0, 0))
pen.lineTo((EM, 0))
pen.lineTo((EM, EM))
pen.lineTo((0, EM))
pen.closePath()

# --- map A → A.color0 using palette index 0 ---
g.lib["public.colorLayerMapping"] = [
    ("A.color0", 0)
]

# --- save ---
f.save("MagentaA.ufo")
