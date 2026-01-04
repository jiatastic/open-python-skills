# Claude Code Commands

## open-python-skills

### Available Commands

#### Search Knowledge Database
```bash
# Search entries
python3 .shared/scripts/knowledge_db.py "async routes"

# Filter by category
python3 .shared/scripts/knowledge_db.py "validation" --category pydantic

# Get full entry with code
python3 .shared/scripts/knowledge_db.py --get async-routes-io

# List all categories
python3 .shared/scripts/knowledge_db.py --list-categories

# List all tags
python3 .shared/scripts/knowledge_db.py --list-tags

# Show stats
python3 .shared/scripts/knowledge_db.py --stats
```
