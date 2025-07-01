from pathlib import Path
from .base import BaseWriter

class ClaudeWriter(BaseWriter):
    ext = '.md'
    prefix = 'claude_'

    def write(self, reviewers, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for r in reviewers:
            title = r.get('title')
            if not title:
                continue
            slug = title.lower().replace(' ', '_')
            path = output_dir / f"{self.prefix}{slug}{self.ext}"
            content = r.get('system_prompt') or ''
            if r.get('goals'):
                content += '\n\n## Goals\n' + r['goals']
            if r.get('labels'):
                content += '\n\n## Labels\n' + r['labels']
            path.write_text(content)
