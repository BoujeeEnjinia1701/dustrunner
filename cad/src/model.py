"""DustRunner parametric model (build123d), TRL 3, constructable level of detail (DRN-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL and prints the constructability checks
    python cad/src/model.py --check    prints the constructability checks only
Exports into cad/step and cad/stl:
    dustrunner-robot.step / .stl       the robot (items 1 to 10 of bom/bom.csv, with its fittings)
    dustrunner-dock.step / .stl        clamp-on dock with panel, charger, contacts, latch tab and anemometer (11 to 13, 16)
    dustrunner-end-stop.step / .stl    pair of clamp-on end stops (14)
    dustrunner-assembly.step           robot parked in the dock at the start of the row, with one
                                       reference module and an end stop pair (reference module not in the BOM)

Local table coordinates (mm), used for every part:
    X = u  along the row (direction of travel, away from the dock is +X)
    Y = v  up the slope, from the lower module edge (v = 0) to the upper edge (v = mod_l)
    Z = w  normal to the glass, glass surface at w = 0, frame top at w = frame_proud
The robot is centred at u = 0. build_components() returns every made and bought component as
a Comp (name, shape, BOM line, media group); robot_parts() and dock_parts() group them the way
the calculation note and the concept media use them. The same PARAMS feed
docs/04-calcs/sizing.py (DRN-CAL-001). BUILD PLAN MODEL, PLAN NOT YET BUILT; not for fabrication.

Design for construction (DRN-DDR-003, 2026-09-30): plate gap 28 mm with clevis-mounted guide
rollers, a sprung hook slider, flange bearings, drive housings carrying the motors, beam end cleats,
hood spacers, sunshade posts, sensor and contact brackets, a robot-side latch solenoid, dock cross
members kept clear of the hook roller path, rail brackets, frame clamps, a contact post, bolted
legs, a vertical anemometer mast and three-piece end stops that sit below the IR sensors.
"""
import sys
from collections import namedtuple
from math import radians, sin, cos
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # reference module and table (DRN-REQ-001 reference row)
    "mod_l": 2278.0,          # module length up the slope (1P portrait)
    "mod_w": 1134.0,          # module width along the row
    "gap": 20.0,              # gap between modules along the row
    "lip": 25.0,              # frame top flange width seen from above (assumed; see DRN-CAL-001)
    "frame_d": 33.0,          # frame depth
    "frame_t": 2.5,           # frame wall (massing)
    "frame_proud": 1.0,       # frame top above the glass surface
    "tilt": 25.0,             # table tilt
    "h0": 600.0,              # lower glass edge above ground
    # chassis beam: 40 x 80 x 2 mm 6063 aluminum rectangular tube, long side normal to the glass
    "beam_b": 40.0, "beam_h": 80.0, "beam_t": 2.0,
    # microfiber brush
    "brush_d": 120.0,         # sleeve outside diameter
    "core_d": 50.0, "core_t": 2.0,   # aluminum core tube (50 mm keeps the interference in band, DRN-CAL-001 B5)
    "shaft_d": 20.0,          # stub shafts in the flange bearings (15 mm outboard of the lower bearing)
    "plug_l": 20.0,           # turned end plug inside each end of the core
    "brush_edge": 40.0,       # brushed band starts this far from each module edge
    "interference": 4.5,      # nominal pile interference at the bearings (R3: 3 to 5 mm along the sleeve)
    # hood (bent aluminum sheet over the brush, with end guards), hung from the beam on 3 mm spacers
    "hood_r": 76.0, "hood_t": 0.8, "hood_clear": 25.0,   # hood lower edges this far above the brush axis
    # end trucks
    "plate_t": 5.0,           # 5 mm aluminum plate
    "plate_half_u": 130.0,    # plate 260 mm along the row
    "plate_w": (-80.0, 216.0),  # plate extent normal to the glass (below the hook spring seat to the beam top)
    "plate_gap": 28.0,        # plate inner face this far outboard of the frame outer face (room for the guide clevises)
    "housing_d": 40.0,        # drive housing depth outboard of the plate (bearings, pulleys, belts, coupling)
    "wheel_d": 70.0, "wheel_w": 18.0,     # polyurethane wheels on the frame top flange
    "wheel_u": 90.0,          # wheel centers at +/- this along the row (wheelbase 180 mm)
    "wheel_v": (3.0, 21.0),   # wheel tread on the frame flange, from the frame outer face
    "axle_d": 10.0,           # wheel axles in two 2-bolt flange bearings each
    "guide_d": 22.0, "guide_u": 60.0,     # guide rollers on the frame outer face, each in a clevis
    "hook_d": 16.0, "hook_v": (3.0, 21.0),  # hook roller under the frame bottom flange
    "hook_axle_d": 8.0,       # hook roller axle, cantilevered from the slider
    # drives
    "drive_d": 37.0, "drive_l": 66.0,     # 37 mm gearmotor with encoder
    "brush_motor": (70.0, 66.0, 70.0),    # brush gearmotor envelope (u, v, w)
    # enclosures on the beam
    "pack": (65.0, 151.0, 94.0),          # 12.8 V 10 Ah LiFePO4 (u, v, w), common 151 x 65 x 94 mm case
    "pack_v": 250.0,                      # pack lower end from the lower module edge
    "ebox": (80.0, 140.0, 55.0),          # IP65 controller box
    "ebox_v": 480.0,
    "shade_t": 1.0,                       # sunshade over pack and controller
    "shade_gap": 6.0,                     # air gap between the pack top and the sunshade
    # dock (continues the frame profile past the row start)
    "dock_rail_l": 780.0,                 # parking rails
    "dock_u0": -1300.0,                   # far end of the dock (panel bay)
    "cross": 40.0,                        # dock cross members and legs, 40 x 40 x 2 square tube
    "cross_top": -38.0,                   # top of the dock cross members (6 mm below the frame bottom)
    "panel": (350.0, 530.0, 25.0),        # 20 W panel (u, v, w)
    "mast_h": 560.0,                      # vertical anemometer mast length
    # end stop
    "stop_l": 40.0, "stop_h": 39.0,       # stop block top 40 mm above the glass, below the IR sensors
    "buffer_t": 5.0,
}

P = PARAMS
Comp = namedtuple("Comp", "name shape bom group")


