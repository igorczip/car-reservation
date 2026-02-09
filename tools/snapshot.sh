#!/usr/bin/env bash
set -euo pipefail

TS="$(date +"%Y-%m-%d_%H-%M-%S")"
mkdir -p snapshots backups

echo "== Snapshot: $TS =="

# -----------------------------
# 1) System + toolchain
# -----------------------------
{
  echo "# OS"
  cat /etc/os-release 2>/dev/null || true
  echo
  echo "# Kernel"
  uname -a 2>/dev/null || true
  echo
  echo "# Python / Poetry"
  python --version 2>&1 || true
  which python 2>&1 || true
  poetry --version 2>&1 || true
  echo
  echo "# Poetry env info"
  poetry env info 2>&1 || true
} > "snapshots/system_${TS}.txt"

# -----------------------------
# 2) Poetry deps snapshot
# -----------------------------
poetry show --tree > "snapshots/poetry_deps_tree_${TS}.txt" || true
poetry check > "snapshots/poetry_check_${TS}.txt" || true

# -----------------------------
# 3) Git snapshot + patch
# -----------------------------
{
  echo "# HEAD"
  git rev-parse HEAD 2>/dev/null || true
  echo
  echo "# Status"
  git status 2>/dev/null || true
  echo
  echo "# Remotes"
  git remote -v 2>/dev/null || true
} > "snapshots/git_${TS}.txt"

git diff > "snapshots/uncommitted_${TS}.patch" || true

# -----------------------------
# 4) Sanitizované env (bez tajných klíčů)
# -----------------------------
{
  echo "# Env (sanitized)"
  printenv | sort | grep -Ev 'SECRET|PASSWORD|TOKEN|KEY|PASS|PWD' || true
} > "snapshots/container_env_sanitized_${TS}.txt"

# -----------------------------
# 5) OpenAPI snapshot (už máte soubory - jen “zatím” kopie pro archiv)
# -----------------------------
if [[ -f "src/openapi.json" ]]; then
  cp "src/openapi.json" "snapshots/openapi_${TS}.json"
fi
if [[ -f "src/openapi_full.json" ]]; then
  cp "src/openapi_full.json" "snapshots/openapi_full_${TS}.json"
fi

# -----------------------------
# 6) Postgres dump (bez Dockeru)
# -----------------------------
if command -v pg_dump >/dev/null 2>&1; then
  echo "Dumping Postgres via pg_dump (host=db)..."
  PGPASSWORD="${POSTGRES_PASSWORD:-car}" pg_dump \
    -h db -p 5432 -U "${POSTGRES_USER:-car}" -d "${POSTGRES_DB:-car_reservation}" -Fc \
    > "backups/db_${TS}.dump"
else
  echo "WARNING: pg_dump not found in container. DB dump skipped."
fi


echo "DONE:
- snapshots/*_${TS}.txt (+ openapi copies if present)
- backups/db_${TS}.dump (Postgres dump)
"
