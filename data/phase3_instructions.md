# Phase 3 – Frontend Binding Instructions

## Step 1: Add loader.js
Place loader.js in the root or /data folder and include it in ALL dashboards:

<script src="/data/loader.js"></script>

(Add before </body>)

## Step 2: Add data-key attributes
For every numeric field, add data-key without changing layout.

Examples:
- raw series: data-key="DGS10"
- derived series: data-key="DGS10_1d"

## Step 3: Do NOT add logic to HTML
HTML must only contain placeholders and keys.

## Step 4: Validation
Open dashboard.html and verify values populate.

If data is missing, placeholder (—) remains.

## Step 5: Extend
Any new metric only requires:
- adding to backend JSON
- adding matching data-key in HTML

No JS changes required.
