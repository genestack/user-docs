#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────
SRC_REPO="git@github.com:genestack/odms-internal.git"
SRC_BRANCH="develop"
SRC_DIR="demo-materials/jupyter-notebook/odm-trial/user-docs"

DST_REPO="git@github.com:genestack/user-docs.git"
DST_BRANCH="develop"
DST_DIR="docs/user-guide/doc-odm-user-guide/doc-odm-user-guide/notebooks"

PR_TITLE="Sync notebooks from odms-internal"
# ─────────────────────────────────────────────────────────────────────

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

printf "==> Cloning source repo (sparse, odms-internal @ $SRC_BRANCH)...\n"
git clone --depth 1 --branch "$SRC_BRANCH" --single-branch \
    --filter=blob:none --sparse \
    "$SRC_REPO" "$TMP/src"
git -C "$TMP/src" sparse-checkout set "$SRC_DIR"

printf "\n==> Cloning target repo (sparse, user-docs @ $DST_BRANCH)...\n"
git clone --depth 1 --branch "$DST_BRANCH" --single-branch \
    --filter=blob:none --sparse \
    "$DST_REPO" "$TMP/dst"
git -C "$TMP/dst" sparse-checkout set "$DST_DIR"

printf "\n==> Syncing $SRC_DIR -> $DST_DIR...\n"
mkdir -p "$TMP/dst/$DST_DIR"
rsync -av --delete "$TMP/src/$SRC_DIR/" "$TMP/dst/$DST_DIR/"

cd "$TMP/dst"

git add "$DST_DIR"

if git diff --staged --quiet; then
    echo "No changes to sync. Exiting."
    exit 0
fi

BRANCH="docs/sync-notebooks-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"

git commit -m "Sync notebooks folder from odms-internal"

git push -u origin "$BRANCH"

gh pr create \
    --repo genestack/user-docs \
    --base "$DST_BRANCH" \
    --head "$BRANCH" \
    --title "$PR_TITLE" \
    --body "Automated sync of notebooks from \`genestack/odms-internal\` ($SRC_BRANCH branch)."

printf "\n==> Done.\n"
