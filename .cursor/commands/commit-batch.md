# commit-batch

Analyze git changes and suggest batch commits.

## Instructions

1. Analyze all changes:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --analyze
   ```

2. Get batch commit suggestions:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --batch
   ```

3. Generate message for specific files:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --generate "*.py"
   ```

## Examples

- `/commit-batch` - Suggest how to split changes into commits
