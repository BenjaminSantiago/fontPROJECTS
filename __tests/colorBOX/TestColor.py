from fontParts.world import NewFont

EM = 1000

f = NewFont()
f.info.familyName = "TestColor"
f.info.styleName = "Regular"
f.info.unitsPerEm = EM
f.info.ascender = EM
f.info.descender = 0

# palette (CPAL intent)
f.naked().lib["public.colorPalettes"] = [
    [(1.0, 0.0, 1.0, 1.0)]
]

# base glyph A (empty by design)
g = f.newGlyph("A")
g.clear()
g.width = EM
g.unicode = ord("A")

# layer glyph A.color0 (contains geometry)
lg = f.newGlyph("A.color0")
lg.width = EM

pen = lg.getPen()
pen.moveTo((0, 0))
pen.lineTo((EM, 0))
pen.lineTo((EM, EM))
pen.lineTo((0, EM))
pen.closePath()

# map base → layer glyph (THIS IS THE CRITICAL LINE)
g.naked().lib["public.colorLayerMapping"] = [
    ("A.color0", 0)
]

f.save("TestColor-Regular.ufo")
print("saved")
