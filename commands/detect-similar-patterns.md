---
description: Detect and display similar patterns for merging
allowed-tools: [Bash]
---

Execute similar pattern detection functionality.

Using Levenshtein distance, detect patterns that may be similar (e.g., "test" and "testing") and display merge candidates.

Execution:
1. Detect similar patterns with similarity_detector.py
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
if [ ! -f scripts/similarity_detector.py ]; then
  echo "❌ similarity_detector.py not found"
  exit 1
fi

echo "🔍 Detecting similar patterns..."
echo ""

SIMILAR_PATTERNS=$(python3 scripts/similarity_detector.py 2>/dev/null)

echo "$SIMILAR_PATTERNS" | python3 <<'EOF'
import json
import sys

try:
    data = json.load(sys.stdin)

    if len(data) == 0:
        print("✓ No similar patterns detected")
        sys.exit(0)

    print(f"📊 Detected {len(data)} similar pairs:")
    print("")

    for item in data:
        patterns = ' / '.join(item['patterns'])
        distance = item['distance']
        counts = ' / '.join(str(c) for c in item['counts'])
        total = item['total_count']
        suggestion = item['suggestion']

        print(f"Similar pair: {patterns} (distance: {distance})")
        print(f"  Occurrences: {counts} → Total {total}")
        print(f"  Recommended merge target: {suggestion}")
        print("")

    print("💡 To merge patterns:")
    print("   /as-you:merge-patterns")
    print("")
    print("⚙️  To change detection threshold:")
    print("   SIMILARITY_THRESHOLD=3 python3 scripts/similarity_detector.py")

except (json.JSONDecodeError, ValueError) as e:
    print(f"❌ Error parsing similarity data: {e}", file=sys.stderr)
    sys.exit(1)
EOF
```
