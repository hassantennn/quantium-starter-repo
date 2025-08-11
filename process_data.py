import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = DATA_DIR / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_csvs(folder: Path) -> pd.DataFrame:
    frames = []
    for p in sorted(folder.glob("*.csv")):
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

    pm = df[df["product"].str.strip().str.lower() == "pink morsel"]

    pm["quantity"] = pd.to_numeric(pm["quantity"], errors="coerce")
    pm["price"] = pd.to_numeric(pm["price"], errors="coerce")
    pm = pm.dropna(subset=["quantity","price"])
    pm["Sales"] = pm["quantity"] * pm["price"]

    pm["Date"] = pd.to_datetime(pm["date"], errors="coerce")
    pm = pm.dropna(subset=["Date"])

    pm["Region"] = pm["region"]

    out = pm[["Sales","Date","Region"]].sort_values("Date").reset_index(drop=True)

    out_path = OUT_DIR / "pink_morsel_sales.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {len(out)} rows to {out_path}")

if __name__ == "__main__":
    main()
