"""DustRunner sizing calculations, DRN-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that DRN-CAL-001 (docs/04-calcs/01-sizing.md) quotes, each on a line
tagged like [A1]. Geometry comes from cad/src/model.py (PARAMS, derived and the part solids),
so the calc note, the STEP files and drawing DRN-DWG-001 use the same dimensions. The BOM
total is read from bom/bom.csv and the budget from project.yaml. First-principles estimates
for a paper proof of concept; every assumption is set in the ASSUMPTIONS block below.
"""
import csv
import sys
from math import acos, cos, degrees, pi, radians, sin, sqrt, tan
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, robot_parts, build_components, bx  # noqa: E402

D = derived(P)
g = 9.81

# ------------------------------------------------------------------ ASSUMPTIONS
A = {
    # materials
    "al_rho": 2700.0, "steel_rho": 7850.0, "pu_rho": 1200.0, "pile_rho": 40.0,   # pile: effective density of the microfiber annulus
    "E_al": 69e9, "fy_al": 160e6,            # 6063-T6 yield about 160 MPa (T5 about 110 MPa)
    # brush contact
    "p_contact": 750.0,                      # mean pile contact pressure at 4 mm interference, Pa (range 500 to 1000)
    "mu_brush": 0.45,                        # microfiber on dry dusty glass (range 0.3 to 0.6)
    "brush_rpm": 150.0,
    # traction and resistance
    "mu_wheel": 0.40,                        # polyurethane on dusty anodized aluminum (range 0.3 to 0.6), to measure
    "crr": 0.02,                             # rolling coefficient, PU wheels and rollers on aluminum
    "preload": 70.0,                         # hook roller spring preload per truck, N
    "grade_deg": 2.0,                        # along-row grade of the table
    "v_travel": 0.20,                        # m/s
    # wind
    "rho_air": 1.2, "cd_side": 1.5, "cl_plan": 1.0, "cn_panel": 1.2,
    "v_op": 8.0, "v_start": 6.0, "v_park": 35.0,   # v_op: abort limit; v_start: start limit (DRN-DDR-002)
    # electrical
    "eta_brush": 0.60, "eta_drive": 0.50, "p_elec": 3.0, "p_standby": 0.15,
    "pack_Wh": 128.0, "usable": 0.80, "eta_charge": 0.96,
    "panel_W": 20.0, "derate": 0.75, "sun_design": 3.0, "sun_typical": 5.5,
    "t_overhead": 30.0,                      # start warning, undocking and docking per cycle, s
    "dock_travel": 0.9,                      # m each way between parked position and the row start
    # yield and economics
    "kwp_per_module": 0.58, "yield": 5.5, "rate_mid": 0.003, "rate_high": 0.0049,
    "wash_days": 30.0, "residual": 0.015, "price": 0.10, "sleeve_cost": 40.0,
    "evening_irr": 100.0, "module_area": 2.278 * 1.134, "module_eff": 0.225,
    # structure
    "pin_d": 6.0, "tau_pin": 100e6, "clamp_preload": 5000.0, "mu_clamp": 0.30,
    "buffer_mm": 5.0,
}

# bought-in part masses, kg (typical catalog values, to confirm by weighing)
BOUGHT = {"brush_motor": 0.80, "drive_motors": 0.50, "rollers": 0.35, "battery": 1.30,
          "controller": 0.45, "sensors": 0.12}
WIRING = 0.50            # item 15, wiring, fuse, main switch, cable ties (kg)
TRUCK_EXTRA = 0.30       # per truck: four 10 mm pressed-steel flange bearings, axles, pulleys, belt, coupling (kg)
BRUSH_BEARINGS = 0.40    # two 20 mm pressed-steel flange bearings (kg)
FITTINGS_BOUGHT = 0.34   # two stop buttons 0.16, latch solenoid 0.08, pack straps 0.05, cleat and hood screws 0.05 (kg)
# made fittings added for construction (DRN-DDR-003), aluminium, mass from the model solids
CMP = build_components(P)
FIT_AL = {"trucks": ["housing_lo", "housing_hi", "contact_bracket"],
          "rollers": ["clevises_lo", "clevises_hi", "slider_lo", "slider_hi"],
          "sensors": ["sensor_brackets_lo", "sensor_brackets_hi"],
          "brush": ["plugs"],
          "fittings": ["cleats_lo", "cleats_hi", "shade_posts", "hood_spacers"]}
fit_al = {g: sum(CMP[k].shape.volume for k in ks) * 1e-9 * 2700.0 for g, ks in FIT_AL.items()}

out = {}


def say(tag, text, **vals):
    out[tag] = vals
    print(f"[{tag}] {text}")


def row_len(n):
    return (n * P["mod_w"] + (n - 1) * P["gap"]) / 1000.0


