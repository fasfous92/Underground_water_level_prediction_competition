import zipfile
from pathlib import Path

# This script zips the submission.py from the solution folder
# so it's ready to be uploaded to Codabench.

def create_submission_zip(output_filename="submission.zip"):
    # Path to the participant's actual code
    # Assuming they are working in the starting_kit/solution/ directory
    submission_script = Path("solution/submission.py")
    
    if not submission_script.exists():
        print(f"❌ Error: {submission_script} not found!")
        print("Make sure you are running this script from the starting_kit root.")
        return

    with zipfile.ZipFile(output_filename, 'w') as zipf:
        # Crucial: We write 'submission.py' as the arcname 
        # so it's at the root of the ZIP, not in a folder.
        zipf.write(submission_script, arcname="submission.py")
        
    print(f"✅ Success! Created '{output_filename}'.")
    print("You can now upload this file to the Codabench platform.")

if __name__ == "__main__":
    create_submission_zip()
