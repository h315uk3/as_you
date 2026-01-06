#!/usr/bin/env python3
"""
Extract contexts for frequent patterns from archived memos.
Replaces extract-contexts.sh with testable Python implementation.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List


def load_tracker(tracker_file: Path) -> Dict:
    """
    Load tracker data.

    Args:
        tracker_file: Path to pattern_tracker.json

    Returns:
        Tracker data dictionary

    Examples:
        >>> from pathlib import Path
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        ...     _ = f.write('{"patterns": {"test": {"count": 5}}}')
        ...     temp_path = Path(f.name)
        >>> data = load_tracker(temp_path)
        >>> 'patterns' in data
        True
        >>> temp_path.unlink()
    """
    if not tracker_file.exists():
        return {}

    try:
        with open(tracker_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def get_top_patterns(tracker: Dict, limit: int = 10) -> List[str]:
    """
    Get top N patterns by count.

    Args:
        tracker: Tracker data dictionary
        limit: Maximum number of patterns to return

    Returns:
        List of pattern names sorted by count (descending)

    Examples:
        >>> tracker = {
        ...     "patterns": {
        ...         "python": {"count": 10},
        ...         "test": {"count": 5},
        ...         "deploy": {"count": 15}
        ...     }
        ... }
        >>> get_top_patterns(tracker, limit=2)
        ['deploy', 'python']
        >>> get_top_patterns(tracker, limit=5)
        ['deploy', 'python', 'test']
    """
    patterns = tracker.get("patterns", {})

    # Sort by count (descending)
    sorted_patterns = sorted(
        patterns.items(), key=lambda x: x[1].get("count", 0), reverse=True
    )

    # Return top N pattern names
    return [name for name, _ in sorted_patterns[:limit]]


def extract_contexts_for_pattern(
    pattern: str, archive_dir: Path, max_contexts: int = 5
) -> List[str]:
    """
    Extract context lines for a pattern from archived memos.

    Args:
        pattern: Pattern to search for
        archive_dir: Path to session archive directory
        max_contexts: Maximum number of context lines to return

    Returns:
        List of context lines (with surrounding context)

    Examples:
        >>> from pathlib import Path
        >>> import tempfile
        >>> temp_dir = Path(tempfile.mkdtemp())
        >>> _ = (temp_dir / "memo1.md").write_text("Line before\\nPython is great\\nLine after")
        >>> contexts = extract_contexts_for_pattern("Python", temp_dir, max_contexts=3)
        >>> len(contexts) > 0
        True
        >>> import shutil
        >>> shutil.rmtree(temp_dir)
    """
    if not archive_dir.exists():
        return []

    contexts = []

    try:
        # Search all .md files in archive
        for md_file in archive_dir.glob("*.md"):
            if not md_file.is_file():
                continue

            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except (IOError, UnicodeDecodeError):
                continue

            # Search for pattern (case-insensitive)
            pattern_lower = pattern.lower()
            for i, line in enumerate(lines):
                if pattern_lower in line.lower():
                    # Get context: line before, matching line, line after
                    context_lines = []
                    if i > 0:
                        context_lines.append(lines[i - 1].strip())
                    context_lines.append(line.strip())
                    if i < len(lines) - 1:
                        context_lines.append(lines[i + 1].strip())

                    # Add non-empty context lines
                    for ctx_line in context_lines:
                        if ctx_line and ctx_line != "--":
                            contexts.append(ctx_line)

                            if len(contexts) >= max_contexts:
                                return contexts
    except Exception:
        pass

    return contexts


def extract_contexts(
    tracker_file: Path, archive_dir: Path, top_n: int = 10, max_contexts: int = 5
) -> Dict:
    """
    Extract contexts for top N patterns.

    Args:
        tracker_file: Path to pattern_tracker.json
        archive_dir: Path to session archive directory
        top_n: Number of top patterns to process
        max_contexts: Maximum contexts per pattern

    Returns:
        Dictionary with pattern contexts

    Examples:
        >>> from pathlib import Path
        >>> import tempfile, json
        >>> tracker_data = {"patterns": {"test": {"count": 5}}}
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        ...     json.dump(tracker_data, f)
        ...     tracker_path = Path(f.name)
        >>> archive_path = Path(tempfile.mkdtemp())
        >>> result = extract_contexts(tracker_path, archive_path)
        >>> 'patterns' in result
        True
        >>> tracker_path.unlink()
        >>> archive_path.rmdir()
    """
    # Load tracker
    tracker = load_tracker(tracker_file)
    if not tracker:
        return {}

    # Get top patterns
    top_patterns = get_top_patterns(tracker, limit=top_n)
    if not top_patterns:
        return {}

    # Extract contexts for each pattern
    result = {"patterns": {}}

    for pattern in top_patterns:
        count = tracker["patterns"][pattern].get("count", 0)
        contexts = extract_contexts_for_pattern(pattern, archive_dir, max_contexts)

        result["patterns"][pattern] = {"count": count, "contexts": contexts}

    return result


def main():
    """CLI entry point."""
    # Get paths from environment or defaults
    project_root = os.getenv("PROJECT_ROOT", os.getcwd())
    claude_dir = Path(os.getenv("CLAUDE_DIR", os.path.join(project_root, ".claude")))
    tracker_file = claude_dir / "as_you" / "pattern_tracker.json"
    archive_dir = claude_dir / "as_you" / "session_archive"

    # Extract contexts
    result = extract_contexts(tracker_file, archive_dir, top_n=10, max_contexts=5)

    # Output JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import doctest

    # Check if running doctests
    if "--test" in sys.argv or "-v" in sys.argv:
        print("Running context extractor doctests:")
        results = doctest.testmod(verbose=("--verbose" in sys.argv or "-v" in sys.argv))
        if results.failed == 0:
            print(f"\n✓ All {results.attempted} doctests passed")
        else:
            print(f"\n✗ {results.failed}/{results.attempted} doctests failed")
            sys.exit(1)
    else:
        main()
