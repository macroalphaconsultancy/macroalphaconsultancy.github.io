# Derived Data Schema

All derived fields are computed from raw.json and written to derived.json.

## Conventions
- `_1d`   : 1-day change (market series)
- `_WoW`  : week-over-week change
- `_MoM`  : month-over-month change
- `_YoY`  : year-over-year change
- Spreads are expressed in percentage points

## Core Derived Fields

### Rates & Curves
- DGS10_1d
- DGS2_1d
- DGS30_1d
- spread_2s10s
- spread_10s30s
- real_10y_1d
- term_premium_10y_1d

### Inflation
- CPI_YoY
- CoreCPI_YoY

### Labor
- PAYEMS_MoM
- UNRATE_MoM
- AHETPI_YoY

### Liquidity
- WALCL_WoW
- RRP_WoW
- TGA_WoW

### Markets
- SP500_1d
- VIX_1d
- DXY_1d

All fields are nullable if data is unavailable.