def derived(p=PARAMS):
    """Dimensions the calculation note and drawing use, computed from PARAMS."""
    d = {}
    d["glass_v"] = (p["lip"], p["mod_l"] - p["lip"])
    d["glass_across"] = p["mod_l"] - 2 * p["lip"]
    d["brush_v"] = (p["brush_edge"], p["mod_l"] - p["brush_edge"])
    d["brush_len"] = d["brush_v"][1] - d["brush_v"][0]
    d["brush_w"] = p["brush_d"] / 2 - p["interference"]       # brush axis height above the glass
    d["wheel_c"] = p["frame_proud"] + p["wheel_d"] / 2        # wheel axle height
    d["hook_c"] = p["frame_proud"] - p["frame_d"] - p["hook_d"] / 2
    d["hood_top"] = d["brush_w"] + p["hood_r"] + p["hood_t"]
    d["beam_w"] = (d["hood_top"] + 3.0, d["hood_top"] + 3.0 + p["beam_h"])
    d["plate_v"] = (-p["plate_gap"] - p["plate_t"], -p["plate_gap"])
    d["span"] = p["mod_l"] + 2 * p["plate_gap"]                # between plate inner faces
    d["beam_len"] = d["span"]
    d["housing_v"] = (d["plate_v"][0] - p["housing_d"], d["plate_v"][0])
    d["overall_v"] = p["mod_l"] + 2 * (p["plate_gap"] + p["plate_t"] + p["housing_d"] + p["drive_l"])
    d["overall_u"] = 2 * p["plate_half_u"] + 2 * 22.0        # plate plus IR sensors
    d["contact_w"] = 2 * ((p["brush_d"] / 2) ** 2 - d["brush_w"] ** 2) ** 0.5   # brush contact width on the glass
    d["shade_w"] = d["beam_w"][1] + p["pack"][2] + p["shade_gap"]
    d["top_w"] = d["shade_w"] + p["shade_t"]
    d["frame_bot"] = p["frame_proud"] - p["frame_d"]
    d["rail_u"] = (-p["gap"] - p["dock_rail_l"], -p["gap"])
    d["cross_u"] = (p["dock_u0"], d["rail_u"][0], -p["gap"] - 100.0)   # far, rail-start and near cross members (-u face)
    return d


# ---------------- helpers ----------------
def bx(u0, u1, v0, v1, w0, w1):
    from build123d import Box, Pos
    return Pos((u0 + u1) / 2, (v0 + v1) / 2, (w0 + w1) / 2) * Box(abs(u1 - u0), abs(v1 - v0), abs(w1 - w0))


def cyl_u(v, w, u0, u1, r):
    from build123d import Cylinder, Pos, Rot
    return Pos((u0 + u1) / 2, v, w) * Rot(0, 90, 0) * Cylinder(r, abs(u1 - u0))


def cyl_v(u, w, v0, v1, r):
    from build123d import Cylinder, Pos, Rot
    return Pos(u, (v0 + v1) / 2, w) * Rot(90, 0, 0) * Cylinder(r, abs(v1 - v0))


def cyl_w(u, v, w0, w1, r):
    from build123d import Cylinder, Pos
    return Pos(u, v, (w0 + w1) / 2) * Cylinder(r, abs(w1 - w0))


def ring_v(u, w, v0, v1, r_out, r_in):
    return cyl_v(u, w, v0, v1, r_out) - cyl_v(u, w, v0 - 1, v1 + 1, r_in)


def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def mirror_v(shape, p=PARAMS):
    """Mirror a lower-end shape to the upper module edge (v -> mod_l - v)."""
    from build123d import Plane, Pos
    return Pos(0, p["mod_l"], 0) * shape.mirror(Plane.XZ)


def to_world(shape, p=PARAMS):
    """Local (u, v, w) table coordinates to world (Z up, ground at Z = 0), as in concept_media.py."""
    from build123d import Pos, Rot
    return Pos(0, 0, p["h0"]) * Rot(0, 0, 90) * Rot(p["tilt"], 0, 0) * shape


def to_local(shape, p=PARAMS):
    from build123d import Pos, Rot
    return Rot(-p["tilt"], 0, 0) * Rot(0, 0, -90) * Pos(0, 0, -p["h0"]) * shape


def local_point_to_world(u, v, w, p=PARAMS):
    t = radians(p["tilt"])
    return (-(v * cos(t) - w * sin(t)), u, p["h0"] + v * sin(t) + w * cos(t))


def frame_edge(u0, u1, p=PARAMS):
    """Module frame profile at the lower edge (C section open toward the glass): top flange,
    outer web and bottom flange. Used for the reference module and the dock rails."""
    top = p["frame_proud"]; bot = top - p["frame_d"]; t = p["frame_t"]
    return (bx(u0, u1, 0, p["lip"], top - t, top) + bx(u0, u1, 0, t, bot, top)
            + bx(u0, u1, 0, p["lip"], bot, bot + t))


def frame_end(u0, sign, p=PARAMS):
    """Module frame along a long side (u end), C section open toward the glass (+u for sign=+1)."""
    top = p["frame_proud"]; bot = top - p["frame_d"]; t = p["frame_t"]; L = p["mod_l"]
    a, b = (u0, u0 + sign * p["lip"])
    a, b = min(a, b), max(a, b)
    wa, wb = (u0, u0 + sign * t)
    wa, wb = min(wa, wb), max(wa, wb)
    return bx(a, b, 0, L, top - t, top) + bx(wa, wb, 0, L, bot, top) + bx(a, b, 0, L, bot, bot + t)


