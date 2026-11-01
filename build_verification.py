#!/usr/bin/env python3
"""Validate repository scans and build the verification catalog with only stdlib.

Inputs are _verification/*.json. Legacy _reviewers entries are never inspected or
converted. Source collection happens elsewhere; this build never executes any
command from a scanned repository.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

SITE_URL = "https://awesomereviewers.com"
STATUS_LABELS = {
    "ci_configured": "Configured in CI",
    "configured": "Configured locally",
    "implemented": "Implementation present",
}
STATUS_DESCRIPTIONS = {
    "ci_configured": "A CI definition invokes this check. Conditions may limit when it runs.",
    "configured": "A command or configuration enables this check. CI invocation was not established.",
    "implemented": "Source code implements this check. Its invocation was not established.",
}
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9_.-]*\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
SHA = re.compile(r"[0-9a-fA-F]{40}\Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: object, field: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{field} must be nonempty text")
    require("\x00" not in value, f"{field} contains a null character")
    return value


def strings(value: object, field: str) -> list[str]:
    require(isinstance(value, list), f"{field} must be an array")
    for item in value:
        text(item, field)
    return value


def repo_slug(repository: str) -> str:
    return repository.replace("/", "--").lower()


def validate_manifest(raw: object, source: str = "manifest") -> dict:
    """Reject malformed provenance before replacing any generated output."""
    require(isinstance(raw, dict), f"{source}: expected an object")
    manifest = copy.deepcopy(raw)
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
            f"{source}: unsupported schema_version")
    repository = text(manifest.get("repository"), "repository")
    require(bool(REPOSITORY.fullmatch(repository)), f"{source}: invalid repository")
    require(all(part not in (".", "..") for part in repository.split("/")), "invalid repository path")
    sha = text(manifest.get("commit_sha"), "commit_sha")
    require(bool(SHA.fullmatch(sha)), f"{source}: commit_sha must be a full 40-character SHA")
    text(manifest.get("default_branch"), "default_branch")
    scanned_at = text(manifest.get("scanned_at"), "scanned_at")
    try:
        stamp = datetime.fromisoformat(scanned_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{source}: invalid scanned_at") from exc
    require(stamp.tzinfo is not None, f"{source}: scanned_at needs a timezone")
    manifest["scanned_at"] = stamp.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    coverage = manifest.get("coverage")
    require(isinstance(coverage, dict), f"{source}: coverage must be an object")
    require(type(coverage.get("tree_complete")) is bool, "coverage.tree_complete must be a boolean")
    for field in ("files_considered", "candidate_files", "files_fetched", "files_skipped"):
        require(type(coverage.get(field)) is int and coverage[field] >= 0,
                f"coverage.{field} must be a nonnegative integer")
    require(coverage["candidate_files"] <= coverage["files_considered"],
            "candidate files cannot exceed considered files")
    require(coverage["files_fetched"] + coverage["files_skipped"] == coverage["candidate_files"],
            "fetched and skipped files must account for all candidates")
    strings(coverage.get("limitations"), "coverage.limitations")
    require(isinstance(manifest.get("methods"), list), f"{source}: methods must be an array")
    ids = set()
    for method in manifest["methods"]:
        require(isinstance(method, dict), "method must be an object")
        method_id = text(method.get("id"), "method.id")
        require(bool(IDENTIFIER.fullmatch(method_id)), f"invalid method id: {method_id}")
        require(method_id.startswith(repo_slug(repository) + "--"),
                f"{method_id}: id must be prefixed with the source repository")
        require(method_id not in ids, f"duplicate method id: {method_id}")
        ids.add(method_id)
        for field in ("method", "category"):
            require(bool(IDENTIFIER.fullmatch(text(method.get(field), field))), f"invalid {field}")
        require(method_id == repo_slug(repository) + "--" + method["method"],
                f"{method_id}: id must match the repository and method identifier")
        for field in ("title", "summary"):
            text(method.get(field), field)
        for field in ("tools", "commands"):
            strings(method.get(field), field)
        status = method.get("status")
        require(status in STATUS_LABELS, f"{method_id}: unsupported status")
        evidence = method.get("evidence")
        require(isinstance(evidence, list) and len(evidence) > 0, f"{method_id}: source evidence is required")
        for item in evidence:
            require(isinstance(item, dict), "evidence must be an object")
            path = text(item.get("path"), "evidence.path")
            parts = PurePosixPath(path).parts
            require(not path.startswith("/") and "\\" not in path and ".." not in parts and
                    not any(ord(c) < 32 for c in path), "evidence.path must be a safe relative path")
            require(PurePosixPath(path).name.lower() not in ("skill.md", "agents.md", "claude.md") and
                    "_reviewers" not in parts, "instruction files cannot establish a verification method")
            start, end = item.get("start_line"), item.get("end_line")
            require(type(start) is int and type(end) is int and 1 <= start <= end,
                    "evidence needs a valid 1-based line range")
            excerpt = text(item.get("excerpt"), "evidence.excerpt")
            require(len(excerpt.splitlines()) == end - start + 1,
                    "evidence excerpt must match the complete linked line range")
            require(item.get("kind") in STATUS_LABELS, "unsupported evidence kind")
            url = urlsplit(text(item.get("url"), "evidence.url"))
            expected = f"/{repository}/blob/{sha}/{path}"
            fragments = {f"L{start}-L{end}"}
            if start == end:
                fragments.add(f"L{start}")
            require(url.scheme == "https" and url.netloc == "github.com" and not url.query and
                    unquote(url.path) == expected and url.fragment in fragments,
                    f"{method_id}: evidence URL must pin the exact repository, commit, path and line range")
            item.setdefault("conditions", [])
            strings(item["conditions"], "evidence.conditions")
            item.setdefault("working_directory", None)
            if item["working_directory"] is not None:
                text(item["working_directory"], "evidence.working_directory")
            item.setdefault("environment", {})
            require(isinstance(item["environment"], dict), "evidence.environment must be an object")
            for key, value in item["environment"].items():
                text(key, "environment key")
                require(isinstance(value, str), "environment values must be strings")
        require(any(item["kind"] == status for item in evidence),
                f"{method_id}: status needs matching source evidence")
    return manifest


def humanize(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").capitalize()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fence(value: str) -> str:
    marker = "`" * max(3, max((len(m.group()) + 1 for m in re.finditer(r"`+", value)), default=3))
    return f"{marker}\n{value}\n{marker}"


def method_markdown(entry: dict) -> str:
    lines = [f"# {entry['title']}", "", entry["summary"], "",
             f"Repository: {entry['repository']}", f"Commit: `{entry['commit_sha']}`",
             f"Inspected: {entry['scanned_at']}",
             f"Status: {STATUS_LABELS[entry['status']]}. {STATUS_DESCRIPTIONS[entry['status']]}", "",
             "This record describes source evidence. It does not attest to a successful run or a required merge check.", "",
             "## Tools", "", ", ".join(entry["tools"]) or "No named tool recorded.", "",
             "## Recorded commands", ""]
    lines.extend(fence(command) + "\n" for command in entry["commands"])
    if not entry["commands"]:
        lines.append("No invocation command was established by this scan.")
    lines += ["", "## Source evidence", ""]
    for item in entry["evidence"]:
        lines += [f"### {item['path']}:{item['start_line']}-{item['end_line']}", "",
                  item["url"], "", f"Evidence: {STATUS_LABELS[item['kind']]}", ""]
        if item["conditions"]:
            lines += ["Conditions: " + "; ".join(item["conditions"]), ""]
        if item["working_directory"]:
            lines += [f"Working directory: `{item['working_directory']}`", ""]
        if item["environment"]:
            lines += ["Environment:", fence(json.dumps(item["environment"], ensure_ascii=False, indent=2)), ""]
        lines += [fence(item["excerpt"]), ""]
    lines += ["## Scan coverage", "",
              f"Files inspected: {entry['coverage']['files_fetched']} of {entry['coverage']['candidate_files']} candidates.",
              f"Repository tree complete: {str(entry['coverage']['tree_complete']).lower()}."]
    lines.extend(entry["coverage"]["limitations"])
    return "\n".join(lines) + "\n"


def build_openapi(site_url: str) -> dict:
    """Keep the new API separate from the existing instruction API."""
    schemas = {
        "Evidence": {"type": "object", "required": ["path", "start_line", "end_line", "excerpt", "url", "kind"],
                     "properties": {"path": {"type": "string"}, "start_line": {"type": "integer", "minimum": 1},
                                    "end_line": {"type": "integer", "minimum": 1}, "excerpt": {"type": "string"},
                                    "url": {"type": "string", "format": "uri"}, "kind": {"type": "string", "enum": list(STATUS_LABELS)},
                                    "conditions": {"type": "array", "items": {"type": "string"}},
                                    "working_directory": {"type": ["string", "null"]},
                                    "environment": {"type": "object", "additionalProperties": {"type": "string"}}}},
        "Method": {"type": "object", "required": ["id", "method", "title", "category", "summary", "status", "tools", "commands", "evidence"],
                   "properties": {**{k: {"type": "string"} for k in ("id", "method", "title", "category", "summary", "repository", "commit_sha", "scanned_at")},
                                  "status": {"type": "string", "enum": list(STATUS_LABELS)},
                                  "tools": {"type": "array", "items": {"type": "string"}},
                                  "commands": {"type": "array", "items": {"type": "string"}},
                                  "evidence": {"type": "array", "minItems": 1, "items": {"$ref": "#/components/schemas/Evidence"}}}},
        "Coverage": {"type": "object", "properties": {
            "tree_complete": {"type": "boolean"},
            **{k: {"type": "integer", "minimum": 0} for k in ("files_considered", "candidate_files", "files_fetched", "files_skipped")},
            "limitations": {"type": "array", "items": {"type": "string"}}}},
        "RepositoryScan": {"type": "object", "required": ["schema_version", "repository", "commit_sha", "scanned_at", "coverage", "methods"],
                           "properties": {"schema_version": {"type": "integer", "const": 1},
                                          "repository": {"type": "string"}, "commit_sha": {"type": "string", "pattern": "^[0-9a-fA-F]{40}$"},
                                          "scanned_at": {"type": "string", "format": "date-time"},
                                          "coverage": {"$ref": "#/components/schemas/Coverage"},
                                          "methods": {"type": "array", "items": {"$ref": "#/components/schemas/Method"}}}},
        "Catalog": {"type": "object", "required": ["schema_version", "total", "repository_count", "entries", "repositories"],
                    "properties": {"schema_version": {"type": "integer", "const": 1}, "total": {"type": "integer"},
                                   "repository_count": {"type": "integer"}, "entries": {"type": "array", "items": {"$ref": "#/components/schemas/Method"}},
                                   "repositories": {"type": "array", "items": {"type": "object"}}}},
    }
    resources = [
        ("/raw/verification/index.json", "catalog", "Read all verification records and scan coverage", "application/json", "Catalog"),
        ("/raw/verification/{id}.json", "method", "Read one verification record", "application/json", "Method"),
        ("/raw/verification/{id}.md", "methodMarkdown", "Read one verification record as Markdown", "text/markdown", None),
        ("/raw/verification/repositories/{repository}.json", "repositoryScan", "Read a source scan manifest", "application/json", "RepositoryScan"),
        ("/raw/verification/site.md", "overview", "Read the verification catalog overview", "text/markdown", None),
        ("/raw/verification/llms.txt", "llmsIndex", "Read the verification record index", "text/plain", None),
        ("/raw/verification/openapi.json", "description", "Read this API description", "application/json", None),
    ]
    paths = {}
    for path, operation_id, summary, media, schema in resources:
        response_schema = {"$ref": f"#/components/schemas/{schema}"} if schema else {"type": "object" if media == "application/json" else "string"}
        operation = {"operationId": operation_id, "summary": summary, "responses": {
            "200": {"description": "Static file", "content": {media: {"schema": response_schema}}},
            "404": {"description": "GitHub Pages returns the HTML not-found page", "content": {"text/html": {"schema": {"type": "string"}}}}}}
        parameters = re.findall(r"\{([^}]+)\}", path)
        if parameters:
            operation["parameters"] = [{"name": p, "in": "path", "required": True,
                                        "schema": {"type": "string"},
                                        "description": "Use the exact identifier from index.json."} for p in parameters]
        paths[path] = {"get": operation}
    return {"openapi": "3.1.0", "info": {"title": "Awesome Verification API", "version": "1",
            "description": "Source-backed verification methods at pinned repository commits. No execution or merge-gate attestation."},
            "servers": [{"url": site_url}], "paths": paths, "components": {"schemas": schemas}}


def build(root: Path | str = ".", site_url: str = SITE_URL) -> dict:
    root = Path(root)
    manifests = []
    repositories_seen, ids_seen = set(), set()
    for path in sorted((root / "_verification").glob("*.json")):
        try:
            manifest = validate_manifest(json.loads(path.read_text(encoding="utf-8")), str(path))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
        repository_key = manifest["repository"].lower()
        require(repository_key not in repositories_seen, f"duplicate repository scan: {repository_key}")
        repositories_seen.add(repository_key)
        for method in manifest["methods"]:
            require(method["id"] not in ids_seen, f"duplicate method id: {method['id']}")
            ids_seen.add(method["id"])
        manifests.append(manifest)

    entries, repositories = [], []
    for manifest in manifests:
        repository = manifest["repository"]
        repositories.append({k: v for k, v in manifest.items() if k != "methods"} | {
            "method_count": len(manifest["methods"]), "slug": repo_slug(repository),
            "methods": sorted({m["method"] for m in manifest["methods"]}),
            "tools": sorted({tool for m in manifest["methods"] for tool in m["tools"]}),
            "raw": f"/raw/verification/repositories/{repo_slug(repository)}.json",
        })
        for method in manifest["methods"]:
            entry = copy.deepcopy(method)
            entry.update({k: manifest[k] for k in ("repository", "commit_sha", "default_branch", "scanned_at", "coverage")})
            entry.update({"status_label": STATUS_LABELS[method["status"]],
                          "status_description": STATUS_DESCRIPTIONS[method["status"]],
                          "category_label": humanize(method["category"]), "updated": manifest["scanned_at"][:10],
                          "url": f"/methods/{method['id']}/", "raw_json": f"/raw/verification/{method['id']}.json",
                          "raw_markdown": f"/raw/verification/{method['id']}.md"})
            entries.append(entry)
    entries.sort(key=lambda e: (e["scanned_at"], e["repository"], e["title"]), reverse=True)
    repositories.sort(key=lambda r: r["repository"].lower())
    filters = {}
    for field in ("method", "category", "status"):
        counts = Counter(e[field] for e in entries)
        filters[field] = [{"value": value, "label": STATUS_LABELS.get(value, humanize(value)), "count": count}
                          for value, count in sorted(counts.items())]
    filters["tool"] = sorted({tool for entry in entries for tool in entry["tools"]})
    latest = max((m["scanned_at"] for m in manifests), default=None)
    catalog = {"schema_version": 1, "total": len(entries), "method_count": len(filters["method"]),
               "repository_count": len(repositories), "scanned_at": latest, "updated": latest[:10] if latest else None,
               "status_labels": STATUS_LABELS, "status_descriptions": STATUS_DESCRIPTIONS,
               "filters": filters, "entries": entries, "repositories": repositories}

    # Only owned generated directories are replaced. Validation above is complete
    # before deleting old records, so a rejected manifest cannot publish a partial catalog.
    raw_dir, pages_dir = root / "raw" / "verification", root / "methods"
    for path in (raw_dir, pages_dir):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)
    write_json(root / "_data" / "verification.json", catalog)
    write_json(raw_dir / "index.json", catalog)
    write_json(raw_dir / "openapi.json", build_openapi(site_url))
    for manifest in manifests:
        write_json(raw_dir / "repositories" / f"{repo_slug(manifest['repository'])}.json", manifest)
    for entry in entries:
        write_json(raw_dir / f"{entry['id']}.json", entry)
        (raw_dir / f"{entry['id']}.md").write_text(method_markdown(entry), encoding="utf-8")
        page_dir = pages_dir / entry["id"]
        page_dir.mkdir()
        (page_dir / "index.html").write_text(
            "---\nlayout: verification\nmethod_id: " + json.dumps(entry["id"]) +
            "\ntitle: " + json.dumps(entry["title"]) + "\ndescription: " + json.dumps(entry["summary"]) + "\n---\n",
            encoding="utf-8")
    overview = ["# Awesome Verification", "", "Verification methods found in repository code and configuration, with evidence pinned to the inspected commit.", "",
                f"{len(entries)} records across {len(repositories)} inspected repositories.", "",
                "Source evidence does not establish a successful run or a required merge check.", "",
                f"Catalog: {site_url}/raw/verification/index.json",
                f"API: {site_url}/raw/verification/openapi.json",
                f"Documentation: {site_url}/verification-api/", ""]
    (raw_dir / "site.md").write_text("\n".join(overview), encoding="utf-8")
    index = overview + ["## Records", ""] + [
        f"- [{e['title']}]({site_url}{e['raw_markdown']}) | {e['repository']} | {e['status_label']} | {e['commit_sha']}"
        for e in entries]
    (raw_dir / "llms.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"verification: {len(entries)} records, {len(repositories)} inspected repositories")
    return catalog


if __name__ == "__main__":
    build(Path(__file__).resolve().parent)
