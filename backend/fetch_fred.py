import requests
import json

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

HEADERS = {
    "User-Agent": "macroalphaconsultancy-dashboard/1.0"
}

SERIES = [

    # ---- US Rates & Curves ----
    "DGS2","DGS5","DGS10","DGS30",
    "DFII10",                # 10Y TIPS real yield
    "THREEFYTP10",           # ACM term premium

    # ---- Liquidity / Money Markets ----
    "WALCL",                 # Fed balance sheet
    "RESBALNS",              # Bank reserves
    "WTREGEN",               # TGA
    "RRPONTSYD",             # ON RRP
    "EFFR",
    "SOFR",

    # ---- Global Central Bank Balance Sheets ----
    "ECBASSETSW",
    "JPNASSETSW",
    "CHNASETS",

    # ---- Inflation ----
    "CPIAUCSL",
    "CPILFESL",
    "CUSR0000SAS",           # CPI services
    "CUSR0000SEHA",          # CPI shelter
    "PPIFDG",                # PPI final demand
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

    # ---- Housing / Consumer Stress ----
    "MORTGAGE30US",
    "HOUST",
    "EXHOSLUSM495S",
    "HSN1F",
    "UMCSENT",

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
    "IRLTLT01DEM156N",        # Germany 10Y
    "IRLTLT01FRM156N",        # France 10Y
    "IRLTLT01ITM156N",        # Italy 10Y
    "IRLTLT01GBM156N",        # UK 10Y
    "IRLTLT01CHM156N",        # Switzerland 10Y
    "IRLTLT01ESM156N",        # Spain 10Y
    "IRLTLT01JPM156N",        # Japan 10Y
    "IRLTLT01CNM156N",        # China 10Y

    # ---- Policy Rates ----
    "ECBDFR",
    "IRSTCB01GBM156N",
    "IRSTCB01JPM156N",

    # ---- FX (USD base) ----
    "DEXUSEU",
    "DEXUSUK",
    "DEXJPUS",
    "DEXSZUS",
    "DEXCHUS",
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

    except Exception:
        raw[s] = {"value": None, "updated": None}

with open("data/raw.json", "w") as f:
    json.dump(raw, f, indent=2)
