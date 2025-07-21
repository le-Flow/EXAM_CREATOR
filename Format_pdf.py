import os
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

# Configuration
INPUT_FILE = "Flashcards Druckvorlage.pdf"
OUTPUT_FILE = "flashcards_output.html"
CARDS_PER_GRID = 9
GRID_ROWS = 3
GRID_COLS = 3

# Convert PDF pages to images
print("Converting PDF to images...")
images = convert_from_path(INPUT_FILE, dpi=150)
total_pages = len(images)
assert total_pages % 2 == 0, "PDF should have even number of pages (front/back pairs)"

# Utility: convert image to base64 for HTML embedding
def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# Build grids
html_blocks = []
for i in range(0, total_pages, 2 * CARDS_PER_GRID):
    # Fronts (odd pages)
    fronts = images[i:i + CARDS_PER_GRID]
    # Backs (even pages)
    backs = images[i + CARDS_PER_GRID:i + 2 * CARDS_PER_GRID]

    # Pad if not full
    while len(fronts) < CARDS_PER_GRID:
        fronts.append(Image.new("RGB", fronts[0].size, (255, 255, 255)))
    while len(backs) < CARDS_PER_GRID:
        backs.append(Image.new("RGB", backs[0].size, (255, 255, 255)))

    for row in range(GRID_ROWS):
        front_html += "<tr>"
        for col in range(GRID_COLS):
            index = row * GRID_COLS + col
            img_data = pil_to_base64(fronts[index])
            front_html += f'<td><img src="data:image/png;base64,{img_data}" width="200"/></td>'
        front_html += "</tr>"
    front_html += "</table>"

    for row in range(GRID_ROWS):
        back_html += "<tr>"
        for col in range(GRID_COLS):
            index = (GRID_ROWS - 1 - row) * GRID_COLS + (GRID_COLS - 1 - col)
            img_data = pil_to_base64(backs[index])
            back_html += f'<td><img src="data:image/png;base64,{img_data}" width="200"/></td>'
        back_html += "</tr>"
    back_html += "</table>"

# Assemble final HTML
print("Generating HTML...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(html_blocks)
    f.write("</body></html>")

print(f"Done. Output saved to: {OUTPUT_FILE}")
