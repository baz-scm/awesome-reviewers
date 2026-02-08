#!/usr/bin/env python3
"""Audit AwesomeReviewers prompts for agent-skill readiness.

The report focuses on practical traits that make prompts easier for coding agents
to execute consistently:
- clear trigger and scope language
- imperative guideline style
- actionable checklist formatting
- explicit response/output expectations
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from statistics import median
from typing import Iterable

RE_IMPERATIVE_START = re.compile(
    r"^(avoid|use|ensure|prefer|document|validate|keep|add|remove|check|guard|extract|name)\b",
    re.IGNORECASE,
)
RE_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_body(markdown: str) -> str:
    match = RE_FRONTMATTER.match(markdown)
    if not match:
        return markdown.strip()
    return markdown[match.end() :].strip()


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _collect_markdown_stats(paths: Iterable[Path]) -> dict:
    total = 0
    has_examples = 0
    has_bullets = 0
    has_numbered = 0
    has_output_contract = 0
    imperative_opening = 0
    words = []

    for path in paths:
        total += 1
        raw = _read_text(path)
        body = _extract_body(raw)
        lower = body.lower()

        if "example" in lower:
            has_examples += 1
        if re.search(r"^\s*[-*]\s+", body, flags=re.MULTILINE):
            has_bullets += 1
        if re.search(r"^\s*\d+\.\s+", body, flags=re.MULTILINE):
            has_numbered += 1
        if any(
            token in lower
            for token in (
                "output format",
                "response format",
                "when reviewing",
                "when to apply",
                "return:",
                "reply with",
            )
        ):
            has_output_contract += 1

        first = _first_nonempty_line(body)
        if RE_IMPERATIVE_START.match(first):
            imperative_opening += 1

        words.append(len(re.findall(r"\b\w+\b", body)))

    if total == 0:
        return {}

    return {
        "markdown_total": total,
        "has_examples": has_examples,
        "has_bullets": has_bullets,
        "has_numbered": has_numbered,
        "has_output_contract": has_output_contract,
        "imperative_opening": imperative_opening,
        "median_word_count": int(median(words)),
        "very_short_under_80_words": sum(1 for w in words if w < 80),
        "very_long_over_500_words": sum(1 for w in words if w > 500),
    }


def _collect_json_stats(paths: Iterable[Path]) -> dict:
    total = 0
    parse_failures = 0
    entries = 0
    comments = 0
    authors = Counter()

    for path in paths:
        total += 1
        try:
            payload = json.loads(_read_text(path))
        except json.JSONDecodeError:
            parse_failures += 1
            continue

        if isinstance(payload, list):
            entries += len(payload)
            for item in payload:
                for comment in item.get("discussion_comments", []) if isinstance(item, dict) else []:
                    comments += 1
                    author = comment.get("comment_author")
                    if author:
                        authors[str(author)] += 1

    return {
        "json_total": total,
        "json_parse_failures": parse_failures,
        "json_discussions": entries,
        "json_comments": comments,
        "top_comment_authors": authors.most_common(10),
    }


def build_report(reviewers_dir: Path) -> str:
    md_paths = sorted(reviewers_dir.glob("*.md"))
    json_paths = sorted(reviewers_dir.glob("*.json"))

    md = _collect_markdown_stats(md_paths)
    js = _collect_json_stats(json_paths)

    md_total = md.get("markdown_total", 1)
    report = [
        "# Reviewer Skill Readiness Audit",
        "",
        f"- Markdown prompts: **{md.get('markdown_total', 0)}**",
        f"- JSON reviewer datasets: **{js.get('json_total', 0)}**",
        "",
        "## Current quality snapshot",
        "",
        f"- Prompts with examples: **{md.get('has_examples', 0)}** ({md.get('has_examples', 0)/md_total:.1%})",
        f"- Prompts with bullet lists: **{md.get('has_bullets', 0)}** ({md.get('has_bullets', 0)/md_total:.1%})",
        f"- Prompts with numbered steps: **{md.get('has_numbered', 0)}** ({md.get('has_numbered', 0)/md_total:.1%})",
        f"- Prompts with explicit output/response contract keywords: **{md.get('has_output_contract', 0)}** ({md.get('has_output_contract', 0)/md_total:.1%})",
        f"- Prompts whose first line starts with an imperative verb: **{md.get('imperative_opening', 0)}** ({md.get('imperative_opening', 0)/md_total:.1%})",
        f"- Median prompt length: **{md.get('median_word_count', 0)} words**",
        f"- Very short prompts (<80 words): **{md.get('very_short_under_80_words', 0)}**",
        f"- Very long prompts (>500 words): **{md.get('very_long_over_500_words', 0)}**",
        "",
        "## Why this matters for agent skills",
        "",
        "Agent skills work best when prompts include clear trigger conditions, deterministic checklist-style actions, and an expected response format. The current corpus is strong on examples, but weaker on explicit execution contracts (what an agent should output) and standardized structure.",
        "",
        "## Recommended improvements",
        "",
        "1. **Standardize a skill wrapper section during export**",
        "   - Inject sections like `When to apply`, `Review checklist`, and `Expected output` when converting to SKILL.md.",
        "   - Keep original reviewer text under `Source guidance` to preserve nuance.",
        "2. **Introduce an optional strict mode linter**",
        "   - Fail if prompt lacks imperative guidance, bullets/checklist, or output contract.",
        "3. **Segment by prompt length**",
        "   - Split very long prompts into concise must-follow rules + optional rationale.",
        "4. **Leverage JSON datasets for synthesis**",
        "   - Mine recurring comment patterns and auto-generate candidate checklist statements to backfill weak prompts.",
        "5. **Add confidence metadata**",
        "   - Include metadata like `evidence_count` and `source_repos` in generated skills to help agents prioritize stronger signals.",
        "",
        "## JSON dataset signal",
        "",
        f"- Parsed discussion records: **{js.get('json_discussions', 0)}**",
        f"- Parsed review comments: **{js.get('json_comments', 0)}**",
        f"- Parse failures: **{js.get('json_parse_failures', 0)}**",
    ]

    top = js.get("top_comment_authors", [])
    if top:
        report.append("- Top reviewer authors in JSON samples:")
        for author, count in top:
            report.append(f"  - `{author}`: {count}")

    return "\n".join(report) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reviewers-dir",
        type=Path,
        default=Path("_reviewers"),
        help="Path to the _reviewers directory.",
    )
    parser.add_argument(
        "--write-report",
        type=Path,
        default=None,
        help="Optional output markdown file path.",
    )
    args = parser.parse_args()

    report = build_report(args.reviewers_dir)
    if args.write_report:
        args.write_report.write_text(report, encoding="utf-8")
        print(f"Wrote audit report to {args.write_report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
