---
description: "Review and maintain skills/agents based on usage patterns"
allowed-tools: [Bash, Read, Glob, AskUserQuestion]
---

# Knowledge Base Review and Maintenance

Review Skills/Agents status based on usage statistics and suggest maintenance.

## Execution Steps

### 1. Initialize Usage Statistics

Check if statistics file exists, initialize if not:

```bash
if [ ! -f .claude/skill-usage-stats.json ]; then
    ./scripts/init-usage-stats.sh
fi
```

### 2. Check Current Status

```bash
# Number of Skills
jq '.skills | length' .claude/skill-usage-stats.json

# Number of Agents
jq '.agents | length' .claude/skill-usage-stats.json

# Last updated
jq -r '.last_updated' .claude/skill-usage-stats.json
```

### 3. Detect Unused Knowledge Base

#### Skills Unused for 30 Days

```bash
jq -r '.skills | to_entries | .[] |
    select(
        (.value.last_used == null or
         (.value.last_used | fromdateiso8601) < (now - 2592000))  # 30 days
    ) |
    .key' .claude/skill-usage-stats.json
```

#### Agents Unused for 30 Days

```bash
jq -r '.agents | to_entries | .[] |
    select(
        (.value.last_used == null or
         (.value.last_used | fromdateiso8601) < (now - 2592000))
    ) |
    .key' .claude/skill-usage-stats.json
```

### 4. Create Review Report

Report in the following format:

```markdown
# Knowledge Base Review

## Current Status

- **Skills**: {skill_count}
- **Agents**: {agent_count}
- **Last Updated**: {last_updated}

## Maintenance Suggestions

### Unused Knowledge Base ({count})

#### Skills
- `{skill-name}` - Created: {created}, Invocations: {invocations}

#### Agents
- `{agent-name}` - Created: {created}, Invocations: {invocations}

### Recommended Actions

1. **Archive**: Move long-unused Skills/Agents to `.claude/archived/`
2. **Consolidate**: Merge Skills/Agents with similar functionality
3. **Update**: Improve frequently-used but outdated implementations

---

Automatic usage frequency tracking is not yet implemented.
Manual evaluation of Skill/Agent usefulness and removal of unnecessary ones is recommended.
```

### 5. User Confirmation (Optional)

If 5+ unused knowledge base items exist, confirm using AskUserQuestion:
- "Archive unused Skills/Agents?"
- Options: "Yes", "Review individually", "No"

If "Yes":
```bash
mkdir -p .claude/archived/skills
mkdir -p .claude/archived/agents

# Move unused Skills
for skill in {list}; do
    mv "skills/$skill" ".claude/archived/skills/"
done
```

## Notes

- **Important**: Do not delete system agents (memory-analyzer, component-generator, promotion-reviewer)
- Archived Skills/Agents can be restored later
- Always confirm with user before permanent deletion

## Future Implementation Plans

- Automatic tracking of Skill/Agent usage
- Effectiveness measurement (effectiveness evaluation)
- Usage pattern analysis
