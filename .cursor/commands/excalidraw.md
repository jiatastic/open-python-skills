# excalidraw

Generate Excalidraw diagram from text.

## Instructions

1. Generate diagram:
   ```bash
   python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "description" --type flowchart
   ```

2. Generate a backend architecture diagram from the current Python project:
   ```bash
   python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --output diagram_architecture.json
   ```

## Examples

- `/excalidraw "User login flow" --type flowchart`
- `/excalidraw --project . --type architecture`
