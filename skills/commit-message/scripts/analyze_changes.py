#!/usr/bin/env python3
"""
Analyze git changes and suggest commit messages.

Usage:
    python3 analyze_changes.py --analyze          # Show all changes
    python3 analyze_changes.py --batch            # Suggest batch commits
    python3 analyze_changes.py --generate "*.py"  # Generate message for pattern
    python3 analyze_changes.py --staged           # Only staged changes
"""

import argparse
import json
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional


@dataclass
class FileChange:
    path: str
    status: str  # A=Added, M=Modified, D=Deleted, R=Renamed
    old_path: Optional[str] = None

    @property
    def filename(self) -> str:
        return Path(self.path).name

    @property
    def directory(self) -> str:
        parent = Path(self.path).parent
        return str(parent) if str(parent) != "." else ""

    @property
    def extension(self) -> str:
        return Path(self.path).suffix


@dataclass
class CommitGroup:
    files: list[FileChange] = field(default_factory=list)
    commit_type: str = "chore"
    scope: str = ""
    description: str = ""

    @property
    def message(self) -> str:
        if self.scope:
            return f"{self.commit_type}({self.scope}): {self.description}"
        return f"{self.commit_type}: {self.description}"


class GitAnalyzer:
    def __init__(self, patterns_path: Optional[Path] = None):
        if patterns_path is None:
            patterns_path = Path(__file__).parent.parent / "data" / "commit_patterns.json"
        self.patterns = self._load_patterns(patterns_path)

    def _load_patterns(self, path: Path) -> dict:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_changes(self, staged_only: bool = False) -> list[FileChange]:
        """Get list of changed files from git."""
        if staged_only:
            cmd = ["git", "diff", "--cached", "--name-status"]
        else:
            cmd = ["git", "status", "--porcelain"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            return []

        changes = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            if staged_only:
                # Format: M\tpath or R100\told\tnew
                parts = line.split("\t")
                status = parts[0][0]
                path = parts[-1]
                old_path = parts[1] if len(parts) > 2 else None
            else:
                # Format: XY path or XY old -> new
                status = line[0] if line[0] != " " else line[1]
                path = line[3:].strip()
                if " -> " in path:
                    old_path, path = path.split(" -> ")
                else:
                    old_path = None

            if status in "AMD?R":
                changes.append(FileChange(
                    path=path,
                    status="A" if status == "?" else status,
                    old_path=old_path
                ))

        return changes

    def _detect_type(self, files: list[FileChange]) -> str:
        """Detect commit type based on files."""
        file_hints = self.patterns.get("file_type_hints", {})
        type_scores = defaultdict(int)

        for f in files:
            # Check file patterns
            for pattern, hint_type in file_hints.items():
                if fnmatch(f.filename, pattern) or f.extension == pattern:
                    type_scores[hint_type] += 1

            # Check if new file
            if f.status == "A":
                type_scores["feat"] += 1
            elif f.status == "D":
                type_scores["chore"] += 1

        if type_scores:
            return max(type_scores, key=type_scores.get)

        # Default based on status
        statuses = {f.status for f in files}
        if statuses == {"A"}:
            return "feat"
        elif statuses == {"D"}:
            return "chore"
        return "refactor"

    def _detect_scope(self, files: list[FileChange]) -> str:
        """Detect scope based on file paths."""
        scope_mappings = self.patterns.get("scope_mappings", {})

        for f in files:
            for prefix, scope in scope_mappings.items():
                if f.path.startswith(prefix) or f"/{prefix}" in f.path:
                    return scope

        # Use common directory as scope
        dirs = [f.directory for f in files if f.directory]
        if dirs and len(set(dirs)) == 1:
            return Path(dirs[0]).name

        return ""

    def _generate_description(self, files: list[FileChange], commit_type: str) -> str:
        """Generate commit description."""
        if len(files) == 1:
            f = files[0]
            action = {"A": "add", "M": "update", "D": "remove", "R": "rename"}.get(f.status, "update")
            return f"{action} {f.filename}"

        # Multiple files
        statuses = {f.status for f in files}
        dirs = list(set(f.directory for f in files if f.directory))

        if len(statuses) == 1:
            action = {"A": "add", "M": "update", "D": "remove"}.get(statuses.pop(), "update")
        else:
            action = "update"

        if len(dirs) == 1:
            return f"{action} {dirs[0]} files"

        return f"{action} {len(files)} files"

    def group_changes(self, changes: list[FileChange]) -> list[CommitGroup]:
        """Group changes into logical commits."""
        if not changes:
            return []

        # Group by directory first
        by_dir: dict[str, list[FileChange]] = defaultdict(list)
        for f in changes:
            key = f.directory or "root"
            by_dir[key].append(f)

        groups = []
        for dir_name, files in by_dir.items():
            # Further split by change type
            by_status: dict[str, list[FileChange]] = defaultdict(list)
            for f in files:
                by_status[f.status].append(f)

            for status, status_files in by_status.items():
                commit_type = self._detect_type(status_files)
                scope = self._detect_scope(status_files)
                description = self._generate_description(status_files, commit_type)

                groups.append(CommitGroup(
                    files=status_files,
                    commit_type=commit_type,
                    scope=scope,
                    description=description
                ))

        # Sort: tests and docs last
        priority = self.patterns.get("grouping_rules", {}).get("priority", [])

        def sort_key(g: CommitGroup) -> tuple:
            type_priority = priority.index(g.commit_type) if g.commit_type in priority else -1
            return (type_priority, g.scope, g.description)

        groups.sort(key=sort_key)
        return groups

    def analyze(self, staged_only: bool = False) -> None:
        """Print analysis of changes."""
        changes = self.get_changes(staged_only)

        if not changes:
            print("No changes found.")
            return

        print(f"\n{'='*60}")
        print(f"Git Changes Analysis {'(staged only)' if staged_only else '(all)'}")
        print(f"{'='*60}\n")

        # Group by status
        by_status: dict[str, list[FileChange]] = defaultdict(list)
        for f in changes:
            by_status[f.status].append(f)

        status_labels = {"A": "Added", "M": "Modified", "D": "Deleted", "R": "Renamed"}

        for status, label in status_labels.items():
            if status in by_status:
                print(f"{label} ({len(by_status[status])}):")
                for f in by_status[status]:
                    print(f"  {f.path}")
                print()

        print(f"Total: {len(changes)} file(s)")

    def batch_suggest(self, staged_only: bool = False) -> None:
        """Suggest batch commits."""
        changes = self.get_changes(staged_only)

        if not changes:
            print("No changes found.")
            return

        groups = self.group_changes(changes)

        print(f"\n{'='*60}")
        print("Suggested Batch Commits")
        print(f"{'='*60}\n")

        for i, group in enumerate(groups, 1):
            print(f"Commit {i}: {group.message}")
            for f in group.files:
                status_symbol = {"A": "+", "M": "~", "D": "-", "R": "→"}.get(f.status, "?")
                print(f"  {status_symbol} {f.path}")
            print()

        print(f"{'─'*60}")
        print(f"Total: {len(groups)} commit(s) for {len(changes)} file(s)")
        print("\nTo commit in order:")
        for i, group in enumerate(groups, 1):
            files_str = " ".join(f'"{f.path}"' for f in group.files)
            print(f"  {i}. git add {files_str}")
            print(f"     git commit -m \"{group.message}\"")

    def generate_message(self, pattern: str = "*", staged_only: bool = False) -> None:
        """Generate commit message for files matching pattern."""
        changes = self.get_changes(staged_only)

        # Filter by pattern
        if pattern != "*":
            changes = [f for f in changes if fnmatch(f.path, pattern) or fnmatch(f.filename, pattern)]

        if not changes:
            print(f"No files matching '{pattern}'")
            return

        commit_type = self._detect_type(changes)
        scope = self._detect_scope(changes)
        description = self._generate_description(changes, commit_type)

        if scope:
            message = f"{commit_type}({scope}): {description}"
        else:
            message = f"{commit_type}: {description}"

        print("Suggested commit message:")
        print(f"  {message}")
        print(f"\nFiles ({len(changes)}):")
        for f in changes:
            print(f"  {f.status} {f.path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze git changes and suggest commit messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze all changes")
    parser.add_argument("--batch", "-b", action="store_true", help="Suggest batch commits")
    parser.add_argument("--generate", "-g", metavar="PATTERN", help="Generate message for pattern")
    parser.add_argument("--staged", "-s", action="store_true", help="Only staged changes")

    args = parser.parse_args()

    analyzer = GitAnalyzer()

    if args.analyze:
        analyzer.analyze(staged_only=args.staged)
    elif args.batch:
        analyzer.batch_suggest(staged_only=args.staged)
    elif args.generate:
        analyzer.generate_message(pattern=args.generate, staged_only=args.staged)
    else:
        # Default: show batch suggestions
        analyzer.batch_suggest(staged_only=args.staged)


if __name__ == "__main__":
    main()
