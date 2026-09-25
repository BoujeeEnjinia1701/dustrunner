"""DustRunner parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    dustrunner-robot.step / .stl       the robot (items 1 to 10 of bom/bom.csv)
    dustrunner-dock.step / .stl        clamp-on dock with panel, charger, contacts and anemometer (11 to 13, 16)
    dustrunner-end-stop.step / .stl    pair of clamp-on end stops (14)
    dustrunner-assembly.step           robot parked in the dock at the start of the row, with one
                                       reference module and an end stop (reference module not in the BOM)

Local table coordinates (mm), used for every part:
    X = u  along the row (direction of travel, away from the dock is +X)
    Y = v  up the slope, from the lower module edge (v = 0) to the upper edge (v = mod_l)
    Z = w  normal to the glass, glass surface at w = 0, frame top at w = frame_proud
The robot is centered at u = 0. Main dimensions and interfaces only (frame profile, wheel,
guide and hook roller contact lines, brush interference, beam, truck plates, enclosures,
dock rails that continue the frame profile). Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (DRN-CAL-001).
"""
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
    "shaft_d": 20.0,          # stub shafts into the truck bearings
    "brush_edge": 40.0,       # brushed band starts this far from each module edge
    "interference": 4.5,      # nominal pile interference at the bearings (R3: 3 to 5 mm along the sleeve)
    # hood (bent aluminum sheet over the brush, with end guards)
    "hood_r": 76.0, "hood_t": 0.8, "hood_clear": 25.0,   # hood lower edges this far above the brush axis
    # end trucks
    "plate_t": 5.0,           # 5 mm aluminum plate
    "plate_half_u": 130.0,    # plate 260 mm along the row
    "plate_w": (-56.0, 216.0),  # plate extent normal to the glass (under the frame to the beam top)
    "plate_gap": 22.0,        # plate inner face this far outboard of the frame outer face
    "wheel_d": 70.0, "wheel_w": 18.0,     # polyurethane wheels on the frame top flange
    "wheel_u": 90.0,          # wheel centers at +/- this along the row (wheelbase 180 mm)
    "wheel_v": (3.0, 21.0),   # wheel tread on the frame flange, from the frame outer face
    "guide_d": 22.0, "guide_u": 60.0,     # guide rollers on the frame outer face
    "hook_d": 16.0, "hook_v": (3.0, 21.0),  # hook roller under the frame bottom flange
    # drives
    "drive_d": 37.0, "drive_l": 66.0,     # 37 mm gearmotor with encoder
    "brush_motor": (70.0, 66.0, 70.0),    # brush gearmotor envelope (u, v, w)
    # enclosures on the beam
    "pack": (65.0, 151.0, 94.0),          # 12.8 V 10 Ah LiFePO4 (u, v, w), common 151 x 65 x 94 mm case
    "pack_v": 250.0,                      # pack lower end from the lower module edge
    "ebox": (80.0, 140.0, 55.0),          # IP65 controller box
    "ebox_v": 480.0,
    "shade_t": 1.0,                       # sunshade over pack and controller (part of the hood line)
    # dock (continues the frame profile past the row start)
    "dock_rail_l": 780.0,                 # parking rails
    "dock_u0": -1300.0,                   # far end of the dock (panel bay)
    "panel": (350.0, 530.0, 25.0),        # 20 W panel (u, v, w)
    "mast_h": 450.0,                      # anemometer mast above the dock plane
    # end stop
    "stop_l": 40.0, "stop_h": 50.0,
}

P = PARAMS


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
    d["beam_w"] = (d["brush_w"] + p["hood_r"] + p["hood_t"] + 3.0,
                   d["brush_w"] + p["hood_r"] + p["hood_t"] + 3.0 + p["beam_h"])
    d["plate_v"] = (-p["plate_gap"] - p["plate_t"], -p["plate_gap"])
    d["span"] = p["mod_l"] + 2 * p["plate_gap"]                # between plate inner faces
    d["beam_len"] = d["span"]
    d["overall_v"] = p["mod_l"] + 2 * (p["plate_gap"] + p["plate_t"]) + 2 * (p["drive_l"] + 12.0)
    d["overall_u"] = 2 * p["plate_half_u"] + 2 * 22.0        # plate plus IR sensors
    d["contact_w"] = 2 * ((p["brush_d"] / 2) ** 2 - d["brush_w"] ** 2) ** 0.5   # brush contact width on the glass
    d["top_w"] = d["beam_w"][1] + max(p["pack"][2], p["ebox"][2]) + 8.0
    return d


