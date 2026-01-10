import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_KEY = "222e2d889d8d5e99c83789b4f556df45"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_series(series_id, limit=400):
    r = requests.get(BASE_URL, params={
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit
    }).json()
    return r["observations"]

def latest_and_prior(series, offset):
    latest = float(series[0]["value"])
    target_date = datetime.strptime(series[0]["date"], "%Y-%m-%d") - offset
    for obs in series:
        if datetime.strptime(obs["date"], "%Y-%m-%d") <= target_date:
            return latest, float(obs["value"])
    return latest, None

derived = {}

# Rates
for s in ["DGS2","DGS10","DGS30"]:
    series = fetch_series(s, 5)
    latest, prior = latest_and_prior(series, relativedelta(days=1))
    derived[f"{s}_1d"] = latest - prior if prior else None

# Curve spreads
series2 = fetch_series("DGS2", 2)
series10 = fetch_series("DGS10", 2)
series30 = fetch_series("DGS30", 2)
derived["spread_2s10s"] = float(series10[0]["value"]) - float(series2[0]["value"])
derived["spread_10s30s"] = float(series30[0]["value"]) - float(series10[0]["value"])

# Real rates
series = fetch_series("DFII10", 5)
latest, prior = latest_and_prior(series, relativedelta(days=1))
derived["real_10y_1d"] = latest - prior if prior else None

# Term premium
series = fetch_series("THREEFYTP10", 5)
latest, prior = latest_and_prior(series, relativedelta(days=1))
derived["term_premium_10y_1d"] = latest - prior if prior else None

# Inflation YoY
for s, key in [("CPIAUCSL","CPI_YoY"),("CPILFESL","CoreCPI_YoY")]:
    series = fetch_series(s, 400)
    latest, prior = latest_and_prior(series, relativedelta(years=1))
    derived[key] = (latest/prior - 1)*100 if prior else None

# Labor
series = fetch_series("PAYEMS", 24)
latest, prior = latest_and_prior(series, relativedelta(months=1))
derived["PAYEMS_MoM"] = latest - prior if prior else None

series = fetch_series("UNRATE", 24)
latest, prior = latest_and_prior(series, relativedelta(months=1))
derived["UNRATE_MoM"] = latest - prior if prior else None

series = fetch_series("AHETPI", 400)
latest, prior = latest_and_prior(series, relativedelta(years=1))
derived["AHETPI_YoY"] = (latest/prior - 1)*100 if prior else None

# Liquidity WoW
for s, key in [("WALCL","WALCL_WoW"),("RRPONTSYD","RRP_WoW"),("WTREGEN","TGA_WoW")]:
    series = fetch_series(s, 30)
    latest, prior = latest_and_prior(series, relativedelta(weeks=1))
    derived[key] = latest - prior if prior else None

# Markets
for s, key in [("SP500","SP500_1d"),("VIXCLS","VIX_1d"),("DTWEXBGS","DXY_1d")]:
    series = fetch_series(s, 5)
    latest, prior = latest_and_prior(series, relativedelta(days=1))
    derived[key] = latest - prior if prior else None

with open("derived.json","w") as f:
    json.dump(derived,f,indent=2)
