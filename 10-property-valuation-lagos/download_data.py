"""Download Lagos housing prices."""
from pathlib import Path
import subprocess
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
subprocess.run(["kaggle", "datasets", "download", "-d", "thedevastator/investigating-housing-prices-in-lagos-nigeria",
                "--unzip", "-p", str(DATA_DIR)], check=True)
print("Downloaded into", DATA_DIR)