# ---------------- robot ----------------
def _truck(p, lower=True):
    """One end truck at the lower module edge (the upper truck is its mirror image); lower=True
    adds the brush drive, the dock contact bracket and the latch solenoid."""
    d = derived(p)
    pv0, pv1 = d["plate_v"]
    hv0, hv1 = d["housing_v"]
    hu = p["plate_half_u"]; wc = d["wheel_c"]; wr = p["wheel_d"] / 2; bw = d["brush_w"]
    wu = p["wheel_u"]
    c = {}
    # plate with holes for the axles, the lower brush shaft and the stop button
    plate = bx(-hu, hu, pv0, pv1, *p["plate_w"])
    for su in (-1, 1):
        plate -= cyl_v(su * wu, wc, pv0 - 1, pv1 + 1, p["axle_d"] / 2 + 1)
    if lower:
        plate -= cyl_v(0, bw, pv0 - 1, pv1 + 1, 11)
    plate -= cyl_v(95, 185, pv0 - 1, pv1 + 1, 11)
    for su in (-1, 1):
        plate -= cyl_v(su * 13, -40, pv0 - 1, pv1 + 1, 3.25)                 # hook slider shoulder bolts
        for wz in (25.0, 55.0):
            plate -= cyl_v(su * 37, d["beam_w"][0] + wz, pv0 - 1, pv1 + 1, 3.25)   # beam cleat bolts
    c["plate"] = plate
    # wheels, axles, two 2-bolt flange bearings per axle (one each side of the plate), pulleys and belt
    wheels = axles = bearings = pulleys = None
    for su in (-1, 1):
        u = su * wu
        wheels = fuse([wheels, ring_v(u, wc, *p["wheel_v"], wr, p["axle_d"] / 2)])
        axles = fuse([axles, cyl_v(u, wc, hv0 + 16, p["wheel_v"][1], p["axle_d"] / 2)])
        for v0, v1, h0, h1 in ((pv1, pv1 + 7, pv1 + 7, pv1 + 12), (pv0 - 7, pv0, pv0 - 12, pv0 - 7)):
            bearings = fuse([bearings, bx(u - 18, u + 18, v0, v1, wc - 30, wc + 30) - cyl_v(u, wc, v0 - 1, v1 + 1, p["axle_d"] / 2),
                             ring_v(u, wc, h0, h1, 14, p["axle_d"] / 2)])
        pulleys = fuse([pulleys, ring_v(u, wc, hv0 + 16, hv0 + 26, 8, p["axle_d"] / 2)])
    belt = (bx(-wu, wu, hv0 + 16.5, hv0 + 25.5, wc - 9.5, wc + 9.5) + cyl_v(-wu, wc, hv0 + 16.5, hv0 + 25.5, 9.5)
            + cyl_v(wu, wc, hv0 + 16.5, hv0 + 25.5, 9.5)) - (bx(-wu, wu, hv0 + 16, hv0 + 26, wc - 8, wc + 8)
                                                           + cyl_v(-wu, wc, hv0 + 16, hv0 + 26, 8) + cyl_v(wu, wc, hv0 + 16, hv0 + 26, 8))
    c["wheels"] = wheels
    c["axles"] = axles + pulleys + belt
    c["axle_bearings"] = bearings
    # coupling from the drive motor shaft to the +u axle, inside the housing
    c["coupling"] = cyl_v(wu, wc, hv0 + 3, hv0 + 15, 8)
    # drive housing: 3 mm folded tray screwed to the plate's outer face by side flanges; the motors bolt to its outer wall
    htop = 160.0 if lower else 74.0
    hb = -5.0
    ht = 2.0 if lower else 1.5                                               # 2 mm sheet where the brush motor hangs
    housing = bx(-118, 118, hv0, pv0, hb, htop) - bx(-118 + ht, 118 - ht, hv0 + ht, pv0 + 1, hb + ht, htop - ht)
    housing -= cyl_v(wu, wc, hv0 - 1, hv0 + 4, 4)                           # motor shaft hole
    if lower:
        housing -= cyl_v(0, 117, hv0 - 1, hv0 + 4, 5)                      # brush motor shaft hole
    flanges = bx(118, 130, pv0 - 3, pv0, hb, htop) + bx(-130, -118, pv0 - 3, pv0, hb, htop)
    c["housing"] = housing + flanges
    # drive gearmotor, face-mounted on the housing's outer wall, coaxial with the +u axle
    c["drive_motor"] = cyl_v(wu, wc, hv0 - p["drive_l"], hv0, p["drive_d"] / 2) + cyl_v(wu, wc, hv0, hv0 + 4, 3)
    # guide rollers, each on an M8 bolt in a folded 3 mm clevis screwed to the plate's inner face
    gr = p["guide_d"] / 2
    guides = clevis = None
    for su in (-1, 1):
        u = su * p["guide_u"]
        guides = fuse([guides, cyl_w(u, -gr, -27, -4, gr) - cyl_w(u, -gr, -28, -3, 4)])
        clevis = fuse([clevis, bx(u - 11, u + 11, pv1, pv1 + 3, -30, -1), bx(u - 11, u + 11, pv1 + 3, -5, -30, -27),
                       bx(u - 11, u + 11, pv1 + 3, -5, -4, -1)]) - cyl_w(u, -gr, -31, 0, 4.25)
    c["guide_rollers"] = guides
    c["guide_clevises"] = clevis
    # hook roller on an 8 mm axle cantilevered from a 10 mm slider; slider rides on two shoulder bolts
    # in the plate and is pushed up by a compression spring on a seat bracket (70 N preload)
    hc = d["hook_c"]; hr = p["hook_d"] / 2
    c["hook_roller"] = ring_v(0, hc, *p["hook_v"], hr, p["hook_axle_d"] / 2)
    c["hook_axle"] = cyl_v(0, hc, pv1 + 10, p["hook_v"][1] + 2, p["hook_axle_d"] / 2)
    c["hook_slider"] = (bx(-20, 20, pv1, pv1 + 10, -55, -25) - cyl_v(0, hc, pv1 - 1, pv1 + 11, p["hook_axle_d"] / 2)
                        - bx(-16.25, -9.75, pv1 - 1, pv1 + 11, -47, -33) - bx(9.75, 16.25, pv1 - 1, pv1 + 11, -47, -33))
    c["hook_spring"] = cyl_w(0, pv1 + 5, -75, -55, 4.5) - cyl_w(0, pv1 + 5, -76, -54, 3)
    c["spring_seat"] = bx(-15, 15, pv1, pv1 + 3, -80, -62) + bx(-15, 15, pv1 + 3, pv1 + 12, -78, -75)
    # brush flange bearing on the plate's inner face (both trucks)
    c["brush_bearing"] = (bx(-30, 30, pv1, pv1 + 8, bw - 45, bw + 45) + cyl_v(0, bw, pv1 + 8, pv1 + 22, 20)
                          - cyl_v(0, bw, pv1 - 1, pv1 + 23, p["shaft_d"] / 2))
    # beam end cleats: 40 x 40 x 4 angle each side of the beam, through-bolted across it and bolted to the plate
    bw0, bw1 = d["beam_w"]
    b2 = p["beam_b"] / 2
    cl = None
    for su in (-1, 1):
        a0, a1 = sorted((su * b2, su * (b2 + 3)))
        c0, c1 = sorted((su * b2, su * (b2 + 30)))
        cl = fuse([cl, bx(a0, a1, pv1 + 3, pv1 + 30, bw0 + 5, bw0 + 75), bx(c0, c1, pv1, pv1 + 3, bw0 + 5, bw0 + 75)])
    holes = (cyl_u(pv1 + 17, bw0 + 25, -b2 - 10, b2 + 10, 3.25) + cyl_u(pv1 + 17, bw0 + 55, -b2 - 10, b2 + 10, 3.25)
             + fuse([cyl_v(su * 37, bw0 + wz, pv1 - 1, pv1 + 4, 3.25) for su in (-1, 1) for wz in (25.0, 55.0)]))
    c["cleats"] = cl - holes
    c["beam_holes"] = cyl_u(pv1 + 17, bw0 + 25, -b2 - 1, b2 + 1, 3.25) + cyl_u(pv1 + 17, bw0 + 55, -b2 - 1, b2 + 1, 3.25)
    c["cleat_bolts"] = (cyl_u(pv1 + 17, bw0 + 25, -b2 - 9, b2 + 9, 3) + cyl_u(pv1 + 17, bw0 + 55, -b2 - 9, b2 + 9, 3)
                        + cyl_v(37, bw0 + 25, pv0 - 4, pv1 + 4, 3) + cyl_v(-37, bw0 + 25, pv0 - 4, pv1 + 4, 3)
                        + cyl_v(37, bw0 + 55, pv0 - 4, pv1 + 4, 3) + cyl_v(-37, bw0 + 55, pv0 - 4, pv1 + 4, 3))
    # IR edge sensors, two per truck, on folded 3 mm brackets screwed to the plate's inner face
    sens = brk = None
    for su in (-1, 1):
        s0, s1 = sorted((su * hu, su * (hu + 22)))
        k0, k1 = sorted((su * 112, su * 130))
        h0, h1 = sorted((su * 112, su * (hu + 22)))
        sens = fuse([sens, bx(s0, s1, p["wheel_v"][0], p["wheel_v"][1], 45, 78)])
        brk = fuse([brk, bx(k0, k1, pv1, pv1 + 3, 55, 78), bx(h0, h1, pv1, p["wheel_v"][1], 78, 81)])
    c["sensors"] = sens
    c["sensor_brackets"] = brk
    # emergency stop button through a 22 mm hole in the plate
    c["estop"] = cyl_v(95, 185, pv0 - 40, pv0, 20) + cyl_v(95, 185, pv1, pv1 + 30, 15)
    if lower:
        # brush stub shaft, flange bearing outboard side, pulleys, belt and brush gearmotor
        mu, mv, mw = p["brush_motor"]
        mz = 117.0
        c["brush_pulleys"] = (ring_v(0, bw, hv0 + 4, hv0 + 14, 12, 7.5) + ring_v(0, mz, hv0 + 4, hv0 + 14, 12, 3))
        c["brush_belt"] = ((bx(-13.5, 13.5, hv0 + 4.5, hv0 + 13.5, bw, mz) + cyl_v(0, bw, hv0 + 4.5, hv0 + 13.5, 13.5)
                            + cyl_v(0, mz, hv0 + 4.5, hv0 + 13.5, 13.5))
                           - (bx(-12, 12, hv0 + 4, hv0 + 14, bw, mz) + cyl_v(0, bw, hv0 + 4, hv0 + 14, 12) + cyl_v(0, mz, hv0 + 4, hv0 + 14, 12)))
        c["brush_motor"] = bx(-mu / 2, mu / 2, hv0 - mv, hv0, mz - mw / 2, mz + mw / 2) + cyl_v(0, mz, hv0, hv0 + 14, 3)
        # robot-side dock contacts: insulating block with three copper strips on a folded bracket,
        # and the latch: a 12 V pull solenoid whose spring-out 6 mm pin drops into the dock latch tab
        c["contact_bracket"] = (bx(-127, -100, pv1, pv1 + 3, 88, 150) + bx(-130, -127, pv1, 18, 88, 126)
                                + bx(-127, -100, pv1 + 3, 5, 147, 150)) - cyl_w(-115, -8, 146, 151, 3.5)
        c["contact_pad"] = bx(-138, -130, pv1 + 1, 18, 90, 126)
        c["solenoid"] = cyl_w(-115, -8, 150, 180, 12) + cyl_w(-115, -8, 124, 150, 3)
    return c


