---
description: "Display workflow details"
argument-hint: "<workflow-name>"
allowed-tools: [Read]
---

# Show Workflow Details

Display details of specified workflow.

If $ARGUMENTS is empty, display help:

## Usage
```
/as-you:show-workflow "workflow-name"
```

## Examples
```
/as-you:show-workflow "deploy-staging"
/as-you:show-workflow "run-tests"
```

---

If $ARGUMENTS is provided:

1. Remove extension from workflow name (if .md exists)
2. Read `commands/{workflow-name}.md` using Read tool
3. If file doesn't exist:
   - Respond: "Workflow '{name}' not found"
   - Guide: Check list with `/as-you:list-workflows`
4. If file exists:
   - Display file contents as-is
   - Add metadata at the end:
     - File path
     - Last modified date (if available)

## Related Commands
- `/as-you:list-workflows` - List all
- `/as-you:update-workflow "name"` - Update
- `/as-you:delete-workflow "name"` - Delete