# ---------------- helpers ----------------
def bx(u0, u1, v0, v1, w0, w1):
    from build123d import Box, Pos
    return Pos((u0 + u1) / 2, (v0 + v1) / 2, (w0 + w1) / 2) * Box(abs(u1 - u0), abs(v1 - v0), abs(w1 - w0))


def cyl_v(u, w, v0, v1, r):
    from build123d import Cylinder, Pos, Rot
    return Pos(u, (v0 + v1) / 2, w) * Rot(90, 0, 0) * Cylinder(r, abs(v1 - v0))


def cyl_w(u, v, w0, w1, r):
    from build123d import Cylinder, Pos
    return Pos(u, v, (w0 + w1) / 2) * Cylinder(r, abs(w1 - w0))


def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def mirror_v(shape, p=PARAMS):
    """Mirror a lower-end shape to the upper module edge (v -> mod_l - v)."""
    from build123d import Plane, Pos
    return Pos(0, p["mod_l"], 0) * shape.mirror(Plane.XZ)


def frame_edge(u0, u1, p=PARAMS):
    """Module frame profile at the lower edge (C section open toward the glass): top flange,
    outer web and bottom flange. Used for the reference module and the dock rails."""
    top = p["frame_proud"]; bot = top - p["frame_d"]; t = p["frame_t"]
    return (bx(u0, u1, 0, p["lip"], top - t, top) + bx(u0, u1, 0, t, bot, top)
            + bx(u0, u1, 0, p["lip"], bot, bot + t))


# ---------------- robot ----------------
def robot_parts(p=PARAMS):
    """Robot parts in local coordinates, centered at u = 0. Keys match the BOM mapping in
    cad/src/concept_media.py; *_lo and *_hi are the lower and upper halves of paired items."""
    d = derived(p)
    pv0, pv1 = d["plate_v"]
    L = p["mod_l"]
    # 1 chassis beam, hollow rectangular tube spanning between the truck plates
    b, h, t = p["beam_b"], p["beam_h"], p["beam_t"]
    w0, w1 = d["beam_w"]
    beam = bx(-b / 2, b / 2, pv1, L - pv1, w0, w1) - bx(-b / 2 + t, b / 2 - t, pv1 - 1, L - pv1 + 1, w0 + t, w1 - t)
    # 2 brush: microfiber sleeve on a core tube, stub shafts through both plates
    bw = d["brush_w"]; v0, v1 = d["brush_v"]
    sleeve = cyl_v(0, bw, v0, v1, p["brush_d"] / 2) - cyl_v(0, bw, v0 - 1, v1 + 1, p["core_d"] / 2)
    core = cyl_v(0, bw, v0 - 10, v1 + 10, p["core_d"] / 2) - cyl_v(0, bw, v0 - 11, v1 + 11, p["core_d"] / 2 - p["core_t"])
    shafts = cyl_v(0, bw, pv0 - 6, v0 - 10, p["shaft_d"] / 2) + cyl_v(0, bw, v1 + 10, L - pv0 + 6, p["shaft_d"] / 2)
    brush = sleeve + core + shafts
    # 3 hood: part of a ring above the brush, with end guards and a sunshade over the enclosures
    r0, r1 = p["hood_r"], p["hood_r"] + p["hood_t"]
    ring = cyl_v(0, bw, v0 - 5, v1 + 5, r1) - cyl_v(0, bw, v0 - 6, v1 + 6, r0)
    hood = ring & bx(-r1 - 1, r1 + 1, v0 - 6, v1 + 6, bw + p["hood_clear"], bw + r1 + 1)
    guard = (cyl_v(0, bw, v0 - 6, v0 - 5, r1) & bx(-r1, r1, v0 - 7, v0 - 4, bw + p["hood_clear"], bw + r1))
    hood = hood + guard + mirror_v(guard, p)
    # 5 end trucks: plate, wheel axles, wheels, belt cover, hook arm (lower truck; upper is mirrored)
    hu = p["plate_half_u"]
    wc = d["wheel_c"]; wr = p["wheel_d"] / 2
    plate = bx(-hu, hu, pv0, pv1, *p["plate_w"])
    hook_arm = bx(-15, 15, pv0, p["hook_v"][1] + 3, p["plate_w"][0], d["hook_c"] - p["hook_d"] / 2 - 2)
    axles = cyl_v(-p["wheel_u"], wc, pv1, p["wheel_v"][0], 5) + cyl_v(p["wheel_u"], wc, pv1, p["wheel_v"][0], 5)
    wheels = cyl_v(-p["wheel_u"], wc, *p["wheel_v"], wr) + cyl_v(p["wheel_u"], wc, *p["wheel_v"], wr)
    belt_cover = bx(-p["wheel_u"] - 20, p["wheel_u"] + 20, pv0 - 12, pv0, wc - 20, wc + 8)
    contact_pad = bx(-hu - 8, -hu, pv0, pv1 + 40, 90, 130)      # robot-side charge contacts, facing the dock
    truck_lo = plate + hook_arm + axles + wheels + belt_cover + contact_pad
    # 7 rollers: guide rollers on the frame outer face, hook roller under the bottom flange
    gr = p["guide_d"] / 2
    guides = cyl_w(-p["guide_u"], -gr, -p["frame_d"] + 6, -4, gr) + cyl_w(p["guide_u"], -gr, -p["frame_d"] + 6, -4, gr)
    hook = cyl_v(0, d["hook_c"], *p["hook_v"], p["hook_d"] / 2)
    rollers_lo = guides + hook
    # 6 drive gearmotors, one per truck, outboard of the belt cover on the +u wheel axle
    drive_lo = cyl_v(p["wheel_u"], wc, pv0 - 12 - p["drive_l"], pv0 - 12, p["drive_d"] / 2)
    # 4 brush gearmotor and belt cover at the lower truck
    mu, mv, mw = p["brush_motor"]
    bm_w0 = wc + 16
    brush_motor = bx(-mu / 2, mu / 2, pv0 - 12 - mv, pv0 - 12, bm_w0 + 30, bm_w0 + 30 + mw) + \
        bx(-22, 22, pv0 - 12, pv0, bw - 10, bm_w0 + 30 + mw)
    # 10 IR edge sensors, two per truck, ahead of the wheels, looking down at the frame top flange
    def sensor(s):
        return bx(s * hu, s * (hu + 22), p["wheel_v"][0], p["wheel_v"][1], 45, 65) + \
            bx(s * hu, s * (hu + 22), pv0, p["wheel_v"][0], 55, 65)
    sens_lo = sensor(1) + sensor(-1)
    # 8 pack and 9 controller on top of the beam, lower end (short cable run to the brush motor)
    pu, pvl, pw = p["pack"]
    battery = bx(-pu / 2, pu / 2, p["pack_v"], p["pack_v"] + pvl, w1, w1 + pw)
    eu, evl, ew = p["ebox"]
    controller = bx(-eu / 2, eu / 2, p["ebox_v"], p["ebox_v"] + evl, w1, w1 + ew)
    shade = bx(-60, 60, p["pack_v"] - 20, p["ebox_v"] + evl + 20, w1 + pw + 6, w1 + pw + 6 + p["shade_t"])
    hood = hood + shade
    parts = dict(beam=beam, brush=brush, hood=hood, brush_motor=brush_motor,
                 trucks_lo=truck_lo, trucks_hi=mirror_v(truck_lo, p),
                 rollers_lo=rollers_lo, rollers_hi=mirror_v(rollers_lo, p),
                 drive_motors_lo=drive_lo, drive_motors_hi=mirror_v(drive_lo, p),
                 sensors_lo=sens_lo, sensors_hi=mirror_v(sens_lo, p),
                 battery=battery, controller=controller)
    for k in ("trucks", "rollers", "drive_motors", "sensors"):
        parts[k] = parts[k + "_lo"] + parts[k + "_hi"]
    return parts


