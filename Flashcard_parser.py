import sqlite3
import json

DB_PATH = r"C:\Users\adamw\AppData\Roaming\Anki2\User 1\collection.anki2"

# Die sprechenden Tags für die Klausuren
klausur_tags = [
    "Arithmetik",
    "Cache",
    "Formeln",
    "Generel",
    "Mips",
    "Multiprozessoren",
    "Pipeline",
    "Storage",
    "Virtualisierung"
]

deck_names = [f"Klausur_{i}" for i in range(1, 10)]

def get_deck_ids_for_sf(cursor, sf_value):
    query = """
    SELECT DISTINCT c.did
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE n.sfld = ?
    """
    cursor.execute(query, (sf_value,))
    return [row[0] for row in cursor.fetchall()]

def get_front_fields_for_deck(cursor, deck_id):
    query = """
    SELECT n.sfld
    FROM notes n
    JOIN cards c ON n.id = c.nid
    WHERE c.did = ?
    """
    cursor.execute(query, (deck_id,))
    return [row[0] for row in cursor.fetchall()]

def get_back_fields_for_deck(cursor, deck_id):
    query = """
    SELECT n.flds
    FROM notes n
    JOIN cards c ON n.id = c.nid
    WHERE c.did = ?
    """
    cursor.execute(query, (deck_id,))
    back_fields = []
    for (flds,) in cursor.fetchall():
        fields = flds.split('\x1f')
        if len(fields) > 1:
            back_fields.append(fields[1])
        else:
            back_fields.append("")
    return back_fields

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    results = {}

    for i, deck_name in enumerate(deck_names):
        tag = klausur_tags[i]
        print(f"Processing notes with front field = '{deck_name}' (tag: {tag})...")
        deck_ids = get_deck_ids_for_sf(cursor, deck_name)
        if not deck_ids:
            print(f"  No deck IDs found for '{deck_name}'")
            continue

        for did in deck_ids:
            fronts = get_front_fields_for_deck(cursor, did)
            backs = get_back_fields_for_deck(cursor, did)

            # Entferne Einträge, deren front field == Klausur_x ist oder die mit "Deck_" anfangen
            filtered = [
                (f, b)
                for f, b in zip(fronts, backs)
                if not f.startswith("Deck_") and f != deck_name
            ]

            if not filtered:
                print(f"  Keine gültigen Karten für '{tag}' gefunden.")
                continue

            key = f"{tag} (deck id {did})"
            results[key] = [{"front": f, "back": b} for f, b in filtered]

    conn.close()

    with open("Flashcards.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Results saved to Flashcards.json")

if __name__ == "__main__":
    main()
