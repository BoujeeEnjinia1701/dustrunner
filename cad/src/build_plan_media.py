"""DustRunner prototype build plan pictures (DRN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/DRN-DWG-101 to 119        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
Pictures are drawn in table coordinates with the table laid flat: the glass is horizontal, the row
runs left to right and "up the slope" runs into the picture. Uses .kit/build_views.py.
BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from math import radians, tan
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, derived, frame_edge, frame_end, mirror_v, bx,  # noqa: E402
                   park_u, to_world, fuse)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
C = build_components(P)
L = P["mod_l"]
S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"plate": "#475569", "wheel": "#0F766E", "bearing": "#9CA3AF", "housing": "#64748B", "motor": "#115E59",
       "guide": "#D4A017", "clevis": "#B45309", "hook": "#CA8A04", "slider": "#7C2D12", "spring": "#A16207",
       "sensor": "#0EA5E9", "sbrk": "#0369A1", "estop": "#DC2626", "contact": "#16A34A", "solenoid": "#15803D",
       "cleat": "#1D4ED8", "beam": "#64748B", "sleeve": "#14B8A6", "core": "#94A3B8", "shaft": "#334155",
       "hood": "#CBD5E1", "shade": "#E2E8F0", "post": "#6D28D9", "pack": "#C2410C", "ctrl": "#7C3AED",
       "rail": "#A16207", "cross": "#92400E", "rbrk": "#B45309", "spacer": "#F59E0B", "clamp": "#1E40AF",
       "jaw": "#3B82F6", "tie": "#78350F", "leg": "#854D0E", "panel": "#2563EB", "charger": "#16A34A",
       "dpost": "#065F46", "dcont": "#22C55E", "tab": "#14532D", "anem": "#DB2777", "stop": "#B91C1C",
       "buffer": "#111827", "frame": "#B8C0C8", "glass": "#1E3A8A", "bolt": "#111827"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def frame_stub(u0=-260.0, u1=260.0, both=False):
    s = frame_edge(u0, u1, P)
    return s + mirror_v(s, P) if both else s


def win(shape, u0, u1, v0, v1, w0, w1):
    return shape & bx(u0, u1, v0, v1, w0, w1)


LO = (-200, 200, -250, 260, -120, 340)          # window round the lower truck


def lo(k, name, color, explode=(0, 0, 0)):
    return part(name, win(C[k].shape, *LO), color, explode)


# ----------------------------------------------------------------- overview
BREAK = (640.0, L - 420.0)       # broken view: the long middle of the beam, brush, hood and dock members is left out


def broken(shape, gap=90.0):
    """Shorten a shape up the slope: keep v below BREAK[0] and above BREAK[1], close the middle to a gap."""
    from build123d import Pos
    a, b = BREAK
    lo_ = shape & bx(-5000, 5000, -500, a, -3000, 3000)
    hi_ = shape & bx(-5000, 5000, b, L + 500, -3000, 3000)
    out = []
    for s_, sh_ in ((lo_, 0.0), (hi_, -(b - a - gap))):
        try:
            if s_.volume > 1e-3:
                out.append(Pos(0, sh_, 0) * s_)
        except Exception:
            pass
    return fuse(out)


def _key_overview(items, out, title, subtitle, elev, azim, size=(12, 8), dpi=150, first=1):
    """Exploded view with numbered bubbles and a key, like build_views.overview(key=True), except that
    each item's bubble sits on its lower-end piece and a twin at the upper end is drawn unnumbered."""
    import matplotlib.pyplot as plt
    import numpy as np
    names = [n for n, *_ in items]
    longest = max(len(n) for n in names)
    kw = min(0.34, 0.05 + longest * 0.0105 * 8 / size[0])
    W, H = int(size[0] * dpi * (1 - kw)), int(size[1] * dpi * bv.PIC_HEIGHT)
    rows = []
    for n, num_shape, twin, col, ex in items:
        rows.append((part(n, num_shape, col), col, 1.0, ex))
        if twin is not None:
            rows.append((part(n, twin, col), col, 1.0, ex))
    img, proj, verts = bv._raster(rows, elev, azim, W, H)
    fig, ax = bv._frame(size, dpi, title, subtitle)
    ax.set_position([kw, bv.PIC_BOTTOM, 1 - kw, bv.PIC_HEIGHT])
    ax.imshow(img, interpolation="bilinear")
    k = 0
    for i, (n, num_shape, twin, col, ex) in enumerate(items):
        x, y = proj(bv._anchor(verts[k]))
        ax.text(x, y, str(first + i), fontsize=7.5, fontweight="bold", color="white", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.3", fc=bv.ACCENT, ec="white", lw=0.8))
        k += 2 if twin is not None else 1
    top = bv.PIC_BOTTOM + bv.PIC_HEIGHT - 0.02
    step_ = min(0.042, (bv.PIC_HEIGHT - 0.04) / max(len(items), 1))
    for i, (n, *_r) in enumerate(items):
        col = _r[2]
        yk = top - i * step_
        fig.text(0.025, yk, str(first + i), fontsize=7.5, fontweight="bold", color="white", ha="center", va="center",
                 bbox=dict(boxstyle="circle,pad=0.3", fc=bv.ACCENT, ec="white", lw=0.8))
        fig.patches.append(plt.Rectangle((0.042, yk - 0.008), 0.012, 0.016, transform=fig.transFigure, fc=col, ec=bv.INK, lw=0.5))
        fig.text(0.062, yk, n, fontsize=8, color=bv.INK, va="center")
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def overview():
    def pair(*ks, lower=True):
        a = fuse([C[k].shape for k in ks if not k.endswith("_hi")])
        b = fuse([C[k].shape for k in ks if k.endswith("_hi")])
        return a, b

    def lohi(shape):
        a = shape & bx(-5000, 5000, -600, L / 2, -3000, 3000)
        b = shape & bx(-5000, 5000, L / 2, L + 600, -3000, 3000)
        return a, b

    def it(name, ks=None, shape=None, col="#0F766E", ex=(0, 0, 0), split=True):
        sh = shape if shape is not None else fuse([C[k].shape for k in ks])
        if split:
            a, b = lohi(sh)
            try:
                if b.volume < 1e-3:
                    b = None
            except Exception:
                b = None
            try:
                if a.volume < 1e-3:
                    a, b = b, None
            except Exception:
                a, b = b, None
        else:
            a, b = sh, None
        return (name, broken(a), broken(b) if b is not None else None, col, ex)
    robot = [
        it("Truck plates (2)", ["plate_lo", "plate_hi"], col=COL["plate"]),
        it("Wheels, axles, flange bearings, belts", ["wheels_lo", "wheels_hi", "axles_lo", "axles_hi", "axle_bearings_lo", "axle_bearings_hi"], col=COL["wheel"], ex=(0, 0, -150)),
        it("Guide rollers in clevises (4)", ["guides_lo", "guides_hi", "clevises_lo", "clevises_hi"], col=COL["guide"], ex=(0, 0, -260)),
        it("Hook rollers on sprung sliders (2)", ["hook_lo", "hook_hi", "slider_lo", "slider_hi", "spring_lo", "spring_hi"], col=COL["slider"], ex=(0, 0, -380)),
        it("Brush flange bearings (2)", ["brush_bearings"], col=COL["bearing"], ex=(220, 0, 0)),
        it("IR sensors on brackets (4)", ["sensors_lo", "sensors_hi", "sensor_brackets_lo", "sensor_brackets_hi"], col=COL["sensor"], ex=(0, 0, 150)),
        it("Stop buttons (2)", ["estop_lo", "estop_hi"], col=COL["estop"], ex=(0, -60, 120)),
        it("Contact bracket, contact block, latch solenoid", ["contact_bracket", "contact_pad", "solenoid"], col=COL["contact"], ex=(-160, 0, 160)),
        it("Beam end cleats (4)", ["cleats_lo", "cleats_hi", "cleat_bolts_lo", "cleat_bolts_hi"], col=COL["cleat"], ex=(0, 0, 330)),
        it("Chassis beam", ["beam"], col=COL["beam"], ex=(0, 0, 480), split=False),
        it("Brush: sleeve, core, plugs, shafts", ["sleeve", "core", "plugs", "shafts"], col=COL["sleeve"], ex=(0, 0, 0), split=False),
        it("Drive housings and drive gearmotors", ["housing_lo", "housing_hi", "drive_lo", "drive_hi"], col=COL["housing"], ex=(0, 0, -560)),
        it("Brush gearmotor, pulleys and belt", ["brush_motor", "brush_drive"], col=COL["motor"], ex=(-260, 0, -560)),
        it("Hood and spacers", ["hood", "hood_spacers"], col=COL["hood"], ex=(0, 0, 230), split=False),
        it("LiFePO4 pack and straps", ["battery", "straps"], col=COL["pack"], ex=(0, 0, 640)),
        it("Controller box", ["controller"], col=COL["ctrl"], ex=(0, 0, 640)),
        it("Sunshade and posts", ["shade", "shade_posts"], col=COL["shade"], ex=(0, 0, 800)),
    ]
    a = _key_overview(robot, OUT / "overview.png", "DustRunner prototype: the robot, pulled apart",
                      "Numbered in build order. Broken view: the long middle of the beam, brush and hood is left out. "
                      "Table laid flat, seen from the front and above", elev=30, azim=-35)
    from build123d import Pos as _Pos

    def wit(name, ks, col, ex=(0, 0, 0), shift=0.0, split=False):
        sh = _Pos(shift, 0, 0) * fuse([C[k].shape for k in ks])
        if split:
            lo_ = to_world(sh & bx(-5000, 5000, -600, L / 2, -3000, 3000), P)
            hi_ = to_world(sh & bx(-5000, 5000, L / 2, L + 600, -3000, 3000), P)
            return (name, lo_, hi_, col, ex)
        return (name, to_world(sh, P), None, col, ex)
    dock = [
        wit("Dock cross members, legs and ties", ["cross", "legs", "ties"], COL["cross"]),
        wit("Frame clamps (2)", ["clamp_bars", "clamp_jaws"], COL["clamp"], ex=(0, 260, 0), split=True),
        wit("Dock rails with brackets, spacers, shims", ["rails", "rail_brackets", "spacers", "dock_bolts"], COL["rail"], ex=(0, 0, 260), split=True),
        wit("Dock PV panel", ["panel"], COL["panel"], ex=(0, 0, 300)),
        wit("Charger, contact post, contacts, latch tab", ["charger", "contact_post", "dock_contacts", "latch_tab"], COL["charger"], ex=(0, 0, 420)),
        wit("Anemometer, mast and clamps", ["anemometer", "mast_clamps"], COL["anem"], ex=(0, -250, 150)),
        wit("End stops (2), drawn beside the dock", ["stop_blocks", "stop_screws", "stop_buffers"], COL["stop"],
            shift=-P["mod_w"] + 700.0, split=True),
    ]
    b = _key_overview(dock, OUT / "overview-dock.png", "DustRunner prototype: the dock and end stops, pulled apart",
                      "Numbered on from the robot. Shown as installed, legs vertical, seen from the front left. The end stops are "
                      "drawn beside the dock; on the row they clamp to the last module", elev=22, azim=-40, first=len(robot) + 1)
    return [a, b]


# ----------------------------------------------------------------- making sketches
def sheets():
    from build123d import Pos, Rot
    base = dict(project="DustRunner", date=DATE)
    out = []
    fs = part("Module frame (reference)", frame_stub(), COL["frame"])
    pv0, pv1 = D["plate_v"]
    bw = D["brush_w"]

    def sheet(k, dwg, title, material, notes, neighbours, view_shape=None, inset=(24, -58), shape=None):
        sh = shape if shape is not None else C[k].shape
        out.append(bv.component_sheet(Part(title, sh, "#0F766E"), neighbours, dwg_no=dwg,
                                      title=f"DustRunner {title}: making sketch", material=material, notes=notes,
                                      view_shape=view_shape, inset_view=inset, **base))

    # 101 truck plate (lower; the upper is its mirror image)
    sheet("plate_lo", "DRN-DWG-101", "truck plate (make 2, a lower and an upper)", "Aluminium plate 5 mm, 5083 or 6082",
          ["Cut two blanks 260 x 296 mm. Heights below are up from the bottom edge;",
           "  'toward the row' and 'toward the dock' are along the 260 mm edge.",
           "Axle holes 12 mm, 90 each side of centre, 116 up.",
           "Lower plate only: brush shaft hole 22 mm on the centre line, 135.5 up.",
           "Stop button hole 22 mm, 95 toward the row, 265 up.",
           "Bearing bolt holes: drill through the bought flange bearings",
           "  once they are centred on the axle and brush holes.",
           "Hook slider: two 6.5 mm holes 13 each side of centre, 40 up.",
           "Cleat holes 6.5 mm, 37 each side of centre, 240 and 270 up.",
           "Housing flange, clevis, bracket and seat holes: drill through each",
           "  part in place, 3.3 mm, and tap M4 (marked from the part).",
           "The upper plate is the mirror image, without the brush hole.",
           "Deburr; round the corners 3 mm. Check: axle holes 180 apart."],
          [lo("wheels_lo", "", COL["wheel"]), lo("housing_lo", "", COL["housing"]), lo("clevises_lo", "", COL["clevis"]),
           lo("beam", "", COL["beam"]), fs], inset=(20, -120))
    # 102 drive housing (lower; upper is lower in height)
    sheet("housing_lo", "DRN-DWG-102", "drive housing (lower; the upper is 79 tall)",
          "Aluminium sheet 2 mm (lower), 1.5 mm (upper), 5052",
          ["A folded tray, open toward the plate: 236 long, 165 tall, 40 deep,",
           "  with a 12 mm flange on each end that screws to the plate.",
           "Mark the blank: back 236 x 165; top and bottom walls 40 deep;",
           "  end walls 40 deep plus the 12 mm flanges. Relief holes 3 mm at",
           "  each corner. Fold the walls 90 degrees, then the flanges outward.",
           "Drive motor: 8 mm shaft hole 90 toward the row, 41 up from the",
           "  bottom edge; motor screw holes from the motor's datasheet.",
           "Brush motor (lower only): 10 mm shaft hole on the centre line,",
           "  122 up; screw holes from its datasheet.",
           "Flanges: three 4.5 mm holes each, 6 from the outer edge.",
           "Upper housing: 79 tall, 1.5 mm sheet, drive motor hole only.",
           "Check: the tray sits flat on the plate all round its rim."],
          [lo("plate_lo", "", COL["plate"]), lo("drive_lo", "", COL["motor"]), lo("brush_motor", "", COL["motor"])],
          inset=(20, -130))
    # 103 guide roller clevis
    cl = C["clevises_lo"].shape & bx(30, 90, -40, 10, -40, 10)
    sheet(None, "DRN-DWG-103", "guide roller clevis (make 4)", "Aluminium sheet 3 mm, 5052",
          ["Cut a strip 22 wide x 69 long. Fold 90 degrees at 20 and 49 mm",
           "  to make a U: back 29 tall, two arms 20 deep.",
           "Drill one 8.5 mm hole through both arms, 17 from the outside",
           "  of the back, on the centre line (drill the arms together).",
           "Two 4.5 mm holes in the back, 8 from each end.",
           "Fit: back flat on the plate's inner face, 60 each side of",
           "  centre, from 50 to 79 up; M4 screws into the plate.",
           "The 22 x 23 mm roller goes between the arms on an M8 bolt,",
           "  head up, nyloc nut below.",
           "Check: the roller turns freely and stands 6 mm off the plate."],
          [lo("plate_lo", "", COL["plate"]), lo("guides_lo", "", COL["guide"]), lo("wheels_lo", "", COL["wheel"])], shape=cl, inset=(10, 70))
    # 104 hook slider and spring seat
    hs = S("slider_lo", "spring_lo")
    sheet(None, "DRN-DWG-104", "hook slider and spring seat (make 2 of each)", "Aluminium plate 10 mm (slider), sheet 3 mm (seat)",
          ["Slider: 40 x 30 mm from 10 mm plate.",
           "  8 mm reamed hole on the centre line, 15 up from the bottom.",
           "  Two slots 6.5 wide x 14 tall, 13 each side of centre,",
           "  centred 15 up: chain drill and file.",
           "Axle: 8 mm silver-steel rod 51 long, pressed 10 mm into the",
           "  slider with retaining compound; e-clip groove at the far end.",
           "Seat: 3 mm sheet 30 wide, folded to an angle with an 18 mm",
           "  leg on the plate and a 9 mm shelf; two 4.5 mm holes.",
           "Fit: slider on two M6 shoulder bolts through the plate,",
           "  free to slide up and down; spring between seat and slider.",
           "Spring: about 9 mm across, 60 N at 20 mm long (about 3 N/mm).",
           "Check: the slider moves 8 mm by hand without binding."],
          [lo("plate_lo", "", COL["plate"]), lo("hook_lo", "", COL["hook"]), lo("wheels_lo", "", COL["wheel"])], shape=hs, inset=(5, 70))
    # 105 sensor bracket
    sb = C["sensor_brackets_lo"].shape & bx(100, 200, -50, 40, 40, 100)
    sheet(None, "DRN-DWG-105", "IR sensor bracket (make 4)", "Aluminium sheet 3 mm, 5052",
          ["Cut a blank: a top 40 x 49 mm with an 18 x 23 mm tab on one",
           "  long edge, at the end nearest the plate centre.",
           "Fold the tab down 90 degrees.",
           "Tab: two 4.5 mm holes, 9 apart up and down, on its centre line.",
           "Top: holes for the sensor's own screws at the outer end,",
           "  so the sensor hangs over the frame flange, 3 to 21 from",
           "  the frame's outer face.",
           "Make two right-hand and two left-hand (mirror) brackets.",
           "Fit: tab on the plate's inner face at its end, 140 to 158 up;",
           "  the sensor lens 44 mm above the frame top.",
           "Check: the top clears the wheel by at least 5 mm."],
          [lo("plate_lo", "", COL["plate"]), lo("sensors_lo", "", COL["sensor"]), lo("wheels_lo", "", COL["wheel"]), fs],
          shape=sb, inset=(25, 50))
    # 106 contact bracket
    sheet("contact_bracket", "DRN-DWG-106", "contact and latch bracket (make 1)", "Aluminium sheet 3 mm, 5052",
          ["One blank, folded twice: a 27 x 62 mm leg that screws to the",
           "  plate; a 46 x 38 mm wing folded 90 degrees at the dock end;",
           "  a 27 x 30 mm shelf folded 90 degrees at the top.",
           "Leg: two 4.5 mm holes, 13 in from the dock end, 12 and 52 up.",
           "Wing: holes for the robot contact block (three copper strips",
           "  on an 8 mm insulating block) on its dock-facing side.",
           "Shelf: 7 mm hole for the latch pin, 15 from the dock end,",
           "  17 in from the plate; solenoid screw holes from its datasheet.",
           "Fit: on the lower plate's inner face at the dock end,",
           "  168 to 230 up.",
           "Check: the pin drops through the shelf without rubbing."],
          [part("", win(S("plate_lo", "contact_pad", "solenoid"), -170, -50, -60, 60, 50, 210), COL["plate"])],
          inset=(25, 120))
    # 107 beam
    sheet("beam", "DRN-DWG-107", "chassis beam (make 1)", "Aluminium rectangular tube 40 x 80 x 2 mm, 6063-T6",
          ["Cut 2,334 mm long, ends square (the module length plus 56).",
           "  For another module length, cut to that length plus 56.",
           "Ends: two 6.5 mm holes across both side walls, 17 from each",
           "  end, 25 and 55 up from the bottom face (for the cleat bolts).",
           "Bottom face: five M5 rivet nuts on the centre line, 328, 788,",
           "  1,167, 1,546 and 2,006 from the lower end (hood spacers).",
           "Top face: four M5 rivet nuts 12 each side of the centre line,",
           "  266 and 660 from the lower end (sunshade posts).",
           "Top face: holes for the controller box screws, 523 and 633",
           "  from the lower end, to suit the box.",
           "The 80 mm side stands normal to the glass.",
           "Check: length within 1 mm; end holes square across."],
          [part("", S("plate_lo", "plate_hi"), COL["plate"]), part("", S("hood"), COL["hood"])],
          view_shape=Rot(0, 0, 90) * C["beam"].shape, inset=(25, -60))
    # 108 beam end cleat
    cle = C["cleats_lo"].shape & bx(0, 100, -40, 20, 100, 260)
    sheet(None, "DRN-DWG-108", "beam end cleat (make 4)", "Aluminium equal angle 30 x 30 x 3 mm",
          ["Cut four 70 mm lengths; deburr.",
           "Leg on the beam: two 6.5 mm holes, 17 from the face that sits",
           "  on the plate, 20 and 50 from the bottom end.",
           "Leg on the plate: two 6.5 mm holes, 17 from the corner",
           "  (outside), 20 and 50 from the bottom end.",
           "Drill each pair of cleats together so the holes match.",
           "Fit: one cleat each side of each beam end; one M6 bolt",
           "  across the beam through both cleats at each hole, and",
           "  two M6 bolts through each cleat into the plate.",
           "Check: the beam end sits square and tight on the plate."],
          [lo("plate_lo", "", COL["plate"]), lo("beam", "", COL["beam"])], shape=cle, inset=(25, 50))
    # 109 brush core with plugs and shafts
    br = S("core", "plugs", "shafts")
    sheet(None, "DRN-DWG-109", "brush core, end plugs and stub shafts", "Aluminium tube 50 x 2 mm; aluminium bar 50 mm; steel bar 20 mm",
          ["Core: cut 2,218 mm of 50 x 2 tube; ends square, deburred.",
           "Plugs (2): turn 46 mm outside, 20 long, 20 mm bore, from",
           "  50 mm bar; press into each core end flush, retaining compound",
           "  and two M5 screws through the tube into each plug.",
           "Upper shaft: 20 mm steel, 76 long; 20 into the upper plug.",
           "Lower shaft: 120 long, 20 mm for 83 (20 in the plug), then",
           "  15 mm for 37 at the outer end, with a 5 mm key flat.",
           "Press both shafts into the plugs with retaining compound.",
           "Slide on the microfiber sleeve (2,198 long), 10 in from each",
           "  core end; a hose clip on each end holds it.",
           "Check: spin it between centres: run-out under 1 mm."],
          [lo("brush_bearings", "", COL["bearing"]), lo("plate_lo", "", COL["plate"]), lo("sleeve", "", COL["sleeve"])],
          view_shape=Rot(0, 0, 90) * br, shape=win(br, *LO), inset=(20, -130))
    # 110 hood
    hd = C["hood"].shape
    sheet("hood", "DRN-DWG-110", "brush hood (make 1)", "Aluminium sheet 0.8 mm, 5052; end guards 1 mm",
          ["Hood: a strip 189 wide x 2,208 long, rolled to a 76 mm inside",
           "  radius so it covers 142 degrees of the brush (a sheet-metal",
           "  shop's slip roll, or bend round a 150 mm pipe).",
           "Its edges sit 25 above the brush axis; the top is on the",
           "  centre line, 3 mm below the beam.",
           "End guards (2): 1 mm sheet, the shape of the hood's end",
           "  (145 wide, 52 tall), with folded tabs riveted inside the",
           "  hood, 5 in from each end.",
           "Five 5.5 mm holes along the top centre line at the spacer",
           "  positions of the beam (from DRN-DWG-107).",
           "Fit: M5 screws through the hood and 3 mm spacers into the",
           "  rivet nuts in the beam's bottom face.",
           "Check: 16 mm clear of the brush all along."],
          [part("", S("beam"), COL["beam"]), part("", S("sleeve"), COL["sleeve"])],
          view_shape=Rot(0, 0, 90) * hd, inset=(25, -60))
    # 111 sunshade and posts
    sh = S("shade", "shade_posts")
    sheet(None, "DRN-DWG-111", "sunshade and posts", "Aluminium sheet 1 mm, white; aluminium tube 12 x 3 mm",
          ["Sunshade: 120 x 410 mm from 1 mm sheet, corners rounded.",
           "  Four 5.5 mm holes, 12 each side of the centre line, 8 in",
           "  from each short end.",
           "Posts (4): 12 mm tube, 100 long, ends square.",
           "Fit: an M5 screw 120 long through the shade and each post into",
           "  the rivet nuts in the beam's top face.",
           "The shade stands 6 mm above the pack, so air moves under it.",
           "Check: the shade is level and clears the pack and box."],
          [part("", win(S("beam"), -100, 100, 150, 750, 0, 400), COL["beam"]), part("", S("battery", "controller"), COL["pack"])],
          shape=sh, inset=(25, -60))
    # 112 dock rail
    rl = C["rails"].shape & bx(-900, 0, -10, 40, -50, 10)
    sheet(None, "DRN-DWG-112", "dock rail (make 2)", "Aluminium channel 33 x 25 x 2.5 mm, or a module frame offcut",
          ["Cut two 780 mm lengths of channel with the same outside size",
           "  as the module frame: 33 deep, a 25 mm top flange.",
           "File both ends square; chamfer the row end of the top and",
           "  bottom flanges 1 mm so the wheels and hook rollers roll on.",
           "Web: two pairs of countersunk 5.5 mm holes for the rail",
           "  brackets, 20 and 700 from the outer (dock) end, 11 and",
           "  21 down from the top. Heads must sit flush: the guide",
           "  rollers run over them.",
           "The upper rail is the mirror image (holes the same).",
           "Check: the top flange is straight within 1 mm."],
          [part("", S("rail_brackets", "spacers") & bx(-900, 0, -10, 80, -100, 10), COL["rbrk"]),
           part("", S("cross") & bx(-900, 0, -10, 300, -100, 10), COL["cross"])],
          shape=rl, inset=(30, -60))
    # 113 cross member
    cm = C["cross"].shape & bx(-140, -70, -100, 3000, -200, 200)
    sheet(None, "DRN-DWG-113", "dock cross member (make 3)", "Aluminium square tube 40 x 40 x 2 mm, 6063",
          ["Cut three 2,218 mm lengths (module length less 60).",
           "All three: 8.5 mm holes top to bottom on the centre line, 20",
           "  from each end (rail bracket and clamp bolts).",
           "Far and rail-start members: two 8.5 mm holes across, 10 below",
           "  the top and 10 above the bottom, 270 and 1,918 from the",
           "  lower end (legs).",
           "Far and rail-start members: 6.5 mm holes top to bottom, 100,",
           "  600 and 2,138 from the lower end (ties).",
           "Far member: holes for the charger box and the mast U-bolts.",
           "Rail-start member: two 6.5 mm holes across, 30 from the lower",
           "  end, for the contact post.",
           "Check: the three are the same length within 1 mm."],
          [part("", S("clamp_bars", "rails", "rail_brackets"), COL["clamp"])],
          view_shape=Rot(0, 0, 90) * cm, shape=cm, inset=(30, -60))
    # 114 rail bracket and spacers
    rb = (C["rail_brackets"].shape & bx(-900, -700, -10, 80, -50, 10))
    sheet(None, "DRN-DWG-114", "rail bracket (make 4), spacer and shim", "Aluminium sheet 4 mm, 5083; plate 8.5 mm; sheet 2.5 mm",
          ["Bracket: 4 mm sheet 40 wide, folded 90 degrees to an L: a",
           "  67.5 mm foot and a 21 mm upright.",
           "Foot: one 8.5 mm hole on the centre line, 47.5 from the",
           "  outside of the upright.",
           "Upright: two M5 tapped holes on the centre line, 10 and 20 up",
           "  from the foot, matching the rail web holes.",
           "Spacer (rail-start member, 2): 40 x 40 x 8.5, 8.5 mm hole.",
           "Shim (near member, 2): 40 x 40 x 2.5, 8.5 mm hole.",
           "Fit: the upright inside the rail against its web, the foot",
           "  on the rail's bottom flange and on the spacer or shim.",
           "Check: the rail top lines up with the module frame top."],
          [part("", S("rails") & bx(-850, -650, -10, 40, -50, 10), COL["rail"]),
           part("", S("cross", "spacers") & bx(-850, -650, -10, 120, -100, 10), COL["cross"])], shape=rb, inset=(30, -40))
    # 115 frame clamp
    fc = S("clamp_bars", "clamp_jaws") & bx(-150, 60, 0, 100, -60, 0)
    sheet(None, "DRN-DWG-115", "frame clamp (make 2)", "Aluminium flat bar 40 x 6 mm; sheet 2.5 mm",
          ["Clamp bar: 40 x 6 flat bar, 165 long.",
           "  8.5 mm holes on the centre line, 20 from the dock end",
           "  and 7.5 from the module end.",
           "Jaw: 40 x 40 from 6 mm bar; 8.5 mm hole 32.5 from its inner",
           "  end. Spacer: 15 x 40 from 2.5 mm sheet, same hole.",
           "Fit: the bar under the first module's long-side frame flange,",
           "  the jaw on top of the flange inside the frame, the spacer",
           "  beside the flange edge; one M8 bolt pulls them together.",
           "The dock end of the bar bolts down onto the near cross member.",
           "No drilling of the module.",
           "Check: the clamp cannot slide when pushed by hand."],
          [part("", frame_end(0, 1, P) & bx(-10, 60, 0, 120, -50, 10), COL["frame"]),
           part("", S("cross") & bx(-150, -60, 0, 120, -100, 0), COL["cross"])], shape=fc, inset=(20, -130))
    # 116 tie
    ti = C["ties"].shape & bx(-1400, -700, 100, 160, -100, 0)
    sheet(None, "DRN-DWG-116", "dock tie (make 3)", "Aluminium rectangular tube 40 x 20 x 2 mm, 6063",
          ["Cut three 540 mm lengths.",
           "6.5 mm holes top to bottom on the centre line, 20 from each",
           "  end, to bolt onto the far and rail-start cross members.",
           "Two of them carry the dock panel: drill 6.5 mm holes",
           "  to match the panel frame's mounting holes.",
           "Fit: lying flat (40 wide) on top of the cross members, 110,",
           "  610 and 2,148 up the slope from the lower module edge.",
           "Check: both panel ties are parallel within 1 mm."],
          [part("", S("cross") & bx(-1400, -700, 0, 700, -200, 50), COL["cross"]), part("", S("panel"), COL["panel"])],
          view_shape=ti, shape=ti, inset=(30, -60))
    # 117 leg
    lg = to_world(C["legs"].shape, P)
    one = [s for s in lg.solids() if s.bounding_box().max.Z > 1000][0]
    bb = one.bounding_box()
    th = 40 * tan(radians(P["tilt"]))
    sheet(None, "DRN-DWG-117", "dock leg with foot plate (make 4)", "Aluminium square tube 40 x 40 x 2 mm; plate 6 mm",
          [f"Upper legs (2): {bb.max.Z - 6:.0f} mm on the long side, {bb.max.Z - 6 - th:.0f} on the short side;",
           "  the top is cut at 25 degrees to sit flush with the top of",
           "  the cross member. Lower legs (2): about 700 and 681.",
           "These lengths are for a lower glass edge 600 above level",
           "  ground: on site, cut to suit so the rails line up with",
           "  the module frames.",
           "Two 8.5 mm holes across, to match the cross member.",
           "Foot plate 100 x 100 x 6: the leg stands on it; join with an",
           "  angle cleat and M6 bolts, or weld. Two 10 mm holes for",
           "  ground anchors.",
           "Fit: vertical, beside the cross member's outer face.",
           "Check: plumb within 1 degree."],
          [part("", to_world(S("cross", "ties", "rails"), P), COL["cross"])], view_shape=Pos(-bb.center().X, -bb.center().Y, 0) * one,
          shape=lg, inset=(20, -40))
    # 118 contact post, dock contact block and latch tab
    cp = S("contact_post", "dock_contacts", "latch_tab")
    sheet(None, "DRN-DWG-118", "contact post, dock contacts and latch tab", "Aluminium tube 40 x 20 x 2; insulating block; plate 6 mm",
          ["Post: 40 x 20 tube, 206 long; two 6.5 mm holes across at the",
           "  bottom to bolt to the rail-start cross member's row side.",
           "Contact block: 20 x 77 x 38 from HDPE or PTFE, holding the",
           "  three spring contacts (charge +, charge -, anemometer),",
           "  screwed to the post's lower-edge side at the top.",
           "Latch tab: 6 mm plate 65 x 30; 7 mm hole 45 from the block",
           "  end; chamfer the free end's underside 45 degrees so the",
           "  robot's pin rides up onto it. Screwed on top of the block.",
           "Fit: the contact faces stand 2 mm from the robot's contact",
           "  block when the robot is parked; the pin drops through",
           "  the hole.",
           "Check: each spring contact moves 3 mm freely."],
          [part("", S("cross") & bx(-850, -700, -50, 200, -100, 0), COL["cross"]),
           part("", C["rails"].shape & bx(-850, -650, -10, 40, -50, 10), COL["rail"])], shape=cp, inset=(25, -40))
    # 119 end stop
    es = S("stop_blocks", "stop_screws", "stop_buffers") & bx(1000, 1200, -50, 60, -80, 80)
    sheet(None, "DRN-DWG-119", "end stop (make 2)", "Aluminium bar 40 x 25 and 40 x 12 mm; rubber 5 mm",
          ["Top block: 40 x 25 x 39. Outer plate: 40 x 12 x 86.",
           "  Bottom jaw: 40 x 25 x 12.",
           "Screw the outer plate to the top block and the jaw with two",
           "  M6 screws each, leaving a 35 mm gap between block and jaw.",
           "Jaw: M8 tapped hole on its centre, 12.5 from the plate.",
           "Buffer: 5 mm rubber, 25 x 34, glued to the block's face",
           "  that faces the robot.",
           "Fit: slide over the last module's frame edge, top block on",
           "  the top flange, jaw under the bottom flange; tighten the",
           "  M8 clamp screw up against the flange.",
           "The top is 40 above the glass: the sensors pass over it and",
           "  the wheels meet the buffer.",
           "Check: it cannot be pulled along the frame by hand."],
          [part("", frame_edge(950, 1134, P) + frame_end(1134, -1, P) & bx(900, 1200, -20, 80, -40, 10), COL["frame"])],
          shape=es, inset=(25, -40))
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    fr = frame_stub(-300, 300)

    def J(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))
    # 1 wheel axle through the plate in two flange bearings, pulley and belt in the housing (cut through the +u axle)
    box = (40, 90, -150, 30, -10, 80)
    J(1, [part("Module frame (reference)", win(fr, *box), COL["frame"]),
          part("Truck plate", win(C["plate_lo"].shape, *box), COL["plate"]),
          part("Two flange bearings", win(C["axle_bearings_lo"].shape, *box), COL["bearing"]),
          part("Wheel", win(C["wheels_lo"].shape, *box), COL["wheel"]),
          part("Axle, pulley, belt, coupling", win(C["axles_lo"].shape, *box), COL["shaft"]),
          part("Drive housing", win(C["housing_lo"].shape, *box), COL["housing"]),
          part("Drive gearmotor", win(C["drive_lo"].shape, *box), COL["motor"])],
      "wheel axle in two flange bearings (lower truck, row end)", "Cut through the axle. One bearing each side of the plate; the motor drives the axle through a coupling",
      elev=18, azim=25, size=(8, 6))
    # 2 guide roller in its clevis on the frame face
    box = (25, 60, -45, 30, -45, 10)
    J(2, [part("Module frame (reference)", win(fr, *box), COL["frame"]),
          part("Truck plate", win(C["plate_lo"].shape, *box), COL["plate"]),
          part("Clevis", win(C["clevises_lo"].shape, *box), COL["clevis"]),
          part("Guide roller on an M8 bolt", win(C["guides_lo"].shape, *box), COL["guide"])],
      "guide roller in its clevis", "Cut through the roller. It bears on the frame's outer face and stands 6 mm off the plate",
      elev=20, azim=20, size=(8, 6))
    # 3 hook roller, slider and spring (cut on the centre line)
    box = (-35, 0, -40, 30, -85, 10)
    J(3, [part("Module frame (reference)", win(fr, *box), COL["frame"]),
          part("Truck plate", win(C["plate_lo"].shape, *box), COL["plate"]),
          part("Hook slider", win(C["slider_lo"].shape, *box), COL["slider"]),
          part("Hook roller and axle", win(C["hook_lo"].shape, *box), COL["hook"]),
          part("Spring and seat", win(C["spring_lo"].shape, *box), COL["spring"])],
      "hook roller under the frame flange", "Cut on the centre line. The spring pushes the slider up so the roller presses 60 N under the flange",
      elev=12, azim=20, size=(8, 6))
    # 4 beam end cleats
    box = (-70, 70, -40, 40, 130, 220)
    J(4, [part("Truck plate", win(C["plate_lo"].shape, *box), COL["plate"]),
          part("Beam", win(C["beam"].shape, *box), COL["beam"]),
          part("Cleats, one each side", win(C["cleats_lo"].shape, *box), COL["cleat"]),
          part("M6 bolts", win(C["cleat_bolts_lo"].shape, *box), COL["bolt"])],
      "beam end on the truck plate", "Seen from inside. Two bolts across the beam through both cleats; two bolts through each cleat into the plate",
      elev=25, azim=50, size=(8, 6))
    # 5 brush shaft: plug in the core, flange bearing, pulley in the housing (cut)
    box = (-60, 60, -80, 70, -10, 140)
    J(5, [part("Truck plate", win(C["plate_lo"].shape, *box), COL["plate"]),
          part("Brush flange bearing", win(C["brush_bearings"].shape, *box), COL["bearing"]),
          part("Stub shaft", win(C["shafts"].shape, *box), COL["shaft"]),
          part("Core end plug", win(C["plugs"].shape, *box), COL["core"]),
          part("Core tube", win(C["core"].shape, *box), "#64748B"),
          part("Microfiber sleeve", win(C["sleeve"].shape, *box), COL["sleeve"]),
          part("Brush pulley and belt", win(C["brush_drive"].shape, *box), COL["motor"]),
          part("Drive housing", win(C["housing_lo"].shape, *box), COL["housing"])],
      "brush shaft at the lower truck", "Cut through the brush axis. Plug pressed in the core; shaft in the flange bearing; pulley inside the housing",
      cut="-X", elev=15, azim=-20, size=(8, 6))
    # 6 hood spacer and sunshade post
    box = (-90, 90, 200, 330, 40, 330)
    J(6, [part("Beam", win(C["beam"].shape, *box), COL["beam"]),
          part("Hood", win(C["hood"].shape, *box), COL["hood"]),
          part("3 mm hood spacer", win(C["hood_spacers"].shape, *box), COL["post"]),
          part("Sleeve", win(C["sleeve"].shape, *box), COL["sleeve"]),
          part("Sunshade post", win(C["shade_posts"].shape, *box), COL["post"]),
          part("Sunshade", win(C["shade"].shape, *box), COL["shade"]),
          part("Pack and strap", win(S("battery", "straps"), *box), COL["pack"])],
      "hood and sunshade on the beam", "Cut across the beam. The hood hangs 3 mm below the beam; the shade stands 6 mm over the pack",
      cut="+X", elev=10, azim=-75, size=(8, 6))
    # 7 rail bracket on the rail-start cross member (cut through the bolt)
    u0 = D["cross_u"][1]
    box = (u0 - 10, u0 + 50, -15, 85, -85, 5)
    J(7, [part("Dock rail", win(C["rails"].shape, *box), COL["rail"]),
          part("Rail bracket", win(C["rail_brackets"].shape, *box), COL["rbrk"]),
          part("8.5 mm spacer", win(C["spacers"].shape, *box), COL["spacer"]),
          part("Cross member", win(C["cross"].shape, *box), COL["cross"]),
          part("M8 bolt", win(C["dock_bolts"].shape, *box), COL["bolt"])],
      "dock rail on its bracket", "Cut through the bolt. The bracket sits inside the rail; the cross member stays 6 mm below the rail, clear of the hook roller",
      cut="-X", elev=15, azim=-60, size=(8, 6))
    # 8 frame clamp on the first module
    un = D["cross_u"][2]
    box = (un - 10, 60, 10, 90, -85, 10)
    mod = frame_end(0, 1, P) + frame_edge(0, 200, P)
    J(8, [part("First module's frame (reference)", win(mod, *box), COL["frame"]),
          part("Clamp bar", win(C["clamp_bars"].shape, *box), COL["clamp"]),
          part("Jaw and spacer", win(C["clamp_jaws"].shape, *box), COL["jaw"]),
          part("Near cross member", win(C["cross"].shape, *box), COL["cross"]),
          part("Shim, rail bracket", win(S("spacers", "rail_brackets"), *box), COL["rbrk"]),
          part("M8 bolts", win(C["dock_bolts"].shape, *box), COL["bolt"])],
      "frame clamp on the first module", "Cut through the bolts. The jaw and bar grip the frame's bottom flange; nothing is drilled",
      cut="+Y", elev=12, azim=-90, size=(8, 6))
    # 9 dock contacts and latch, robot parked
    from build123d import Pos
    pu = park_u(P)
    ur = D["cross_u"][1]
    box = (ur, ur + 120, -50, 90, 60, 190)
    J(9, [part("Contact post", win(C["contact_post"].shape, *box), COL["dpost"]),
          part("Dock contact block", win(C["dock_contacts"].shape, *box), COL["dcont"]),
          part("Latch tab", win(C["latch_tab"].shape, *box), COL["tab"]),
          part("Robot contact block", win(Pos(pu, 0, 0) * C["contact_pad"].shape, *box), "#F59E0B"),
          part("Contact bracket (on the truck plate, not shown)", win(Pos(pu, 0, 0) * C["contact_bracket"].shape, *box), COL["sbrk"]),
          part("Latch solenoid and pin", win(Pos(pu, 0, 0) * C["solenoid"].shape, *box), "#7C3AED")],
      "dock contacts and latch, robot parked", "Seen from inside, truck plate left out. Contact blocks 2 mm apart (the springs close it); the pin drops through the tab",
      elev=30, azim=60, size=(8, 6))
    # 10 end stop with the wheel at the buffer
    us = P["mod_w"]
    uh = us - P["stop_l"] - P["buffer_t"] - P["wheel_u"] - P["wheel_d"] / 2
    box = (us - 120, us + 10, -50, 40, -70, 90)
    J(10, [part("Last module's frame (reference)", win(frame_edge(us - 300, us, P) + frame_end(us, -1, P), *box), COL["frame"]),
           part("End stop", win(C["stop_blocks"].shape, *box), COL["stop"]),
           part("Clamp screw", win(C["stop_screws"].shape, *box), COL["bolt"]),
           part("Rubber buffer", win(C["stop_buffers"].shape, *box), COL["buffer"]),
           part("Robot wheel at the buffer", win(Pos(uh, 0, 0) * C["wheels_lo"].shape, *box), COL["wheel"]),
           part("IR sensor, passing over", win(Pos(uh, 0, 0) * S("sensors_lo", "sensor_brackets_lo"), *box), COL["sensor"])],
       "end stop on the last module", "The stop clamps round the frame edge; the wheel meets the buffer and the sensor passes 5 mm over the stop",
       elev=20, azim=-60, size=(8, 6))
    # 11 leg on the cross member
    uf = D["cross_u"][0]
    from model import local_point_to_world
    from build123d import Box as _Box
    cx, cy, cz = local_point_to_world(uf - 20, 300.0, P["cross_top"] - 20, P)
    wbox = Pos(cx, cy, cz - 60) * _Box(260, 200, 260)
    J(11, [part("Far cross member", to_world(C["cross"].shape, P) & wbox, COL["cross"]),
           part("Leg (top cut at 25 degrees)", to_world(C["legs"].shape, P) & wbox, "#CA8A04")],
       "leg on the far cross member", "As installed. The leg stands vertical beside the cross member; two M8 bolts through both",
       elev=15, azim=-140, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    from build123d import Pos
    out = []

    import os
    only = {int(x) for x in os.environ.get("STEPS", "").split(",") if x}

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        if 4 <= n <= 8 or n == 15:           # long parts: broken view so the small parts stay readable
            done = [Part(p.name, broken(p.shape), p.color, None, p.explode, p.alpha) for p in done]
            new = [Part(p.name, broken(p.shape), p.color, None, p.explode, p.alpha) for p in new]
            sub = sub + " (broken view)"
        if n >= 9:                           # dock steps: drawn as installed, legs vertical
            from math import cos as _c, sin as _s
            t = radians(P["tilt"])

            def wv(e):
                du, dv, dw = e
                return (-(dv * _c(t) - dw * _s(t)), du, dv * _s(t) + dw * _c(t))
            done = [Part(p.name, to_world(p.shape, P), p.color, None, wv(p.explode), p.alpha) for p in done]
            new = [Part(p.name, to_world(p.shape, P), p.color, None, wv(p.explode), p.alpha) for p in new]
            if "context" in kw:
                kw["context"] = [Part(p.name, to_world(p.shape, P), p.color, None, (0, 0, 0), p.alpha) for p in kw["context"]]
            kw["azim"] = -28 if n == 9 else -40
            kw["elev"] = 22
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    fr = part("Module frame (reference)", win(frame_stub(-300, 300), *LO), COL["frame"])
    plate = lo("plate_lo", "Truck plate", COL["plate"])
    wheels = lo("wheels_lo", "Wheels", COL["wheel"])
    axle = part("Axle flange bearings, axles, pulleys, belt", win(S("axle_bearings_lo", "axles_lo"), *LO), COL["bearing"])
    st(1, [plate], [mv(axle, (0, 80, 0)), mv(wheels, (0, 160, 0))], "axles and wheels onto each truck plate",
       "Lower truck, seen from inside; the upper is its mirror. A bearing each side of the plate; pulleys and belt on the outside",
       elev=25, azim=55)
    rollers = part("Guide rollers in clevises", win(S("guides_lo", "clevises_lo"), *LO), COL["guide"])
    hook = part("Hook slider, roller, spring and seat", win(S("slider_lo", "hook_lo", "spring_lo"), *LO), COL["slider"])
    d1 = [plate, wheels, axle]
    st(2, d1, [mv(rollers, (0, 90, 0)), mv(hook, (0, 90, -60))], "guide and hook rollers onto each plate",
       "Seen from inside. Clevises with M4 screws; slider on two M6 shoulder bolts, spring under it; leave the springs slack",
       elev=25, azim=55, label_done=False)
    d2 = d1 + [rollers, hook]
    bb_ = part("Brush flange bearing", win(C["brush_bearings"].shape, *LO), COL["bearing"])
    sens = part("Sensors on brackets", win(S("sensors_lo", "sensor_brackets_lo"), *LO), COL["sensor"])
    es = part("Stop button", win(C["estop_lo"].shape, *LO), COL["estop"])
    cb = part("Contact bracket, contact block, latch solenoid", win(S("contact_bracket", "contact_pad", "solenoid"), *LO), COL["contact"])
    st(3, d2, [mv(bb_, (0, 90, 0)), mv(sens, (0, 90, 60)), mv(es, (0, -90, 0)), mv(cb, (-90, 60, 0))],
       "bearing, sensors, stop button and contact bracket",
       "Seen from inside. Brush bearing on the inner face; sensors at both ends; contact bracket on the lower plate only",
       elev=25, azim=55, label_done=False)
    truck_lo = d2 + [bb_, sens, es, cb]
    # whole robot
    TL = ["plate_lo", "wheels_lo", "axles_lo", "axle_bearings_lo", "guides_lo", "clevises_lo", "slider_lo", "hook_lo",
          "spring_lo", "sensors_lo", "sensor_brackets_lo", "estop_lo", "contact_bracket", "contact_pad", "solenoid"]
    TH = [k.replace("_lo", "_hi") for k in TL if k.endswith("_lo")]
    tlo = part("Lower truck", S(*TL) + (C["brush_bearings"].shape & bx(-200, 200, -100, 300, -200, 300)), COL["plate"])
    thi = part("Upper truck", S(*TH) + (C["brush_bearings"].shape & bx(-200, 200, L - 300, L + 100, -200, 300)), COL["plate"])
    beam = part("Beam with its four cleats", S("beam", "cleats_lo", "cleats_hi"), COL["beam"])
    st(4, [tlo], [mv(beam, (0, 0, 260))], "beam onto the lower truck",
       "Cleats bolted across the beam ends; two M6 bolts per lower cleat into the plate",
       elev=28, azim=-55)
    brush = part("Brush (core, plugs, shafts, sleeve)", S("sleeve", "core", "plugs", "shafts"), COL["sleeve"])
    st(5, [tlo, beam], [mv(brush, (0, 0, -200)), mv(thi, (0, 260, 0))], "brush, then the upper truck",
       "Lower shaft into its bearing; upper truck over the upper shaft, bolted to the cleats",
       elev=28, azim=-55, label_done=False)
    rb = [tlo, thi, beam, brush]
    drv = part("Drive housings, gearmotors, brush drive", S("housing_lo", "housing_hi", "drive_lo", "drive_hi", "brush_motor", "brush_drive"), COL["housing"])
    st(6, rb, [Part("Drive housing, gearmotor, brush pulleys and belt (lower)", S("housing_lo", "drive_lo", "brush_motor", "brush_drive"), COL["housing"], None, (0, -150, 0), 1.0),
               Part("Drive housing and gearmotor (upper)", S("housing_hi", "drive_hi"), COL["motor"], None, (0, 150, 0), 1.0)],
       "drive housings and motors", "Brush pulleys and belt first; each housing with its gearmotor screwed to the plate",
       elev=28, azim=-55, label_done=False)
    rb2 = rb + [drv]
    hood = part("Hood on five spacers", S("hood", "hood_spacers"), COL["hood"])
    st(7, rb2, [mv(hood, (-260, 0, 0))],
       "hood onto the beam", "Hood slid in from the side over the brush; M5 screws through spacers into the beam",
       elev=28, azim=-55, label_done=False)
    rb3 = rb2 + [hood]
    pk = part("Pack and straps", S("battery", "straps"), COL["pack"])
    ct = part("Controller box", S("controller"), COL["ctrl"])
    shd = part("Sunshade on its posts", S("shade", "shade_posts"), COL["shade"])
    st(8, rb3, [mv(pk, (0, 0, 200)), mv(ct, (0, 0, 200)), mv(shd, (0, 0, 380))], "pack, controller and sunshade",
       "Pack strapped to the beam, controller screwed on and wired; sunshade on four posts",
       elev=28, azim=-55, label_done=False)
    # dock
    dframe = part("Far and rail-start cross members, legs, ties", S("legs", "ties") + (C["cross"].shape & bx(-1400, -700, -100, 3000, -200, 200)), COL["cross"])
    st(9, [], [Part(dframe.name, dframe.shape, dframe.color, None, (0, 0, 0), 1.0)], "dock frame on the ground",
       "Legs bolted beside the two outer cross members; ties bolted on top. Set the legs plumb",
       elev=28, azim=-55)
    mod = part("First module (reference)", frame_edge(0, 400, P) + mirror_v(frame_edge(0, 400, P), P) + frame_end(0, 1, P), COL["frame"])
    near = part("Near cross member with the two frame clamps", (C["cross"].shape & bx(-200, -60, -100, 3000, -200, 200)) + S("clamp_bars", "clamp_jaws"), COL["clamp"])
    st(10, [dframe], [mv(near, (0, 0, -200))], "near cross member and frame clamps",
       "Clamp bars under the first module's long-side frame flange, jaws inside the frame; one M8 bolt each",
       context=[mod], elev=28, azim=-55, label_done=False)
    rails = part("Rails with brackets, spacers and shims", S("rails", "rail_brackets", "spacers", "dock_bolts"), COL["rail"])
    st(11, [dframe, near], [mv(rails, (0, 0, 200))], "dock rails onto the cross members",
       "Brackets screwed inside the rails; M8 bolts through brackets, spacers and members. Shim until the rails meet the frames",
       context=[mod], elev=28, azim=-55, label_done=False)
    dock_done = [dframe, near, rails]
    pc = part("Dock panel and charger box", S("panel", "charger"), COL["panel"])
    st(12, dock_done, [mv(pc, (0, 0, 200))], "panel and charger",
       "Panel bolted to two ties through its frame holes; charger box screwed to the far cross member",
       context=[mod], elev=28, azim=-55, label_done=False)
    robot = part("Robot", fuse([C[k].shape for k, c in C.items() if c.group in
                                ("beam", "brush", "hood", "brush_motor", "trucks", "drive_motors", "rollers", "battery", "controller", "sensors", "fittings")]), COL["sleeve"])
    from build123d import Pos as _P
    pu = park_u(P)
    rob_parked = Part("Robot, slid onto the rails from the dock's outer end", _P(pu, 0, 0) * robot.shape, COL["sleeve"], None, (-900, 0, 0), 1.0)
    st(13, dock_done + [pc], [rob_parked], "robot onto the dock rails",
       "Two people. Wheels on the rail tops, hook rollers under the bottom flanges, guide rollers on the webs. Then set the hook springs",
       context=[mod], elev=28, azim=-55, label_done=False)
    rob_in = part("Robot", _P(pu, 0, 0) * robot.shape, COL["sleeve"])
    cont = part("Contact post, dock contacts and latch tab", S("contact_post", "dock_contacts", "latch_tab"), COL["dcont"])
    an = part("Anemometer mast in two U-bolt clamps", S("anemometer", "mast_clamps"), COL["anem"])
    st(14, dock_done + [pc, rob_in], [mv(cont, (0, 0, 200)), mv(an, (-200, 0, 0))], "contacts, latch tab and anemometer",
       "Post bolted to the rail-start member; contact block and latch tab on it; mast vertical in its clamps on the far member",
       context=[mod], elev=28, azim=-55, label_done=False)
    us = P["mod_w"]
    last = part("Last module (reference)", frame_edge(us - 400, us, P) + mirror_v(frame_edge(us - 400, us, P), P) + frame_end(us, -1, P), COL["frame"])
    stops = part("End stops", S("stop_blocks", "stop_screws", "stop_buffers"), COL["stop"])
    st(15, [last], [mv(stops, (200, 0, 0))], "end stops onto the last module",
       "Slide each stop over the frame edge at the row end; tighten the M8 clamp screw against the flange",
       elev=28, azim=-55, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "DustRunner prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Robot (left) and dock (right). Bought modules wired at block level; no circuit board is laid out. "
            "Stranded copper; ferrules on every screw terminal.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/dustrunner", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((2, 8), 78, 54, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(3.5, 60.8, "On the robot", fontsize=8, color=MUT, va="top")
    ax.add_patch(FancyBboxPatch((86, 8), 32, 54, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(87.5, 60.8, "In the dock", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=6.9, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=6.9, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(5, 44, 15, 12, "LiFePO4 pack", "12.8 V 10 Ah,\nBMS inside", "#C2410C")
    blk(25, 44, 14, 12, "15 A fuse and\nmain switch", "at the pack lead", "#B91C1C")
    blk(44, 44, 16, 12, "Stop buttons", "two, one per truck,\nin series, latching", "#DC2626")
    blk(64, 44, 13, 12, "Power bus", "terminal block,\n12.8 V", "#16A34A")
    blk(5, 26, 17, 12, "Controller", "ESP32 class, humidity\nand temperature", "#7C3AED")
    blk(25, 26, 17, 12, "Motor drivers", "two drive channels\nand brush driver", "#16A34A")
    blk(46, 26, 15, 12, "Motors", "two drive gearmotors\nwith encoders, brush", "#115E59")
    blk(64, 26, 13, 12, "Latch solenoid", "12 V pull,\nspring return", "#15803D")
    blk(5, 11, 17, 10, "IR sensors (4)", "two per truck", "#0EA5E9")
    blk(46, 11, 31, 10, "Robot contact block", "charge +, charge -, anemometer", "#16A34A")
    blk(90, 44, 25, 12, "Dock panel", "20 W", "#2563EB")
    blk(90, 28, 25, 12, "Charge controller", "LiFePO4, about 5 A,\n14.4 V charge limit", "#16A34A")
    blk(90, 11, 25, 12, "Dock contact block", "three spring contacts;\nanemometer pulse", "#22C55E")
    wire([(20, 50), (25, 50)], RED); lab(22.5, 52.6, "2.5 mm²", RED, "center")
    wire([(39, 50), (44, 50)], RED); lab(41.5, 52.6, "2.5 mm²", RED, "center")
    wire([(60, 50), (64, 50)], RED); lab(62, 52.6, "2.5 mm²", RED, "center")
    wire([(70.5, 44), (70.5, 38)], RED); lab(71.2, 41, "1.0 mm²", RED)
    wire([(66, 44), (66, 41), (33.5, 41), (33.5, 38)], RED); lab(48, 42.4, "drivers 1.5 mm²", RED, "center")
    wire([(13.5, 41), (13.5, 38)], RED); wire([(33.5, 41), (13.5, 41)], RED); lab(15, 39.4, "0.5 mm²", RED)
    wire([(42, 32), (46, 32)], RED); lab(44, 34.4, "1.5 mm²", RED, "center")
    wire([(22, 30), (25, 30)], BLU); lab(23.5, 32.2, "PWM", BLU, "center")
    wire([(13.5, 26), (13.5, 21)], BLU); lab(14.2, 23.5, "0.25 mm²", BLU)
    wire([(22, 34.5), (24, 34.5), (24, 39.5), (62.5, 39.5), (62.5, 35), (64, 35)], GRY, 1.2); lab(55, 39.5, "solenoid enable", GRY, "center")
    wire([(50, 26), (50, 23.5), (23.3, 23.5), (23.3, 28), (22, 28)], BLU); lab(37, 23.5, "encoders to controller", BLU, "center")
    wire([(77, 16), (90, 16)], RED); lab(83.5, 18.2, "charge, when parked", RED, "center")
    wire([(77, 14), (90, 14)], BLU, 1.2); lab(83.5, 12, "anemometer pulse", BLU, "center")
    wire([(102.5, 44), (102.5, 40)], RED); lab(103.2, 42, "1.5 mm²", RED)
    wire([(102.5, 28), (102.5, 23)], RED); lab(103.2, 25.5, "1.5 mm²", RED)
    wire([(46, 14), (40, 14), (40, 9.6), (3.5, 9.6), (3.5, 50), (5, 50)], RED); lab(30, 9.6, "charge in, to the pack's BMS charge port", RED, "center")
    ax.text(3, 5.6, "Safety: fit the fuse last and only after the checks of section 6; never charge below 0 °C or above 45 °C. "
            "All circuits are extra-low voltage (12.8 V pack, about 22 V from the dock panel).", fontsize=7.4, color="#B45309", fontweight="bold")
    ax.text(3, 3.3, "Red: power. Blue: signal. Grey: control. The anemometer cups and mast are wired to the dock contact block, "
            "read by the robot through the third contact.", fontsize=7, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
