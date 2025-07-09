import requests
from pathlib import Path

def fetch(cpv_list=None, countries=None, days_back=30, limit=50):
    """
    Holt Notices aus TED JSON-API.
    - cpv_list: Liste von CPV-Codes (z.B. ["72221000"])
    - countries: Liste von Ländercodes (["DE", "AT"])
    """
    from datetime import datetime, timedelta

    # Fallbacks
    cpv_list = cpv_list or ["72221000", "72224000", "72316000", "72262000", "72514000"]
    countries = countries or ["DE"]

    start_date = (datetime.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    cpv_query = ",".join(cpv_list)
    place_query = ",".join(countries)

    url = "https://ted.europa.eu/api/v2/notices"
    params = {
        "cpv": cpv_query,
        "place": place_query,
        "publication_date": f"{start_date}:",
        "limit": str(limit),
        "format": "json"
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("results", []):
        results.append({
            "noticeTitle": item.get("title", ""),
            "noticePublicationDate": item.get("publication_date", ""),
            "cpvCodes": ",".join(item.get("cpv", [])),
            "buyerName": item.get("buyer", {}).get("name", ""),
            "contractValue": item.get("value", {}).get("amount", ""),
            "region": ",".join(item.get("place", []))
        })
    return results

if __name__ == "__main__":
    from pprint import pprint
    pprint(fetch()[:3])
