# open-python-skills

Search and use Python backend best practices from the knowledge base.

## Instructions

1. Search knowledge database:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py "{{query}}"
   ```

2. Filter by category:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py "{{query}}" --category {{category}}
   ```

3. Get full entry with code examples:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py --get {{entry-id}}
   ```

## Available Categories

Use `--list-categories` to discover all categories.

## Knowledge Database

- `.shared/python-backend/data/*.json` (multiple databases; incremental and searchable)

## Examples

- `/open-python-skills async routes`
- `/open-python-skills jwt authentication`
- `/open-python-skills pydantic validation`
- `/open-python-skills database connection pooling`
