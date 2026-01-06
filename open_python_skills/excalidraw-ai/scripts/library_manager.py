#!/usr/bin/env python3
"""
Excalidraw Library Manager - Helper Utility

A simple utility for AI agents to:
1. Load and search icon libraries from .excalidrawlib files
2. Get professional color palettes for different component types
3. Instantiate library components at specific positions

This is an optional helper - agents can also generate Excalidraw JSON directly
using the schema documented in SKILL.md.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import uuid
import copy
import re


# Professional color palettes for different component types
# These colors are designed for architecture diagrams and system design
COMPONENT_COLORS: Dict[str, Dict[str, str]] = {
    # Databases - purple tones
    "database": {"stroke": "#7c3aed", "bg": "#ede9fe"},
    "relational_db": {"stroke": "#6d28d9", "bg": "#ddd6fe"},
    "document_db": {"stroke": "#8b5cf6", "bg": "#e0e7ff"},
    "graph_db": {"stroke": "#a78bfa", "bg": "#f3e8ff"},
    "columnar_db": {"stroke": "#7c3aed", "bg": "#ede9fe"},
    
    # Cache - red tones
    "cache": {"stroke": "#dc2626", "bg": "#fee2e2"},
    
    # Storage - amber/yellow tones
    "object_storage": {"stroke": "#d97706", "bg": "#fef3c7"},
    "storage": {"stroke": "#d97706", "bg": "#fef3c7"},
    "cold_storage": {"stroke": "#92400e", "bg": "#fde68a"},
    
    # Servers - blue tones
    "server": {"stroke": "#2563eb", "bg": "#dbeafe"},
    "service": {"stroke": "#2563eb", "bg": "#dbeafe"},
    "application_server": {"stroke": "#1d4ed8", "bg": "#bfdbfe"},
    
    # Network - teal/cyan tones
    "load_balancer": {"stroke": "#0891b2", "bg": "#cffafe"},
    "cdn": {"stroke": "#06b6d4", "bg": "#e0f2fe"},
    "dns": {"stroke": "#0284c7", "bg": "#bae6fd"},
    
    # Messaging - green tones
    "message_queue": {"stroke": "#16a34a", "bg": "#dcfce7"},
    "queue": {"stroke": "#16a34a", "bg": "#dcfce7"},
    "pipeline": {"stroke": "#15803d", "bg": "#bbf7d0"},
    
    # Security - rose/pink tones
    "auth": {"stroke": "#e11d48", "bg": "#ffe4e6"},
    "auth_iam": {"stroke": "#e11d48", "bg": "#ffe4e6"},
    
    # Cloud - sky blue
    "cloud": {"stroke": "#0ea5e9", "bg": "#e0f2fe"},
    
    # Client - indigo tones
    "web_application": {"stroke": "#4f46e5", "bg": "#e0e7ff"},
    "frontend": {"stroke": "#4f46e5", "bg": "#e0e7ff"},
    "mobile": {"stroke": "#6366f1", "bg": "#eef2ff"},
    
    # Infrastructure - various
    "gateway": {"stroke": "#475569", "bg": "#f1f5f9"},
    "container": {"stroke": "#0284c7", "bg": "#bae6fd"},
    "function": {"stroke": "#f59e0b", "bg": "#fef3c7"},
    "monitoring": {"stroke": "#84cc16", "bg": "#ecfccb"},
    
    # Default
    "default": {"stroke": "#64748b", "bg": "#f1f5f9"},
}

# Keywords for component type detection
COMPONENT_KEYWORDS: Dict[str, List[str]] = {
    "database": ["database", "db", "sql", "postgres", "mysql", "postgresql", "mariadb"],
    "document_db": ["document", "mongodb", "mongo", "nosql", "firestore"],
    "graph_db": ["graph", "neo4j", "graphdb", "neptune"],
    "cache": ["cache", "redis", "memcached", "elasticache"],
    "storage": ["object", "s3", "blob", "storage", "minio", "gcs"],
    "load_balancer": ["load", "balancer", "lb", "elb", "alb", "nlb", "nginx"],
    "cdn": ["cdn", "cloudfront", "akamai", "fastly", "edge"],
    "message_queue": ["queue", "message", "mq", "sqs", "rabbitmq", "kafka", "pubsub"],
    "auth": ["auth", "iam", "identity", "oauth", "cognito", "keycloak", "jwt"],
    "gateway": ["gateway", "api gateway", "kong", "apigee"],
    "container": ["container", "docker", "kubernetes", "k8s", "pod"],
    "function": ["function", "lambda", "serverless", "faas"],
    "monitoring": ["monitoring", "metrics", "prometheus", "grafana", "datadog"],
    "frontend": ["web", "frontend", "webapp", "browser", "react", "vue"],
    "mobile": ["mobile", "ios", "android", "app", "phone"],
    "service": ["service", "api", "backend", "server", "app", "microservice"],
}


def get_component_colors(component_type: str) -> Dict[str, str]:
    """
    Get colors for a specific component type.
    
    Args:
        component_type: Type of component (e.g., "database", "cache", "queue")
        
    Returns:
        Dict with "stroke" and "bg" color values
        
    Example:
        >>> colors = get_component_colors("database")
        >>> colors
        {"stroke": "#7c3aed", "bg": "#ede9fe"}
    """
    return COMPONENT_COLORS.get(component_type.lower(), COMPONENT_COLORS["default"])


def detect_component_type(name: str) -> str:
    """
    Detect component type from a name using keyword matching.
    
    Args:
        name: Component name (e.g., "Redis Cache", "PostgreSQL Database")
        
    Returns:
        Detected component type string
        
    Example:
        >>> detect_component_type("Redis Cache")
        "cache"
        >>> detect_component_type("PostgreSQL")
        "database"
    """
    name_lower = name.lower()
    
    for comp_type, keywords in COMPONENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return comp_type
    
    return "service"  # Default type


def get_colors_for_name(name: str) -> Dict[str, str]:
    """
    Get colors for a component based on its name.
    
    Args:
        name: Component name
        
    Returns:
        Dict with "stroke" and "bg" color values
        
    Example:
        >>> get_colors_for_name("Redis Cache")
        {"stroke": "#dc2626", "bg": "#fee2e2"}
    """
    comp_type = detect_component_type(name)
    return get_component_colors(comp_type)


class LibraryComponent:
    """Represents a reusable component from an Excalidraw library."""

    def __init__(self, name: str, elements: List[Dict[str, Any]], keywords: List[str]):
        self.name = name
        self.elements = elements  # Raw Excalidraw elements
        self.keywords = keywords
        self._bounds: Optional[Tuple[float, float, float, float]] = None

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Calculate bounding box (min_x, min_y, width, height)."""
        if self._bounds is not None:
            return self._bounds

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for el in self.elements:
            x = el.get("x", 0)
            y = el.get("y", 0)
            w = el.get("width", 0)
            h = el.get("height", 0)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + w)
            max_y = max(max_y, y + h)

        if min_x == float("inf"):
            self._bounds = (0, 0, 100, 100)
        else:
            self._bounds = (min_x, min_y, max_x - min_x, max_y - min_y)

        return self._bounds

    def instantiate(self, x: float, y: float, scale: float = 1.0) -> List[Dict[str, Any]]:
        """
        Create a positioned instance of this component.
        
        Args:
            x: X position for the component
            y: Y position for the component
            scale: Scale factor (default 1.0)
            
        Returns:
            List of Excalidraw element dicts ready to include in a diagram
        """
        min_x, min_y, _, _ = self.bounds
        new_group_id = str(uuid.uuid4())
        result = []

        for el in self.elements:
            new_el = copy.deepcopy(el)
            new_el["id"] = str(uuid.uuid4())
            new_el["x"] = (el.get("x", 0) - min_x) * scale + x
            new_el["y"] = (el.get("y", 0) - min_y) * scale + y
            new_el["width"] = el.get("width", 0) * scale
            new_el["height"] = el.get("height", 0) * scale
            new_el["groupIds"] = [new_group_id]
            new_el["seed"] = hash(new_el["id"]) % 1000000
            new_el["versionNonce"] = hash(new_el["id"] + "v") % 1000000
            result.append(new_el)

        return result


