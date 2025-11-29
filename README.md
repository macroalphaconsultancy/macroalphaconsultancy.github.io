# Macro Alpha Consultancy — GitHub Pages Site

This repository contains a static website for *Macro Alpha Consultancy (MAC)*.

## Structure
- `index.html` — Main page.
- `style.css` — Stylesheet.
- `script.js` — Loads research.json and renders Research Notes.
- `research.json` — Research items shown on the Research Notes section.
- `assets/logo.png` — Company logo (transparent PNG).
- `assets/favicon.png` — Favicon (64x64 PNG).

## How to update Research Notes
1. Open `research.json`.
2. Add a new object with fields:
```json
{
  "title": "Article Title",
  "author": "Your Name",
  "source": "Medium",
  "url": "https://link-to-article",
  "date": "YYYY-MM-DD",
  "summary": "Short summary or teaser."
}
```
3. Save the file and push to GitHub. The site will update automatically.

The `script.js` automatically creates a card for each entry and displays an icon for known sources (Medium). Unknown sources show a generic link icon.

## How to update Founder / About / Services
Edit `index.html`:
- `#about` section contains About Us copy.
- `#services` contains service cards — duplicate or modify `<div class="card">` blocks to add/remove services.
- `#founder` section contains founder bio and contact; update text or replace the placeholder CV link at `assets/Ishrit_Tewari_CV.pdf`.

## Adding CV or Assets
Place files in the `assets` folder and link them in `index.html`, for example:
```html
<a href="assets/Ishrit_Tewari_CV.pdf">Download CV</a>
```

## Deployment
Create a repository named `macroalphaconsultancy.github.io` and push all files to the repository root (not a subfolder). GitHub Pages will serve the site at `https://macroalphaconsultancy.github.io`.

