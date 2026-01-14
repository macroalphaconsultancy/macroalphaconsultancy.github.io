# Wick Research — GitHub Pages Site

This repository contains a static website for *Wick Research*.

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

