# RAM — S&OP Planning Engine

> An S&OP planning engine that defends a configurable-PC maker's build plan
> against the 2026 RAM shortage — demand forecasting, constrained production
> planning, and multi-echelon inventory optimization.

## Problem
A PC manufacturer sells configurable laptops (Base, Mid, Gaming, Pro).
Many configs share the same DDR5 RAM pool. The 2026 RAMmageddon shortage
(~100% price spike, 40% supply cut, 2× lead times) makes RAM the binding
constraint across the entire product line.

## Three Objectives
| Objective | Technique | Output |
|---|---|---|
| 1 — Demand | Time-series forecasting | Predicted demand per config + MAPE |
| 2 — Production plan | Linear programming (PuLP) | Optimal build plan under RAM constraint |
| 3 — Shortage | Scenario / sensitivity analysis | Cost + service impact under disruption |

## Product Configurations
| Config | RAM | GPU | SSD |
|---|---|---|---|
| Base | 8 GB DDR5 | — | 512 GB |
| Mid | 16 GB DDR5 | — | 1024 GB |
| Gaming | 32 GB DDR5 | ✓ | 1024 GB |
| Pro | 32 GB DDR5 | ✓ | 2048 GB |

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```

## Running (synthetic data)
```bash
python src/demand.py           # generates data/processed/config_demand.csv
python src/ram_prices.py       # prints baseline and shortage $/GB
python src/forecast.py         # scores forecast accuracy
```

## Switching to Real Data
1. Drop Kaggle CSVs into `data/raw/`
2. Rename RAM pricing file to `ram_pricing.csv`
3. Rename Google Trends file to `google_trends_laptop.csv`
4. Flip `USE_REAL = True` in `demand.py` and `ram_prices.py`

## Data Sources
- **Demand backbone:** Google Trends "laptop" (2021–2025)
- **Magnitude anchor:** IDC Global PC Shipments 2024 (262.7M units)
- **Config split:** Steam Hardware Survey RAM distribution
- **RAM cost:** E-Commerce RAM Pricing Intelligence 2026 (Kaggle)
- **Shortage params:** RAMmageddon 2026 (~100% QoQ price, 40% supply cut)
