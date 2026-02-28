"""Quick test to verify homepage image extraction."""
from scraper import create_driver, load_page, extract_images

driver = create_driver()
load_page(driver, "https://www.tzieldhcp.com/")
images = extract_images(driver, "https://www.tzieldhcp.com/")

with open("test_result.txt", "w", encoding="utf-8") as f:
    f.write("Total images found: %d\n" % len(images))
    for i, img in enumerate(images):
        src = img["src"][:100]
        alt = img.get("alt", "N/A")
        f.write("%d. %s | alt=%s\n" % (i + 1, src, alt))

driver.quit()
print("Done. Found %d images. Check test_result.txt" % len(images))
