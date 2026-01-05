#!/usr/bin/env python3
"""
Excalidraw Library Manager
Loads and manages component libraries for professional diagram generation.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import uuid
import copy
import re


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
        """Create a positioned instance of this component."""
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

            # Update group IDs to keep elements together
            if new_el.get("groupIds"):
                new_el["groupIds"] = [new_group_id]
            else:
                new_el["groupIds"] = [new_group_id]

            new_el["seed"] = hash(new_el["id"]) % 1000000
            new_el["versionNonce"] = hash(new_el["id"] + "v") % 1000000
            result.append(new_el)

        return result


class LibraryManager:
    """Manages Excalidraw component libraries."""

    # Mapping from component keywords to library component names
    COMPONENT_KEYWORDS = {
        # Databases
        "database": ["database", "db", "sql", "postgres", "mysql", "postgresql", "mariadb"],
        "relational_db": ["relational", "rdbms", "sql", "postgres", "mysql"],
        "document_db": ["document", "mongodb", "mongo", "nosql", "firestore"],
        "graph_db": ["graph", "neo4j", "graphdb", "neptune"],
        "columnar_db": ["columnar", "column", "cassandra", "hbase", "clickhouse"],
        "cache": ["cache", "redis", "memcached", "elasticache"],
        # Storage
        "object_storage": ["object", "s3", "blob", "storage", "minio", "gcs"],
        "cold_storage": ["cold", "archive", "glacier", "backup"],
        "stack_storage": ["stack", "queue", "buffer"],
        # Servers
        "server": ["server", "instance", "vm", "ec2", "compute"],
        "application_server": ["app", "application", "backend", "api"],
        "multi_instance": ["multi", "cluster", "replicated", "scaled"],
        # Network
        "load_balancer": ["load", "balancer", "lb", "elb", "alb", "nlb", "nginx"],
        "cdn": ["cdn", "cloudfront", "akamai", "fastly", "edge"],
        "dns": ["dns", "route53", "domain", "nameserver"],
        # Messaging
        "message_queue": ["queue", "message", "mq", "sqs", "rabbitmq", "kafka", "pubsub"],
        "pipeline": ["pipeline", "etl", "stream", "kinesis", "dataflow"],
        # Security
        "auth_iam": ["auth", "iam", "identity", "oauth", "cognito", "keycloak"],
        # Cloud
        "cloud": ["cloud", "aws", "gcp", "azure", "provider"],
        # Client
        "web_application": ["web", "frontend", "webapp", "browser", "react", "vue"],
        "mobile": ["mobile", "ios", "android", "app", "phone"],
        # Generic
        "gateway": ["gateway", "api gateway", "kong", "apigee"],
        "container": ["container", "docker", "kubernetes", "k8s", "pod"],
        "function": ["function", "lambda", "serverless", "faas"],
        "monitoring": ["monitoring", "metrics", "prometheus", "grafana", "datadog"],
    }

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

        library_items = data.get("library", [])
        lib_name = lib_path.stem

        for idx, item in enumerate(library_items):
            if not isinstance(item, list) or not item:
                continue

            # Try to extract a name from text elements
            component_name = self._extract_component_name(item, idx, lib_name)
            keywords = self._extract_keywords(item, component_name)

            component = LibraryComponent(
                name=component_name,
                elements=item,
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
                    # Clean up the text for use as a name
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

        # Add words from the component name
        for word in re.split(r"[_\s-]", component_name.lower()):
            if len(word) > 2:
                keywords.add(word)

        # Add words from text elements
        for el in elements:
            if el.get("type") == "text":
                text = el.get("text", "").lower()
                for word in re.split(r"[\s\n_-]", text):
                    clean_word = re.sub(r"[^a-z0-9]", "", word)
                    if len(clean_word) > 2:
                        keywords.add(clean_word)

        return list(keywords)

    def find_component(self, query: str) -> Optional[LibraryComponent]:
        """Find the best matching component for a query."""
        self.load_libraries()
        query_lower = query.lower()
        query_words = set(re.split(r"[\s_-]", query_lower))

        best_match: Optional[LibraryComponent] = None
        best_score = 0

        for component in self.components.values():
            score = 0

            # Check for keyword matches
            for keyword in component.keywords:
                if keyword in query_lower:
                    score += 2
                if keyword in query_words:
                    score += 3

            # Check against known component types
            for comp_type, type_keywords in self.COMPONENT_KEYWORDS.items():
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

    def get_component_for_type(self, component_type: str) -> Optional[LibraryComponent]:
        """Get a component matching a specific type."""
        self.load_libraries()

        # First try direct name match
        for name, component in self.components.items():
            if component_type.lower().replace("_", "") in name.lower().replace("_", ""):
                return component

        # Then try keyword-based search
        keywords = self.COMPONENT_KEYWORDS.get(component_type, [])
        if keywords:
            for keyword in keywords:
                result = self.find_component(keyword)
                if result:
                    return result

        return None

    def classify_component(self, name: str) -> str:
        """Classify a component name into a known type."""
        name_lower = name.lower()

        for comp_type, keywords in self.COMPONENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in name_lower:
                    return comp_type

        return "service"  # Default type

    def get_available_types(self) -> List[str]:
        """Get list of available component types."""
        return list(self.COMPONENT_KEYWORDS.keys())

    def list_components(self) -> List[str]:
        """List all loaded components."""
        self.load_libraries()
        return list(self.components.keys())


# Professional color palettes for different component types
COMPONENT_COLORS = {
    # Databases - purple tones
    "database": {"stroke": "#7c3aed", "bg": "#ede9fe"},
    "relational_db": {"stroke": "#6d28d9", "bg": "#ddd6fe"},
    "document_db": {"stroke": "#8b5cf6", "bg": "#e0e7ff"},
    "graph_db": {"stroke": "#a78bfa", "bg": "#f3e8ff"},
    "columnar_db": {"stroke": "#7c3aed", "bg": "#ede9fe"},
    "cache": {"stroke": "#dc2626", "bg": "#fee2e2"},
    # Storage - amber/yellow tones
    "object_storage": {"stroke": "#d97706", "bg": "#fef3c7"},
    "cold_storage": {"stroke": "#92400e", "bg": "#fde68a"},
    "stack_storage": {"stroke": "#b45309", "bg": "#fef3c7"},
    # Servers - blue tones
    "server": {"stroke": "#2563eb", "bg": "#dbeafe"},
    "application_server": {"stroke": "#1d4ed8", "bg": "#bfdbfe"},
    "multi_instance": {"stroke": "#3b82f6", "bg": "#93c5fd"},
    # Network - teal/cyan tones
    "load_balancer": {"stroke": "#0891b2", "bg": "#cffafe"},
    "cdn": {"stroke": "#06b6d4", "bg": "#e0f2fe"},
    "dns": {"stroke": "#0284c7", "bg": "#bae6fd"},
    # Messaging - green tones
    "message_queue": {"stroke": "#16a34a", "bg": "#dcfce7"},
    "pipeline": {"stroke": "#15803d", "bg": "#bbf7d0"},
    # Security - rose/pink tones
    "auth_iam": {"stroke": "#e11d48", "bg": "#ffe4e6"},
    # Cloud - sky blue
    "cloud": {"stroke": "#0ea5e9", "bg": "#e0f2fe"},
    # Client - indigo tones
    "web_application": {"stroke": "#4f46e5", "bg": "#e0e7ff"},
    "mobile": {"stroke": "#6366f1", "bg": "#eef2ff"},
    # Generic - gray/slate
    "gateway": {"stroke": "#475569", "bg": "#f1f5f9"},
    "container": {"stroke": "#0284c7", "bg": "#bae6fd"},
    "function": {"stroke": "#f59e0b", "bg": "#fef3c7"},
    "monitoring": {"stroke": "#84cc16", "bg": "#ecfccb"},
    "service": {"stroke": "#64748b", "bg": "#f1f5f9"},
}


def get_component_colors(component_type: str) -> Dict[str, str]:
    """Get colors for a specific component type."""
    return COMPONENT_COLORS.get(component_type, COMPONENT_COLORS["service"])


if __name__ == "__main__":
    # Test the library manager
    manager = LibraryManager()
    manager.load_libraries()

    print(f"Loaded {len(manager.components)} components from libraries\n")

    print("Sample components:")
    for name in list(manager.components.keys())[:15]:
        comp = manager.components[name]
        print(f"  - {name}: {len(comp.elements)} elements, bounds: {comp.bounds}")

    print("\nTesting component search:")
    test_queries = ["database", "redis", "load balancer", "message queue", "cdn", "api gateway"]
    for query in test_queries:
        result = manager.find_component(query)
        if result:
            print(f"  '{query}' -> {result.name}")
        else:
            print(f"  '{query}' -> (no match)")
