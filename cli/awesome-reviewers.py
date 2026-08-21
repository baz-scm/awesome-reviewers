#!/usr/bin/env python3
"""awesome-reviewers — the Awesome Reviewers corpus from the command line.

One file, the standard library, Python 3.9+. It drives the documented endpoints
of https://awesomereviewers.com and nothing else, so anything it can do you can
do with curl; it just already knows the paths, the paging and how to tell what
changed since last time.

    awesome-reviewers domains                          every domain, with counts
    awesome-reviewers search "kv cache" --limit 5       titles and descriptions
    awesome-reviewers get <slug>                        one instruction as markdown
    awesome-reviewers get <slug> --json                 the same, as typed JSON
    awesome-reviewers bundle llm-infra -o rubric.md     a whole domain in one file
    awesome-reviewers sync ./corpus --domain security   mirror a domain to disk
    awesome-reviewers version                           interface version and policies

Endpoints, schemas and the versioning policy: https://awesomereviewers.com/developers/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Iterable, Optional

__version__ = "1.0.0"

DEFAULT_SITE = os.environ.get("AWESOME_REVIEWERS_SITE", "https://awesomereviewers.com")
API_BASE = "/v1"
USER_AGENT = f"awesome-reviewers-cli/{__version__} (+https://awesomereviewers.com/developers/)"
# The interface advertises its quota in the RateLimit header fields and its
# retry delay in Retry-After. Honour both rather than guessing a backoff.
MAX_ATTEMPTS = 4
FALLBACK_RETRY_SECONDS = 5


# --------------------------------------------------------------------------- #
# URLs — every path this CLI knows, in one place
# --------------------------------------------------------------------------- #


def url_for(site: str, kind: str, key: str = "") -> str:
    site = site.rstrip("/")
    paths = {
        "version": f"{API_BASE}/version.json",
        "index": f"{API_BASE}/index.json",
        "domains": f"{API_BASE}/domains.json",
        "facets": f"{API_BASE}/facets.json",
        "sources": f"{API_BASE}/sources.json",
        "instruction": f"{API_BASE}/instructions/{key}.json",
        "markdown": f"/raw/{key}.md",
        "bundle": f"/raw/bundles/{key}.md",
    }
    if kind not in paths:
        raise KeyError(f"unknown endpoint {kind!r}")
    return f"{site}{paths[kind]}"


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #


class ApiError(RuntimeError):
    """An error the interface reported, with the problem details it carried."""

    def __init__(self, status: int, message: str, resolution: str = "") -> None:
        super().__init__(message if not resolution else f"{message}\n  → {resolution}")
        self.status = status
        self.resolution = resolution


def _problem(body: bytes) -> tuple[str, str]:
    """Pull `detail` and `resolution` out of an RFC 9457 problem body."""
    try:
        problem = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return "", ""
    if not isinstance(problem, dict):
        return "", ""
    return str(problem.get("detail", "")), str(problem.get("resolution", ""))


def retry_delay(headers, attempt: int) -> float:
    """Seconds to wait after a 429, from Retry-After, then RateLimit's `t`."""
    after = headers.get("Retry-After") if headers else None
    if after:
        try:
            return max(0.0, float(after))
        except ValueError:
            pass
    limit = headers.get("RateLimit") if headers else None
    if limit and ";t=" in limit:
        try:
            return max(0.0, float(limit.split(";t=")[1].split(";")[0].split(",")[0]))
        except ValueError:
            pass
    return float(FALLBACK_RETRY_SECONDS * attempt)


def fetch(url: str, accept: str = "*/*", *, sleep=time.sleep) -> bytes:
    """GET a URL, retrying only what the interface asks us to retry."""
    request = urllib.request.Request(
        url, headers={"Accept": accept, "User-Agent": USER_AGENT}
    )
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            body = error.read()
            detail, resolution = _problem(body)
            if error.code == 429 and attempt < MAX_ATTEMPTS:
                sleep(retry_delay(error.headers, attempt))
                continue
            raise ApiError(
                error.code,
                detail or f"{error.code} {error.reason} for {url}",
                resolution,
            ) from error
        except urllib.error.URLError as error:  # pragma: no cover - network
            raise ApiError(0, f"cannot reach {url}: {error.reason}") from error
    raise ApiError(429, f"gave up on {url} after {MAX_ATTEMPTS} attempts")


