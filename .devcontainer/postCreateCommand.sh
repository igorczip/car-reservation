#!/usr/bin/env bash
set -e

cd /workspace

poetry --version

# pojistka: venv v projektu (./.venv)
poetry config virtualenvs.in-project true --local || true

# instalace závislostí podle poetry.lock
poetry install --no-interaction --no-ansi --no-root

echo "✅ Hotovo. Závislosti nainstalované do /workspace/.venv"
echo "✅ Django (host):   http://127.0.0.1:8010/   (container: 0.0.0.0:8000)"
echo "✅ Postgres (host): 127.0.0.1:5433           (container: db:5432)"
echo "✅ PlantUML (host): http://127.0.0.1:18081/"
