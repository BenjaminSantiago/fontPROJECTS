from fontParts.world import OpenFont
import math

# -------------------------
# SETTINGS
# -------------------------

UFO_PATH = "TEST__compREDISTRIBUTE_Regular.ufo"     # <-- change this
SOURCE_GLYPH = "s"            # curve glyph
COMPONENT_GLYPH = "dingus"       # glyph to distribute
TARGET_GLYPH = "S_decorated"  # output glyph
SPACING = 30                 # distance between components
SUBDIVISIONS = 40             # curve resolution (higher = smoother)

# -------------------------
# LOAD FONT
# -------------------------

font = OpenFont(UFO_PATH, showInterface=False)

source = font[SOURCE_GLYPH]

if TARGET_GLYPH in font:
    target = font[TARGET_GLYPH]
    target.clear()
else:
    target = font.newGlyph(TARGET_GLYPH)

# -------------------------
# UTILITIES
# -------------------------

def sample_cubic(p0, p1, p2, p3, steps=20):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (
            (1 - t) ** 3 * p0[0]
            + 3 * (1 - t) ** 2 * t * p1[0]
            + 3 * (1 - t) * t ** 2 * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            (1 - t) ** 3 * p0[1]
            + 3 * (1 - t) ** 2 * t * p1[1]
            + 3 * (1 - t) * t ** 2 * p2[1]
            + t ** 3 * p3[1]
        )
        pts.append((x, y))
    return pts


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


# -------------------------
# STEP 1: SAMPLE CURVE
# -------------------------

all_points = []

for contour in source:
    segments = contour.segments

    if not segments:
        continue

    # get starting on-curve
    if not contour.open:
        # closed contour → start from first segment's on-curve
        first_seg = segments[0]
        first_pt = first_seg.points[-1]
        prev_on = (first_pt.x, first_pt.y)

        # IMPORTANT: rotate segments so we don't double-count seam
        segments = segments[1:] + [segments[0]]

    else:
        first_seg = segments[0]
        first_pt = first_seg.points[0]
        prev_on = (first_pt.x, first_pt.y)

    # --- PROCESS SEGMENTS ---
    for segment in segments:
        pts = segment.points

        if segment.type == "line":
            p0 = prev_on
            p1 = (pts[0].x, pts[0].y)

            for i in range(SUBDIVISIONS + 1):
                t = i / SUBDIVISIONS
                x = p0[0] + t * (p1[0] - p0[0])
                y = p0[1] + t * (p1[1] - p0[1])

                if all_points and i == 0:
                    continue

                all_points.append((x, y))

            prev_on = p1

        elif segment.type == "curve":
            # pts = [off1, off2, on]
            p0 = prev_on
            p1 = (pts[0].x, pts[0].y)
            p2 = (pts[1].x, pts[1].y)
            p3 = (pts[2].x, pts[2].y)

            sampled = sample_cubic(p0, p1, p2, p3, SUBDIVISIONS)

            if all_points:
                sampled = sampled[1:]

            all_points.extend(sampled)

            prev_on = p3

        elif segment.type == "qcurve":
            # skip or approximate later if needed
            prev_on = (pts[-1].x, pts[-1].y)

        elif segment.type == "move":
            prev_on = (pts[0].x, pts[0].y)

# -------------------------
# STEP 2: ARC LENGTH
# -------------------------

lengths = [0]

for i in range(1, len(all_points)):
    lengths.append(lengths[-1] + dist(all_points[i - 1], all_points[i]))

total_length = lengths[-1]

# -------------------------
# STEP 3: EVEN SAMPLING
# -------------------------

positions = []

d = 0
while d < total_length:
    for i in range(1, len(lengths)):
        if lengths[i] >= d:
            seg_len = lengths[i] - lengths[i - 1]

            if seg_len == 0:
                continue

            t = (d - lengths[i - 1]) / seg_len

            x = all_points[i - 1][0] + t * (all_points[i][0] - all_points[i - 1][0])
            y = all_points[i - 1][1] + t * (all_points[i][1] - all_points[i - 1][1])

            # wrap-safe tangent
            next_i = (i + 1) % len(all_points)
            prev_i = (i - 1) % len(all_points)

            dx = all_points[next_i][0] - all_points[prev_i][0]
            dy = all_points[next_i][1] - all_points[prev_i][1]

            angle = math.degrees(math.atan2(dy, dx))

            positions.append((x, y, angle))
            break

    d += SPACING

# -------------------------
# STEP 4: PLACE COMPONENTS
# -------------------------

for x, y, angle in positions:
    comp = target.appendComponent(COMPONENT_GLYPH)

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # affine transform: (a, b, c, d, tx, ty)
    comp.transformation = (
        cos_a, sin_a,
        -sin_a, cos_a,
        x, y
    )

# optional: match width
target.width = source.width

# -------------------------
# SAVE
# -------------------------

font.save()
font.close()

print("DONE.")