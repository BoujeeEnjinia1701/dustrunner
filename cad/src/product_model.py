"""DustRunner product appearance model (build123d), TRL 3, updated 2026-10-02 to the constructable design.

Finished-product look for photoreal renders: the robot on a compact two-module row of a ground-mount
table, partway along the first module and moving away from its dock, with dusty glass still ahead of
it. The robot gets a filleted anodized beam with a name plate and accent stripe, a white powder-coated
brush hood on nylon spacers, a microfiber brush sleeve on its core and stub shafts, a sunshade on
four posts over a strapped LiFePO4 pack and an IP65 controller box with a clear side window (board,
module and a lit status light behind it), a main switch and cable glands. Each end truck is
model.py's constructable truck: a graphite plate with bolts and a badge, polyurethane wheels in
2-bolt flange bearings, a folded drive housing carrying the gearmotor, guide rollers on folded
clevises, a sprung hook slider with its roller and spring, beam end cleats, IR edge sensors on
brackets and a red emergency stop on a yellow base; the lower truck also has the brush drive and
gearmotor, the dock contact bracket and block, and the latch solenoid. The dock is model.py's
constructable dock: C-section rails on rail brackets, cross members, frame clamps, ties, vertical
square-tube legs on foot plates, a framed 20 W panel with cells, a charger box with a lit charge
light, the contact post with its latch tab, and a vertical anemometer mast in two clamps with a
three-cup head. End stops are the clamp-on three-piece blocks with rubber buffers.
Context: two reference modules (cells, backsheet, frames), purlins, rafters, posts with footings and
a compact patch of gravel ground.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and the geometry in model.py
(_truck, _brush_and_hood, build_components for the dock, _stops, frame_edge). The dock contact
bracket and the bearing flanges are the model's own parts, not appearance-only (decision of 2026-10-02). Parts are built in model.py's local
table coordinates (u along the row, v up the slope, w normal to the glass) and then placed in world
coordinates with the same transform as cad/src/concept_media.py (table tilted by PARAMS["tilt"], lower
glass edge PARAMS["h0"] above the ground, Z up), because the renderer needs Z up and a ground plane.
In world coordinates the row runs along +Y, the glass faces +X and the slope rises toward -X.

Groups: "internal" holds the lower end truck and brush drive (the edge clamp) with a short section of
the module frame it rides on, so the "detail" view can frame that subsystem; the upper truck, which is
its mirror image, is in "shell". The dock and end stops are "accessory".

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import radians, sin, cos
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import Axis, Box, Cylinder, Pos, RegularPolygon, Rot, Sphere, extrude, fillet
from model import (PARAMS, derived, bx, cyl_v, cyl_w, mirror_v, frame_edge, tube, build_components,  # noqa: E402
                   _truck, _brush_and_hood, _stops as _model_stops)

TITLE = "DustRunner: rail-free cleaning robot for solar panel rows"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); robot partway along a "
             "two-module row with dusty glass ahead of it, its dock with the 20 W panel and anemometer in front"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): chassis beam, hood and "
             "sunshade, brush, pack and controller, both end trucks with wheels, guide and hook rollers and "
             "gearmotors, brush drive; dock rails, panel, charger, contacts and anemometer; end stops"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 20, "az": -110,
     "note": "Detail from the dock end on the uphill side, above (about 20 deg elevation): lower end truck "
             "clamped on a section of the module frame, wheels on the top flange, hook arm and roller under the "
             "lip, charge contacts facing the dock and the emergency stop; rest of the robot and row not shown"},
]

# Scene layout (render only)
N_MOD = 2                                     # modules shown (a reference row is about 35)
U_ROBOT = 560.0                               # robot centre along the row, partway along module 1
SECTION = 300.0                               # frame section under the lower truck: U_ROBOT +/- this

# Colours (restrained product palette; kit accent)
C_ACCENT = "#0F766E"
C_WHITE = "#E8EAEC"
C_ALU = "#C3C9D0"
C_ALU_D = "#9AA2AB"
C_GRAPH = "#3A4048"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_RUBBER = "#26292E"
C_SLEEVE = "#56687A"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LED_G = "#22C55E"
C_LABEL = "#F4F4F2"
C_WINDOW = "#DCEBF5"
C_COPPER = "#B87333"
C_YELLOW = "#E0B000"
C_RED = "#B91C1C"
C_CELL = "#1B2A4A"
C_BACK = "#D5D9DE"
C_FRAME = "#B8C0C8"
C_DUST = "#CBBE9E"
C_STEEL = "#AEB4BB"
C_CONC = "#BDB8AE"
C_GROUND = "#CFC8BA"

P = PARAMS
TILT, H0 = P["tilt"], P["h0"]


# ---------------- placement ----------------
def T(shape):
    """Local (u, v, w) table coordinates to world, as concept_media.T()."""
    return Pos(0, 0, H0) * Rot(0, 0, 90) * Rot(TILT, 0, 0) * shape


def t_vec(u, v, w):
    """Local vector to world (no H0 offset), matching T()."""
    t = radians(TILT)
    return (-(v * cos(t) - w * sin(t)), float(u), v * sin(t) + w * cos(t))


# ---------------- helpers ----------------
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _sum(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def cyl_u(u0, u1, v, w, r):
    """Cylinder with its axis along u."""
    return Pos((u0 + u1) / 2, v, w) * Rot(0, 90, 0) * Cylinder(r, abs(u1 - u0))


def _par(s, axis):
    return s.edges().filter_by(axis)


def _face_edges(s, axis, i):
    return s.faces().sort_by(axis)[i].edges()


def _hex_v(u, v0, v1, w, af):
    """Hex prism along v from v0 to v1 (across flats af)."""
    h = RegularPolygon(af / 1.732, 6)
    return Pos(u, min(v0, v1), w) * Rot(-90, 0, 0) * extrude(h, amount=abs(v1 - v0))


def _hex_u(u0, u1, v, w, af):
    h = RegularPolygon(af / 1.732, 6)
    return Pos(min(u0, u1), v, w) * Rot(0, 90, 0) * extrude(h, amount=abs(u1 - u0))


def _hex_w(u, v, w0, w1, af):
    return Pos(u, v, min(w0, w1)) * extrude(RegularPolygon(af / 1.732, 6), amount=abs(w1 - w0))


# ---------------- robot pieces (local, robot centred at u = 0) ----------------
_MEMO = {}


def _tr(lower):
    """model.py's end truck (memoised): lower=True has the brush drive, dock contacts and latch solenoid."""
    if lower not in _MEMO:
        _MEMO[lower] = _truck(P, lower=lower)
    return _MEMO[lower]


