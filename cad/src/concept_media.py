"""DustRunner concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

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
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, human_figure

# ---------------- reference table (grey or blue, no BOM number) ----------------
MOD_L, MOD_W, GAP = 2278.0, 1134.0, 20.0   # module slope length, width along row, gap between modules
N_MOD = 3                                   # modules shown (a real reference row is about 35)
ROW_L = N_MOD * MOD_W + (N_MOD - 1) * GAP
TILT = 25.0                                 # table tilt, degrees
H0 = 600.0                                  # lower glass edge above ground
FRAME_W = 25.0                              # visible frame flange width
FRAME_T = 33.0                              # frame depth; frame top 1 mm proud of the glass

# ---------------- robot dimensions ----------------
BRUSH_R = 60.0                              # 120 mm microfiber brush
BRUSH_V = (40.0, MOD_L - 40.0)              # brushed band up the slope
PLATE_V = (-30.0, -22.0)                    # lower end-truck plate, outboard of the frame face (v = 0)
PLATE_HALF_U = 150.0
WHEEL_R, WHEEL_U = 35.0, 100.0
BEAM_W = (138.0, 218.0)

U_ROBOT = MOD_W + GAP + 0.5 * MOD_W        # robot shown mid-way along module 2, moving toward +u
U_PARK = -625.0                             # robot center when parked in the dock

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


# ---------------- robot (local, centered at u = 0) ----------------
def lower_truck():
    plate = bx(-PLATE_HALF_U, PLATE_HALF_U, *PLATE_V, -56, 250)
    hook_arm = bx(-15, 15, PLATE_V[0], 24, -56, -48)
    axles = cyl_v(-WHEEL_U, WHEEL_R + 1, PLATE_V[1], 3, 6) + cyl_v(WHEEL_U, WHEEL_R + 1, PLATE_V[1], 3, 6)
    wheels = cyl_v(-WHEEL_U, WHEEL_R + 1, 3, 23, WHEEL_R) + cyl_v(WHEEL_U, WHEEL_R + 1, 3, 23, WHEEL_R)
    return plate + hook_arm + axles + wheels


def lower_rollers():
    guides = cyl_w(-60, -11, -28, -4, 11) + cyl_w(60, -11, -28, -4, 11)
    hook = cyl_v(0, -FRAME_T + 1 - 8, 3, 21, 8)
    return guides + hook


def robot_local(u=0.0):
    P = Pos(u, 0, 0)
    brush = cyl_v(0, BRUSH_R + 2, *BRUSH_V, BRUSH_R) + cyl_v(0, BRUSH_R + 2, PLATE_V[1], MOD_L - PLATE_V[1], 10)
    hood = (cyl_v(0, BRUSH_R + 2, BRUSH_V[0], BRUSH_V[1], 76) - cyl_v(0, BRUSH_R + 2, BRUSH_V[0] - 1, BRUSH_V[1] + 1, 72)) \
        & bx(-80, 80, BRUSH_V[0], BRUSH_V[1], BRUSH_R + 2, 200)
    beam = bx(-20, 20, PLATE_V[1], MOD_L - PLATE_V[1], *BEAM_W)
    trucks = lower_truck() + mirror_v(lower_truck())
    rollers = lower_rollers() + mirror_v(lower_rollers())
    brush_motor = bx(-35, 35, -95, PLATE_V[0], 30, 100)
    drive_lo = cyl_v(WHEEL_U, WHEEL_R + 1, -80, PLATE_V[0], 22)
    drive_motors = drive_lo + mirror_v(drive_lo)
    sensor = lambda s: bx(s * 150, s * 176, -30, 20, 45, 65)
    sensors = sensor(1) + sensor(-1)
    sensors = sensors + mirror_v(sensors)
    battery = bx(-45, 45, 250, 430, BEAM_W[1], BEAM_W[1] + 100)
    controller = bx(-40, 40, 480, 620, BEAM_W[1], BEAM_W[1] + 55)
    sens_lo = sensor(1) + sensor(-1)
    split = dict(trucks_lo=lower_truck(), trucks_hi=mirror_v(lower_truck()),
                 rollers_lo=lower_rollers(), rollers_hi=mirror_v(lower_rollers()),
                 drive_motors_lo=drive_lo, drive_motors_hi=mirror_v(drive_lo),
                 sensors_lo=sens_lo, sensors_hi=mirror_v(sens_lo))
    return {k: P * s for k, s in dict(beam=beam, brush=brush, hood=hood, brush_motor=brush_motor, trucks=trucks,
                                      drive_motors=drive_motors, rollers=rollers, battery=battery,
                                      controller=controller, sensors=sensors, **split).items()}


# ---------------- dock at the start of the row, end stop at the far end (local) ----------------
DOCK_U0 = -1300.0                           # far end of the dock (panel bay beyond the parking rails)


def dock_local():
    rails = bx(-800, -20, 0, 25, -FRAME_T + 1, 1) + bx(-800, -20, MOD_L - 25, MOD_L, -FRAME_T + 1, 1)
    cross = None
    for u0 in (DOCK_U0, -800, -120):
        c = bx(u0, u0 + 40, 30, MOD_L - 30, -100, -60)
        cross = c if cross is None else cross + c
    brackets = None
    for u0 in (-800, -120):
        for v0 in (30, MOD_L - 60):
            b = bx(u0, u0 + 40, v0, v0 + 30, -60, -FRAME_T + 1)
            brackets = b if brackets is None else brackets + b
    clamps = bx(-60, 60, 30, 70, -50, -FRAME_T + 1) + bx(-60, 60, MOD_L - 70, MOD_L - 30, -50, -FRAME_T + 1)
    clamps = clamps + bx(-60, -20, 30, 70, -FRAME_T + 1, -FRAME_T + 11)
    # panel bay: two side members from the far cross member to the parking cross member
    bay = bx(DOCK_U0, -760, 90, 130, -60, -40) + bx(DOCK_U0, -760, 600, 640, -60, -40)
    frame = rails + cross + brackets + clamps + bay
    panel = bx(-1225, -875, 100, 630, -40, -15)
    charge = bx(DOCK_U0, DOCK_U0 + 100, 700, 800, -60, 0) + bx(-800, -785, -30, 25, 1, 70)
    return frame, panel, charge


def dock_legs_world():
    legs = None
    for u, v in ((-780, 300), (DOCK_U0 + 20, 300), (-780, 1950), (DOCK_U0 + 20, 1950)):
        top = t_vec(u, v, -100) + np.array([0, 0, H0])
        leg = tube3((top[0], top[1], 0), tuple(top), 25)
        legs = leg if legs is None else legs + leg
    return legs


def stop_local(u_end):
    lo = bx(u_end - 40, u_end, 0, 25, 1, 50) + bx(u_end - 40, u_end, 0, 25, -60, -FRAME_T + 1) + \
        bx(u_end - 40, u_end, -12, 0, -60, 50)
    return lo + mirror_v(lo)


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
]
NAMES = {k: (n, name, col) for k, n, name, col in BOM + DOCK_BOM}

frames, glass, dust, purlins, rafters = table_local()
robot = robot_local(U_ROBOT)
dock_frame, dock_panel, dock_charge = dock_local()
dock = {"dock": dock_frame, "panel": dock_panel, "charge": dock_charge, "stop": stop_local(ROW_L)}

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
    if key == "dock":
        shape = shape + dock_legs_world()
    parts.append(Part(name, shape, col, n))

KEY_FIGURES = [
    "Brush 2.2 m long, 120 mm diameter, about 150 rpm; water-free",
    "Travel 0.2 m/s: 40 m row out and back in about 7 min (estimate)",
    "About 70 W while cleaning; about 8 Wh per cycle (estimate)",
    "Robot about 12 kg; about 52 N per wheel on the frames (estimate)",
    "Robot and dock about $485 in parts (indicative)",
]

FLOW = {"title": "energy per cleaning cycle, 40 m row out and back, Wh (estimates)", "unit": "Wh",
        "stages": [("Dock charge in", 8.2), ("Stored in pack", 7.9), ("Pack output", 7.7),
                   ("Motor input", 7.4), ("Brush and wheels", 4.2)],
        "losses": [(0, "Charging (4 %)", 0.3), (1, "Pack and wiring (3 %)", 0.2),
                   (2, "Controller and sensors", 0.3), (3, "Motors and gears (43 %)", 3.2)]}


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
    shift = Pos(2300, 0, 0)                     # dock group drawn beside the robot (schematic)
    add("dock", shift * dock_frame, (0, 0, -150))
    add("panel", shift * dock_panel, (0, 0, 250))
    add("charge", shift * dock_charge, (0, 0, 120))
    stop = stop_local(0.0)
    lo = stop & bx(-100, 100, -100, 200, -200, 200)
    hi = stop & bx(-100, 100, MOD_L - 200, MOD_L + 100, -200, 200)
    add("stop", Pos(700, 0, 0) * lo, (0, -250, -250))
    add("stop", Pos(700, 0, 0) * hi, (0, 250, 0), numbered=False)
    return sorted(out, key=lambda p: (p.bom is None, p.bom or 0))


def cutaway_detail():
    """Section across the row through the robot center, cropped to the lower module edge."""
    region = T(bx(U_ROBOT, U_ROBOT + 450, -130, 300, -110, 330))
    out = []
    for p in parts:
        s = p.shape & region
        if s.volume > 1e-6:
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
                    title="DustRunner: exploded view (robot laid flat; dock and end stop drawn beside it)")
    concept._render(cutaway_detail(), md / "cutaway.png", azim=-90, elev=6, labels=True,
                    title="DustRunner: section across the row at the lower module edge",
                    note="Silver: module frame; blue: glass. Truck (5) wheels ride the frame top; rollers (7) bear on the frame "
                         "face and hook under its lip")
    for d in md.glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
