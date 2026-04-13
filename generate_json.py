import os
import json
import re
import unicodedata  # Potřebujeme pro správné řazení
from datetime import date

# Konfigurace
SONGS_DIR = 'songs'
JSON_FILE = 'songs.json'

def normalize_for_sort(text):
    """Převede text na malá písmena a odstraní diakritiku pro potřeby řazení."""
    # Např. 'Ā' -> 'A', 'ś' -> 's'
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def extract_metadata(file_path):
    """Vytáhne název, kategorii a tagy z ChordPro souboru, ignoruje komentáře."""
    metadata = {
        "title": os.path.basename(file_path).replace('.pro', ''),
        "category": None,
        "tags": None
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                t_match = re.search(r'\{(?:t|title):\s*(.*?)\}', line, re.IGNORECASE)
                if t_match:
                    metadata["title"] = t_match.group(1).strip()
                    continue
                
                c_match = re.search(r'\{category:\s*(.*?)\}', line, re.IGNORECASE)
                if c_match:
                    metadata["category"] = c_match.group(1).strip()
                    continue
                    
                tags_match = re.search(r'\{tags:\s*(.*?)\}', line, re.IGNORECASE)
                if tags_match:
                    metadata["tags"] = [t.strip() for t in tags_match.group(1).split(',') if t.strip()]
                    continue
                
    except Exception as e:
        print(f"Chyba při čtení souboru {file_path}: {e}")
    
    return metadata

def update_songs_json():
    existing_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                for s in json.load(f):
                    existing_data[s['file']] = s
            except json.JSONDecodeError:
                pass

    new_songs_list = []
    
    if not os.path.exists(SONGS_DIR):
        print(f"Chyba: Složka '{SONGS_DIR}' neexistuje!")
        return

    # Procházíme složku - pokud soubor neexistuje, do new_songs_list se nedostane (tím se maže z JSONu)
    for filename in os.listdir(SONGS_DIR):
        if filename.endswith('.pro'):
            file_slug = filename[:-4]
            file_path = os.path.join(SONGS_DIR, filename)
            
            meta = extract_metadata(file_path)
            
            if file_slug in existing_data:
                song = existing_data[file_slug]
                song['name'] = meta['title']
                if meta['category']:
                    song['category'] = meta['category']
                if meta['tags'] is not None:
                    song['tags'] = meta['tags']
            else:
                song = {
                    "name": meta['title'],
                    "category": meta['category'] if meta['category'] else "Ostatní",
                    "file": file_slug,
                    "audio": f"audio/{file_slug}.mp3",
                    "tags": meta['tags'] if meta['tags'] is not None else [],
                    "dateAdded": str(date.today())
                }
            
            new_songs_list.append(song)

    # VYLEPŠENÉ ŘAZENÍ: Použijeme naši normalizační funkci
    new_songs_list.sort(key=lambda x: normalize_for_sort(x['name']))

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_songs_list, f, indent=2, ensure_ascii=False)
    
    print(f"Hotovo! V JSONu je {len(new_songs_list)} písniček. Neexistující byly odstraněny.")

if __name__ == "__main__":
    update_songs_json()