def _truck_items(D, lower):
    """One end truck, taken from model.py's constructable parts (plate, flange bearings, drive housing,
    clevis-mounted guide rollers, sprung hook slider, beam cleats, sensor brackets; for the lower truck
    also the brush drive, dock contact bracket and latch solenoid), coloured for the renders.
    Returns a list of (name, shape, color, material, bom, explode)."""
    c = _tr(lower)
    pv0, pv1 = D["plate_v"]
    hv0 = D["housing_v"][0]
    hu = P["plate_half_u"]
    wc = D["wheel_c"]
    w_lo, w_hi = P["plate_w"]
    items = []

    blank = bx(-hu, hu, pv0, pv1, w_lo, w_hi)
    plate = _fillet_try(blank, _par(blank, Axis.Y), [14.0, 10.0, 6.0]) - (blank - c["plate"])
    items.append(("End truck plate", plate, C_GRAPH, "painted", 5, (0, -380, 0)))
    bolts = _sum(_hex_v(su * 12, pv0 - 4, pv0, wz, 10.0) for su in (-1, 1) for wz in (175, 205))
    items.append(("Truck plate bolts", bolts, C_ALU, "metal", 15, (0, -420, 0)))
    badge = bx(-120, -50, pv0 - 0.5, pv0, 162, 194)
    badge = _fillet_try(badge, _par(badge, Axis.Y), [4.0, 2.0])
    items.append(("Truck badge", badge, C_ACCENT, "painted", 5, (0, -400, 0)))
    bprint = bx(-112, -70, pv0 - 0.8, pv0 - 0.5, 180, 186) + bx(-112, -85, pv0 - 0.8, pv0 - 0.5, 170, 173)
    items.append(("Truck badge print", bprint, C_LABEL, "paper", 5, (0, -400, 0)))

    items.append(("Wheel tyres (polyurethane)", c["wheels"], C_ACCENT, "rubber", 5, (0, -330, 0)))
    items.append(("Wheel axles, pulleys and belt", c["axles"] + c["coupling"], C_ALU, "metal", 5, (0, -330, 0)))
    items.append(("Axle flange bearings (2-bolt)", c["axle_bearings"], C_ALU_D, "metal", 5, (0, -250, 0)))
    items.append(("Drive housing (folded sheet)", c["housing"], C_DARK, "painted", 5, (0, -500, 0)))
    items.append(("Brush flange bearing", c["brush_bearing"], C_ALU_D, "metal", 2, (0, -200, 0)))

    # drive gearmotor on the housing's outer wall, coaxial with the +u axle: gearbox, can, encoder cap
    u, rd = P["wheel_u"], P["drive_d"] / 2
    va, vb = hv0, hv0 - P["drive_l"]
    gbox = cyl_v(u, wc, va - 22, va, rd)
    gbox = _fillet_try(gbox, _face_edges(gbox, Axis.Y, 0), [1.5, 1.0])
    items.append(("Drive gearbox", gbox, C_ALU_D, "metal", 6, (0, -600, 0)))
    can = cyl_v(u, wc, vb + 8, va - 22, rd - 1.0)
    for k in range(4):
        can -= cyl_v(u, wc, va - 30 - 7 * k, va - 28.8 - 7 * k, rd + 1) - cyl_v(u, wc, va - 31 - 7 * k, va - 28 - 7 * k, rd - 1.8)
    items.append(("Drive motor can", can, C_ALU, "metal", 6, (0, -600, 0)))
    cap = cyl_v(u, wc, vb, vb + 8, rd - 1.0)
    cap = _fillet_try(cap, _face_edges(cap, Axis.Y, 0), [3.0, 2.0, 1.0])
    items.append(("Drive encoder cap", cap, C_BLACK, "plastic", 6, (0, -600, 0)))
    items.append(("Motor shaft", c["drive_motor"] - cyl_v(u, wc, vb - 1, va, rd + 1), C_STEEL, "metal", 6, (0, -600, 0)))

    items.append(("Guide roller tyres", c["guide_rollers"], C_RUBBER, "rubber", 7, (0, -380, -170)))
    items.append(("Guide roller clevises (folded)", c["guide_clevises"], C_ALU, "metal", 7, (0, -380, -170)))
    items.append(("Hook roller tyre", c["hook_roller"], C_RUBBER, "rubber", 7, (0, -380, -280)))
    items.append(("Hook roller axle", c["hook_axle"], C_ALU, "metal", 7, (0, -380, -280)))
    items.append(("Hook slider (sprung)", c["hook_slider"], C_GRAPH, "painted", 7, (0, -380, -280)))
    items.append(("Hook preload spring and seat", c["hook_spring"] + c["spring_seat"], C_STEEL, "metal", 7, (0, -380, -230)))

    sens, lens = [], []
    for sg in (-1, 1):
        a, b = sorted((sg * hu, sg * (hu + 22)))
        lens.append(cyl_w((a + b) / 2, 12, 44.4, 45, 5.0))
    items.append(("IR edge sensor housings", c["sensors"], C_BLACK, "plastic", 10, (0, -380, 110)))
    items.append(("IR edge sensor lenses", _sum(lens), "#3B0D12", "screen", 10, (0, -380, 110)))
    items.append(("Sensor brackets", c["sensor_brackets"], C_GRAPH, "painted", 10, (0, -380, 110)))
    items.append(("Beam end cleats", c["cleats"], C_ALU, "metal", 15, (0, -300, 380)))
    items.append(("Beam cleat bolts", c["cleat_bolts"], C_STEEL, "metal", 15, (0, -300, 420)))

    # emergency stop: yellow base ring on the plate, red mushroom button
    base = cyl_v(95, 185, pv0 - 8, pv0, 26.0)
    items.append(("Emergency stop base", base, C_YELLOW, "plastic", 15, (0, -380, 190)))
    mush = cyl_v(95, 185, pv0 - 40, pv0 - 8, 20.0)
    mush = _fillet_try(mush, _face_edges(mush, Axis.Y, 0), [5.0, 3.0, 2.0])
    items.append(("Emergency stop button", mush, C_RED, "plastic", 15, (0, -380, 230)))
    items.append(("Emergency stop inner body", c["estop"] - cyl_v(95, 185, pv0 - 40, pv0, 21.0), C_DARK, "plastic", 15, (0, -380, 190)))

    if lower:
        mu, mv, mw = P["brush_motor"]
        items.append(("Brush drive pulleys", c["brush_pulleys"], C_ALU_D, "metal", 4, (0, -500, 70)))
        items.append(("Brush drive belt", c["brush_belt"], C_BLACK, "rubber", 4, (0, -500, 70)))
        bm = _fillet_try(c["brush_motor"], _par(c["brush_motor"], Axis.Y), [8.0, 5.0, 3.0])
        items.append(("Brush gearmotor", bm, C_DARK, "plastic", 4, (0, -640, 140)))
        blab = bx(-mu / 2 - 0.4, -mu / 2, hv0 - mv + 10, hv0 - 22, 117.0 - 8, 117.0 + 8)
        items.append(("Brush gearmotor accent label", blab, C_ACCENT, "painted", 4, (0, -640, 140)))
        items.append(("Dock contact bracket (folded)", c["contact_bracket"], C_ALU, "metal", 13, (-140, -380, 0)))
        items.append(("Charge contact block", c["contact_pad"], C_BLACK, "plastic", 13, (-140, -380, 0)))
        strips = _sum(bx(-138.6, -138, -22 + k * 14, -13 + k * 14, 96, 120) for k in range(3))
        items.append(("Charge contact plates (copper)", strips, C_COPPER, "metal", 13, (-140, -380, 0)))
        items.append(("Latch solenoid and pin", c["solenoid"], C_STEEL, "metal", 13, (-140, -380, 60)))
    return items


