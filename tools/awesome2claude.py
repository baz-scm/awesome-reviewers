#!/usr/bin/env python3
"""CLI for converting AwesomeReviewers prompts into Claude Skills."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple

import click
import yaml


REVIEWERS_DIR = "_reviewers"
DEFAULT_REPO_URL = "https://github.com/baz-scm/awesome-reviewers.git"
DEFAULT_REPO_DIR = "awesome-reviewers"
DEFAULT_VERSION = "1.0"
SCRIPT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Prompt:
    path: Path
    metadata: dict
    body: str

    @property
    def title(self) -> str:
        meta_title = self.metadata.get("title") or self.metadata.get("name")
        if meta_title:
            return str(meta_title)
        return self.path.stem.replace("-", " ").title()

    @property
    def category(self) -> Optional[str]:
        category = self.metadata.get("category") or self.metadata.get("Category")
        return str(category) if category else None

    @property
    def slug(self) -> str:
        title = self.title.strip()
        if not title:
            title = "untitled"
        normalized = unicodedata.normalize("NFKD", title)
        ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^0-9a-zA-Z]+", "-", ascii_only).strip("-").lower()
        return slug or "untitled"

    @property
    def description(self) -> str:
        for key in ("description", "excerpt", "summary"):
            value = self.metadata.get(key)
            if value:
                return _clean_description(str(value))
        # Fallback: first paragraph of body
        body = self.body.strip()
        if not body:
            return self.title
        first_para, _ = _split_first_paragraph(body)
        cleaned = _clean_description(first_para)
        return cleaned if cleaned else self.title


@dataclass
class SkillArtifact:
    prompt: Prompt
    description: str
    skill_dir: Path
    skill_file: Path

    def build_frontmatter(self) -> str:
        data = {
            "name": self.prompt.slug,
            "description": self.description,
            "version": DEFAULT_VERSION,
        }
        yaml_text = yaml.safe_dump(data, sort_keys=False).rstrip()
        return f"---\n{yaml_text}\n---\n"

    def build_body(self) -> str:
        body = self.prompt.body.strip()
        if body:
            return f"# {self.prompt.title}\n\n{body}\n"
        return f"# {self.prompt.title}\n\n"

    def render(self) -> str:
        return f"{self.build_frontmatter()}{self.build_body()}"


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--output-dir",
    "output_dir",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Directory where Claude skills will be generated.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing skill directories if they already exist.",
)
@click.option(
    "--single",
    type=str,
    default=None,
    metavar="FILENAME",
    help="Convert a single prompt file from _reviewers (optionally omit .md).",
)
@click.option(
    "--group-by-category",
    is_flag=True,
    default=False,
    help="Group generated skills by category subdirectories.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview the generated skills without writing any files.",
)
@click.option(
    "--repo-url",
    default=DEFAULT_REPO_URL,
    show_default=True,
    help="Git repository URL for AwesomeReviewers.",
)
@click.option(
    "--repo-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path(DEFAULT_REPO_DIR),
    show_default=True,
    help="Local directory used for the AwesomeReviewers repository clone.",
)
@click.option(
    "--limit",
    type=click.IntRange(1, None),
    default=None,
    metavar="N",
    help="Process at most N prompts (after sorting).",
)
def convert_reviewers(
    output_dir: Path,
    overwrite: bool,
    single: Optional[str],
    group_by_category: bool,
    dry_run: bool,
    repo_url: str,
    repo_dir: Path,
    limit: Optional[int],
) -> None:
    """Convert AwesomeReviewers prompts into Claude Skills."""
    repo_dir = repo_dir.expanduser()
    if repo_dir == Path(DEFAULT_REPO_DIR):
        local_repo = SCRIPT_ROOT
        if (local_repo / REVIEWERS_DIR).is_dir():
            repo_dir = local_repo
    repo_dir = repo_dir.resolve()
    output_dir = output_dir.expanduser().resolve()

    if not _ensure_repo(repo_dir, repo_url):
        raise SystemExit(1)

    reviewers_dir = repo_dir / REVIEWERS_DIR
    if not reviewers_dir.is_dir():
        click.echo(f"Error: '{REVIEWERS_DIR}' directory not found in {repo_dir}.", err=True)
        raise SystemExit(1)

    prompt_paths = _collect_prompt_paths(reviewers_dir, single, limit)
    if not prompt_paths:
        click.echo("No prompts found to process.")
        return

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for path in prompt_paths:
        prompt = _load_prompt(path)
        if not prompt:
            continue

        description = prompt.description
        skill_dir = _determine_skill_dir(output_dir, prompt, group_by_category)
        skill_file = skill_dir / "SKILL.md"
        artifact = SkillArtifact(prompt, description, skill_dir, skill_file)

        if dry_run:
            _print_dry_run(artifact)
            continue

        if artifact.skill_dir.exists():
            if not overwrite:
                click.echo(
                    f"Skipping existing skill directory: {artifact.skill_dir} (use --overwrite to replace)."
                )
                continue
            shutil.rmtree(artifact.skill_dir)

        artifact.skill_dir.mkdir(parents=True, exist_ok=True)
        try:
            artifact.skill_file.write_text(artifact.render(), encoding="utf-8")
        except OSError as exc:
            click.echo(f"Error: Failed to write {artifact.skill_file}: {exc}", err=True)
            continue

        click.echo(f"Generated skill: {artifact.skill_file}")

    if dry_run:
        click.echo("Done. (Dry-run mode: no files written.)")
    else:
        click.echo("Done.")


def _ensure_repo(repo_dir: Path, repo_url: str) -> bool:
    if repo_dir.exists():
        if not (repo_dir / ".git").is_dir():
            click.echo(
                f"Error: {repo_dir} exists but is not a git repository. Specify a different --repo-dir.",
                err=True,
            )
            return False
        return _git_pull(repo_dir)
    return _git_clone(repo_dir, repo_url)


def _git_clone(repo_dir: Path, repo_url: str) -> bool:
    click.echo(f"Cloning repository from {repo_url} ...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(repo_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        click.echo(f"Error: Git clone failed: {exc}", err=True)
        return False
    return True


def _git_pull(repo_dir: Path) -> bool:
    click.echo(f"Updating repository in {repo_dir} (git pull)...")
    try:
        subprocess.run(
            ["git", "-C", str(repo_dir), "pull"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        click.echo(
            f"Warning: Git pull failed for {repo_dir}: {exc}. Proceeding with the existing checkout.",
            err=True,
        )
        return True
    return True


def _collect_prompt_paths(
    reviewers_dir: Path, single: Optional[str], limit: Optional[int]
) -> Iterable[Path]:
    if single:
        filename = single if single.endswith(".md") else f"{single}.md"
        path = reviewers_dir / filename
        if not path.is_file():
            click.echo(f"Error: Specified file '{filename}' not found in {reviewers_dir}.", err=True)
            return []
        return [path]

    paths = sorted(p for p in reviewers_dir.glob("*.md") if p.is_file())
    if limit is not None:
        return paths[:limit]
    return paths


def _load_prompt(path: Path) -> Optional[Prompt]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        click.echo(f"Warning: Could not read {path}: {exc}", err=True)
        return None

    frontmatter, body = _split_frontmatter(content)
    if frontmatter is None:
        click.echo(f"Skipping {path}: No valid YAML front-matter found.")
        return None

    try:
        metadata = yaml.safe_load(frontmatter) or {}
        if not isinstance(metadata, dict):
            raise TypeError("YAML front-matter must be a mapping")
    except Exception as exc:  # noqa: BLE001 - broad to report YAML issues
        click.echo(f"Warning: Failed to parse YAML in {path}: {exc}", err=True)
        return None

    return Prompt(path=path, metadata=metadata, body=body)


def _split_frontmatter(content: str) -> Tuple[Optional[str], str]:
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return None, content

    parts = re.split(r"^---\s*$", stripped, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return None, content

    # parts will look like: ['', '<yaml>', '\n<body>'] when the front-matter is valid
    _, frontmatter, body = parts
    body = body.lstrip("\r\n")
    return frontmatter.strip(), body


def _split_first_paragraph(text: str) -> Tuple[str, str]:
    paragraphs = text.split("\n\n", 1)
    first = paragraphs[0]
    remainder = paragraphs[1] if len(paragraphs) > 1 else ""
    return first.strip(), remainder


def _determine_skill_dir(output_dir: Path, prompt: Prompt, group_by_category: bool) -> Path:
    if group_by_category and prompt.category:
        return output_dir / prompt.category / prompt.slug
    return output_dir / prompt.slug


def _print_dry_run(artifact: SkillArtifact) -> None:
    click.echo(
        textwrap.dedent(
            f"""\
            [DRY-RUN] Would generate skill '{artifact.prompt.slug}' from '{artifact.prompt.path.name}':
                Title: {artifact.prompt.title}
                Description: {artifact.description}
                Category: {artifact.prompt.category or 'None'}
                Output path: {artifact.skill_file}
            """
        ).rstrip()
    )


def _clean_description(value: str) -> str:
    without_links = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", value)
    without_newlines = re.sub(r"\s+", " ", without_links)
    return without_newlines.strip()


if __name__ == "__main__":
    try:
        convert_reviewers(standalone_mode=False)
    except SystemExit as exc:
        raise
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)
