# As You

**Yet Another Claude Code Memory Mechanism.**

A Claude Code plugin that extracts and accumulates patterns from your session notes, automatically building a personalized knowledge base.

## Features

- **NO Auth / NO Backend / NO Connection** - Completely local execution
- **Pattern Extraction & Accumulation** - Automatically extract frequently-appearing patterns from manual notes and make them reusable
- **Statistical Scoring** - TF-IDF, PMI, and time-decay-based importance evaluation
- **Automatic Pattern Merging** - Automatically merge similar patterns using Levenshtein distance
- **Language-Agnostic** - Implemented using only bash/awk/jq/bc (no NLP libraries)

## How It Works

### Automatic Extraction Flow: From Session Notes to Knowledge Base

```
1. During Session
   /as-you:note "Investigating authentication feature bug"
   → Saved to .claude/as-you/session-notes.local.md

2. On SessionEnd (Automatic)
   → Archive session-notes.local.md
   → Save as .claude/as-you/session-archive/2026-01-04.md

3. Pattern Extraction & Scoring (Automatic)
   → Extract words from archive
   → Calculate TF-IDF, PMI, time-decay scores
   → Auto-merge similar patterns (Levenshtein distance)
   → Save to .claude/as-you/pattern-tracker.json

4. Promotion Notification (Automatic)
   → Display patterns with composite score > 0.3 as promotion candidates
   → Viewable with /as-you:show-scores

5. Knowledge Base Creation (Manual)
   → /as-you:promote-to-skill to create Skill
   → /as-you:promote-to-agent to create Agent
   → Save to skills/*, agents/*
   → Agents automatically leverage them
```

Patterns are automatically extracted from your session notes, and frequently-appearing patterns accumulate as your knowledge base.

## Installation

### Method 1: Via Marketplace (Recommended)

Run the following commands in Claude Code:

```bash
# Add marketplace (first time only)
/plugin marketplace add h315uk3/as_you

# Install plugin
/plugin install as-you@h315uk3-as_you
```

Or use the interactive UI:

1. Run `/plugin`
2. Select the **Discover** tab
3. Select **as-you** and press **Enter**
4. Choose installation scope:
   - **User**: Available across all projects
   - **Project**: Only for this project (saved in `.claude/settings.json`)
   - **Local**: Only for this repository (not shared)

### Method 2: Direct Clone from GitHub (For Developers)

```bash
# Clone into plugins directory
git clone https://github.com/h315uk3/as_you.git ~/.claude/plugins/as_you

# Or clone to any directory
git clone https://github.com/h315uk3/as_you.git /path/to/as_you
claude --plugin-dir /path/to/as_you
```

### Requirements

- **Claude Code CLI**: https://claude.com/claude-code
- **jq**: JSON processing
- **bc**: Mathematical calculations (logarithms and exponential functions)
- **awk**: Text processing (usually pre-installed)

```bash
# Install dependencies (if needed)
# Ubuntu/Debian
sudo apt-get install jq bc

# macOS
brew install jq bc

# awk is usually pre-installed
```

Optional (for developers):
- mise: Task runner (https://mise.jdx.dev/)

### Verification

```bash
# Check if plugin is installed
/plugin

# Try As You commands
/as-you:note "Test note"
/as-you:note-show
```

## Usage

### Session Notes

Record your work. What you write becomes the raw data for pattern extraction.

```bash
/as-you:note "Investigating authentication feature bug"
/as-you:note-show          # View current note
/as-you:note-history       # View past 7 days
```

#### Why Manual Input?

Reasons for manual input rather than automatic recording:

- Intentional data selection
- Privacy control
- High-quality data accumulation
- Simple, lightweight implementation

#### Effective Note Writing

Good examples (specific keywords):
```bash
/as-you:note "Fixed deployment pipeline CI/CD configuration"
/as-you:note "Updated testing framework setup"
/as-you:note "Implemented JWT token validation in authentication"
```

Examples to avoid (too abstract/generic):
```bash
/as-you:note "Working"                     # ✗ Unclear what work
/as-you:note "Fixed a bug"                 # ✗ What bug?
/as-you:note "Did various things"          # ✗ No specificity
```

Tips:
- Include technical keywords (deployment, testing, authentication, etc.)
- Specify component or feature names
- Use consistent terminology for repeated work (improves pattern detection)

### Workflows

Save and reuse repeated work as slash commands.

```bash
/as-you:save-workflow "deploy-staging"   # Save recent work
/as-you:list-workflows                    # List all
/as-you:show-workflow "deploy-staging"    # View details
/deploy-staging                           # Execute saved workflow
```

#### How Workflows Work

1. Perform work
   - Code editing, test execution, deployment, etc.

2. Save workflow
   ```bash
   /as-you:save-workflow "deploy-staging"
   ```
   - Analyze last 10-20 tool use history
   - Organize into repeatable steps
   - Save as `commands/deploy-staging.md`

3. Reuse
   ```bash
   /deploy-staging
   ```
   - Execute saved workflow as a slash command
   - Reproduce same work multiple times

Use cases:
- Deployment procedures
- Test execution patterns
- Code generation routines
- Documentation update flows

### Knowledge Base Creation

Auto-detect frequent patterns and convert them to Skills/Agents.

```bash
/as-you:show-scores             # View scoring results
/as-you:promote-to-skill        # Promote to Skill
/as-you:promote-to-agent        # Promote to Agent
/as-you:detect-similar-patterns # Detect similar patterns
```

#### How Knowledge Base Creation Works

1. Auto-extract patterns (on SessionEnd)
   - Extract words from archived session notes
   - Score with TF-IDF, PMI, time-decay
   - Auto-merge similar patterns
   - Mark patterns with composite score > 0.3 as promotion candidates

2. Review promotion candidates
   ```bash
   /as-you:show-scores
   ```
   Display scoring ranking in percentage format

3. Convert to Skill/Agent (Manual)
   ```bash
   /as-you:promote-to-skill    # Convert knowledge/concepts to Skill
   /as-you:promote-to-agent    # Convert tasks/processes to Agent
   ```
   Select pattern, generate draft, save to `skills/` or `agents/`

4. Automatic leverage by agents
   - Agents automatically invoke saved Skills/Agents
   - Reuse past knowledge

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

```bash
mise run test      # Run tests
mise run lint      # Validate code
mise run validate  # Validate plugin
```

## License

MIT License - [LICENSE](LICENSE)

## Related Resources

- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [MCP Specification](https://modelcontextprotocol.io/)