def modules_for(length_m):
    return int(round((length_m * 1000.0 + P["gap"]) / (P["mod_w"] + P["gap"])))


th = radians(P["tilt"])
rp = robot_parts(P)

# ------------------------------------------------------------------ A. mass and balance
print("A. Mass and balance (R10)")
beam_area = P["beam_b"] * P["beam_h"] - (P["beam_b"] - 2 * P["beam_t"]) * (P["beam_h"] - 2 * P["beam_t"])
m = {}
m["beam"] = beam_area * 1e-6 * D["beam_len"] / 1000 * A["al_rho"]
core_area = pi / 4 * (P["core_d"] ** 2 - (P["core_d"] - 2 * P["core_t"]) ** 2)
sleeve_vol = pi / 4 * (P["brush_d"] ** 2 - P["core_d"] ** 2) * D["brush_len"] * 1e-9
m_core = core_area * 1e-6 * (D["brush_len"] + 20) / 1000 * A["al_rho"]
m_sleeve = sleeve_vol * A["pile_rho"]
m_shafts = 2 * pi / 4 * (P["shaft_d"] / 1000) ** 2 * 0.075 * A["steel_rho"]
m["brush"] = m_core + m_sleeve + m_shafts + fit_al["brush"] + BRUSH_BEARINGS
m["hood"] = rp["hood"].volume * 1e-9 * A["al_rho"]
plate_vol = 2 * P["plate_t"] * 2 * P["plate_half_u"] * (P["plate_w"][1] - P["plate_w"][0]) * 1e-9
wheel_vol = 4 * pi * (P["wheel_d"] / 2000) ** 2 * P["wheel_w"] / 1000
m["trucks"] = plate_vol * A["al_rho"] + wheel_vol * A["pu_rho"] + 2 * TRUCK_EXTRA + fit_al["trucks"]
m.update(BOUGHT)
m["rollers"] += fit_al["rollers"]
m["sensors"] += fit_al["sensors"]
m["fittings"] = fit_al["fittings"] + FITTINGS_BOUGHT
m["wiring"] = WIRING
M = sum(m.values())
# center of mass up the slope (v) and normal to the glass (w) from the part solids
cg_v = cg_w = 0.0
for k, mk in m.items():
    if k == "wiring":
        c = (0.0, P["mod_l"] / 2, D["beam_w"][1])
    else:
        c0 = rp[k].center()
        c = (c0.X, c0.Y, c0.Z)
    cg_v += mk * c[1]; cg_w += mk * c[2]
cg_v /= M; cg_w /= M
say("A1", f"beam {m['beam']:.2f} kg, brush {m['brush']:.2f} kg (core {m_core:.2f}, sleeve {m_sleeve:.2f}), hood and shade {m['hood']:.2f} kg, "
    f"trucks and wheels {m['trucks']:.2f} kg", beam=m["beam"], brush=m["brush"], hood=m["hood"], trucks=m["trucks"])
say("A2", "bought parts " + ", ".join(f"{k} {v:.2f}" for k, v in BOUGHT.items()) + f", wiring {WIRING:.2f} kg")
say("A3", f"robot mass {M:.1f} kg (R10 limit 15 kg); CG {cg_v:.0f} mm up the slope of {P['mod_l']:.0f}, {cg_w:.0f} mm above the glass",
    M=M, cg_v=cg_v, cg_w=cg_w)
plate_add = (plate_vol - 2 * P["plate_t"] * 2 * P["plate_half_u"] * 272.0 * 1e-9) * A["al_rho"]   # concept plates were 272 mm tall
add = sum(fit_al.values()) + BRUSH_BEARINGS + FITTINGS_BOUGHT + plate_add
say("A4", f"added for construction (DRN-DDR-003): drive housings, clevises, hook sliders, brackets, cleats, posts and core plugs "
    f"{sum(fit_al.values()):.2f} kg; brush flange bearings {BRUSH_BEARINGS:.2f} kg; stop buttons, solenoid, straps and screws "
    f"{FITTINGS_BOUGHT:.2f} kg; taller truck plates {plate_add:.2f} kg; "
    f"total {add:.2f} kg", add=add)

# ------------------------------------------------------------------ B. brush contact, drag and deflection
print("B. Brush contact, drag and deflection (R3, R8)")
Lb = D["brush_len"] / 1000
cw = D["contact_w"] / 1000
r_b = P["brush_d"] / 2000
d_ref = 0.004
cw_ref = 2 * sqrt(r_b ** 2 - (r_b - d_ref) ** 2)
k_pile = A["p_contact"] * cw_ref / d_ref       # pile stiffness, N per m of interference per m of length (linearized)
vs = A["brush_rpm"] * 2 * pi / 60 * r_b


