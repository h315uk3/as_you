---
description: "Display As You plugin help and usage guide"
allowed-tools: []
---

# As You Plugin Help

**External Memory Plugin that Becomes More Personalized the More You Use It**

---

## Types of Memory

### 📝 Session Memos
Temporary memos valid only during the current session

**Commands**:
- `/as-you:note "content"` - Add memo (with timestamp)
- `/as-you:note-show` - Display current memos
- `/as-you:note-clear` - Clear memos
- `/as-you:note-history` - Display history for the past 7 days

**Features**:
- Automatically archived on session end
- Cleared on next session start
- Frequent patterns automatically detected

---

### 🔄 Workflows
Save repeatedly executed work procedures

**Commands**:
- `/as-you:save-workflow "name"` - Save new workflow
- `/as-you:update-workflow "name"` - Update existing workflow
- `/as-you:list-workflows` - List all (sorted by last update)
- `/as-you:show-workflow "name"` - Show details
- `/as-you:delete-workflow "name"` - Delete (with confirmation)

**Use Cases**: Deployment procedures, test execution, routine tasks, etc.

---

### 🧠 Knowledge Base (Skills & Agents)
Specialized knowledge automatically generated from frequent patterns

**Analysis & Promotion**:
- `/as-you:memory-analyze` - Analyze patterns and suggest knowledge base creation
- `/as-you:promote-to-skill` - Promote frequent pattern to Skill
- `/as-you:promote-to-agent` - Promote frequent task to Agent

**Manual Creation**:
- `/as-you:create-skill "name"` - Create skill (AI-assisted/manual)
- `/as-you:create-agent "name"` - Create agent (AI-assisted/manual)

**Maintenance**:
- `/as-you:review-long-term-memory` - Suggest maintenance based on usage statistics

**Automation**:
- Pattern appears in 3+ sessions or 5+ total occurrences
- Automatic notification via SessionStart hook
- Interactive knowledge base creation suggestions

---

## Statistics

- `/as-you:memory-stats` - Display memory usage statistics

---

## Quick Start

### 1. Record Work Memos
```
/as-you:note "Investigating authentication bug"
/as-you:note "User.findById() returning null"
```

### 2. Save Workflows
```
/as-you:save-workflow "deploy-staging"
```

### 3. Analyze Patterns
```
/as-you:memory-analyze
```

---

## Automatic Features

### SessionStart (On Session Start)
- Clear session memos
- Delete archives older than 7 days
- Notify about frequent patterns

### SessionEnd (On Session End)
- Archive session memos (skip if empty)
- Update pattern frequencies

---

## Directory Structure

```
.claude/
├── short-term-memory.local.md  # Current session memos
└── session-archive/             # Archives (7-day retention)
    ├── 2026-01-03.md
    ├── 2026-01-02.md
    └── pattern-tracker.json  # Pattern tracking
```

---

## Design Philosophy

**Fully Local Operation**: No internet connection required, no external APIs

**Personal Optimization**: Adapts to your development style the more you use it

**Progressive Learning**:
1. Record thoughts in session memos
2. Automatically detect frequent patterns
3. Consolidate as knowledge base (Skills/Agents)

---

For details, run each command.
