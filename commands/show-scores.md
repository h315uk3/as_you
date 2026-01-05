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

CANDIDATE_COUNT=$(jq '.promotion_candidates | length' .claude/as_you/pattern_tracker.json 2>/dev/null || echo "0")

if [ "$CANDIDATE_COUNT" -eq 0 ]; then
  echo "📊 No promotion candidates currently"
  echo "   Continue sessions until patterns are detected"
  exit 0
fi

echo "📊 Top Promotion Candidates (Top ${CANDIDATE_COUNT})"
echo ""

jq -r '.promotion_candidates[] |
  "[\(.composite_score | tonumber | . * 100 | floor)%] \(.pattern)
  Occurrences: \(.count) times, Sessions: \(.sessions)
  TF-IDF: \(.tfidf | tonumber | . * 10 | floor / 10)
  Reason: \(.reason)
"' .claude/as_you/pattern_tracker.json | head -20

echo ""
echo "💡 Promotion commands:"
echo "   /as-you:promote-to-skill  - Promote as Skill"
echo "   /as-you:promote-to-agent  - Promote as Agent"
```