def _brush_and_hood(p):
    d = derived(p)
    pv0, pv1 = d["plate_v"]; hv0 = d["housing_v"][0]
    L = p["mod_l"]; bw = d["brush_w"]; v0, v1 = d["brush_v"]
    rc = p["core_d"] / 2; ri = rc - p["core_t"]
    c = {}
    c["sleeve"] = ring_v(0, bw, v0, v1, p["brush_d"] / 2, rc)
    c["core"] = ring_v(0, bw, v0 - 10, v1 + 10, rc, ri)
    c["plugs"] = (ring_v(0, bw, v0 - 10, v0 - 10 + p["plug_l"], ri, p["shaft_d"] / 2)
                  + ring_v(0, bw, v1 + 10 - p["plug_l"], v1 + 10, ri, p["shaft_d"] / 2))
    lower = cyl_v(0, bw, pv0, v0 - 10 + p["plug_l"], p["shaft_d"] / 2) + cyl_v(0, bw, hv0 + 3, pv0, 7.5)
    upper = cyl_v(0, bw, v1 + 10 - p["plug_l"], L - pv1 - 2, p["shaft_d"] / 2)
    c["shafts"] = lower + upper
    # hood: part of a ring above the brush, with end guards
    r0, r1 = p["hood_r"], p["hood_r"] + p["hood_t"]
    ring = ring_v(0, bw, v0 - 5, v1 + 5, r1, r0)
    hood = ring & bx(-r1 - 1, r1 + 1, v0 - 6, v1 + 6, bw + p["hood_clear"], bw + r1 + 1)
    guard = (cyl_v(0, bw, v0 - 6, v0 - 5, r1) & bx(-r1, r1, v0 - 7, v0 - 4, bw + p["hood_clear"], bw + r1))
    c["hood"] = hood + guard + mirror_v(guard, p)
    # sunshade over pack and controller, on four 12 mm spacer posts screwed into the beam's top wall
    bw1 = d["beam_w"][1]; sw = d["shade_w"]
    sv0, sv1 = p["pack_v"] - 20, p["ebox_v"] + p["ebox"][1] + 20
    c["shade"] = bx(-60, 60, sv0, sv1, sw, sw + p["shade_t"])
    c["shade_posts"] = fuse([cyl_w(su * 12, vv, bw1, sw, 6) - cyl_w(su * 12, vv, bw1 - 1, sw + 1, 3)
                             for su in (-1, 1) for vv in (sv0 + 8, sv1 - 8)])
    # hood spacers: 3 mm nylon spacers on M5 screws into rivet nuts in the beam's lower wall
    hs = d["hood_top"]
    c["hood_spacers"] = fuse([cyl_w(0, vv, hs, d["beam_w"][0], 6) for vv in (300.0, 760.0, L / 2, L - 760.0, L - 300.0)])
    return c


