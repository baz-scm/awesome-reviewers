"""Pillar 3 — reproducible artifacts that survive leaving this machine.

An artifact store is easy. An artifact store whose output is *byte-identical* when
two machines build the same inputs is the part that makes provenance worth
signing, because it lets a third party rebuild and compare rather than trust.

Three mechanisms:

  content addressing   a blob lives at `sha256/<ab>/<rest>`; its name is its hash,
                       so publishing twice is idempotent and a corrupted read is
                       detectable rather than merely unlucky
  manifests            the logical view — names, sizes, media types, modes, the
                       step and source tree that produced them — digested as a
                       whole, so one digest commits to the entire output set
  deterministic tar    every field that a normal tar fills in from the ambient
                       system (mtime, uid, gid, uname, gname, member order,
                       non-exec permission bits) is pinned to a constant

Derived from the corpus:
  aidlc-workflows-no-silent-null-artifacts — publishing a zero-byte artifact is
      an error unless the step declared that it may be empty. A silent empty
      output is the failure mode that reaches production looking like success.
  aidlc-workflows-deterministic-boundary-modeling — the bundle is a boundary; pin
      every field a reader could observe.
  aidlc-workflows-secure-path-confinement — member names in an imported bundle are
      untrusted input (see paths.safe_extract).
"""

from __future__ import annotations

import mimetypes
import shutil
import tarfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import SCHEMA_VERSION
from .digest import canonical_json, digest_bytes, digest_file, digest_json, hex_of, require_digest
from .errors import HarnessError, IntegrityError, UsageError
from .paths import ensure_dir, resolve_within, safe_extract
from .workspace import atomic_write_bytes, utc_now

DEFAULT_MEDIA_TYPE = "application/octet-stream"

# Tar members are written with these fixed values. `0` rather than a build
# timestamp: SOURCE_DATE_EPOCH's default is exactly this, and anything derived from
# the clock makes two identical builds produce two different bundles.
FIXED_MTIME = 0
FIXED_OWNER = 0
FIXED_OWNER_NAME = ""

MANIFEST_MEMBER = "manifest.json"
PAYLOAD_PREFIX = "artifacts/"


class EmptyArtifact(HarnessError):
    """A step produced a zero-byte output without declaring that it might."""

    exit_code = 10
    kind = "empty-artifact"


@dataclass(frozen=True)
class Artifact:
    name: str
    digest: str
    size: int
    media_type: str
    # Only the executable bit is carried. Preserving the full mode would import the
    # producing machine's umask into the bundle and break reproducibility.
    executable: bool = False

    @property
    def mode(self) -> int:
        return 0o755 if self.executable else 0o644

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Artifact":
        return cls(
            name=str(raw["name"]),
            digest=require_digest(raw["digest"], field="artifact digest"),
            size=int(raw["size"]),
            media_type=str(raw.get("media_type", DEFAULT_MEDIA_TYPE)),
            executable=bool(raw.get("executable", False)),
        )


@dataclass
class Manifest:
    """The logical output set of one step, or of a whole run."""

    run_id: str
    step: str
    source_tree: str | None = None
    source_commit: str | None = None
    created: str = field(default_factory=utc_now)
    artifacts: list[Artifact] = field(default_factory=list)
    schema: int = SCHEMA_VERSION

    def payload(self) -> dict[str, Any]:
        """Canonical form. `created` is excluded from the digest on purpose.

        The digest must identify *content*, so that the same inputs built an hour
        apart produce the same manifest digest and therefore the same cache hit and
        the same bundle. The timestamp stays in the file for humans.
        """
        return {
            "schema": self.schema,
            "run_id": self.run_id,
            "step": self.step,
            "source_tree": self.source_tree,
            "source_commit": self.source_commit,
            "artifacts": [a.to_json() for a in sorted(self.artifacts, key=lambda a: a.name)],
        }

    @property
    def digest(self) -> str:
        return digest_json(self.payload())

    @property
    def total_size(self) -> int:
        return sum(a.size for a in self.artifacts)

    def to_json(self) -> dict[str, Any]:
        return {**self.payload(), "created": self.created, "digest": self.digest}

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Manifest":
        schema = raw.get("schema", SCHEMA_VERSION)
        if not isinstance(schema, int) or schema > SCHEMA_VERSION:
            raise IntegrityError(f"manifest schema {schema!r} is newer than this harness understands")
        manifest = cls(
            run_id=str(raw.get("run_id", "")),
            step=str(raw.get("step", "")),
            source_tree=raw.get("source_tree"),
            source_commit=raw.get("source_commit"),
            created=str(raw.get("created", "")),
            artifacts=[Artifact.from_json(a) for a in raw.get("artifacts", [])],
            schema=schema,
        )
        claimed = raw.get("digest")
        if claimed and claimed != manifest.digest:
            raise IntegrityError(
                f"manifest digest mismatch: file claims {str(claimed)[:19]}, "
                f"contents hash to {manifest.digest[:19]}"
            )
        return manifest


