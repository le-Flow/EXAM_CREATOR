import sqlite3
import json

DB_PATH = r"C:\Users\adamw\AppData\Roaming\Anki2\User 1\collection.anki2"

deck_names = [f"Deck_{i}" for i in range(1, 6)]

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

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    results = {}

    for deck_name in deck_names:
        print(f"Processing notes with front field = '{deck_name}'...")
        deck_ids = get_deck_ids_for_sf(cursor, deck_name)
        if not deck_ids:
            print(f"  No deck IDs found for '{deck_name}'")
            continue

        for did in deck_ids:
            fronts = get_front_fields_for_deck(cursor, did)
            fronts = [f for f in fronts if not f.startswith("Deck_")]
            key = f"{deck_name} (deck id {did})"
            results[key] = fronts

    conn.close()

    with open("deck_fronts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Results saved to deck_fronts.json")

if __name__ == "__main__":
    main()
