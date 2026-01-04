---
description: "Delete a saved workflow with confirmation"
argument-hint: "<workflow-name>"
allowed-tools: [Read, Bash]
---

# Delete Workflow

Delete a specified workflow (with confirmation).

If $ARGUMENTS is empty, display help:

## Usage
```
/as-you:delete-workflow "workflow-name"
```

## Examples
```
/as-you:delete-workflow "old-deployment"
```

## Notes
- Confirmation prompt will be displayed before deletion
- Deletion cannot be undone

---

If $ARGUMENTS is provided:

1. Remove extension from workflow name (if .md exists)
2. Check if `commands/{workflow-name}.md` exists
3. If file doesn't exist:
   - Respond: "Workflow '{name}' not found"
4. If file exists:
   - **Use AskUserQuestion tool for confirmation**:
     ```
     Question: "Delete workflow '{name}'?"
     Options:
       - "Yes, delete it"
       - "No, cancel"
     ```
   - If "Yes":
     - Delete using Bash tool: `rm commands/{name}.md`
     - Respond: "Workflow '{name}' deleted"
   - If "No":
     - Respond: "Deletion cancelled"

## Related Commands
- `/as-you:list-workflows` - List all workflows
- `/as-you:show-workflow "name"` - Show workflow details
