import requests
import json
from pathlib import Path

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

HEADERS = {
    "User-Agent": "wick-research-dashboard/1.0"
}

FAST_SERIES = [

    # ---- US Rates & Curves ----
    "DGS2","DGS5","DGS10","DGS30",
    "DFII10",
    "THREEFYTP10",

    # ---- Money Markets ----
    "EFFR",
    "SOFR",

    # ---- Commodities ----
    "GOLDAMGBD228NLBM",
    "DCOILWTICO",
    "DCOILBRENTEU",
    "PCOPPUSDM",
    "DHHNGSP",

    # ---- Equity Markets ----
    "SP500",
    "SP500REAL",
    "NASDAQCOM",
    "RUT",
    "WILL5000PR",
    "VIXCLS",
    "DTWEXBGS",

    # ---- Global Equity Indices ----
    "NIKKEI225",
    "SHCOMP",
    "DAX",
    "FTSE100",
    "FRANCE40",
    "STOXX50E",
    "HANGSENG",

    # ---- Global Sovereign Bonds ----
    "IRLTLT01DEM156N",
    "IRLTLT01FRM156N",
    "IRLTLT01ITM156N",
    "IRLTLT01GBM156N",
    "IRLTLT01CHM156N",
    "IRLTLT01ESM156N",
    "IRLTLT01JPM156N",
    "IRLTLT01CNM156N",

    # ---- FX (USD base) ----
    "DEXUSEU",
    "DEXUSUK",
    "DEXJPUS",
    "DEXSZUS",
    "DEXCHUS",
]

# Load existing raw.json to avoid overwrites
raw_path = Path("data/raw.json")
raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}

for s in FAST_SERIES:
    try:
        r = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={
                "series_id": s,
                "api_key": API_KEY,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 1
            },
            timeout=20
        ).json()

        obs = r.get("observations", [])
        if not obs:
            raw[s] = {"value": None, "updated": None}
            continue

        val = obs[0]["value"]
        raw[s] = {
            "value": None if val in (None, ".", "") else float(val),
            "updated": obs[0]["date"]
        }

    except Exception:
        raw[s] = raw.get(s, {"value": None, "updated": None})

raw_path.write_text(json.dumps(raw, indent=2))
