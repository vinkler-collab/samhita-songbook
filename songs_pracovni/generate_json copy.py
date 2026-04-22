import os
import json
import re
import unicodedata
from datetime import date

# Konfigurace
SONGS_DIR = 'songs'
JSON_FILE = 'songs.json'
PDF_DIR = 'pdfs'  # Složka, kde máš uložená PDF

def normalize_for_sort(text):
    """Převede text na malá písmena a odstraní diakritiku pro potřeby řazení."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def extract_metadata_and_analysis(file_path):
    """Vytáhne název, kategorii, tagy a text analýzy z ChordPro souboru."""
    metadata = {
        "title": os.path.basename(file_path).replace('.pro', ''),
        "category": None,
        "tags": None,
        "analysis": ""
    }
    
    analysis_lines = []
    is_analysis_section = False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                raw_line = line.strip()
                
                # Detekce začátku sekce analýzy
                if '{start_of_analysis}' in raw_line.lower():
                    is_analysis_section = True
                    continue
                
                # Pokud jsme v sekci analýzy, sbíráme řádky
                if is_analysis_section:
                    analysis_lines.append(line.rstrip())
                    continue

                # Standardní metadata
                if not raw_line or raw_line.startswith('#'):
                    continue
                
                t_match = re.search(r'\{(?:t|title):\s*(.*?)\}', raw_line, re.IGNORECASE)
                if t_match:
                    metadata["title"] = t_match.group(1).strip()
                    continue
                
                c_match = re.search(r'\{category:\s*(.*?)\}', raw_line, re.IGNORECASE)
                if c_match:
                    metadata["category"] = c_match.group(1).strip()
                    continue
                
                tags_match = re.search(r'\{tags:\s*(.*?)\}', raw_line, re.IGNORECASE)
                if tags_match:
                    metadata["tags"] = [t.strip() for t in tags_match.group(1).split(',') if t.strip()]
                    continue
                    
    except Exception as e:
        print(f"Chyba při čtení souboru {file_path}: {e}")
    
    metadata["analysis"] = "\n".join(analysis_lines).strip()
    return metadata

def update_songs_json():
    # Načtení stávajících dat
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

    # HLAVNÍ CYKLUS
    for filename in os.listdir(SONGS_DIR):
        if filename.endswith('.pro') and not filename.startswith('_'):
            file_slug = filename[:-4]
            file_path = os.path.join(SONGS_DIR, filename)
            
            print(f"-> Zpracovávám: {filename}")
            
            # Získáme metadata i analýzu
            meta = extract_metadata_and_analysis(file_path)
            
            # Kontrola existence PDF
            pdf_path = os.path.join(PDF_DIR, f"{file_slug}.pdf")
            has_pdf = os.path.exists(pdf_path)
            
            if file_slug in existing_data:
                song = existing_data[file_slug]
                song['name'] = meta['title']
                if meta['category']: song['category'] = meta['category']
                if meta['tags'] is not None: song['tags'] = meta['tags']
                # Aktualizujeme nové položky
                song['hasPDF'] = has_pdf
                song['analysis'] = meta['analysis']
            else:
                song = {
                    "name": meta['title'],
                    "category": meta['category'] if meta['category'] else "Ostatní",
                    "file": file_slug,
                    "audio": f"audio/{file_slug}.mp3",
                    "tags": meta['tags'] if meta['tags'] is not None else [],
                    "dateAdded": str(date.today()),
                    "hasPDF": has_pdf,
                    "analysis": meta['analysis']
                }
            new_songs_list.append(song)

    # Řazení
    new_songs_list.sort(key=lambda x: normalize_for_sort(x['name']))

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_songs_list, f, indent=2, ensure_ascii=False)
    
    print(f"--- Hotovo! V JSONu je {len(new_songs_list)} písniček. ---")

if __name__ == "__main__":
    update_songs_json()