def brush_deflection(core_d, core_t, n=241):
    """Core tube as a pinned beam between the truck bearings on an elastic foundation (the pile),
    loaded by its own weight toward the glass. Returns the interference minimum and maximum along the
    sleeve (mm) and the total pile force (N)."""
    I = pi / 64 * ((core_d / 1000) ** 4 - ((core_d - 2 * core_t) / 1000) ** 4)
    EI = A["E_al"] * I
    Ls = (D["span"] + 2 * P["plate_t"]) / 1000
    x = np.linspace(0, Ls, n); h = x[1] - x[0]
    x0 = D["brush_v"][0] / 1000 + (P["plate_gap"] + P["plate_t"]) / 1000
    on = (x >= x0) & (x <= x0 + Lb)
    d0 = P["interference"] / 1000
    k = k_pile
    q_w = m["brush"] * g * cos(th) / Ls          # own weight toward the glass, N/m
    # unknown y (toward the glass, m); EI y'''' + k_on y = q_w - k_on d0
    Kmat = np.zeros((n, n)); f = np.full(n, q_w) - np.where(on, k * d0, 0.0)
    for i in range(2, n - 2):
        Kmat[i, i - 2:i + 3] = EI / h ** 4 * np.array([1, -4, 6, -4, 1])
    Kmat += np.diag(np.where(on, k, 0.0))
    for i in (0, n - 1):                         # y = 0 at the bearings
        Kmat[i] = 0; Kmat[i, i] = 1; f[i] = 0
    Kmat[1] = 0; Kmat[1, 0:3] = [1, -2, 1]; f[1] = 0     # y'' = 0 (pinned)
    Kmat[n - 2] = 0; Kmat[n - 2, n - 3:n] = [1, -2, 1]; f[n - 2] = 0
    y = np.linalg.solve(Kmat, f)
    inter = (d0 + y[on]) * 1000
    return inter.min(), inter.max(), k * float(np.sum(d0 + y[on])) * h


for cd, ct, tag in ((40.0, 2.0, "B4"), (P["core_d"], P["core_t"], "B5")):
    lo, hi, F = brush_deflection(cd, ct)
    say(tag, f"core {cd:.0f} x {ct:.1f} mm tube: interference {lo:.1f} to {hi:.1f} mm along the sleeve (R3 band 3 to 5 mm); "
        f"total pile force {F:.0f} N", lo=lo, hi=hi)
i_lo, i_hi = out["B5"]["lo"], out["B5"]["hi"]
_, _, Fb = brush_deflection(P["core_d"], P["core_t"])
Ft = A["mu_brush"] * Fb
Pb = Ft * vs
say("B1", f"pile stiffness {k_pile/1000:.1f} kN/m per m ({A['p_contact']:.0f} Pa at 4 mm); contact width {cw*1000:.0f} mm at "
    f"{P['interference']:.1f} mm nominal interference; normal force {Fb:.0f} N; tangential {Ft:.0f} N; surface speed {vs:.2f} m/s; "
    f"brush power {Pb:.0f} W mechanical, {Pb/A['eta_brush']:.0f} W electrical", Fb=Fb, Ft=Ft, vs=vs, Pb=Pb)
for tag, lo, hi in (("B2", 500.0, 0.30), ("B3", 1000.0, 0.60)):
    say(tag, f"range: p {lo:.0f} Pa and mu {hi:.2f} gives {Fb*lo/A['p_contact']*hi*vs:.0f} W mechanical")
# metal within 10 mm of the glass (R3): any robot solid other than the brush sleeve inside a 10 mm slab over the glass
slab = bx(-500, 500, D["glass_v"][0], D["glass_v"][1], 0.0, 10.0)
metal_hits = {k: (rp[k] & slab).volume for k in ("beam", "hood", "trucks", "rollers", "drive_motors", "sensors",
                                                  "brush_motor", "battery", "controller")}
core_clear = D["brush_w"] - P["core_d"] / 2
say("B6", f"solids other than the brush inside the 10 mm slab over the glass: {sum(metal_hits.values()):.0f} mm3; "
    f"core tube {core_clear:.0f} mm above the glass; hood edges {D['brush_w'] + P['hood_clear']:.0f} mm above the glass",
    hits=sum(metal_hits.values()))

# ------------------------------------------------------------------ C. wheel loads, traction and steps
print("C. Wheel loads, traction and frame steps (R4, R9, R10)")
w_cg = cg_w / 1000
w_guide = (-P["frame_d"] / 2) / 1000
span_w = (P["mod_l"] - 2 * sum(P["wheel_v"]) / 2) / 1000   # between wheel tread centers
v_wl = sum(P["wheel_v"]) / 2 / 1000


