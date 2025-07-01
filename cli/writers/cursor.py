import json
from pathlib import Path
from .base import BaseWriter

class CursorWriter(BaseWriter):
    def write(self, reviewers, output_dir):
        output_dir = Path(output_dir) / '.cursor'
        output_dir.mkdir(parents=True, exist_ok=True)
        rules_file = output_dir / 'rules.json'
        data = {}
        if rules_file.exists():
            try:
                data = json.loads(rules_file.read_text())
            except Exception:
                pass
        for r in reviewers:
            title = r.get('title')
            if not title:
                continue
            data[title] = {
                'system_prompt': r.get('system_prompt'),
                'goals': r.get('goals'),
                'labels': r.get('labels'),
                'description': r.get('description')
            }
        rules_file.write_text(json.dumps(data, indent=2))
