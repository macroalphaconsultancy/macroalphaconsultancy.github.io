import requests
import json

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES = [
    "DGS2","DGS5","DGS10","DGS30","DFII10","THREEFYTP10",
    "WALCL","RESBALNS","WTREGEN","RRPONTSYD","EFFR","SOFR","ECBASSETSW",
    "CPIAUCSL","CPILFESL","UNRATE","PAYEMS","AHETPI","CIVPART",
    "SP500","VIXCLS","DTWEXBGS","NIKKEI225","SHCOMP","DAX","FTSE100","FRANCE40","MSCIWORLD","MSCIEM",
    "GOLDAMGBD228NLBM","DCOILWTICO","DCOILBRENTEU","PCOPPUSDM","DHHNGSP",
    "IRLTLT01DEM156N","IRLTLT01ITM156N","IRLTLT01JPM156N","IRLTLT01CNM156N",
    "DEXJPUS","DEXUSEU","DEXUSUK","DEXSZUS","DEXCHUS"
]

raw = {}

for s in SERIES:
    r = requests.get(BASE_URL, params={
        "series_id": s,
        "api_key": API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }).json()
    obs = r["observations"][0]
    raw[s] = {
        "value": obs["value"],
        "updated": obs["date"]
    }

with open("raw.json","w") as f:
    json.dump(raw,f,indent=2)
