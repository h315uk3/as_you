---
description: "Display current session memos"
allowed-tools: [Read]
---

# Display Current Session Notes

Read and display contents of `.claude/as-you/session-notes.local.md`.

## Execution Steps

1. Read `.claude/as-you/session-notes.local.md` using Read tool
2. If file doesn't exist or is empty:
   - Respond: "No notes in current session"
3. If file exists:
   - Display contents as-is
   - Add at the end: "Total notes: X" (count lines)

## Related Commands
- `/as-you:note "content"` - Add note
- `/as-you:note-clear` - Clear notes
- `/as-you:note-history` - View past notes
