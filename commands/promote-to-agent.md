---
description: "Promote frequent task pattern to agent"
allowed-tools: [Bash, Read, Task, AskUserQuestion, Write]
---

# Promote Pattern to Agent

Analyze frequent task patterns and promote them to knowledge base (Agent).

## Execution Steps

### 1. Retrieve Agent Candidates

Retrieve promotion candidates using Bash tool:

```bash
./scripts/suggest-promotions.sh | jq '[.[] | select(.type == "agent")]'
```

If 0 candidates:
- Respond: "No agent promotion candidates currently available"
- Check if Skill candidates exist and suggest `/as-you:promote-to-skill`

### 2. Candidate Selection

Present candidates using AskUserQuestion tool:
- Display each candidate's pattern, composite_score (percentage format), count, sessions, reason
- Display format: `{pattern} [{score}%] - {reason}` (e.g., `deployment [100%] - High score: TF-IDF=58.22, Recently used`)
- Let user select
- Options: List of candidate pattern names (with scores) + "Cancel"

### 3. Agent Generation

For selected pattern:

1. Organize context information:
   ```bash
   jq -r '.patterns["selected_pattern"].contexts[]' .claude/as_you/pattern_tracker.json
   ```

2. Infer required tools from task pattern:
   - "analyze", "review" → Read, Grep, Bash
   - "generate", "create" → Write, Read
   - "test", "validate" → Bash, Read
   - "build", "deploy" → Bash

3. Generate draft using plugin-dev:agent-development skill:
   - Include pattern name, context, inferred tools in prompt
   - Present generated Agent to user

4. User confirmation:
   - Use AskUserQuestion: "Create this Agent?"
   - Options: "Create", "Modify and create", "Cancel"

5. Execute creation:
   - If "Create": Create `agents/{suggested_name}.md`
   - If "Modify and create": Ask user for modifications then create

6. Update pattern_tracker.json:
   ```bash
   # Mark promotion status (also record promoted_to, promoted_at, promoted_path)
   ./scripts/mark-promoted.sh "selected_pattern" agent "agents/{agent-name}.md"
   ```

### 4. Completion Report

```markdown
✅ Agent created: {agent-name}

File: agents/{agent-name}.md
The agent will automatically activate when this task is needed.

Related commands:
- /as-you:memory-stats - View statistics
- /as-you:promote-to-agent - Promote other patterns
```

## Notes

- Check for duplicates with existing Agents (search `agents/*.md` using Glob tool)
- frontmatter description must be specific (for autonomous agent invocation)
- Specify minimum required tools (don't include unnecessary tools)
- color is optional (blue, green, purple, orange, etc.)
