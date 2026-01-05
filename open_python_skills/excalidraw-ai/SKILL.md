---
name: excalidraw-ai
description: >
  AI-powered professional Excalidraw diagram generator with a rich component library.
  Use when: (1) Creating flowcharts from text, (2) Generating architecture diagrams
  with a professional look, (3) Building mind maps, (4) Designing system workflows,
  (5) Creating technical documentation visuals, or (6) Converting complex ideas into visuals.
  Features automatic component type detection, rich color palettes, and library icon support.
---

# excalidraw-ai

AI-powered professional Excalidraw diagram generator with intelligent component detection and extensive library icon support.

## ✨ Features

- **🎨 Professional color palettes** - Each component type has a unique color scheme (e.g., Database = purple, Cache = red, Queue = green, etc.)
- **🧠 Smart Component Recognition** - Automatically detects the type of each component (e.g., "Redis" → cache, "PostgreSQL" → database)
- **📚 Library Icon Support** - Uses professional icons from `.excalidrawlib` files
- **🏗️ Multi-layer Architecture Layouts** - Automatically arranges components in architectural layers (Client → Gateway → Service → Database)
- **🏷️ Type Badges** - Optionally displays component type badges (e.g., "🗄️ DB", "⚡ Cache")

## Usage

```bash
# 🌟 Professional architecture diagram (auto-detects and colors components)
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  "Load Balancer -> API Gateway -> Redis Cache -> PostgreSQL" \
  --type architecture --style pro

# Complete system architecture
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  "CDN -> Nginx -> FastAPI Service -> Kafka Queue -> MongoDB" \
  --type architecture --style pro --output system_arch.json

# Basic flowchart
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  "User Login -> Verify -> Access Data" --type flowchart

# Hand-drawn style architecture diagram
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  "API Gateway -> Microservice -> Database" --type architecture --theme sketchy

# Mind map
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  "Python Development: FastAPI, SQLAlchemy, Redis, Celery" --type mindmap

# ✅ Auto-generate backend architecture from a Python project
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py \
  --project . --type architecture --style pro --output backend_arch.json

# See supported component types
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --list-types

# Interactive mode
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --interactive
```

## 🎨 Supported Component Types & Colors

| Component Type   | Keywords                              | Border Color | Fill Color |
|------------------|---------------------------------------|--------------|------------|
| **Database**     | database, postgres, mysql, mongodb    | Purple       | Light purple |
| **Cache**        | redis, cache, memcached               | Red          | Light red    |
| **Message Queue**| kafka, rabbitmq, queue, sqs           | Green        | Light green  |
| **Load Balancer**| load balancer, nginx, elb             | Teal         | Light teal   |
| **Gateway**      | gateway, kong, apigee                 | Gray         | Light gray   |
| **CDN**          | cdn, cloudfront, edge                 | Sky Blue     | Light blue   |
| **Auth**         | auth, iam, oauth                      | Rose         | Light pink   |
| **Storage**      | s3, storage, blob                     | Amber        | Light yellow |
| **Service**      | service, api, backend                 | Blue         | Light blue   |
| **Container**    | docker, kubernetes, k8s               | Blue         | Light blue   |
| **Function**     | lambda, function, serverless          | Orange       | Light orange |
| **Monitoring**   | prometheus, grafana, monitor          | Lime         | Light green  |

## Supported Diagram Types

- `flowchart` - Flowcharts
- `architecture` - Architecture diagrams (with `--style pro` for advanced coloring)
- `mindmap` - Mind maps

## Themes

- `modern` - Minimalistic modern style
- `sketchy` - Hand-drawn look
- `technical` - Documentation/technical style
- `colorful` - Vivid, colorful style

## Style Options

- `pro` - Professional palette, unique colors per component type (default)
- `basic` - Theme-based uniform coloring

## Output

Generated diagrams can be:
- Imported directly into [Excalidraw.com](https://excalidraw.com)
- Integrated into web apps via API
- Exported as PNG/SVG images
- Embedded in Markdown documentation

## 📚 Library Support

You can load component icons from `.excalidrawlib` files:

- `software-architecture.excalidrawlib` - Software architecture icons
- `system-design.excalidrawlib` - System design elements
- `system-design-template.excalidrawlib` - System design templates
- `drwnio.excalidrawlib` - Draw.io style icon set
- `aws-architecture-icons.excalidrawlib` - AWS architecture icons

## Key Capabilities

1. **Text-to-Diagram** - Generate professional diagrams from natural language descriptions
2. **Intelligent Component Detection** - Auto-detect and classify components and style them accordingly
3. **Professional Color Schemes** - Rich palettes based on component type
4. **Python Project Analysis** - Scan code to generate backend architecture diagrams (`--project`)
5. **Optional ty Metadata** - Integrate summary output from Astral `ty` type checking (`--use-ty`)
6. **Multiple Visual Themes** - Choose from modern, sketchy, technical, or colorful themes
7. **Interactive Editing** - Supports iterative, interactive editing

## Example Output

```
✅ Diagram generated: diagram_architecture.json
📊 Elements: 24
🌐 Import it at https://excalidraw.com
```
