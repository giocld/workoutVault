#!/bin/bash
# Manual sync script for workout vault

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$VAULT_DIR"

echo "Syncing workout vault..."

git pull origin main 2>/dev/null || echo "Pull skipped"

git add -A

if git diff --cached --quiet; then
    echo "No changes to commit"
else
    git commit -m "Auto: $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main 2>/dev/null || echo "Push skipped"
fi

echo "Sync complete!"
