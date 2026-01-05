---
description: "Analyze memory patterns and suggest long-term memory promotion"
allowed-tools: [Read, Task]
---

# Analyze Memory Patterns

Analyze frequent patterns and suggest knowledge base creation (Skills/Agents).

## Execution Steps

1. Read `.claude/as_you/pattern_tracker.json`
2. If file doesn't exist or `promotion_candidates` is empty:
   - Respond: "No knowledge base promotion candidates yet"
   - Guide: "Record memos across multiple sessions to detect frequent patterns"
3. If candidates exist:
   - **Launch memory-analyzer agent using Task tool**:
     ```
     subagent_type: "memory-analyzer"
     prompt: "Analyze pattern_tracker.json and suggest knowledge base promotion candidates"
     description: "Analyze memory patterns"
     ```
   - Display agent analysis results
   - Use AskUserQuestion to confirm knowledge base creation
   - If "Yes", guide to execute `/as-you:create-skill` or `/as-you:create-agent`

## Analysis Criteria

The following patterns are detected as knowledge base promotion candidates:
- Same keyword appears in **3+ sessions**
- Same keyword recorded **5+ times**
- Not yet promoted to knowledge base (`promoted: false`)

## Related Commands
- `/as-you:memory-stats` - Display statistics
- `/as-you:create-skill "name"` - Create skill
- `/as-you:create-agent "name"` - Create agent
- `/as-you:note-history` - View memo history
