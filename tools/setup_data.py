import pandas as pd
import os
import requests
import zipfile
import shutil
from pathlib import Path

# --- CONFIGURATION ---
ZENODO_URL = "https://zenodo.org/records/16736908/files/GEMS-GER_data.zip?download=1"
RAW_DIR = Path("raw_data")
EXTRACT_DIR = RAW_DIR / "extracted"
MAX_TRAIN_ROWS = 100000  # <--- LIMIT TRAINING SIZE HERE (e.g., 100k rows)

def run_setup():
    # 1. Directory Setup
    input_base = Path("dev_phase/input_data")
    for f in ["train", "test"]: (input_base / f).mkdir(parents=True, exist_ok=True)
    Path("dev_phase/reference_data/test").mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Download & Extract (Same logic as before)
    zip_path = RAW_DIR / "GEMS-GER_data.zip"
    if not zip_path.exists():
        print("Downloading...")
        r = requests.get(ZENODO_URL, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # 3. Locate & Merge
    static_file = next(EXTRACT_DIR.rglob("*static*.csv"))
    dynamic_folder = next(EXTRACT_DIR.rglob("dynamic"))
    df_static = pd.read_csv(static_file)
    df_static.columns = df_static.columns.str.strip()

    li = []
    for filename in dynamic_folder.glob("*.csv"):
        df = pd.read_csv(filename)
        df['well_id_str'] = filename.stem
        if 'Unnamed: 0' in df.columns:
            df['date_dt'] = pd.to_datetime(df['Unnamed: 0'])
            df['month'] = df['date_dt'].dt.month
            df['year'] = df['date_dt'].dt.year
        df.drop(columns=[c for c in ['Unnamed: 0', 'GWL_flag'] if c in df.columns], inplace=True)
        li.append(df)

    master_df = pd.concat(li, ignore_index=True)
    master_df = pd.merge(master_df, df_static, left_on='well_id_str', right_on='MW_ID', how='left').drop(columns=['MW_ID'])

    # 4. Temporal Split (80/20)
    master_df = master_df.sort_values('date_dt')
    unique_dates = sorted(master_df['date_dt'].unique())
    split_date = unique_dates[int(len(unique_dates) * 0.8)]
    
    train_df = master_df[master_df['date_dt'] < split_date]
    test_df = master_df[master_df['date_dt'] >= split_date]

    # --- 5. REDUCE DATA SIZE ---
    if len(train_df) > MAX_TRAIN_ROWS:
        print(f"Reducing training data from {len(train_df)} to {MAX_TRAIN_ROWS} rows...")
        # Option A: Take the MOST RECENT rows (Best for time-series)
        train_df = train_df.tail(MAX_TRAIN_ROWS)
        
        # Option B: Random Sampling (Uncomment if you prefer variety over recency)
        # train_df = train_df.sample(n=MAX_TRAIN_ROWS, random_state=42).sort_values('date_dt')

    # 6. Save Files
    train_df.to_csv(input_base / "train/train.csv", index=False)
    
    meta_cols = ['well_id_str', 'date_dt']
    test_df.drop(columns=['GWL'] + meta_cols).to_csv(input_base / "test/test_features.csv", index=False)
    test_df[['GWL']].to_csv("dev_phase/reference_data/test/test_labels.csv", index=False)

    print(f"🚀 Setup Complete! Final Train Size: {len(train_df)}")

if __name__ == "__main__":
    run_setup()
