#!/bin/bash
# SessionEnd hook: Archive session notes, track patterns, and merge similar patterns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$REPO_ROOT}"

# Archive session notes
"${REPO_ROOT}/scripts/archive-note.sh"

# Track pattern frequency
"${REPO_ROOT}/scripts/track-frequency.sh"

# Merge similar patterns automatically
echo "📊 類似パターンをチェック中..."
MERGE_OUTPUT=$("${REPO_ROOT}/scripts/merge-similar-patterns.sh" 2>&1)
MERGE_COUNT=$(echo "$MERGE_OUTPUT" | grep -c "マージしました" 2>/dev/null || echo "0")

if [ "$MERGE_COUNT" -gt 0 ]; then
  echo "✅ ${MERGE_COUNT} 件のパターンをマージしました"
  echo "$MERGE_OUTPUT" | grep "マージしました"
else
  echo "✓ 類似パターンなし"
fi

exit 0
