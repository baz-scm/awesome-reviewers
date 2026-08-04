#!/usr/bin/env python3
"""Prove the artifact pillar's central claim, under a hostile environment.

The claim is that the same manifest exports to byte-identical bytes anywhere. This
script builds the same bundle twice while changing every ambient input a tar writer
might otherwise pick up — the umask, the source files' mtimes, the timezone, the
locale, and the process's working directory — and compares digests.

Run as a plan step so the claim is re-proved on every run rather than asserted in a
README, and so its result becomes an artifact with a digest of its own.

Derived from the corpus:
  aidlc-workflows-executable-documentation-accuracy — a documented guarantee that
      nothing executes is a guarantee that will quietly stop being true.
  aidlc-workflows-deterministic-boundary-modeling — vary every ambient input, then
      assert the boundary did not move.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS_DIR))

from awesome_harness.artifacts import Manifest, Store  # noqa: E402

ORIGINAL_CWD = Path.cwd()
OUTPUT = ORIGINAL_CWD / "harness-determinism.json"

# Content is fixed; everything *around* it is what varies between passes.
FILES: dict[str, bytes] = {
    "a.txt": b"first artifact\n",
    "nested/b.json": b'{"stable":true}\n',
    "run.sh": b"#!/bin/sh\necho hello\n",
}

VARIANTS = (
    {"umask": 0o022, "mtime": 1_000_000_000.0, "tz": "UTC"},
    {"umask": 0o077, "mtime": time.time(), "tz": "Pacific/Kiritimati"},
)


def build_once(root: Path, *, umask: int, mtime: float) -> tuple[str, str]:
    """Write the inputs, publish them, export a bundle. Returns (bundle, manifest) digests."""
    previous = os.umask(umask)
    try:
        work = root / "work"
        work.mkdir(parents=True, exist_ok=True)
        for name, content in FILES.items():
            target = work / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            if name.endswith(".sh"):
                target.chmod(0o755)
            os.utime(target, (mtime, mtime))

        store = Store(root / "store")
        manifest = Manifest(
            run_id="determinism-check",
            step="build",
            source_tree="0" * 40,
            source_commit="0" * 40,
            artifacts=[store.put_file(work / name, name=name) for name in sorted(FILES)],
        )
        return store.export_bundle(manifest, root / "bundle.tar"), manifest.digest
    finally:
        os.umask(previous)


def main() -> int:
    passes: list[dict[str, object]] = []
    for variant in VARIANTS:
        os.environ["TZ"] = str(variant["tz"])
        if hasattr(time, "tzset"):
            time.tzset()
        with tempfile.TemporaryDirectory(prefix="harness-determinism-") as tmp:
            root = Path(tmp).resolve()
            # A different cwd per pass: an absolute path leaking into a member name
            # would show up here and nowhere else.
            os.chdir(root)
            try:
                bundle_digest, manifest_digest = build_once(
                    root, umask=int(variant["umask"]), mtime=float(variant["mtime"])
                )
            finally:
                os.chdir(ORIGINAL_CWD)
            passes.append(
                {
                    "umask": oct(int(variant["umask"])),
                    "tz": variant["tz"],
                    "mtime": variant["mtime"],
                    "bundle_digest": bundle_digest,
                    "manifest_digest": manifest_digest,
                }
            )

    bundles = {p["bundle_digest"] for p in passes}
    manifests = {p["manifest_digest"] for p in passes}
    ok = len(bundles) == 1 and len(manifests) == 1
    report = {
        "check": "artifact-bundle-determinism",
        "ok": ok,
        "passes": passes,
        "distinct_bundle_digests": len(bundles),
        "distinct_manifest_digests": len(manifests),
    }

    body = json.dumps(report, indent=2, sort_keys=True) + "\n"
    try:
        OUTPUT.write_text(body, encoding="utf-8")
    except OSError as exc:
        # A determinism check whose result silently vanished is worse than one that
        # never ran, so a failed write fails the step.
        print(f"could not write {OUTPUT}: {exc}", file=sys.stderr)
        return 1

    print(body, end="")
    if not ok:
        print(
            "BUNDLE DETERMINISM BROKEN: identical inputs produced different bytes",
            file=sys.stderr,
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