def loads(tilt_deg, brush_on=True, preload=None, M_=None):
    t = radians(tilt_deg); Mm = M_ or M
    pre = A["preload"] if preload is None else preload
    Wn = Mm * g * cos(t); Fs = Mm * g * sin(t)
    share_hi = (cg_v / 1000 - v_wl) / span_w
    tip = Fs * (w_cg - w_guide) / span_w          # moves load from the upper truck to the lower one
    Fb_ = Fb if brush_on else 0.0
    N_lo = Wn * (1 - share_hi) + tip + pre - Fb_ / 2
    N_hi = Wn * share_hi - tip + pre - Fb_ / 2
    return dict(Wn=Wn, Fs=Fs, N_lo=N_lo, N_hi=N_hi, N=N_lo + N_hi, pre=pre)


def resistance(Ld, wind=0.0, extra=0.0):
    roll = A["crr"] * (Ld["N"] + 2 * Ld["pre"] + Ld["Fs"])
    grade = M * g * sin(radians(A["grade_deg"]))
    return roll + Ft + grade + wind + extra, roll, grade


# hook preload rule (DRN-CAL-001 Table 3): the highest preload, in 5 N steps, that keeps the steady brushing
# wheel load at 60 N or less at every tilt from 10 to 35 degrees
def _worst_steady(pre):
    return max(max(loads(t, preload=pre)["N_lo"], loads(t, preload=pre)["N_hi"]) / 2 for t in range(10, 36))


A["preload"] = float(max(pp for pp in range(20, 101, 5) if _worst_steady(pp) <= 60.0))
say("C0", f"hook preload by the 60 N rule: {A['preload']:.0f} N per truck (worst steady wheel load {_worst_steady(A['preload']):.1f} N; "
    f"{_worst_steady(A['preload'] + 5):.1f} N at {A['preload'] + 5:.0f} N)", pre=A["preload"])

A_side = D["brush_len"] / 1000 * (D["beam_w"][1] / 1000) + 0.03     # beam, hood and brush silhouette plus enclosures and motors
q_op = 0.5 * A["rho_air"] * A["v_op"] ** 2
F_wind_op = q_op * A["cd_side"] * A_side
L0 = loads(P["tilt"])
R0, roll0, grade0 = resistance(L0)
Rw, _, _ = resistance(L0, F_wind_op)
T0 = A["mu_wheel"] * L0["N"]
say("C1", f"normal weight {L0['Wn']:.0f} N, down-slope {L0['Fs']:.0f} N (upper guide rollers); per wheel, brushing: lower "
    f"{L0['N_lo']/2:.0f} N, upper {L0['N_hi']/2:.0f} N with {A['preload']:.0f} N hook preload per truck and {Fb:.0f} N brush reaction",
    wl_lo=L0["N_lo"] / 2, wl_hi=L0["N_hi"] / 2)
Ldock = loads(P["tilt"], brush_on=False)
say("C2", f"per wheel, brush off the glass (parked on the dock rails, or the lead wheel entering the first module): lower {Ldock['N_lo']/2:.0f} N, upper {Ldock['N_hi']/2:.0f} N",
    wl=Ldock["N_lo"] / 2)
say("C3", f"resistance, still air: rolling {roll0:.1f} N, brush {Ft:.0f} N, {A['grade_deg']:.0f} deg grade {grade0:.1f} N, total {R0:.0f} N; "
    f"traction available {T0:.0f} N (mu {A['mu_wheel']}); margin {T0/R0:.2f}", R0=R0, T0=T0, margin=T0 / R0)
say("C4", f"wind along the row at {A['v_op']:.0f} m/s: {F_wind_op:.0f} N on {A_side:.2f} m2 (Cd {A['cd_side']}); total {Rw:.0f} N; "
    f"margin {T0/Rw:.2f}", Fw=F_wind_op, Rw=Rw, margin=T0 / Rw)
for tag, mu in (("C5", 0.30), ("C6", 0.60)):
    say(tag, f"mu {mu:.2f}: margin {mu*L0['N']/R0:.2f} in still air, {mu*L0['N']/Rw:.2f} at {A['v_op']:.0f} m/s")
# wind speed at which the margin falls to 1.25 with mu 0.4
v_lim = sqrt(max(0.0, (T0 / 1.25 - R0)) / (0.5 * A["rho_air"] * A["cd_side"] * A_side))
L35 = loads(35.0); R35 = resistance(L35)[0]
v_lim35 = sqrt(max(0.0, (A["mu_wheel"] * L35["N"] / 1.25 - R35)) / (0.5 * A["rho_air"] * A["cd_side"] * A_side))
say("C7", f"wind along the row for a traction margin of 1.25 at mu 0.4: {v_lim:.1f} m/s at 25 deg tilt, {v_lim35:.1f} m/s at 35 deg",
    v_lim=v_lim, v_lim35=v_lim35)
