---
description: "Display memo history from last 7 days"
allowed-tools: [Read, Bash, Glob]
---

# Note History (Last 7 Days)

Display archived notes by date.

## Execution Steps

1. Search `.claude/as_you/session_archive/*.md` using Glob tool
2. If no files found:
   - Respond: "No archived notes found"
3. If files found:
   - Sort each file by date (newest first)
   - For each file:
     - Extract date from filename (YYYY-MM-DD)
     - Display header: "## YYYY-MM-DD"
     - Read and display file content using Read tool
     - Add separator line
4. Display at the end: "Total archives: X"

## Related Commands
- `/as-you:note "content"` - Add note
- `/as-you:note-show` - Display current notes
- `/as-you:memory-analyze` - Analyze patterns
