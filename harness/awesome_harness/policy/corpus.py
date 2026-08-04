"""Pillar 6a — reading the Awesome Reviewers corpus.

The corpus is the policy source of truth, and it comes in two shapes:

  `_reviewers/` layout   `<slug>.md` with flat YAML front matter — the source of
                         truth in the awesome-reviewers repository itself
  `raw/` layout          `index.json` plus `<slug>.md` files whose metadata is an
                         HTML comment — what `curl`ing the public endpoints gives
                         you, deliberately not front matter so that Jekyll serves
                         those files verbatim

Both are read here so the harness works vendored *and* against a download. Nothing
else in the package parses corpus files.

Two rules that matter more than the parsing:

  **A slug that does not resolve is a hard failure.** Not a warning, not a skipped
  rule. A policy pack naming an instruction that does not exist would look
  identical to a working one while enforcing nothing, and the whole value of
  citing a source is that the citation can be checked.

  **Every instruction is pinned by the digest of its body.** A pack records the
  digest it compiled against, so a corpus update is detected as drift rather than
  silently changing what a signed attestation meant.

Derived from the corpus:
  aidlc-workflows-portable-configuration-standards — read the documented format,
      not a convenient derived artifact. `_data/*.json` is generated and
      uncommitted; depending on it would make the harness require a site build.
  aidlc-workflows-no-silent-null-artifacts — a corpus that parses to zero entries
      is an error, not an empty result.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterable, Iterator

from ..digest import digest_text
from ..errors import CorpusError

# The corpus front matter is deliberately flat: string and integer scalars, some
# wrapped over continuation lines. Matching that with two regexes keeps the harness
# dependency-free, exactly as build_data.py does for the site.
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
COMMENT_HEADER_RE = re.compile(r"\A<!--\n(.*?)\n-->\n?(.*)\Z", re.DOTALL)

SITE = "https://awesomereviewers.com"


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].strip()
    return value


def parse_metadata_block(block: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    key: str | None = None
    for line in block.split("\n"):
        scalar = SCALAR_RE.match(line)
        if scalar:
            key = scalar.group(1)
            meta[key] = scalar.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            meta[key] = f"{meta[key]} {line.strip()}".strip()
    return {k: _unquote(v) for k, v in meta.items()}


@dataclass(frozen=True)
class Instruction:
    slug: str
    title: str
    description: str
    repository: str
    topic: str
    language: str
    body: str
    comments: int = 0
    stars: int = 0

    @cached_property
    def digest(self) -> str:
        """Digest of the instruction body — what a pack pins.

        The body and not the whole file: front matter carries `comments_count` and
        `repository_stars`, which change as the source discussion attracts more
        activity without the rule itself changing. Pinning those would report drift
        on every corpus refresh and train everyone to ignore drift.
        """
        return digest_text(self.body)

    @property
    def url(self) -> str:
        return f"{SITE}/reviewers/{self.slug}/"

    @property
    def raw_url(self) -> str:
        return f"{SITE}/raw/{self.slug}.md"

    def as_context(self) -> str:
        """Render for an agent's review context — the advisory enforcement tier."""
        return (
            f"## {self.title}\n\n"
            f"<!-- awesome-reviewers: {self.slug} | source: {self.repository} | "
            f"topic: {self.topic} | language: {self.language} | {self.raw_url} -->\n\n"
            f"{self.body}\n"
        )


def _parse_reviewers_file(path: Path) -> Instruction | None:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    meta = parse_metadata_block(match.group(1))
    body = match.group(2).strip()
    if not meta.get("title") or not body:
        return None
    return Instruction(
        slug=path.stem,
        title=meta["title"],
        description=meta.get("description", ""),
        repository=meta.get("repository", ""),
        topic=meta.get("label", ""),
        language=meta.get("language", ""),
        body=body,
        comments=_as_int(meta.get("comments_count")),
        stars=_as_int(meta.get("repository_stars")),
    )


def _parse_raw_file(path: Path) -> Instruction | None:
    text = path.read_text(encoding="utf-8")
    match = COMMENT_HEADER_RE.match(text)
    if not match:
        return None
    meta = parse_metadata_block(match.group(1))
    body = match.group(2).strip()
    if not meta.get("title") or not body:
        return None
    return Instruction(
        slug=path.stem,
        title=meta["title"],
        description=meta.get("description", ""),
        repository=meta.get("source", ""),
        topic=meta.get("topic", ""),
        language=meta.get("language", ""),
        body=body,
    )


def _as_int(value: str | None) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


