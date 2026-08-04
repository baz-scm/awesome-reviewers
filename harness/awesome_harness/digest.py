"""One hash function, one canonical serialization.

Five of the six pillars are digests of something: the ledger chains them, the
artifact store is addressed by them, the cache is keyed on them, the attestation
signs over them, and a policy pack is pinned by them. If two code paths in this
package computed a digest of the "same" object differently, every one of those
guarantees would silently degrade to a guess. So there is exactly one way to
serialize and exactly one way to hash, and both live here.

Derived from the corpus:
  aidlc-workflows-deterministic-boundary-modeling — the serialized form is the
      boundary; make it total and order-independent.
  aidlc-workflows-use-correct-null-semantics — absent and empty are different
      inputs and must hash differently, see `digest_tree`.
  azure-sentinel-timeout-aware-chunking (Azure/Azure-Sentinel) — size chunks
      realistically instead of reading a whole input into memory; `CHUNK_BYTES` and
      the streaming `digest_file` come from this.
  apisix-verify-download-integrity (apache/apisix) — hold the expected digest in
      versioned configuration and fail closed on mismatch. `require_digest`
      validating at every boundary is the same instinct applied inward.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

ALGORITHM = "sha256"
PREFIX = f"{ALGORITHM}:"
HEX_LEN = 64

# Artifacts can be large, so files are hashed in chunks and never read whole.
CHUNK_BYTES = 1 << 20

# Chain sentinel for the first ledger record. Not a real digest of anything: it is
# the documented "nothing precedes this" value, and `is_digest` accepts it so the
# genesis record verifies with the same code path as every other record.
ZERO = PREFIX + "0" * HEX_LEN

# Marks an input path that does not exist, so that "file absent" and "file present
# but empty" produce different cache keys. Empty content hashes to a real digest;
# absence has to be its own token or the two collapse.
ABSENT = "absent"


def canonical_json(value: Any) -> bytes:
    """Serialize deterministically: sorted keys, no padding, no NaN.

    `allow_nan=False` matters. Python would otherwise emit `NaN`/`Infinity`, which
    is not JSON, so a record written by us could fail to parse in any other
    language — and a digest over unparseable bytes is not a commitment to
    anything. Failing at write time is the loud option.
    """
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return PREFIX + hashlib.sha256(data).hexdigest()


def digest_text(text: str) -> str:
    return digest_bytes(text.encode("utf-8"))


def digest_json(value: Any) -> str:
    """Digest of an object's canonical form. The pack/manifest/cache-key primitive."""
    return digest_bytes(canonical_json(value))


def digest_file(path: Path) -> str:
    """Streaming digest of a file's contents. Follows symlinks deliberately: the
    artifact store commits to bytes, and the bytes are what the reader gets."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK_BYTES)
            if not block:
                break
            hasher.update(block)
    return PREFIX + hasher.hexdigest()


def digest_of(path: Path) -> str:
    """Digest of a file, or the ABSENT token when it is not there."""
    return digest_file(path) if path.is_file() else ABSENT


def digest_tree(root: Path, relative_paths: Iterable[str]) -> dict[str, str]:
    """Map each relative path to its digest, or to ABSENT.

    Returned as a mapping rather than a single rolled-up hash so that a cache miss
    can be explained ("this input changed") instead of merely reported.
    """
    return {rel: digest_of(root / rel) for rel in sorted(set(relative_paths))}


def digest_set(digests: Iterable[str]) -> str:
    """Order-independent digest over a set of digests.

    Sorted before hashing, so the same inputs discovered in a different order —
    two globs, two filesystems, two walk orders — collapse to one value.
    """
    return digest_json(sorted(set(digests)))


def is_digest(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith(PREFIX):
        return False
    hexpart = value[len(PREFIX) :]
    return len(hexpart) == HEX_LEN and all(c in "0123456789abcdef" for c in hexpart)


def require_digest(value: object, *, field: str = "digest") -> str:
    """Validate before trusting. Every digest crossing a file or process boundary
    goes through here, so a malformed record is rejected at the edge rather than
    compared against later and quietly failing to match."""
    from .errors import IntegrityError

    if not is_digest(value):
        raise IntegrityError(f"{field} is not a well-formed {ALGORITHM} digest: {value!r}")
    return str(value)


def hex_of(value: str) -> str:
    """The bare hex, for filesystem sharding. Assumes a validated digest."""
    return value[len(PREFIX) :]


def short(value: str, length: int = 12) -> str:
    """Human-facing abbreviation. Never used for lookup or comparison."""
    return hex_of(value)[:length] if is_digest(value) else str(value)


def digest_mapping(mapping: Mapping[str, Any]) -> str:
    return digest_json(dict(mapping))
