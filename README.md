# RAM — S&OP Planning Engine
### Tathya Kamdar | MS Industrial Engineering | Northeastern University
### Co-op Project | Supply Chain  | Jan 2027

---

## Overview

RAM is a Sales & Operations Planning (S&OP) engine that models how a configurable PC manufacturer should respond to the 2026 DDR5 memory shortage — a real, ongoing supply chain disruption where RAM prices have increased over 300% and lead times have doubled.

The project combines demand forecasting, constrained production planning via linear programming, and multi-supplier procurement optimization into a single end-to-end planning pipeline.

---

## The Problem

A PC manufacturer sells four configurable laptop tiers — Base, Mid, Gaming, and Pro — each consuming different amounts of DDR5 RAM. Because all configurations share the same RAM supply pool, a memory shortage cascades across the entire product line simultaneously.

The 2026 "RAMmageddon" shortage has made DDR5 the binding constraint for PC manufacturers:

- DDR5 prices increased ~300% from mid-2025 to early 2026
- Consumer DDR5 allocation cut by ~40% as manufacturers redirected capacity to AI server memory (HBM)
- Lead times stretched from ~8 weeks to ~16 weeks

The planning question becomes: **given scarce RAM, how should a manufacturer allocate it across configurations to maximize profit while minimizing unmet demand?**

---

## Product Configurations

| Config | RAM | GPU | SSD | Target Segment |
|---|---|---|---|---|
| Base | 8 GB DDR5 | None | 512 GB | Budget / Students |
| Mid | 16 GB DDR5 | None | 1 TB | Productivity / Work |
| Gaming | 32 GB DDR5 | Dedicated | 1 TB | Gaming / Content Creation |
| Pro | 32 GB DDR5 | Dedicated (High-end) | 2 TB | Professional Workstation |

---

## Three Objectives

### Objective 1 — Demand Forecasting
Generate a defensible synthetic monthly demand series for each configuration using real-world anchors:

- **Seasonal shape** → STL decomposition of Google Trends "laptop" search data (2021–2024)
- **Demand magnitude** → IDC 2024 global PC shipments (262.7M units), 0.5% firm market share
- **Config split** → Steam Hardware Survey RAM distribution (real monthly data)
- **Trend** → IDC projected PC market CAGR of ~2% (2024–2028)

Accuracy measured using MAPE (Mean Absolute Percentage Error).

**Why synthetic?** No public component-level PC demand data exists. The approach — decompose a real signal, extract its structure, rescale to fit — is standard practice in supply chain modeling when proprietary data is unavailable.

---

### Objective 2 — Constrained Production Planning (MIP)
A Mixed Integer Program (MIP) built in PuLP that determines the optimal monthly build plan under RAM supply constraints.

**Decision Variables:**
- `x[config, month]` — units of each configuration to build (48 variables)
- `y[supplier, config, month]` — GB of RAM to procure from each supplier
- `z[supplier, month]` — binary, whether a supplier contract is active (0 or 1)

**Objective:** Maximize total profit = revenue margins − RAM procurement cost

**Key Constraints:**
- RAM consumed ≤ RAM available from contracted suppliers
- Units built ≤ monthly demand per configuration
- Supplier contract minimum 3-month commitment (realistic take-or-pay contract)
- Non-negativity and binary constraints

**Supplier Design:**

| | Supplier A | Supplier B |
|---|---|---|
| Specialization | Base, Mid (8GB, 16GB) | Gaming, Pro (32GB) |
| Lead Time | 7 days | 10 days |
| Monthly Capacity | 500,000 GB | 400,000 GB |
| 8GB price/GB | $5.50 | $6.50 |
| 16GB price/GB | $5.00 | $5.75 |
| 32GB price/GB | $4.50 | $4.25 |

Prices anchored to real 2024 DDR5 consumer market pricing. Margins anchored to Dell's 2024 reported gross margin (~19%), tiered upward for higher-spec configurations.

---

### Objective 3 — Shortage Scenario Analysis
Rerun the optimizer under RAMmageddon conditions and compare outcomes:

| Parameter | Baseline (2024) | Shortage (2026) |
|---|---|---|
| RAM price | Market rate | 2× baseline |
| Supply available | 100% | 60% (40% cut) |
| Lead time | Normal | 2× normal |

Output: cost impact, service level degradation, which configurations get prioritized, and what the optimal build plan looks like under disruption.

---

## Data Sources

| Data | Source | Used For |
|---|---|---|
| PC shipments | IDC Global PC Tracker 2024 (262.7M units) | Demand magnitude |
| Seasonal pattern | Google Trends "laptop" (2021–2025) | Seasonal shape |
| Config split | Steam Hardware Survey — System RAM distribution | Base/Mid/Gaming/Pro % |
| RAM pricing | E-Commerce RAM Pricing Intelligence 2026 (Kaggle) | Optimizer cost input |
| Profit margins | Dell 2024 gross margin ~19% (MacroTrends) | LP objective function |
| Shortage params | Reported DDR5 market data (Tom's Hardware, Newegg, TrendForce) | Scenario analysis |

---

## Technical Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| PuLP | MIP optimizer |
| statsmodels (STL) | Seasonal decomposition |
| pandas / numpy | Data processing |
| matplotlib | Visualization |
| scikit-learn | MAPE scoring |

---

## Project Status

| Module | File | Status |
|---|---|---|
| Constants & BOM | `config.py` | ✅ Complete |
| Demand generation | `demand.py` | ✅ Complete — 48 rows output |
| RAM pricing | `ram_prices.py` | ⬜ Stand-in, pending Kaggle data |
| Demand forecast | `forecast.py` | ⬜ In progress |
| MIP Optimizer | `optimizer.py` | ⬜ In progress |
| Shortage scenarios | `scenarios.py` | ⬜ Pending optimizer |

---

## Repository Structure

```
RAM_PLAN/
├── src/
│   ├── config.py       # All constants, BOM, supplier specs, margins
│   ├── demand.py       # Synthetic demand generation → config_demand.csv
│   ├── ram_prices.py   # DDR5 $/GB from Kaggle dataset
│   ├── forecast.py     # Demand forecast + MAPE scoring
│   └── optimizer.py    # MIP production planning engine (in progress)
├── data/
│   ├── raw/            # Kaggle CSVs (not committed — licensing)
│   └── processed/      # config_demand.csv (generated)
├── outputs/            # Results, plots, scenario comparisons
├── requirements.txt
└── README.md
```

---

## Setup

```bash
git clone https://github.com/TathyaKamdar/RAM_PLAN.git
cd RAM_PLAN
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/demand.py