class Store:
    """Content-addressed blob store rooted at `.harness/artifacts`."""

    def __init__(self, root: Path) -> None:
        self.root = ensure_dir(root)

    def blob_path(self, digest: str) -> Path:
        hexpart = hex_of(require_digest(digest))
        return self.root / "sha256" / hexpart[:2] / hexpart[2:]

    def has(self, digest: str) -> bool:
        return self.blob_path(digest).is_file()

    # ---- writing --------------------------------------------------------- #

    def put_file(
        self,
        source: Path,
        *,
        name: str,
        media_type: str | None = None,
        allow_empty: bool = False,
    ) -> Artifact:
        """Copy a produced file into the store and describe it.

        Idempotent: a blob that already exists is left alone rather than rewritten,
        because its name is its hash and rewriting could only ever replace correct
        bytes with the same correct bytes — or, if they differed, with wrong ones.
        """
        if not source.is_file():
            raise EmptyArtifact(
                f"declared output is missing: {name}",
                hint="the step exited successfully but did not produce this path",
            )
        size = source.stat().st_size
        if size == 0 and not allow_empty:
            raise EmptyArtifact(
                f"artifact {name!r} is zero bytes",
                hint='set "allow_empty": true on the output if an empty file is a valid result',
            )
        digest = digest_file(source)
        target = self.blob_path(digest)
        if not target.exists():
            ensure_dir(target.parent)
            tmp = target.parent / f".{target.name}.tmp"
            try:
                shutil.copyfile(source, tmp)
                tmp.replace(target)
            except BaseException:
                tmp.unlink(missing_ok=True)
                raise
            target.chmod(0o444)  # blobs are immutable; make that hard to forget
        return Artifact(
            name=name,
            digest=digest,
            size=size,
            media_type=media_type or _guess_media_type(name),
            executable=bool(source.stat().st_mode & 0o111),
        )

    def put_bytes(self, data: bytes, *, name: str, media_type: str | None = None) -> Artifact:
        tmp = ensure_dir(self.root / "incoming") / f"{name.replace('/', '_')}.tmp"
        try:
            atomic_write_bytes(tmp, data)
            return self.put_file(tmp, name=name, media_type=media_type, allow_empty=True)
        finally:
            tmp.unlink(missing_ok=True)

    # ---- reading --------------------------------------------------------- #

    def read_bytes(self, digest: str, *, verify: bool = True) -> bytes:
        """Read a blob, re-hashing it by default.

        Verification on read is what turns "we recorded a digest" into "the bytes
        are the bytes". It costs a hash of data already in page cache, and it is
        the only thing standing between disk corruption and a signed attestation
        over content that no longer exists.
        """
        path = self.blob_path(digest)
        if not path.is_file():
            raise IntegrityError(f"blob missing from store: {digest}")
        data = path.read_bytes()
        if verify:
            recomputed = digest_bytes(data)
            if recomputed != digest:
                raise IntegrityError(
                    f"blob is corrupt: {path} hashes to {recomputed[:19]}, expected {digest[:19]}"
                )
        return data

    def materialize(self, manifest: Manifest, dest: Path, *, verify: bool = True) -> list[Path]:
        """Write a manifest's artifacts back out under `dest`."""
        written: list[Path] = []
        for artifact in sorted(manifest.artifacts, key=lambda a: a.name):
            target = resolve_within(ensure_dir(dest), artifact.name)
            ensure_dir(target.parent)
            atomic_write_bytes(target, self.read_bytes(artifact.digest, verify=verify), mode=artifact.mode)
            written.append(target)
        return written

    # ---- bundles --------------------------------------------------------- #

    def export_bundle(self, manifest: Manifest, output: Path) -> str:
        """Write a bundle and return its own digest.

        Same manifest, same bytes — on any machine, under any umask, in any
        timezone, with any locale. That is the whole contract, and it is why every
        TarInfo field is assigned rather than defaulted.
        """
        ensure_dir(output.parent)
        tmp = output.parent / f".{output.name}.tmp"
        try:
            # GNU_FORMAT with explicit fields; PAX would add per-member headers whose
            # content depends on the writing implementation.
            with tarfile.open(tmp, "w", format=tarfile.GNU_FORMAT) as tar:
                manifest_bytes = _manifest_bytes(manifest)
                _add_member(tar, MANIFEST_MEMBER, manifest_bytes, executable=False)
                for artifact in sorted(manifest.artifacts, key=lambda a: a.name):
                    blob = self.blob_path(artifact.digest)
                    if not blob.is_file():
                        raise IntegrityError(
                            f"cannot export {artifact.name}: blob {artifact.digest[:19]} is not in the store"
                        )
                    info = tarfile.TarInfo(name=PAYLOAD_PREFIX + artifact.name)
                    info.size = artifact.size
                    info.mode = artifact.mode
                    info.mtime = FIXED_MTIME
                    info.uid = info.gid = FIXED_OWNER
                    info.uname = info.gname = FIXED_OWNER_NAME
                    info.type = tarfile.REGTYPE
                    with open(blob, "rb") as handle:
                        tar.addfile(info, handle)
            tmp.replace(output)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
        return digest_file(output)

    def import_bundle(self, bundle: Path, *, scratch: Path) -> Manifest:
        """Ingest a bundle produced elsewhere, verifying every artifact.

        The manifest in the bundle is a claim, not a fact. Each member is hashed
        after extraction and compared to the digest the manifest asserts, and an
        artifact the manifest does not mention is rejected rather than ignored —
        an unlisted member is how you smuggle a file into a "verified" bundle.
        """
        if not bundle.is_file():
            raise UsageError(f"bundle not found: {bundle}")
        work = ensure_dir(scratch / f"import-{bundle.stem}")
        try:
            with tarfile.open(bundle, "r:*") as tar:
                safe_extract(tar, work)
            manifest_path = work / MANIFEST_MEMBER
            if not manifest_path.is_file():
                raise IntegrityError(f"bundle has no {MANIFEST_MEMBER}: {bundle}")
            import json

            manifest = Manifest.from_json(json.loads(manifest_path.read_text(encoding="utf-8")))

            payload_root = work / PAYLOAD_PREFIX.rstrip("/")
            expected = {a.name: a for a in manifest.artifacts}
            found = sorted(
                p.relative_to(payload_root).as_posix()
                for p in payload_root.rglob("*")
                if p.is_file()
            ) if payload_root.exists() else []

            unlisted = sorted(set(found) - set(expected))
            if unlisted:
                raise IntegrityError(
                    f"bundle contains {len(unlisted)} member(s) absent from its manifest: "
                    f"{', '.join(unlisted[:5])}"
                )
            missing = sorted(set(expected) - set(found))
            if missing:
                raise IntegrityError(
                    f"bundle manifest lists {len(missing)} member(s) not present: "
                    f"{', '.join(missing[:5])}"
                )

            for name, artifact in sorted(expected.items()):
                extracted = payload_root / name
                actual = digest_file(extracted)
                if actual != artifact.digest:
                    raise IntegrityError(
                        f"bundle member {name} hashes to {actual[:19]}, "
                        f"manifest claims {artifact.digest[:19]}"
                    )
                self.put_file(
                    extracted, name=name, media_type=artifact.media_type, allow_empty=True
                )
            return manifest
        finally:
            shutil.rmtree(work, ignore_errors=True)

    # ---- housekeeping ---------------------------------------------------- #

    def iter_blobs(self) -> Iterator[Path]:
        base = self.root / "sha256"
        if base.is_dir():
            for shard in sorted(base.iterdir()):
                if shard.is_dir():
                    yield from sorted(p for p in shard.iterdir() if p.is_file())

    def gc(self, referenced: Iterable[str], *, dry_run: bool = True) -> tuple[int, int]:
        """Drop blobs no manifest points at. Returns `(count, bytes)`.

        `dry_run` defaults to True: the store is the only copy of a build output,
        and a garbage collector whose default is to delete is a garbage collector
        that eventually deletes the wrong thing.
        """
        keep = {hex_of(require_digest(d)) for d in referenced}
        count = 0
        freed = 0
        for blob in self.iter_blobs():
            if blob.parent.name + blob.name in keep:
                continue
            freed += blob.stat().st_size
            count += 1
            if not dry_run:
                blob.chmod(0o644)
                blob.unlink()
        return count, freed

    def size(self) -> tuple[int, int]:
        count = 0
        total = 0
        for blob in self.iter_blobs():
            count += 1
            total += blob.stat().st_size
        return count, total


def _manifest_bytes(manifest: Manifest) -> bytes:
    return canonical_json(manifest.to_json()) + b"\n"


def _add_member(tar: tarfile.TarFile, name: str, data: bytes, *, executable: bool) -> None:
    import io

    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mode = 0o755 if executable else 0o644
    info.mtime = FIXED_MTIME
    info.uid = info.gid = FIXED_OWNER
    info.uname = info.gname = FIXED_OWNER_NAME
    info.type = tarfile.REGTYPE
    tar.addfile(info, io.BytesIO(data))


def _guess_media_type(name: str) -> str:
    guessed, encoding = mimetypes.guess_type(name)
    if encoding == "gzip":
        return "application/gzip"
    if guessed:
        return f"{guessed}; charset=utf-8" if guessed.startswith("text/") else guessed
    # Common build outputs mimetypes does not know about.
    suffix = Path(name).suffix.lower()
    return {
        ".jsonl": "application/x-ndjson",
        ".log": "text/plain; charset=utf-8",
        ".md": "text/markdown; charset=utf-8",
        ".sarif": "application/sarif+json",
        ".whl": "application/zip",
    }.get(suffix, DEFAULT_MEDIA_TYPE)
