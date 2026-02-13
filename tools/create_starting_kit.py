import shutil
import zipfile
import os
from pathlib import Path

# Configuration
KIT_NAME = "starting_kit"
ROOT_DIR = Path(".")
# Temporary staging directory
STAGING_DIR = ROOT_DIR / "temp_kit_staging"

# Items to include in the kit
# Format: (Source Path, Destination Path inside the ZIP)
ITEMS_TO_COPY = [
    ("template_starting_kit.ipynb", "template_starting_kit.ipynb"),
    ("tools/zip_submission.py", "zip_submission.py"), # Move to root for easier use
    ("requirements.txt", "requirements.txt"),
    ("solution/submission.py", "submission.py"),     # Move to root as the template
    ("ingestion_program/ingestion.py", "ingestion_program/ingestion.py"),
    ("scoring_program/scoring.py", "scoring_program/scoring.py"),
    ("dev_phase/input_data", "dev_phase/input_data"), # Include only input data
]

def build():
    # 1. Clean up old builds
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(exist_ok=True)

    print(f"📦 Preparing files for {KIT_NAME}.zip...")

    # 2. Copy files and folders to staging
    for src_path, dst_rel_path in ITEMS_TO_COPY:
        src = ROOT_DIR / src_path
        dst = STAGING_DIR / dst_rel_path
        
        if not src.exists():
            print(f"⚠️ Warning: {src} not found, skipping.")
            continue
            
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"  + Added directory: {src_path}/")
        else:
            shutil.copy2(src, dst)
            print(f"  + Added file: {src_path}")

    # 3. Create a README for the user
    with open(STAGING_DIR / "README.md", "w") as f:
        f.write("# GEMS-GER Starting Kit\n\n"
                "This kit contains everything you need to participate in the challenge.\n\n"
                "### Quick Start:\n"
                "1. Install dependencies: `pip install -r requirements.txt`\n"
                "2. Open `template_starting_kit.ipynb` and run the cells.\n"
                "### Submitting:\n"
                "Run `python zip_submission.py` to create your submission package.")

    # 4. Create the ZIP and CLEAN UP
    zip_filename = f"{KIT_NAME}.zip"
    
    # We use shutil.make_archive to zip the content of STAGING_DIR
    # base_name is the path/name of the zip to create
    # root_dir is the directory we want to zip the contents of
    shutil.make_archive(KIT_NAME, 'zip', STAGING_DIR)
    
    # Clean up the staging folder so only the ZIP remains
    shutil.rmtree(STAGING_DIR)
    
    print(f"\n✅ SUCCESS!")
    print(f"Generated: {zip_filename}")
    print(f"Temporary staging folder has been removed.")

if __name__ == "__main__":
    build()
