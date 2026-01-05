---
description: "Update an existing slash command with recent work or modifications"
argument-hint: "[command-name]"
allowed-tools: [Read, Write, AskUserQuestion, Glob]
---

# Update Workflow

Update an existing slash command with recent work or modifications.

## Process

1. **List Existing Commands**
   - Scan `commands/*.md` for available slash commands
   - Display command names and their descriptions
   - Ask user which command to update

2. **Read Current Command**
   - Load the selected command file
   - Display current workflow steps
   - Analyze structure and patterns

3. **Analyze Recent Work**
   - Review the last 10-20 tool uses (Bash, Edit, Write, Read, etc.)
   - Extract patterns from executed commands and file operations
   - Identify steps that could enhance the existing workflow

4. **Update Options**
   Ask the user how to update:
   - **Append**: Add new steps at the end
   - **Prepend**: Add new steps at the beginning
   - **Replace**: Replace specific step(s) with new work
   - **Merge**: Intelligently merge new patterns into existing steps
   - **Refine**: Keep the same workflow but improve descriptions/parameters

5. **Preview Changes**
   - Show side-by-side comparison:
     - Left: Current command
     - Right: Updated command
   - Highlight differences

6. **Confirmation**
   - Ask user to approve changes
   - If approved, save to `commands/{command-name}.md`
   - If rejected, ask for modifications or cancel

7. **Session Restart Required**
   After successfully updating the command, output the following message:
   ```
   ✅ Updated command: /{command-name}

   ⚠️  To use the updated command, you must restart the session:
   - Type `/exit` and press Enter
   - Then resume the session or start a new one

   The updated command will be available after restart.
   ```

## Example Usage

**Scenario**: You have `/qa-check` that runs formatter and linter, but you want to add test execution and build verification.

```
/update-workflow
```

**Output**:
```
Available commands:
1. qa-check - Run quality checks on the current project
2. save-workflow - Save recent work as a slash command
3. update-workflow - Update an existing slash command

Which command to update? > 1

Current workflow in qa-check:
1. Identify project type and verify project structure
2. Run formatter according to project conventions
3. Run linter with strict settings

Recent work detected:
- Executed test suite
- Ran build process

How to update?
1. Append - Add test & build steps at the end
2. Prepend - Add before formatting
3. Replace - Replace specific step
4. Merge - Intelligently integrate
5. Cancel

> 1

Preview:
──────────────────────────────────────────────
BEFORE                      AFTER
──────────────────────────────────────────────
1. Identify project         1. Identify project
2. Run formatter            2. Run formatter
3. Run linter               3. Run linter
                            4. Execute test suite
                            5. Run build process
──────────────────────────────────────────────

Apply changes? (y/n) > y

✅ Updated /qa-check
```

## Advanced Features

### Pattern Recognition
- Detect similar operations and suggest consolidation
- Identify redundant steps
- Suggest parallel execution where possible

### Smart Merging
- If new work overlaps with existing steps, suggest improvements
- Example: "Step 3 already runs linter, but recent work adds stricter flags. Update step 3 with new parameters?"

### Version Control
- Before updating, create backup as `commands/.backup/{command-name}.{timestamp}.md`
- Allow rollback with `/restore-workflow`

## Important Notes

- Always preview changes before applying
- Backup original command automatically
- Preserve comments and documentation in the command file
- Maintain consistent formatting and style
