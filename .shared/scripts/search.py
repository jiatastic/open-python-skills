#!/usr/bin/env python3
"""
Knowledge base search for Python Backend Pro Max skill.
Searches reference documents for patterns, examples, and best practices.
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchResult:
    domain: str
    section: str
    content: str
    relevance: float
    line_number: int


DOMAINS = {
    "fastapi": "FastAPI framework best practices",
    "security": "Authentication, authorization, security patterns",
    "database": "Database operations and ORM patterns",
    "upstash": "Upstash Redis, QStash integration",
    "deslop": "Deslopification - AI code cleanup",
    "api": "API design patterns and conventions",
    "perf": "Performance optimization techniques",
    "template": "Project templates and architectures",
}


def get_references_dir() -> Path:
    """Get the references directory path."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "references"


def load_document(domain: str) -> Optional[str]:
    """Load a reference document by domain name."""
    ref_path = get_references_dir() / f"{domain}.md"
    if ref_path.exists():
        return ref_path.read_text()
    return None


def extract_sections(content: str) -> list[tuple[str, str, int]]:
    """Extract sections from markdown content. Returns (heading, content, line_num)."""
    sections = []
    lines = content.split("\n")
    current_heading = "Introduction"
    current_content = []
    current_line = 1
    heading_line = 1

    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            if current_content:
                sections.append((current_heading, "\n".join(current_content), heading_line))
            current_heading = line.lstrip("#").strip()
            current_content = []
            heading_line = i
        else:
            current_content.append(line)

    if current_content:
        sections.append((current_heading, "\n".join(current_content), heading_line))

    return sections


def calculate_relevance(query: str, text: str) -> float:
    """Calculate relevance score for a text against a query."""
    query_terms = query.lower().split()
    text_lower = text.lower()
    
    matches = sum(1 for term in query_terms if term in text_lower)
    exact_match = 1.0 if query.lower() in text_lower else 0.0
    
    return (matches / len(query_terms)) * 0.7 + exact_match * 0.3


def search(query: str, domain: Optional[str] = None, limit: int = 5) -> list[SearchResult]:
    """Search the knowledge base for relevant content."""
    results = []
    domains_to_search = [domain] if domain else list(DOMAINS.keys())

    for d in domains_to_search:
        content = load_document(d)
        if not content:
            continue

        sections = extract_sections(content)
        for heading, section_content, line_num in sections:
            relevance = calculate_relevance(query, f"{heading} {section_content}")
            if relevance > 0.1:
                display_content = section_content.strip()[:500]
                if len(section_content) > 500:
                    display_content += "..."
                
                results.append(SearchResult(
                    domain=d,
                    section=heading,
                    content=display_content,
                    relevance=relevance,
                    line_number=line_num,
                ))

    results.sort(key=lambda x: x.relevance, reverse=True)
    return results[:limit]


def format_results(results: list[SearchResult]) -> str:
    """Format search results for display."""
    if not results:
        return "No results found."

    output = []
    for i, r in enumerate(results, 1):
        output.append(f"\n{'='*60}")
        output.append(f"[{i}] {r.domain}.md → {r.section}")
        output.append(f"    Relevance: {r.relevance:.0%} | Line: {r.line_number}")
        output.append(f"{'─'*60}")
        for line in r.content.split("\n")[:10]:
            output.append(f"    {line}")
        if r.content.count("\n") > 10:
            output.append("    ...")
    
    return "\n".join(output)


def list_domains() -> str:
    """List all available domains."""
    output = ["\nAvailable Domains:\n"]
    for domain, desc in DOMAINS.items():
        output.append(f"  {domain:12} - {desc}")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Search Python Backend Pro Max knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "jwt authentication"
  %(prog)s "dependency injection" --domain fastapi
  %(prog)s "async database" --limit 10
  %(prog)s --list
        """,
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(DOMAINS.keys()),
                        help="Limit search to specific domain")
    parser.add_argument("--limit", "-n", type=int, default=5,
                        help="Maximum number of results (default: 5)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available domains")

    args = parser.parse_args()

    if args.list:
        print(list_domains())
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    results = search(args.query, args.domain, args.limit)
    print(format_results(results))


if __name__ == "__main__":
    main()
