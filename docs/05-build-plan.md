---
doc_id: DRN-BLD-001
title: DustRunner prototype build plan
project: DustRunner
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (DRN-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# DustRunner prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. The robot, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. The robot pulled apart and numbered in build order. The long middle of the beam, brush and hood is left out so the trucks can be seen.*

![Figure 2. The dock and end stops, pulled apart](05-build-plan/overview-dock.png)

*Figure 2. The dock and the end stops, numbered on from the robot, shown as installed.*

The prototype is one DustRunner robot for the reference table (portrait modules 2,278 mm long, 25° tilt), its dock at the start of the row and a pair of end stops at the far end. The robot is a 2.3 m aluminium beam carrying a microfiber brush between two end trucks; each truck has two driven wheels on the module frame's top flange, two guide rollers on the frame's outer face and a sprung hook roller under its bottom flange, with the motors and belts in a folded drive housing outside. The dock is a small aluminium frame on four legs, clamped to the first module's frame, whose two short rails continue the frame profile; it carries a 20 W panel, a charger, the contact block the robot parks against, a latch tab and a cup anemometer. Figures 1 and 2 show the 24 components in the order you make or fit them. Nineteen are made in a small workshop from aluminium plate, sheet, tube, angle and bar, with sawing, drilling, tapping, folding and a little turning (Section 3); the rest are bought: wheels, bearings, belts and pulleys, gearmotors, rollers, the pack, the controller and drivers, sensors, the solenoid, the panel, the charger and the anemometer. The parts cost about $573 from the bill of materials, against a value-engineering target of $500.

> **Safety:** DustRunner is moving machinery with an unattended rotating brush, belts and wheels, a 128 Wh lithium iron phosphate pack, and it works on a live PV array that can carry several hundred volts DC, on glass up to about 75 °C, up to about 1.6 m above the ground. Keep the pack fuse out until Section 6 says otherwise, never charge the pack below 0 °C or above 45 °C, and never let the robot touch array cables, connectors or junction boxes. Cut aluminium edges are sharp: deburr everything and wear gloves when handling plate and sheet.

## 2. What changed to make it buildable

The concept showed what DustRunner does; many of its parts floated, rubbed or had no fixing. Each change below keeps what the robot and dock do, and all of them are recorded in decision record DRN-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Guide rollers | A roller filling the gap between the truck plate and the frame face, with no axle | A roller on an M8 bolt in a folded clevis; the plate sits 28 mm (not 22) outside the frame (Figure 7) | The roller turns freely, 6 mm off the plate |
| Hook rollers | A roller floating over a rigid arm, with no spring | A sliding block on the plate, pushed up by a spring, carrying the roller on an 8 mm axle under the flange (Figure 9) | Gives the set preload, now 60 N per truck |
| Wheel axles and motors | Stub axles on the inside, a belt on the outside, motors fixed to nothing | Each axle in two flange bearings through the plate; belts and motors in a folded drive housing on the outside (Figures 4 and 16) | The housing guards the belts and holds the motors |
| Brush ends | Shafts butted against the core, no bearings | Turned plugs in the core, stub shafts in the plugs, one flange bearing on each plate (Figure 16) | The shafts can carry the brush and its drive |
| Beam | Butted against the plates, no fixing | Two angle cleats at each end, through-bolted (Figure 13) | Bolted, so the beam can be replaced for another module length |
| Hood, sunshade, pack | Floating a few millimetres from the beam | Hood on five 3 mm spacers; shade on four posts; pack strapped (Figure 18) | Keeps the gaps the concept meant |
| Sensors, robot contacts | Butted against the plate edge | On folded brackets screwed to the plate face (Figures 10 and 11) | Fixed to a face, not an edge |
| Dock latch | A pin with nothing to engage and no release | A sprung pin on a 12 V solenoid on the robot drops through a tab on the dock (Figure 30) | Holds the parked robot in wind; fails latched |
| Dock rails and supports | Posts under the rails in the hook roller's path; cross members not touching the rails; clamps not touching anything | Rails held by brackets inside the channel on cross members 6 mm lower; frame clamps grip the first module's flange (Figures 22 and 25) | The robot can drive out, and the dock is fixed without drilling |
| Dock legs, mast | Legs meeting tilted members at an angle; the mast leaning 25° | Vertical legs bolted beside the members, on foot plates; vertical mast in U-bolt clamps (Figure 28) | Bolted at any tilt; the anemometer reads correctly upright |
| End stops | Taller than the sensors, so a sensor hit first; no clamp screw | Three-piece clamp with an M8 screw, top 40 mm above the glass (Figure 32) | The wheels meet the buffer; the sensors pass over |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Inner face" of a truck plate is the face toward the brush; "outer face" is the face away from it. "Toward the row" and "toward the dock" are along the row; "up" on a truck plate is measured from its bottom edge. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4. Folding 2 and 3 mm aluminium needs a sheet-metal brake (a local sheet-metal shop, or a bench brake); the short 3 mm folds can be made in a vice between two hardwood blocks.

### 3.1 Truck plates (make 2, a lower and an upper)

![Figure 3. Making sketch of the truck plate](../cad/drawings/DRN-DWG-101.png)

*Figure 3. Truck plate making sketch (DRN-DWG-101).*

**What it is and what it is made from.** The plate at each end of the robot that everything on that truck bolts to. Aluminium plate 5 mm, 5083 or 6082 class, 260 x 296 mm.

**How to make it.**

1. Cut two blanks 260 x 296 mm, square. Mark one face of each as the inner face and the long edges as top and bottom.
2. Axle holes: 12 mm, 90 each side of the centre line, 116 up. Drill the two plates clamped together.
3. Lower plate only: brush shaft hole 22 mm on the centre line, 135.5 up.
4. Stop button hole: 22 mm, 95 toward the row from the centre line, 265 up.
5. Hook slider bolts: two 6.5 mm holes, 13 each side of the centre line, 40 up.
6. Beam cleat bolts: four 6.5 mm holes, 37 each side of the centre line, 240 and 270 up.
7. All other holes (flange bearings, drive housing flanges, clevises, sensor and contact brackets, spring seat) are drilled through the part in place, 3.3 mm and tapped M4, or 6.5 mm where the part's bolt is M6. Mark them from the part when you fit it.
8. The upper plate is the mirror image of the lower, without the brush hole. Deburr every hole and round the corners to about 3 mm.

**How it fits the parts next to it.**

![Figure 4. Joint 1: wheel axle in two flange bearings](05-build-plan/joint-01.png)

*Figure 4. Cut through the axle: a flange bearing each side of the plate, the wheel on the inside, the pulley and the motor coupling inside the drive housing.*

Each axle turns in two 2-bolt flange bearings, one bolted to each face of the plate, so the wheel overhangs only 19 mm past the inner bearing. The wheel runs on the frame's top flange, 3 to 21 from the frame's outer face; the plate stands 28 mm outside the frame and never touches it.

**Check before moving on.** Axle holes 180 apart within 0.5 mm; an axle pushed through both holes of the two plates clamped together turns freely.

### 3.2 Drive housings (make 2: a lower and an upper)

![Figure 5. Making sketch of the drive housing](../cad/drawings/DRN-DWG-102.png)

*Figure 5. Lower drive housing making sketch (DRN-DWG-102). The upper housing is the same but 79 tall.*

**What it is and what it is made from.** A folded tray on the outer face of each truck plate that covers the wheel belt (and, at the lower truck, the brush belt) and carries the gearmotors. Aluminium sheet 5052: 2 mm for the lower housing, which carries the brush motor; 1.5 mm for the upper.

**How to make it.**

1. Mark the lower blank: a back 236 x 165; top and bottom walls 40 deep; end walls 40 deep plus a 12 mm flange on each. Drill a 3 mm relief hole at each corner where fold lines cross.
2. Fold the walls 90° toward you, then the flanges 90° outward.
3. Drive motor shaft hole: 8 mm, 90 toward the row from the centre, 41 up from the bottom edge. Motor screw holes from the gearmotor's datasheet, centred on it.
4. Lower housing only: brush motor shaft hole 10 mm on the centre line, 122 up, with the brush motor's screw holes round it.
5. Three 4.5 mm holes in each flange, 6 from the outer edge.
6. The upper housing is the same with a back 236 x 79 and the drive motor hole only.

**How it fits the parts next to it.** The open side faces the plate's outer face; the flanges screw to the plate with M4 screws and the rim sits flat on the plate all round. The drive gearmotor bolts face-on to the outer wall and its shaft joins the axle through a 6 to 10 mm coupling (Figure 4). At the lower truck the brush gearmotor bolts above it and drives the brush shaft through a 1:1 toothed belt in a second layer (Figure 16).

**Check before moving on.** The tray sits flat on the plate all round; both belts turn by hand without touching the walls.

### 3.3 Guide roller clevises (make 4)

![Figure 6. Making sketch of the guide roller clevis](../cad/drawings/DRN-DWG-103.png)

*Figure 6. Guide roller clevis making sketch (DRN-DWG-103).*

**What it is and what it is made from.** A small U bracket that carries a guide roller against the frame's outer face. Aluminium sheet 3 mm, 5052.

**How to make it.**

1. Cut four strips 22 x 69. Fold each 90° at 20 and 49 to make a U with a 29 mm back and two 20 mm arms.
2. Drill one 8.5 mm hole through both arms, 17 from the outside of the back, on the centre line, with the arms clamped together.
3. Drill two 4.5 mm holes in the back, 8 from each end.

**How it fits the parts next to it.**

![Figure 7. Joint 2: guide roller in its clevis](05-build-plan/joint-02.png)

*Figure 7. Cut through the roller: the clevis back on the plate, the roller between the arms on its bolt, bearing on the frame's outer face.*

The back screws flat to the plate's inner face, 60 each side of the centre line, from 50 to 79 up. The 22 mm roller turns between the arms on an M8 bolt, head up and nyloc nut below; it bears on the frame's outer face and stands 6 mm off the plate. The upper arm stays 5 mm clear of the frame's top corner.

**Check before moving on.** The roller turns freely and the arms are parallel.

### 3.4 Hook sliders and spring seats (make 2 of each)

![Figure 8. Making sketch of the hook slider and spring seat](../cad/drawings/DRN-DWG-104.png)

*Figure 8. Hook slider and spring seat making sketch (DRN-DWG-104).*

**What it is and what it is made from.** The sliding block that holds the hook roller up under the frame's bottom flange, and the bracket its spring pushes from. Aluminium plate 10 mm (slider); 3 mm sheet (seat); 8 mm silver-steel rod (axle).

**How to make it.**

1. Slider: cut 40 x 30 from 10 mm plate. Ream an 8 mm hole on the centre line, 15 up from the bottom.
2. Cut two slots 6.5 wide and 14 tall, 13 each side of the centre line, centred 15 up: chain drill and file.
3. Axle: cut 8 mm silver steel 51 long; cut an e-clip groove 2 from one end. Press the other end 10 mm into the slider with retaining compound.
4. Seat: fold 3 mm sheet 30 wide into an angle with an 18 mm leg and a 9 mm shelf; two 4.5 mm holes in the leg.

**How it fits the parts next to it.**

![Figure 9. Joint 3: hook roller under the frame flange](05-build-plan/joint-03.png)

*Figure 9. Cut on the centre line: slider on the plate, the roller under the frame's bottom flange, the spring below the slider.*

The slider sits flat on the plate's inner face on two M6 shoulder bolts through its slots, free to slide about 8 mm up and down. The 16 x 18 mm roller turns on the axle under the frame's bottom flange, 3 to 21 from the frame's outer face; the axle passes 4 mm under the frame web. The seat screws to the plate below the slider and a compression spring about 9 mm across stands between them. Choose the spring to give 60 N at 20 mm long (about 3 N/mm); the robot weighs more than the concept, so 60 N, not 70 N, keeps each wheel at 60 N or less.

**Check before moving on.** The slider moves by hand without binding; the roller is square to the slider.

### 3.5 IR sensor brackets (make 4: two right-hand, two left-hand)

![Figure 10. Making sketch of the IR sensor bracket](../cad/drawings/DRN-DWG-105.png)

*Figure 10. IR sensor bracket making sketch (DRN-DWG-105).*

**What it is and what it is made from.** A folded bracket that holds an edge sensor ahead of each wheel, looking down at the frame's top flange. Aluminium sheet 3 mm, 5052.

**How to make it.**

1. Cut a blank: a top 40 x 49 with an 18 x 23 tab on one long edge, at the end nearest the plate centre. Make two, and two mirror images.
2. Fold the tab down 90°. Drill two 4.5 mm holes in the tab, 9 apart, on its centre line.
3. Drill the top for the sensor's own screws at its outer end.

**How it fits the parts next to it.** The tab screws to the plate's inner face at each end of the plate, 140 to 158 up; the top runs inward over the frame and the sensor hangs from it, its lens 44 mm above the frame's top flange, over the wheel track. The top clears the wheel by 12 mm. At the far end the sensor passes 5 mm over the end stop (Figure 32).

**Check before moving on.** The sensor sits square over the flange, 3 to 21 from the frame's outer face.

### 3.6 Contact and latch bracket (make 1, lower truck only)

![Figure 11. Making sketch of the contact and latch bracket](../cad/drawings/DRN-DWG-106.png)

*Figure 11. Contact and latch bracket making sketch (DRN-DWG-106).*

**What it is and what it is made from.** A twice-folded bracket at the dock end of the lower plate that carries the robot's contact block and the latch solenoid. Aluminium sheet 3 mm, 5052.

**How to make it.**

1. Mark one blank: a 27 x 62 leg; a 46 x 38 wing on the dock end of the leg; a 27 x 30 shelf on its top. Fold the wing 90° inward and the shelf 90° inward.
2. Leg: two 4.5 mm holes, 13 from the dock end, 12 and 52 up from its bottom edge.
3. Shelf: a 7 mm hole for the latch pin, 15 from the dock end and 17 in from the plate; the solenoid's screw holes from its datasheet.
4. Wing: holes for the robot contact block (an 8 mm insulating block of HDPE or PTFE carrying three copper strips) on its dock-facing side.

**How it fits the parts next to it.** The leg screws to the lower plate's inner face at the dock end, 168 to 230 up. The contact block faces the dock; the solenoid stands on the shelf with its 6 mm pin pointing down through the hole. When the robot parks, the pin drops through the dock's latch tab (Figure 30).

**Check before moving on.** The pin drops through the shelf hole without rubbing when the solenoid is off and lifts clear when it is energised from a 12 V bench supply.

### 3.7 Chassis beam (make 1)

![Figure 12. Making sketch of the chassis beam](../cad/drawings/DRN-DWG-107.png)

*Figure 12. Chassis beam making sketch (DRN-DWG-107).*

**What it is and what it is made from.** The backbone that spans between the trucks and carries the hood, pack, controller and sunshade. Aluminium rectangular tube 40 x 80 x 2 mm, 6063-T6.

**How to make it.**

1. Cut 2,334 long with square ends (the module length plus 56; for another module length, cut that length plus 56).
2. At each end, two 6.5 mm holes across both side walls, 17 from the end, 25 and 55 up from the bottom face.
3. Bottom face: five M5 rivet nuts on the centre line, 328, 788, 1,167, 1,546 and 2,006 from the lower end, for the hood spacers.
4. Top face: four M5 rivet nuts, 12 each side of the centre line, 266 and 660 from the lower end, for the sunshade posts; and holes for the controller box screws, about 523 and 633 from the lower end, to suit the box.

**How it fits the parts next to it.**

![Figure 13. Joint 4: beam end on the truck plate](05-build-plan/joint-04.png)

*Figure 13. Seen from inside: a cleat each side of the beam end, through-bolted across the beam and bolted to the plate.*

The 80 mm side stands normal to the glass; the beam's ends sit square against the plates' inner faces, its bottom face 3 mm above the hood.

**Check before moving on.** Length within 1 mm; the end holes are square across the tube.

### 3.8 Beam end cleats (make 4)

![Figure 14. Making sketch of the beam end cleat](../cad/drawings/DRN-DWG-108.png)

*Figure 14. Beam end cleat making sketch (DRN-DWG-108).*

**What it is and what it is made from.** A short angle each side of each beam end that bolts the beam to its truck plate. Aluminium equal angle 30 x 30 x 3 mm.

**How to make it.**

1. Cut four 70 mm lengths; deburr.
2. Leg on the beam: two 6.5 mm holes, 17 from the face that sits on the plate, 20 and 50 from the bottom end.
3. Leg on the plate: two 6.5 mm holes, 17 from the outside of the corner, 20 and 50 from the bottom end.
4. Drill each pair together so the holes match.

**How it fits the parts next to it.** One cleat each side of each beam end (Figure 13). One M6 bolt across the beam passes through both cleats at each hole, and two M6 bolts through each cleat go into the plate.

**Check before moving on.** The beam end sits square and tight on the plate with no gap.

### 3.9 Brush core, end plugs and stub shafts

![Figure 15. Making sketch of the brush core, plugs and shafts](../cad/drawings/DRN-DWG-109.png)

*Figure 15. Brush core, plugs and shafts making sketch (DRN-DWG-109).*

**What it is and what it is made from.** The rotating core that carries the microfiber sleeve. Aluminium tube 50 x 2 mm (core); aluminium bar 50 mm (plugs); steel bar 20 mm (shafts). The plugs and the lower shaft are turned on a lathe (a local turning shop).

**How to make it.**

1. Core: cut 2,218 mm of tube; square and deburr the ends.
2. Plugs (2): turn 46 outside, 20 long, with a 20 mm bore. Press one flush into each core end with retaining compound and fix with two M5 screws through the tube.
3. Upper shaft: 20 mm steel, 76 long; press 20 into the upper plug.
4. Lower shaft: 120 long, 20 mm for 83 (20 of it in the plug), then turned to 15 mm for 37 at the outer end with a 5 mm key flat for the pulley. Press it into the lower plug.
5. Slide on the microfiber sleeve (2,198 long), 10 in from each core end; a hose clip at each end holds it.

**How it fits the parts next to it.**

![Figure 16. Joint 5: brush shaft at the lower truck](05-build-plan/joint-05.png)

*Figure 16. Cut through the brush axis: plug in the core, shaft through the flange bearing and the plate, pulley and belt inside the drive housing.*

Each shaft runs in a 20 mm 2-bolt flange bearing on the plate's inner face. The lower shaft passes through the plate into the drive housing, where its pulley sits in the second belt layer, 2.5 mm clear of the wheel belt. The brush axis sits 55.5 above the glass, so the 120 mm sleeve presses 4.5 mm into the glass plane at the bearings.

**Check before moving on.** Spun between centres, the core runs true within 1 mm.

### 3.10 Brush hood (make 1)

![Figure 17. Making sketch of the brush hood](../cad/drawings/DRN-DWG-110.png)

*Figure 17. Brush hood making sketch (DRN-DWG-110).*

**What it is and what it is made from.** A rolled cover over the top of the brush that keeps thrown dust off clean glass and guards the brush ends. Aluminium sheet 0.8 mm, 5052; end guards 1 mm.

**How to make it.**

1. Cut a strip 189 wide x 2,208 long. Roll it to a 76 mm inside radius on a sheet-metal shop's slip roll (or bend it round a 150 mm pipe) so it covers 142° of the brush.
2. End guards (2): 1 mm sheet, the shape of the hood's end (145 wide, 52 tall), with folded tabs; rivet one inside each end, 5 in from the end.
3. Drill five 5.5 mm holes along the top centre line at the beam's spacer positions (Section 3.7).

**How it fits the parts next to it.**

![Figure 18. Joint 6: hood and sunshade on the beam](05-build-plan/joint-06.png)

*Figure 18. Cut across the beam: the hood hangs on 3 mm spacers below the beam; the sunshade stands on posts 6 mm over the pack.*

M5 screws pass up through the hood and a 3 mm nylon spacer into the rivet nuts in the beam's bottom face. The hood's edges sit 25 above the brush axis and its inside is 16 mm clear of the brush all along.

**Check before moving on.** Turn the brush by hand: nothing touches.

### 3.11 Sunshade and posts

![Figure 19. Making sketch of the sunshade and posts](../cad/drawings/DRN-DWG-111.png)

*Figure 19. Sunshade and posts making sketch (DRN-DWG-111).*

**What it is and what it is made from.** A sheet that shades the pack and controller. Aluminium sheet 1 mm, white; aluminium tube 12 x 3 mm for the posts.

**How to make it.**

1. Cut the shade 120 x 410; round the corners. Drill four 5.5 mm holes, 12 each side of the centre line, 8 in from each short end.
2. Cut four posts from 12 mm tube, 100 long, ends square.

**How it fits the parts next to it.** An M5 screw 120 long passes through the shade and each post into a rivet nut in the beam's top face (Figure 18). The shade stands 6 mm above the pack so air can move under it.

**Check before moving on.** The shade is level and clears the pack and the controller box.

### 3.12 Dock rails (make 2)

![Figure 20. Making sketch of the dock rail](../cad/drawings/DRN-DWG-112.png)

*Figure 20. Dock rail making sketch (DRN-DWG-112).*

**What it is and what it is made from.** The two short rails the robot parks on, continuing the module frame's profile past the end of the row. Aluminium channel 33 x 25 x 2.5 mm, or an offcut of the same module frame.

**How to make it.**

1. Cut two 780 mm lengths of channel the same outside size as the module frame: 33 deep with a 25 mm top flange.
2. File both ends square; chamfer the row end of the top and bottom flanges 1 mm so the wheels and hook rollers roll on.
3. Web: two pairs of countersunk 5.5 mm holes, 20 and 700 from the outer (dock) end, 11 and 21 down from the top. The heads must sit flush, because the guide rollers run over them.

**How it fits the parts next to it.** Each rail lies in line with the module frame, its top level with the frame top and its outer face in line with the frame's outer face, with the same 20 mm gap as between modules. It sits on two rail brackets (Section 3.14).

**Check before moving on.** The top flange is straight within 1 mm.

### 3.13 Dock cross members (make 3)

![Figure 21. Making sketch of the dock cross member](../cad/drawings/DRN-DWG-113.png)

*Figure 21. Dock cross member making sketch (DRN-DWG-113).*

**What it is and what it is made from.** The three members across the slope that make the dock frame: the far member (panel end), the rail-start member and the near member (next to the first module). Aluminium square tube 40 x 40 x 2 mm, 6063.

**How to make it.**

1. Cut three 2,218 mm lengths (the module length less 60).
2. All three: 8.5 mm holes top to bottom on the centre line, 20 from each end.
3. Far and rail-start members: two 8.5 mm holes across, 10 below the top and 10 above the bottom, 270 and 1,918 from the lower end, for the legs; and 6.5 mm holes top to bottom 100, 600 and 2,138 from the lower end, for the ties.
4. Far member: holes for the charger box and the two mast U-bolts. Rail-start member: two 6.5 mm holes across, 30 from the lower end, for the contact post.

**How it fits the parts next to it.**

![Figure 22. Joint 7: dock rail on its bracket](05-build-plan/joint-07.png)

*Figure 22. Cut through the bolt: the bracket inside the rail, the spacer, and the cross member 6 mm below the rail.*

Each member's top is 6 mm below the rail's bottom flange and its end 30 mm inside the rail, so the robot's hook roller, which runs under the rail, never meets it.

**Check before moving on.** The three members are the same length within 1 mm.

### 3.14 Rail brackets (make 4), spacers and shims

![Figure 23. Making sketch of the rail bracket](../cad/drawings/DRN-DWG-114.png)

*Figure 23. Rail bracket, spacer and shim making sketch (DRN-DWG-114).*

**What it is and what it is made from.** The brackets that hold each rail from inside its channel. Aluminium sheet 4 mm, 5083; spacers from 8.5 mm plate; shims from 2.5 mm sheet.

**How to make it.**

1. Brackets: 4 mm sheet 40 wide, folded 90° to an L with a 67.5 mm foot and a 21 mm upright.
2. Foot: one 8.5 mm hole on the centre line, 47.5 from the outside of the upright.
3. Upright: two M5 tapped holes on the centre line, 10 and 20 up from the foot, to match the rail web holes.
4. Spacers (2, for the rail-start member): 40 x 40 x 8.5 with an 8.5 mm hole. Shims (2, for the near member): 40 x 40 x 2.5 with an 8.5 mm hole.

**How it fits the parts next to it.** The upright stands inside the rail against its web, held by two countersunk M5 screws through the web; the foot lies on the inside of the rail's bottom flange and runs out of the channel onto the spacer (rail-start member) or onto the shim on the clamp bar (near member). One M8 bolt goes down through foot, spacer or shim and clamp bar, and the cross member (Figure 22). Add shims under the foot until the rail top is level with the module frame top.

**Check before moving on.** The rail top lines up with the module frame top within 1 mm.

### 3.15 Frame clamps (make 2)

![Figure 24. Making sketch of the frame clamp](../cad/drawings/DRN-DWG-115.png)

*Figure 24. Frame clamp making sketch (DRN-DWG-115).*

**What it is and what it is made from.** The clamps that hold the dock to the first module's frame without drilling it. Aluminium flat bar 40 x 6 mm; sheet 2.5 mm.

**How to make it.**

1. Clamp bar: 40 x 6 flat bar, 165 long. 8.5 mm holes on the centre line, 20 from the dock end and 7.5 from the module end.
2. Jaw: 40 x 40 from 6 mm bar, with an 8.5 mm hole 32.5 from its inner end.
3. Spacer: 15 x 40 from 2.5 mm sheet, with an 8.5 mm hole to match.

**How it fits the parts next to it.**

![Figure 25. Joint 8: frame clamp on the first module](05-build-plan/joint-08.png)

*Figure 25. Cut through the bolts: the bar under the frame's bottom flange, the jaw on top of it inside the frame, one M8 bolt; the bar's dock end bolted to the near cross member.*

The bar lies under the first module's long-side frame flange, 30 to 70 in from the module's lower and upper corners, clear of the table's own clamps. The jaw lies on top of the flange inside the frame, the spacer beside the flange edge keeps the jaw level, and one M8 bolt pulls jaw and bar together.

**Check before moving on.** The clamp cannot be slid along the frame by hand.

### 3.16 Dock ties (make 3)

![Figure 26. Making sketch of the dock tie](../cad/drawings/DRN-DWG-116.png)

*Figure 26. Dock tie making sketch (DRN-DWG-116).*

**What it is and what it is made from.** Three members along the row that join the far and rail-start cross members; two carry the dock panel. Aluminium rectangular tube 40 x 20 x 2 mm, 6063.

**How to make it.**

1. Cut three 540 mm lengths.
2. 6.5 mm holes top to bottom on the centre line, 20 from each end.
3. On two of them, 6.5 mm holes to match the panel frame's mounting holes.

**How it fits the parts next to it.** The ties lie flat (40 wide) on top of the two cross members, 110, 610 and 2,148 up the slope from the lower module edge, bolted with M6 bolts. The panel bolts through its frame holes to the first two.

**Check before moving on.** The two panel ties are parallel within 1 mm.

### 3.17 Dock legs with foot plates (make 4)

![Figure 27. Making sketch of the dock leg](../cad/drawings/DRN-DWG-117.png)

*Figure 27. Dock leg making sketch (DRN-DWG-117).*

**What it is and what it is made from.** Four vertical legs that carry the dock frame. Aluminium square tube 40 x 40 x 2 mm; plate 6 mm for the feet.

**How to make it.**

1. For a lower glass edge 600 above level ground: two upper legs 1,396 long on the long side and 1,377 on the short side, and two lower legs about 700 and 681; the top of each is cut at 25° so it sits flush with the top of the cross member. On site, cut to suit so the rails line up with the module frames.
2. Two 8.5 mm holes across, to match the cross member's leg holes.
3. Foot plate 100 x 100 x 6; join leg and foot with an angle cleat and M6 bolts (or weld); two 10 mm holes for ground anchors.

**How it fits the parts next to it.**

![Figure 28. Joint 11: leg on the far cross member](05-build-plan/joint-11.png)

*Figure 28. As installed: the leg stands vertical beside the cross member's outer face, bolted through both.*

**Check before moving on.** Each leg stands plumb within 1°.

### 3.18 Contact post, dock contacts and latch tab

![Figure 29. Making sketch of the contact post, dock contacts and latch tab](../cad/drawings/DRN-DWG-118.png)

*Figure 29. Contact post, dock contacts and latch tab making sketch (DRN-DWG-118).*

**What it is and what it is made from.** The post at the rail start that carries the dock's contact block and the latch tab. Aluminium tube 40 x 20 x 2 mm (post); HDPE or PTFE (contact block); 6 mm aluminium plate (tab).

**How to make it.**

1. Post: cut 206 long; two 6.5 mm holes across at the bottom, to bolt to the rail-start cross member's row side.
2. Contact block: 20 x 77 x 38 of HDPE or PTFE, drilled for the three spring contacts (charge positive, charge negative, anemometer signal) and screwed to the post's lower side at the top.
3. Latch tab: 65 x 30 from 6 mm plate, with a 7 mm hole 45 from the block end; chamfer the underside of the free end 45° so the robot's pin rides up onto it. Screw it on top of the block.

**How it fits the parts next to it.**

![Figure 30. Joint 9: dock contacts and latch, robot parked](05-build-plan/joint-09.png)

*Figure 30. Seen from inside with the truck plate left out: the contact blocks 2 mm apart, closed by the spring contacts; the pin through the tab.*

When the robot parks, its contact block stops 2 mm from the dock's block, which the spring contacts close; its pin rides up the chamfer and drops through the tab's hole. To leave, the robot lifts the pin for about a second.

**Check before moving on.** Each spring contact moves 3 mm freely; the tab hole lines up with the pin when the robot is pushed home by hand.

### 3.19 End stops (make 2)

![Figure 31. Making sketch of the end stop](../cad/drawings/DRN-DWG-119.png)

*Figure 31. End stop making sketch (DRN-DWG-119).*

**What it is and what it is made from.** A clamp-on stop at the far end of the row on the lower and upper frame edges, the mechanical backstop to the IR sensors. Aluminium bar 40 x 25 and 40 x 12 mm; rubber 5 mm.

**How to make it.**

1. Cut a top block 40 x 25 x 39, an outer plate 40 x 12 x 86 and a bottom jaw 40 x 25 x 12.
2. Screw the outer plate to the top block and to the jaw with two M6 screws each, leaving a 35 mm gap between block and jaw.
3. Tap an M8 hole through the jaw on its centre, 12.5 from the plate.
4. Glue a 5 mm rubber buffer, 25 x 34, to the face of the top block that faces the robot.

**How it fits the parts next to it.**

![Figure 32. Joint 10: end stop on the last module](05-build-plan/joint-10.png)

*Figure 32. The stop clamps round the frame edge; the wheel meets the buffer and the sensor passes 5 mm over the stop.*

Slide the stop over the last module's frame edge at the row end: top block on the top flange, outer plate down the frame's outer face, jaw under the bottom flange. Tighten the M8 clamp screw up against the flange. Its top is 40 above the glass, so the sensors pass over it and the wheels meet the buffer.

**Check before moving on.** The stop cannot be pulled along the frame by hand.

### 3.20 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Microfiber sleeve and brush bearings (line 2).** Helical microfiber sleeve 120 mm outside for a 50 mm core, 2,198 long; two 20 mm bore 2-bolt flange bearing units with locking collars.
- **Brush gearmotor and drive (line 4).** 12 V DC gearmotor about 60 W, about 150 rpm out, face mounting; two HTD 3M pulleys and a belt for a 1:1 drive about 62 mm between centres.
- **Wheels and drive (line 5).** Four 70 x 18 mm polyurethane wheels with a 10 mm bore and a set screw or key; eight 10 mm bore 2-bolt pressed-steel flange bearings; four 10 mm steel axles; HTD 3M pulleys and a belt for 180 mm between centres per truck; two 6 to 10 mm shaft couplings.
- **Drive gearmotors (line 6).** Two 12 V 37 mm gearmotors with Hall encoders, about 10 W, face mounting.
- **Rollers and springs (line 7).** Four 22 mm guide rollers about 23 long with sealed bearings for an M8 bolt; two 16 mm hook rollers about 18 long for an 8 mm axle; two compression springs about 9 mm across giving 60 N at 20 mm; four M6 shoulder bolts.
- **Pack (line 8).** 12.8 V 10 Ah LiFePO4 pack with a BMS that cuts charging below 0 °C and above 45 °C, about 151 x 65 x 94 mm.
- **Controller (line 9).** ESP32-class board, a dual motor driver and a brush motor driver, current sensing, a humidity and temperature sensor and a driver for the latch solenoid, in an IP65 box about 140 x 80 x 55 mm with cable glands.
- **IR sensors (line 10).** Four sealed downward-looking reflective IR sensors.
- **Dock panel (line 12).** 20 W monocrystalline, about 530 x 350 mm, with mounting holes in its frame.
- **Charger, contacts and latch (line 13).** LiFePO4 solar charge controller about 5 A with a 14.4 V charge limit; three spring contacts with 3 mm travel; three copper contact strips; a 12 V spring-return pull solenoid with a 6 mm steel plunger and about 10 mm stroke.
- **Wiring and hardware (line 15).** Silicone wire, a 15 A fuse, a main switch, two latching emergency stop buttons for a 22 mm hole, M5 rivet nuts, stainless fasteners, cable ties, two pack straps.
- **Anemometer (line 16).** Cup anemometer with a pulse output, 0 to 30 m/s, on a 24 mm mast, and two U-bolt clamps.

#### 3.20.1 Wiring

![Figure 33. Block-level wiring](05-build-plan/wiring.png)

*Figure 33. Block-level wiring with wire sizes. No circuit board is laid out; bought modules are wired together.*

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Pack to the 15 A fuse and main switch, then through the two stop buttons in series to the power bus (a small terminal block): 2.5 mm². A stop button cuts all motor power.
2. Power bus to the motor drivers: 1.5 mm²; drivers to the three gearmotors: 1.5 mm².
3. Power bus to the controller: 0.5 mm²; power bus to the latch solenoid through its driver: 1.0 mm².
4. Controller to the drivers (speed signals), to the encoders, to the four IR sensors and to the solenoid driver: 0.25 mm².
5. Robot contact block to the pack's BMS charge port (charge positive and negative) and to the controller (anemometer signal).
6. In the dock: panel to the charge controller, charge controller to the dock contact block, and the anemometer's pulse lead to the third contact: 1.5 mm² for power.

**Check before moving on.** With the fuse out, every power wire reads open to the pack terminals; each stop button opens the motor feed; every wire is labelled.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 3 are done on both trucks; the pictures show the lower one.

### Step 1: axles and wheels onto each truck plate

![Step 1](05-build-plan/step-01.png)

Bolt a flange bearing to each face of the plate at each axle hole. Slide the axle through, fit the wheel on the inside and the pulley on the outside, and fit the belt. Lock the bearing collars and the wheel set screws.

### Step 2: guide and hook rollers onto each plate

![Step 2](05-build-plan/step-02.png)

Screw the two clevises to the inner face with their rollers on M8 bolts. Fit the hook slider on its two shoulder bolts, the spring seat below it and the spring between them. The springs set the hook preload; it is checked in step 13.

### Step 3: brush bearing, sensors, stop button and contact bracket

![Step 3](05-build-plan/step-03.png)

Bolt the brush flange bearing to the inner face, centred on the brush hole. Screw on the sensor brackets with their sensors. Fit the stop button through its hole from outside. On the lower plate only, screw on the contact bracket with the contact block and the latch solenoid.

### Step 4: beam onto the lower truck

![Step 4](05-build-plan/step-04.png)

Bolt the four cleats across the beam ends with M6 bolts. Set the beam on the lower plate's inner face and fit two M6 bolts through each lower cleat into the plate, snug.

### Step 5: brush, then the upper truck

![Step 5](05-build-plan/step-05.png)

Slide the brush's lower shaft into the lower bearing. Slide the upper truck's bearing over the upper shaft, bring the plate against the upper cleats and bolt it. Square the trucks to the beam, tighten every cleat bolt and lock the brush bearing collars. **Hold point:** the brush turns freely by hand.

### Step 6: drive housings and motors

![Step 6](05-build-plan/step-06.png)

Fit the brush pulley on the lower shaft and the brush gearmotor's pulley and belt. Bolt each gearmotor to its housing's outer wall, join the drive motor's shaft to its axle with the coupling, and screw each housing to its plate by its flanges.

### Step 7: hood onto the beam

![Step 7](05-build-plan/step-07.png)

Slide the hood in from the side over the brush. Fit the five M5 screws up through the hood and the 3 mm spacers into the beam's rivet nuts.

### Step 8: pack, controller and sunshade

![Step 8](05-build-plan/step-08.png)

Strap the pack to the beam's top, screw on the controller box and wire them as Figure 33, with the fuse out. Fit the four posts and the sunshade. **Hold point:** the wiring checks of Section 3.20.1 pass.

### Step 9: dock frame on the ground

![Step 9](05-build-plan/step-09.png)

Bolt two legs beside each of the far and rail-start cross members, and the three ties on top. Stand the frame at the start of the row, legs plumb.

### Step 10: near cross member and frame clamps

![Step 10](05-build-plan/step-10.png)

Lay the clamp bars across the top of the near cross member and slide their module ends under the first module's long-side frame flange, jaws on top of the flange inside the frame. Tighten the M8 bolt at each jaw.

### Step 11: dock rails onto the cross members

![Step 11](05-build-plan/step-11.png)

Screw the brackets inside the rails. Set each rail on its spacer (rail-start member) and its shim on the clamp bar (near member) and bolt through with M8 bolts. Add shims until each rail's top and outer face line up with the module frame with a 20 mm gap.

### Step 12: panel and charger

![Step 12](05-build-plan/step-12.png)

Bolt the panel to the two panel ties through its frame holes, and screw the charger box to the far cross member's row side.

### Step 13: robot onto the dock rails

![Step 13](05-build-plan/step-13.png)

Two people. Push the hook sliders down, slide the robot onto the rails from the dock's outer end with the wheels on the rail tops, the hook rollers under the bottom flanges and the guide rollers against the webs, then let the sliders up. Check each hook preload is 60 N (Section 5). **Hold point:** safety stop S5.

### Step 14: contacts, latch tab and anemometer

![Step 14](05-build-plan/step-14.png)

Bolt the contact post to the rail-start cross member, then the contact block and latch tab on it, lined up with the parked robot. Clamp the anemometer mast vertical to the far cross member and run its lead to the dock contact block.

### Step 15: end stops onto the last module

![Step 15](05-build-plan/step-15.png)

At the far end of the row, slide a stop over the lower and the upper frame edge of the last module and tighten each M8 clamp screw against the bottom flange. **Hold point:** safety stop S7.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of DRN-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Robot mass | R10 | Weigh the robot before step 13 | Mass recorded, within 0.5 kg of the 15.9 kg estimate |
| Hook preload | R9, R10 | Spring scale under each hook slider | 60 N per truck, give or take 5 N |
| Brush interference | R3 | Robot on the first module, brush still; measure the core's height above the glass at both ends and mid-span | Core 30 to 32 mm above the glass (sleeve pressed 3 to 5 mm into the glass plane); nothing but the sleeve within 10 mm of the glass |
| Frame fit | R4 | Push the robot by hand over the first module joint and along one module | Wheels stay on the flange; guide rollers stay on the web; no step stops it |
| Drives and stop buttons | R12 | Bench supply at 12.8 V in place of the pack, 5 A limit; run the brush and drives; press each stop button | Everything stops within 2 s; the brush ends are guarded |
| End stop | R9 | Drive slowly into the end stop with the IR sensors covered | The wheels meet the buffers; nothing else touches the stop |
| Latch | R9 | Drive into the dock; pull the robot toward the row by hand | The pin drops through the tab and holds; the solenoid lifts it |
| Dock charge | R8 | Panel in sun or a bench supply in its place; measure at the robot's contacts | Charge current flows only when parked; charge stops at 14.4 V |
| Anemometer | R9 | Spin the cups by hand; read the signal at the robot | The controller reads the pulses through the third contact |
| Coverage | R5 | Run once over a module dusted with flour | 98 % or more of the glass brushed |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the pack comes into the workshop.** Pack voltage about 12.8 to 13.4 V; no swelling, dents or damage; a datasheet from its maker showing the BMS and its 0 °C and 45 °C charge cut-offs. Fuse out. A charging spot ready on a non-combustible surface with a fire extinguisher for electrical fires within reach.
- **S2. Before the fuse goes in.** All wiring checks of Section 3.20.1 pass. Polarity at the pack and the drivers checked with a meter, not by wire colour.
- **S3. Before the motors first run.** Robot on stands with the wheels off the ground; drive housings fitted over the belts; hood fitted; hair tied back, no loose clothing; both stop buttons tested on a bench supply with a 5 A limit.
- **S4. Before the dock charges the pack.** The charge controller is set to the LiFePO4 profile (14.4 V) and measured at the contacts with the pack out; the pack's charge cut-offs are confirmed.
- **S5. Before the robot goes on the dock rails.** The dock is clamped to the first module and its legs are on firm ground; the array owner has agreed to the work and their electrical safety rules are followed; nothing on the robot or dock can reach array cables, connectors or junction boxes; gloves on (glass and frames can reach about 75 °C).
- **S6. Before the robot first leaves the dock under power.** The pack fuse is in; the IR sensors stop the drives when covered; the latch lifts and drops; the wind at the anemometer is below 6 m/s.
- **S7. Before the first run along the row.** Both end stops fitted and tight; nobody below or beside the row; one person at the dock lockout and one at the far end, each able to reach a stop button; the first runs are watched end to end.
- **S8. Before any unattended run (outside this plan).** A warning label on the robot, an audible start warning and a lockout switch at the dock are fitted, and the module maker's cleaning and frame-load guidance has been checked.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade, or a bandsaw; bench vice with soft jaws; bench drill or a drill in a stand; drills 3 to 22 mm and a step drill; countersink; M4, M5, M6 and M8 taps; rivet-nut tool; files and a deburring tool; scriber, engineer's square, protractor, steel rule and calipers; feeler gauges; sheet-metal brake for 2 and 3 mm aluminium up to 240 mm long (or a sheet-metal shop); access to a lathe for the core plugs and lower shaft (or a turning shop); slip roll for the hood (or a shop); hand rivet tool; torque wrench; spring scale to 10 kg; digital angle finder and spirit level; ferrule crimper and wire strippers; multimeter; bench power supply 0 to 15 V, 0 to 5 A with a current limit; two stands to hold the robot off the ground.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, tapping, folding sheet), screw-terminal wiring and crimping, safe use of a bench power supply and care with lithium packs. All robot circuits are extra-low voltage (12.8 V pack, about 22 V from the dock panel); no mains wiring is part of this build. Work near the array follows the array owner's electrical safety rules.

**Workspace.** A bench about 2.5 m long, or two trestles, for the robot; a metalwork corner kept apart from the electronics; the charging spot of S1. For steps 9 to 15, a PV table with clear short edges, with the owner's agreement.

**Personal protective equipment.** Safety glasses for cutting, drilling and folding; cut-resistant gloves for plate and sheet; heat-resistant gloves at the array in daylight; hearing protection when sawing; no gloves near a turning drill or lathe.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 123 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/DRN-DWG-101` to `DRN-DWG-119`.
- General arrangement: `cad/drawings/DRN-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (DRN-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; mass [A3], [A4], hook preload [C0], wheel loads [C1], [C2], wind and latch [D1], [D2], end stop [D4], energy [F1] to [F7], cost [I1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (DRN-DDR-003), with DRN-DDR-001 and DRN-DDR-002; open decisions in `docs/06-design-decisions.md` (DRN-DEC-001).
- Requirements: `docs/03-requirements.md` (DRN-REQ-001 v0.5).
