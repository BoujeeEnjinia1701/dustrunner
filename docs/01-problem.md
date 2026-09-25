---
doc_id: DRN-PRB-001
title: DustRunner problem statement
project: DustRunner
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
---

# DustRunner problem statement

Soiling cuts output of PV arrays in dusty regions by 15 to 25%, and water for washing is scarce. Utility-scale plants solve this with water-free cleaning robots, but small and mid-size ground-mounted arrays of tens of kilowatts, which are common on farms, mini-grids and commercial sites in the same regions, are still washed by hand with water or left dirty.

## The problem

Dust settles on PV glass every day. In desert climates the loss grows quickly between cleanings. Qatar's QEERI test facility measured a soiling rate of about 0.49 % per day on fixed-tilt modules, about 13 % a month without rain or cleaning, and losses of up to 60 % over long uncleaned periods ([PV Tech, "Challenges of PV soiling in desert climates"](https://www.pv-tech.org/challenges-of-pv-soiling-in-desert-climates/)). A 2026 study for Arar, Saudi Arabia, used monthly losses of 3 to 5 % in winter rising to 11 to 18 % in summer ([Alharbi, Energies 19(18) 4373](https://www.mdpi.com/1996-1073/19/18/4373)). The 15 to 25 % in the summary above is therefore typical of an array left for a month or more in the dusty season, not a year-round average.

Worldwide, soiling cost at least 3 to 4 % of solar production in 2018, about 3 to 5 billion euros of revenue, with 4 to 7 % projected for 2023 ([Ilse et al., Joule 3, 2303 to 2321, 2019](https://www.cell.com/joule/fulltext/S2542-4351(19)30422-2); [open access PDF](https://elib.dlr.de/129424/1/Joule-ils.pdf)).

Washing with water works but uses water where it is scarcest. Field trials found about 3.5 L to more than 10 L of water used to clean and rinse a single module ([Polywater, "Water consumption in PV panel cleaning"](https://www.polywater.com/wp-content/uploads/2021/08/SPW-Intl-blog-Water-Use-IndiaCA.pdf)). Manual cleaning also needs labor, so small owners stretch the interval: at low tariffs the cost-optimal manual interval can be 60 days or more ([Alharbi, 2026](https://www.mdpi.com/1996-1073/19/18/4373)), and the array runs dirty for most of that time.

The underlying gap is that each manual cleaning is expensive, so it happens rarely. A small robot that cleans dry every day changes that trade-off, provided it is cheap enough for one row and does not damage the glass.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Owner of a small ground-mounted array | More energy from the same array without buying water or hiring cleaners | Farms (solar irrigation pumping), mini-grids, schools and clinics, small commercial sites; 10 to 200 kW |
| O&M technician or site caretaker | A machine that runs itself, is easy to install on an existing row and is repairable with local parts | Visits the site weekly or less |
| Mini-grid or community solar operator | Predictable yield and lower operating cost in the dry season | Arrays of several rows, remote sites |
| Open hardware community | A documented, buildable reference design to adapt to other module and table sizes | Makerspaces, university labs, technical colleges |

Operating context assumed for the concept:

- **Climate:** hot, dry and dusty (for example the Middle East and North Africa, the Sahel, northwest India and the US Southwest). Ambient 0 to 50 °C, glass up to about 75 °C, nightly dew possible in coastal and desert areas.
- **Arrays:** fixed-tilt ground-mounted tables, one module high in portrait (1P), tilt 10 to 35°, rows 20 to 100 m long. Modules of about 2,278 x 1,134 mm with 30 to 35 mm aluminum frames are now common ([DAS Solar 590 W example](https://www.solar-hub.co.uk/products/590w-das-solar-n-type-grey-frame-2278-x-1134)).
- **Dust:** mostly dry, loose mineral dust between rain events. Cemented dust after dew, bird droppings and lichen are outside what dry brushing can remove.

## Prior work

- **Ecoppia** (Israel, India, United States): water-free robots that use microfiber elements and airflow, charge from their own onboard solar module and clean utility-scale rows nightly and autonomously ([Ecoppia technology](https://www.ecoppia.com/technology/)). Sold to large plants as a service.
- **NOMADD** (Saudi Arabia): the "NO-water Mechanical Automated Dusting Device", designed to clean every panel as often as daily in desert plants, at about 10 US cents per watt of added cost ([RenewEconomy](https://reneweconomy.com.au/desert-solar-panel-cleaners-water-free-88183/)).
- **SolarCleano F1** (Luxembourg): an 82 kg operator-moved robot with 1.2 m helical brushes, dry or wet, up to 1,200 m²/h, able to cross gaps up to 70 cm ([SolarCleano](https://www.solarcleano.com/products/remote-solarcleano-f1)). Suited to contractors, not to a single small row.
- **Academic prototypes:** for example a tracked robot with two helical brushes and ultrasonic sensing for desert PV ([Antonelli et al., Mechatronics, 2020](https://www.sciencedirect.com/science/article/abs/pii/S0957415820300520)).
- **Robotic cleaning cost** on utility-scale plants is about 2.4 to 8.2 € per m² of module area ([Ilse et al., 2019](https://elib.dlr.de/129424/1/Joule-ils.pdf)).

The gap DustRunner targets is an open, garage-buildable robot for one small row that installs without rails and costs less than one or two years of the energy it recovers.

## Constraints

- Garage-buildable prototype, about $500 USD for one robot and its dock, using off-the-shelf motors, aluminum sections and hobby electronics.
- Must not void or endanger module warranties. Manufacturers forbid abrasive cleaning and some require prior approval of motorized cleaning tools; First Solar, for example, reviews automated tools and gives no warranty for modules damaged by cleaning ([First Solar module cleaning guidelines](https://www.firstsolar.com/-/media/First-Solar/Technical-Documents/Series-4-Application-Note/Module-Cleaning-Guidelines.ashx?la=en)). Abrasion of anti-reflective coatings by robots is still being studied in the field ([PV Tech](https://www.pv-tech.org/challenges-of-pv-soiling-in-desert-climates/); [Ilse et al., 2019](https://elib.dlr.de/129424/1/Joule-ils.pdf)).
- No drilling of modules or of the mounting structure; only clamp-on parts.
- Works on an energized array. PV strings can carry DC voltages of several hundred volts, so the robot must never touch cables, connectors or junction boxes.
- No water and no consumables other than replaceable microfiber.

## Out of scope

- Utility-scale plants, single-axis trackers and rooftop arrays.
- Automatic transfer from row to row (one robot per row, or carried by hand).
- Wet cleaning, bird droppings and cemented soiling.
- A commercial cleaning service or fleet software.

## Open questions

- Which pilot site and partner to design with first (a solar pumping farm, a mini-grid operator or a university test array)? Proposed, awaiting Amish.
- Which module and table formats to support first? Proposed: 1P portrait tables of 2,278 mm modules, awaiting Amish.
- Is daily dry cleaning effective on the local dust, or does dew cementation limit it? This needs site dust data and later testing.
