#!/usr/bin/env python3
"""
Track pattern frequency and update pattern_tracker.json.
Replaces track-frequency.sh with testable Python implementation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def load_tracker(tracker_file: Path) -> Dict:
    """
    Load pattern tracker, initialize if needed.

    Args:
        tracker_file: Path to pattern_tracker.json

    Returns:
        Tracker data dictionary

    Examples:
        >>> from pathlib import Path
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        ...     _ = f.write('{"patterns": {}, "promotion_candidates": []}')
        ...     temp_path = Path(f.name)
        >>> data = load_tracker(temp_path)
        >>> 'patterns' in data
        True
        >>> temp_path.unlink()
    """
    if not tracker_file.exists() or tracker_file.stat().st_size == 0:
        return {"patterns": {}, "promotion_candidates": [], "cooccurrences": []}

    try:
        with open(tracker_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure required keys exist
        if "patterns" not in data:
            data["patterns"] = {}
        if "promotion_candidates" not in data:
            data["promotion_candidates"] = []
        if "cooccurrences" not in data:
            data["cooccurrences"] = []

        return data
    except (json.JSONDecodeError, IOError):
        # Invalid or corrupted JSON, reinitialize
        return {"patterns": {}, "promotion_candidates": [], "cooccurrences": []}


def update_pattern(patterns: Dict, word: str, count: int, current_date: str) -> None:
    """
    Update or create pattern entry.

    Args:
        patterns: Patterns dictionary (modified in place)
        word: Pattern word
        count: Occurrence count in this session
        current_date: Current date (YYYY-MM-DD)

    Examples:
        >>> patterns = {}
        >>> update_pattern(patterns, "python", 5, "2026-01-06")
        >>> patterns["python"]["count"]
        5
        >>> patterns["python"]["last_seen"]
        '2026-01-06'
        >>> update_pattern(patterns, "python", 3, "2026-01-07")
        >>> patterns["python"]["count"]
        8
        >>> len(patterns["python"]["sessions"])
        2
    """
    if word in patterns:
        # Update existing pattern
        patterns[word]["count"] = patterns[word].get("count", 0) + count
        patterns[word]["last_seen"] = current_date

        # Add current date to sessions if not already present
        sessions = patterns[word].get("sessions", [])
        if current_date not in sessions:
            sessions.append(current_date)
            patterns[word]["sessions"] = sessions
    else:
        # Create new pattern
        patterns[word] = {
            "count": count,
            "last_seen": current_date,
            "sessions": [current_date],
            "promoted": False,
        }


def merge_contexts(patterns: Dict, contexts_data: Dict) -> None:
    """
    Merge context data into patterns.

    Args:
        patterns: Patterns dictionary (modified in place)
        contexts_data: Context data from extract_contexts

    Examples:
        >>> patterns = {"python": {"count": 5}}
        >>> contexts = {"patterns": {"python": {"contexts": ["test context"]}}}
        >>> merge_contexts(patterns, contexts)
        >>> patterns["python"]["contexts"]
        ['test context']
    """
    contexts_patterns = contexts_data.get("patterns", {})

    for word, context_info in contexts_patterns.items():
        if word in patterns:
            patterns[word]["contexts"] = context_info.get("contexts", [])


def update_frequency(
    tracker_file: Path,
    patterns_data: List[Dict],
    contexts_data: Dict = None,
    cooccurrences: List[Dict] = None,
) -> Dict:
    """
    Update pattern tracker with new frequency data.

    Args:
        tracker_file: Path to pattern_tracker.json
        patterns_data: List of {"word": str, "count": int} dicts
        contexts_data: Optional context data
        cooccurrences: Optional co-occurrence data

    Returns:
        Updated tracker data with statistics

    Examples:
        >>> from pathlib import Path
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        ...     _ = f.write('{"patterns": {}, "promotion_candidates": [], "cooccurrences": []}')
        ...     temp_path = Path(f.name)
        >>> patterns = [{"word": "test", "count": 3}, {"word": "python", "count": 5}]
        >>> result = update_frequency(temp_path, patterns)
        >>> result["pattern_count"]
        2
        >>> temp_path.unlink()
    """
    # Load existing tracker
    tracker = load_tracker(tracker_file)
    patterns = tracker["patterns"]

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Update patterns
    for pattern_obj in patterns_data:
        word = pattern_obj.get("word")
        count = pattern_obj.get("count", 0)

        if not word:
            continue

        update_pattern(patterns, word, count, current_date)

    # Merge contexts if provided
    if contexts_data:
        merge_contexts(patterns, contexts_data)

    # Update co-occurrences if provided
    if cooccurrences is not None:
        tracker["cooccurrences"] = cooccurrences

    # Save tracker
    with open(tracker_file, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)

    # Return statistics
    return {
        "pattern_count": len(patterns),
        "candidate_count": len(tracker.get("promotion_candidates", [])),
    }


def main():
    """CLI entry point."""
    import os
    import subprocess

    # Get paths from environment or defaults
    project_root = os.getenv("PROJECT_ROOT", os.getcwd())
    script_dir = Path(__file__).parent.parent
    claude_dir = Path(os.getenv("CLAUDE_DIR", os.path.join(project_root, ".claude")))
    tracker_file = claude_dir / "as_you" / "pattern_tracker.json"

    # Ensure archive directory exists
    archive_dir = claude_dir / "as_you" / "session_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Get detected patterns from Python implementation
    result = subprocess.run(
        ["python3", str(script_dir / "lib" / "pattern_detector.py")],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "CLAUDE_DIR": str(claude_dir), "PROJECT_ROOT": project_root},
    )

    if result.returncode != 0:
        print("Error detecting patterns", file=sys.stderr)
        sys.exit(1)

    try:
        patterns_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Error parsing pattern data", file=sys.stderr)
        sys.exit(1)

    # Extract contexts (call existing shell script for now)
    contexts_result = subprocess.run(
        [str(script_dir / "extract-contexts.sh")],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PROJECT_ROOT": project_root, "CLAUDE_DIR": str(claude_dir)},
    )
    contexts_data = None
    if contexts_result.returncode == 0 and contexts_result.stdout.strip():
        try:
            contexts_data = json.loads(contexts_result.stdout)
        except json.JSONDecodeError:
            pass

    # Detect co-occurrences (call existing shell script for now)
    cooccur_result = subprocess.run(
        [str(script_dir / "detect-cooccurrence.sh")],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PROJECT_ROOT": project_root, "CLAUDE_DIR": str(claude_dir)},
    )
    cooccurrences = None
    if cooccur_result.returncode == 0 and cooccur_result.stdout.strip():
        try:
            cooccurrences = json.loads(cooccur_result.stdout)
        except json.JSONDecodeError:
            pass

    # Update frequency tracker
    stats = update_frequency(tracker_file, patterns_data, contexts_data, cooccurrences)

    # Calculate scores using Python implementation
    subprocess.run(
        ["python3", str(script_dir / "lib" / "score_calculator.py")],
        env={**os.environ, "PROJECT_ROOT": project_root, "CLAUDE_DIR": str(claude_dir)},
        check=False,
    )

    # Print statistics
    print(
        f"Frequency tracker updated: {stats['pattern_count']} patterns tracked, "
        f"{stats['candidate_count']} promotion candidates (scored)"
    )


if __name__ == "__main__":
    import doctest

    # Check if running doctests
    if "--test" in sys.argv or "-v" in sys.argv:
        print("Running frequency tracker doctests:")
        results = doctest.testmod(verbose=("--verbose" in sys.argv or "-v" in sys.argv))
        if results.failed == 0:
            print(f"\n✓ All {results.attempted} doctests passed")
        else:
            print(f"\n✗ {results.failed}/{results.attempted} doctests failed")
            sys.exit(1)
    else:
        main()
