---
description: Display pattern composite scores and rankings
allowed-tools: [Bash]
---

Display pattern scoring results.

Shows top 20 promotion candidates (composite_score > 0.3) with detailed scores (TF-IDF, freshness, session spread) and promotion reasons for each pattern.

Execution:
1. Read promotion_candidates from pattern_tracker.json
2. Format scores for readability
3. Display with promotion reasons

Example output:
```
[100%] deployment
  Occurrences: 84 times, Sessions: 2
  TF-IDF: 58.2
  Reason: High score: TF-IDF=58.22, Recently used

[85%] testing
  Occurrences: 129 times, Sessions: 3
  TF-IDF: 42.1
  Reason: High frequency pattern, Cross-session
```

```bash
if [ ! -f .claude/as_you/pattern_tracker.json ]; then
  echo "❌ pattern_tracker.json not found"
  echo "   Please end the session to execute pattern tracking first"
  exit 1
fi

python3 <<'EOF'
import json
import sys

try:
    with open('.claude/as_you/pattern_tracker.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    candidates = data.get('promotion_candidates', [])

    if len(candidates) == 0:
        print("📊 No promotion candidates currently")
        print("   Continue sessions until patterns are detected")
        sys.exit(0)

    print(f"📊 Top Promotion Candidates (Top {len(candidates)})")
    print("")

    # Show top 20 candidates
    for candidate in candidates[:20]:
        score_pct = int(candidate.get('composite_score', 0) * 100)
        pattern = candidate.get('pattern', '')
        count = candidate.get('count', 0)
        sessions = candidate.get('sessions', 0)
        tfidf = round(candidate.get('tfidf', 0), 1)
        reason = candidate.get('reason', '')

        print(f"[{score_pct}%] {pattern}")
        print(f"  Occurrences: {count} times, Sessions: {sessions}")
        print(f"  TF-IDF: {tfidf}")
        print(f"  Reason: {reason}")
        print("")

    print("💡 Promotion commands:")
    print("   /as-you:promote-to-skill  - Promote as Skill")
    print("   /as-you:promote-to-agent  - Promote as Agent")

except (json.JSONDecodeError, IOError) as e:
    print(f"❌ Error reading pattern_tracker.json: {e}", file=sys.stderr)
    sys.exit(1)
EOF
```
