"""Path confinement and safe archive extraction.

Every pillar writes somewhere: run folders, the artifact store, the cache, the
ledger. Each of those is a base directory that inputs must not escape, and inputs
here include step-declared output globs, artifact names in a bundle manifest, and
tar member names from a bundle produced on another machine.

Derived from the corpus:
  aidlc-workflows-secure-path-confinement — never use a string prefix check to
      keep a path inside a base directory. `/run/foo` is a prefix of
      `/run/foobar`, and `..` normalizes away only after `resolve()`. Use
      `Path.is_relative_to` on resolved paths.
  aidlc-workflows-secure-scope-and-input-validation — validate at the boundary,
      once, and reject rather than sanitize.
"""

from __future__ import annotations

import os
import tarfile
from pathlib import Path, PurePosixPath

from .errors import HarnessError, UsageError


class PathEscape(HarnessError):
    """A path resolved outside the base directory it was confined to."""

    exit_code = 4
    kind = "path-escape"


def is_within(base: Path, candidate: Path) -> bool:
    """True when `candidate` resolves inside `base`.

    Both sides are resolved first, so `..` segments and symlinks are collapsed
    before the comparison. `is_relative_to` compares path *components*, which is
    why the sibling-prefix bypass (`/run` vs `/runner`) does not apply.
    """
    return candidate.resolve().is_relative_to(base.resolve())


def resolve_within(base: Path, relative: str | os.PathLike[str]) -> Path:
    """Resolve `relative` under `base` or raise.

    Absolute inputs are rejected outright rather than reinterpreted: silently
    re-rooting `/etc/passwd` to `<base>/etc/passwd` would hide a caller bug.
    """
    text = os.fspath(relative)
    if not text:
        raise UsageError("empty path")
    if Path(text).is_absolute():
        raise PathEscape(f"absolute path not allowed here: {text}")
    resolved = (base / text).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise PathEscape(
            f"path escapes {base}: {text}",
            hint="paths are confined to the run folder; use a path relative to it",
        )
    return resolved


def relative_to(base: Path, path: Path) -> str:
    """POSIX-style path of `path` inside `base`. Stable across platforms, because
    it ends up in manifests and cache keys that must match on another machine."""
    if not is_within(base, path):
        raise PathEscape(f"{path} is not inside {base}")
    return path.resolve().relative_to(base.resolve()).as_posix()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


# --------------------------------------------------------------------------- #
# Archive extraction
# --------------------------------------------------------------------------- #

def check_tar_member(member: tarfile.TarInfo, *, allow_symlinks: bool = False) -> None:
    """Reject a tar member that could write outside the destination.

    Bundles are the pillar that crosses machines, which makes them the one input
    reaching this process from somewhere it does not control. The checks are
    deliberately absolute-refusal rather than best-effort rewriting.
    """
    name = member.name
    if name.startswith("/") or PurePosixPath(name).is_absolute():
        raise PathEscape(f"archive member is absolute: {name}")
    if ".." in PurePosixPath(name).parts:
        raise PathEscape(f"archive member escapes with '..': {name}")
    if member.isdev():
        raise PathEscape(f"archive member is a device node: {name}")
    if (member.issym() or member.islnk()) and not allow_symlinks:
        raise PathEscape(f"archive member is a link: {name}")
    if member.issym() or member.islnk():
        target = PurePosixPath(member.linkname)
        if target.is_absolute() or ".." in target.parts:
            raise PathEscape(f"archive link escapes: {name} -> {member.linkname}")


def safe_extract(archive: tarfile.TarFile, dest: Path, *, allow_symlinks: bool = False) -> list[str]:
    """Extract every member into `dest`, validating each name first.

    `filter="data"` is also passed where available (3.11.4+), so the standard
    library's own hardening applies on top of these checks rather than instead of
    them: this function must stay correct on an interpreter without it.
    """
    ensure_dir(dest)
    members = archive.getmembers()
    for member in members:
        check_tar_member(member, allow_symlinks=allow_symlinks)
        # Belt and braces: confirm the joined path really lands inside dest.
        resolved = (dest / member.name).resolve()
        if not resolved.is_relative_to(dest.resolve()):
            raise PathEscape(f"archive member escapes destination: {member.name}")
    try:
        archive.extractall(dest, members=members, filter="data")
    except TypeError:  # interpreter without the extraction filter
        archive.extractall(dest, members=members)
    return [m.name for m in members if m.isfile()]
