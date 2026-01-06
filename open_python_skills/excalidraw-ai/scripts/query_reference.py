#!/usr/bin/env python3
"""
Excalidraw Reference Query Tool

Search the Excalidraw JSON schema reference for elements, colors, layouts, and examples.

Usage:
    python query_reference.py "rectangle"
    python query_reference.py "database colors"
    python query_reference.py --category colors
    python query_reference.py --get element-rectangle
    python query_reference.py --list-categories
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_reference() -> Dict[str, Any]:
    """Load the reference JSON file."""
    data_dir = Path(__file__).parent.parent / "data"
    ref_file = data_dir / "excalidraw_reference.json"
    
    if not ref_file.exists():
        print(f"Error: Reference file not found at {ref_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(ref_file, "r", encoding="utf-8") as f:
        return json.load(f)


def search_entries(query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search entries by query string and optional category filter."""
    data = load_reference()
    entries = data.get("entries", [])
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    results = []
    
    for entry in entries:
        # Filter by category if specified
        if category and entry.get("category") != category:
            continue
        
        score = 0
        
        # Check title
        if query_lower in entry.get("title", "").lower():
            score += 10
        
        # Check tags
        for tag in entry.get("tags", []):
            if tag in query_lower or any(w in tag for w in query_words):
                score += 5
        
        # Check summary
        if query_lower in entry.get("summary", "").lower():
            score += 3
        
        # Check content
        if query_lower in entry.get("content", "").lower():
            score += 2
        
        # Check ID
        if query_lower in entry.get("id", "").lower():
            score += 8
        
        if score > 0:
            results.append((score, entry))
    
    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in results]


def get_entry_by_id(entry_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific entry by ID."""
    data = load_reference()
    for entry in data.get("entries", []):
        if entry.get("id") == entry_id:
            return entry
    return None


def list_categories() -> List[str]:
    """List all unique categories."""
    data = load_reference()
    categories = set()
    for entry in data.get("entries", []):
        if cat := entry.get("category"):
            categories.add(cat)
    return sorted(categories)


def list_tags() -> List[str]:
    """List all unique tags."""
    data = load_reference()
    tags = set()
    for entry in data.get("entries", []):
        for tag in entry.get("tags", []):
            tags.add(tag)
    return sorted(tags)


def format_entry(entry: Dict[str, Any], verbose: bool = False) -> str:
    """Format an entry for display."""
    lines = []
    lines.append(f"[{entry.get('id', 'unknown')}] {entry.get('title', 'Untitled')}")
    lines.append(f"   Category: {entry.get('category', 'unknown')}")
    lines.append(f"   Tags: {', '.join(entry.get('tags', []))}")
    lines.append(f"   {entry.get('summary', '')}")
    
    if verbose:
        lines.append("")
        lines.append(f"   Content: {entry.get('content', '')}")
        lines.append("")
        for example in entry.get("code_examples", []):
            lines.append(f"   Example: {example.get('description', '')}")
            lines.append("   ```")
            for line in example.get("code", "").split("\n"):
                lines.append(f"   {line}")
            lines.append("   ```")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search Excalidraw JSON schema reference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "rectangle"           Search for rectangle-related entries
  %(prog)s "database colors"     Search for database color schemes
  %(prog)s --category colors     List all color-related entries
  %(prog)s --get element-arrow   Get full details for arrow element
  %(prog)s --list-categories     List all categories
  %(prog)s --list-tags           List all tags
        """
    )
    
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--get", "-g", help="Get entry by ID")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--list-tags", action="store_true", help="List all tags")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show full details")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.list_categories:
        categories = list_categories()
        if args.json:
            print(json.dumps(categories, indent=2))
        else:
            print("Categories:")
            for cat in categories:
                print(f"  - {cat}")
        return
    
    if args.list_tags:
        tags = list_tags()
        if args.json:
            print(json.dumps(tags, indent=2))
        else:
            print("Tags:")
            for tag in tags:
                print(f"  - {tag}")
        return
    
    if args.get:
        entry = get_entry_by_id(args.get)
        if entry:
            if args.json:
                print(json.dumps(entry, indent=2))
            else:
                print(format_entry(entry, verbose=True))
        else:
            print(f"Entry not found: {args.get}", file=sys.stderr)
            sys.exit(1)
        return
    
    if args.category and not args.query:
        # List all entries in category
        results = search_entries("", category=args.category)
        if not results:
            # Fallback: show all entries matching category
            data = load_reference()
            results = [e for e in data.get("entries", []) if e.get("category") == args.category]
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Entries in category '{args.category}':\n")
            for entry in results:
                print(format_entry(entry, verbose=args.verbose))
                print()
        return
    
    if not args.query:
        parser.print_help()
        return
    
    results = search_entries(args.query, category=args.category)
    
    if not results:
        print(f"No entries found for: {args.query}", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Found {len(results)} result(s) for '{args.query}':\n")
        for entry in results[:10]:  # Limit to top 10
            print(format_entry(entry, verbose=args.verbose))
            print()


if __name__ == "__main__":
    main()
