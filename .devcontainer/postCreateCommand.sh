#!/usr/bin/env bash
set -e

cd /workspace

poetry --version

# pokud chceš, můžeš fixně přepnout do "dependency-only" režimu,
# ale není nutné – jen nebudeme instalovat root balíček.
poetry install --no-interaction --no-ansi --no-root

echo "✅ Hotovo. Django běží v kontejneru web a je mapovaný na http://127.0.0.1:8010/"
echo "✅ PlantUML je na http://127.0.0.1:18081/"