def _erad(e):
    try:
        return e.radius
    except Exception:
        return -1.0


def _robot_body(D):
    """Robot pieces other than the trucks: list of (name, shape, color, material, bom, explode)."""
    L = P["mod_l"]
    pv0, pv1 = D["plate_v"]
    w0, w1 = D["beam_w"]
    bw = D["brush_w"]
    v0, v1 = D["brush_v"]
    items = []

    # 1 chassis beam, name plate and accent stripe on the dock-side face
    b, t = P["beam_b"], P["beam_t"]
    beam = bx(-b / 2, b / 2, pv1, L - pv1, w0, w1)
    beam = _fillet_try(beam, _par(beam, Axis.Y), [2.5, 1.5])
    beam -= bx(-b / 2 + t, b / 2 - t, pv1 - 1, L - pv1 + 1, w0 + t, w1 - t)
    beam -= _tr(True)["beam_holes"] + mirror_v(_tr(False)["beam_holes"], P)      # cleat bolt holes, as model.py
    items.append(("Chassis beam (anodized aluminum)", beam, C_ALU, "metal", 1, (0, 0, 380)))
    stripe = bx(-b / 2 - 0.4, -b / 2, 700, 1880, w1 - 16, w1 - 11)
    items.append(("Beam accent stripe", stripe, C_ACCENT, "painted", 1, (0, 0, 380)))
    plate = bx(-b / 2 - 0.5, -b / 2, 1060, 1360, w0 + 14, w0 + 50)
    plate = _fillet_try(plate, _par(plate, Axis.X), [5.0, 3.0])
    items.append(("Beam name plate", plate, C_LABEL, "paper", 1, (0, 0, 380)))
    nprint = bx(-b / 2 - 0.8, -b / 2 - 0.5, 1080, 1250, w0 + 30, w0 + 42) + \
        bx(-b / 2 - 0.8, -b / 2 - 0.5, 1080, 1320, w0 + 22, w0 + 25) + \
        bx(-b / 2 - 0.8, -b / 2 - 0.5, 1300, 1340, w0 + 30, w0 + 42)
    items.append(("Beam name plate print", nprint, C_DARK, "paper", 1, (0, 0, 380)))

    # 2 brush: microfiber sleeve, core ends and stub shafts
    sleeve = cyl_v(0, bw, v0, v1, P["brush_d"] / 2) - cyl_v(0, bw, v0 - 1, v1 + 1, P["core_d"] / 2)
    sleeve = _fillet_try(sleeve, [e for e in sleeve.edges() if abs(_erad(e) - P["brush_d"] / 2) < 0.5], [8.0, 5.0, 3.0])
    items.append(("Microfiber brush sleeve", sleeve, C_SLEEVE, "fabric", 2, (0, 0, 0)))
    rc = P["core_d"] / 2
    core = (cyl_v(0, bw, v0 - 10, v0 + 1, rc) + cyl_v(0, bw, v1 - 1, v1 + 10, rc))
    core -= cyl_v(0, bw, v0 - 11, v0 + 2, rc - P["core_t"]) + cyl_v(0, bw, v1 - 2, v1 + 11, rc - P["core_t"])
    core += cyl_v(0, bw, v0 - 8, v0 - 4, rc - P["core_t"]) + cyl_v(0, bw, v1 + 4, v1 + 8, rc - P["core_t"])
    items.append(("Brush core ends", core, C_ALU, "metal", 2, (0, 0, 0)))

    # 3 hood: bent sheet with rolled edges, end guards and hangers to the beam
    r0, r1 = P["hood_r"], P["hood_r"] + P["hood_t"]
    ring = cyl_v(0, bw, v0 - 5, v1 + 5, r1) - cyl_v(0, bw, v0 - 6, v1 + 6, r0)
    wc0 = bw + P["hood_clear"]
    hood = ring & bx(-r1 - 1, r1 + 1, v0 - 6, v1 + 6, wc0, bw + r1 + 1)
    guard = cyl_v(0, bw, v0 - 6, v0 - 5, r1) & bx(-r1, r1, v0 - 7, v0 - 4, wc0, bw + r1)
    hood = hood + guard + mirror_v(guard, P)
    ue = ((r0 + P["hood_t"] / 2) ** 2 - P["hood_clear"] ** 2) ** 0.5
    for su in (-1, 1):
        hood += cyl_v(su * ue, wc0 + 0.5, v0 - 5, v1 + 5, 1.8)
    items.append(("Brush hood (powder-coated)", hood, C_WHITE, "painted", 3, (0, 0, 200)))
    bh = _brush_and_hood(P)
    items.append(("Hood spacers (nylon, on M5 screws)", bh["hood_spacers"], C_WHITE, "plastic", 15, (0, 0, 290)))
    items.append(("Brush stub shafts", bh["shafts"], C_ALU, "metal", 2, (0, 0, 0)))
    hlab = bx(-r1 - 2, 0, 700, 1880, wc0 + 12, wc0 + 19) & (
        cyl_v(0, bw, 690, 1890, r1 + 0.45) - cyl_v(0, bw, 680, 1900, r1 - 0.2))
    items.append(("Hood accent band", hlab, C_ACCENT, "painted", 3, (0, 0, 200)))

    # sunshade over the pack and controller, on four spacer posts screwed into the beam's top wall (model.py)
    st = D["shade_w"]
    sv0, sv1 = P["pack_v"] - 20, P["ebox_v"] + P["ebox"][1] + 20
    shade = bx(-60, 60, sv0, sv1, st, st + P["shade_t"])
    shade = _fillet_try(shade, _par(shade, Axis.Z), [6.0, 3.0])
    items.append(("Sunshade (powder-coated)", shade, C_WHITE, "painted", 3, (0, 0, 800)))
    items.append(("Sunshade posts", bh["shade_posts"], C_STEEL, "metal", 15, (0, 0, 700)))

    # 8 LiFePO4 pack, label and straps
    pu, pvl, pw = P["pack"]
    pv_ = P["pack_v"]
    pack = bx(-pu / 2, pu / 2, pv_, pv_ + pvl, w1, w1 + pw)
    pack = _fillet_try(pack, _par(pack, Axis.Z), [6.0, 4.0, 2.0])
    pack = _fillet_try(pack, _face_edges(pack, Axis.Z, -1), [2.0, 1.0])
    pack -= bx(-pu / 2 - 1, pu / 2 + 1, pv_ - 1, pv_ + pvl + 1, w1 + pw - 20.8, w1 + pw - 20) - \
        bx(-pu / 2 + 0.8, pu / 2 - 0.8, pv_ + 0.8, pv_ + pvl - 0.8, w1, w1 + pw)
    items.append(("LiFePO4 pack case", pack, C_DARK, "plastic", 8, (0, 0, 580)))
    plab = bx(-pu / 2 - 0.5, -pu / 2, pv_ + 42, pv_ + 110, w1 + 18, w1 + 64)
    items.append(("Pack label", plab, C_LABEL, "paper", 8, (0, 0, 580)))
    pband = bx(-pu / 2 - 0.8, -pu / 2 - 0.5, pv_ + 42, pv_ + 110, w1 + 56, w1 + 62) + \
        bx(-pu / 2 - 0.8, -pu / 2 - 0.5, pv_ + 50, pv_ + 80, w1 + 40, w1 + 48)
    items.append(("Pack label print", pband, C_ACCENT, "paper", 8, (0, 0, 580)))
    straps = None
    for vv in (pv_ + 30, pv_ + pvl - 50):                  # as model.py: round the beam and the pack
        sx_ = bx(-pu / 2 - 2, pu / 2 + 2, vv, vv + 20, w0 - 2, w1 + pw + 2) - bx(-pu / 2, pu / 2, vv - 1, vv + 21, w0, w1 + pw)
        straps = sx_ if straps is None else straps + sx_
    items.append(("Pack straps (webbing)", straps, C_BLACK, "fabric", 15, (0, 0, 620)))

    # 9 controller: IP65 box, clear side window, board behind it, main switch, glands
    eu, evl, ew = P["ebox"]
    ev0, ev1 = P["ebox_v"], P["ebox_v"] + evl
    EC = (0, 0, 560)
    box = bx(-eu / 2, eu / 2, ev0, ev1, w1, w1 + ew)
    box = _fillet_try(box, _par(box, Axis.Z), [5.0, 3.0])
    box = _fillet_try(box, _face_edges(box, Axis.Z, -1), [3.0, 2.0, 1.0])
    box -= bx(-eu / 2 + 2.5, eu / 2 - 2.5, ev0 + 2.5, ev1 - 2.5, w1 + 2.5, w1 + ew - 2.5)
    wv0, wv1, ww0, ww1 = ev0 + 26, ev1 - 12, w1 + 10, w1 + 42
    box -= bx(-eu / 2 - 1, -eu / 2 + 3, wv0, wv1, ww0, ww1)
    box -= bx(-eu / 2 - 1, eu / 2 + 1, ev0 - 1, ev1 + 1, w1 + ew - 9.6, w1 + ew - 9) - \
        bx(-eu / 2 + 0.6, eu / 2 - 0.6, ev0 + 0.6, ev1 - 0.6, w1, w1 + ew)
    items.append(("Controller enclosure", box, "#DDE1E5", "plastic", 9, EC))
    pane = bx(-eu / 2 + 0.4, -eu / 2 + 2.5, wv0 - 3, wv1 + 3, ww0 - 3, ww1 + 3)
    items.append(("Controller window (clear polycarbonate)", pane, C_WINDOW, "clear", 9, (-150, 0, 560)))
    pcb = bx(-eu / 2 + 10, -eu / 2 + 11.6, ev0 + 6, ev1 - 6, w1 + 5, w1 + ew - 12)
    items.append(("Controller board", pcb, C_PCB, "plastic", 9, (-75, 0, 560)))
    chips = bx(-eu / 2 + 5, -eu / 2 + 10, wv0 + 8, wv0 + 34, ww0 + 6, ww0 + 26) + \
        bx(-eu / 2 + 7, -eu / 2 + 10, wv0 + 44, wv0 + 60, ww0 + 4, ww0 + 14) + \
        bx(-eu / 2 + 6, -eu / 2 + 10, wv0 + 44, wv0 + 70, ww0 + 18, ww0 + 28)
    items.append(("Controller chips and drivers", chips, C_CHIP, "plastic", 9, (-75, 0, 560)))
    shield = bx(-eu / 2 + 4.4, -eu / 2 + 5, wv0 + 10, wv0 + 32, ww0 + 8, ww0 + 24)
    items.append(("Controller module shield can", shield, C_ALU, "metal", 9, (-75, 0, 560)))
    led = cyl_u(-eu / 2 + 7, -eu / 2 + 10, wv1 - 8, ww1 - 6, 2.4)
    items.append(("Controller status light (lit)", led, C_LED_G, "emissive", 9, (-75, 0, 560)))
    sw = bx(-eu / 2 - 3, -eu / 2, ev0 + 6, ev0 + 20, w1 + 16, w1 + 36)
    sw = _fillet_try(sw, _par(sw, Axis.X), [2.0, 1.0])
    items.append(("Main switch bezel", sw, C_BLACK, "plastic", 15, EC))
    rock = bx(-eu / 2 - 5, -eu / 2 - 3, ev0 + 8, ev0 + 18, w1 + 18, w1 + 34) - \
        Pos(-eu / 2 - 6.8, ev0 + 13, w1 + 22) * Rot(20, 0, 0) * Box(4, 12, 12)
    items.append(("Main switch rocker", rock, C_RED, "plastic", 15, EC))
    gl = None
    for u in (-18, 18):
        g = _hex_v(u, ev0 - 5, ev0, w1 + 28, 16.0) + cyl_v(u, w1 + 28, ev0 - 12, ev0 - 5, 6.5)
        g = _fillet_try(g, _face_edges(g, Axis.Y, 0), [2.0, 1.0])
        gl = g if gl is None else gl + g
    items.append(("Controller cable glands", gl, C_DARK, "plastic", 9, EC))
    return items