def fetch_json(url: str, **kwargs) -> object:
    return json.loads(fetch(url, "application/json", **kwargs).decode("utf-8"))


def fetch_text(url: str, **kwargs) -> str:
    return fetch(url, "text/markdown, text/plain", **kwargs).decode("utf-8")


# --------------------------------------------------------------------------- #
# Selection — pure, so it can be tested without a network
# --------------------------------------------------------------------------- #


def matches(entry: dict, query: str, domain: str, topic: str, language: str) -> bool:
    if domain and entry.get("domain") != domain:
        return False
    if topic and (entry.get("topic") or "").lower() != topic.lower():
        return False
    if language and (entry.get("language") or "").lower() != language.lower():
        return False
    if not query:
        return True
    haystack = " ".join(
        str(entry.get(field, ""))
        for field in ("title", "description", "repository", "topic", "language")
    ).lower()
    return all(term in haystack for term in query.lower().split())


def select(
    entries: Iterable[dict],
    query: str = "",
    domain: str = "",
    topic: str = "",
    language: str = "",
    limit: Optional[int] = None,
) -> list:
    found = [e for e in entries if matches(e, query, domain, topic, language)]
    found.sort(key=lambda e: (e.get("updated", ""), e.get("comments", 0)), reverse=True)
    return found if limit is None else found[:limit]


def sync_plan(entries: Iterable[dict], manifest: dict, force: bool = False) -> list:
    """The slugs whose `updated` date differs from what is already on disk."""
    return [
        entry
        for entry in entries
        if force or manifest.get(entry["slug"]) != entry.get("updated")
    ]


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #


def cmd_version(args) -> int:
    payload = fetch_json(url_for(args.site, "version"))
    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
        return 0
    limit = payload["rate_limit"]
    print(f"interface     v{payload['api_version']} ({payload['versioning']['stability']})")
    print(f"corpus        {payload['corpus_version']} — {payload['count']} instructions")
    print(f"versioning    {payload['versioning']['scheme']}, base {payload['versioning']['base_path']}")
    print(f"deprecations  {len(payload['deprecations'])}")
    print(f"quota         {limit['quota']} per {limit['window_seconds']}s ({limit['enforced_by']})")
    print(f"docs          {payload['developer_portal']}")
    return 0


def cmd_domains(args) -> int:
    payload = fetch_json(url_for(args.site, "domains"))
    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
        return 0
    for domain in payload["domains"]:
        print(f"{domain['slug']:16} {domain['count']:>5}  updated {domain['updated']}  {domain['title']}")
    return 0


def cmd_search(args) -> int:
    index = fetch_json(url_for(args.site, "index"))
    found = select(
        index["entries"], args.query, args.domain, args.topic, args.language, args.limit
    )
    if args.json:
        json.dump(found, sys.stdout, indent=2)
        print()
        return 0
    if not found:
        print("nothing matched", file=sys.stderr)
        return 1
    for entry in found:
        print(f"{entry['slug']}")
        print(f"    {entry['title']} — {entry['repository']}, {entry['domain']}, updated {entry['updated']}")
    return 0


def write_out(text: str, destination: Optional[str]) -> None:
    if not destination or destination == "-":
        sys.stdout.write(text if text.endswith("\n") else f"{text}\n")
        return
    with open(destination, "w", encoding="utf-8") as handle:
        handle.write(text if text.endswith("\n") else f"{text}\n")
    print(f"wrote {destination}", file=sys.stderr)


