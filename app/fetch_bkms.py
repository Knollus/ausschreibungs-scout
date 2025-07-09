"""
Holt Bekanntmachungen aus der OpenData-Schnittstelle des Bekanntmachungsservice
und liefert eine gekürzte JSON-Liste.
Siehe Doku: https://www.bescha.bund.de/...OpenData-Schnittstelle  :contentReference[oaicite:0]{index=0}
"""
import csv, io, datetime, requests
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parent.parent
CFG  = yaml.safe_load((BASE / "config" / "profile_dos.yml").read_text())

# --- Konstanten ----------------------------------------------------------
BKMS_URL = "https://www.oeffentlichevergabe.de/api/public/v1/releases/csv"

def fetch(max_items: int = 200, days_back: int = 30):
    params = {
        "cpv": ",".join(CFG["cpv_list"]),
        "buyerAssignedLocation": ",".join(CFG["regions"]),
        "publishedAfter": (datetime.date.today() -
                           datetime.timedelta(days=days_back)).isoformat(),
        "limit": max_items
    }
    resp = requests.get(BKMS_URL, params=params, timeout=30)
    resp.raise_for_status()

    reader = csv.DictReader(io.StringIO(resp.text, newline=""))
    results = list(reader)
    return results[:max_items]

if __name__ == "__main__":
    from pprint import pprint
    pprint(fetch(5)[:2])