# ---------------- dock, end stops (local) ----------------
def _dock(Cm):
    """Dock and anemometer from model.py's constructable parts (rails, cross members, rail brackets and
    spacers, frame clamps, ties, vertical legs on foot plates, contact post and latch tab, vertical mast
    in two clamps), with the panel, charger and anemometer cups dressed for the renders."""
    L = P["mod_l"]
    D = derived(P)
    uf, ur, un = D["cross_u"]
    cs, ct, bot = P["cross"], P["cross_top"], D["frame_bot"]
    items = []
    items.append(("Dock rails (aluminum C-section)", Cm["rails"].shape, C_ALU, "metal", 11, (0, 0, 0)))
    items.append(("Dock cross members and ties", Cm["cross"].shape + Cm["ties"].shape, C_ALU_D, "metal", 11, (0, 0, -140)))
    items.append(("Dock rail brackets, spacers and shims", Cm["rail_brackets"].shape + Cm["spacers"].shape, C_STEEL, "metal", 11, (0, 0, -80)))
    items.append(("Dock clamps (bar and jaw)", Cm["clamp_bars"].shape + Cm["clamp_jaws"].shape, C_GRAPH, "painted", 11, (220, 0, -60)))
    items.append(("Dock bolts", Cm["dock_bolts"].shape, C_STEEL, "metal", 11, (220, 0, -100)))
    items.append(("Dock legs (aluminum square tube, foot plates)", Cm["legs"].shape, C_ALU_D, "metal", 11, (0, 0, 0)))

    # 12 PV panel on the ties: frame, backsheet and cells
    pu, pvl, pw = P["panel"]
    pc = (uf + cs + ur) / 2
    pv0, pv1 = 120, 120 + pvl
    pw0, pw1 = ct + 20, ct + 20 + pw
    fr = bx(pc - pu / 2, pc + pu / 2, pv0, pv1, pw0, pw1) - bx(pc - pu / 2 + 12, pc + pu / 2 - 12, pv0 + 12, pv1 - 12, pw0 - 1, pw1 + 1)
    fr += bx(pc - pu / 2 + 11, pc + pu / 2 - 11, pv0 + 11, pv1 - 11, pw0, pw0 + 3)
    items.append(("Dock panel frame (aluminum)", fr, C_ALU, "metal", 12, (0, 0, 240)))
    back = bx(pc - pu / 2 + 12, pc + pu / 2 - 12, pv0 + 12, pv1 - 12, pw1 - 6, pw1 - 3.5)
    items.append(("Dock panel backsheet", back, C_BACK, "paper", 12, (0, 0, 240)))
    cells = bx(pc - pu / 2 + 12, pc + pu / 2 - 12, pv0 + 12, pv1 - 12, pw1 - 3.5, pw1 - 1.5)
    for k in range(1, 4):
        uu = pc - pu / 2 + 12 + k * (pu - 24) / 4
        cells -= bx(uu - 1.2, uu + 1.2, pv0, pv1, pw1 - 5, pw1)
    for k in range(1, 6):
        vv = pv0 + 12 + k * (pvl - 24) / 6
        cells -= bx(pc - pu, pc + pu, vv - 1.2, vv + 1.2, pw1 - 5, pw1)
    items.append(("Dock panel cells (glass)", cells, C_CELL, "screen", 12, (0, 0, 240)))

    # 13 charger box on the far cross member's +u face, charge light, contact post with block and latch tab
    cu0 = uf + cs
    ch = bx(cu0, cu0 + 120, 760, 880, ct - cs - 14, ct + 26)
    ch = _fillet_try(ch, _par(ch, Axis.Z), [5.0, 3.0])
    ch = _fillet_try(ch, _face_edges(ch, Axis.Z, -1), [3.0, 2.0, 1.0])
    items.append(("Dock charger box", ch, "#DDE1E5", "plastic", 13, (0, 0, 280)))
    items.append(("Dock charger label", bx(cu0 + 20, cu0 + 100, 780, 830, ct + 26, ct + 26.4), C_ACCENT, "painted", 13, (0, 0, 280)))
    items.append(("Dock charge light (lit)", cyl_w(cu0 + 90, 860, ct + 26, ct + 28.5, 3.5), C_LED_G, "emissive", 13, (0, 0, 280)))
    post = Cm["contact_post"].shape + Cm["dock_contacts"].shape + Cm["latch_tab"].shape
    items.append(("Dock contact post, block and latch tab", post, C_BLACK, "plastic", 13, (0, -160, 160)))
    uf_c = ur + cs + 20
    tips = _sum(bx(uf_c, uf_c + 0.8, vv, vv + 10, 96, 122) for vv in (-30, -10, 10))
    items.append(("Dock spring contact plates (copper)", tips, C_COPPER, "metal", 13, (0, -160, 160)))

    # 16 anemometer: vertical mast in two clamps on the far cross member (model.py), hub and three cups
    t = radians(P["tilt"])
    up = (0.0, sin(t), cos(t))
    base = (uf - 12, L - 200, ct - cs)
    top = tuple(base[i] + P["mast_h"] * up[i] for i in range(3))
    items.append(("Anemometer mast", tube(base, top, 12.0), C_ALU, "metal", 16, (0, 0, 380)))
    items.append(("Anemometer mast clamps", Cm["mast_clamps"].shape, C_STEEL, "metal", 16, (0, 0, 380)))
    hub = cyl_w(0, 0, 0, 26, 11.0)
    hub = _fillet_try(hub, _face_edges(hub, Axis.Z, -1), [4.0, 2.0])
    cups = hub
    for k in range(3):
        a = 120 * k
        arm = Pos(0, 0, 18) * Rot(0, 0, a) * Pos(22, 0, 0) * Rot(0, 90, 0) * Cylinder(2.0, 44)
        cup = (Sphere(14) - Sphere(12.8)) & Pos(-7.5, 0, 0) * Box(15, 30, 30)
        cup = Pos(0, 0, 18) * Rot(0, 0, a) * Pos(44, 0, 0) * Rot(0, 0, 90) * cup
        cups = cups + arm + cup
    items.append(("Anemometer cups and hub", Pos(*top) * Rot(-P["tilt"], 0, 0) * cups, C_WHITE, "plastic", 16, (0, 0, 420)))
    return items


