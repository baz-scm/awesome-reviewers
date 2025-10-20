#!/usr/bin/env python3
"""CLI for converting AwesomeReviewers prompts into Claude Skills."""
from __future__ import annotations

import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import click
import yaml

try:  # Python 3.11+
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - fallback for <3.11
    try:
        import tomli as tomllib  # type: ignore[assignment]
    except ModuleNotFoundError:  # pragma: no cover - tomli not installed
        tomllib = None  # type: ignore[assignment]


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
        slug_override = self.metadata.get("slug")
        if slug_override:
            return _slugify_text(str(slug_override))
        title = self.title.strip()
        if not title:
            title = "untitled"
        return _slugify_text(title)

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
@click.option(
    "--project-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Optional project directory to scan for package manager files. When provided,"
    " a combined skill will be generated for dependencies with matching Awesome"
    " Reviewers prompts.",
)
@click.option(
    "--combined-skill-slug",
    type=str,
    default="project-dependencies",
    show_default=True,
    help="Directory/slug to use for the combined skill generated from detected dependencies.",
)
@click.option(
    "--combined-skill-title",
    type=str,
    default="Project Dependency Reviewers",
    show_default=True,
    help="Title for the combined skill generated from detected dependencies.",
)
@click.option(
    "--combined-skill-description",
    type=str,
    default=None,
    help="Optional description for the combined skill. If omitted, a description will"
    " be generated from the matched dependencies.",
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
    project_dir: Optional[Path],
    combined_skill_slug: str,
    combined_skill_title: str,
    combined_skill_description: Optional[str],
) -> None:
    """Convert AwesomeReviewers prompts into Claude Skills."""
    repo_dir = repo_dir.expanduser()
    if repo_dir == Path(DEFAULT_REPO_DIR):
        local_repo = SCRIPT_ROOT
        if (local_repo / REVIEWERS_DIR).is_dir():
            repo_dir = local_repo
    repo_dir = repo_dir.resolve()
    output_dir = output_dir.expanduser().resolve()
    if project_dir is not None:
        project_dir = project_dir.expanduser()

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

    prompts: List[Prompt] = []
    for path in prompt_paths:
        prompt = _load_prompt(path)
        if prompt:
            prompts.append(prompt)

    for prompt in prompts:
        description = prompt.description
        skill_dir = _determine_skill_dir(output_dir, prompt, group_by_category)
        skill_file = skill_dir / "SKILL.md"
        artifact = SkillArtifact(prompt, description, skill_dir, skill_file)
        _write_skill_artifact(artifact, overwrite=overwrite, dry_run=dry_run)

    if project_dir is not None:
        _generate_combined_skill(
            project_dir=project_dir,
            output_dir=output_dir,
            prompts=prompts,
            overwrite=overwrite,
            dry_run=dry_run,
            combined_skill_slug=combined_skill_slug,
            combined_skill_title=combined_skill_title,
            combined_skill_description=combined_skill_description,
        )

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


def _slugify_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^0-9a-zA-Z]+", "-", ascii_only).strip("-").lower()
    return slug or "untitled"


def _write_skill_artifact(artifact: SkillArtifact, overwrite: bool, dry_run: bool) -> None:
    if dry_run:
        _print_dry_run(artifact)
        return

    if artifact.skill_dir.exists():
        if not overwrite:
            click.echo(
                f"Skipping existing skill directory: {artifact.skill_dir} (use --overwrite to replace)."
            )
            return
        shutil.rmtree(artifact.skill_dir)

    artifact.skill_dir.mkdir(parents=True, exist_ok=True)
    try:
        artifact.skill_file.write_text(artifact.render(), encoding="utf-8")
    except OSError as exc:
        click.echo(f"Error: Failed to write {artifact.skill_file}: {exc}", err=True)
        return

    click.echo(f"Generated skill: {artifact.skill_file}")