ROBOT_KEYS = ["beam", "brush", "hood", "brush_motor", "trucks", "drive_motors", "rollers",
              "battery", "controller", "sensors"]


def robot(p=PARAMS, u=0.0):
    from build123d import Compound, Pos
    rp = robot_parts(p)
    return Compound(children=[Pos(u, 0, 0) * rp[k] for k in ROBOT_KEYS], label="DustRunner robot")


# ---------------- dock, end stop, reference module ----------------
def leg_local(u, v, w, p=PARAMS):
    """Vertical leg from a dock point (local u, v, w) to the ground, expressed in local coordinates."""
    t = radians(p["tilt"])
    height = p["h0"] + v * sin(t) + w * cos(t)
    end = (u, v - height * sin(t), w - height * cos(t))
    return tube((u, v, w), end, 20.0)


def dock_parts(p=PARAMS, legs=True):
    """Dock parts in local coordinates; legs=False leaves out the four legs (for exploded views)."""
    L = p["mod_l"]; u_end = -p["gap"]; u_rail = u_end - p["dock_rail_l"]; u0 = p["dock_u0"]
    rails = frame_edge(u_rail, u_end, p) + mirror_v(frame_edge(u_rail, u_end, p), p)
    bot = p["frame_proud"] - p["frame_d"]
    cross = None
    for uc in (u0, u_rail, u_end - 100):
        c = bx(uc, uc + 40, 30, L - 30, bot - 40, bot)
        cross = c if cross is None else cross + c
    posts = None
    for uc in (u_rail, u_end - 100):
        for vc in (5, L - 35):
            q = bx(uc, uc + 40, vc, vc + 30, bot - 40, bot)
            posts = q if posts is None else posts + q
    # two clamps onto the first module's bottom flange, and the panel bay side members
    clamps = bx(-p["gap"] - 10, 110, 30, 70, bot - 20, bot) + bx(-p["gap"] - 10, 110, L - 70, L - 30, bot - 20, bot)
    clamps = clamps + bx(60, 110, 30, 70, bot, bot + 12) + bx(60, 110, L - 70, L - 30, bot, bot + 12)
    bay = bx(u0, u_rail + 40, 90, 130, bot - 30, bot - 10) + bx(u0, u_rail + 40, 640, 680, bot - 30, bot - 10)
    leg_set = None
    for uc, vc in ((u_rail + 20, 300.0), (u0 + 20, 300.0), (u_rail + 20, L - 330.0), (u0 + 20, L - 330.0)):
        leg = leg_local(uc, vc, bot - 40, p)
        leg_set = leg if leg_set is None else leg_set + leg
    frame = rails + cross + posts + clamps + bay
    if legs:
        frame = frame + leg_set
    pu, pvl, pw = p["panel"]
    pc = (u0 + u_rail + 40) / 2
    panel = bx(pc - pu / 2, pc + pu / 2, 120, 120 + pvl, bot - 10, bot - 10 + pw)
    # charger box on the far cross member, spring contacts and latch at the parking position
    charge = bx(u0 + 40, u0 + 160, 760, 880, bot - 60, bot + 20) + \
        bx(u_rail + 40, u_rail + 60, -p["plate_gap"] - p["plate_t"] - 10, 40, 90, 130)
    # anemometer on a mast at the far cross member, upper end (clear of the robot and the panel)
    mv = L - 200
    mast = tube((u0 + 20, mv, bot), (u0 + 20, mv, bot + p["mast_h"]), 12.0)
    cups = cyl_w(u0 + 20, mv, bot + p["mast_h"], bot + p["mast_h"] + 40, 60.0)
    anemometer = mast + cups
    return dict(dock=frame, panel=panel, charge=charge, anemometer=anemometer)