def _stops(u_end):
    """Clamp-on end stops from model.py: top block, outer plate and bottom jaw, clamp screw, rubber buffer."""
    S = _model_stops(u_end, P)
    return [("End stop blocks (clamp-on, three-piece)", S["stop_blocks"].shape, C_GRAPH, "painted", 14, (0, 0, -120)),
            ("End stop clamp screws", S["stop_screws"].shape, C_STEEL, "metal", 14, (0, 0, -200)),
            ("End stop rubber buffers", S["stop_buffers"].shape, C_RUBBER, "rubber", 14, (-120, 0, 0))]


# ---------------- context (local, not in the BOM) ----------------
def _row(D):
    L, W, G = P["mod_l"], P["mod_w"], P["gap"]
    lip = P["lip"]
    top, bot = P["frame_proud"], P["frame_proud"] - P["frame_d"]
    frames, backs, cells, dust = [], [], [], []
    s0, s1 = U_ROBOT - SECTION, U_ROBOT + SECTION
    for k in range(N_MOD):
        u0 = k * (W + G)
        lower = frame_edge(u0, u0 + W, P)
        if u0 < s0 and s1 < u0 + W:
            lower = frame_edge(u0, s0, P) + frame_edge(s1, u0 + W, P)
        ring = lower + mirror_v(frame_edge(u0, u0 + W, P), P)
        ring += bx(u0, u0 + lip, 0, L, bot, top) + bx(u0 + W - lip, u0 + W, 0, L, bot, top)
        frames.append(ring)
        backs.append(bx(u0 + lip, u0 + W - lip, lip, L - lip, -6, -2.5))
        c = bx(u0 + lip, u0 + W - lip, lip, L - lip, -2.5, 0)
        for j in range(1, 6):
            uu = u0 + lip + j * (W - 2 * lip) / 6
            c -= bx(uu - 1.5, uu + 1.5, 0, L, -3, 1)
        for j in range(1, 24):
            vv = lip + j * (L - 2 * lip) / 24
            c -= bx(u0, u0 + W, vv - 1.5, vv + 1.5, -3, 1)
        cells.append(c)
        a = max(u0 + lip, U_ROBOT + 95)
        if u0 + W - lip > a:
            dust.append(bx(a, u0 + W - lip, lip, L - lip, 0, 0.6))
    section = frame_edge(s0, s1, P)
    return _sum(frames), _sum(backs), _sum(cells), _sum(dust), section