def cmd_get(args) -> int:
    if args.json:
        payload = fetch_json(url_for(args.site, "instruction", args.slug))
        write_out(json.dumps(payload, indent=2), args.output)
        return 0
    write_out(fetch_text(url_for(args.site, "markdown", args.slug)), args.output)
    return 0


def cmd_bundle(args) -> int:
    write_out(fetch_text(url_for(args.site, "bundle", args.domain)), args.output)
    return 0


MANIFEST_NAME = ".awesome-reviewers.json"


def cmd_sync(args) -> int:
    """Mirror instructions into a directory, fetching only what changed."""
    directory = args.directory
    os.makedirs(directory, exist_ok=True)
    manifest_path = os.path.join(directory, MANIFEST_NAME)
    manifest = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                manifest = json.load(handle).get("instructions", {})
        except (OSError, ValueError):
            manifest = {}

    index = fetch_json(url_for(args.site, "index"))
    wanted = select(index["entries"], "", args.domain, args.topic, args.language)
    stale = sync_plan(wanted, manifest, args.force)
    print(
        f"{len(wanted)} instruction(s) selected, {len(stale)} to fetch", file=sys.stderr
    )

    for entry in stale:
        body = fetch_text(url_for(args.site, "markdown", entry["slug"]))
        with open(os.path.join(directory, f"{entry['slug']}.md"), "w", encoding="utf-8") as handle:
            handle.write(body)
        manifest[entry["slug"]] = entry.get("updated", "")

    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "site": args.site.rstrip("/"),
                "corpus_version": index.get("generated", ""),
                "instructions": manifest,
            },
            handle,
            indent=2,
        )
    print(f"{directory}: {len(manifest)} instruction(s) on disk", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awesome-reviewers",
        description="Expert engineering instructions from awesomereviewers.com.",
        epilog="Endpoints and policies: https://awesomereviewers.com/developers/",
    )
    parser.add_argument("--site", default=DEFAULT_SITE, help=f"base URL (default {DEFAULT_SITE})")
    parser.add_argument("--version", action="version", version=f"awesome-reviewers {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_filters(subparser) -> None:
        subparser.add_argument("--domain", default="", help="only this domain slug")
        subparser.add_argument("--topic", default="", help="only this topic")
        subparser.add_argument("--language", default="", help="only this language")

    version = subparsers.add_parser("version", help="interface version and policies")
    version.add_argument("--json", action="store_true", help="print the raw document")
    version.set_defaults(func=cmd_version)

    domains = subparsers.add_parser("domains", help="every domain, with counts")
    domains.add_argument("--json", action="store_true", help="print the raw document")
    domains.set_defaults(func=cmd_domains)

    search = subparsers.add_parser("search", help="search titles and descriptions")
    search.add_argument("query", nargs="?", default="", help="terms; all must match")
    search.add_argument("--limit", type=int, default=20, help="rows to print (default 20)")
    search.add_argument("--json", action="store_true", help="print matching index rows")
    add_filters(search)
    search.set_defaults(func=cmd_search)

    get = subparsers.add_parser("get", help="one instruction")
    get.add_argument("slug", help="instruction slug, as published in the index")
    get.add_argument("--json", action="store_true", help="typed JSON instead of markdown")
    get.add_argument("-o", "--output", help="write to this file instead of stdout")
    get.set_defaults(func=cmd_get)

    bundle = subparsers.add_parser("bundle", help="every instruction in one domain")
    bundle.add_argument("domain", help="domain slug")
    bundle.add_argument("-o", "--output", help="write to this file instead of stdout")
    bundle.set_defaults(func=cmd_bundle)

    sync = subparsers.add_parser("sync", help="mirror instructions to a directory")
    sync.add_argument("directory", help="where to write the markdown files")
    sync.add_argument("--force", action="store_true", help="refetch even if unchanged")
    add_filters(sync)
    sync.set_defaults(func=cmd_sync)

    return parser


def main(argv: Optional[list] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ApiError as error:
        print(f"awesome-reviewers: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:  # pragma: no cover - interactive
        return 130


if __name__ == "__main__":
    sys.exit(main())