class Corpus:
    """Lazily-loaded, slug-indexed view of the instruction corpus."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._index: dict[str, Instruction] | None = None
        self._layout = "unknown"

    # ---- loading --------------------------------------------------------- #

    @property
    def layout(self) -> str:
        self.load()
        return self._layout

    def load(self) -> dict[str, Instruction]:
        if self._index is not None:
            return self._index
        if not self.root.is_dir():
            raise CorpusError(
                f"corpus directory not found: {self.root}",
                hint=(
                    "point policy.corpus at a checkout of _reviewers/, or at a directory "
                    f"holding a download of {SITE}/raw/"
                ),
            )
        is_raw = (self.root / "index.json").is_file()
        self._layout = "raw" if is_raw else "reviewers"
        parse = _parse_raw_file if is_raw else _parse_reviewers_file

        index: dict[str, Instruction] = {}
        unparsed: list[str] = []
        for path in sorted(self.root.glob("*.md")):
            instruction = parse(path)
            if instruction is None:
                unparsed.append(path.name)
                continue
            index[instruction.slug] = instruction

        if not index:
            raise CorpusError(
                f"no instructions parsed from {self.root} "
                f"({len(unparsed)} file(s) present but unreadable in {self._layout} layout)",
                hint="check that the directory holds <slug>.md instruction files",
            )
        self._index = index
        return index

    def __len__(self) -> int:
        return len(self.load())

    def __contains__(self, slug: object) -> bool:
        return str(slug) in self.load()

    def __iter__(self) -> Iterator[Instruction]:
        return iter(sorted(self.load().values(), key=lambda i: i.slug))

    # ---- lookup ---------------------------------------------------------- #

    def get(self, slug: str) -> Instruction:
        """Resolve a slug or fail loudly, with the closest matches offered.

        The hint does real work here: `aidlc-workflows-secure-path-confinment` is
        the kind of typo a person makes once and then cannot see.
        """
        index = self.load()
        if slug in index:
            return index[slug]
        import difflib

        near = difflib.get_close_matches(slug, index.keys(), n=3, cutoff=0.6)
        raise CorpusError(
            f"instruction {slug!r} is not in the corpus at {self.root}",
            hint=("did you mean: " + ", ".join(near)) if near else "check the slug against /raw/index.json",
        )

    def select(
        self,
        *,
        slugs: Iterable[str] = (),
        topics: Iterable[str] = (),
        languages: Iterable[str] = (),
        repositories: Iterable[str] = (),
        limit: int | None = None,
        include_all: bool = False,
    ) -> list[Instruction]:
        """Select instructions by any combination of facets.

        Explicit slugs are resolved first and always included, so a curated rule
        cannot be silently dropped by a `limit` meant for a broad facet sweep.

        `include_all` selects the entire corpus, which is the default a pack is built
        with. Pinning all of it is the point: the corpus is the policy, and a pack that
        held a top-N slice would silently answer a different question than the one its
        digest appears to answer.
        """
        chosen: dict[str, Instruction] = {slug: self.get(slug) for slug in slugs}

        wanted_topics = {t.strip().lower() for t in topics if t.strip()}
        wanted_languages = {t.strip().lower() for t in languages if t.strip()}
        wanted_repositories = {t.strip().lower() for t in repositories if t.strip()}
        if include_all and not (wanted_topics or wanted_languages or wanted_repositories):
            # `None` is unlimited and `0` is none. The CLI maps `--limit 0` to None
            # before it gets here, because "0" reads as "no cap" on a command line and
            # as "zero" in a function signature.
            budget = None if limit is None else max(0, limit - len(chosen))
            ranked = sorted(self, key=lambda i: (-i.comments, -i.stars, i.slug))
            for instruction in (ranked[:budget] if budget is not None else ranked):
                chosen.setdefault(instruction.slug, instruction)
            return sorted(chosen.values(), key=lambda i: i.slug)
        if wanted_topics or wanted_languages or wanted_repositories:
            # Ranked by discussion volume then stars: the instructions distilled from
            # the most reviewer back-and-forth are the ones a team argued about most.
            candidates = sorted(
                (
                    instruction
                    for instruction in self
                    if (not wanted_topics or instruction.topic.lower() in wanted_topics)
                    and (not wanted_languages or instruction.language.lower() in wanted_languages)
                    and (not wanted_repositories or instruction.repository.lower() in wanted_repositories)
                ),
                key=lambda i: (-i.comments, -i.stars, i.slug),
            )
            budget = None if limit is None else max(0, limit - len(chosen))
            for instruction in candidates[:budget] if budget is not None else candidates:
                chosen.setdefault(instruction.slug, instruction)
        return sorted(chosen.values(), key=lambda i: i.slug)

    def facets(self) -> dict[str, dict[str, int]]:
        topics: dict[str, int] = {}
        languages: dict[str, int] = {}
        repositories: dict[str, int] = {}
        for instruction in self:
            for bucket, key in ((topics, instruction.topic), (languages, instruction.language), (repositories, instruction.repository)):
                if key:
                    bucket[key] = bucket.get(key, 0) + 1
        return {"topics": topics, "languages": languages, "repositories": repositories}

    def index_json(self) -> dict[str, object] | None:
        path = self.root / "index.json"
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CorpusError(f"{path} is not valid JSON: {exc.msg}") from exc