def _structure_world():
    """Purlins and rafters (local) plus posts, footings and ground (world), as concept_media."""
    L = P["mod_l"]
    row_l = N_MOD * P["mod_w"] + (N_MOD - 1) * P["gap"]
    ft = P["frame_d"]
    purl = bx(-40, row_l + 40, 400, 450, -ft - 60, -ft) + bx(-40, row_l + 40, 1830, 1880, -ft - 60, -ft)
    raft = None
    for u in (300.0, row_l - 300.0):
        r = bx(u - 30, u + 30, -80, L + 80, -ft - 120, -ft - 60)
        raft = r if raft is None else raft + r
    posts, feet = [], []
    for u in (300.0, row_l - 300.0):
        for v in (350.0, 1950.0):
            x, y, z = t_vec(u, v, -ft - 120)
            z += H0
            posts.append(Pos(x, y, z / 2) * Cylinder(40, z))
            feet.append(Pos(x, y, 15) * Cylinder(110, 30))
    # ground patch around the footprint
    xs, ys = [], []
    for u in (P["dock_u0"], row_l):
        for v in (-120.0, L + 120.0):
            x, y, _ = t_vec(u, v, -ft - 150)
            xs.append(x); ys.append(y)
    m = 150.0
    x0, x1, y0, y1 = min(xs) - m, max(xs) + m, min(ys) - m, max(ys) + m
    ground = Pos((x0 + x1) / 2, (y0 + y1) / 2, -15) * Box(x1 - x0, y1 - y0, 30)
    ground = _fillet_try(ground, _face_edges(ground, Axis.Z, -1), [10.0, 5.0])
    return purl + raft, _sum(posts), _sum(feet), ground


