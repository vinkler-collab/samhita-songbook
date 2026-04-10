import os
import json
import re
from datetime import date

# Konfigurace - uprav podle potřeby
SONGS_DIR = 'songs'
JSON_FILE = 'songs.json'

def extract_metadata(file_path):
    """Vytáhne název a případně další metadata přímo z ChordPro souboru."""
    title = os.path.basename(file_path).replace('.pro', '') # Záloha, kdyby chyběl tag
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Hledá {title: ...} nebo {t: ...}
            match = re.search(r'\{(?:t|title):\s*(.*?)\}', content, re.IGNORECASE)
            if match:
                title = match.group(1)
    except Exception as e:
        print(f"Chyba při čtení souboru {file_path}: {e}")
    
    return title

def update_songs_json():
    # Načteme stávající JSON, abychom nepřišli o ručně zadané kategorie nebo tagy
    existing_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                # Vytvoříme slovník pro rychlé hledání podle názvu souboru
                for s in json.load(f):
                    existing_data[s['file']] = s
            except json.JSONDecodeError:
                pass

    new_songs_list = []
    
    # Projdeme složku se soubory .pro
    for filename in os.listdir(SONGS_DIR):
        if filename.endswith('.pro'):
            file_slug = filename[:-4] # název bez .pro
            file_path = os.path.join(SONGS_DIR, filename)
            
            title = extract_metadata(file_path)
            
            if file_slug in existing_data:
                # Pokud písnička už v JSONu je, aktualizujeme jen název
                song = existing_data[file_slug]
                song['name'] = title
            else:
                # Pokud je nová, vytvoříme nový záznam s výchozími hodnotami
                song = {
                    "name": title,
                    "category": "Ostatní", # Můžeš si později upravit ručně v JSONu
                    "file": file_slug,
                    "audio": f"audio/{file_slug}.mp3",
                    "tags": [],
                    "dateAdded": str(date.today())
                }
            new_songs_list.append(song)

    # Seřadíme písničky abecedně podle jména
    new_songs_list.sort(key=lambda x: x['name'].lower())

    # Uložíme výsledek zpět
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_songs_list, f, indent=2, ensure_ascii=False)
    
    print(f"Hotovo! Zpracováno {len(new_songs_list)} písniček do {JSON_FILE}.")

if __name__ == "__main__":
    update_songs_json()