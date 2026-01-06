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
    python3 scripts/usage_stats_initializer.py
fi
```

### 2. Check Current Status and Detect Unused Knowledge Base

```bash
python3 <<'EOF'
import json
from datetime import datetime, timedelta

try:
    with open('.claude/skill-usage-stats.json', 'r') as f:
        data = json.load(f)

    skills = data.get('skills', {})
    agents = data.get('agents', {})
    last_updated = data.get('last_updated', 'N/A')

    print(f"Skill count: {len(skills)}")
    print(f"Agent count: {len(agents)}")
    print(f"Last updated: {last_updated}")
    print("")

    # Detect unused knowledge base (30 days threshold)
    threshold = datetime.now() - timedelta(days=30)

    unused_skills = []
    for name, info in skills.items():
        last_used = info.get('last_used')
        if last_used is None:
            unused_skills.append(name)
        else:
            try:
                last_used_dt = datetime.fromisoformat(last_used)
                if last_used_dt < threshold:
                    unused_skills.append(name)
            except ValueError:
                unused_skills.append(name)

    unused_agents = []
    for name, info in agents.items():
        last_used = info.get('last_used')
        if last_used is None:
            unused_agents.append(name)
        else:
            try:
                last_used_dt = datetime.fromisoformat(last_used)
                if last_used_dt < threshold:
                    unused_agents.append(name)
            except ValueError:
                unused_agents.append(name)

    if unused_skills:
        print("Unused skills (30+ days):")
        for skill in unused_skills:
            print(f"  - {skill}")
        print("")

    if unused_agents:
        print("Unused agents (30+ days):")
        for agent in unused_agents:
            print(f"  - {agent}")
        print("")

    if not unused_skills and not unused_agents:
        print("✓ All knowledge base items are actively used")

except (json.JSONDecodeError, IOError) as e:
    print(f"❌ Error reading stats: {e}")
EOF
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
