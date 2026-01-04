---
description: "Create a new skill with AI assistance or manual template"
argument-hint: "<skill-name> [--manual]"
allowed-tools: [Skill, Task, Write, Bash]
---

# Create Skill

Create a new skill (AI-assisted or manual).

If $ARGUMENTS is empty, display help:

## Usage
```
/as-you:create-skill "skill-name"              # AI-assisted mode
/as-you:create-skill "skill-name" --manual     # Manual mode
```

## Examples
```
/as-you:create-skill "authentication-debugging"
/as-you:create-skill "api-design-patterns" --manual
```

---

If $ARGUMENTS is provided:

### Manual Mode (with --manual flag)

1. Remove unwanted characters from skill name (convert to kebab-case)
2. Create `skills/{skill-name}/` directory
3. Create template SKILL.md:
   ```markdown
   ---
   name: {skill-name}
   description: "Skill description. Clearly describe when users should use this."
   ---

   # {Skill Name}

   ## Overview

   [Purpose and use cases for this skill]

   ## Use Cases

   - Use case 1
   - Use case 2

   ## Guidelines

   1. Guideline 1
   2. Guideline 2

   ## Examples

   [Specific usage examples]
   ```
4. Create `skills/{skill-name}/reference/` and `skills/{skill-name}/examples/` directories
5. Respond: "Skill '{skill-name}' template created"
6. Guide: "Edit `skills/{skill-name}/SKILL.md` to add content"

### AI-Assisted Mode (default)

1. **Load plugin-dev skill-development skill**:
   ```
   Skill tool: "plugin-dev:skill-development"
   ```
2. **Launch component-generator agent**:
   ```
   Task tool:
   subagent_type: "component-generator"
   prompt: "Create skill '{skill-name}'. Analyze patterns and use cases to generate appropriate SKILL.md."
   description: "Generate skill component"
   ```
3. Review generated content
4. Request approval using AskUserQuestion
5. If approved, create file
6. Respond: "Skill '{skill-name}' created"

## Related Commands
- `/as-you:create-agent "name"` - Create agent
- `/as-you:memory-analyze` - Analyze patterns
