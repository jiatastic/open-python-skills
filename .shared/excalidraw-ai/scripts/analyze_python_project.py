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
    except Exception:
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
    """
    Best-effort integration with Astral ty.
    We only use this for metadata (e.g., ensure the project type-checks), not for the graph itself.
    """
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
        # Keep it small; this is metadata only.
        output = "\n".join(output.splitlines()[:80])
        return {"available": True, "summary": output.strip()}
    except Exception as e:
        return {"available": True, "error": str(e)}


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

    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []

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

