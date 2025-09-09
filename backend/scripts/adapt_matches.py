import pandas as pd

FD_KEEP = [
    "Div","Date","Time","HomeTeam","AwayTeam",
    "FTHG","FTAG","FTR","HTHG","HTAG","HTR","Referee",
    "HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR"
]

RENAME = {
    # identity/when
    "HomeTeam": "Home",
    "AwayTeam": "Away",
    "Date": "Date",
    "Time": "Time",
    "Div": "Division",

    # targets (full/half time)
    "FTHG": "HomeGoals",
    "FTAG": "AwayGoals",
    "FTR":  "Result",        # 'H','D','A'
    "HTHG": "HT_HomeGoals",
    "HTAG": "HT_AwayGoals",
    "HTR":  "HT_Result",

    "Referee": "Referee",

    # team stats (home/away)
    "HS":  "Home_Shots",
    "AS":  "Away_Shots",
    "HST": "Home_ShotsOnTarget_Made",
    "AST": "Away_ShotsOnTarget_Made",
    "HF":  "Home_Fouls_Committed",
    "AF":  "Away_Fouls_Committed",
    "HC":  "Home_Corners",
    "AC":  "Away_Corners",
    "HY":  "Home_Yellow",
    "AY":  "Away_Yellow",
    "HR":  "Home_Red",
    "AR":  "Away_Red",
}

def infer_season(d: pd.Timestamp) -> str:
    """Premier League season label like '2025-2026'."""
    y = d.year
    start = y if d.month >= 7 else y - 1
    return f"{start}-{start+1}"

def load_and_adapt(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Keep only the columns you want (ignore unknowns safely)
    df = df[[c for c in FD_KEEP if c in df.columns]].copy()

    # Rename to your internal names
    df = df.rename(columns=RENAME)

    # Parse Date (football-data uses day-first like 15/08/2025)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Standardize Time to 'HH:MM' string if present
    if "Time" in df.columns:
        t = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce")
        df["Time"] = t.dt.strftime("%H:%M")

    # Season once (no tz gymnastics needed)
    df["Season"] = df["Date"].apply(lambda d: infer_season(d) if pd.notna(d) else pd.NA)

    # Make sure numeric stats are numeric
    num_cols = [
        "HomeGoals","AwayGoals","HT_HomeGoals","HT_AwayGoals",
        "Home_Shots","Away_Shots","Home_ShotsOnTarget_Made","Away_ShotsOnTarget_Made",
        "Home_Fouls_Committed","Away_Fouls_Committed",
        "Home_Corners","Away_Corners","Home_Yellow","Away_Yellow","Home_Red","Away_Red",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df  # ← IMPORTANT: return the adapted DataFrame


if __name__ == "__main__":
    out = load_and_adapt("data/raw/2025-26-premier-league.csv")
    out.to_csv("data/processed/pl_2025_26_minimal.csv", index=False)
    print(f"Saved → data/processed/pl_2025_26_minimal.csv  (rows: {len(out)})")