F_wind_start = 0.5 * A["rho_air"] * A["v_start"] ** 2 * A["cd_side"] * A_side
Rs, _, _ = resistance(L0, F_wind_start)
say("C13", f"start limit {A['v_start']:.0f} m/s along the row (DRN-DDR-002): {F_wind_start:.0f} N; total {Rs:.0f} N; margin {T0/Rs:.2f} at mu 0.4, "
    f"{0.30*L0['N']/Rs:.2f} at mu 0.3; abort at {A['v_op']:.0f} m/s keeps {T0/Rw:.2f} at mu 0.4, {0.30*L0['N']/Rw:.2f} at mu 0.3",
    margin=T0 / Rs, margin03=0.30 * L0["N"] / Rs, Fs=F_wind_start)
for tag, tl in (("C8", 10.0), ("C9", 35.0)):
    Lt = loads(tl); Rt, _, _ = resistance(Lt, F_wind_op)
    say(tag, f"tilt {tl:.0f} deg: per wheel {Lt['N_lo']/2:.0f} / {Lt['N_hi']/2:.0f} N, down-slope {Lt['Fs']:.0f} N, "
        f"margin {A['mu_wheel']*Lt['N']/resistance(Lt)[0]:.2f} still air, {A['mu_wheel']*Lt['N']/Rt:.2f} at {A['v_op']:.0f} m/s",
        wl=Lt["N_lo"] / 2)
# climbing a frame step with both wheels of a truck driven (lead wheel on the step edge)
r_w = P["wheel_d"] / 2
step = 5.0
phi = acos((r_w - step) / r_w)
mu = A["mu_wheel"]
W_lead = L0["N_lo"] / 2
push_needed = W_lead * (sin(phi) - mu * cos(phi)) / (cos(phi) + mu * sin(phi))
avail = mu * (L0["N"] - W_lead) - (R0 - 0)      # the other three wheels, less the steady resistance
say("C10", f"{step:.0f} mm frame step, {P['wheel_d']:.0f} mm wheel: contact angle {degrees(phi):.0f} deg; extra push at the lead axle "
    f"{push_needed:.0f} N (driven lead wheel); spare traction on the other wheels {avail:.0f} N", need=push_needed, avail=avail)
step3 = 3.0; phi3 = acos((r_w - step3) / r_w)
need3 = W_lead * (sin(phi3) - mu * cos(phi3)) / (cos(phi3) + mu * sin(phi3))
gap = 25.0
dip = r_w - sqrt(r_w ** 2 - (gap / 2) ** 2)
say("C11", f"{step3:.0f} mm step needs {need3:.0f} N; a {gap:.0f} mm gap lets the wheel dip {dip:.1f} mm (like a {dip:.1f} mm step)",
    need3=need3, dip=dip)
lip_clear = P["lip"] - P["wheel_v"][1]
say("C12", f"wheel tread {P['wheel_w']:.0f} mm on a {P['lip']:.0f} mm frame flange, {lip_clear:.0f} mm clear of the glass edge; "
    f"flanges narrower than {P['wheel_v'][1]:.0f} mm put the tread on the glass", lip_clear=lip_clear)

# ------------------------------------------------------------------ D. wind, parked and running
print("D. Wind (R9)")
q_park = 0.5 * A["rho_air"] * A["v_park"] ** 2
F_along_park = q_park * A["cd_side"] * A_side
A_plan = (2 * (P["hood_r"] + P["hood_t"]) / 1000) * D["brush_len"] / 1000 + 2 * 0.26 * 0.03
lift_park = q_park * A["cl_plan"] * A_plan
net_up = lift_park - L0["Wn"]
F_panel = q_park * A["cn_panel"] * P["panel"][0] * P["panel"][1] * 1e-6
pin = A["tau_pin"] * pi / 4 * (A["pin_d"] / 1000) ** 2
clamp_hold = 2 * A["mu_clamp"] * A["clamp_preload"]
say("D1", f"parked at {A['v_park']:.0f} m/s: {F_along_park:.0f} N along the row, lift {lift_park:.0f} N on {A_plan:.2f} m2 "
    f"against {L0['Wn']:.0f} N weight, net {net_up:.0f} N up on the two hook rollers ({net_up/2 + A['preload']:.0f} N each with preload)",
    along=F_along_park, net_up=net_up)
say("D2", f"latch pin {A['pin_d']:.0f} mm in single shear holds {pin:.0f} N (factor {pin/F_along_park:.1f}); dock panel {F_panel:.0f} N; "
    f"two dock clamps hold {clamp_hold:.0f} N by friction against {F_along_park + F_panel:.0f} N (factor {clamp_hold/(F_along_park + F_panel):.1f})",
    pin=pin, clamp=clamp_hold)
