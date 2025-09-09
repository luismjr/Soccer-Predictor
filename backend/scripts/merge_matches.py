import glob, pandas as pd
from adapt_matches import load_and_adapt  # from the adapter we wrote

def main():
    paths = sorted(glob.glob("data/raw/pl*.csv"))  # e.g., pl_2021_22.csv ... pl_2025_26.csv
    dfs = []
    for p in paths:
        d = load_and_adapt(p)
        dfs.append(d)

    all_df = pd.concat(dfs, ignore_index=True)
    # de-dupe by (Date, Home, Away) just in case
    all_df = all_df.dropna(subset=["Date"]).sort_values("Date")
    all_df = all_df.drop_duplicates(subset=["Date", "Home", "Away"], keep="last").reset_index(drop=True)

    all_df.to_csv("data/processed/merged_matches.csv", index=False)
    print(f"Saved → data/processed/merged_matches.csv (rows: {len(all_df)})")

if __name__ == "__main__":
    main()