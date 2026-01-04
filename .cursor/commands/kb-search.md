# kb-search

Search Python backend best practices from the knowledge base.

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

## Examples

- `/kb-search async routes`
- `/kb-search jwt authentication`
