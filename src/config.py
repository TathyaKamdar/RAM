# config.py
# Central config for RAM planning engine
# All constants live here — import this everywhere else

# ── Product configurations ──────────────────────────────────────────────────
# Each config: (RAM_GB, GPU_units, SSD_GB, Chassis_units)
CONFIGS = {
    "Base":   {"ram_gb": 8,  "gpu": 0, "ssd_gb": 512,  "chassis": 1},
    "Mid":    {"ram_gb": 16, "gpu": 0, "ssd_gb": 1024, "chassis": 1},
    "Gaming": {"ram_gb": 32, "gpu": 1, "ssd_gb": 1024, "chassis": 1},
    "Pro":    {"ram_gb": 32, "gpu": 1, "ssd_gb": 2048, "chassis": 1},
}

CONFIG_NAMES = list(CONFIGS.keys())

# ── Demand baseline (IDC 2024 + Steam Hardware Survey) ──────────────────────
# IDC 2024: 262.7M global PC shipments
# Firm market share: 0.5% (realistic small-mid configurable PC maker)
# Monthly: 262.7M × 0.005 / 12 = 109,458 units/month
FIRM_MONTHLY_UNITS = 109_458

CONFIG_SPLIT = {
    "Base":   0.09,   # Steam Survey 8GB tier, normalized
    "Mid":    0.49,   # Steam Survey 16GB tier, normalized
    "Gaming": 0.27,   # Steam Survey 32GB tier, 2/3 split (mass market)
    "Pro":    0.15,   # Steam Survey 32GB tier, 1/3 split (premium niche)
}

# ── Demand generation parameters ────────────────────────────────────────────
PLANNING_PERIODS = 12           # monthly planning horizon
TREND_GROWTH     = 0.02         # IDC ~2% annual PC market CAGR 2024-2028
NOISE_STD        = 0.10         # 10% Gaussian noise — typical electronics demand variation

# ── Laptop selling prices (2024 baseline, pre-shortage) ─────────────────────
# Anchored to real 2024 market prices by tier
# Base  → Acer Aspire 3 / Lenovo IdeaPad range
# Mid   → HP Pavilion / Dell Inspiron range
# Gaming→ Lenovo Legion 5 / ASUS ROG range
# Pro   → Dell XPS 15 / premium workstation range
SELLING_PRICE = {
    "Base":   550,
    "Mid":    850,
    "Gaming": 1300,
    "Pro":    2400,
}

# ── Profit margin per unit ───────────────────────────────────────────────────
# Tiered gross margins anchored to Dell 2024 gross margin ~19% (MacroTrends)
# Higher-spec configs earn higher margins due to reduced price competition
# Base 14% → Mid 17% → Gaming 21% → Pro 26%
PROFIT_MARGIN = {
    "Base":   77,
    "Mid":    145,
    "Gaming": 273,
    "Pro":    624,
}

# ── Supplier specifications ──────────────────────────────────────────────────
# Two suppliers, both carry all RAM sizes
# Specialization expressed through price differential:
#   Supplier A → cheaper for 8GB/16GB (Base, Mid)
#   Supplier B → cheaper for 32GB (Gaming, Pro)
# Price per GB varies by RAM size — larger chips cheaper per GB
# (economies of scale in manufacturing)
SUPPLIERS = {
    "A": {
        "lead_time_days":      7,
        "monthly_capacity_gb": 500_000,
        "price_per_gb": {
            "Base":   5.50,   # 8GB DDR5 chips
            "Mid":    5.00,   # 16GB DDR5 chips
            "Gaming": 4.50,   # 32GB DDR5 chips
            "Pro":    4.50,   # 32GB DDR5 chips (same as Gaming)
        }
    },
    "B": {
        "lead_time_days":      10,
        "monthly_capacity_gb": 400_000,
        "price_per_gb": {
            "Base":   6.50,
            "Mid":    5.75,
            "Gaming": 4.25,
            "Pro":    4.25,
        }
    }
}

# Minimum consecutive months once a supplier contract is activated
MIN_CONTRACT_MONTHS = 3

# ── RAM cost stand-in (replaced by real Kaggle data when USE_REAL=True) ─────
RAM_COST_PER_GB_BASELINE = 5.0

# ── Shortage scenario parameters (RAMmageddon 2026) ─────────────────────────
# Source: reported DDR5 market data 2025-2026
#   price_multiplier → DDR5 prices ~doubled QoQ early 2026
#   supply_cut       → ~40% consumer DDR5 allocation reduction
#   lead_time_factor → lead times stretched ~2x
SHORTAGE = {
    "price_multiplier":  2.0,
    "supply_cut":        0.40,
    "lead_time_factor":  2.0,
}

# ── Lead times (weeks) ────────────────────────────────────────────────────────
# Industry-standard assumptions for consumer electronics components
# In production these would come from procurement data
LEAD_TIMES = {
    "ram":     8,   # DDR5 specialized, long procurement cycle
    "gpu":     4,   # moderate complexity
    "ssd":     3,   # commodity component
    "chassis": 2,   # near-shore manufacturing, fastest
}

# ── Safety stock (weeks of cover) ────────────────────────────────────────────
# RAM gets double buffer — highest risk, binding constraint component
SAFETY_STOCK_WEEKS = {
    "ram":     2,
    "gpu":     1,
    "ssd":     1,
    "chassis": 1,
}

# ── Shortage penalty ─────────────────────────────────────────────────────────
# Cost of one unmet laptop demand unit
# Derived from PC manufacturer operating margins 5-8% on ~$900 avg selling price
# $900 × 7% ≈ $63, rounded to $75 for conservatism
SHORTAGE_PENALTY_PER_UNIT = 75