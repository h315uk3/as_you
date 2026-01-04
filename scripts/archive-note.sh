#!/bin/bash
# Archive session notes to session-archive

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
CLAUDE_DIR="${CLAUDE_DIR:-$PROJECT_ROOT/.claude}"
MEMO_FILE="$CLAUDE_DIR/as-you/session-notes.local.md"
ARCHIVE_DIR="$CLAUDE_DIR/as-you/session-archive"

# Create archive directory if not exists
mkdir -p "$ARCHIVE_DIR"

# Check if memo file exists and is not empty
if [ ! -f "$MEMO_FILE" ] || [ ! -s "$MEMO_FILE" ]; then
	# No memo or empty memo - skip archiving
	exit 0
fi

# Archive with date
DATE=$(date +%Y-%m-%d)
ARCHIVE_FILE="$ARCHIVE_DIR/$DATE.md"

# If archive for today already exists, append; otherwise create
if [ -f "$ARCHIVE_FILE" ]; then
	{
		echo ""
		echo "---"
		echo ""
		cat "$MEMO_FILE"
	} >>"$ARCHIVE_FILE"
else
	cp "$MEMO_FILE" "$ARCHIVE_FILE"
fi

echo "Memo archived to $DATE.md"
