---
description: Automatically merge and consolidate similar patterns
allowed-tools: [Bash]
---

Execute similar pattern merging.

Detects patterns with Levenshtein distance below threshold and automatically consolidates them. All scores (TF-IDF, PMI, time decay, composite) are recalculated after merging.

Execution:
1. Detect similar patterns with scripts/merge-similar-patterns.sh
2. Consolidate low-frequency patterns into high-frequency ones
3. Merge counts, sessions, and contexts
4. Automatically recalculate all scores
5. Display merge results

Merge logic:
- Keep the pattern with higher occurrence frequency
- Consolidate counts, sessions, and contexts
- Record original in merged_from field
- Adopt the most recent last_seen date

Notes:
- This operation is irreversible
- Normally runs automatically on SessionEnd
- Execute manually with caution

```bash
if [ ! -f scripts/merge-similar-patterns.sh ]; then
  echo "❌ merge-similar-patterns.sh not found"
  exit 1
fi

echo "🔄 Starting pattern merge..."
echo ""

# Execute merge
MERGE_OUTPUT=$(bash scripts/merge-similar-patterns.sh 2>&1)
MERGE_STATUS=$?

# Display results
echo "$MERGE_OUTPUT"

if [ $MERGE_STATUS -eq 0 ]; then
  echo ""
  echo "✅ Merge completed"
  echo ""
  echo "💡 To view updated scores:"
  echo "   /as-you:show-scores"
else
  echo ""
  echo "❌ Error occurred during merge"
  exit 1
fi
```