def build_components(p=PARAMS):
    """Every robot, dock and end-stop component as a Comp, keyed by a short name, in local
    coordinates with the robot centred at u = 0 and the end stops at the end of the reference module."""
    d = derived(p)
    L = p["mod_l"]
    C = {}
    lo = _truck(p, lower=True)
    hi_src = _truck(p, lower=False)
    hi = {k: mirror_v(v, p) for k, v in hi_src.items()}
    bh = _brush_and_hood(p)
    # 1 beam
    b, h, t = p["beam_b"], p["beam_h"], p["beam_t"]
    pv0, pv1 = d["plate_v"]
    w0, w1 = d["beam_w"]
    beam = bx(-b / 2, b / 2, pv1, L - pv1, w0, w1) - bx(-b / 2 + t, b / 2 - t, pv1 - 1, L - pv1 + 1, w0 + t, w1 - t)
    beam = beam - lo["beam_holes"] - mirror_v(hi_src["beam_holes"], p)
    C["beam"] = Comp("Chassis beam", beam, 1, "beam")
    C["sleeve"] = Comp("Microfiber sleeve", bh["sleeve"], 2, "brush")
    C["core"] = Comp("Brush core tube", bh["core"], 2, "brush")
    C["plugs"] = Comp("Core end plugs (2)", bh["plugs"], 2, "brush")
    C["shafts"] = Comp("Brush stub shafts (2)", bh["shafts"], 2, "brush")
    C["brush_bearings"] = Comp("Brush flange bearings (2)", lo["brush_bearing"] + hi["brush_bearing"], 2, "brush")
    C["hood"] = Comp("Brush hood", bh["hood"], 3, "hood")
    C["shade"] = Comp("Sunshade", bh["shade"], 3, "hood")
    C["brush_motor"] = Comp("Brush gearmotor", lo["brush_motor"], 4, "brush_motor")
    C["brush_drive"] = Comp("Brush pulleys and belt", lo["brush_pulleys"] + lo["brush_belt"], 4, "brush_motor")
    for side, src in (("lo", lo), ("hi", hi)):
        nm = "lower" if side == "lo" else "upper"
        C[f"plate_{side}"] = Comp(f"Truck plate ({nm})", src["plate"], 5, "trucks")
        C[f"wheels_{side}"] = Comp(f"Wheels ({nm})", src["wheels"], 5, "trucks")
        C[f"axles_{side}"] = Comp(f"Axles, pulleys and belt ({nm})", src["axles"] + src["coupling"], 5, "trucks")
        C[f"axle_bearings_{side}"] = Comp(f"Axle flange bearings ({nm})", src["axle_bearings"], 5, "trucks")
        C[f"housing_{side}"] = Comp(f"Drive housing ({nm})", src["housing"], 5, "trucks")
        C[f"drive_{side}"] = Comp(f"Drive gearmotor ({nm})", src["drive_motor"], 6, "drive_motors")
        C[f"guides_{side}"] = Comp(f"Guide rollers ({nm})", src["guide_rollers"], 7, "rollers")
        C[f"clevises_{side}"] = Comp(f"Guide roller clevises ({nm})", src["guide_clevises"], 7, "rollers")
        C[f"hook_{side}"] = Comp(f"Hook roller and axle ({nm})", src["hook_roller"] + src["hook_axle"], 7, "rollers")
        C[f"slider_{side}"] = Comp(f"Hook slider ({nm})", src["hook_slider"], 7, "rollers")
        C[f"spring_{side}"] = Comp(f"Hook spring and seat ({nm})", src["hook_spring"] + src["spring_seat"], 7, "rollers")
        C[f"sensors_{side}"] = Comp(f"IR edge sensors ({nm})", src["sensors"], 10, "sensors")
        C[f"sensor_brackets_{side}"] = Comp(f"Sensor brackets ({nm})", src["sensor_brackets"], 10, "sensors")
        C[f"cleats_{side}"] = Comp(f"Beam end cleats ({nm})", src["cleats"], 15, "fittings")
        C[f"cleat_bolts_{side}"] = Comp(f"Beam cleat bolts ({nm})", src["cleat_bolts"], 15, "fittings")
        C[f"estop_{side}"] = Comp(f"Stop button ({nm})", src["estop"], 15, "fittings")
    C["contact_bracket"] = Comp("Contact bracket", lo["contact_bracket"], 13, "trucks")
    C["contact_pad"] = Comp("Robot contact block", lo["contact_pad"], 13, "trucks")
    C["solenoid"] = Comp("Latch solenoid and pin", lo["solenoid"], 13, "trucks")
    C["hood_spacers"] = Comp("Hood spacers", bh["hood_spacers"], 15, "fittings")
    C["shade_posts"] = Comp("Sunshade posts", bh["shade_posts"], 15, "fittings")
    # 8 pack and 9 controller on top of the beam, lower end; pack held by two straps round the beam
    pu, pvl, pw = p["pack"]
    C["battery"] = Comp("LiFePO4 pack", bx(-pu / 2, pu / 2, p["pack_v"], p["pack_v"] + pvl, w1, w1 + pw), 8, "battery")
    straps = None
    for vv in (p["pack_v"] + 30, p["pack_v"] + pvl - 50):
        straps = fuse([straps, bx(-pu / 2 - 2, pu / 2 + 2, vv, vv + 20, w0 - 2, w1 + pw + 2)
                       - bx(-pu / 2, pu / 2, vv - 1, vv + 21, w0, w1 + pw)])
    C["straps"] = Comp("Pack straps (2)", straps, 15, "fittings")
    eu, evl, ew = p["ebox"]
    C["controller"] = Comp("Controller box", bx(-eu / 2, eu / 2, p["ebox_v"], p["ebox_v"] + evl, w1, w1 + ew), 9, "controller")
    C.update(_dock(p))
    C.update(_stops(p.get("_u_stop", p["mod_w"]), p))
    return C


