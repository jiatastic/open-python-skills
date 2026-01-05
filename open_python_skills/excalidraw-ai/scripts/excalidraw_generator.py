#!/usr/bin/env python3
"""
Excalidraw AI Diagram Generator
Diagram generator that outputs Excalidraw JSON.

Usage:
    python3 scripts/excalidraw_generator.py "User login -> Verify -> Access data" --type flowchart
    python3 scripts/excalidraw_generator.py "API Gateway -> Service -> Database" --type architecture
    python3 scripts/excalidraw_generator.py --project . --type architecture
    python3 scripts/excalidraw_generator.py --interactive
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
import uuid
import re

from analyze_python_project import analyze_python_project_to_graph


@dataclass
class ExcalidrawElement:
    """Base class for Excalidraw elements"""
    id: str
    type: str
    x: float
    y: float
    width: float
    height: float
    angle: float = 0
    strokeColor: str = "#1971c2"
    backgroundColor: str = "#a5d8ff"
    fillStyle: str = "solid"
    strokeWidth: int = 2
    strokeStyle: str = "solid"
    roughness: int = 1
    opacity: int = 100
    groupIds: List[str] = field(default_factory=list)


@dataclass
class Rectangle(ExcalidrawElement):
    type: str = field(default="rectangle", init=False)


@dataclass
class Ellipse(ExcalidrawElement):
    type: str = field(default="ellipse", init=False)


@dataclass
class Diamond(ExcalidrawElement):
    type: str = field(default="diamond", init=False)


@dataclass
class Text(ExcalidrawElement):
    type: str = field(default="text", init=False)
    text: str = ""
    fontSize: int = 20
    fontFamily: int = 1
    textAlign: str = "left"
    verticalAlign: str = "top"


@dataclass
class Arrow(ExcalidrawElement):
    type: str = field(default="arrow", init=False)
    points: List[List[float]] = field(default_factory=lambda: [[0, 0], [100, 0]])
    startBinding: Optional[Dict] = None
    endBinding: Optional[Dict] = None
    startArrowhead: Optional[str] = None
    endArrowhead: str = "arrow"


class DiagramTemplate:
    """Base class for diagram templates."""
    
    def __init__(self, name: str):
        self.name = name
    
    def generate_elements(self, description: str, theme: str = "modern") -> List[ExcalidrawElement]:
        """生成图表元素"""
        raise NotImplementedError


class FlowchartTemplate(DiagramTemplate):
    """Flowchart template."""
    
    def __init__(self):
        super().__init__("flowchart")
    
    def generate_elements(self, description: str, theme: str = "modern") -> List[ExcalidrawElement]:
        """Generate flowchart elements."""
        elements = []
        steps = self._parse_flow_description(description)
        
        x_start = 100
        y_start = 100
        step_width = 140
        step_height = 60
        step_spacing = 200
        
        themes = {
            "modern": {"stroke": "#1971c2", "bg": "#e7f5ff", "line": "#1971c2"},
            "sketchy": {"stroke": "#495057", "bg": "#f8f9fa", "line": "#868e96"},
            "technical": {"stroke": "#2f9e44", "bg": "#ebfbee", "line": "#2f9e44"},
            "colorful": {"stroke": "#e03131", "bg": "#fff5f5", "line": "#e03131"}
        }
        theme_colors = themes.get(theme, themes["modern"])
        
        step_elements = []
        
        for i, step in enumerate(steps):
            element_type = self._determine_step_type(step)
            element_id = str(uuid.uuid4())
            x = x_start + i * step_spacing
            y = y_start
            
            node = None
            if element_type == "start/end":
                node = Ellipse(
                    id=element_id,
                    x=x,
                    y=y,
                    width=120,
                    height=60,
                    strokeColor=theme_colors["stroke"],
                    backgroundColor=theme_colors["bg"],
                    fillStyle="hachure" if theme == "sketchy" else "solid",
                    roughness=2 if theme == "sketchy" else 1,
                    strokeWidth=2
                )
            elif element_type == "decision":
                node = Diamond(
                    id=element_id,
                    x=x,
                    y=y,
                    width=100,
                    height=80,
                    strokeColor=theme_colors["stroke"],
                    backgroundColor=theme_colors["bg"],
                    fillStyle="hachure" if theme == "sketchy" else "solid",
                    roughness=2 if theme == "sketchy" else 1,
                    strokeWidth=2
                )
            else:
                node = Rectangle(
                    id=element_id,
                    x=x,
                    y=y,
                    width=step_width,
                    height=step_height,
                    strokeColor=theme_colors["stroke"],
                    backgroundColor=theme_colors["bg"],
                    fillStyle="hachure" if theme == "sketchy" else "solid",
                    roughness=2 if theme == "sketchy" else 1,
                    strokeWidth=2
                )
            
            elements.append(node)
            step_elements.append(node)
            
            text_id = str(uuid.uuid4())
            text = Text(
                id=text_id,
                x=x + 10,
                y=y + (node.height / 2) - 10,
                width=node.width - 20,
                height=20,
                text=step,
                fontSize=16,
                textAlign="center",
                verticalAlign="middle",
                strokeColor=theme_colors["stroke"],
                backgroundColor="transparent",
                fontFamily=3 if theme == "sketchy" else 1
            )
            
            text.x = x + (node.width - len(step) * 8) / 2
            elements.append(text)
            
            node.groupIds = [element_id]
            text.groupIds = [element_id]
            
            if i > 0:
                prev_node = step_elements[i-1]
                curr_node = node
                
                arrow = Arrow(
                    id=str(uuid.uuid4()),
                    x=prev_node.x + prev_node.width,
                    y=prev_node.y + prev_node.height/2,
                    width=curr_node.x - (prev_node.x + prev_node.width),
                    height=2,
                    points=[[0, 0], [curr_node.x - (prev_node.x + prev_node.width), 0]],
                    strokeColor=theme_colors["line"],
                    startBinding={"elementId": prev_node.id, "focus": 0.5, "gap": 5},
                    endBinding={"elementId": curr_node.id, "focus": 0.5, "gap": 5},
                    endArrowhead="arrow"
                )
                elements.append(arrow)
        
        return elements
    
    def _parse_flow_description(self, description: str) -> List[str]:
        """Parse flow description and extract steps."""
        separators = [r'\s*->\s*', r'\s*→\s*', r'\s*then\s*', r'\s*next\s*']
        
        for sep in separators:
            if re.search(sep, description):
                return [step.strip() for step in re.split(sep, description)]
        
        return [description.strip()]
    
    def _determine_step_type(self, step: str) -> str:
        """Determine step type based on content."""
        step_lower = step.lower()
        if any(keyword in step_lower for keyword in ['start', 'begin', 'end', 'finish', 'complete']):
            return "start/end"
        elif any(keyword in step_lower for keyword in ['if', 'decision', 'judge', 'whether']):
            return "decision"
        else:
            return "process"


class ArchitectureTemplate(DiagramTemplate):
    """Architecture diagram template."""
    
    def __init__(self):
        super().__init__("architecture")
    
    def generate_elements(self, description: str, theme: str = "modern") -> List[ExcalidrawElement]:
        """Generate architecture diagram elements from a text description."""
        elements = []
        components = self._parse_architecture_description(description)
        
        x_start = 100
        y_start = 100
        component_width = 160
        component_height = 80
        layer_spacing = 200
        component_spacing = 250
        
        themes = {
            "modern": {"stroke": "#1971c2", "bg": "#e7f5ff"},
            "sketchy": {"stroke": "#495057", "bg": "#f8f9fa"},
            "technical": {"stroke": "#2f9e44", "bg": "#ebfbee"},
            "colorful": {"stroke": "#e03131", "bg": "#fff5f5"}
        }
        
        theme_colors = themes.get(theme, themes["modern"])
        layers = self._organize_by_layers(components)
        
        component_elements = {}
        
        for layer_idx, layer in enumerate(layers):
            for comp_idx, component in enumerate(layer):
                layer_width = len(layer) * component_spacing
                max_layer_size = max(len(layer_items) for layer_items in layers)
                x_offset = (max_layer_size * component_spacing - layer_width) / 2
                
                x = x_start + x_offset + comp_idx * component_spacing
                y = y_start + layer_idx * layer_spacing
                
                element_type = self._determine_component_type(component)
                element_id = str(uuid.uuid4())
                
                if element_type == "database":
                    node = Ellipse(
                        id=element_id,
                        x=x,
                        y=y,
                        width=component_width,
                        height=component_height,
                        strokeColor=theme_colors["stroke"],
                        backgroundColor=theme_colors["bg"],
                        roughness=2 if theme == "sketchy" else 1,
                        strokeWidth=2
                    )
                else:
                    node = Rectangle(
                        id=element_id,
                        x=x,
                        y=y,
                        width=component_width,
                        height=component_height,
                        strokeColor=theme_colors["stroke"],
                        backgroundColor=theme_colors["bg"],
                        roughness=2 if theme == "sketchy" else 1,
                        strokeWidth=2
                    )
                
                elements.append(node)
                component_elements[component] = node
                
                text_id = str(uuid.uuid4())
                text = Text(
                    id=text_id,
                    x=x + 10,
                    y=y + component_height / 2 - 10,
                    width=component_width - 20,
                    height=20,
                    text=component,
                    fontSize=16,
                    textAlign="center",
                    verticalAlign="middle",
                    strokeColor=theme_colors["stroke"],
                    backgroundColor="transparent",
                    fontFamily=3 if theme == "sketchy" else 1
                )
                
                text.x = x + (component_width - len(component)*8)/2
                elements.append(text)
                
                node.groupIds = [element_id]
                text.groupIds = [element_id]

        if "->" in description or "→" in description:
            # Support multiple flows separated by "|" (best-effort).
            flows = [f.strip() for f in description.split("|") if f.strip()]
            for flow in flows:
                self._add_arrows_for_flow(flow, component_elements, elements, theme_colors["stroke"])

        return elements

    def generate_elements_from_graph(self, graph: Dict[str, Any], theme: str = "modern") -> List[ExcalidrawElement]:
        """Generate architecture diagram elements from a structured graph (nodes + edges)."""
        elements: List[ExcalidrawElement] = []

        themes = {
            "modern": {"stroke": "#1971c2", "bg": "#e7f5ff", "line": "#1971c2"},
            "sketchy": {"stroke": "#495057", "bg": "#f8f9fa", "line": "#868e96"},
            "technical": {"stroke": "#2f9e44", "bg": "#ebfbee", "line": "#2f9e44"},
            "colorful": {"stroke": "#e03131", "bg": "#fff5f5", "line": "#e03131"},
        }
        theme_colors = themes.get(theme, themes["modern"])

        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])

        x_start = 100
        y_start = 100
        w = 220
        h = 90
        layer_spacing = 180
        node_spacing = 260

        def layer_index(layer: str) -> int:
            order = ["external", "edge", "api", "service", "data", "infra"]
            return order.index(layer) if layer in order else 99

        layers: Dict[str, List[Dict[str, Any]]] = {}
        for n in nodes:
            layers.setdefault(n.get("layer", "service"), []).append(n)

        # Sort layers and nodes for stable output.
        ordered_layers = sorted(layers.items(), key=lambda kv: layer_index(kv[0]))

        element_by_key: Dict[str, ExcalidrawElement] = {}

        for li, (layer, layer_nodes) in enumerate(ordered_layers):
            layer_nodes = sorted(layer_nodes, key=lambda n: n.get("label", ""))
            y = y_start + li * layer_spacing
            for ni, n in enumerate(layer_nodes):
                x = x_start + ni * node_spacing
                kind = (n.get("kind") or "service").lower()
                element_id = str(uuid.uuid4())

                shape: ExcalidrawElement
                if kind in {"database", "cache"}:
                    shape = Ellipse(
                        id=element_id,
                        x=x,
                        y=y,
                        width=w,
                        height=h,
                        strokeColor=theme_colors["stroke"],
                        backgroundColor=theme_colors["bg"],
                        roughness=2 if theme == "sketchy" else 1,
                        strokeWidth=2,
                    )
                else:
                    shape = Rectangle(
                        id=element_id,
                        x=x,
                        y=y,
                        width=w,
                        height=h,
                        strokeColor=theme_colors["stroke"],
                        backgroundColor=theme_colors["bg"],
                        roughness=2 if theme == "sketchy" else 1,
                        strokeWidth=2,
                        fillStyle="hachure" if theme == "sketchy" else "solid",
                    )

                elements.append(shape)
                element_by_key[n["key"]] = shape

                label = n.get("label", n.get("key", ""))
                text = Text(
                    id=str(uuid.uuid4()),
                    x=x + 10,
                    y=y + h / 2 - 10,
                    width=w - 20,
                    height=20,
                    text=label,
                    fontSize=16,
                    textAlign="center",
                    verticalAlign="middle",
                    strokeColor=theme_colors["stroke"],
                    backgroundColor="transparent",
                    fontFamily=3 if theme == "sketchy" else 1,
                )
                elements.append(text)

        for e in edges:
            s_key = e.get("source")
            t_key = e.get("target")
            if not s_key or not t_key:
                continue
            if s_key not in element_by_key or t_key not in element_by_key:
                continue
            s_el = element_by_key[s_key]
            t_el = element_by_key[t_key]

            sx = s_el.x + s_el.width / 2
            sy = s_el.y + s_el.height / 2
            tx = t_el.x + t_el.width / 2
            ty = t_el.y + t_el.height / 2

            arrow = Arrow(
                id=str(uuid.uuid4()),
                x=sx,
                y=sy,
                width=abs(tx - sx),
                height=abs(ty - sy),
                strokeColor=theme_colors["line"],
                points=[[0, 0], [tx - sx, ty - sy]],
                startBinding={"elementId": s_el.id, "focus": 0.5, "gap": 10},
                endBinding={"elementId": t_el.id, "focus": 0.5, "gap": 10},
                endArrowhead="arrow",
            )
            elements.append(arrow)

        return elements

    def _add_arrows_for_flow(
        self,
        flow: str,
        component_elements: Dict[str, ExcalidrawElement],
        elements: List[ExcalidrawElement],
        stroke_color: str,
    ) -> None:
        raw_steps = re.split(r"\s*(?:->|→)\s*", flow)
        raw_steps = [s.strip() for s in raw_steps]

        for i in range(len(raw_steps) - 1):
            start_node_name = raw_steps[i]
            end_node_name = raw_steps[i + 1]

            start_nodes = [s.strip() for s in start_node_name.split(",") if s.strip()]
            end_nodes = [s.strip() for s in end_node_name.split(",") if s.strip()]

            for s_name in start_nodes:
                for e_name in end_nodes:
                    if s_name in component_elements and e_name in component_elements:
                        start_el = component_elements[s_name]
                        end_el = component_elements[e_name]

                        sx = start_el.x + start_el.width / 2
                        sy = start_el.y + start_el.height / 2
                        ex = end_el.x + end_el.width / 2
                        ey = end_el.y + end_el.height / 2

                        arrow = Arrow(
                            id=str(uuid.uuid4()),
                            x=sx,
                            y=sy,
                            width=abs(ex - sx),
                            height=abs(ey - sy),
                            strokeColor=stroke_color,
                            points=[[0, 0], [ex - sx, ey - sy]],
                            startBinding={"elementId": start_el.id, "focus": 0.5, "gap": 10},
                            endBinding={"elementId": end_el.id, "focus": 0.5, "gap": 10},
                            endArrowhead="arrow",
                        )
                        elements.append(arrow)
    
    def _parse_architecture_description(self, description: str) -> List[str]:
        """Parse architecture description"""
        separators = [r'\s*,\s*', r'\s*->\s*', r'\s*→\s*']
        
        for sep in separators:
            if re.search(sep, description):
                return [comp.strip() for comp in re.split(sep, description)]
        
        return [description.strip()]
    
    def _organize_by_layers(self, components: List[str]) -> List[List[str]]:
        """Organize components by layers"""
        frontend = []
        backend = []
        database = []
        
        for component in components:
            comp_lower = component.lower()
            if any(keyword in comp_lower for keyword in ['ui', 'frontend', 'web', 'app', 'client']):
                frontend.append(component)
            elif any(keyword in comp_lower for keyword in ['database', 'db', 'redis', 'mysql', 'postgres']):
                database.append(component)
            else:
                backend.append(component)
        
        layers = []
        if frontend:
            layers.append(frontend)
        if backend:
            layers.append(backend)
        if database:
            layers.append(database)
        
        return layers or [components]
    

    def _determine_component_type(self, component: str) -> str:
        """Determine component type"""
        comp_lower = component.lower()
        if any(keyword in comp_lower for keyword in ['database', 'db', 'redis', 'mysql', 'postgres']):
            return "database"
        else:
            return "service"


class MindmapTemplate(DiagramTemplate):
    """Mind map template."""
    
    def __init__(self):
        super().__init__("mindmap")
    
    def generate_elements(self, description: str, theme: str = "modern") -> List[ExcalidrawElement]:
        """Generate mind map elements."""
        elements = []
        
        parts = re.split(r'[:：]', description, maxsplit=1)
        root_text = parts[0].strip()
        children_text = parts[1].strip() if len(parts) > 1 else ""
        
        children = []
        if children_text:
            separators = [r',', r'，', r'、', r';', r'\n']
            split_pattern = '|'.join(separators)
            children = [c.strip() for c in re.split(split_pattern, children_text) if c.strip()]
        
        center_x = 400
        center_y = 300
        radius = 250
        
        themes = {
            "modern": {"stroke": "#1971c2", "bg": "#e7f5ff", "line": "#1971c2"},
            "sketchy": {"stroke": "#495057", "bg": "#f8f9fa", "line": "#868e96"},
            "technical": {"stroke": "#2f9e44", "bg": "#ebfbee", "line": "#2f9e44"},
            "colorful": {"stroke": "#e03131", "bg": "#fff5f5", "line": "#e03131"}
        }
        theme_colors = themes.get(theme, themes["modern"])
        
        root_id = str(uuid.uuid4())
        root_width = max(120, len(root_text) * 15)
        root_height = 60
        
        root_node = Rectangle(
            id=root_id,
            x=center_x - root_width/2,
            y=center_y - root_height/2,
            width=root_width,
            height=root_height,
            strokeColor=theme_colors["stroke"],
            backgroundColor=theme_colors["bg"],
            strokeWidth=2,
            fillStyle="hachure" if theme == "sketchy" else "solid",
            roughness=2 if theme == "sketchy" else 1
        )
        elements.append(root_node)
        
        root_text_el = Text(
            id=str(uuid.uuid4()),
            x=center_x - root_width/2 + 10,
            y=center_y - 10,
            width=root_width - 20,
            height=20,
            text=root_text,
            fontSize=20,
            textAlign="center",
            verticalAlign="middle",
            strokeColor=theme_colors["stroke"]
        )
        root_text_el.x = center_x - (len(root_text) * 10) / 2
        elements.append(root_text_el)
        
        root_node.groupIds = [root_id]
        root_text_el.groupIds = [root_id]
        
        import math
        
        if not children:
            return elements
            
        angle_step = 360 / len(children)
        
        for i, child_text in enumerate(children):
            angle_rad = math.radians(i * angle_step)
            
            child_width = max(100, len(child_text) * 12)
            child_height = 50
            
            child_x = center_x + radius * math.cos(angle_rad)
            child_y = center_y + radius * math.sin(angle_rad)
            
            child_id = str(uuid.uuid4())
            
            child_node = Ellipse(
                id=child_id,
                x=child_x - child_width/2,
                y=child_y - child_height/2,
                width=child_width,
                height=child_height,
                strokeColor=theme_colors["stroke"],
                backgroundColor="transparent",
                strokeStyle="dashed" if theme == "technical" else "solid",
                strokeWidth=1
            )
            elements.append(child_node)
            
            child_text_el = Text(
                id=str(uuid.uuid4()),
                x=child_x - child_width/2 + 5,
                y=child_y - 10,
                width=child_width - 10,
                height=20,
                text=child_text,
                fontSize=16,
                textAlign="center",
                strokeColor=theme_colors["stroke"]
            )
            child_text_el.x = child_x - (len(child_text) * 8) / 2
            elements.append(child_text_el)
            
            child_node.groupIds = [child_id]
            child_text_el.groupIds = [child_id]
            
            arrow = Arrow(
                id=str(uuid.uuid4()),
                x=center_x,
                y=center_y,
                width=abs(child_x - center_x),
                height=abs(child_y - center_y),
                strokeColor=theme_colors["line"],
                points=[[0, 0], [child_x - center_x, child_y - center_y]],
                startBinding={"elementId": root_node.id, "focus": 0.5, "gap": 5},
                endBinding={"elementId": child_node.id, "focus": 0.5, "gap": 5},
                endArrowhead="arrow"
            )
            elements.append(arrow)
            
        return elements


class ExcalidrawGenerator:
    """Excalidraw diagram generator."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = data_dir
        self.templates = {
            "flowchart": FlowchartTemplate(),
            "architecture": ArchitectureTemplate(),
            "mindmap": MindmapTemplate(),
        }
    
    def generate_diagram(
        self, 
        description: str, 
        diagram_type: str = "flowchart",
        theme: str = "modern"
    ) -> Dict[str, Any]:
        """Generate Excalidraw diagram"""
        if diagram_type not in self.templates:
            raise ValueError(f"Unsupported diagram type: {diagram_type}")
        
        template = self.templates[diagram_type]
        elements = template.generate_elements(description, theme)
        
        excalidraw_elements = []
        for element in elements:
            excalidraw_elements.append(self._element_to_dict(element))
        
        diagram = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": excalidraw_elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff",
                "currentItemStrokeColor": "#1971c2",
                "currentItemBackgroundColor": "#a5d8ff",
                "currentItemFillStyle": "solid",
                "currentItemStrokeWidth": 2,
                "currentItemStrokeStyle": "solid",
                "currentItemRoughness": 1,
                "currentItemOpacity": 100,
                "currentItemFontFamily": 1,
                "currentItemFontSize": 20,
                "currentItemTextAlign": "left",
                "currentItemStartArrowhead": None,
                "currentItemEndArrowhead": "arrow",
                "scrollX": 0,
                "scrollY": 0,
                "zoom": {"value": 1}
            },
            "files": {}
        }
        
        return diagram
    
    def _element_to_dict(self, element: ExcalidrawElement) -> Dict[str, Any]:
        """Convert element to dictionary format"""
        result = {
            "id": element.id,
            "type": element.type,
            "x": element.x,
            "y": element.y,
            "width": element.width,
            "height": element.height,
            "angle": element.angle,
            "strokeColor": element.strokeColor,
            "backgroundColor": element.backgroundColor,
            "fillStyle": element.fillStyle,
            "strokeWidth": element.strokeWidth,
            "strokeStyle": element.strokeStyle,
            "roughness": element.roughness,
            "opacity": element.opacity,
            "groupIds": element.groupIds,
            "seed": hash(element.id) % 1000,
            "versionNonce": hash(element.id + "nonce") % 1000,
            "isDeleted": False,
        }
        
        if isinstance(element, Text):
            result.update({
                "text": element.text,
                "fontSize": element.fontSize,
                "fontFamily": element.fontFamily,
                "textAlign": element.textAlign,
                "verticalAlign": element.verticalAlign,
                "containerId": None,
                "originalText": element.text,
            })
        elif isinstance(element, Arrow):
            result.update({
                "points": element.points,
                "lastCommittedPoint": element.points[-1] if element.points else [0, 0],
                "startBinding": element.startBinding,
                "endBinding": element.endBinding,
                "startArrowhead": element.startArrowhead,
                "endArrowhead": element.endArrowhead,
            })
        
        return result