def _generate_combined_skill(
    project_dir: Path,
    output_dir: Path,
    prompts: Sequence[Prompt],
    overwrite: bool,
    dry_run: bool,
    combined_skill_slug: str,
    combined_skill_title: str,
    combined_skill_description: Optional[str],
) -> None:
    project_dir = project_dir.expanduser().resolve()
    if not project_dir.is_dir():
        click.echo(
            f"Warning: Project directory '{project_dir}' not found. Skipping combined skill generation."
        )
        return

    dependencies = _scan_project_dependencies(project_dir)
    if not dependencies:
        click.echo(f"No package manager dependencies detected in {project_dir}.")
        return

    click.echo(f"Detected {len(dependencies)} unique dependency names in {project_dir}.")

    alias_map = _build_dependency_alias_map(dependencies)
    matched_prompts, dependency_to_prompts, prompt_matches = _match_prompts_with_dependencies(
        prompts, alias_map
    )

    if not matched_prompts:
        click.echo(
            "No Awesome Reviewers prompts matched the detected dependencies. Skipping combined skill generation."
        )
        return

    click.echo("Matched dependencies:")
    for dep in sorted(dependency_to_prompts):
        prompt_count = len(dependency_to_prompts[dep])
        click.echo(f"  - {dep} ({prompt_count} prompt{'s' if prompt_count != 1 else ''})")

    description = (
        combined_skill_description
        if combined_skill_description
        else _build_default_combined_description(dependency_to_prompts)
    )

    combined_metadata = {
        "title": combined_skill_title,
        "description": description,
        "slug": combined_skill_slug,
    }
    combined_body = _build_combined_skill_body(
        matched_prompts, dependency_to_prompts, prompt_matches
    )
    combined_prompt = Prompt(
        path=Path(f"{combined_skill_slug}.md"),
        metadata=combined_metadata,
        body=combined_body,
    )
    skill_dir = output_dir / combined_prompt.slug
    skill_file = skill_dir / "SKILL.md"
    artifact = SkillArtifact(combined_prompt, description, skill_dir, skill_file)
    _write_skill_artifact(artifact, overwrite=overwrite, dry_run=dry_run)


def _build_default_combined_description(
    dependency_to_prompts: Dict[str, Set[str]]
) -> str:
    if not dependency_to_prompts:
        return "Combined prompts for detected project dependencies."
    deps_sorted = sorted(dependency_to_prompts.keys())
    if len(deps_sorted) <= 5:
        joined = ", ".join(deps_sorted)
        return f"Combined prompts for project dependencies: {joined}."
    joined = ", ".join(deps_sorted[:5])
    remaining = len(deps_sorted) - 5
    plural = "s" if remaining != 1 else ""
    return f"Combined prompts for project dependencies: {joined}, and {remaining} other dependency{plural}."


def _build_combined_skill_body(
    matched_prompts: Sequence[Prompt],
    dependency_to_prompts: Dict[str, Set[str]],
    prompt_matches: Dict[str, Set[str]],
) -> str:
    lines: List[str] = []
    lines.append(
        "This combined skill aggregates reviewer prompts that match dependencies detected in the target project."
    )
    lines.append("")
    lines.append("### Matched dependencies")
    for dep in sorted(dependency_to_prompts):
        count = len(dependency_to_prompts[dep])
        lines.append(f"- {dep} ({count} prompt{'s' if count != 1 else ''})")
    lines.append("")

    for prompt in matched_prompts:
        slug = prompt.slug
        lines.append(f"## {prompt.title}")
        description = prompt.description
        if description:
            lines.append("")
            lines.append(f"> {description}")
        metadata_lines: List[str] = []
        repository = prompt.metadata.get("repository")
        if repository:
            metadata_lines.append(f"- **Repository:** `{repository}`")
        matched_dependencies = sorted(prompt_matches.get(slug, []))
        if matched_dependencies:
            metadata_lines.append(
                "- **Matched dependencies:** " + ", ".join(matched_dependencies)
            )
        if metadata_lines:
            lines.append("")
            lines.extend(metadata_lines)
        body = prompt.body.strip()
        if body:
            lines.append("")
            lines.append(body)
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def _scan_project_dependencies(project_dir: Path) -> Set[str]:
    dependencies: Set[str] = set()
    for path, parser in _iter_package_files(project_dir):
        try:
            names = parser(path)
        except Exception as exc:  # noqa: BLE001
            click.echo(f"Warning: Failed to parse dependencies from {path}: {exc}", err=True)
            continue
        for name in names:
            cleaned = name.strip()
            if cleaned:
                dependencies.add(cleaned)
    return dependencies


