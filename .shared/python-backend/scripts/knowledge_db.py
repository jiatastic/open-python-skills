#!/usr/bin/env python3
"""
Local Knowledge Database for open-python-skills.
Searches FastAPI best practices and other curated content.

Usage:
    python3 scripts/knowledge_db.py "async routes"
    python3 scripts/knowledge_db.py "pydantic validation" --category pydantic
    python3 scripts/knowledge_db.py --list-categories
    python3 scripts/knowledge_db.py --list-tags
    python3 scripts/knowledge_db.py --tag async
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SearchResult:
    id: str
    title: str
    category: str
    summary: str
    tags: list[str]
    relevance: float
    has_code: bool


class KnowledgeDB:
    """Local searchable knowledge database."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = data_dir
        self.entries: list[dict] = []
        self.sources: list[str] = []
        self._load_all()

    def _load_all(self):
        """Load all JSON data files from data directory."""
        if not self.data_dir.exists():
            return

        for json_file in self.data_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "entries" in data:
                        self.entries.extend(data["entries"])
                        if "source" in data:
                            self.sources.append(data["source"])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load {json_file}: {e}", file=sys.stderr)

    def _calculate_relevance(self, query: str, entry: dict) -> float:
        """Calculate relevance score for an entry against a query."""
        query_terms = query.lower().split()
        score = 0.0

        title = entry.get("title", "").lower()
        for term in query_terms:
            if term in title:
                score += 0.4

        if query.lower() in title:
            score += 0.3

        tags = [t.lower() for t in entry.get("tags", [])]
        for term in query_terms:
            if term in tags:
                score += 0.3

        summary = entry.get("summary", "").lower()
        for term in query_terms:
            if term in summary:
                score += 0.15

        content = entry.get("content", "").lower()
        for term in query_terms:
            if term in content:
                score += 0.05

        category = entry.get("category", "").lower()
        for term in query_terms:
            if term in category:
                score += 0.2

        code_examples = entry.get("code_examples", [])
        for example in code_examples:
            code = example.get("code", "").lower()
            desc = example.get("description", "").lower()
            for term in query_terms:
                if term in code or term in desc:
                    score += 0.1
                    break

        return min(score, 1.0)

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 10,
    ) -> list[SearchResult]:
        """Search the knowledge base."""
        results = []

        for entry in self.entries:
            if category and entry.get("category", "").lower() != category.lower():
                continue

            if tag:
                entry_tags = [t.lower() for t in entry.get("tags", [])]
                if tag.lower() not in entry_tags:
                    continue

            relevance = self._calculate_relevance(query, entry)

            if relevance > 0.05:
                results.append(
                    SearchResult(
                        id=entry.get("id", ""),
                        title=entry.get("title", ""),
                        category=entry.get("category", ""),
                        summary=entry.get("summary", ""),
                        tags=entry.get("tags", []),
                        relevance=relevance,
                        has_code=bool(entry.get("code_examples")),
                    )
                )

        results.sort(key=lambda x: x.relevance, reverse=True)
        return results[:limit]

    def get_entry(self, entry_id: str) -> Optional[dict]:
        """Get a specific entry by ID."""
        for entry in self.entries:
            if entry.get("id") == entry_id:
                return entry
        return None

    def list_categories(self) -> list[str]:
        """List all unique categories."""
        categories = set()
        for entry in self.entries:
            if cat := entry.get("category"):
                categories.add(cat)
        return sorted(categories)

    def list_tags(self) -> list[tuple[str, int]]:
        """List all tags with counts."""
        tag_counts: dict[str, int] = {}
        for entry in self.entries:
            for tag in entry.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))

    def get_by_category(self, category: str) -> list[dict]:
        """Get all entries in a category."""
        return [e for e in self.entries if e.get("category", "").lower() == category.lower()]

    def get_by_tag(self, tag: str) -> list[dict]:
        """Get all entries with a specific tag."""
        tag_lower = tag.lower()
        return [
            e for e in self.entries
            if tag_lower in [t.lower() for t in e.get("tags", [])]
        ]


