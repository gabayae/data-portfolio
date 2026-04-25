"""Download Fast Food Marketing Campaign A/B test data."""
from pathlib import Path
import subprocess
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
subprocess.run(["kaggle", "datasets", "download", "-d", "chebotinaa/fast-food-marketing-campaign-ab-test",
                "--unzip", "-p", str(DATA_DIR)], check=True)
print("Downloaded into", DATA_DIR)