def _iter_package_files(
    project_dir: Path,
) -> Iterable[Tuple[Path, Callable[[Path], Set[str]]]]:
    ignore_dirs = {
        "node_modules",
        "vendor",
        "dist",
        "build",
        "out",
        "target",
        "tmp",
        "temp",
        "cache",
        "__pycache__",
        ".git",
        ".hg",
        ".svn",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".idea",
        ".vscode",
        "venv",
        ".venv",
        "env",
    }

    parsers_by_name: Dict[str, Callable[[Path], Set[str]]] = {
        "package.json": _parse_package_json,
        "package-lock.json": _parse_package_lock,
        "pnpm-lock.yaml": _parse_pnpm_lock,
        "yarn.lock": _parse_yarn_lock,
        "requirements.lock": _parse_requirements_txt,
        "Pipfile": _parse_pipfile,
        "Pipfile.lock": _parse_pipfile_lock,
        "pyproject.toml": _parse_pyproject_toml,
        "poetry.lock": _parse_poetry_lock,
        "requirements.txt": _parse_requirements_txt,
        "environment.yml": _parse_environment_yml,
        "environment.yaml": _parse_environment_yml,
        "Gemfile": _parse_gemfile,
        "Gemfile.lock": _parse_gemfile_lock,
        "gems.locked": _parse_gemfile_lock,
        "Cargo.toml": _parse_cargo_toml,
        "Cargo.lock": _parse_cargo_lock,
        "go.mod": _parse_go_mod,
        "composer.json": _parse_composer_json,
        "composer.lock": _parse_composer_lock,
        "pubspec.yaml": _parse_pubspec_yaml,
        "mix.exs": _parse_mix_exs,
    }

    pattern_parsers: List[Tuple[str, Callable[[Path], Set[str]]]] = [
        ("requirements*.txt", _parse_requirements_txt),
        ("requirements*.in", _parse_requirements_txt),
        ("*.csproj", _parse_csproj),
        ("*.fsproj", _parse_csproj),
        ("*.vbproj", _parse_csproj),
        ("*.deps.json", _parse_dotnet_deps),
    ]

    for root, dirs, files in os.walk(project_dir):
        filtered_dirs = []
        for directory in dirs:
            if directory.lower() in ignore_dirs:
                continue
            if directory.startswith(".") and directory.lower() not in {".config", ".cargo"}:
                continue
            filtered_dirs.append(directory)
        dirs[:] = filtered_dirs

        for file_name in files:
            parser = parsers_by_name.get(file_name)
            path = Path(root) / file_name
            if parser:
                yield path, parser
                continue
            for pattern, pattern_parser in pattern_parsers:
                if fnmatch.fnmatch(file_name, pattern):
                    yield path, pattern_parser
                    break