def product_parts(p=PARAMS):
    D = derived(p)
    out = []
    shift = Pos(U_ROBOT, 0, 0)

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0), world=False, robot=False):
        s = shift * shape if robot else shape
        s = s if world else T(s)
        e = explode if world else t_vec(*explode)
        out.append({"name": name, "shape": s, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in e)})

    # robot body (shell)
    for name, s, c, m, b, e in _robot_body(D):
        add(name, s, c, m, b, "shell", e, robot=True)
    # lower truck and brush drive (internal) and the upper truck, its mirror image (shell)
    for name, s, c, m, b, e in _truck_items(D, True):
        add(name + ", lower", s, c, m, b, "internal", e, robot=True)
    for name, s, c, m, b, e in _truck_items(D, False):
        add(name + ", upper", mirror_v(s, P), c, m, b, "shell", (e[0], -e[1], e[2]), robot=True)
    # dock and end stops (accessory) from the constructable model
    Cm = build_components(P)
    for name, s, c, m, b, e in _dock(Cm):
        e = (e[0] + 300, e[1], e[2])                 # exploded view: dock drawn nearer the robot
        add(name, s, c, m, b, "context" if name.startswith("Dock legs") else "accessory", e)
    row_l = N_MOD * P["mod_w"] + (N_MOD - 1) * P["gap"]
    for name, s, c, m, b, e in _stops(row_l):
        add(name, s, c, m, b, "accessory", (e[0] - 900, e[1], e[2]))   # drawn nearer the robot
    # context
    frames, backs, cells, dust, section = _row(D)
    add("Module frame section under the lower truck (reference, not in BOM)", section, C_FRAME, "metal", None, "internal")
    add("Reference PV module frames (aluminum)", frames, C_FRAME, "metal", None, "context")
    add("Reference PV module backsheet", backs, C_BACK, "paper", None, "context")
    add("Reference PV module cells (glass)", cells, C_CELL, "screen", None, "context")
    add("Dust film, not yet cleaned (illustrative)", dust, C_DUST, "paper", None, "context")
    struct, posts, feet, ground = _structure_world()
    add("Table purlins and rafters (galvanized steel)", struct, C_STEEL, "metal", None, "context")
    add("Table posts (galvanized steel)", posts, C_STEEL, "metal", None, "context", world=True)
    add("Post footings (concrete)", feet, C_CONC, "paper", None, "context", world=True)
    add("Ground patch (gravel)", ground, C_GROUND, "paper", None, "context", world=True)
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:66s} {q['group']:9s} {q['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.1f} cm3")
    print(f"{time.time() - t0:.1f} s")
