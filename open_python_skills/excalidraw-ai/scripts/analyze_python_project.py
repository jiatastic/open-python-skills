#!/usr/bin/env python3
"""
Python Project Analyzer - Helper Utility

Analyzes Python projects to extract architecture information that can be used
to generate Excalidraw diagrams.

This is an optional helper - AI agents can also analyze code directly and
generate diagrams using the JSON schema documented in SKILL.md.

Usage:
    python analyze_python_project.py /path/to/project
    python analyze_python_project.py /path/to/project --json
"""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set


DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git", ".hg", ".svn", ".venv", "venv", "__pycache__",
    ".mypy_cache", ".ruff_cache", ".pytest_cache", "node_modules", "dist", "build",
}


@dataclass(frozen=True)
class ArchitectureNode:
    """Represents a component in the architecture."""
    key: str
    label: str
    kind: str
    layer: str


@dataclass(frozen=True)
class ArchitectureEdge:
    """Represents a connection between components."""
    source: str
    target: str
    label: Optional[str] = None


def _iter_python_files(project_root: Path) -> Iterable[Path]:
    """Iterate over Python files, excluding common non-source directories."""
    for path in project_root.rglob("*.py"):
        if any(part in DEFAULT_EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def _safe_parse(path: Path) -> Optional[ast.AST]:
    """Safely parse a Python file."""
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return None


def _collect_imports(tree: ast.AST) -> Set[str]:
    """Extract top-level module names from imports."""
    modules: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split(".")[0])
    return modules


def _detect_patterns(tree: ast.AST, imports: Set[str]) -> Dict[str, Any]:
    """Detect common backend patterns from AST and imports."""
    patterns = {
        "fastapi": False,
        "flask": False,
        "django": False,
        "sqlalchemy": False,
        "redis": False,
        "celery": False,
        "kafka": False,
        "auth": False,
        "route_count": 0,
    }
    
    # Check imports
    if any(m in imports for m in {"fastapi"}):
        patterns["fastapi"] = True
    if any(m in imports for m in {"flask"}):
        patterns["flask"] = True
    if any(m in imports for m in {"django"}):
        patterns["django"] = True
    if any(m in imports for m in {"sqlalchemy", "alembic"}):
        patterns["sqlalchemy"] = True
    if any(m in imports for m in {"redis", "aioredis", "upstash_redis"}):
        patterns["redis"] = True
    if any(m in imports for m in {"celery", "dramatiq", "rq"}):
        patterns["celery"] = True
    if any(m in imports for m in {"kafka", "confluent_kafka", "aiokafka"}):
        patterns["kafka"] = True
    if any(m in imports for m in {"jwt", "jose", "passlib"}):
        patterns["auth"] = True
    
    # Count route decorators
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    if dec.func.attr in {"get", "post", "put", "delete", "patch", "websocket"}:
                        patterns["route_count"] += 1
    
    return patterns


def analyze_project(project_path: str) -> Dict[str, Any]:
    """
    Analyze a Python project and return architecture information.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Dictionary with:
        - nodes: List of architecture components
        - edges: List of connections between components
        - signals: Detected patterns (fastapi, redis, etc.)
        - file_count: Number of Python files analyzed
        
    Example output:
        {
            "nodes": [
                {"key": "api", "label": "FastAPI API", "kind": "api", "layer": "api"},
                {"key": "db", "label": "Database", "kind": "database", "layer": "data"}
            ],
            "edges": [
                {"source": "api", "target": "db"}
            ],
            "signals": {"fastapi": true, "sqlalchemy": true, ...},
            "file_count": 42
        }
    """
    project_root = Path(project_path).resolve()
    py_files = list(_iter_python_files(project_root))
    
    all_imports: Set[str] = set()
    all_patterns: Dict[str, Any] = {
        "fastapi": False,
        "flask": False,
        "django": False,
        "sqlalchemy": False,
        "redis": False,
        "celery": False,
        "kafka": False,
        "auth": False,
        "route_count": 0,
    }
    
    for file_path in py_files:
        tree = _safe_parse(file_path)
        if tree is None:
            continue
        
        imports = _collect_imports(tree)
        all_imports |= imports
        
        patterns = _detect_patterns(tree, imports)
        for key, value in patterns.items():
            if isinstance(value, bool) and value:
                all_patterns[key] = True
            elif key == "route_count":
                all_patterns[key] += value
    
    # Build architecture graph
    nodes: List[ArchitectureNode] = []
    edges: List[ArchitectureEdge] = []
    
    # Client layer
    nodes.append(ArchitectureNode("client", "Client", "external", "external"))
    
    # API layer
    if all_patterns["fastapi"]:
        route_info = f" ({all_patterns['route_count']} routes)" if all_patterns["route_count"] else ""
        nodes.append(ArchitectureNode("api", f"FastAPI{route_info}", "api", "api"))
    elif all_patterns["flask"]:
        nodes.append(ArchitectureNode("api", "Flask API", "api", "api"))
    elif all_patterns["django"]:
        nodes.append(ArchitectureNode("api", "Django", "api", "api"))
    else:
        nodes.append(ArchitectureNode("api", "API Layer", "api", "api"))
    
    edges.append(ArchitectureEdge("client", "api"))
    
    # Auth
    if all_patterns["auth"]:
        nodes.append(ArchitectureNode("auth", "Auth / Security", "auth", "service"))
        edges.append(ArchitectureEdge("api", "auth"))
    
    # Data layer
    if all_patterns["sqlalchemy"]:
        nodes.append(ArchitectureNode("db", "Database (SQLAlchemy)", "database", "data"))
        edges.append(ArchitectureEdge("api", "db"))
    
    if all_patterns["redis"]:
        nodes.append(ArchitectureNode("cache", "Redis Cache", "cache", "data"))
        edges.append(ArchitectureEdge("api", "cache"))
    
    # Message queue
    if all_patterns["celery"]:
        nodes.append(ArchitectureNode("workers", "Celery Workers", "queue", "infra"))
        edges.append(ArchitectureEdge("api", "workers"))
    
    if all_patterns["kafka"]:
        nodes.append(ArchitectureNode("kafka", "Kafka", "queue", "infra"))
        edges.append(ArchitectureEdge("api", "kafka"))
    
    return {
        "nodes": [asdict(n) for n in nodes],
        "edges": [asdict(e) for e in edges],
        "signals": all_patterns,
        "file_count": len(py_files),
        "top_imports": sorted(list(all_imports))[:30],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_python_project.py <project_path> [--json]")
        print("\nAnalyzes a Python project and extracts architecture information.")
        sys.exit(1)
    
    project_path = sys.argv[1]
    output_json = "--json" in sys.argv
    
    result = analyze_project(project_path)
    
    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Analyzed {result['file_count']} Python files\n")
        
        print("Detected patterns:")
        for signal, value in result["signals"].items():
            if value:
                print(f"  [x] {signal}: {value}")
        
        print(f"\nArchitecture components ({len(result['nodes'])} nodes):")
        for node in result["nodes"]:
            print(f"  [{node['layer']:10}] {node['label']} ({node['kind']})")
        
        print(f"\nConnections ({len(result['edges'])} edges):")
        for edge in result["edges"]:
            label = f" [{edge['label']}]" if edge.get("label") else ""
            print(f"  {edge['source']} -> {edge['target']}{label}")


if __name__ == "__main__":
    main()