def format_diagram_info(diagram: Dict[str, Any]) -> str:
    """Format diagram information"""
    elements = diagram.get("elements", [])
    element_count = len(elements)
    
    types = {}
    for element in elements:
        elem_type = element.get("type", "unknown")
        types[elem_type] = types.get(elem_type, 0) + 1
    
    output = []
    output.append(f"🎨 Generated diagram contains {element_count} elements:")
    for elem_type, count in types.items():
        output.append(f"  • {elem_type}: {count}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Excalidraw diagrams from natural language descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "User login -> Verify -> Access data" --type flowchart
  %(prog)s "API Gateway -> Service -> Database" --type architecture
  %(prog)s --project . --type architecture
  %(prog)s "System overview" --theme modern --output diagram.json
  %(prog)s --interactive
        """,
    )
    
    parser.add_argument("description", nargs="?", help="图表描述")
    parser.add_argument("--project", help="Analyze a Python project and generate an architecture diagram")
    parser.add_argument("--focus", choices=["backend", "all"], default="backend", help="Focus area for project analysis")
    parser.add_argument("--use-ty", action="store_true", help="Include Astral ty metadata if available")
    parser.add_argument("--type", "-t", choices=["flowchart", "architecture", "mindmap"], 
                       default="flowchart", help="图表类型")
    parser.add_argument("--theme", choices=["modern", "sketchy", "technical", "colorful"],
                       default="modern", help="图表主题")
    parser.add_argument("--output", "-o", help="输出文件名")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式生成")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    generator = ExcalidrawGenerator()
    
    if args.project:
        graph = analyze_python_project_to_graph(args.project, focus=args.focus, use_ty=args.use_ty)
        if args.type != "architecture":
            raise SystemExit("Project analysis currently supports only --type architecture")

        elements = generator.templates["architecture"].generate_elements_from_graph(graph, args.theme)
        diagram = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": [generator._element_to_dict(el) for el in elements],
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff",
                "currentItemStrokeColor": "#1971c2",
                "currentItemBackgroundColor": "#a5d8ff",
                "currentItemFillStyle": "solid",
                "currentItemStrokeWidth": 2,
                "currentItemStrokeStyle": "solid",
                "currentItemRoughness": 1,
                "currentItemOpacity": 100,
                "currentItemFontFamily": 1,
                "currentItemFontSize": 20,
                "currentItemTextAlign": "left",
                "currentItemStartArrowhead": None,
                "currentItemEndArrowhead": "arrow",
                "scrollX": 0,
                "scrollY": 0,
                "zoom": {"value": 1},
            },
            "files": {},
        }

        output_file = args.output or f"diagram_project_{args.type}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(diagram, f, indent=2, ensure_ascii=False)
        print(f"✅ Diagram generated: {output_file}")
        print("🌐 Import it at https://excalidraw.com")
        return

    if args.interactive:
        print("🎨 Excalidraw diagram generator (interactive)")
        print("=" * 50)
        
        while True:
            description = input("\nDescribe the diagram (type 'quit' to exit): ")
            if description.lower() in ['quit', 'q', '退出']:
                break
            
            diagram_type = input("Diagram type (flowchart/architecture/mindmap) [flowchart]: ").strip()
            if not diagram_type:
                diagram_type = "flowchart"
            
            theme = input("Theme (modern/sketchy/technical/colorful) [modern]: ").strip()
            if not theme:
                theme = "modern"
            
            try:
                diagram = generator.generate_diagram(description, diagram_type, theme)
                
                if args.verbose:
                    print(format_diagram_info(diagram))
                
                output_file = f"diagram_{len(description)}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(diagram, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Diagram generated: {output_file}")
                print("🌐 Import it at https://excalidraw.com")
                
            except Exception as e:
                print(f"❌ Generation failed: {e}")
        
        return
    
    if not args.description:
        parser.print_help()
        sys.exit(1)
    
    try:
        diagram = generator.generate_diagram(args.description, args.type, args.theme)
        
        if args.verbose:
            print(format_diagram_info(diagram))
        
        output_file = args.output or f"diagram_{args.type}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(diagram, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Diagram generated: {output_file}")
        print("🌐 Import it at https://excalidraw.com")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()