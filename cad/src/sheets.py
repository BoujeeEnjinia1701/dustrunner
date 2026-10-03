"""DustRunner general arrangement sheet DRN-DWG-001, Rev P4 (TRL 3, constructable design of DRN-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/DRN-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept sheet in media/ is DRN-DWG-010.

Sheet axes: X up the slope (model v), Y across the robot (model -u), Z normal to the glass
(model w). Short stubs of the reference module frame (not in the BOM) show the interface.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, derived, robot, frame_edge, mirror_v  # noqa: E402

DATE = "2026-09-25"
DATE3 = "2026-09-30"
DATE4 = "2026-10-02"
STUB = 150.0      # half length of the reference frame stubs along the row


def safe_project_views(part, workdir, line_weight=0.35, hidden_right=True):
    """drawing.project_views, edge by edge, skipping degenerate edges from the hidden-line projection."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if (name == "right" and hidden_right) else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def ortho_cells(sheet, views, names=("front", "top")):
    """Repeat Sheet.add_ortho's layout arithmetic (front and top only) to find where each view lands."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]
    k = sheet.scale
    ax += (aw - (k * max(fw, tw) + gap)) / 2
    ay += (ah - (k * (th + fh) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, k * fh)}


def dim_h(x1, x2, y, text, above=True):
    a = 1.4
    ty = y - 1.0 if above else y + 3.2
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, ty, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, left=True):
    a = 1.4
    cx, cy = (x - 1.0 if left else x + 3.0), (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    from build123d import Box, Compound, Pos, Rot
    D = derived(P)
    to_sheet = Rot(0, 0, -90)                  # model (u, v, w) to sheet axes (X = v, Y = -u, Z = w)
    stubs = frame_edge(-STUB, STUB, P) + mirror_v(frame_edge(-STUB, STUB, P), P)
    part = Compound(children=[to_sheet * robot(P), to_sheet * stubs])
    Lm = P["mod_l"]; pv0, pv1 = D["plate_v"]
    x_cut = Lm - sum(P["wheel_v"]) / 2          # section A-A through the upper wheels and hook roller
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(part, work)
    bb = part.bounding_box()
    slab = Pos(x_cut - 200, 0, 0) * Box(400, 2000, 2000)
    sec = Compound(children=[c & slab for c in (to_sheet * robot(P), to_sheet * stubs)])
    sviews = safe_project_views(sec, work / "sec", hidden_right=False)
    sbb = sec.bounding_box()
    s = Sheet(project="DustRunner", title="General arrangement, robot on the module frames", dwg_no="DRN-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE4, scale=None, theme="technical",
              material="6063 aluminum beam, plates and hood; bought parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"), ("P2", "Layout and labels tidied", "2026-09-30", "AC"),
                         ("P3", "Constructable design (DRN-DDR-003): bearings, housings, clevises, sliders, cleats", DATE3, "AC"),
                         ("P4", "Reissued after the 2026-10-02 decisions; no geometry change (R10 mass limit 16.5 kg)", DATE4, "AC")])
    s.add_ortho(views, names=("front", "top"))
    k = s.scale
    c = ortho_cells(s, views)
    L = []

    # top view (from +Z): X up the slope to the right, Y (= -u, along the row) up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    ttop = Yt(bb.max.Y)
    L += [ext(Xt(pv0), ttop - 1, Xt(pv0), ttop - 8), ext(Xt(Lm - pv0), ttop - 1, Xt(Lm - pv0), ttop - 8)]
    L += dim_h(Xt(pv0), Xt(Lm - pv0), ttop - 7, f"{Lm - 2 * pv0:,.0f} over truck plates")
    hu = P["plate_half_u"]
    L += [ext(Xt(bb.max.X) + 1, Yt(hu), Xt(bb.max.X) + 10, Yt(hu)), ext(Xt(bb.max.X) + 1, Yt(-hu), Xt(bb.max.X) + 10, Yt(-hu))]
    L += dim_v(Xt(bb.max.X) + 8, Yt(hu), Yt(-hu), f"{2 * hu:.0f} plate", left=False)

    # front view (from -Y): X to the right, Z (normal to the glass) up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    bot = Z(bb.min.Z)
    L += [ext(X(0), bot + 1, X(0), bot + 20), ext(X(Lm), bot + 1, X(Lm), bot + 20)]
    L += dim_h(X(0), X(Lm), bot + 19, f"{Lm:,.0f} module length (reference frame stubs)", above=False)
    L += [ext(X(D["brush_v"][0]), Z(0), X(D["brush_v"][0]), bot + 28), ext(X(D["brush_v"][1]), Z(0), X(D["brush_v"][1]), bot + 28)]
    L += dim_h(X(D["brush_v"][0]), X(D["brush_v"][1]), bot + 27, f"{D['brush_len']:,.0f} brushed length, {P['brush_d']:.0f} dia", above=False)
    L += [ext(X(bb.max.X) + 1, Z(0), X(bb.max.X) + 10, Z(0)), ext(X(bb.max.X) + 1, Z(bb.max.Z), X(bb.max.X) + 10, Z(bb.max.Z))]
    L += dim_v(X(bb.max.X) + 8, Z(bb.max.Z), Z(0), f"{bb.max.Z:.0f} above glass", left=False)
    # section line A-A
    xa = X(x_cut)
    L.append(f'<line x1="{xa:.2f}" y1="{Z(bb.max.Z) - 6:.2f}" x2="{xa:.2f}" y2="{bot + 4:.2f}" stroke="{INK}" '
             f'stroke-width="0.25" stroke-dasharray="4 1 0.8 1"/>')
    L += [_t(xa + 1.5, Z(bb.max.Z) - 6, "A", 3.2, 600, INK), _t(xa + 1.5, bot + 6, "A", 3.2, 600, INK)]

    # section A-A, enlarged, looking down the slope from the upper frame edge: Y to the right, Z up
    ks = 0.2
    sx, sy = 24.0, 174.0
    s.add_svg(sviews["right"], sx, sy, scale=ks)
    vw, vh = [v * ks for v in _viewbox(Path(sviews["right"]).read_text())[2:]]
    Yr = lambda my: sx + (my - sbb.min.Y) * ks
    Zr = lambda mz: sy + vh - (mz - sbb.min.Z) * ks
    L.append(_t(sx, sy + vh + 9, "SECTION A-A", 2.8, 600, INK))
    L.append(_t(sx, sy + vh + 13, "Scale 1:5; through the upper wheels, looking down the slope", 2.2, 400, MUTED))
    wu = P["wheel_u"]
    L += [ext(Yr(-wu), Zr(D["wheel_c"]), Yr(-wu), Zr(sbb.min.Z) + 1), ext(Yr(wu), Zr(D["wheel_c"]), Yr(wu), Zr(sbb.min.Z) + 1)]
    L += dim_h(Yr(-wu), Yr(wu), Zr(sbb.min.Z) + 0.5, f"{2 * wu:.0f} wheelbase", above=False)
    tags = [((0.0, D["beam_w"][1] - 10), f"Beam {P['beam_b']:.0f} x {P['beam_h']:.0f} x {P['beam_t']:.0f}"),
            ((-P["hood_r"] * 0.7, D["brush_w"] + P["hood_r"] * 0.7), f"Hood, {P['hood_t']} sheet"),
            ((0.0, D["brush_w"] + 30), f"Brush {P['brush_d']:.0f} dia, {P['interference']:.1f} interference"),
            ((-wu, D["wheel_c"]), f"Wheel {P['wheel_d']:.0f} x {P['wheel_w']:.0f} on frame top flange"),
            ((0.0, D["hook_c"]), f"Hook roller {P['hook_d']:.0f} dia, 60 N preload"),
            ((-(P["plate_half_u"] - 10), P["frame_proud"] - P["frame_d"] / 2), "Module frame (reference)")]
    lx = sx + vw + 8
    for i, ((uy, wz), text) in enumerate(tags):
        ty = sy + 4 + i * (vh - 4) / (len(tags) - 1)
        L.append(f'<line x1="{Yr(-uy):.2f}" y1="{Zr(wz):.2f}" x2="{lx - 1:.2f}" y2="{ty - 0.8:.2f}" stroke="{MUTED}" stroke-width="0.15"/>')
        L.append(f'<circle cx="{Yr(-uy):.2f}" cy="{Zr(wz):.2f}" r="0.5" fill="{INK}"/>')
        L.append(_t(lx, ty, text, 2.2, 400, INK))

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 96, label="Isometric view", sublabel="Not to scale; frame stubs are the reference module")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Reference module {Lm:,.0f} long (1P portrait); frame {P['frame_d']:.0f} deep, top flange {P['lip']:.0f} wide (assumed)",
        f"Wheels {P['wheel_d']:.0f} x {P['wheel_w']:.0f} PU on the frame top flange, {P['wheel_v'][0]:.0f} to {P['wheel_v'][1]:.0f} from its outer face",
        f"Guide rollers {P['guide_d']:.0f} dia on the frame outer face; hook roller {P['hook_d']:.0f} dia under the bottom flange",
        "Hook preload 60 N per truck on a sprung slider (DRN-CAL-001 C0); both wheels driven",
        f"Brush axis {D['brush_w']:.1f} above the glass: {P['interference']:.1f} nominal interference; core {P['core_d']:.0f} x {P['core_t']:.0f}",
        f"Beam {P['beam_b']:.0f} x {P['beam_h']:.0f} x {P['beam_t']:.0f}, {D['beam_len']:,.0f} long, {D['beam_w'][0]:.0f} to {D['beam_w'][1]:.0f} above the glass",
        f"Hood {P['hood_t']} sheet, R{P['hood_r']:.0f}; nothing but the brush within 10 of the glass",
        "Robot about 15.9 kg; about 56 N per wheel brushing (DRN-CAL-001 A3, C1)",
        "Third-angle; sheet X up the slope, Y along the row, Z normal to the glass",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "DRN-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
