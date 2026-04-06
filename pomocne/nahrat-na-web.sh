#!/bin/bash

# Skript pro nahrání změn zpěvníku na GitHub

cd /home/martin/MEGA/samhita-songbook

echo "================================================"
echo "  📤 Nahrávám zpěvník na GitHub"
echo "================================================"
echo ""

# Zobraz změny
echo "Změněné soubory:"
git status --short
echo ""

# Zeptej se na popis změn
read -p "Popis změn (Enter = 'Aktualizace zpěvníku'): " popis

# Pokud je prázdný, použij výchozí
if [ -z "$popis" ]; then
  popis="Aktualizace zpěvníku"
fi

echo ""
echo "Nahrávám změny: $popis"
echo ""

# Přidej všechny změny
git add .

# Commit
git commit -m "$popis"

# Push na GitHub
git push

echo ""
echo "================================================"
echo "  ✅ Hotovo! Změny jsou na webu."
echo "  🌐 https://vinkler-collab.github.io/samhita-songbook/"
echo "================================================"
