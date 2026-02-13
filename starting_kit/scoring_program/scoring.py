import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def compute_rmse(predictions, targets):
    """
    Calculates the Root Mean Squared Error (RMSE).
    """
    # Ensure we are comparing the same number of rows
    # Targets usually has 1 column ('GWL'), Predictions usually has 1 column ('GWL')
    y_pred = predictions.iloc[:, 0] if isinstance(predictions, pd.DataFrame) else predictions
    y_true = targets.iloc[:, 0] if isinstance(targets, pd.DataFrame) else targets

    # Align by index and drop any rows with NaNs in ground truth (if any)
    combined = pd.concat([
        pd.Series(y_pred, name='pred').reset_index(drop=True), 
        pd.Series(y_true, name='true').reset_index(drop=True)
    ], axis=1).dropna()
    
    if combined.empty:
        print("Warning: No data to score.")
        return 999.0
    
    rmse = np.sqrt(mean_squared_error(combined['true'], combined['pred']))
    return float(rmse)

def main(reference_dir, prediction_dir, output_dir):
    scores = {}
    
    try:
        # 1. Path Setup
        # Reference labels: [ref_dir]/test/test_labels.csv (from setup_data.py)
        # Predictions: [pred_dir]/test_predictions.csv (from ingestion.py)
        label_path = reference_dir / 'test' / 'test_labels.csv'
        pred_path = prediction_dir / 'test_predictions.csv'

        # Fallback if structure differs slightly on different platforms
        if not label_path.exists():
            label_path = reference_dir / 'test_labels.csv'

        # 2. Load Data
        targets = pd.read_csv(label_path)
        predictions = pd.read_csv(pred_path)

        # 3. Compute Score
        scores['rmse'] = compute_rmse(predictions, targets)
        
    except Exception as e:
        print(f"❌ Scoring Error: {e}")
        scores['rmse'] = 999.0

    # 4. Include Runtime Metadata (Captured by ingestion.py)
    try:
        metadata_path = prediction_dir / 'metadata.json'
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            scores.update(metadata)
    except Exception:
        pass

    # 5. Save results for the Leaderboard
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / 'scores.json', 'w') as f:
        json.dump(scores, f)
    
    print(f"Scoring finished. RMSE: {scores['rmse']:.4f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Paths provided by Codabench environment
    parser.add_argument("--reference-dir", type=str, default="/app/input/ref")
    parser.add_argument("--prediction-dir", type=str, default="/app/input/res")
    parser.add_argument("--output-dir", type=str, default="/app/output")
    args = parser.parse_args()

    main(Path(args.reference_dir), Path(args.prediction_dir), Path(args.output_dir))
