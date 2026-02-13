import zipfile
from pathlib import Path

# Adjust this to point to your project root
ROOT_DIR = Path(__file__).parent.parent

# Files that MUST be at the root of the ZIP
BUNDLE_FILES = [
    ROOT_DIR / "competition.yaml",
    ROOT_DIR / "logo.png",
    ROOT_DIR / "starting_kit.zip", # Ensure this was built first!
]

# Folders to include as directories
BUNDLE_DIRS = {
    "pages": ROOT_DIR / "pages",
    "ingestion_program": ROOT_DIR / "ingestion_program",
    "scoring_program": ROOT_DIR / "scoring_program",
    "dev_phase": ROOT_DIR / "dev_phase",
    "final_phase": ROOT_DIR / "final_phase",
}

if __name__ == "__main__":
    output_filename = "bundle.zip"
    print(f"📦 Creating {output_filename}...")

    with zipfile.ZipFile(output_filename, mode="w") as bundle:
        # 1. Add root files
        for f in BUNDLE_FILES:
            if f.exists():
                print(f"  [File]  Adding {f.name}")
                bundle.write(f, arcname=f.name)
            else:
                print(f"  ⚠️ Warning: {f.name} not found!")

        # 2. Add directories recursively
        for arc_dirname, dirpath in BUNDLE_DIRS.items():
            if not dirpath.exists():
                print(f"  ❌ Error: {arc_dirname} directory missing!")
                continue
            
            print(f"  [Dir]   Adding {arc_dirname}/")
            for f in dirpath.rglob("*"):
                if f.is_file() and not f.name.startswith(".") and not f.name.endswith(".pyc"):
                    # Maintain internal folder structure
                    relative_path = f.relative_to(ROOT_DIR)
                    bundle.write(f, arcname=relative_path)

    print(f"\n✅ Success! Upload {output_filename} to Codabench.")
