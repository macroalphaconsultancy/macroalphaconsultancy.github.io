import requests
import json
from pathlib import Path

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

HEADERS = {
    "User-Agent": "wick-research-dashboard/1.0"
}

SLOW_SERIES = [

    # ---- Liquidity / Balance Sheets ----
    "WALCL",
    "RESBALNS",
    "WTREGEN",
    "RRPONTSYD",
    "ECBASSETSW",
    "JPNASSETSW",
    "CHNASETS",

    # ---- Inflation ----
    "CPIAUCSL",
    "CPILFESL",
    "CUSR0000SAS",
    "CUSR0000SEHA",
    "PPIFDG",
    "PCEPI",
    "PCEPILFE",

    # ---- Labor ----
    "UNRATE",
    "PAYEMS",
    "AHETPI",
    "CIVPART",
    "ICSA",
    "CCSA",
    "JTSJOL",
    "JTSQUR",

    # ---- Growth / Activity ----
    "INDPRO",
    "RSXFS",
    "NAPMPI",
    "TCU",

    # ---- Housing / Consumer ----
    "MORTGAGE30US",
    "HOUST",
    "EXHOSLUSM495S",
    "HSN1F",
    "UMCSENT",

    # ---- Policy Rates ----
    "ECBDFR",
    "IRSTCB01GBM156N",
    "IRSTCB01JPM156N",
]

raw_path = Path("data/raw.json")
raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}

for s in SLOW_SERIES:
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
