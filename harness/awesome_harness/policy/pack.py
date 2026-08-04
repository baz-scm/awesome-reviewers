"""Pillar 6d — the policy pack: a pinned, digested selection of the corpus.

A pack is the unit of policy versioning. It records, for every rule, the corpus slug
it came from and the digest of that instruction's body at compile time. The pack
itself has a digest, and that digest goes into the cache key and the attestation.

That chain is the pillar's real claim: given an attestation you can say *which
version of which rule, sourced from which review discussion, gated this change* —
and check it, because the pack is committed and the corpus is public.

Two enforcement tiers per rule:

  machine    a coded check from `checks.py`, bound to the slug it enforces
  advisory   the instruction body, delivered as review context for changed files
             that match its language

Advisory is not a lesser tier, it is the honest one. Around five thousand
instructions exist and roughly a dozen of them can be decided by a checker; the rest
are expertise a reviewer applies. The harness's job is to put the right ones in front
of whoever — or whatever — is reviewing, and to record which ones it put there.

Packs are built once and committed. Compiling during a run would make the policy
digest a function of the working tree, and a policy digest that changes when
`_reviewers/` is edited cannot pin anything.

Derived from the corpus:
  aidlc-workflows-pinned-releases-for-ci — pin what you depend on; a floating
      reference is not a version.
  aidlc-workflows-portable-configuration-standards — the pack is one JSON file with
      an explicit schema, readable without this tool.
  aidlc-workflows-behavior-correct-versionless-docs — drift is detected and named,
      not silently tolerated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .. import SCHEMA_VERSION
from ..digest import digest_json
from ..errors import ConfigError, CorpusError, UsageError
from ..workspace import atomic_write_json, read_json, utc_now
from .checks import CHECKS, Check
from .corpus import Corpus, Instruction
from .findings import ERROR, SEVERITIES, WARNING

MACHINE = "machine"
ADVISORY = "advisory"

# A corpus `language` value maps to the files that language's instructions govern.
# `Other`, `Markdown` and friends deliberately map to `**`: an instruction about
# documentation or configuration applies wherever the change is.
LANGUAGE_SELECTORS: dict[str, tuple[str, ...]] = {
    "python": ("**/*.py", "**/*.pyi"),
    "typescript": ("**/*.ts", "**/*.mts", "**/*.cts"),
    "tsx": ("**/*.tsx",),
    "javascript": ("**/*.js", "**/*.mjs", "**/*.cjs"),
    "jsx": ("**/*.jsx",),
    "go": ("**/*.go",),
    "rust": ("**/*.rs",),
    "java": ("**/*.java",),
    "kotlin": ("**/*.kt", "**/*.kts"),
    "ruby": ("**/*.rb",),
    "php": ("**/*.php",),
    "c": ("**/*.c", "**/*.h"),
    "c++": ("**/*.cc", "**/*.cpp", "**/*.cxx", "**/*.hpp", "**/*.hh"),
    "c#": ("**/*.cs",),
    "cuda": ("**/*.cu", "**/*.cuh"),
    "objective-c": ("**/*.m", "**/*.mm"),
    "swift": ("**/*.swift",),
    "shell": ("**/*.sh", "**/*.bash", "**/*.zsh"),
    "yaml": ("**/*.yml", "**/*.yaml"),
    "json": ("**/*.json",),
    "toml": ("**/*.toml",),
    "xml": ("**/*.xml",),
    "html": ("**/*.html", "**/*.htm"),
    "css": ("**/*.css", "**/*.scss", "**/*.sass"),
    "sql": ("**/*.sql",),
    "dockerfile": ("**/Dockerfile", "**/Dockerfile.*", "**/*.dockerfile"),
    "terraform": ("**/*.tf", "**/*.tfvars"),
    "prisma": ("**/*.prisma",),
    "groovy": ("**/*.groovy", "**/Jenkinsfile"),
    "csv": ("**/*.csv",),
    "mdx": ("**/*.mdx",),
    "markdown": ("**",),
    "txt": ("**",),
    "other": ("**",),
}


def selectors_for_language(language: str) -> tuple[str, ...]:
    return LANGUAGE_SELECTORS.get(language.strip().lower(), ("**",))


@dataclass(frozen=True)
class Rule:
    id: str
    slug: str
    title: str
    topic: str
    language: str
    repository: str
    severity: str
    enforcement: str
    selector: tuple[str, ...]
    instruction_digest: str
    check: str | None = None

    def to_json(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "topic": self.topic,
            "language": self.language,
            "repository": self.repository,
            "severity": self.severity,
            "enforcement": self.enforcement,
            "selector": list(self.selector),
            "instruction_digest": self.instruction_digest,
        }
        if self.check:
            payload["check"] = self.check
        return payload

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Rule":
        try:
            return cls(
                id=str(raw["id"]),
                slug=str(raw["slug"]),
                title=str(raw.get("title", "")),
                topic=str(raw.get("topic", "")),
                language=str(raw.get("language", "")),
                repository=str(raw.get("repository", "")),
                severity=str(raw.get("severity", WARNING)),
                enforcement=str(raw["enforcement"]),
                selector=tuple(str(s) for s in raw.get("selector", ("**",))),
                instruction_digest=str(raw["instruction_digest"]),
                check=str(raw["check"]) if raw.get("check") else None,
            )
        except KeyError as exc:
            raise ConfigError(f"policy rule is missing {exc.args[0]!r}: {raw!r}") from exc


@dataclass
class Pack:
    name: str
    rules: list[Rule] = field(default_factory=list)
    threshold: str = ERROR
    corpus_layout: str = "reviewers"
    corpus_size: int = 0
    created: str = field(default_factory=utc_now)
    schema: int = SCHEMA_VERSION

    def payload(self) -> dict[str, Any]:
        """Canonical, digest-covered form.

        `created` is excluded: a pack rebuilt from the same corpus selection is the
        same policy, and a digest that changed with the clock would invalidate every
        cache entry and make two identical packs look different in an attestation.
        """
        return {
            "schema": self.schema,
            "name": self.name,
            "threshold": self.threshold,
            "corpus": {"layout": self.corpus_layout, "size": self.corpus_size},
            "rules": [rule.to_json() for rule in sorted(self.rules, key=lambda r: r.id)],
        }

    @property
    def digest(self) -> str:
        return digest_json(self.payload())

    @property
    def machine_rules(self) -> list[Rule]:
        return [r for r in self.rules if r.enforcement == MACHINE]

    @property
    def advisory_rules(self) -> list[Rule]:
        return [r for r in self.rules if r.enforcement == ADVISORY]

    def checks(self) -> dict[str, Check]:
        """Resolve machine rules to their check implementations.

        A rule naming a check this build does not have is an error: it means the pack
        was compiled by a newer harness, and running it would enforce less than the
        pack claims while reporting the pack's digest.
        """
        resolved: dict[str, Check] = {}
        for rule in self.machine_rules:
            check = CHECKS.get(rule.check or "")
            if check is None:
                raise ConfigError(
                    f"pack {self.name!r} requires check {rule.check!r}, which this harness "
                    f"({SCHEMA_VERSION}) does not implement",
                    hint="upgrade awesome-harness, or rebuild the pack with this version",
                )
            # The pack's severity wins over the check's default, so a repository can
            # tighten or relax a rule without patching code.
            resolved[check.id] = Check(
                id=check.id,
                slug=check.slug,
                summary=rule.title or check.summary,
                severity=rule.severity,
                selector=tuple(rule.selector) or check.selector,
                engine=check.engine,
            )
        return resolved

    def to_json(self) -> dict[str, Any]:
        return {**self.payload(), "created": self.created, "digest": self.digest}

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Pack":
        schema = raw.get("schema", SCHEMA_VERSION)
        if not isinstance(schema, int) or schema > SCHEMA_VERSION:
            raise ConfigError(
                f"policy pack schema {schema!r} is newer than this harness understands "
                f"(supports {SCHEMA_VERSION})"
            )
        pack = cls(
            name=str(raw.get("name", "")),
            rules=[Rule.from_json(r) for r in raw.get("rules", [])],
            threshold=str(raw.get("threshold", ERROR)),
            corpus_layout=str((raw.get("corpus") or {}).get("layout", "reviewers")),
            corpus_size=int((raw.get("corpus") or {}).get("size", 0)),
            created=str(raw.get("created", "")),
            schema=schema,
        )
        claimed = raw.get("digest")
        if claimed and str(claimed) != pack.digest:
            from ..errors import IntegrityError

            raise IntegrityError(
                f"policy pack {pack.name!r} was modified after it was built: file claims "
                f"{str(claimed)[:19]}, contents hash to {pack.digest[:19]}",
                hint="rebuild the pack with `awesome-harness policy build` rather than editing it",
            )
        return pack

    # ---- drift ----------------------------------------------------------- #

    def drift(self, corpus: Corpus) -> list[dict[str, str]]:
        """Rules whose source instruction changed or vanished since compile time.

        Not an error by itself — the corpus is a living body of work and updates are
        the point. It is an error to *ignore*: a signed attestation says the change
        was gated by this pack, so the pack must be rebuilt deliberately, with the
        new digest recorded, rather than drifting under the signature.
        """
        report: list[dict[str, str]] = []
        for rule in sorted(self.rules, key=lambda r: r.slug):
            try:
                instruction = corpus.get(rule.slug)
            except CorpusError:
                report.append({"slug": rule.slug, "state": "removed", "rule": rule.id})
                continue
            if instruction.digest != rule.instruction_digest:
                report.append(
                    {
                        "slug": rule.slug,
                        "state": "changed",
                        "rule": rule.id,
                        "was": rule.instruction_digest,
                        "now": instruction.digest,
                    }
                )
        return report


def _rule_from_check(check: Check, instruction: Instruction) -> Rule:
    return Rule(
        id=check.id,
        slug=check.slug,
        title=check.summary,
        topic=instruction.topic,
        language=instruction.language,
        repository=instruction.repository,
        severity=check.severity,
        enforcement=MACHINE,
        selector=check.selector,
        instruction_digest=instruction.digest,
        check=check.id,
    )


def _rule_from_instruction(instruction: Instruction, severity: str) -> Rule:
    return Rule(
        id=f"ADV-{instruction.slug}",
        slug=instruction.slug,
        title=instruction.title,
        topic=instruction.topic,
        language=instruction.language,
        repository=instruction.repository,
        severity=severity,
        enforcement=ADVISORY,
        selector=selectors_for_language(instruction.language),
        instruction_digest=instruction.digest,
    )


def build_pack(
    corpus: Corpus,
    *,
    name: str = "default",
    check_ids: Iterable[str] | None = None,
    topics: Iterable[str] = (),
    languages: Iterable[str] = (),
    repositories: Iterable[str] = (),
    slugs: Iterable[str] = (),
    # No cap by default. A pack pins the whole corpus, because that is what makes its
    # digest mean "this policy" rather than "the two hundred most-discussed rules as of
    # whenever this was built". Selection down to what a particular change needs is the
    # bundle's job, not the pack's.
    limit: int | None = None,
    threshold: str = ERROR,
    advisory_severity: str = "info",
) -> Pack:
    """Compile a pack. Every slug is resolved against the corpus or the build fails.

    That resolution is the anti-fiction guard. A check whose slug does not exist
    would still run — and would still report a rule and a URL — while citing
    nothing. Failing the build is the only way the citation stays worth reading.
    """
    if threshold not in SEVERITIES:
        raise UsageError(f"threshold must be one of {', '.join(SEVERITIES)}, got {threshold!r}")

    wanted = set(check_ids) if check_ids is not None else set(CHECKS)
    unknown = sorted(wanted - set(CHECKS))
    if unknown:
        raise UsageError(
            f"unknown check id(s): {', '.join(unknown)}",
            hint=f"available: {', '.join(sorted(CHECKS))}",
        )

    rules: list[Rule] = []
    machine_slugs: set[str] = set()
    for check_id in sorted(wanted):
        check = CHECKS[check_id]
        instruction = corpus.get(check.slug)  # raises CorpusError with near-matches
        rules.append(_rule_from_check(check, instruction))
        machine_slugs.add(check.slug)

    selected = corpus.select(
        slugs=slugs,
        topics=topics,
        languages=languages,
        repositories=repositories,
        limit=limit,
        # With no facet filter, "build a pack from the corpus" means the corpus.
        include_all=not (list(topics) or list(languages) or list(repositories)),
    )
    for instruction in selected:
        if instruction.slug in machine_slugs:
            # Already enforced mechanically; adding it again as context would spend
            # tokens restating a rule the gate already decided.
            continue
        rules.append(_rule_from_instruction(instruction, advisory_severity))

    return Pack(
        name=name,
        rules=rules,
        threshold=threshold,
        corpus_layout=corpus.layout,
        corpus_size=len(corpus),
    )


def pack_path(policy_dir: Path, name: str) -> Path:
    if not name or "/" in name or name.startswith("."):
        raise UsageError(f"invalid pack name {name!r}")
    return policy_dir / f"{name}.pack.json"


def save_pack(policy_dir: Path, pack: Pack) -> Path:
    path = pack_path(policy_dir, pack.name)
    atomic_write_json(path, pack.to_json())
    return path


def load_pack(policy_dir: Path, name: str) -> Pack:
    path = pack_path(policy_dir, name)
    if not path.is_file():
        raise ConfigError(
            f"policy pack {name!r} not found at {path}",
            hint="build it with `awesome-harness policy build` and commit it",
        )
    return Pack.from_json(read_json(path, what="policy pack"))
