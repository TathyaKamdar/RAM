# ram_prices.py
# Loads real DDR5 $/GB from Kaggle RAM pricing dataset
# Falls back to config.py constant when USE_REAL=False

import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from config import RAM_COST_PER_GB_BASELINE, SHORTAGE

USE_REAL = False   # Flip to True once Kaggle CSV is in data/raw/

RAW_DIR   = Path(__file__).parent.parent / "data" / "raw"
RAM_FILE  = RAW_DIR / "ram_pricing.csv"    # rename your Kaggle file to this


def load_real_ram_price() -> float:
    """
    Load Kaggle DDR5 RAM pricing dataset.
    Filter: DDR5, New, consumer, non-bulk.
    Return mean $/GB as a single float.
    """
    # YOUR CODE HERE
    # Steps:
    #   - Read RAM_FILE
    #   - Filter rows to DDR5, New condition, consumer grade, non-bulk
    #   - Calculate $/GB column if not already present
    #   - Return the mean $/GB
    raise NotImplementedError("load_real_ram_price() not implemented yet")


def get_ram_price(scenario: str = "baseline") -> float:
    """
    Return $/GB for the given scenario.
    scenario options: 'baseline', 'shortage'
    """
    if USE_REAL:
        base_price = load_real_ram_price()
    else:
        base_price = RAM_COST_PER_GB_BASELINE

    if scenario == "shortage":
        return base_price * SHORTAGE["price_multiplier"]
    return base_price


if __name__ == "__main__":
    print(f"Baseline RAM price: ${get_ram_price('baseline'):.2f}/GB")
    print(f"Shortage RAM price: ${get_ram_price('shortage'):.2f}/GB")
