"""Download daily NASA POWER irradiance + weather for Nairobi."""
from pathlib import Path
import urllib.request

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

URL = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    "?parameters=ALLSKY_SFC_SW_DWN,T2M,RH2M,WS2M,PRECTOTCORR,CLOUD_AMT"
    "&community=RE"
    "&longitude=36.8219&latitude=-1.2921"
    "&start=20140101&end=20231231"
    "&format=CSV"
)
out = DATA_DIR / "nairobi_daily.csv"
print(f"GET {URL}")
urllib.request.urlretrieve(URL, out)
print(f"Saved {out} ({out.stat().st_size / 1024:.1f} KB)")
