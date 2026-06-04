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

# ── Demand baseline (from IDC 2024 + Steam Hardware Survey) ─────────────────
GLOBAL_WEEKLY_UNITS = 5_051_923   # IDC 262.7M / 52 weeks
MARKET_SHARE        = 0.005       # 0.5% of global market
FIRM_MONTHLY_UNITS = 109_458     # FIRM_MONTHLY_UNITS = GLOBAL_WEEKLY_UNITS * MARKET_SHARE * 4.33 weeks/month

CONFIG_SPLIT = {
    "Base":   0.09,
    "Mid":    0.49,
    "Gaming": 0.27,
    "Pro":    0.15,
}

# ── Demand generation parameters ─────────────────────────────────────────────
PLANNING_PERIODS = 12
TREND_GROWTH    = 0.02          # IDC 2% annual PC market growth
NOISE_STD       = 0.10          # 10% Gaussian noise std

# ── RAM cost ($/GB) — baseline DDR5, sourced from Kaggle RAM pricing dataset ─
RAM_COST_PER_GB_BASELINE = 5.0  # stand-in; flip USE_REAL in ram_prices.py

# ── Shortage scenario parameters (RAMmageddon 2026) ─────────────────────────
SHORTAGE = {
    "price_multiplier":  2.0,   # ~100% price increase QoQ
    "supply_cut":        0.40,  # 40% supply reduction
    "lead_time_factor":  2.0,   # 2x lead time increase
}

# ── Lead times (weeks) ────────────────────────────────────────────────────────
LEAD_TIMES = {
    "ram":     8,
    "gpu":     4,
    "ssd":     3,
    "chassis": 2,
}

# ── Safety stock (weeks of cover) ────────────────────────────────────────────
SAFETY_STOCK_WEEKS = {
    "ram":     2,
    "gpu":     1,
    "ssd":     1,
    "chassis": 1,
}
