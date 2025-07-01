import json
from pathlib import Path
from .base import BaseWriter

class AugmentWriter(BaseWriter):
    def write(self, reviewers, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        data = {r['title']: r.get('system_prompt') for r in reviewers if r.get('title')}
        path = output_dir / 'augment_reviewers.json'
        path.write_text(json.dumps(data, indent=2))
