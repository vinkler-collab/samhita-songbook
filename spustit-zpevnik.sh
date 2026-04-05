#!/bin/bash

# Skript pro spuštění lokálního zpěvníku
# Automaticky otevře prohlížeč a spustí server

cd /home/martin/MEGA/samhita-songbook

echo "================================================"
echo "  🎵 Spouštím Samhita Songbook"
echo "================================================"
echo ""
echo "  Zpěvník poběží na: http://localhost:8000"
echo ""
echo "  Pro ZASTAVENÍ serveru stiskněte Ctrl+C"
echo ""
echo "================================================"
echo ""

# Otevři prohlížeč po 2 sekundách na pozadí
(sleep 2 && xdg-open http://localhost:8000) &

# Spusť server
python3 -m http.server 8000