def _dock(p):
    d = derived(p)
    L = p["mod_l"]; bot = d["frame_bot"]; cs = p["cross"]; ct = p["cross_top"]
    ur0, ur1 = d["rail_u"]
    uf, ur, un = d["cross_u"]
    C = {}
    C["rails"] = Comp("Dock rails (2)", frame_edge(ur0, ur1, p) + mirror_v(frame_edge(ur0, ur1, p), p), 11, "dock")
    cross = fuse([bx(uc, uc + cs, 30, L - 30, ct - cs, ct) - bx(uc + 2, uc + cs - 2, 29, L - 29, ct - cs + 2, ct - 2)
                  for uc in (uf, ur, un)])
    C["cross"] = Comp("Cross members (3)", cross, 11, "dock")
    # rail brackets: 4 mm L bracket inside the rail channel, screwed through the web, bolted down
    # through a spacer (or the clamp bar and a shim) to the cross member
    rb = sp = None
    for uc in (ur, un):
        one = bx(uc, uc + cs, 2.5, 70, bot + 2.5, bot + 6.5) + bx(uc, uc + cs, 2.5, 6.5, bot + 6.5, -4.5)
        rb = fuse([rb, one, mirror_v(one, p)])
        if uc == ur:
            s = bx(uc, uc + cs, 30, 70, ct, bot + 2.5)
        else:
            s = bx(uc, uc + cs, 30, 70, bot, bot + 2.5)
        sp = fuse([sp, s, mirror_v(s, p)])
    C["rail_brackets"] = Comp("Rail brackets (4)", rb, 11, "dock")
    C["spacers"] = Comp("Spacers and shims", sp, 11, "dock")
    # frame clamps to the first module's long-side frame: clamp bar under the bottom flange, jaw on top of
    # it inside the frame, 2.5 mm spacer beside the flange edge, one M8 bolt
    clamp = jaw = None
    for vv in (30.0,):
        bar = bx(un, 45, vv, vv + 40, ct, bot)
        j = bx(5, 45, vv, vv + 40, bot + 2.5, bot + 8.5) + bx(30, 45, vv, vv + 40, bot, bot + 2.5)
        clamp = fuse([clamp, bar, mirror_v(bar, p)])
        jaw = fuse([jaw, j, mirror_v(j, p)])
    C["clamp_bars"] = Comp("Clamp bars (2)", clamp, 11, "dock")
    C["clamp_jaws"] = Comp("Clamp jaws and spacers (2)", jaw, 11, "dock")
    bolts = None
    for vv in (50.0,):
        for bolt in (cyl_w(37.5, vv, ct - 6, bot + 14, 4),                    # frame clamp
                     cyl_w(un + cs / 2, vv, ct - cs - 6, bot + 12.5, 4),      # near rail bracket stack
                     cyl_w(ur + cs / 2, vv, ct - cs - 6, bot + 12.5, 4)):     # rail-start rail bracket stack
            bolts = fuse([bolts, bolt, mirror_v(bolt, p)])
    C["dock_bolts"] = Comp("Dock bolts", bolts, 11, "dock")
    holes = None
    for vv in (50.0,):
        for hx in (37.5, un + cs / 2, ur + cs / 2):
            hcyl = cyl_w(hx, vv, ct - cs - 10, bot + 20, 4.25)
            holes = fuse([holes, hcyl, mirror_v(hcyl, p)])
    for k in ("cross", "rail_brackets", "spacers", "clamp_bars", "clamp_jaws"):
        C[k] = C[k]._replace(shape=C[k].shape - holes)
    # ties on top of the far and rail-start cross members; the panel bolts to the first two
    ties = fuse([bx(uf, ur + cs, vv, vv + 40, ct, ct + 20) - bx(uf - 1, ur + cs + 1, vv + 2, vv + 38, ct + 2, ct + 18)
                 for vv in (110.0, 610.0, L - 130.0)])
    C["ties"] = Comp("Ties (3)", ties, 11, "dock")
    # legs: vertical 40 x 40 square tube bolted to the -u side of the far and rail-start cross members, foot plates
    from build123d import Box, Pos
    legs = feet = None
    for uc in (uf, ur):
        for vc in (300.0, L - 330.0):
            x, y, z = local_point_to_world(uc - cs / 2, vc, ct - cs / 2, p)
            tall = z + 200
            leg_w = Pos(x, y, (tall + 6) / 2) * Box(cs, cs, tall - 6)          # stands on its 6 mm foot plate
            leg_l = to_local(leg_w, p) & bx(uc - cs, uc, -2000, 3000, -3000, ct)
            leg_l -= to_local(Pos(x, y, (tall + 6) / 2) * Box(cs - 4, cs - 4, tall + 10), p)
            legs = fuse([legs, leg_l])
            feet = fuse([feet, to_local(Pos(x, y, 3) * Box(100, 100, 6), p)])
    C["legs"] = Comp("Legs (4) and foot plates", legs + feet, 11, "dock")
    # panel on the ties
    pu, pvl, pw = p["panel"]
    pc = (uf + cs + ur) / 2
    C["panel"] = Comp("Dock PV panel", bx(pc - pu / 2, pc + pu / 2, 120, 120 + pvl, ct + 20, ct + 20 + pw), 12, "panel")
    # charger box on the far cross member's +u face; contact post on the rail-start cross member's +u
    # face; dock contact block on the post; latch tab on the block
    C["charger"] = Comp("Dock charger box", bx(uf + cs, uf + cs + 120, 760, 880, ct - cs - 14, ct + 26), 13, "charge")
    C["contact_post"] = Comp("Contact post", bx(ur + cs, ur + cs + 20, 40, 80, ct - cs, 128)
                             - bx(ur + cs + 2, ur + cs + 18, 42, 78, ct - cs - 1, 129), 13, "charge")
    C["dock_contacts"] = Comp("Dock contact block", bx(ur + cs, ur + cs + 20, -37, 40, 90, 128), 13, "charge")
    C["latch_tab"] = Comp("Latch tab", bx(ur + cs, ur + cs + 65, -20, 10, 128, 134) - cyl_w(ur + cs + 45, -8, 127, 135, 3.5), 13, "charge")
    # anemometer: vertical mast in two U-bolt clamps on the far cross member's -u face
    t = radians(p["tilt"])
    mv = L - 200
    base = (uf - 12, mv, ct - cs)
    up = (0.0, sin(t), cos(t))
    top = tuple(base[i] + p["mast_h"] * up[i] for i in range(3))
    mast = tube(base, top, 12.0)
    cups = tube(top, tuple(top[i] + 40 * up[i] for i in range(3)), 60.0)
    clamps = None
    for s in (8.0, 32.0):
        a = tuple(base[i] + s * up[i] for i in range(3))
        b_ = tuple(base[i] + (s + 8) * up[i] for i in range(3))
        r = tube(a, b_, 15.0) - tube(a, b_, 12.0)
        clamps = fuse([clamps, r & bx(uf - 40, uf, -1000, 4000, -1000, 1000)])
    C["anemometer"] = Comp("Anemometer and mast", mast + cups, 16, "anemometer")
    C["mast_clamps"] = Comp("Mast clamps (2)", clamps, 16, "anemometer")
    return C


def _stops(u_end, p):
    """Clamp-on end stop pair at the far end of the row: top block on the frame top flange, outer
    plate down the frame's outer face, bottom jaw under its bottom flange, an M8 clamp screw up
    through the jaw, and a rubber buffer facing the robot."""
    top = p["frame_proud"]; bot = top - p["frame_d"]; sl = p["stop_l"]
    blk = bx(u_end - sl, u_end, 0, p["lip"], top, top + p["stop_h"])
    plate = bx(u_end - sl, u_end, -12, 0, bot - 14, top + p["stop_h"])
    jaw = bx(u_end - sl, u_end, 0, p["lip"], bot - 14, bot - 2)
    screw = cyl_w(u_end - sl / 2, 12.5, bot - 24, bot, 4)
    buf = bx(u_end - sl - p["buffer_t"], u_end - sl, 0, p["lip"], top + 4, top + p["stop_h"] - 2)
    C = {}
    C["stop_blocks"] = Comp("End stop blocks", blk + plate + jaw + mirror_v(blk + plate + jaw, p), 14, "stop")
    C["stop_screws"] = Comp("End stop clamp screws", screw + mirror_v(screw, p), 14, "stop")
    C["stop_buffers"] = Comp("End stop buffers", buf + mirror_v(buf, p), 14, "stop")
    return C


ROBOT_GROUPS = ["beam", "brush", "hood", "brush_motor", "trucks", "drive_motors", "rollers",
                "battery", "controller", "sensors", "fittings"]
ROBOT_KEYS = ROBOT_GROUPS


def _robot_comps(C):
    return {k: c for k, c in C.items() if c.group in ROBOT_GROUPS}


def robot_parts(p=PARAMS):
    """Robot parts grouped by BOM line, local coordinates, centred at u = 0. Keys match the BOM
    mapping in cad/src/concept_media.py; *_lo and *_hi are the lower and upper halves of paired items."""
    C = build_components(p)
    R = _robot_comps(C)
    out = {}
    for g in ROBOT_GROUPS:
        out[g] = fuse([c.shape for c in R.values() if c.group == g])
    for g in ("trucks", "drive_motors", "rollers", "sensors"):
        for side in ("lo", "hi"):
            out[f"{g}_{side}"] = fuse([c.shape for k, c in R.items() if c.group == g and k.endswith("_" + side)]
                                      + ([C["contact_bracket"].shape, C["contact_pad"].shape, C["solenoid"].shape]
                                         if (g == "trucks" and side == "lo") else []))
    return out


def robot(p=PARAMS, u=0.0):
    from build123d import Compound, Pos
    rp = robot_parts(p)
    return Compound(children=[Pos(u, 0, 0) * rp[k] for k in ROBOT_GROUPS], label="DustRunner robot")


def dock_parts(p=PARAMS, legs=True):
    """Dock parts in local coordinates, grouped as the BOM lines: dock (11), panel (12),
    charge (13) and anemometer (16); legs=False leaves out the four legs (for exploded views)."""
    C = build_components(p)
    out = {}
    for g in ("dock", "panel", "charge", "anemometer"):
        out[g] = fuse([c.shape for k, c in C.items() if c.group == g and (legs or k != "legs")])
    return out


def stop_parts(u_end, p=PARAMS):
    """Clamp-on end stop pair at the far end of the row (lower and upper frame)."""
    S = _stops(u_end, p)
    return fuse([c.shape for c in S.values()])


