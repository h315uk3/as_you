---
description: "Clear current session memos"
allowed-tools: [Bash]
---

# Clear Session Notes

Clear current session notes.

## Execution Steps

1. Execute the following command with Bash tool:
   ```bash
   > .claude/as-you/session-notes.local.md
   ```
2. Respond: "Session notes cleared"

## Notes
- File is not deleted, only content is cleared
- Notes are automatically archived on session end
- Archived notes are not affected
- Past notes can be viewed with `/as-you:note-history`

## Related Commands
- `/as-you:note "content"` - Add note
- `/as-you:note-show` - Display notes
- `/as-you:note-history` - View past notes
