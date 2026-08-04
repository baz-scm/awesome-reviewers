"""Pillar 6 — machine-enforceable rules, compiled from the Awesome Reviewers corpus.

    corpus.py    read `_reviewers/` or a `raw/` download; resolve slugs or fail
    findings.py  the finding record, its fingerprint, and the gate result
    checks.py    the machine tier: ast-based Python checks plus text/file checks
    pack.py      pinned, digested rule selections — the unit of policy versioning
    engine.py    gate evaluation, waivers, and the advisory context bundle
"""

from __future__ import annotations

from .checks import CHECKS, Check, Context
from .corpus import Corpus, Instruction
from .engine import Waivers, advisory_bundle, build_context, evaluate, render_gate, summary
from .findings import ERROR, INFO, SEVERITIES, WARNING, Finding, GateResult, Waiver
from .pack import ADVISORY, MACHINE, Pack, Rule, build_pack, load_pack, pack_path, save_pack

__all__ = [
    "ADVISORY",
    "CHECKS",
    "ERROR",
    "INFO",
    "MACHINE",
    "SEVERITIES",
    "WARNING",
    "Check",
    "Context",
    "Corpus",
    "Finding",
    "GateResult",
    "Instruction",
    "Pack",
    "Rule",
    "Waiver",
    "Waivers",
    "advisory_bundle",
    "build_context",
    "build_pack",
    "evaluate",
    "load_pack",
    "pack_path",
    "render_gate",
    "save_pack",
    "summary",
]
