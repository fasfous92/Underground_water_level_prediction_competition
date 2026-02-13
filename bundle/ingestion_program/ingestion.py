import json
import sys
import time
from pathlib import Path
import pandas as pd

# We only have one test set now
EVAL_SETS = ["test"]

def evaluate_model(model, X_test):
    """
    Generate predictions. 
    Note: We pass the RAW X_test to the model. 
    The participant's pipeline must handle dropping strings!
    """
    y_pred = model.predict(X_test)
    return pd.DataFrame({'GWL': y_pred})

def get_train_data(data_dir, chunksize=100000):
    """
    Loads 'train.csv' in chunks for memory safety.
    Contains both features and labels.
    """
    data_dir = Path(data_dir)
    train_path = data_dir / "train" / "train.csv"
    
    # Fallback for local testing vs Codabench environment
    if not train_path.exists():
        train_path = data_dir / "train.csv"

    print(f"Reading {train_path} in chunks...")
    
    chunks = []
    for chunk in pd.read_csv(train_path, chunksize=chunksize):
        chunks.append(chunk)
    
    full_df = pd.concat(chunks, axis=0)
    
    y_train = full_df['GWL']
    X_train = full_df.drop(columns=['GWL'])
    
    return X_train, y_train

def main(data_dir, output_dir):
    # Import the participant's model
    from submission import get_model

    print("--- 1. Loading Training Data ---")
    X_train, y_train = get_train_data(data_dir)

    print("--- 2. Training the Model ---")
    model = get_model()

    start_train = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_train
    print(f"Training completed in {train_time:.2f}s")

    print("--- 3. Evaluating on Test Set ---")
    start_test = time.time()
    
    # Load test features (Matches setup_data.py output)
    X_test_path = data_dir / "test" / "test_features.csv"
    X_test = pd.read_csv(X_test_path)
    
    y_test_pred = evaluate_model(model, X_test)
    
    test_time = time.time() - start_test
    print(f"Testing completed in {test_time:.2f}s")

    # --- 4. Write Output Files ---
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metadata for the leaderboard (Runtime)
    with open(output_dir / "metadata.json", "w") as f:
        json.dump({
            "train_time": train_time, 
            "test_time": test_time,
            "duration": train_time + test_time
        }, f)

    # Save predictions (Matches what scoring.py expects)
    y_test_pred.to_csv(output_dir / "test_predictions.csv", index=False)
    
    print(f"Ingestion finished. Total duration: {train_time + test_time:.2f}s")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingestion program")
    parser.add_argument("--data-dir", type=str, default="/app/input_data")
    parser.add_argument("--output-dir", type=str, default="/app/output")
    parser.add_argument("--submission-dir", type=str, default="/app/ingested_program")

    args = parser.parse_args()
    
    # Add submission and current folder to path so we can find 'submission.py'
    sys.path.append(args.submission_dir)
    sys.path.append(str(Path(__file__).parent.resolve()))

    main(Path(args.data_dir), Path(args.output_dir))
