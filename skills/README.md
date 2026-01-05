# As You Plugin - Skills

This directory contains skills that extend Claude's capabilities when working with this plugin.

## Core Skills

*(Currently no core skills - patterns are promoted to skills dynamically)*

## Optional Skills

### mcp-builder-rust

**Purpose**: Comprehensive guide for creating production-grade MCP (Model Context Protocol) servers in Rust.

**Size**: ~264KB, 21 files

**When to use**: Building MCP servers with type safety, performance, and async support.

**Optional**: This skill is not required for the core pattern learning functionality of the as-you plugin. You can safely remove this directory if you don't plan to build Rust-based MCP servers.

**To remove**:
```bash
rm -rf skills/mcp-builder-rust
```

## Adding Custom Skills

Skills are automatically discovered by Claude Code. To add a custom skill:

1. Create a directory: `skills/your-skill-name/`
2. Add a `SKILL.md` file with frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: Clear description for automatic invocation
   ---

   # Your Skill Content
   ```

3. Add supporting files in subdirectories:
   - `reference/` - Reference documentation
   - `examples/` - Code examples
   - `templates/` - Templates

## Skill Best Practices

- **Name**: Use kebab-case for skill directory names
- **Description**: Write clear descriptions so agents can invoke skills autonomously
- **Size**: Keep skills focused and under 500 lines per file
- **Structure**: Use subdirectories to organize large skills
- **License**: Include license information in frontmatter if distributing

## Promoted Skills

Skills promoted from patterns via `/as-you:promote-to-skill` will be created in this directory with the pattern's name and accumulated knowledge.
