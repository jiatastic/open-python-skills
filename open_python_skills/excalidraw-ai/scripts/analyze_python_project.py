#!/usr/bin/env python3
"""
Python project analyzer for diagram generation.

This module extracts high-level backend architecture signals from a Python codebase
using a best-effort approach:
- AST-based scanning (always available)
- Optional Astral `ty` integration (if installed) for type-check diagnostics metadata
- Optional `ty` LSP symbol scan (best-effort, non-fatal if unsupported)

The output is a small "graph" (nodes + edges) that a renderer can turn into an
Excalidraw diagram.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}


LAYER_ORDER: List[str] = [
    "external",
    "edge",
    "api",
    "service",
    "data",
    "infra",
]


@dataclass(frozen=True)
class GraphNode:
    key: str
    label: str
    kind: str
    layer: str


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    label: Optional[str] = None


def _iter_python_files(project_root: Path) -> Iterable[Path]:
    for path in project_root.rglob("*.py"):
        if any(part in DEFAULT_EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def _safe_parse(path: Path) -> Optional[ast.AST]:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return None


def _collect_imports(tree: ast.AST) -> Set[str]:
    modules: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split(".")[0])
    return modules


def _path_hints(path: Path) -> Set[str]:
    hints: Set[str] = set()
    lower_parts = [p.lower() for p in path.parts]
    for part in lower_parts:
        if part in {"api", "apis", "router", "routers", "routes", "controllers"}:
            hints.add("api")
        if part in {"service", "services", "usecase", "usecases", "domain"}:
            hints.add("service")
        if part in {"repo", "repos", "repository", "repositories", "crud", "dao"}:
            hints.add("data")
        if part in {"db", "database", "models", "model", "migrations"}:
            hints.add("data")
    return hints


def _detect_fastapi(tree: ast.AST) -> Tuple[bool, int]:
    """
    Returns (is_fastapi, route_decorator_count).
    """
    fastapi_imported = False
    route_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("fastapi"):
                fastapi_imported = True
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"FastAPI", "APIRouter"}:
                fastapi_imported = True
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                # router.get("/x"), app.post("/y"), etc.
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    if dec.func.attr in {"get", "post", "put", "delete", "patch", "options", "head", "websocket"}:
                        route_count += 1
    return fastapi_imported, route_count


def _detect_auth(imports: Set[str], tree: ast.AST) -> bool:
    if any(m in imports for m in {"jwt", "jose", "passlib"}):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("fastapi.security"):
                return True
    return False


def _run_ty_check(project_root: Path) -> Dict[str, Any]:
    """Best-effort integration with Astral ty for type-check metadata."""
    if shutil.which("ty") is None:
        return {"available": False}

    try:
        proc = subprocess.run(
            ["ty", "check", "--project", str(project_root), "--output-format", "concise", "--exit-zero"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        output = "\n".join(output.splitlines()[:80])
        return {"available": True, "summary": output.strip()}
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"available": True, "error": str(e)}


def _detect_package_structure(project_root: Path) -> Dict[str, Any]:
    """
    Detect Python package structure: modules, subpackages, entry points.
    Returns structure info for non-backend projects (CLI tools, libraries, etc.)
    """
    structure: Dict[str, Any] = {
        "is_package": False,
        "package_name": None,
        "modules": [],
        "subpackages": [],
        "entry_points": [],
        "data_dirs": [],
        "script_dirs": [],
    }
    
    # Check for pyproject.toml or setup.py
    has_pyproject = (project_root / "pyproject.toml").exists()
    has_setup = (project_root / "setup.py").exists()
    
    if has_pyproject or has_setup:
        structure["is_package"] = True
    
    # Find package directories (dirs with __init__.py)
    for init_file in project_root.rglob("__init__.py"):
        if any(part in DEFAULT_EXCLUDE_DIRS for part in init_file.parts):
            continue
        pkg_dir = init_file.parent
        rel_path = pkg_dir.relative_to(project_root)
        
        # Skip nested packages for now, get top-level
        if len(rel_path.parts) == 1:
            structure["package_name"] = rel_path.parts[0]
            
            # Scan subpackages
            for subdir in pkg_dir.iterdir():
                if subdir.is_dir() and not subdir.name.startswith(("_", ".")):
                    if (subdir / "SKILL.md").exists() or (subdir / "scripts").exists():
                        # This is a skill/module
                        subpkg_info = {
                            "name": subdir.name,
                            "has_skill_md": (subdir / "SKILL.md").exists(),
                            "has_scripts": (subdir / "scripts").exists(),
                            "has_data": (subdir / "data").exists(),
                            "scripts": [],
                            "data_files": [],
                        }
                        
                        # List scripts
                        scripts_dir = subdir / "scripts"
                        if scripts_dir.exists():
                            for script in scripts_dir.glob("*.py"):
                                if not script.name.startswith("_"):
                                    subpkg_info["scripts"].append(script.name)
                        
                        # List data files
                        data_dir = subdir / "data"
                        if data_dir.exists():
                            for data_file in data_dir.iterdir():
                                if data_file.is_file() and not data_file.name.startswith("."):
                                    subpkg_info["data_files"].append(data_file.name)
                        
                        structure["subpackages"].append(subpkg_info)
            
            # Check for CLI entry point
            cli_file = pkg_dir / "cli.py"
            if cli_file.exists():
                structure["entry_points"].append("cli.py")
            main_file = pkg_dir / "__main__.py"
            if main_file.exists():
                structure["entry_points"].append("__main__.py")
    
    return structure


def _build_package_graph(structure: Dict[str, Any], project_root: Path) -> Tuple[List[GraphNode], List[GraphEdge]]:
    """
    Build a graph representing package structure (for CLI tools, libraries, skill packages).
    Uses cleaner labels for better diagram readability.
    """
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    
    pkg_name = structure.get("package_name") or project_root.name
    
    # Main package node
    nodes.append(GraphNode(
        key="package",
        label=pkg_name,
        kind="package",
        layer="external"
    ))
    
    # Entry point (CLI)
    has_cli = bool(structure.get("entry_points"))
    if has_cli:
        nodes.append(GraphNode(
            key="cli",
            label="CLI",
            kind="cli",
            layer="edge"
        ))
        edges.append(GraphEdge(source="package", target="cli"))
    
    # Subpackages / Skills
    for subpkg in structure.get("subpackages", []):
        subpkg_name = subpkg["name"]
        subpkg_key = f"skill_{subpkg_name}"
        
        nodes.append(GraphNode(
            key=subpkg_key,
            label=subpkg_name,
            kind="skill",
            layer="api"
        ))
        
        # Connect from CLI or package
        parent_key = "cli" if has_cli else "package"
        edges.append(GraphEdge(source=parent_key, target=subpkg_key))
        
        # Scripts - show count only for cleaner display
        scripts = subpkg.get("scripts", [])
        if scripts:
            scripts_key = f"scripts_{subpkg_name}"
            script_count = len(scripts)
            nodes.append(GraphNode(
                key=scripts_key,
                label=f"{script_count} script{'s' if script_count > 1 else ''}",
                kind="script",
                layer="service"
            ))
            edges.append(GraphEdge(source=subpkg_key, target=scripts_key))
        
        # Data files - show count and max 2 extensions
        data_files = subpkg.get("data_files", [])
        if data_files:
            data_key = f"data_{subpkg_name}"
            data_count = len(data_files)
            extensions = sorted(set(Path(f).suffix for f in data_files if Path(f).suffix))
            ext_str = ", ".join(extensions[:2])
            if len(extensions) > 2:
                ext_str += "..."
            
            nodes.append(GraphNode(
                key=data_key,
                label=f"{data_count} files ({ext_str})",
                kind="data",
                layer="data"
            ))
            source_key = scripts_key if scripts else subpkg_key
            edges.append(GraphEdge(source=source_key, target=data_key))
    
    return nodes, edges


def analyze_python_project_to_graph(
    project_path: str,
    *,
    focus: str = "backend",
    use_ty: bool = False,
) -> Dict[str, Any]:
    """
    Analyze a Python project and return a renderable graph:
    {
      "nodes": [{"key","label","kind","layer"}, ...],
      "edges": [{"source","target","label"}, ...],
      "meta": {...}
    }
    
    Supports both:
    - Backend applications (FastAPI, SQLAlchemy, Redis, etc.)
    - Package/CLI tools (skill packages, libraries, etc.)
    """
    project_root = Path(project_path).resolve()
    py_files = list(_iter_python_files(project_root))

    imports_all: Set[str] = set()
    route_count = 0
    fastapi_present = False
    auth_present = False
    sqlalchemy_present = False
    redis_present = False
    queue_present = False
    http_client_present = False
    service_hint_present = False
    data_hint_present = False

    for file_path in py_files:
        tree = _safe_parse(file_path)
        if tree is None:
            continue

        imports = _collect_imports(tree)
        imports_all |= imports

        hints = _path_hints(file_path)
        if "service" in hints:
            service_hint_present = True
        if "data" in hints:
            data_hint_present = True

        is_fastapi, file_routes = _detect_fastapi(tree)
        if is_fastapi:
            fastapi_present = True
        route_count += file_routes

        if _detect_auth(imports, tree):
            auth_present = True

    sqlalchemy_present = any(m in imports_all for m in {"sqlalchemy", "alembic"})
    redis_present = any(m in imports_all for m in {"redis", "aioredis", "upstash_redis"})
    queue_present = any(m in imports_all for m in {"celery", "rq", "dramatiq"})
    http_client_present = any(m in imports_all for m in {"requests", "httpx"})

    # Detect package structure
    pkg_structure = _detect_package_structure(project_root)
    
    # If it's a package with subpackages (skill package, library, etc.), use package graph
    # instead of backend graph
    is_skill_package = pkg_structure.get("is_package") and pkg_structure.get("subpackages")
    is_backend_app = fastapi_present or route_count > 0 or sqlalchemy_present or redis_present
    
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []

    if is_skill_package and not is_backend_app:
        # This is a package/CLI tool, not a backend service
        nodes, edges = _build_package_graph(pkg_structure, project_root)
    else:
        # Original backend analysis logic
        # External caller / client
        nodes.append(GraphNode(key="client", label="Client", kind="external", layer="external"))

        # Edge / gateway (heuristic only)
        nodes.append(GraphNode(key="edge", label="API Gateway / Edge", kind="edge", layer="edge"))
        edges.append(GraphEdge(source="client", target="edge"))

        # API layer
        if fastapi_present or route_count > 0:
            api_label = f"FastAPI API ({route_count} routes)" if route_count else "FastAPI API"
        else:
            api_label = "API Layer"
        nodes.append(GraphNode(key="api", label=api_label, kind="api", layer="api"))
        edges.append(GraphEdge(source="edge", target="api"))

        if auth_present:
            nodes.append(GraphNode(key="auth", label="Auth / Security", kind="service", layer="service"))
            edges.append(GraphEdge(source="api", target="auth"))

        # Service layer
        if focus in {"backend", "all"} and (service_hint_present or http_client_present or auth_present):
            nodes.append(GraphNode(key="svc", label="Service Layer", kind="service", layer="service"))
            edges.append(GraphEdge(source="api", target="svc"))
            if auth_present:
                edges.append(GraphEdge(source="auth", target="svc", label="auth context"))

        # Data layer
        if sqlalchemy_present or data_hint_present:
            nodes.append(GraphNode(key="db", label="Database (SQLAlchemy)", kind="database", layer="data"))
            if any(n.key == "svc" for n in nodes):
                edges.append(GraphEdge(source="svc", target="db"))
            else:
                edges.append(GraphEdge(source="api", target="db"))

        if redis_present:
            nodes.append(GraphNode(key="cache", label="Redis Cache", kind="cache", layer="data"))
            if any(n.key == "svc" for n in nodes):
                edges.append(GraphEdge(source="svc", target="cache"))
            else:
                edges.append(GraphEdge(source="api", target="cache"))

        if queue_present:
            nodes.append(GraphNode(key="queue", label="Queue / Workers", kind="infra", layer="infra"))
            if any(n.key == "svc" for n in nodes):
                edges.append(GraphEdge(source="svc", target="queue"))
            else:
                edges.append(GraphEdge(source="api", target="queue"))

    meta: Dict[str, Any] = {
        "project_root": str(project_root),
        "python_files": len(py_files),
        "imports_top": sorted(list(imports_all))[:30],
        "project_type": "skill_package" if (is_skill_package and not is_backend_app) else "backend",
        "package_structure": pkg_structure if is_skill_package else None,
        "signals": {
            "fastapi": fastapi_present,
            "routes": route_count,
            "auth": auth_present,
            "sqlalchemy": sqlalchemy_present,
            "redis": redis_present,
            "queue": queue_present,
            "http_client": http_client_present,
        },
    }
    if use_ty:
        meta["ty"] = _run_ty_check(project_root)

    return {
        "nodes": [n.__dict__ for n in nodes],
        "edges": [e.__dict__ for e in edges],
        "meta": meta,
    }

