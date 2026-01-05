---
description: "Display memory usage statistics"
allowed-tools: [Glob, Bash, Read]
---

# Memory Statistics

Display As You plugin memory usage statistics.

## Execution Steps

Collect and display the following statistics:

### 1. Workflow Statistics
- Count workflow files in `commands/` directory using Bash
  ```bash
  ls commands/*.md | grep -v -E '(example-command|memo|list-workflows|show-workflow|delete-workflow|help|memory-stats|memory-analyze|create-skill|create-agent)\.md' | wc -l
  ```
- Display: "Workflows: X"

### 2. Session Memo Statistics
- Check if `.claude/as_you/session_notes.local.md` exists
- If exists, count lines
- Display: "Current session memos: X entries"

### 3. Archive Statistics
- Search `.claude/as_you/session_archive/*.md` using Glob
- Count files
- Display: "Archives: X days"

### 4. Pattern Detection Statistics
- Check if `.claude/as_you/pattern_tracker.json` exists
- If exists, Read file and display:
  - Detected patterns: number of keys in `.patterns`
  - Knowledge base promotion candidates: length of `.promotion_candidates` array
  - Top 5 patterns (by frequency)

### 5. Knowledge Base Statistics
- Number of skills in `skills/` directory (directories containing SKILL.md)
- Number of agents in `agents/` directory (.md files)

## Display Format Example

```
# As You Memory Statistics

## Workflows
- Workflows: 3

## Session Memos
- Current session memos: 5 entries
- Archives: 7 days

## Pattern Detection
- Detected patterns: 12
- Knowledge base promotion candidates: 2
- Top 5 patterns:
  1. authentication-bug (8 times)
  2. database-connection (6 times)
  3. test-execution (5 times)
  ...

## Knowledge Base (Skills & Agents)
- Skills: 2
- Agents: 4
```

## Related Commands
- `/as-you:memory-analyze` - Analyze patterns
- `/as-you:list-workflows` - List workflows
- `/as-you:note-history` - View memo history
