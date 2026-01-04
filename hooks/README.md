# Hooks

Event hook configuration is managed in `.claude/settings.json`.

## Supported Hook Events

- `PreToolUse` - Before tool use
- `PermissionRequest` - On permission request
- `PostToolUse` - After tool use
- `UserPromptSubmit` - On user prompt submission
- `Stop` - On stop
- `SubagentStop` - On subagent stop
- `PreCompact` - Before compact
- `SessionStart` - On session start
- `SessionEnd` - On session end
- `Notification` - On notification

## Hook Format

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash script.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Hook scripts are placed in this directory and referenced from settings.json.
