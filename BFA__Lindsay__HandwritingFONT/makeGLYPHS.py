from fontParts.world import OpenFont

font = OpenFont("LOSTandFOUND_Regular.ufo", showInterface=False)

for name in "abcdefghijklmnopqrstuvwxyz":
    if name not in font:
        glyph = font.newGlyph(name)
        glyph.width = 600
        glyph.unicode = ord(name)

for name in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if name not in font:
        glyph = font.newGlyph(name)
        glyph.width = 600
        glyph.unicode = ord(name)

for suffix in ["_2", "_3"]:
    for base in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
        glyph_name = base + suffix
        if glyph_name not in font:
            glyph = font.newGlyph(glyph_name)
            glyph.width = 600
            # No unicode for alternates

font.save()
font.close()