def stop_parts(u_end, p=PARAMS):
    """Clamp-on end stop pair at the far end of the row (lower and upper frame)."""
    top = p["frame_proud"]; bot = top - p["frame_d"]
    lo = bx(u_end - p["stop_l"], u_end, 0, p["lip"], top, top + p["stop_h"]) + \
        bx(u_end - p["stop_l"], u_end, -12, 0, bot - 25, top + p["stop_h"]) + \
        bx(u_end - p["stop_l"], u_end, 0, p["lip"], bot - 25, bot)
    return lo + mirror_v(lo, p)


def reference_module(u0, p=PARAMS):
    """One reference module (frame ring and glass) starting at u0. Not in the BOM."""
    from build123d import Compound
    L, W = p["mod_l"], p["mod_w"]
    edges = frame_edge(u0, u0 + W, p) + mirror_v(frame_edge(u0, u0 + W, p), p)
    ends = bx(u0, u0 + p["lip"], 0, L, p["frame_proud"] - p["frame_d"], p["frame_proud"]) + \
        bx(u0 + W - p["lip"], u0 + W, 0, L, p["frame_proud"] - p["frame_d"], p["frame_proud"])
    glass = bx(u0 + p["lip"], u0 + W - p["lip"], p["lip"], L - p["lip"], -4.0, 0.0)
    return Compound(children=[edges + ends, glass], label="Reference module (not in BOM)")


def park_u(p=PARAMS):
    """Robot center when parked: truck contact pad against the dock contacts."""
    return -p["gap"] - p["dock_rail_l"] + 60 + 8 + p["plate_half_u"] + 2


def assembly(p=PARAMS):
    from build123d import Compound
    dp = dock_parts(p)
    u_stop = p["mod_w"]
    return Compound(children=[robot(p, park_u(p)), reference_module(0.0, p),
                              Compound(children=list(dp.values()), label="Dock"),
                              stop_parts(u_stop, p)], label="DustRunner assembly")


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    r = robot()
    dock = Compound(children=list(dock_parts().values()), label="Dock")
    stop = stop_parts(PARAMS["mod_w"])
    for name, shape in (("dustrunner-robot", r), ("dustrunner-dock", dock), ("dustrunner-end-stop", stop)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
    export_step(assembly(), str(root / "step" / "dustrunner-assembly.step"))
    bb = r.bounding_box()
    print(f"robot envelope {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (u x v x w)")
    print("exported STEP to cad/step and STL to cad/stl")