lift_op = q_op * A["cl_plan"] * A_plan
say("D3", f"running at {A['v_op']:.0f} m/s: lift {lift_op:.0f} N against {L0['Wn']:.0f} N weight (stays on the frames without the hooks)",
    lift_op=lift_op)
ke = 0.5 * M * A["v_travel"] ** 2
F_buffer = 2 * ke / (A["buffer_mm"] / 1000)
F_stall = A["mu_wheel"] * L0["N"]
stop_hold = A["mu_clamp"] * A["clamp_preload"]
say("D4", f"end stop, IR failed: impact {ke:.2f} J, {F_buffer:.0f} N on a {A['buffer_mm']:.0f} mm buffer; then drive stall up to {F_stall:.0f} N; "
    f"each stop clamp holds {stop_hold:.0f} N", F_buffer=F_buffer)

# ------------------------------------------------------------------ E. beam
print("E. Chassis beam")
I_beam = (P["beam_b"] * P["beam_h"] ** 3 - (P["beam_b"] - 2 * P["beam_t"]) * (P["beam_h"] - 2 * P["beam_t"]) ** 3) / 12 * 1e-12
Lspan = D["span"] / 1000
q_beam = (m["beam"] + m["brush"] + m["hood"] + m["battery"] + m["controller"] + WIRING) * g * cos(th) / Lspan
Mmax = q_beam * Lspan ** 2 / 8 + 250.0 * Lspan / 4            # plus a 250 N point load at mid span (a hand on the beam)
sig = Mmax * (P["beam_h"] / 2000) / I_beam
defl = 5 * q_beam * Lspan ** 4 / (384 * A["E_al"] * I_beam) + 250.0 * Lspan ** 3 / (48 * A["E_al"] * I_beam)
say("E1", f"beam span {Lspan:.2f} m, I {I_beam*1e12:,.0f} mm4; with its carried parts and a 250 N point load: stress {sig/1e6:.0f} MPa "
    f"(6063-T6 yield about {A['fy_al']/1e6:.0f} MPa), deflection {defl*1000:.1f} mm", sig=sig, defl=defl)

# ------------------------------------------------------------------ F. power, cycle, energy, autonomy
print("F. Power, cycle time and energy (R7, R8)")
v = A["v_travel"]
P_drive = R0 * v / A["eta_drive"]
P_brush_e = Pb / A["eta_brush"]
P_run = P_brush_e + P_drive + A["p_elec"]


def cycle(length_m):
    t_clean = 2 * length_m / v
    t_dock = 2 * A["dock_travel"] / v
    t = t_clean + t_dock + A["t_overhead"]
    E = (P_run * t_clean + (P_drive + A["p_elec"]) * t_dock + A["p_elec"] * A["t_overhead"]) / 3600
    return t, E


say("F1", f"electrical power while cleaning: brush {P_brush_e:.0f} W, drives {P_drive:.0f} W, electronics {A['p_elec']:.0f} W, total {P_run:.0f} W",
    P_run=P_run, P_drive=P_drive, P_brush=P_brush_e)
rows = {}
for tag, n in (("F2", 35), ("F3", modules_for(60.0)), ("F4", modules_for(100.0))):
    Lr = row_len(n); t, E = cycle(Lr)
    rows[n] = (Lr, t, E)
    say(tag, f"{n} modules, {Lr:.1f} m, {n*A['kwp_per_module']:.1f} kWp: cycle {t/60:.1f} min, {E:.1f} Wh from the pack, "
        f"{E/A['eta_charge']:.1f} Wh from the dock", n=n, L=Lr, t=t, E=E)
n100 = modules_for(100.0)
E100 = rows[n100][2]
usable = A["pack_Wh"] * A["usable"]
standby_day = A["p_standby"] * 24
need3 = 3 * E100 + 3 * standby_day
say("F5", f"usable pack {usable:.0f} Wh; three cycles on the 100 m row plus three days standby ({standby_day:.1f} Wh/day) need {need3:.0f} Wh "
    f"(margin {usable/need3:.2f}); days with no sun on the 40 m row {usable/(rows[35][2] + standby_day):.0f}", need3=need3, usable=usable)
harvest3 = A["panel_W"] * A["sun_design"] * A["derate"]
harvest55 = A["panel_W"] * A["sun_typical"] * A["derate"]
day_need = E100 / A["eta_charge"] + standby_day
say("F6", f"dock harvest {harvest3:.0f} Wh/day at {A['sun_design']:.0f} sun hours, {harvest55:.0f} Wh/day at {A['sun_typical']}; one 100 m day needs "
    f"{day_need:.0f} Wh (margin {harvest3/day_need:.2f})", harvest3=harvest3, day_need=day_need)