def reference_module(u0, p=PARAMS):
    """One reference module (frame ring and glass) starting at u0. Not in the BOM."""
    from build123d import Compound
    L, W = p["mod_l"], p["mod_w"]
    edges = frame_edge(u0, u0 + W, p) + mirror_v(frame_edge(u0, u0 + W, p), p)
    ends = frame_end(u0, 1, p) + frame_end(u0 + W, -1, p)
    glass = bx(u0 + p["lip"], u0 + W - p["lip"], p["lip"], L - p["lip"], -4.0, 0.0)
    return Compound(children=[edges + ends, glass], label="Reference module (not in BOM)")


def park_u(p=PARAMS):
    """Robot centre when parked: robot contact block 2 mm short of the dock contact block."""
    return derived(p)["rail_u"][0] + p["cross"] + 20 + 2 + 138


def assembly(p=PARAMS):
    from build123d import Compound
    dp = dock_parts(p)
    u_stop = p["mod_w"]
    return Compound(children=[robot(p, park_u(p)), reference_module(0.0, p),
                              Compound(children=list(dp.values()), label="Dock"),
                              stop_parts(u_stop, p)], label="DustRunner assembly")


# ---------------- constructability checks ----------------
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _gap(a, b_):
    return a.distance_to(b_)


def checks(p=PARAMS):
    """Pairs that must touch (bolted, bearing or rolling contact) and pairs that must be apart by
    a clearance (mm). Robot checked on the reference module (at u = 560, mid-module) and parked in
    the dock; returns (description, overlap mm3, gap mm, expectation, ok)."""
    from build123d import Pos
    d = derived(p)
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    mod = reference_module(0.0, p)
    frame = mod.children[0]
    glass = mod.children[1]
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = _gap(a, b_)
        if expect == "overlap":
            ok = v > 1.0
        else:
            ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # robot on the module, mid-module
    um = 560.0
    M = lambda k: Pos(um, 0, 0) * S(k)  # noqa: E731
    for s in ("lo", "hi"):
        n = "lower" if s == "lo" else "upper"
        chk(f"Wheels ({n}) on the frame top flange", M(f"wheels_{s}"), frame, "touch")
        chk(f"Guide rollers ({n}) on the frame outer face", M(f"guides_{s}"), frame, "touch")
        chk(f"Hook roller ({n}) under the frame bottom flange", M(f"hook_{s}"), frame, "touch")
        chk(f"Truck plate ({n}) clear of the frame", M(f"plate_{s}"), frame, 20.0)
        chk(f"Guide clevises ({n}) clear of the frame", M(f"clevises_{s}"), frame, 3.0)
        chk(f"Hook slider ({n}) clear of the frame", M(f"slider_{s}"), frame, 10.0)
        chk(f"Sensors ({n}) clear of the frame", M(f"sensors_{s}"), frame, 40.0)
        chk(f"Axle bearings ({n}) clear of the frame", M(f"axle_bearings_{s}"), frame, 2.0)
        chk(f"Guide clevises ({n}) on the plate", S(f"clevises_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Guide rollers ({n}) clear of the plate", S(f"guides_{s}"), S(f"plate_{s}"), 5.0)
        chk(f"Guide rollers ({n}) between the clevis arms", S(f"guides_{s}"), S(f"clevises_{s}"), "touch")
        chk(f"Hook slider ({n}) on the plate", S(f"slider_{s}"), S(f"plate_{s}"), "touch")
        win = bx(-30, 30, p["hook_v"][0] - 0.5, 40, -60, 0)
        chk(f"Hook roller ({n}) clear of the slider", S(f"hook_{s}") & (win if s == "lo" else mirror_v(win, p)),
            S(f"slider_{s}"), 5.0)
        chk(f"Hook spring ({n}) on the slider", S(f"spring_{s}"), S(f"slider_{s}"), "touch")
        chk(f"Spring seat ({n}) on the plate", S(f"spring_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Axle bearings ({n}) on the plate", S(f"axle_bearings_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Wheels ({n}) clear of the axle bearings", S(f"wheels_{s}"), S(f"axle_bearings_{s}"), 10.0)
        chk(f"Drive housing ({n}) on the plate", S(f"housing_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Drive gearmotor ({n}) on the housing", S(f"drive_{s}"), S(f"housing_{s}"), "touch")
        chk(f"Axles and belt ({n}) clear of the housing walls", S(f"axles_{s}") & bx(-200, 200, -200, 3000, -100, 300),
            S(f"housing_{s}") & (bx(-200, 200, -200, -38, -100, 300) if s == "lo" else bx(-200, 200, p["mod_l"] + 38, 3000, -100, 300)), 0.0)
        chk(f"Beam end cleats ({n}) on the plate", S(f"cleats_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Beam end cleats ({n}) on the beam", S(f"cleats_{s}"), S("beam"), "touch")
        chk(f"Sensor brackets ({n}) on the plate", S(f"sensor_brackets_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Sensors ({n}) on their brackets", S(f"sensors_{s}"), S(f"sensor_brackets_{s}"), "touch")
        chk(f"Sensor brackets ({n}) clear of the wheels", S(f"sensor_brackets_{s}"), S(f"wheels_{s}"), 5.0)
        chk(f"Sensor brackets ({n}) clear of the axle bearings", S(f"sensor_brackets_{s}"), S(f"axle_bearings_{s}"), 2.0)
        chk(f"Stop button ({n}) in the plate", S(f"estop_{s}"), S(f"plate_{s}"), "touch")
        chk(f"Stop button ({n}) clear of the housing and cleats", S(f"estop_{s}"), S(f"housing_{s}") + S(f"cleats_{s}"), 3.0)
        chk(f"Brush bearing clear of the guide clevises ({n})", S("brush_bearings"), S(f"clevises_{s}"), 3.0)
        chk(f"Brush bearing clear of the axle bearings ({n})", S("brush_bearings"), S(f"axle_bearings_{s}"), 3.0)
        chk(f"Hook slider ({n}) clear of the brush bearing", S(f"slider_{s}"), S("brush_bearings"), 3.0)
    chk("Brush bearings on the plates", S("brush_bearings"), S("plate_lo") + S("plate_hi"), "touch")
    chk("Brush shafts in the bearings", S("shafts"), S("brush_bearings"), "touch")
    chk("Brush shafts in the core plugs", S("shafts"), S("plugs"), "touch")
    chk("Core plugs inside the core", S("plugs"), S("core"), "touch")
    chk("Sleeve on the core", S("sleeve"), S("core"), "touch")
    chk("Brush shaft clear of the wheel belt", S("shafts"), S("axles_lo"), 2.0)
    chk("Brush pulleys and belt clear of the wheel belt", S("brush_drive"), S("axles_lo"), 1.0)
    chk("Brush gearmotor on the lower housing", S("brush_motor"), S("housing_lo"), "touch")
    chk("Brush gearmotor clear of the drive gearmotor", S("brush_motor"), S("drive_lo"), 5.0)
    chk("Beam between the plates", S("beam"), S("plate_lo") + S("plate_hi"), "touch")
    chk("Hood spacers on the hood", S("hood_spacers"), S("hood"), "touch")
    chk("Hood spacers on the beam", S("hood_spacers"), S("beam"), "touch")
    chk("Hood and end guards clear of the sleeve", S("hood"), S("sleeve"), 4.0)
    chk("Hood clear of the plates and bearings", S("hood"), S("plate_lo") + S("plate_hi") + S("brush_bearings"), 3.0)
    chk("Pack on the beam", S("battery"), S("beam"), "touch")
    chk("Controller on the beam", S("controller"), S("beam"), "touch")
    chk("Sunshade posts on the beam", S("shade_posts"), S("beam"), "touch")
    chk("Sunshade on its posts", S("shade"), S("shade_posts"), "touch")
    chk("Sunshade clear of the pack (air gap)", S("shade"), S("battery"), 5.0)
    chk("Sunshade posts clear of the pack and controller", S("shade_posts"), S("battery") + S("controller"), 3.0)
    chk("Pack straps round the pack", S("straps"), S("battery"), "touch")
    chk("Contact bracket on the lower plate", S("contact_bracket"), S("plate_lo"), "touch")
    chk("Robot contact block on its bracket", S("contact_pad"), S("contact_bracket"), "touch")
    chk("Latch solenoid on the contact bracket", S("solenoid"), S("contact_bracket"), "touch")
    chk("Contact bracket clear of the sensor brackets", S("contact_bracket"), S("sensor_brackets_lo"), 3.0)
    chk("Contact bracket clear of the beam cleats", S("contact_bracket"), S("cleats_lo"), 3.0)
    chk("Robot clear of the glass except the brush (10 mm)", fuse([M(k) for k, c in _robot_comps(C).items()
                                                                   if k not in ("sleeve",) and not k.startswith("wheels")]), glass, 10.0)
    chk("Wheels on the frame, clear of the glass edge", M("wheels_lo") + M("wheels_hi"), glass, 4.0)
    chk("Brush sleeve pressed into the glass (interference)", M("sleeve"), glass, "overlap")
    # dock
    pu_ = park_u(p)
    R = lambda k: Pos(pu_, 0, 0) * S(k)  # noqa: E731
    robot_all = fuse([R(k) for k in _robot_comps(C)])
    dock_keys = ["rails", "cross", "rail_brackets", "spacers", "clamp_bars", "clamp_jaws", "ties", "legs", "panel",
                 "charger", "contact_post", "dock_contacts", "anemometer", "mast_clamps"]
    chk("Rail brackets in the rails", S("rail_brackets"), S("rails"), "touch")
    chk("Rail brackets on the spacers and shims", S("rail_brackets"), S("spacers"), "touch")
    chk("Spacers on the cross members", S("spacers") & bx(-900, -700, -100, 3000, -200, 200), S("cross"), "touch")
    chk("Clamp bars on the near cross member", S("clamp_bars"), S("cross"), "touch")
    chk("Shims on the clamp bars", S("spacers") & bx(-200, 0, -100, 3000, -200, 200), S("clamp_bars"), "touch")
    chk("Clamp bars under the module frame flange", S("clamp_bars"), frame, "touch")
    chk("Clamp jaws on the module frame flange", S("clamp_jaws"), frame, "touch")
    chk("Clamp jaws clear of the glass", S("clamp_jaws"), glass, 10.0)
    chk("Cross members clear of the rails (hook roller path)", S("cross"), S("rails"), 5.0)
    chk("Ties on the cross members", S("ties"), S("cross"), "touch")
    chk("Legs bolted beside the cross members", S("legs"), S("cross"), "touch")
    chk("Panel on the ties", S("panel"), S("ties"), "touch")
    chk("Charger box on the far cross member", S("charger"), S("cross"), "touch")
    chk("Contact post on the rail-start cross member", S("contact_post"), S("cross"), "touch")
    chk("Dock contact block on the post", S("dock_contacts"), S("contact_post"), "touch")
    chk("Latch tab on the dock contact block", S("latch_tab"), S("dock_contacts"), "touch")
    chk("Anemometer mast in its clamps", S("anemometer"), S("mast_clamps"), "touch")
    chk("Mast clamps on the far cross member", S("mast_clamps"), S("cross"), "touch")
    chk("Parked: wheels on the dock rails", R("wheels_lo") + R("wheels_hi"), S("rails"), "touch")
    chk("Parked: hook rollers under the dock rails", R("hook_lo") + R("hook_hi"), S("rails"), "touch")
    chk("Parked: guide rollers on the dock rails", R("guides_lo") + R("guides_hi"), S("rails"), "touch")
    chk("Parked: contact blocks 2 mm apart (spring contacts)", R("contact_pad"), S("dock_contacts"), 2.0)
    chk("Parked: latch pin through the latch tab", R("solenoid"), S("latch_tab"), 0.4)
    rest = fuse([S(k) for k in dock_keys if k not in ("rails",)])
    chk("Parked: robot clear of the dock frame and fittings", robot_all - (R("solenoid")), rest, 1.5)
    chk("Parked: robot clear of the latch tab (except the pin)", robot_all - R("solenoid"), S("latch_tab"), 1.0)
    rails_free = S("rails")
    chk("Parked: robot clear of the rails except wheels and rollers",
        fuse([R(k) for k in _robot_comps(C) if not k.startswith(("wheels", "hook", "guides"))]), rails_free, 3.0)
    # hook roller path: the whole travel from the dock to the row must be free under the frame line
    path = bx(d["rail_u"][0], 3 * p["mod_w"], p["hook_v"][0] - 1, p["hook_v"][1] + 3,
              d["hook_c"] - p["hook_d"] / 2 - 25, d["frame_bot"])
    chk("Hook roller path under the rails free of dock parts", path, fuse([S(k) for k in dock_keys if k != "rails"]), 0.5)
    # end stop
    us = p["mod_w"]
    chk("End stop blocks on the frame", S("stop_blocks"), frame, "touch")
    chk("End stop clamp screws on the frame flange", S("stop_screws"), frame, "touch")
    chk("End stop buffers on the blocks", S("stop_buffers"), S("stop_blocks"), "touch")
    u_hit = us - p["stop_l"] - p["buffer_t"] - p["wheel_u"] - p["wheel_d"] / 2
    H = lambda k: Pos(u_hit, 0, 0) * S(k)  # noqa: E731
    chk("At the stop: wheels meet the buffers", H("wheels_lo") + H("wheels_hi"), S("stop_buffers"), "touch")
    others = fuse([H(k) for k in _robot_comps(C) if not k.startswith("wheels")])
    chk("At the stop: nothing else meets the stop (sensors pass over)", others, S("stop_blocks") + S("stop_buffers") + S("stop_screws"), 3.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    r = robot()
    dock = Compound(children=list(dock_parts().values()), label="Dock")
    stop = stop_parts(PARAMS["mod_w"])
    for name, shape in (("dustrunner-robot", r), ("dustrunner-dock", dock), ("dustrunner-end-stop", stop)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    export_step(assembly(), str(root / "step" / "dustrunner-assembly.step"))
    bb = r.bounding_box()
    print(f"robot envelope {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (u x v x w)")
    print("exported STEP to cad/step and STL to cad/stl")
    print_checks()
