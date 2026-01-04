---
description: Detect and display similar patterns for merging
---

Execute similar pattern detection functionality.

Using Levenshtein distance, detect patterns that may be similar (e.g., "test" and "testing") and display merge candidates.

Execution:
1. Detect similar patterns with scripts/detect-similar-patterns.sh
2. Display detected similar pairs (distance, occurrence counts, recommended merge target)
3. Notify that merging can be performed with /as-you:merge-patterns

Detection threshold:
- Default: Levenshtein distance ≤ 2
- Configurable via SIMILARITY_THRESHOLD environment variable

Example output:
```
Similar pair: test / testing (distance: 3)
  Occurrences: 176 / 129 → Total 305
  Recommended merge target: test

Similar pair: deploy / deployment (distance: 4)
  Occurrences: 84 / 84 → Total 168
  Recommended merge target: deploy
```

```bash
if [ ! -f scripts/detect-similar-patterns.sh ]; then
  echo "❌ detect-similar-patterns.sh not found"
  exit 1
fi

echo "🔍 Detecting similar patterns..."
echo ""

SIMILAR_PATTERNS=$(bash scripts/detect-similar-patterns.sh 2>/dev/null)
SIMILAR_COUNT=$(echo "$SIMILAR_PATTERNS" | jq '. | length' 2>/dev/null || echo "0")

if [ "$SIMILAR_COUNT" -eq 0 ]; then
  echo "✓ No similar patterns detected"
  exit 0
fi

echo "📊 Detected ${SIMILAR_COUNT} similar pairs:"
echo ""

echo "$SIMILAR_PATTERNS" | jq -r '.[] |
  "Similar pair: \(.patterns | join(" / ")) (distance: \(.distance))
  Occurrences: \(.counts | join(" / ")) → Total \(.total_count)
  Recommended merge target: \(.suggestion)
"'

echo ""
echo "💡 To merge patterns:"
echo "   /as-you:merge-patterns"
echo ""
echo "⚙️  To change detection threshold:"
echo "   SIMILARITY_THRESHOLD=3 bash scripts/detect-similar-patterns.sh"
```