def _parse_package_json(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    names: Set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        section = data.get(key)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    return names


def _parse_package_lock(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    names: Set[str] = set()
    dependencies = data.get("dependencies")
    if isinstance(dependencies, dict):
        names.update(map(str, dependencies.keys()))
    packages = data.get("packages")
    if isinstance(packages, dict):
        for pkg_data in packages.values():
            if isinstance(pkg_data, dict):
                name = pkg_data.get("name")
                if name:
                    names.add(str(name))
    return names


def _parse_pnpm_lock(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    names: Set[str] = set()
    importers = data.get("importers", {})
    if isinstance(importers, dict):
        for importer in importers.values():
            if not isinstance(importer, dict):
                continue
            for key in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
                section = importer.get(key)
                if isinstance(section, dict):
                    names.update(map(str, section.keys()))
    return names


def _parse_yarn_lock(path: Path) -> Set[str]:
    names: Set[str] = set()
    pattern = re.compile(r"^(?:\"|')?(?P<name>@?[^@:\"']+)(?:@[^:]+)?:\s*$")
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            match = pattern.match(line.strip())
            if match:
                name = match.group("name")
                if name:
                    names.add(name)
    return names


def _parse_requirements_txt(path: Path) -> Set[str]:
    names: Set[str] = set()
    requirement_pattern = re.compile(r"^[A-Za-z0-9_.\-]+")
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith(("-r", "--requirement")):
                continue
            if stripped.startswith("git+"):
                continue
            match = requirement_pattern.match(stripped)
            if match:
                names.add(match.group(0))
    return names


def _parse_pyproject_toml(path: Path) -> Set[str]:
    if tomllib is None:
        raise RuntimeError("tomllib/tomli is required to parse pyproject.toml")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: Set[str] = set()

    project = data.get("project")
    if isinstance(project, dict):
        for dep in project.get("dependencies", []) or []:
            parsed = _split_dependency_name(str(dep))
            if parsed:
                names.add(parsed)
        optional_deps = project.get("optional-dependencies", {})
        if isinstance(optional_deps, dict):
            for deps in optional_deps.values():
                for dep in deps or []:
                    parsed = _split_dependency_name(str(dep))
                    if parsed:
                        names.add(parsed)

    tool = data.get("tool")
    if isinstance(tool, dict):
        poetry = tool.get("poetry")
        if isinstance(poetry, dict):
            for section_name in ("dependencies", "dev-dependencies"):
                section = poetry.get(section_name)
                if isinstance(section, dict):
                    names.update(map(str, section.keys()))
            groups = poetry.get("group", {})
            if isinstance(groups, dict):
                for group in groups.values():
                    if isinstance(group, dict):
                        deps = group.get("dependencies")
                        if isinstance(deps, dict):
                            names.update(map(str, deps.keys()))
        pdm = tool.get("pdm")
        if isinstance(pdm, dict):
            for section_name in ("dependencies", "dev-dependencies"):
                deps = pdm.get(section_name)
                if isinstance(deps, list):
                    for dep in deps:
                        parsed = _split_dependency_name(str(dep))
                        if parsed:
                            names.add(parsed)
    return names


def _parse_pipfile(path: Path) -> Set[str]:
    if tomllib is None:
        raise RuntimeError("tomllib/tomli is required to parse Pipfile")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: Set[str] = set()
    for section_name in ("packages", "dev-packages"):
        section = data.get(section_name)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    return names


def _parse_pipfile_lock(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    names: Set[str] = set()
    for section_name in ("default", "develop"):
        section = data.get(section_name)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    return names


def _parse_poetry_lock(path: Path) -> Set[str]:
    if tomllib is None:
        raise RuntimeError("tomllib/tomli is required to parse poetry.lock")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    packages = data.get("package")
    names: Set[str] = set()
    if isinstance(packages, list):
        for package in packages:
            if isinstance(package, dict):
                name = package.get("name")
                if name:
                    names.add(str(name))
    return names


def _parse_environment_yml(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    dependencies = data.get("dependencies") or []
    names: Set[str] = set()
    for dep in dependencies:
        if isinstance(dep, str):
            parsed = _split_dependency_name(dep)
            if parsed:
                names.add(parsed)
        elif isinstance(dep, dict):
            for nested in dep.get("pip", []) or []:
                parsed = _split_dependency_name(str(nested))
                if parsed:
                    names.add(parsed)
    return names


def _parse_gemfile(path: Path) -> Set[str]:
    pattern = re.compile(r"^\s*gem\s+['\"]([^'\"]+)['\"]")
    names: Set[str] = set()
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            match = pattern.match(line)
            if match:
                names.add(match.group(1))
    return names


def _parse_gemfile_lock(path: Path) -> Set[str]:
    names: Set[str] = set()
    in_specs = False
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped == "specs:":
                in_specs = True
                continue
            if not stripped and in_specs:
                in_specs = False
                continue
            if in_specs and stripped:
                match = re.match(r"([A-Za-z0-9_.\-]+) ", stripped)
                if match:
                    names.add(match.group(1))
    return names


def _parse_cargo_toml(path: Path) -> Set[str]:
    if tomllib is None:
        raise RuntimeError("tomllib/tomli is required to parse Cargo.toml")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: Set[str] = set()
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        section = data.get(key)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    targets = data.get("target")
    if isinstance(targets, dict):
        for target in targets.values():
            if not isinstance(target, dict):
                continue
            for key in ("dependencies", "dev-dependencies", "build-dependencies"):
                section = target.get(key)
                if isinstance(section, dict):
                    names.update(map(str, section.keys()))
    return names


def _parse_cargo_lock(path: Path) -> Set[str]:
    if tomllib is None:
        raise RuntimeError("tomllib/tomli is required to parse Cargo.lock")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    packages = data.get("package")
    names: Set[str] = set()
    if isinstance(packages, list):
        for package in packages:
            if isinstance(package, dict):
                name = package.get("name")
                if name:
                    names.add(str(name))
    return names


def _parse_go_mod(path: Path) -> Set[str]:
    names: Set[str] = set()
    in_require_block = False
    with path.open("r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("//"):
                continue
            if line.startswith("require ("):
                in_require_block = True
                continue
            if in_require_block and line == ")":
                in_require_block = False
                continue
            if line.startswith("require "):
                line = line[len("require ") :]
            if in_require_block or raw_line.strip().startswith("require "):
                parts = line.split()
                if parts:
                    names.add(parts[0])
    return names


def _parse_composer_json(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    names: Set[str] = set()
    for key in ("require", "require-dev"):
        section = data.get(key)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    return names


def _parse_composer_lock(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    names: Set[str] = set()
    for key in ("packages", "packages-dev"):
        packages = data.get(key)
        if isinstance(packages, list):
            for package in packages:
                if isinstance(package, dict):
                    name = package.get("name")
                    if name:
                        names.add(str(name))
    return names


def _parse_pubspec_yaml(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    names: Set[str] = set()
    for key in ("dependencies", "dev_dependencies"):
        section = data.get(key)
        if isinstance(section, dict):
            names.update(map(str, section.keys()))
    return names


def _parse_mix_exs(path: Path) -> Set[str]:
    pattern = re.compile(r"\{\s*:([A-Za-z0-9_]+)")
    names: Set[str] = set()
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            match = pattern.search(line)
            if match:
                names.add(match.group(1))
    return names


def _parse_csproj(path: Path) -> Set[str]:
    from xml.etree import ElementTree

    tree = ElementTree.parse(path)
    names: Set[str] = set()
    for elem in tree.findall(".//PackageReference"):
        include = elem.attrib.get("Include") or elem.attrib.get("Update")
        if include:
            names.add(include)
    return names


def _parse_dotnet_deps(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    targets = data.get("targets", {})
    names: Set[str] = set()
    if isinstance(targets, dict):
        for packages in targets.values():
            if isinstance(packages, dict):
                for package_name in packages.keys():
                    names.add(str(package_name))
    return names


def _split_dependency_name(value: str) -> Optional[str]:
    match = re.match(r"[A-Za-z0-9_.\-]+", value)
    if match:
        return match.group(0)
    return None


def _build_dependency_alias_map(
    dependencies: Iterable[str],
) -> Dict[str, Set[str]]:
    alias_map: Dict[str, Set[str]] = defaultdict(set)
    for dep in dependencies:
        for alias in _dependency_aliases(dep):
            for key in _alias_keys(alias):
                if key:
                    alias_map[key].add(dep)
    return alias_map


def _dependency_aliases(name: str) -> Set[str]:
    raw = name.strip()
    aliases = {raw, raw.lower()}
    normalized = _normalize_key(raw)
    if normalized:
        aliases.add(normalized)
    if raw.startswith("@"):
        _, _, remainder = raw.partition("/")
        if remainder:
            aliases.add(remainder)
            normalized_remainder = _normalize_key(remainder)
            if normalized_remainder:
                aliases.add(normalized_remainder)
    if "/" in raw:
        parts = raw.split("/")
        aliases.add(parts[-1])
        if len(parts) >= 2:
            owner_repo = "/".join(parts[-2:])
            aliases.add(owner_repo)
            normalized_owner_repo = _normalize_key(owner_repo)
            if normalized_owner_repo:
                aliases.add(normalized_owner_repo)
    lower = raw.lower()
    for prefix in ("github.com/", "gitlab.com/", "bitbucket.org/"):
        if lower.startswith(prefix):
            remainder = raw[len(prefix) :]
            aliases.add(remainder)
            if "/" in remainder:
                aliases.add(remainder.split("/", 1)[1])
    return {alias for alias in aliases if alias}


def _alias_keys(alias: str) -> Set[str]:
    lowered = alias.lower()
    normalized = _normalize_key(alias)
    if normalized and normalized != lowered:
        return {lowered, normalized}
    return {lowered}


def _normalize_key(value: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", value.lower())


def _match_prompts_with_dependencies(
    prompts: Sequence[Prompt], alias_map: Dict[str, Set[str]]
) -> Tuple[List[Prompt], Dict[str, Set[str]], Dict[str, Set[str]]]:
    matched_prompts: List[Prompt] = []
    dependency_to_prompts: Dict[str, Set[str]] = defaultdict(set)
    prompt_matches: Dict[str, Set[str]] = defaultdict(set)
    seen_slugs: Set[str] = set()

    for prompt in prompts:
        repository = prompt.metadata.get("repository")
        if not repository:
            continue
        prompt_alias_keys = _prompt_alias_keys(prompt)
        matching_keys = [key for key in prompt_alias_keys if key in alias_map]
        if not matching_keys:
            continue
        slug = prompt.slug
        if slug not in seen_slugs:
            matched_prompts.append(prompt)
            seen_slugs.add(slug)
        for key in matching_keys:
            for dep in alias_map[key]:
                dependency_to_prompts[dep].add(slug)
                prompt_matches[slug].add(dep)

    return matched_prompts, dependency_to_prompts, prompt_matches


def _prompt_alias_keys(prompt: Prompt) -> Set[str]:
    aliases: Set[str] = set()
    repo = prompt.metadata.get("repository")
    if repo:
        repo_str = str(repo)
        aliases.add(repo_str)
        if "/" in repo_str:
            _, _, name = repo_str.partition("/")
            if name:
                aliases.add(name)
                aliases.update(_repo_name_variants(name))
        aliases.add(repo_str.replace("/", "-"))
    slug = prompt.slug
    aliases.add(slug)
    slug_parts = slug.split("-")
    if slug_parts:
        aliases.add(slug_parts[0])
        if len(slug_parts) > 1:
            aliases.add("-".join(slug_parts[:2]))

    keys: Set[str] = set()
    for alias in aliases:
        for key in _alias_keys(alias):
            if key:
                keys.add(key)
    return keys


def _repo_name_variants(name: str) -> Set[str]:
    variants = {name}
    lowered = name.lower()
    if lowered.endswith(".js"):
        variants.add(name[:-3])
    for suffix in (".ts", ".rb", ".py", ".rs", ".go", ".php", ".kt", ".java"):
        if lowered.endswith(suffix):
            variants.add(name[: -len(suffix)])
    if lowered.endswith("-js"):
        variants.add(name[:-3])
    variants.add(name.replace(".", ""))
    variants.add(name.replace(".", "-"))
    return {variant for variant in variants if variant}


if __name__ == "__main__":
    try:
        convert_reviewers(standalone_mode=False)
    except SystemExit as exc:
        raise
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)
