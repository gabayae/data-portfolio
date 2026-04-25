"""Download Lake Kariba reservoir data from Kaggle.

Requires the Kaggle CLI configured (https://www.kaggle.com/docs/api).
"""
from pathlib import Path
import subprocess

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

subprocess.run(
    ["kaggle", "datasets", "download", "-d", "marbin/lake-kariba-reservoir-data",
     "--unzip", "-p", str(DATA_DIR)],
    check=True,
)
print("Downloaded into", DATA_DIR)
