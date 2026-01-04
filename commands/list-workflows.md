---
description: "List all saved workflows sorted by last modified date"
allowed-tools: [Glob, Bash]
---

# List Workflows

Display all saved workflows sorted by last modified date (newest first).

## Execution Steps

1. Execute the following command with Bash tool to retrieve workflows:
   ```bash
   ls -lt commands/*.md 2>/dev/null | grep -v -E 'commands/(example-command|memo|save-workflow|update-workflow|list-workflows|show-workflow|delete-workflow|help|memory-stats|memory-analyze|create-skill|create-agent|README)' | grep -v 'commands/memo-' | awk '{print $9, $6, $7, $8}' | sed 's|commands/||' | sed 's|\.md||'
   ```

2. If no results:
   - Respond: "No saved workflows found"
   - Guide: Can create new ones with `/as-you:save-workflow "name"`

3. If results exist:
   - Display in table format:
     ```
     | Workflow Name | Last Updated |
     |--------------|--------------|
     | workflow1    | 2026-01-03   |
     | workflow2    | 2026-01-02   |
     ```
   - Display at the end: "Total: X workflows"

## Related Commands
- `/as-you:show-workflow "name"` - Show details
- `/as-you:save-workflow "name"` - Create new
- `/as-you:update-workflow "name"` - Update existing
- `/as-you:delete-workflow "name"` - Delete
