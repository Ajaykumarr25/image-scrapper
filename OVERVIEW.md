# Full-Site Image Scraper — Overview

## What It Does

This tool automatically scans an entire website and collects every image it finds, then creates a detailed Excel report. It's designed for **web accessibility auditing** — checking whether images have proper alt text descriptions.

## How to Use

1. **Run the app**: Double-click or run `python scraper.py`
2. **Enter a website URL**: Type or paste the homepage address (e.g. `https://example.com`)
3. **Set page limit**: Choose how many pages to scan (default: 20)
4. **Click "Start Crawl & Scrape"** and wait for it to finish
5. **Open the Excel file** (`scraped_images.xlsx`) to see results

## What You Get

### Excel Report with Two Types of Sheets

**Summary Sheet**
- Total number of images found across the entire website
- How many images have alt text descriptions ✅
- How many images are missing alt text ⚠️
- An accessibility score percentage
- A table showing each page and how many images it contains

**Page Sheets** (one per webpage)
- A preview thumbnail of each image
- The image's web address (URL)
- The image's alt text — or a red **⚠ MISSING** warning if it has none

## Smart Features

| Feature | What It Means |
|---------|---------------|
| **Automatic page discovery** | You only enter the homepage — the tool finds all other pages automatically |
| **Handles modern websites** | Uses a real browser engine, so JavaScript-heavy sites work correctly |
| **SVG support** | Vector graphics (SVGs) are converted to regular images for the report |
| **Smart backgrounds** | White logos on white backgrounds? The tool detects image colors and adds a contrasting background so every image is clearly visible |
| **No duplicates** | Repeated images (like logos that appear on every page) are only counted once |
| **Only visible images** | Ignores hidden images, tracking pixels, and tiny decorative elements |

## Requirements

- **Python 3.10+** installed on your computer
- **Google Chrome** browser installed
- Install the required packages by running:
  ```
  pip install -r requirements.txt
  ```

## Example Output

After scanning a website with 15 pages and 87 images, you'd get:

```
📊 Summary:
   Pages crawled:  15
   Total images:   87
   With alt text:  62
   Missing alt:    25
   Accessibility:  71.3%
```

Plus 15 Excel sheets (one per page) with image previews and alt text status.
