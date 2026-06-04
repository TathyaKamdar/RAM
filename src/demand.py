# demand.py
# Generates synthetic weekly demand per config → data/processed/config_demand.csv
#
# Pipeline:
#   1. Load Google Trends CSV
#   2. Parse dates, set as index
#   3. STL decompose → extract seasonal component   ← YOUR LOGIC
#   4. Normalize seasonal index around 1.0           ← YOUR LOGIC
#   5. Expand monthly → weekly (52 weeks)            ← YOUR LOGIC
#   6. Apply baseline units + config split           ← YOUR LOGIC
#   7. Apply growth trend                            ← YOUR LOGIC
#   8. Add Gaussian noise                            ← YOUR LOGIC
#   9. Output config_demand.csv

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from config import (
    CONFIG_NAMES, CONFIG_SPLIT, FIRM_WEEKLY_UNITS,
    PLANNING_WEEKS, TREND_GROWTH, NOISE_STD
)

# ── Toggle between synthetic and real data ───────────────────────────────────
USE_REAL = False   # Flip to True once google_trends_laptop.csv is in data/raw/

RAW_DIR       = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
TRENDS_FILE   = RAW_DIR / "google_trends_laptop.csv"


def load_trends() -> pd.Series:
    """Load Google Trends CSV and return a monthly Series indexed by date."""
    # YOUR CODE HERE
    # Steps:
    #   - Read TRENDS_FILE with pd.read_csv()
    #   - Parse the date column with pd.to_datetime()
    #   - Set date as index
    #   - Return the 'Laptop' column as a Series
    raise NotImplementedError("load_trends() not implemented yet")


def get_seasonal_index(series: pd.Series) -> pd.Series:
    """
    Run STL decomposition and return a normalised weekly seasonal index.
    Input:  monthly Series (full date range from Trends CSV)
    Output: weekly Series of length 52, values centred around 1.0
    """
    # YOUR CODE HERE
    # Steps:
    #   - Filter to clean period (2021-2024, exclude RAMmageddon spike)
    #   - Run STL with period=12
    #   - Extract seasonal component
    #   - Average by month across years → 12 values
    #   - Normalise by dividing by mean
    #   - Expand to 52 weekly values using resample + interpolate
    raise NotImplementedError("get_seasonal_index() not implemented yet")


def make_stand_in_seasonal() -> np.ndarray:
    """
    Stand-in seasonal index when USE_REAL=False.
    Manually encodes known consumer electronics seasonality:
      - Aug bump (back to school)
      - Nov-Dec spike (holiday)
      - Jan-Feb dip (post-holiday)
    Returns a numpy array of 52 weekly multipliers centred around 1.0
    """
    monthly = np.array([
        0.85, 0.83, 0.90, 0.92, 0.95, 0.97,
        1.00, 1.08, 1.05, 0.98, 1.15, 1.20
    ])
    # Repeat monthly values across weeks, then trim/pad to 52
    weekly = np.repeat(monthly, [4,4,4,5,4,4,4,5,4,4,5,5])[:52]
    return weekly / weekly.mean()


def generate_demand(seasonal_index: np.ndarray) -> pd.DataFrame:
    """
    Apply baseline × trend × seasonal × noise to produce
    weekly demand per config.
    Returns DataFrame with columns: week, config, demand_units
    """
    # YOUR CODE HERE
    # Steps:
    #   - For each week t in range(PLANNING_WEEKS):
    #       growth = (1 + TREND_GROWTH) ** (t / 52)
    #       For each config:
    #           base    = FIRM_WEEKLY_UNITS * CONFIG_SPLIT[config]
    #           noise   = np.random.normal(1.0, NOISE_STD)
    #           units   = base * growth * seasonal_index[t] * noise
    #           Append row (week=t+1, config=config, demand_units=round(units))
    raise NotImplementedError("generate_demand() not implemented yet")


def main():
    np.random.seed(42)   # reproducibility
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if USE_REAL:
        print("Loading real Google Trends data...")
        series = load_trends()
        seasonal = get_seasonal_index(series)
        seasonal = seasonal.values
    else:
        print("USE_REAL=False → using stand-in seasonal pattern")
        seasonal = make_stand_in_seasonal()

    print("Generating demand...")
    df = generate_demand(seasonal)

    out_path = PROCESSED_DIR / "config_demand.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")
    print(df.head(8))


if __name__ == "__main__":
    main()
