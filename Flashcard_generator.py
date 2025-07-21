import json
import os
import html
import re

FLASHCARDS_JSON = "Flashcards.json"
OUTPUT_HTML = "flashcards.html"
IMAGE_MEDIA_PATH = r"C:/Users/adamw/AppData/Roaming/Anki2/User 1/collection.media"

import os
import re

def convert_content_to_html(content, html_base_path, image_media_path):
    if not isinstance(content, str):
        return ""

    # Remove any raw path prefix before <img>
    content = re.sub(
        r'([^\s"<>\']+\/)+(?=<img\s)',
        '',
        content
    )

    # Fix existing <img src="paste-..."> tags
    def fix_img_src(m):
        filename = m.group(2)
        abs_img_path = os.path.join(image_media_path, filename)
        rel_path = os.path.relpath(abs_img_path, os.path.dirname(html_base_path)).replace("\\", "/")
        return f'{m.group(1)}{rel_path}{m.group(3)}'

    content = re.sub(
        r'(<img\s+[^>]*src=")(paste-[\w\d]+\.png|paste-[\w\d]+\.jpg)(")',
        fix_img_src,
        content
    )

    # Replace raw filenames only if they are NOT inside <img> tags already
    # To avoid replacing inside tags, split on <img and process only outside of img tags
    def replace_raw_filename_outside_img(text):
        def replacement(m):
            abs_img_path = os.path.join(image_media_path, m.group(1))
            rel_path = os.path.relpath(abs_img_path, os.path.dirname(html_base_path)).replace("\\", "/")
            return f'<img src="{rel_path}" alt="{m.group(1)}" class="flashcard-image"/>'
        return re.sub(
            r'\b(paste-[\w\d]+\.png|paste-[\w\d]+\.jpg)\b',
            replacement,
            text
        )


    # Split content on <img to separate parts that might contain tags
    parts = re.split(r'(<img[^>]*>)', content)
    # For parts which are actual img tags, leave them untouched
    # For other parts (outside img), replace raw filenames
    for i in range(0, len(parts), 2):
        parts[i] = replace_raw_filename_outside_img(parts[i])

    content = ''.join(parts)

    return content


def main():
    with open(FLASHCARDS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    html_parts = []
    html_parts.append("""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<title>Flashcards Druckvorlage</title>
<style>
    @page {
        size: A7 landscape;
        margin: 5mm;
    }
    body {
        font-family: Arial, sans-serif;
        font-size: 9pt;
        margin: 0;
        padding: 0;
    }
    .flashcard {
        width: 105mm;
        height: 74mm;
        box-sizing: border-box;
        border: 1px solid #333;
        padding: 5mm;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        page-break-after: always;
    }
    .flashcard.front {
        justify-content: center;
    }
    h3 {
        margin: 0 0 5px 0;
        font-size: 11pt;
        color: #111;
        text-align: center;
    }
    .flashcard-content {
        overflow-y: auto;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    .flashcard.front .flashcard-content {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    .flashcard-image {
        max-width: 100%;
        max-height: 50mm;
        margin: 5px 0;
    }
    .flashcard-content img {
        max-width: 100%;
        max-height: 50mm;
        margin: 5px 0;
        object-fit: contain; /* optional: keep aspect ratio */
    }
    .flashcard:not(.front) .flashcard-content {
        text-align: left;
        align-items: flex-start;
        justify-content: center;
    }
    ul {
        padding-left: 12px;
        margin: 0 0 5px 0;
    }
    li {
        margin-bottom: 2px;
    }
</style>
</head>
<body>
""")

    for deck_name, cards in data.items():
        simple_name = deck_name.split(" ")[0]

        for card in cards:
            front = convert_content_to_html(card.get("front", ""), OUTPUT_HTML, IMAGE_MEDIA_PATH)
            back = convert_content_to_html(card.get("back", ""), OUTPUT_HTML, IMAGE_MEDIA_PATH)

            # Vorderseite, mit zentriertem Text
            html_parts.append(f"""
            <div class="flashcard front">
                <h3>{simple_name}</h3>
                <div class="flashcard-content">{front}</div>
            </div>
            """)

            # Rückseite, normal linksbündig
            html_parts.append(f"""
            <div class="flashcard">
                <h3>{simple_name}</h3>
                <div class="flashcard-content">{back}</div>
            </div>
            """)

    html_parts.append("""
</body>
</html>
""")

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))

    print(f"HTML-Datei erzeugt: {OUTPUT_HTML}")
    print("→ Im Browser öffnen und als PDF drucken (A7 Querformat)")

if __name__ == "__main__":
    main()