def format_results(results: list[SearchResult], verbose: bool = False) -> str:
    """Format search results for display."""
    if not results:
        return "No results found."

    output = []
    for i, r in enumerate(results, 1):
        output.append(f"\n{'='*70}")
        output.append(f"[{i}] {r.title}")
        output.append(
            f"    Category: {r.category} | Relevance: {r.relevance:.0%} | Code: {'yes' if r.has_code else 'no'}"
        )
        output.append(f"    Tags: {', '.join(r.tags)}")
        output.append(f"{'─'*70}")
        
        words = r.summary.split()
        lines = []
        current_line = "    "
        for word in words:
            if len(current_line) + len(word) + 1 > 70:
                lines.append(current_line)
                current_line = "    " + word
            else:
                current_line += " " + word if current_line.strip() else "    " + word
        if current_line.strip():
            lines.append(current_line)
        output.extend(lines)

        if verbose:
            output.append(f"\n    ID: {r.id}")

    return "\n".join(output)


def format_entry_detail(entry: dict) -> str:
    """Format a full entry for display."""
    output = []
    output.append(f"\n{'='*70}")
    output.append(f"# {entry.get('title', 'Untitled')}")
    output.append(f"{'='*70}")
    output.append(f"Category: {entry.get('category', 'N/A')}")
    output.append(f"Tags: {', '.join(entry.get('tags', []))}")
    output.append(f"\n## Summary\n{entry.get('summary', 'N/A')}")
    output.append(f"\n## Content\n{entry.get('content', 'N/A')}")

    code_examples = entry.get("code_examples", [])
    if code_examples:
        output.append("\n## Code Examples")
        for i, example in enumerate(code_examples, 1):
            output.append(f"\n### Example {i}: {example.get('description', 'Code')}")
            output.append(f"```python\n{example.get('code', '')}\n```")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Search open-python-skills knowledge database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "async routes"
  %(prog)s "pydantic validation" --category pydantic
  %(prog)s --tag async
  %(prog)s --list-categories
  %(prog)s --list-tags
  %(prog)s --get project-structure
        """,
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--tag", "-t", help="Filter by tag")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--list-tags", action="store_true", help="List all tags with counts")
    parser.add_argument("--get", "-g", metavar="ID", help="Get full entry by ID")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show entry IDs")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")

    args = parser.parse_args()

    db = KnowledgeDB()

    if args.stats:
        print("Knowledge Database Statistics")
        print(f"{'─'*40}")
        print(f"Total entries: {len(db.entries)}")
        print(f"Sources: {len(db.sources)}")
        for source in db.sources:
            print(f"  - {source}")
        print(f"Categories: {len(db.list_categories())}")
        print(f"Unique tags: {len(db.list_tags())}")
        return

    if args.list_categories:
        print("\nAvailable Categories:\n")
        for cat in db.list_categories():
            count = len(db.get_by_category(cat))
            print(f"  {cat:20} ({count} entries)")
        return

    if args.list_tags:
        print("\nAvailable Tags:\n")
        for tag, count in db.list_tags():
            print(f"  {tag:25} ({count})")
        return

    if args.get:
        entry = db.get_entry(args.get)
        if entry:
            print(format_entry_detail(entry))
        else:
            print(f"Entry '{args.get}' not found.")
            sys.exit(1)
        return

    if not args.query and not args.tag:
        parser.print_help()
        sys.exit(1)

    query = args.query or ""
    if args.tag and not args.query:
        entries = db.get_by_tag(args.tag)
        if entries:
            print(f"\nEntries tagged with '{args.tag}':\n")
            for e in entries:
                code_mark = "yes" if e.get("code_examples") else "no"
                print(f"  [{e.get('id')}] {e.get('title')} ({e.get('category')}) Code:{code_mark}")
        else:
            print(f"No entries found with tag '{args.tag}'")
        return

    results = db.search(query, category=args.category, tag=args.tag, limit=args.limit)
    print(format_results(results, verbose=args.verbose))


if __name__ == "__main__":
    main()
