from pathlib import Path
from .base import BaseWriter
import json

class CodexWriter(BaseWriter):
    def write(self, reviewers, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        items = {r['title']: r.get('system_prompt') for r in reviewers if r.get('title')}
        lines = ["export const reviewers = "+json.dumps(items, indent=2)+";\n"]
        path = output_dir / 'reviewers.ts'
        path.write_text("\n".join(lines))
