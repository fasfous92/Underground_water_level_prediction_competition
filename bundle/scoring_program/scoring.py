import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def compute_rmse(predictions, targets):
    """
    Calculates the Root Mean Squared Error (RMSE) for Groundwater Level Prediction.
    """
    # Ensure inputs are handled correctly whether they are DataFrames or Series
    y_pred = predictions.iloc[:, 0] if isinstance(predictions, pd.DataFrame) else predictions
    y_true = targets.iloc[:, 0] if isinstance(targets, pd.DataFrame) else targets

    # Align predictions with ground truth and remove any missing values in labels
    combined = pd.concat([
        pd.Series(y_pred, name='pred').reset_index(drop=True), 
        pd.Series(y_true, name='true').reset_index(drop=True)
    ], axis=1).dropna()
    
    if combined.empty:
        print("Warning: No overlapping data found for scoring.")
        return 999.0
    
    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(combined['true'], combined['pred']))
    return float(rmse)

def main(reference_dir, prediction_dir, output_dir):
    scores = {}
    eval_set = "test"
    
    try:
        # Load predictions and reference labels
        predictions = pd.read_csv(prediction_dir / f'{eval_set}_predictions.csv')
        targets = pd.read_csv(reference_dir / eval_set / f'{eval_set}_labels.csv')

        # Calculate the score
        scores['rmse'] = compute_rmse(predictions, targets)
        
    except Exception as e:
        print(f"❌ Scoring Error: {e}")
        scores['rmse'] = 999.0

    # Include runtime metadata for the leaderboard
    try:
        metadata_path = prediction_dir / 'metadata.json'
        if metadata_path.exists():
            durations = json.loads(metadata_path.read_text())
            scores.update(durations)
    except Exception:
        pass

    # Save to scores.json for Codabench
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / 'scores.json', 'w') as f:
        json.dump(scores, f)
    
    print(f"Scoring finished. Leaderboard RMSE: {scores['rmse']:.4f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-dir", type=str, default="/app/input/ref")
    parser.add_argument("--prediction-dir", type=str, default="/app/input/res")
    parser.add_argument("--output-dir", type=str, default="/app/output")
    args = parser.parse_args()

    main(Path(args.reference_dir), Path(args.prediction_dir), Path(args.output_dir))