# flow diagram values for the 40 m row (Wh per cycle)
E40 = rows[35][2]
t40 = 2 * rows[35][0] / v
e_brush_mech = Pb * t40 / 3600
e_wheels = R0 * v * t40 / 3600 + R0 * v * (2 * A["dock_travel"] / v) / 3600
e_elec = A["p_elec"] * rows[35][1] / 3600
e_motor_in = E40 - e_elec
e_in = E40 / A["eta_charge"]
say("F7", f"flow, 40 m row: dock {e_in:.2f} Wh, pack out {E40:.2f} Wh, electronics {e_elec:.2f} Wh, motor input {e_motor_in:.2f} Wh, "
    f"brush and wheels {e_brush_mech + e_wheels:.2f} Wh", e_in=e_in, E40=E40, e_elec=e_elec, e_motor=e_motor_in, e_mech=e_brush_mech + e_wheels)

# ------------------------------------------------------------------ G. coverage
print("G. Coverage (R5)")
across = D["brush_len"] / D["glass_across"]
u_stop_face = -P["stop_l"] - P["buffer_t"]    # buffer face measured from the end of the last module
brush_reach = u_stop_face - (P["wheel_u"] + P["wheel_d"] / 2) + P["brush_d"] / 2   # the lead wheels meet the buffers
unbrushed = -P["lip"] - brush_reach
glass_w = P["mod_w"] - 2 * P["lip"]
cov40 = across * (1 - unbrushed / (35 * glass_w))
say("G1", f"across the slope {D['brush_len']:.0f} of {D['glass_across']:.0f} mm ({across*100:.1f} %); last {unbrushed:.0f} mm of glass on the "
    f"final module unbrushed; coverage of the 40 m row {cov40*100:.1f} %", cov=cov40, unbrushed=unbrushed)

# ------------------------------------------------------------------ H. stopping (R12)
print("H. Stopping (R12)")
I_brush = 0.5 * m_sleeve * ((P["brush_d"] / 2000) ** 2 + (P["core_d"] / 2000) ** 2) + m_core * (P["core_d"] / 2000) ** 2
ratio = 3000.0 / A["brush_rpm"]
I_tot = I_brush + 3e-5 * ratio ** 2
w_b = A["brush_rpm"] * 2 * pi / 60
t_brush = I_tot * w_b / (Ft * P["brush_d"] / 2000)
t_robot = M * v / R0
say("H1", f"brush inertia {I_brush*1e3:.1f} g m2 plus motor rotor {3e-5*ratio**2*1e3:.1f} g m2 reflected: coasts to rest in {t_brush:.2f} s; "
    f"robot stops in {t_robot:.2f} s on its own resistance", t_brush=t_brush, t_robot=t_robot)

# ------------------------------------------------------------------ I. cost and payback
print("I. Cost and payback (R13, R14)")
bom = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
say("I1", f"BOM total ${cost:.2f} for {len(bom)} lines against budget_usd ${budget:.0f}; margin ${budget - cost:.2f}", cost=cost, budget=budget)


def payback(n, rate, sleeve=0.0):
    kwp = n * A["kwp_per_module"]
    E_year = kwp * A["yield"] * 365
    loss_wash = rate * A["wash_days"] / 2
    dE = (loss_wash - A["residual"]) * E_year
    shade = n * A["evening_irr"] * A["module_area"] * A["module_eff"] / 3 * \
        (2 * (P["mod_w"] + 2 * P["plate_half_u"]) / 1000 / v) / 3600 / 1000 * 365
    val = (dE - shade) * A["price"] - sleeve
    return kwp, loss_wash, dE, shade, val, cost / val


for tag, n, rate in (("I2", 35, A["rate_mid"]), ("I3", 35, A["rate_high"]), ("I4", modules_for(60.0), A["rate_mid"]),
                     ("I5", n100, A["rate_mid"])):
    kwp, lw, dE, sh, val, pb = payback(n, rate)
    say(tag, f"{n} modules ({kwp:.1f} kWp), {rate*100:.2f} %/day: monthly-wash loss {lw*100:.1f} %, recovered {dE:,.0f} kWh/yr, "
        f"self-shading {sh:.0f} kWh/yr, value ${val:.0f}/yr, payback {pb:.1f} yr", pb=pb, val=val, dE=dE)
