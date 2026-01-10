import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_series(series_id, limit=400):
    r = requests.get(
        BASE_URL,
        params={
            "series_id": series_id,
            "api_key": API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit
        },
        timeout=20
    ).json()
    return r.get("observations", [])

def safe_float(x):
    try:
        if x in (None, ".", ""):
            return None
        return float(x)
    except:
        return None

def latest_and_prior(series, offset):
    if not series:
        return None, None

    latest_val = safe_float(series[0]["value"])
    if latest_val is None:
        return None, None

    latest_date = datetime.strptime(series[0]["date"], "%Y-%m-%d")
    target_date = latest_date - offset

    for obs in series[1:]:
        obs_date = datetime.strptime(obs["date"], "%Y-%m-%d")
        obs_val = safe_float(obs["value"])
        if obs_val is None:
            continue
        if obs_date <= target_date:
            return latest_val, obs_val

    return latest_val, None

derived = {}

# ---- Rates (1D) ----
for s in ["DGS2", "DGS10", "DGS30"]:
    series = fetch_series(s, 10)
    latest, prior = latest_and_prior(series, relativedelta(days=1))
    derived[f"{s}_1d"] = (latest - prior) if latest is not None and prior is not None else None

# ---- Curve spreads ----
s2 = fetch_series("DGS2", 2)
s10 = fetch_series("DGS10", 2)
s30 = fetch_series("DGS30", 2)

v2 = safe_float(s2[0]["value"]) if s2 else None
v10 = safe_float(s10[0]["value"]) if s10 else None
v30 = safe_float(s30[0]["value"]) if s30 else None

derived["spread_2s10s"] = (v10 - v2) if v10 is not None and v2 is not None else None
derived["spread_10s30s"] = (v30 - v10) if v30 is not None and v10 is not None else None

# ---- Real rates ----
series = fetch_series("DFII10", 10)
latest, prior = latest_and_prior(series, relativedelta(days=1))
derived["real_10y_1d"] = (latest - prior) if latest is not None and prior is not None else None

# ---- Term premium ----
series = fetch_series("THREEFYTP10", 10)
latest, prior = latest_and_prior(series, relativedelta(days=1))
derived["term_premium_10y_1d"] = (latest - prior) if latest is not None and prior is not None else None

# ---- Inflation YoY ----
for s, key in [("CPIAUCSL", "CPI_YoY"), ("CPILFESL", "CoreCPI_YoY")]:
    series = fetch_series(s, 400)
    latest, prior = latest_and_prior(series, relativedelta(years=1))
    derived[key] = ((latest / prior - 1) * 100) if latest is not None and prior is not None else None

# ---- Labor ----
series = fetch_series("PAYEMS", 24)
latest, prior = latest_and_prior(series, relativedelta(months=1))
derived["PAYEMS_MoM"] = (latest - prior) if latest is not None and prior is not None else None

series = fetch_series("UNRATE", 24)
latest, prior = latest_and_prior(series, relativedelta(months=1))
derived["UNRATE_MoM"] = (latest - prior) if latest is not None and prior is not None else None

series = fetch_series("AHETPI", 400)
latest, prior = latest_and_prior(series, relativedelta(years=1))
derived["AHETPI_YoY"] = ((latest / prior - 1) * 100) if latest is not None and prior is not None else None

# ---- Liquidity WoW ----
for s, key in [("WALCL", "WALCL_WoW"), ("RRPONTSYD", "RRP_WoW"), ("WTREGEN", "TGA_WoW")]:
    series = fetch_series(s, 30)
    latest, prior = latest_and_prior(series, relativedelta(weeks=1))
    derived[key] = (latest - prior) if latest is not None and prior is not None else None

# ---- Markets (1D) ----
for s, key in [("SP500", "SP500_1d"), ("VIXCLS", "VIX_1d"), ("DTWEXBGS", "DXY_1d")]:
    series = fetch_series(s, 10)
    latest, prior = latest_and_prior(series, relativedelta(days=1))
    derived[key] = (latest - prior) if latest is not None and prior is not None else None

with open("data/derived.json", "w") as f:
    json.dump(derived, f, indent=2)
