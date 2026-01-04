# Development Guide

This guide explains how to develop and extend the As You plugin.

## Development Environment Setup

### Prerequisites

- Git
- [mise](https://mise.jdx.dev/) - Tool version management and task runner

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/h315uk3/as_you.git
cd as_you

# Install mise (if not already installed)
curl https://mise.run | sh

# Install all dependencies
mise install
```

`mise install` installs the following (defined in `mise.toml`):
- **bats** (1.13.0) - Bash test framework
- **jq** (1.8.1) - JSON processing
- **shellcheck** (0.11.0) - Shell script linter
- **shfmt** (3.12.0) - Shell script formatter
- **rust** (1.92.0) - For MCP development (optional)

### Project Structure

```
as_you/
├── .claude-plugin/plugin.json  # Plugin manifest
├── commands/                    # Slash commands (20 total)
├── agents/                      # Custom agents
├── skills/                      # Agent Skills
├── hooks/                       # Event hooks
│   ├── hooks.json
│   ├── session-start.sh
│   ├── session-end.sh
│   └── post-edit-format.sh
├── scripts/                     # Pattern extraction & scoring scripts (16 total)
├── tests/                       # bats test suite
│   ├── unit/
│   ├── integration/
│   └── validation/
├── LICENSE                      # MIT License
└── mise.toml                    # Task and tool definitions
```

## Development Tasks

```bash
# Testing
mise run test              # Run all tests
mise run test:unit         # Run unit tests
mise run test:integration  # Run integration tests
mise run test:validation   # Run validation tests
mise run test:watch        # Watch mode

# Code quality
mise run lint              # Run shellcheck linter
mise run format            # Format with shfmt
mise run validate          # Validate plugin (includes JSON validation)

# Scoring debug execution
mise run scoring:tfidf     # Calculate TF-IDF
mise run scoring:pmi       # Calculate PMI
mise run scoring:decay     # Calculate time decay
mise run scoring:composite # Calculate composite score batch
```

## Extension Methods

### Adding Slash Commands

Create a Markdown file in the `commands/` directory. The filename (without extension) becomes the command name.

**Filename**: `commands/my-command.md`

```markdown
---
description: Command description (one line)
---

Instructions for the agent.
Use $ARGUMENTS to reference user input.
```

### Adding Skills

Create a `skills/my-skill/` directory and place `SKILL.md` inside.

```markdown
---
name: my-skill
description: Clear description so agents can autonomously invoke it
---

Detailed skill description.
```

Recommended directory structure:
- `reference/` - Reference materials
- `examples/` - Sample code

### Adding Agents

Create a Markdown file in the `agents/` directory. Define behavior in frontmatter.

### Adding Hooks

Edit `hooks/hooks.json`. Currently implemented hooks:
- **SessionStart** → `session-start.sh`
- **SessionEnd** → `session-end.sh` (runs pattern extraction)
- **PostToolUse (Edit)** → `post-edit-format.sh`

Available events:
- `SessionStart` / `SessionEnd`
- `PreToolUse` / `PostToolUse`
- `SubagentStop`
- `UserPromptSubmit`

### Adding Scripts

Create bash scripts in `scripts/`. Grant execution permission.

```bash
chmod +x scripts/my-script.sh
```

**Constraints**:
- Dependencies: bash/awk/jq/bc only (no external libraries)
- JSON processing must use jq
- Error handling required

## Testing

### Adding Tests

Use bats-core framework.

**Example**: `tests/unit/my-test.bats`

```bash
#!/usr/bin/env bats

@test "test description" {
  run bash scripts/my-script.sh
  [ "$status" -eq 0 ]
  [[ "$output" == *"expected"* ]]
}
```

### Existing Test Files

- `tests/unit/scripts.bats` - Script unit tests
- `tests/unit/hooks.bats` - Hook unit tests
- `tests/integration/workflow.bats` - Integration tests
- `tests/validation/frontmatter.bats` - Frontmatter validation
- `tests/validation/json-schema.bats` - JSON validation

## Development Guidelines

### Prohibitions

1. **No Guessing** - Always refer to official documentation or actual code
2. **No Unresolved Issues** - Identify root cause before fixing
3. **No Legacy Code** - Follow latest best practices
4. **No Unreviable Changes** - Keep changes at a human-verifiable granularity

### Coding Standards

- Must pass shellcheck
- Must be formatted with shfmt
- JSON processing must use jq
- Proper error handling required

## CI/CD

GitHub Actions (`.github/workflows/test.yml`) runs automatic tests on:
- Push (main branch)
- Pull requests (to main)

Execution flow:
1. Install dependencies with mise
2. Run `mise run lint`
3. Run `mise run test`
4. Run `mise run validate`

## Architecture

### Pattern Extraction Flow

```
Session Notes (.claude/as-you/session-notes.local.md)
  ↓ Automatically run on SessionEnd
Archive (.claude/as-you/session-archive/YYYY-MM-DD.md)
  ↓ Extract patterns and score
Pattern Tracker (.claude/as-you/pattern-tracker.json)
  ↓ Auto-detect promotion candidates
Knowledge Base (skills/*/SKILL.md, agents/*.md)
```

Workflows are a separate system: saved as `commands/` for repeated work.

### SessionEnd Processing

`hooks/session-end.sh` executes the following in sequence:

1. `archive-note.sh` - Archive session notes
2. `track-frequency.sh` - Extract patterns and score
   - `detect-patterns.sh` - Extract words
   - `extract-contexts.sh` - Record surrounding context (1 line before/after)
   - `detect-cooccurrence.sh` - Detect word co-occurrence patterns
   - `calculate-tfidf.sh` - Calculate TF-IDF
   - `calculate-pmi.sh` - Calculate PMI
   - `calculate-time-decay.sh` - Calculate time decay
   - `calculate-composite-score.sh` - Calculate composite score
3. `merge-similar-patterns.sh` - Auto-merge similar patterns (Levenshtein distance ≤ 2)

### Scoring Methods

- **TF-IDF**: Word frequency × inverse document frequency
- **PMI**: Mutual information of word co-occurrence (log(P(A,B) / (P(A) × P(B))))
- **Time Decay**: Exponential decay (λ=0.1, 37% after 10 days)
- **Composite Score**: TF-IDF 40% + Freshness 30% + Session Spread 30%
- **Similarity**: Levenshtein distance (edit distance)

**Implementation Features**:
- No NLP libraries (bash/awk/jq/bc only)
- Basic statistics and string processing
- Simple, understandable logic

For details: See plugin documentation

## Plugin Distribution

### GitHub Marketplace

Repository already supports marketplace installation:

```bash
/plugin marketplace add h315uk3/as_you
/plugin install as-you@h315uk3-as_you
```

### Official Marketplace Registration

Submit PR to [claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

Review criteria:
- Security
- Code quality
- Documentation completeness
- User value

## Related Resources

- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [rmcp SDK (Rust)](https://docs.rs/rmcp/)

## License

MIT License - [LICENSE](LICENSE)
