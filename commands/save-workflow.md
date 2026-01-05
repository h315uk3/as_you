---
description: "Save a sequence of recent work as a reusable slash command"
argument-hint: "<workflow-name>"
allowed-tools: [Task, Write, Read]
---

# Save Workflow

Save a sequence of recent work as a reusable slash command.

## Process

1. **Analyze Recent Work**
   - Review the last 10-20 tool uses (Bash, Edit, Write, Read, etc.)
   - Extract patterns from executed commands and file operations
   - Organize into repeatable steps

2. **Gather Requirements**
   Ask the user:
   - **Command name**: Name for the slash command (e.g., `update-docs`, `qa-check`)
   - **Description**: Purpose of this workflow (1-2 sentences)
   - **Abstraction level**:
     - `specific`: Save exact file paths and commands as-is
     - `generic`: Generalize patterns (e.g., `*.rs` → "Rust files", specific dir → "project root")
   - **Scope**: All recent work or select specific steps (present options)

3. **Generate Slash Command**
   Save as `commands/{command-name}.md`:
   ```markdown
   <!-- Description -->

   Execute the following steps:

   1. [Step 1 description]
      - Specific operations
      - Tool usage if needed

   2. [Step 2 description]
      ...

   If errors occur, report details and confirm before proceeding to next step.
   ```

4. **Confirmation**
   Present the generated command to the user and ask if modifications are needed

5. **Session Restart Required**
   After successfully saving the command, output the following message:
   ```
   ✅ Saved new command: /{command-name}

   ⚠️  To use this command, you must restart the session:
   - Type `/exit` and press Enter
   - Then resume the session or start a new one

   The new command will be available after restart.
   ```

## Example Output

Recent work:
- Ran formatter command
- Ran linter command
- Ran test suite

↓ After saving

`commands/qa-check.md`:
```markdown
Run quality checks on the current project.

1. Identify project type and verify project structure
2. Run formatter according to project conventions
3. Run linter with strict settings
4. Execute test suite
5. Report results (details if errors, success message otherwise)
```

Usage: `/qa-check`

## Important Notes

- Do NOT save workflows containing sensitive data (API keys, passwords, etc.)
- For destructive operations (delete, force push, etc.), include explicit warnings
- For steps requiring user input, recommend using `AskUserQuestion` tool
