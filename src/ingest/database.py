from pathlib import Path
import pandas as pd
import sqlite3

#path and columns
RAW_DATA_DIR = Path("data/raw")
DB_PATH = Path("data/soccer.db")

#defining needed columns
USEFUL_COLUMNS = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HS",
    "AS",
    "HST",
    "AST",
    "HC",
    "AC",
]

def ingest_csvs_to_db():
    all_dfs = []

    for csv_file in RAW_DATA_DIR.glob("*.csv"):
        df = pd.read_csv(csv_file, usecols=USEFUL_COLUMNS)
        all_dfs.append(df)

    #combine to one master dataframe
    master_df = pd.concat(all_dfs, ignore_index=True)

    #standardize dates and sort chronologically
    master_df["Date"] = pd.to_datetime(
        master_df["Date"], format="mixed", dayfirst=True, errors="coerce"
    )
    master_df = master_df.sort_values("Date").reset_index(drop=True)

    #write to SQLite database
    conn = sqlite3.connect(DB_PATH)
    master_df.to_sql("matches", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Successfully ingested {len(master_df)} matches into SQLite database!")

if __name__ == "__main__":
    ingest_csvs_to_db()