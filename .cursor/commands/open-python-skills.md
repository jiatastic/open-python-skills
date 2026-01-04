# open-python-skills

Search and use Python backend best practices from the knowledge base.

## Instructions

1. Search knowledge database:
   ```bash
   python3 .shared/scripts/knowledge_db.py "{{query}}"
   ```

2. Filter by category:
   ```bash
   python3 .shared/scripts/knowledge_db.py "{{query}}" --category {{category}}
   ```

3. Get full entry with code examples:
   ```bash
   python3 .shared/scripts/knowledge_db.py --get {{entry-id}}
   ```

## Discover Categories / Tags

```bash
python3 .shared/scripts/knowledge_db.py --list-categories
python3 .shared/scripts/knowledge_db.py --list-tags
```

## Knowledge Database

- `.shared/data/*.json` (multiple databases; loaded automatically)

## Examples

- `/open-python-skills async routes`
- `/open-python-skills jwt authentication`
- `/open-python-skills pydantic validation`
- `/open-python-skills database connection pooling`
