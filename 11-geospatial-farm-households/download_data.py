"""Download Agricultural Survey of African Farm Households."""
from pathlib import Path
import subprocess
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
subprocess.run(["kaggle", "datasets", "download", "-d", "crawford/agricultural-survey-of-african-farm-households",
                "--unzip", "-p", str(DATA_DIR)], check=True)
print("Downloaded into", DATA_DIR)
