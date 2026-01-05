---
description: "Add note to current session memory with timestamp"
argument-hint: "<memo-content>"
allowed-tools: [Bash]
---

# Add Session Note

If $ARGUMENTS is empty, display help:

## Usage
```
/as-you:note "note content"
```

## Examples
```
/as-you:note "Investigating User.findById() returning null issue"
/as-you:note "JWT verification error - secret key not set in environment variables"
/as-you:note "Implementing Phase 5: Scripts done, next is Hooks"
```

## Features
- Recorded with timestamp
- Automatically archived on session end
- Frequent patterns suggested for knowledge base creation

## Related Commands
- `/as-you:note-show` - Display current session notes
- `/as-you:note-history` - View notes from last 7 days
- `/as-you:memory-analyze` - Analyze patterns

---

If $ARGUMENTS is provided, execute the following:

1. Execute with Bash tool:
   ```bash
   mkdir -p .claude/as-you
   echo "[$(date +%H:%M)] $ARGUMENTS" >> .claude/as_you/session_notes.local.md
   ```
2. Respond: "Note added"
