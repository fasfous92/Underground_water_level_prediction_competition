import pandas as pd
import numpy as np
import requests
import zipfile
from pathlib import Path

# --- CONFIGURATION ---
ZENODO_URL = "https://zenodo.org/records/16736908/files/GEMS-GER_data.zip?download=1"
RAW_DIR = Path("raw_data")
EXTRACT_DIR = RAW_DIR / "extracted"
MAX_TRAIN_ROWS = 1000000 
MAX_TEST_ROWS = 50000   # <--- Capping test size for efficiency

def run_setup():
    # 1. Directory Setup
    for phase in ["dev_phase", "final_phase"]:
        (Path(phase) / "input_data/test").mkdir(parents=True, exist_ok=True)
        (Path(phase) / "reference_data/test").mkdir(parents=True, exist_ok=True)
    (Path("dev_phase/input_data/train")).mkdir(parents=True, exist_ok=True)
    
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Download & Extract (Skipped if exists)
    zip_path = RAW_DIR / "GEMS-GER_data.zip"
    if not zip_path.exists():
        print("📥 Downloading dataset...")
        r = requests.get(ZENODO_URL, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
    
    if not any(EXTRACT_DIR.iterdir()):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)

    # 3. Process Data
    print("📊 Merging and optimizing memory...")
    static_file = next(EXTRACT_DIR.rglob("*static*.csv"))
    df_static = pd.read_csv(static_file)
    df_static.columns = df_static.columns.str.strip()

    li = []
    dynamic_folder = next(EXTRACT_DIR.rglob("dynamic"))
    for filename in dynamic_folder.glob("*.csv"):
        df = pd.read_csv(filename)
        df['well_id_str'] = filename.stem
        if 'Unnamed: 0' in df.columns:
            df['date_dt'] = pd.to_datetime(df['Unnamed: 0'])
            df.drop(columns=['Unnamed: 0'], inplace=True)
        # Drop and optimize
        df.drop(columns=[c for c in ['GWL_flag'] if c in df.columns], inplace=True)
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = df[col].astype('float32')
        li.append(df)

    master_df = pd.concat(li, ignore_index=True)
    master_df = pd.merge(master_df, df_static, left_on='well_id_str', right_on='MW_ID', how='left').drop(columns=['MW_ID'])

    # 4. Strict Temporal Split
    master_df = master_df.sort_values('date_dt')
    unique_dates = sorted(master_df['date_dt'].unique())
    
    # We define the boundaries based on the total timeline
    idx_80 = int(len(unique_dates) * 0.8)
    idx_90 = int(len(unique_dates) * 0.9)
    
    train_df = master_df[master_df['date_dt'] < unique_dates[idx_80]]
    dev_df = master_df[(master_df['date_dt'] >= unique_dates[idx_80]) & (master_df['date_dt'] < unique_dates[idx_90])]
    final_df = master_df[master_df['date_dt'] >= unique_dates[idx_90]]

    # 5. Applying the Caps
    if len(train_df) > MAX_TRAIN_ROWS:
        train_df = train_df.tail(MAX_TRAIN_ROWS)
    
    # We take the FIRST rows of the test segments to stay close to training timeline
    if len(dev_df) > MAX_TEST_ROWS:
        dev_df = dev_df.head(MAX_TEST_ROWS)
    if len(final_df) > MAX_TEST_ROWS:
        final_df = final_df.head(MAX_TEST_ROWS)

    # 6. Saving
    meta_cols = ['well_id_str', 'date_dt']
    train_df.to_csv("dev_phase/input_data/train/train.csv", index=False)
    
    # Public Dev
    dev_df.drop(columns=['GWL'] + meta_cols).to_csv("dev_phase/input_data/test/test_features.csv", index=False)
    dev_df[['GWL']].to_csv("dev_phase/reference_data/test/test_labels.csv", index=False)
    
    # Private Final
    final_df.drop(columns=['GWL'] + meta_cols).to_csv("final_phase/input_data/test/test_features.csv", index=False)
    final_df[['GWL']].to_csv("final_phase/reference_data/test/test_labels.csv", index=False)

    print(f"🚀 Setup Complete!\nTrain: {len(train_df):,}\nDev Test: {len(dev_df):,}\nFinal Test: {len(final_df):,}")

if __name__ == "__main__":
    run_setup()
