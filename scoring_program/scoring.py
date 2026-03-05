import json
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def compute_rmse(predictions, targets):
    """
    Calculates the Root Mean Squared Error (RMSE) for the GWL column.
    """
    # Assuming both DataFrames have a 'GWL' column based on ingestion.py
    y_pred = predictions['GWL'].values
    y_true = targets['GWL'].values
    
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return float(rmse)

def main(input_dir, output_dir):
    # Codabench passes a single input_dir containing 'ref' (answers) and 'res' (predictions)
    ref_dir = Path(input_dir) / 'ref'
    res_dir = Path(input_dir) / 'res'

    scores = {}

    try:
        # --- 1. Collect Predictions (from Ingestion) ---
        pred_path = res_dir / "test_predictions.csv"
        predictions = pd.read_csv(pred_path)

        # --- 2. Collect Reference Labels (Ground Truth) ---
        # Adjust this path if your labels are not inside a 'test' subfolder!
        label_path = ref_dir / "test" / "test_labels.csv"
        if not label_path.exists():
            label_path = ref_dir / "test_labels.csv" # Fallback
            
        targets = pd.read_csv(label_path)

        # --- 3. Compute Score ---
        scores['rmse'] = compute_rmse(predictions, targets)
        
    except Exception as e:
        print(f"❌ Scoring Error: {e}")
        # Assign a terrible score if something breaks so the leaderboard doesn't crash
        scores['rmse'] = 999.0

    # --- 4. Collect Metadata (from Ingestion) ---
    # This pulls your train_time, test_time, and duration into the leaderboard!
    try:
        metadata_path = res_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                scores.update(metadata)
    except Exception as e:
        print(f"Warning: Could not read metadata.json. {e}")

    # --- 5. Save Results for Leaderboard ---
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "scores.json", "w") as f:
        json.dump(scores, f)
        
    print(f"Scoring complete. RMSE: {scores.get('rmse', 'ERROR'):.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scoring program")
    
    # Codabench passes these as positional arguments
    parser.add_argument("input_dir", type=str, help="Directory containing ref and res folders")
    parser.add_argument("output_dir", type=str, help="Directory to save scores.json")
    parser.add_argument("program_dir", type=str, nargs='?', default="", help="Optional program dir")
    
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
