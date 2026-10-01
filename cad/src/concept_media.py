"""DustRunner concept media (refreshed at TRL 3 from the parametric model).

Run from the repo root:  python cad/src/concept_media.py
The robot, dock and end stops come from cad/src/model.py (PARAMS), so the media match the
STEP files, drawing DRN-DWG-001 and DRN-CAL-001. The reference table (modules, purlins,
posts) is drawn here for context only. Not for fabrication.

The robot is modeled in the plane of the PV table, in local coordinates (mm):
    u  along the row (the direction of travel)
    v  up the slope, from the lower module edge (v = 0) to the upper edge (v = MOD_L)
    w  normal to the glass, glass surface at w = 0
The table is then tilted by TILT about the row axis and placed with its lower glass edge
at H0 above the ground. In world coordinates the row runs along Y, the glass faces +X
and the slope rises toward -X.

Reference table: one module high in portrait (1P), 2278 x 1134 mm modules, 30 to 35 mm
frames, table clamps on the long sides so the short (top and bottom) edges are clear.
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, human_figure
from model import PARAMS as MP, robot_parts, dock_parts, stop_parts

# ---------------- reference table (grey or blue, no BOM number) ----------------
MOD_L, MOD_W, GAP = MP["mod_l"], MP["mod_w"], MP["gap"]   # module slope length, width along row, gap
N_MOD = 3                                   # modules shown (a real reference row is about 35)
ROW_L = N_MOD * MOD_W + (N_MOD - 1) * GAP
TILT = MP["tilt"]                           # table tilt, degrees
H0 = MP["h0"]                               # lower glass edge above ground
FRAME_W = MP["lip"]                         # visible frame flange width
FRAME_T = MP["frame_d"]                     # frame depth; frame top 1 mm proud of the glass

# ---------------- robot placement ----------------
PLATE_HALF_U = MP["plate_half_u"]
U_ROBOT = MOD_W + GAP + 0.5 * MOD_W        # robot shown mid-way along module 2, moving toward +u

TABLE_GREY = "#9CA3AF"
FRAME_SILVER = "#B8C0C8"
GLASS = "#1E3A8A"
DUST = "#C9A66B"


def T(shape):
    """Local (u, v, w) table coordinates to world."""
    return Pos(0, 0, H0) * Rot(0, 0, 90) * Rot(TILT, 0, 0) * shape


def t_vec(u, v, w):
    """Local vector or point to world (numpy), matching T()."""
    t = np.radians(TILT)
    return np.array([-(v * np.cos(t) - w * np.sin(t)), u, v * np.sin(t) + w * np.cos(t)])


def bx(u0, u1, v0, v1, w0, w1):
    """Axis-aligned box in local coordinates from its extents."""
    return Pos((u0 + u1) / 2, (v0 + v1) / 2, (w0 + w1) / 2) * Box(abs(u1 - u0), abs(v1 - v0), abs(w1 - w0))


def cyl_v(u, w, v0, v1, r):
    """Cylinder with its axis along v."""
    return Pos(u, (v0 + v1) / 2, w) * Rot(90, 0, 0) * Cylinder(r, v1 - v0)


def cyl_w(u, v, w0, w1, r):
    """Cylinder with its axis along w."""
    return Pos(u, v, (w0 + w1) / 2) * Cylinder(r, w1 - w0)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def mirror_v(shape):
    """Mirror a lower-end shape to the upper module edge (v -> MOD_L - v)."""
    return Pos(0, MOD_L, 0) * shape.mirror(Plane.XZ)


# ---------------- table, modules and dust (local) ----------------
def table_local():
    frames = glass = None
    for k in range(N_MOD):
        u0 = k * (MOD_W + GAP)
        ring = bx(u0, u0 + MOD_W, 0, MOD_L, -FRAME_T + 1, 1) - bx(u0 + FRAME_W, u0 + MOD_W - FRAME_W,
                                                                   FRAME_W, MOD_L - FRAME_W, -FRAME_T, 2)
        pane = bx(u0 + FRAME_W, u0 + MOD_W - FRAME_W, FRAME_W, MOD_L - FRAME_W, -4, 0)
        frames = ring if frames is None else frames + ring
        glass = pane if glass is None else glass + pane
    # dust film ahead of the robot (not yet cleaned)
    d0 = U_ROBOT + PLATE_HALF_U + 10
    dust = None
    for k in range(N_MOD):
        u0 = k * (MOD_W + GAP)
        a, b = max(u0 + FRAME_W, d0), u0 + MOD_W - FRAME_W
        if b > a:
            film = bx(a, b, FRAME_W, MOD_L - FRAME_W, 0, 1.2)
            dust = film if dust is None else dust + film
    purlins = bx(-40, ROW_L + 40, 400, 450, -FRAME_T - 60, -FRAME_T) + \
        bx(-40, ROW_L + 40, 1830, 1880, -FRAME_T - 60, -FRAME_T)
    rafters = None
    for u in (300.0, ROW_L - 300.0):
        r = bx(u - 30, u + 30, -80, MOD_L + 80, -FRAME_T - 120, -FRAME_T - 60)
        rafters = r if rafters is None else rafters + r
    return frames, glass, dust, purlins, rafters


def posts_world():
    posts = None
    for u in (300.0, ROW_L - 300.0):
        for v in (350.0, 1950.0):
            top = t_vec(u, v, -FRAME_T - 120) + np.array([0, 0, H0])
            p = tube3((top[0], top[1], 0), tuple(top), 40)
            posts = p if posts is None else posts + p
    return posts


# ---------------- robot, dock and end stops from the parametric model (local) ----------------
def robot_local(u=0.0):
    return {k: Pos(u, 0, 0) * v for k, v in robot_parts(MP).items()}


def stop_local(u_end):
    return stop_parts(u_end, MP)


# ---------------- BOM numbering (matches bom/bom.csv) ----------------
BOM = [
    # key, bom no, name, color
    ("beam", 1, "Chassis beam, 40 x 80 mm", "#64748B"),
    ("brush", 2, "Microfiber brush, 120 mm x 2.2 m", "#14B8A6"),
    ("hood", 3, "Brush hood", "#CBD5E1"),
    ("brush_motor", 4, "Brush motor and belt drive", "#0F766E"),
    ("trucks", 5, "End trucks and wheels (pair)", "#475569"),
    ("drive_motors", 6, "Drive gearmotors (2)", "#115E59"),
    ("rollers", 7, "Guide and hook rollers (set)", "#D4A017"),
    ("battery", 8, "LiFePO4 pack, 12.8 V 10 Ah", "#C2410C"),
    ("controller", 9, "Controller and motor drivers", "#7C3AED"),
    ("sensors", 10, "IR edge sensors (4)", "#0EA5E9"),
]
DOCK_BOM = [
    ("dock", 11, "Dock frame, rails and clamps", "#A16207"),
    ("panel", 12, "Dock PV panel, 20 W", "#3B82F6"),
    ("charge", 13, "Dock charger and contacts", "#16A34A"),
    ("stop", 14, "End stops (pair)", "#B91C1C"),
    ("anemometer", 16, "Dock anemometer", "#DB2777"),
]
NAMES = {k: (n, name, col) for k, n, name, col in BOM + DOCK_BOM}

frames, glass, dust, purlins, rafters = table_local()
robot = robot_local(U_ROBOT)
dock = dock_parts(MP)
dock_frame, dock_panel, dock_charge, dock_anem = dock["dock"], dock["panel"], dock["charge"], dock["anemometer"]
dock["stop"] = stop_local(ROW_L)

table_parts = [
    Part("Reference PV modules, frames (not in BOM)", T(frames), FRAME_SILVER, None),
    Part("Reference PV modules, glass (not in BOM)", T(glass), GLASS, None),
    Part("Dust film, uncleaned (illustrative)", T(dust), DUST, None),
    Part("Table purlins and rafters (existing)", T(purlins + rafters), TABLE_GREY, None),
    Part("Table posts (existing)", posts_world(), TABLE_GREY, None),
]
parts = list(table_parts)
for key, n, name, col in BOM:
    parts.append(Part(name, T(robot[key]), col, n))
for key, n, name, col in DOCK_BOM:
    shape = T(dock[key])
    parts.append(Part(name, shape, col, n))

KEY_FIGURES = [
    "Brush 2.2 m long, 120 mm diameter, about 150 rpm; water-free",
    "Travel 0.2 m/s: 40 m row out and back in about 7.4 min (DRN-CAL-001)",
    "About 67 W while cleaning; about 7.6 Wh per cycle (DRN-CAL-001)",
    "Robot about 13.8 kg; about 55 N per wheel on the frames (DRN-CAL-001)",
    "Robot, dock and anemometer $500 in parts (indicative)",
]

FLOW = {"title": "energy per cleaning cycle, 40 m row out and back, Wh (estimates, DRN-CAL-001 F7)", "unit": "Wh",
        "stages": [("Dock charge in", 7.94), ("Pack output", 7.62), ("Motor input", 7.25), ("Brush and wheels", 4.16)],
        "losses": [(0, "Charging and pack (4 %)", 0.32), (1, "Controller and sensors", 0.37),
                   (2, "Motors and gears (43 %)", 3.09)]}


def exploded_parts():
    """Robot laid flat in the table plane, dock and end stop placed beside it. Numbered callouts
    sit on the lower-end item of each pair; the upper-end twin is shown without a number."""
    r = robot_local(0.0)
    out = []

    def add(key, shape, explode, numbered=True):
        n, name, col = NAMES[key]
        out.append(Part(name if numbered else name + " (twin)", shape, col, n if numbered else None, explode))

    add("beam", r["beam"], (0, 0, 420))
    add("hood", r["hood"], (0, 0, 230))
    add("brush", r["brush"], (0, 0, 0))
    add("battery", r["battery"], (0, 0, 640))
    add("controller", r["controller"], (0, 150, 600))
    add("brush_motor", r["brush_motor"], (250, -650, -250))
    for key, ev in (("trucks", (0, -380, -300)), ("rollers", (0, -380, -620)),
                    ("drive_motors", (350, -520, -460)), ("sensors", (500, -380, -40))):
        add(key, r[key + "_lo"], ev)
        add(key, r[key + "_hi"], (ev[0], -ev[1], ev[2]), numbered=False)
    dk = dock_parts(MP, legs=False)
    dock_frame, dock_panel, dock_charge, dock_anem = dk["dock"], dk["panel"], dk["charge"], dk["anemometer"]
    shift = Pos(2300, 0, 0)                     # dock group drawn beside the robot (schematic)
    add("dock", shift * dock_frame, (0, 0, -150))
    add("panel", shift * dock_panel, (0, 0, 250))
    add("charge", shift * dock_charge, (0, 0, 120))
    add("anemometer", shift * dock_anem, (0, 0, 350))
    stop = stop_local(0.0)
    lo = stop & bx(-100, 100, -100, 200, -200, 200)
    hi = stop & bx(-100, 100, MOD_L - 200, MOD_L + 100, -200, 200)
    add("stop", Pos(1300, 0, 0) * lo, (0, -250, -250))
    add("stop", Pos(1300, 0, 0) * hi, (0, 250, 0), numbered=False)
    return sorted(out, key=lambda p: (p.bom is None, p.bom or 0))


def cutaway_detail():
    """Section across the row through the robot center, cropped to the lower module edge."""
    region = T(bx(U_ROBOT, U_ROBOT + 450, -130, 300, -110, 330))
    out = []
    for p in parts:
        s = p.shape & region
        if s is not None and s.volume > 1e-6:
            out.append(Part(p.name, s, p.color, p.bom))
    return out


if __name__ == "__main__":
    import shutil
    md = Path.cwd() / "media"
    person = human_figure(1750.0, x=500.0, y=ROW_L + 350.0, z=0.0)
    person.name = "1.75 m person"
    render_all(parts, project="DustRunner", title="Row-cleaning crawler concept", dwg_no="DRN-DWG-010",
               key_figures=KEY_FIGURES, cut=False, flow=FLOW, scale_figure=False, context=[person])
    concept._render(exploded_parts(), md / "exploded.png", offsets=True, labels=True, azim=-35, elev=28,
                    title="DustRunner: exploded view",
                    note="Robot laid flat; dock and end stop drawn beside it; numbers match bom/bom.csv")
    concept._render(cutaway_detail(), md / "cutaway.png", azim=-90, elev=0, labels=True,
                    title="DustRunner: section across the row at the lower module edge",
                    note="Silver: module frame; blue: glass. Truck (5) wheels ride the frame top; rollers (7) bear on the frame "
                         "face and hook under its lip")
    for d in md.glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
