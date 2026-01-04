#!/usr/bin/env bats

# Validation tests for JSON files

setup() {
    export PROJECT_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    export PLUGIN_JSON="$PROJECT_ROOT/.claude-plugin/plugin.json"
    export HOOKS_JSON="$PROJECT_ROOT/hooks/hooks.json"
}

# Test: plugin.json is valid JSON
@test "validation: plugin.json is valid JSON" {
    run jq '.' "$PLUGIN_JSON"

    [ "$status" -eq 0 ]
}

# Test: plugin.json has required fields
@test "validation: plugin.json has required fields" {
    # Check name
    run jq -r '.name' "$PLUGIN_JSON"
    [ "$status" -eq 0 ]
    [ -n "$output" ]
    [ "$output" != "null" ]

    # Check version
    run jq -r '.version' "$PLUGIN_JSON"
    [ "$status" -eq 0 ]
    [ -n "$output" ]
    [ "$output" != "null" ]

    # Check description
    run jq -r '.description' "$PLUGIN_JSON"
    [ "$status" -eq 0 ]
    [ -n "$output" ]
    [ "$output" != "null" ]
}

# Test: plugin.json version follows semver
@test "validation: plugin.json version follows semver" {
    run jq -r '.version' "$PLUGIN_JSON"

    [[ "$output" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]
}

# Test: hooks.json is valid JSON
@test "validation: hooks.json is valid JSON" {
    run jq '.' "$HOOKS_JSON"

    [ "$status" -eq 0 ]
}

# Test: hooks.json has valid structure
@test "validation: hooks.json has valid hooks structure" {
    # Check description exists
    run jq -r '.description' "$HOOKS_JSON"
    [ "$status" -eq 0 ]

    # Check hooks object exists
    run jq -r '.hooks' "$HOOKS_JSON"
    [ "$status" -eq 0 ]
    [ "$output" != "null" ]
}

# Test: hooks.json hook commands use ${CLAUDE_PLUGIN_ROOT}
@test "validation: hooks use \${CLAUDE_PLUGIN_ROOT} for paths" {
    # Extract all command paths
    commands=$(jq -r '.. | .command? | select(. != null)' "$HOOKS_JSON")

    while IFS= read -r cmd; do
        if [[ "$cmd" =~ \.sh$ ]]; then
            # Verify it uses ${CLAUDE_PLUGIN_ROOT}
            if [[ ! "$cmd" =~ \$\{CLAUDE_PLUGIN_ROOT\} ]]; then
                echo "Hook command should use \${CLAUDE_PLUGIN_ROOT}: $cmd"
                return 1
            fi
        fi
    done <<< "$commands"
}

# Test: hooks.json references existing scripts
@test "validation: hooks reference existing scripts" {
    # Extract all command paths
    commands=$(jq -r '.. | .command? | select(. != null)' "$HOOKS_JSON")

    while IFS= read -r cmd; do
        if [[ "$cmd" =~ \.sh$ ]]; then
            # Extract script path (remove ${CLAUDE_PLUGIN_ROOT}/)
            script_path="${cmd//\$\{CLAUDE_PLUGIN_ROOT\}\//}"

            # Check if script exists
            if [ ! -f "$PROJECT_ROOT/$script_path" ]; then
                echo "Referenced script does not exist: $script_path"
                return 1
            fi
        fi
    done <<< "$commands"
}

# Test: pattern-tracker.json structure (if exists)
@test "validation: pattern-tracker.json has valid structure" {
    tracker_file="$PROJECT_ROOT/.claude/as-you/pattern-tracker.json"

    # Skip if file doesn't exist
    if [ ! -f "$tracker_file" ]; then
        skip "pattern-tracker.json does not exist yet"
    fi

    # Validate JSON
    run jq '.' "$tracker_file"
    [ "$status" -eq 0 ]

    # Check required fields
    run jq -r '.patterns' "$tracker_file"
    [ "$output" != "null" ]

    run jq -r '.promotion_candidates' "$tracker_file"
    [ "$output" != "null" ]
}

# Test: skill-usage-stats.json structure (if exists)
@test "validation: skill-usage-stats.json has valid structure" {
    stats_file="$PROJECT_ROOT/.claude/as-you/skill-usage-stats.json"

    # Skip if file doesn't exist
    if [ ! -f "$stats_file" ]; then
        skip "skill-usage-stats.json does not exist yet"
    fi

    # Validate JSON
    run jq '.' "$stats_file"
    [ "$status" -eq 0 ]

    # Should be an object with skill names as keys
    run jq -r 'type' "$stats_file"
    [ "$output" == "object" ]
}

# Test: All JSON files in project are valid
@test "validation: all JSON files in project are valid" {
    invalid_count=0

    while IFS= read -r json_file; do
        if ! jq '.' "$json_file" > /dev/null 2>&1; then
            echo "Invalid JSON: $json_file"
            ((invalid_count++))
        fi
    done < <(find "$PROJECT_ROOT" -name "*.json" -type f ! -path "*/node_modules/*" ! -path "*/.git/*")

    [ "$invalid_count" -eq 0 ]
}