class LibraryManager:
    """
    Manages Excalidraw component libraries.
    
    Load professional icons from .excalidrawlib files and use them in diagrams.
    
    Example:
        >>> manager = LibraryManager()
        >>> manager.load_libraries()
        >>> 
        >>> # Find a component by keyword
        >>> component = manager.find_component("database")
        >>> if component:
        ...     elements = component.instantiate(x=100, y=200)
        >>> 
        >>> # List all available components
        >>> print(manager.list_components())
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.components: Dict[str, LibraryComponent] = {}
        self._loaded = False

    def load_libraries(self) -> None:
        """Load all .excalidrawlib files from the data directory."""
        if self._loaded:
            return

        lib_files = list(self.data_dir.glob("*.excalidrawlib"))
        for lib_file in lib_files:
            self._load_library_file(lib_file)

        self._loaded = True

    def _load_library_file(self, lib_path: Path) -> None:
        """Load a single library file."""
        try:
            with open(lib_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load library {lib_path}: {e}")
            return

        lib_name = lib_path.stem
        
        # Support both formats: "library" (v1) and "libraryItems" (v2)
        library_items = data.get("library", [])
        library_items_v2 = data.get("libraryItems", [])

        # Process v1 format (array of element arrays)
        for idx, item in enumerate(library_items):
            if not isinstance(item, list) or not item:
                continue

            component_name = self._extract_component_name(item, idx, lib_name)
            keywords = self._extract_keywords(item, component_name)

            component = LibraryComponent(
                name=component_name,
                elements=item,
                keywords=keywords,
            )
            self.components[component_name] = component
        
        # Process v2 format (array of {status, elements, ...} objects)
        for idx, item in enumerate(library_items_v2):
            if not isinstance(item, dict):
                continue
            
            elements = item.get("elements", [])
            if not elements:
                continue

            component_name = self._extract_component_name(elements, idx, lib_name)
            keywords = self._extract_keywords(elements, component_name)

            component = LibraryComponent(
                name=component_name,
                elements=elements,
                keywords=keywords,
            )
            self.components[component_name] = component

    def _extract_component_name(
        self, elements: List[Dict[str, Any]], idx: int, lib_name: str
    ) -> str:
        """Extract a meaningful name from component elements."""
        for el in elements:
            if el.get("type") == "text":
                text = el.get("text", "").strip()
                if text and len(text) < 50:
                    clean_name = re.sub(r"\s+", "_", text.lower())
                    clean_name = re.sub(r"[^a-z0-9_]", "", clean_name)
                    if clean_name:
                        return f"{lib_name}_{clean_name}"

        return f"{lib_name}_component_{idx}"

    def _extract_keywords(
        self, elements: List[Dict[str, Any]], component_name: str
    ) -> List[str]:
        """Extract searchable keywords from component elements."""
        keywords = set()

        for word in re.split(r"[_\s-]", component_name.lower()):
            if len(word) > 2:
                keywords.add(word)

        for el in elements:
            if el.get("type") == "text":
                text = el.get("text", "").lower()
                for word in re.split(r"[\s\n_-]", text):
                    clean_word = re.sub(r"[^a-z0-9]", "", word)
                    if len(clean_word) > 2:
                        keywords.add(clean_word)

        return list(keywords)

    def find_component(self, query: str) -> Optional[LibraryComponent]:
        """
        Find the best matching component for a query.
        
        Args:
            query: Search query (e.g., "database", "redis", "load balancer")
            
        Returns:
            LibraryComponent if found, None otherwise
        """
        self.load_libraries()
        query_lower = query.lower()
        query_words = set(re.split(r"[\s_-]", query_lower))

        best_match: Optional[LibraryComponent] = None
        best_score = 0

        for component in self.components.values():
            score = 0

            for keyword in component.keywords:
                if keyword in query_lower:
                    score += 2
                if keyword in query_words:
                    score += 3

            for comp_type, type_keywords in COMPONENT_KEYWORDS.items():
                for kw in type_keywords:
                    if kw in query_lower:
                        if any(k in component.keywords for k in type_keywords):
                            score += 5
                        if comp_type.replace("_", "") in component.name.lower():
                            score += 10

            if score > best_score:
                best_score = score
                best_match = component

        return best_match if best_score >= 5 else None

    def list_components(self) -> List[str]:
        """List all loaded component names."""
        self.load_libraries()
        return list(self.components.keys())

    def list_available_types(self) -> List[str]:
        """List all available component types with colors."""
        return list(COMPONENT_COLORS.keys())


# Convenience functions for direct use
def list_colors() -> None:
    """Print all available component colors."""
    print("Available component colors:\n")
    for comp_type, colors in sorted(COMPONENT_COLORS.items()):
        print(f"  {comp_type:20} stroke: {colors['stroke']}  bg: {colors['bg']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--colors":
        list_colors()
    else:
        # Demo usage
        print("Excalidraw Library Manager - Helper Utility\n")
        
        manager = LibraryManager()
        manager.load_libraries()
        
        print(f"Loaded {len(manager.components)} components from libraries\n")
        
        # Show sample components
        print("Sample components:")
        for name in list(manager.components.keys())[:10]:
            print(f"  - {name}")
        
        # Show color detection
        print("\nColor detection examples:")
        test_names = ["Redis Cache", "PostgreSQL", "API Gateway", "Kafka Queue"]
        for name in test_names:
            colors = get_colors_for_name(name)
            print(f"  {name:20} -> stroke: {colors['stroke']}, bg: {colors['bg']}")
        
        print("\nRun with --colors to see all available colors")
