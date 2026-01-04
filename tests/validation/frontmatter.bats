#!/usr/bin/env bats

# Validation tests for YAML frontmatter in commands, agents, and skills

setup() {
    export PROJECT_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    export COMMANDS_DIR="$PROJECT_ROOT/commands"
    export AGENTS_DIR="$PROJECT_ROOT/agents"
    export SKILLS_DIR="$PROJECT_ROOT/skills"
    export FIXTURES_DIR="${BATS_TEST_DIRNAME}/../fixtures"
}

# Helper function to check frontmatter validity
has_valid_frontmatter() {
    local file="$1"
    local required_fields=("${@:2}")

    # Check if file starts with ---
    if ! head -n 1 "$file" | grep -q "^---$"; then
        return 1
    fi

    # Extract frontmatter
    local frontmatter=$(sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d')

    # Check required fields
    for field in "${required_fields[@]}"; do
        if ! echo "$frontmatter" | grep -q "^${field}:"; then
            echo "Missing field: $field in $file"
            return 1
        fi
    done

    return 0
}

# Test: All commands have valid frontmatter
@test "validation: all commands have valid frontmatter" {
    skip_count=0

    for cmd in "$COMMANDS_DIR"/*.md; do
        # Skip README
        [[ "$(basename "$cmd")" == "README.md" ]] && continue

        if ! has_valid_frontmatter "$cmd" "name" "description"; then
            echo "Invalid frontmatter in: $(basename "$cmd")"
            ((skip_count++))
        fi
    done

    [ "$skip_count" -eq 0 ]
}

# Test: All agents have valid frontmatter
@test "validation: all agents have valid frontmatter" {
    skip_count=0

    for agent in "$AGENTS_DIR"/*.md; do
        # Skip README
        [[ "$(basename "$agent")" == "README.md" ]] && continue

        if ! has_valid_frontmatter "$agent" "name" "description"; then
            echo "Invalid frontmatter in: $(basename "$agent")"
            ((skip_count++))
        fi
    done

    [ "$skip_count" -eq 0 ]
}

# Test: All skills have valid frontmatter
@test "validation: all skills have valid SKILL.md frontmatter" {
    skip_count=0

    for skill_dir in "$SKILLS_DIR"/*; do
        [ -d "$skill_dir" ] || continue

        skill_file="$skill_dir/SKILL.md"
        if [ -f "$skill_file" ]; then
            if ! has_valid_frontmatter "$skill_file" "name" "description"; then
                echo "Invalid frontmatter in: $skill_file"
                ((skip_count++))
            fi
        fi
    done

    [ "$skip_count" -eq 0 ]
}

# Test: Commands have unique names
@test "validation: command names are unique" {
    names=()

    for cmd in "$COMMANDS_DIR"/*.md; do
        [[ "$(basename "$cmd")" == "README.md" ]] && continue

        name=$(sed -n '/^---$/,/^---$/p' "$cmd" | grep "^name:" | cut -d: -f2- | xargs)
        if [ -n "$name" ]; then
            # Check for duplicates
            if [[ " ${names[@]} " =~ " ${name} " ]]; then
                echo "Duplicate command name: $name"
                return 1
            fi
            names+=("$name")
        fi
    done

    [ "${#names[@]}" -gt 0 ]
}

# Test: Sample valid frontmatter passes validation
@test "validation: sample valid frontmatter passes" {
    has_valid_frontmatter "$FIXTURES_DIR/sample-command.md" "name" "description"
}

# Test: Sample invalid frontmatter fails validation
@test "validation: sample invalid frontmatter fails" {
    run has_valid_frontmatter "$FIXTURES_DIR/invalid-frontmatter.md" "name" "description"

    [ "$status" -ne 0 ]
}

# Test: Frontmatter description is not empty
@test "validation: frontmatter descriptions are not empty" {
    for cmd in "$COMMANDS_DIR"/*.md; do
        [[ "$(basename "$cmd")" == "README.md" ]] && continue

        description=$(sed -n '/^---$/,/^---$/p' "$cmd" | grep "^description:" | cut -d: -f2- | xargs)

        if [ -z "$description" ]; then
            echo "Empty description in: $(basename "$cmd")"
            return 1
        fi
    done
}

# Test: YAML frontmatter is parseable
@test "validation: YAML frontmatter is valid YAML syntax" {
    # Check if yq is available
    if ! command -v yq &> /dev/null; then
        skip "yq not installed"
    fi

    for cmd in "$COMMANDS_DIR"/*.md; do
        [[ "$(basename "$cmd")" == "README.md" ]] && continue

        # Extract frontmatter and validate with yq
        sed -n '/^---$/,/^---$/p' "$cmd" | yq eval '.' - > /dev/null 2>&1 || {
            echo "Invalid YAML in: $(basename "$cmd")"
            return 1
        }
    done
}
