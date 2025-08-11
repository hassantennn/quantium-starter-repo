import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = DATA_DIR / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_csvs(folder: Path) -> pd.DataFrame:
    frames = []
    for p in sorted(folder.glob("*.csv")):
        if p.name == "pink_morsel_sales.csv":
            continue
        df = pd.read_csv(p)
        df.columns = [c.strip().lower() for c in df.columns]
        frames.append(df)
    if not frames:
        raise FileNotFoundError("No CSV files found in the data/ folder.")
    return pd.concat(frames, ignore_index=True)

def main():
    df = load_all_csvs(DATA_DIR)

    required = {"product","quantity","price","date","region"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Filter only Pink Morsels (robust to spacing/case) and work on a copy
    mask = df["product"].astype(str).str.strip().str.lower() == "pink morsel"
    pm = df.loc[mask].copy()

    # Clean numeric fields
    pm["quantity"] = pd.to_numeric(pm["quantity"], errors="coerce")

    # Remove $ and commas from price before converting
    pm["price"] = (
        pm["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    pm["price"] = pd.to_numeric(pm["price"], errors="coerce")

    # Drop rows with bad numerics
    pm = pm.dropna(subset=["quantity", "price"])

    # Compute Sales
    pm["Sales"] = pm["quantity"] * pm["price"]

    # Parse date
    pm["Date"] = pd.to_datetime(pm["date"], errors="coerce", dayfirst=False)
    pm = pm.dropna(subset=["Date"])

    # Region passthrough (consistent casing)
    pm["Region"] = pm["region"].astype(str).str.strip()

    # Final output
    out = pm[["Sales","Date","Region"]].sort_values("Date").reset_index(drop=True)

    out_path = OUT_DIR / "pink_morsel_sales.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {len(out)} rows to {out_path}")

if __name__ == "__main__":
    main()
