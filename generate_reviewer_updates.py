#!/usr/bin/env python3
"""Generate aggregated reviewer metadata for freshness indicators.

This script scans all reviewer discussion JSON files stored in the
``_reviewers`` directory and computes the timestamp of the most recent
code review comment for each reviewer. The output is a JSON file that can
be consumed on the client to display freshness information and enable
sorting/filtering by last update time.

Usage::
    python generate_reviewer_updates.py

The generated file is written to ``assets/data/reviewer-updates.json``.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional

REVIEWERS_DIR = Path('_reviewers')
OUTPUT_PATH = Path('assets/data/reviewer-updates.json')


@dataclass
class ReviewerUpdate:
    slug: str
    last_comment_at: Optional[datetime]

    def to_dict(self) -> dict:
        timestamp_ms: Optional[int] = None
        iso_timestamp: Optional[str] = None
        if self.last_comment_at is not None:
            dt = self.last_comment_at.astimezone(timezone.utc)
            timestamp_ms = int(dt.timestamp() * 1000)
            iso_timestamp = dt.isoformat()
        return {
            'slug': self.slug,
            'last_comment_at': iso_timestamp,
            'last_comment_timestamp': timestamp_ms,
        }


def parse_comment_timestamp(raw: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(raw)
    except Exception:
        return None


def iter_reviewer_files() -> Iterable[Path]:
    if not REVIEWERS_DIR.exists():
        raise FileNotFoundError(f'Reviewers directory not found: {REVIEWERS_DIR}')
    for path in sorted(REVIEWERS_DIR.glob('*.json')):
        # Skip potential non-discussion JSON such as aggregated files
        if path.name == 'reviewer-updates.json':
            continue
        yield path


def extract_last_comment(path: Path) -> ReviewerUpdate:
    slug = path.stem
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise ValueError(f'Failed to parse JSON for {slug}: {exc}') from exc

    latest: Optional[datetime] = None

    if isinstance(payload, list):
        for discussion in payload:
            if not isinstance(discussion, dict):
                continue
            # Consider individual discussion comments first
            comments = discussion.get('discussion_comments') or []
            for comment in comments:
                if not isinstance(comment, dict):
                    continue
                raw = comment.get('comment_created_at')
                ts = parse_comment_timestamp(raw) if raw else None
                if ts is not None and (latest is None or ts > latest):
                    latest = ts
            # Fallback to discussion level created_at when no nested comments
            if latest is None:
                raw_discussion = discussion.get('created_at')
                ts_discussion = parse_comment_timestamp(raw_discussion) if raw_discussion else None
                if ts_discussion is not None and (latest is None or ts_discussion > latest):
                    latest = ts_discussion
    else:
        raise ValueError(f'Unexpected payload structure in {path}')

    return ReviewerUpdate(
        slug=slug,
        last_comment_at=latest,
    )


def build_updates() -> List[ReviewerUpdate]:
    updates: List[ReviewerUpdate] = []
    for path in iter_reviewer_files():
        try:
            updates.append(extract_last_comment(path))
        except Exception as exc:
            print(exc, file=sys.stderr)
    updates.sort(key=lambda item: (item.last_comment_at or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
    return updates


def main() -> None:
    updates = build_updates()
    data = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'reviewers': [update.to_dict() for update in updates],
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f'Wrote {len(updates)} reviewer freshness records to {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
