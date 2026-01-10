import requests
import json

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

HEADERS = {
    "User-Agent": "macroalphaconsultancy-dashboard/1.0"
}

SERIES = [
    "DGS2","DGS5","DGS10","DGS30","DFII10","THREEFYTP10",
    "WALCL","RESBALNS","WTREGEN","RRPONTSYD","EFFR","SOFR","ECBASSETSW",
    "CPIAUCSL","CPILFESL","UNRATE","PAYEMS","AHETPI","CIVPART",
    "SP500","VIXCLS","DTWEXBGS","NIKKEI225","SHCOMP",
    "DAX","FTSE100","FRANCE40",
    "GOLDAMGBD228NLBM","DCOILWTICO","DCOILBRENTEU","PCOPPUSDM","DHHNGSP",
    "IRLTLT01DEM156N","IRLTLT01ITM156N","IRLTLT01JPM156N","IRLTLT01CNM156N",
    "DEXJPUS","DEXUSEU","DEXUSUK","DEXSZUS","DEXCHUS"
]

raw = {}

for s in SERIES:
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

        obs_list = r.get("observations", [])
        if not obs_list:
            raw[s] = {"value": None, "updated": None}
            continue

        obs = obs_list[0]
        val = obs.get("value")

        if val in (None, ".", ""):
            raw[s] = {"value": None, "updated": obs.get("date")}
        else:
            raw[s] = {"value": float(val), "updated": obs.get("date")}

    except Exception as e:
        raw[s] = {"value": None, "updated": None}

with open("data/raw.json", "w") as f:
    json.dump(raw, f, indent=2)
