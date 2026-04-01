# Symbiosis - Copilot Instructions

Instructions for GitHub Copilot code completion.

Path-specific standards are defined in `.github/instructions/*.instructions.md` — this file covers project-wide context.

---

## Project Context

Symbiosis is a local-first, privacy-by-design Human-AI development tool suite. Two Claude Code plugins:

- **as-you**: Pattern learning via BM25 scoring, Thompson sampling, SM-2 spaced repetition
- **with-me**: Bayesian requirement elicitation via belief tracking and Thompson sampling

### Hard Constraints

- Python 3.11+ standard library only — no external packages, no exceptions
- All processing local — no network calls, no external services, no telemetry
- File-based persistence — JSON and Markdown, human-readable
- CI enforces: `ruff` lint, `pyright` type check, doctests, plugin validation

### Infrastructure

- `.monitoring/` — Local-only Docker dev tooling (OTEL Collector, Prometheus, Loki, Grafana). Not production infrastructure. Ephemeral, user-controlled, `:latest` tags are intentional.
- Shell scripts — Minimal glue code under 10 lines delegating to Python. `set -euo pipefail` provides sufficient error handling for local dev scripts.

---

## Code Completion Context

### Python modules (`plugins/**/lib/*.py`)

- Pure functions with type hints and doctests
- Algorithms: BM25, Thompson sampling, SM-2, Bayesian updating
- Use `math`, `json`, `pathlib`, `datetime`, `re`, `difflib` from stdlib
- Doctest isolation: use `tempfile.mkdtemp()` for file operations

### Commands/Agents (`commands/*.md`, `agents/*.md`)

- Markdown with YAML frontmatter (`description`, `allowed-tools`)
- Thin entry points delegating logic to `lib/` modules

### Monitoring configs (`.monitoring/`)

- Docker Compose, OTEL Collector YAML, Prometheus YAML, Loki YAML, Grafana JSON
- PromQL for Prometheus queries, LogQL for Loki queries
- LogQL supports both `"double quotes"` and `` `backticks` `` for string literals

### Shell scripts (`.monitoring/*.sh`)

- Bash with `set -euo pipefail`
- Under 10 lines of logic, delegates to Python or Docker

---

## Build & Test

Prerequisite: [mise](https://mise.jdx.dev/) manages Python and all tool versions.

```bash
mise run test            # All doctests
mise run lint            # ruff check
mise run typecheck       # pyright
mise run validate        # Plugin config validation
```

CI requires all four checks to pass.