kwp, lw, dE, sh, val, pb60s = payback(modules_for(60.0), A["rate_mid"], A["sleeve_cost"])
say("I6", f"60 m row, mid case, with a ${A['sleeve_cost']:.0f} sleeve set every year: payback {pb60s:.1f} yr", pb=pb60s)
res_break = A["rate_mid"] * A["wash_days"] / 2 - cost / 3 / A["price"] / (modules_for(60.0) * A["kwp_per_module"] * A["yield"] * 365)
say("I7", f"60 m row meets 3 years while the daily-cleaning residual loss stays below {res_break*100:.1f} % (assumed {A['residual']*100:.1f} %)",
    res=res_break)
n3 = next(n for n in range(10, 400) if payback(n, A["rate_mid"])[5] <= 3.0)
say("I9", f"shortest row with a mid-case payback of 3 years or less at ${cost:.0f}: {n3} modules, {row_len(n3):.1f} m",
    n=n3, length=row_len(n3))
water = (35 * 3.5, 35 * 10.0)
say("I8", f"water avoided per monthly wash of the 40 m row {water[0]:.0f} to {water[1]:.0f} L; {12*water[0]/1000:.1f} to {12*water[1]/1000:.1f} m3/yr")

# ------------------------------------------------------------------ J. requirement status
print("J. Requirement status")
wl_max = max(L0["N_lo"], L0["N_hi"]) / 2
wl_max_t = max(loads(10.0)["N_lo"], loads(35.0)["N_lo"]) / 2
wl_entry = out["C2"]["wl"]
status = [
    ("R1", "No water", "none by design", "Met"),
    ("R2", "Residual loss 1.5 % or less", "assumed, not calculable", "Not verifiable at TRL 3"),
    ("R3", "Interference 3 to 5 mm; no metal within 10 mm", f"{i_lo:.1f} to {i_hi:.1f} mm; {out['B6']['hits']:.0f} mm3 in slab; abrasion unknown",
     "Not verifiable at TRL 3"),
    ("R4", "Reference table; 25 mm gaps; 5 mm steps", f"5 mm step extra push {push_needed:.0f} N vs {avail:.0f} N spare; lip {P['lip']:.0f} mm assumed",
     "At risk"),
    ("R5", "Coverage 95 % or more", f"{cov40*100:.1f} %", "Met"),
    ("R6", "Rail-free; installed in 60 min", "rail-free and clamp-on by design; time not calculable", "Not verifiable at TRL 3"),
    ("R7", "100 m row in 20 min or less", f"{rows[n100][1]/60:.1f} min", "Met"),
    ("R8", "3 cycles on 100 m with no sun; recharge at 3 sun hours", f"{need3:.0f} of {usable:.0f} Wh; {harvest3:.0f} vs {day_need:.0f} Wh/day", "Met"),
    ("R9", "End stops; hooks in wind; start below 6 m/s, abort at 8 m/s; 35 m/s parked",
     f"traction margin {out['C13']['margin']:.2f} at the 6 m/s start limit, {T0/Rw:.2f} at the 8 m/s abort (mu 0.4); "
     f"{out['C13']['margin03']:.2f} and {0.30*L0['N']/Rw:.2f} at mu 0.3; parked holds",
     "At risk" if out["C13"]["margin03"] < 1.25 else "Met"),
    ("R10", "15 kg or less; 60 N or less per wheel steady; 75 N or less for the row-entry transient",
     f"{M:.1f} kg; {wl_max:.0f} N at 25 deg, {wl_max_t:.0f} N worst tilt; {wl_entry:.0f} N transient at row entry",
     "Met" if M <= 15 and wl_max_t <= 60 and wl_entry <= 75 else ("At risk" if M <= 15 and wl_max_t <= 60 else "Not met")),
    ("R11", "IP65; 0 to 50 C; glass to 75 C", "pack charge limit 45 C in the sun", "At risk"),
    ("R12", "Stops within 2 s", f"brush {t_brush:.2f} s, robot {t_robot:.2f} s", "Met"),
    ("R13", "Parts $500 or less", f"${cost:.2f}", "At risk" if budget - cost < 0.05 * budget and cost <= budget else ("Met" if cost <= budget else "Not met")),
    ("R14", "Payback 3 yr or less on rows of 60 m or more, mid case", f"{out['I4']['pb']:.1f} yr (60 m), {out['I5']['pb']:.1f} yr (100 m)",
     "Met" if out["I4"]["pb"] <= 3.0 else "Not met"),
    ("R15", "Sleeve change in 15 min on the row; catalog parts", "catalog parts; time not calculable", "Not verifiable at TRL 3"),
]
for rid, tgt, val, st in status:
    say(f"J-{rid}", f"{rid}: {st}; {val} (target: {tgt})", status=st)
counts = {}
for *_, st in status:
    counts[st] = counts.get(st, 0) + 1
say("J0", "counts " + ", ".join(f"{k} {v}" for k, v in counts.items()))
