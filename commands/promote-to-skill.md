---
description: "Promote frequent pattern to long-term skill"
allowed-tools: [Bash, Read, Task, AskUserQuestion, Write]
---

# Promote Pattern to Skill

Analyze frequent patterns and promote them to knowledge base (Skill).

## Execution Steps

### 1. Retrieve Skill Candidates

Retrieve promotion candidates using Bash tool:

```bash
./scripts/suggest-promotions.sh | jq '[.[] | select(.type == "skill")]'
```

If 0 candidates:
- Respond: "No skill promotion candidates currently available"
- Check if Agent candidates exist and suggest `/as-you:promote-to-agent`

### 2. Candidate Selection

Present candidates using AskUserQuestion tool:
- Display each candidate's pattern, composite_score (percentage format), count, sessions, reason
- Display format: `{pattern} [{score}%] - {reason}` (e.g., `deployment [100%] - High score: TF-IDF=58.22, Recently used`)
- Let user select
- Options: List of candidate pattern names (with scores) + "Cancel"

### 3. Skill Generation

For selected pattern:

1. Organize context information:
   ```bash
   jq -r '.patterns["selected_pattern"].contexts[]' .claude/as_you/pattern_tracker.json
   ```

2. Generate draft using plugin-dev:skill-development skill:
   - Include pattern name, context, description in prompt
   - Present generated Skill to user

3. User confirmation:
   - Use AskUserQuestion: "Create this Skill?"
   - Options: "Create", "Modify and create", "Cancel"

4. Execute creation:
   - If "Create": Create `skills/{suggested_name}/SKILL.md`
   - If "Modify and create": Ask user for modifications then create

5. Update pattern_tracker.json:
   ```bash
   # Mark promotion status (also record promoted_to, promoted_at, promoted_path)
   ./scripts/mark-promoted.sh "selected_pattern" skill "skills/{skill-name}/"
   ```

### 4. Completion Report

```markdown
✅ Skill created: {skill-name}

File: skills/{skill-name}/SKILL.md
Agents can now automatically leverage this skill.

Related commands:
- /as-you:memory-stats - View statistics
- /as-you:promote-to-skill - Promote other patterns
```

## Notes

- Check for duplicates with existing Skills (search `skills/*/SKILL.md` using Glob tool)
- frontmatter description is required (for autonomous agent invocation)
- Recommended to also create reference/ and examples/ directories
