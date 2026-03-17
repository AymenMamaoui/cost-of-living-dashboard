import pandas as pd
import os

def load_raw_data(path: str) -> pd.DataFrame:
    """Load raw CSV dataset and return a DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at: {path}")
    df = pd.read_csv(path)
    print(f"Dataset loaded — {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def load_processed_data(path: str) -> pd.DataFrame:
    """Load cleaned CSV dataset and return a DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed dataset not found at: {path}")
    df = pd.read_csv(path)
    print(f"Processed dataset loaded — {df.shape[0]} rows, {df.shape[1]} columns")
    return df