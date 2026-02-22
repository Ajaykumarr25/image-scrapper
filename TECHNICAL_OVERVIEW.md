# Full-Site Image Scraper — Technical Overview

## Architecture

The scraper is a single-file Python application (`scraper.py`, ~1050 lines) built with a **Tkinter GUI** front-end and a multi-phase **Selenium + Pillow + openpyxl** backend pipeline.

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  Tkinter UI │ ──► │  BFS Crawler │ ──► │ Image Scraper│ ──► │ Excel Gen  │
│ (dark theme)│     │  (Selenium)  │     │  + Downloads │     │ (openpyxl) │
└─────────────┘     └─────────────┘     └──────────────┘     └────────────┘
```

## Technology Stack

| Component         | Library           | Purpose                                      |
|-------------------|-------------------|----------------------------------------------|
| Web automation    | Selenium 4        | Headless Chrome — renders JS, checks visibility |
| HTML parsing      | BeautifulSoup 4   | Link extraction during BFS crawl             |
| SVG → PNG         | PyMuPDF (`fitz`)  | Renders SVG at 2× scale, no native C deps    |
| Image processing  | Pillow (PIL)      | Thumbnails, background correction, format conversion |
| Excel generation  | openpyxl          | Multi-sheet workbook with embedded images     |
| HTTP downloads    | Requests          | Image file downloads with streaming           |
| GUI               | Tkinter           | Dark-themed desktop interface                 |
| Hashing           | hashlib (MD5)     | SVG deduplication across pages                |

## Processing Pipeline

### Phase 1 — Site Crawl (BFS)
- Starts from user-provided homepage URL
- `normalize_url()` — deduplicates URLs (strips fragments, normalizes paths)
- `discover_links()` — extracts `<a href>` links, filters to same domain
- Skips non-HTML resources (PDFs, images, JS, CSS, etc.) via `SKIP_EXTENSIONS`
- Respects configurable `max_pages` limit (default 20, max 100)
- Returns ordered list of discovered page URLs

### Phase 2 — Image Extraction & Download
- `extract_images()` — uses **Selenium** (not BeautifulSoup) for visibility filtering:
  - `element.is_displayed()` — skips hidden/CSS-hidden images
  - `element.size` — skips images < 5×5px (tracking pixels, spacers)
  - Resolves `src`, `data-src`, `data-lazy-src`, `srcset`
  - Extracts inline `<svg>` elements (visible, > 10×10px, > 50 chars)
- **SVG deduplication** — MD5 hash of SVG content, shared across all pages
- `download_image()` — returns `(local_path, svg_source_code)` tuple
  - Reads SVG source before conversion for later color analysis
- `convert_svg_to_png()` — PyMuPDF renders at 2× matrix scale
- `convert_webp_to_png()` — Pillow format conversion

### Phase 2.5 — SVG Color Analysis
- `_extract_svg_colors()` — regex-based extraction of:
  - `fill="..."` and `stroke="..."` attributes
  - `style="fill: ...; stroke: ..."` inline styles
  - `<style>` block CSS rules
- `_parse_color()` — handles hex (`#RGB`, `#RRGGBB`), `rgb()/rgba()`, and 40+ named CSS colors
- `_luminance()` — perceptual luminance formula: `(0.299R + 0.587G + 0.114B) / 255`
- `_svg_contrast_bg()` — maps luminance to background:
  - `> 0.7` (light/white SVG) → dark bg `(50, 55, 65)`
  - `< 0.3` (dark SVG) → light bg `(240, 242, 245)`
  - Otherwise → neutral `(230, 232, 235)`

### Phase 2.5b — Thumbnail Generation
- `make_thumbnail(image_path, bg_hint=None)`:
  - Resizes to max 150×100px (Lanczos)
  - 8px padding on all sides
  - Background selection: `bg_hint` (SVG) > light/transparent detection > default
  - Raster images: dark bg `(50,55,65)` for light/transparent, light bg `(230,232,235)` for dark
  - Adaptive 2px border (light border on dark bg, dark border on light bg)
  - Saves as `_thumb.png`

### Phase 3 — Excel Generation
- `save_to_excel()` creates a multi-sheet workbook:
  - **Summary sheet**: accessibility metrics + per-page breakdown table
  - **Per-page sheets**: named by URL path (`_safe_sheet_name`, 31-char limit with dedup)
  - Pages with 0 images are skipped (no empty sheets)
- `_build_page_sheet()`:
  - Row 1: merged page URL bar (blue accent)
  - Row 2: column headers (dark bg)
  - Row 3+: S.No | Image Preview | Image Source URL | Alt Text
  - Row height: 90px for image cells
  - Alternating row fills, thin borders
  - Alt text: red `⚠ MISSING` tag with red fill when absent
- `_build_summary()`:
  - Total images, with/missing alt text counts
  - Accessibility score with color-coded font (green ≥80%, yellow ≥50%, red <50%)
  - Pages crawled table with image counts and sheet name references

## GUI (Tkinter)

- Dark theme: `#0F172A` background, `#1E293B` cards, `#6366F1` accent
- Single URL entry field with max-pages spinner (1–100)
- Progress bar + scrollable log with emoji status markers
- Threaded worker — UI stays responsive during scraping

## Error Handling

- Per-image: download failures logged, other images still proceed
- Per-page: `try/except` with log entry, scraping continues to next page
- SVG conversion: falls back to original path on failure
- Thumbnail: returns `None`, cell shows "(unsupported)"

## File Structure

```
image scrapper/
├── scraper.py            # All application code (~1050 lines)
├── requirements.txt      # Python dependencies
├── .gitignore            # Excludes venv, downloads, xlsx output
├── downloaded_images/    # Created at runtime — image cache
└── scraped_images.xlsx   # Generated report
```

## Dependencies

```
requests>=2.31.0
beautifulsoup4>=4.12.0
openpyxl>=3.1.0
Pillow>=10.0.0
pymupdf>=1.27.0
selenium>=4.15.0
```

Also requires **Google Chrome** and **ChromeDriver** (auto-managed by Selenium 4).
