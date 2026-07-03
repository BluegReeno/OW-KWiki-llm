---
type: Technology
title: HVDC Grid Connection
description: High-voltage direct current transmission — via offshore converter platforms and subsea export cables — used to bring power from large or distant offshore wind farms to shore.
tags: [hvdc, grid-connection, converter-platform, export-cable, transmission]
timestamp: 2026-07-02T00:00:00Z
---

# Overview

Offshore wind farms generate power as medium-voltage AC (typically 66 kV) at the turbine, which is stepped up and carried to shore either as high-voltage AC (HVAC) or converted to high-voltage direct current (HVDC) for transmission. HVDC becomes the economic choice once a farm sits roughly 80-100 km or more from its grid connection point, because HVAC cables suffer increasing reactive power losses over distance while HVDC losses stay low regardless of cable length. As farms move farther offshore and scale past 1 GW, HVDC has become the default choice for flagship projects such as [dogger-bank](/projects/dogger-bank.md), which uses HVDC Light technology.

# How It Works

An HVDC transmission system has three main components:

1. **Offshore converter platform**: collects AC power from the array's [offshore substations](offshore-substations.md), and converts it to DC (commonly ±320 kV) using large power-electronics converter modules. These platforms are among the heaviest, most expensive single structures in an offshore wind project.
2. **Subsea export cable**: carries DC power to shore. HVDC cables have lower losses and require only two (not three) conductor cores compared to HVAC, but subsea HVDC cable faults are costly to repair — industry data suggests roughly 0.07-0.10 faults per 100 km-years, with average repair times around 60 days, making export-cable reliability a material project risk.
3. **Onshore converter station**: converts DC back to AC and injects it into the national grid.

# Floating and Dynamic Cable Variants

Floating wind farms sited in deeper water need dynamic (flexible, motion-tolerant) export cables rather than static seabed cables, since the floating substation itself moves with wind and waves. Floating HVDC converter platforms are now in development — designs exist for units rated up to roughly 1.4 GW — to serve future large-scale floating clusters without requiring a fixed-bottom converter platform nearshore.

# Cross-References

- [offshore-substations.md](offshore-substations.md) — the AC collection stage upstream of HVDC conversion
- [floating-wind.md](floating-wind.md) — drives demand for dynamic HVDC cables
- [/projects/dogger-bank.md](/projects/dogger-bank.md), [/projects/hornsea-2.md](/projects/hornsea-2.md), [/projects/empire-wind-1.md](/projects/empire-wind-1.md) — HVDC-connected projects
- [/companies/orsted.md](/companies/orsted.md), [/companies/rwe-offshore-wind.md](/companies/rwe-offshore-wind.md), [/companies/equinor.md](/companies/equinor.md) — developers of HVDC-scale farms
- [/companies/aker-solutions.md](/companies/aker-solutions.md) — EPC supplier of HVDC converter platform substructures
- [/companies/ls-cable-system.md](/companies/ls-cable-system.md) — cable manufacturer building a US subsea export cable factory
- [/policy/uk-contracts-for-difference-scheme.md](/policy/uk-contracts-for-difference-scheme.md), [/policy/eu-offshore-wind-strategy.md](/policy/eu-offshore-wind-strategy.md)

# Citations

- [Transmission Systems for Grid Connection of Offshore Wind Farms (DiVA)](https://www.diva-portal.org/smash/get/diva2:1561060/FULLTEXT01.pdf)
- [Why HVDC Export Cables Are An Underappreciated Risk In Offshore Wind (CleanTechnica)](https://cleantechnica.com/2026/03/20/why-hvdc-export-cables-are-an-underappreciated-risk-in-offshore-wind/)
- [Dynamic HVDC export cables and floating substation for shallow water floating wind (IOPscience)](https://iopscience.iop.org/article/10.1088/1742-6596/3232/1/012008)
- [Offshore wind transmission explained (Business Norway)](https://businessnorway.com/articles/offshore-wind-transmission-this-is-how-wind-energy-is-transported)
