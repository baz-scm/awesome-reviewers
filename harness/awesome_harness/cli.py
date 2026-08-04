"""Command line interface.

One entry point per pillar, plus `run` which uses all six. Every command that can
fail does so with its own exit code (see errors.py) rather than a generic 1, because
the primary caller is CI or an agent, and both need to branch on the reason.

`--json` is available on the commands whose output an agent would parse. Human
output goes to stdout, diagnostics to stderr, and the two are never interleaved into
one stream that has to be re-parsed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .artifacts import Manifest, Store
from .cache import Cache
from .digest import short
from .errors import HarnessError, UsageError
from .execution import select_sandbox
from .identity import Signer, commit_trailers, resolve_actor
from .ledger import Ledger
from .paths import ensure_dir
from .plan import Plan, Runner, approval_token
from .policy import (
    CHECKS,
    Corpus,
    Waivers,
    advisory_bundle,
    build_context,
    build_pack,
    evaluate,
    load_pack,
    render_gate,
    save_pack,
)
from .scm import Git
from .verify import verify_attestation
from .workspace import Workspace, atomic_write_bytes, atomic_write_json


# --------------------------------------------------------------------------- #
# init / doctor
# --------------------------------------------------------------------------- #

def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else Workspace.find_root()
    ws = Workspace.open(root, require=False)
    ws.root = root
    created = ws.initialize(corpus=args.corpus)
    print(f"initialized {ws.dir}")
    for path in created:
        print(f"  + {path.relative_to(root)}")
    print(
        "\nnext:\n"
        "  awesome-harness policy build     # compile a pack from the corpus and commit it\n"
        "  awesome-harness gate             # evaluate it against your working change"
    )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Report what is actually available. No inference, no defaults presented as facts."""
    ws = Workspace.open(require=False)
    git = Git(ws.root)
    rows: list[tuple[str, str]] = [
        ("harness", __version__),
        ("python", sys.version.split()[0]),
        ("root", str(ws.root)),
        ("initialized", "yes" if ws.config_path.is_file() else "no — run `awesome-harness init`"),
        ("git repository", "yes" if git.is_repo() else "no"),
    ]
    try:
        sandbox, note = select_sandbox(
            str(ws.setting("execution.backend", "auto")), str(ws.setting("execution.image", ""))
        )
        rows.append(("execution backend", f"{sandbox.name} ({note})"))
    except HarnessError as exc:
        rows.append(("execution backend", f"unusable: {exc}"))

    corpus = Corpus(ws.corpus_path())
    try:
        rows.append(("corpus", f"{len(corpus)} instructions ({corpus.layout} layout) at {corpus.root}"))
    except HarnessError as exc:
        rows.append(("corpus", f"unavailable: {exc}"))

    signer = Signer(key=str(ws.setting("identity.key", "")))
    available, reason = signer.available()
    rows.append(("signing", reason if available else f"unavailable — attestations will be unsigned ({reason})"))

    actor = resolve_actor(ws.root)
    rows.append(("actor", f"{actor.id} ({', '.join(actor.evidence) or 'no evidence'})"))

    if ws.config_path.is_file():
        ledger = Ledger(ws.ledger_dir)
        chain = ledger.verify()
        rows.append(
            ("ledger", f"{chain.count} record(s), chain {'intact' if chain.ok else 'BROKEN: ' + str(chain.reason)}")
        )

    width = max(len(name) for name, _ in rows)
    if args.json:
        print(json.dumps({name: value for name, value in rows}, indent=2, sort_keys=True))
    else:
        for name, value in rows:
            print(f"{name.rjust(width)}  {value}")
    return 0


# --------------------------------------------------------------------------- #
# policy
# --------------------------------------------------------------------------- #

def cmd_policy_build(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    corpus = Corpus(ws.corpus_path())
    pack = build_pack(
        corpus,
        name=args.name,
        check_ids=args.check or None,
        topics=args.topic,
        languages=args.language,
        repositories=args.repository,
        slugs=args.slug,
        limit=args.limit or None,
        threshold=args.threshold,
    )
    path = save_pack(ensure_dir(ws.policy_dir), pack)
    print(
        f"built pack {pack.name!r}: {len(pack.machine_rules)} machine rule(s), "
        f"{len(pack.advisory_rules)} advisory rule(s)"
    )
    print(f"  digest  {pack.digest}")
    print(f"  written {path.relative_to(ws.root)}  — commit this file")
    return 0


def cmd_policy_list(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    packs = sorted(ws.policy_dir.glob("*.pack.json"))
    if not packs:
        print("no policy packs; build one with `awesome-harness policy build`")
        return 0
    for path in packs:
        pack = load_pack(ws.policy_dir, path.name[: -len(".pack.json")])
        print(
            f"{pack.name:<20} {len(pack.machine_rules):>3} machine  "
            f"{len(pack.advisory_rules):>4} advisory  threshold={pack.threshold:<8} {short(pack.digest)}"
        )
    return 0


def cmd_policy_show(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    pack = load_pack(ws.policy_dir, args.name)
    if args.json:
        print(json.dumps(pack.to_json(), indent=2, sort_keys=True))
        return 0
    print(f"pack {pack.name!r}  digest {pack.digest}  threshold {pack.threshold}")
    print(f"compiled against {pack.corpus_size} instructions ({pack.corpus_layout} layout)\n")
    print("machine rules — a coded check, bound to the instruction it enforces")
    for rule in sorted(pack.machine_rules, key=lambda r: r.id):
        print(f"  {rule.id}  {rule.severity:<8} {rule.title}")
        print(f"        from {rule.slug} ({rule.repository or 'unknown'}) {short(rule.instruction_digest)}")
    advisory = sorted(pack.advisory_rules, key=lambda r: (r.topic, r.slug))
    print(f"\nadvisory rules — delivered as review context ({len(advisory)})")
    for rule in advisory if args.all else advisory[:20]:
        print(f"  {rule.topic:<26} {rule.language:<12} {rule.slug}")
    if not args.all and len(advisory) > 20:
        print(f"  ... {len(advisory) - 20} more (use --all)")
    return 0


def cmd_policy_checks(args: argparse.Namespace) -> int:
    """Every machine check and the corpus instruction it came from."""
    if args.json:
        print(json.dumps([c.to_json() for c in CHECKS.values()], indent=2, sort_keys=True))
        return 0
    for check in CHECKS.values():
        print(f"{check.id}  {check.severity:<8} {check.engine:<7} {check.summary}")
        print(f"        {check.slug}")
        print(f"        applies to {', '.join(check.selector)}")
    return 0


def cmd_policy_verify(args: argparse.Namespace) -> int:
    """Report drift between a pack and the corpus it was compiled from."""
    ws = Workspace.open()
    pack = load_pack(ws.policy_dir, args.name)
    drift = pack.drift(Corpus(ws.corpus_path()))
    if not drift:
        print(f"pack {pack.name!r} ({short(pack.digest)}) is current: {len(pack.rules)} rule(s), no drift")
        return 0
    for row in drift:
        if row["state"] == "removed":
            print(f"REMOVED  {row['slug']}  (rule {row['rule']})")
        else:
            print(f"CHANGED  {row['slug']}  {short(row['was'])} -> {short(row['now'])}  (rule {row['rule']})")
    print(
        f"\n{len(drift)} rule(s) drifted. Rebuild with `awesome-harness policy build --name {pack.name}` "
        "so the new digest is recorded deliberately."
    )
    return 9


# --------------------------------------------------------------------------- #
# gate / context
# --------------------------------------------------------------------------- #

def _gate(ws: Workspace, args: argparse.Namespace):  # type: ignore[no-untyped-def]
    git = Git(ws.root)
    pack = load_pack(ws.policy_dir, args.pack or str(ws.setting("policy.pack", "default")))
    ctx = build_context(git, ws.root, args.base)
    result = evaluate(
        pack,
        ctx,
        waivers=Waivers.load(ws.waivers_path),
        threshold=args.threshold or str(ws.setting("policy.threshold", "error")),
    )
    return pack, ctx, result


def cmd_gate(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    pack, ctx, result = _gate(ws, args)
    # Which advisory instructions apply is part of the gate's record even though it is
    # not part of its verdict: a reader needs to know what expertise was on offer.
    _, slugs, notes = advisory_bundle(pack, Corpus(ws.corpus_path()), ctx.files, added=ctx.added)
    result.advisory_slugs = slugs
    result.notes.extend(notes)
    if args.json:
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
    else:
        print(render_gate(result, verbose=args.verbose))
    if args.out:
        atomic_write_json(Path(args.out), result.to_json())
    if result.verdict == "fail" and not args.advisory_only:
        return 3
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    """Emit the advisory instructions matching the current change.

    This is the corpus doing its original job: expertise delivered to whoever reviews
    next. It is an input to review, not evidence about the code, and the gate report
    is kept separate for exactly that reason.
    """
    ws = Workspace.open()
    git = Git(ws.root)
    pack = load_pack(ws.policy_dir, args.pack or str(ws.setting("policy.pack", "default")))
    corpus = Corpus(ws.corpus_path())
    ctx = build_context(git, ws.root, args.base)
    files = list(ctx.files)
    bundle, slugs, notes = advisory_bundle(pack, corpus, files, added=ctx.added)
    if args.out:
        atomic_write_bytes(Path(args.out), bundle.encode("utf-8"))
        print(f"{len(slugs)} instruction(s) for {len(files)} changed file(s) -> {args.out}")
    else:
        sys.stdout.write(bundle)
    for note in notes:
        print(f"note: {note}", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #
# run / approve
# --------------------------------------------------------------------------- #

def cmd_run(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    plan_path = Path(args.plan) if args.plan else ws.root / str(ws.setting("plan", "harness/plans/default.json"))
    plan = Plan.load(plan_path)
    runner = Runner(
        ws,
        base=args.base,
        advisory_only=args.advisory_only,
        approve=(["*"] if args.yes else list(args.approve)),
        no_cache=args.no_cache,
        keep_worktree=args.keep_worktree,
        declared_model=args.model,
    )
    try:
        result = runner.run(plan)
    except HarnessError as exc:
        # The run recorded its own failure in the ledger and wrote an attestation
        # before this propagated; the exit code is what CI reads.
        print(exc.render(), file=sys.stderr)
        return exc.exit_code

    if args.json:
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
        return 0

    print(f"run {result.run_id}  {result.status}")
    print(f"  plan       {result.plan}")
    print(f"  backend    {result.backend_note}")
    if result.snapshot:
        print(f"  snapshot   tree {result.snapshot.tree[:12]} commit {result.snapshot.commit[:12]} ({result.snapshot.ref})")
    for step in result.steps:
        marker = "cached" if step.cached else f"{step.duration_ms} ms"
        print(f"  step       {step.step:<24} exit {step.exit_code}  {marker}  {len(step.outputs)} output(s)")
        if step.note:
            print(f"             {step.note}")
    if result.gate:
        print(
            f"  gate       {result.gate['verdict']}  {result.gate['blocking']} blocking, "
            f"{result.gate['unsuppressed']} reported of {result.gate['total']} finding(s)"
        )
    if result.drift:
        print(f"  drift      {len(result.drift)} pinned instruction(s) changed since the pack was built")
    print(f"  attest     {result.attestation}  ({result.signature})")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    runner = Runner(ws)
    runner.record_approval(args.token, phase=args.phase, run_id=args.run_id or "", note=args.note)
    # harness:allow AH011 - an approval token is a public digest of the thing approved, not a credential
    print(f"recorded approval for phase {args.phase!r} bound to {short(args.token)} as {runner.actor.id}")
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    git = Git(ws.root)
    from .workspace import new_run_id

    run_id = args.id or new_run_id()
    snapshot = git.snapshot(
        run_id, message=args.message or f"awesome-harness snapshot {run_id}", tmp_dir=ws.tmp_dir
    )
    if args.json:
        print(json.dumps({
            "tree": snapshot.tree, "commit": snapshot.commit, "ref": snapshot.ref,
            "parent": snapshot.parent, "changed": list(snapshot.changed),
        }, indent=2, sort_keys=True))
        return 0
    print(f"tree    {snapshot.tree}")
    print(f"commit  {snapshot.commit}")
    print(f"ref     {snapshot.ref}")
    print(f"changed {len(snapshot.changed)} file(s) relative to {snapshot.parent[:12] if snapshot.parent else 'an empty tree'}")
    print(f"\ninspect it with: git show {snapshot.commit[:12]}")
    return 0


def cmd_trailers(args: argparse.Namespace) -> int:
    """Commit trailers for the most recent run, for attribution inside git itself."""
    ws = Workspace.open()
    ledger = Ledger(ws.ledger_dir)
    from .ledger import ATTESTATION_CREATED, RUN_STARTED

    started = ledger.last(RUN_STARTED)
    if started is None:
        raise UsageError("no runs recorded yet")
    attested = ledger.last(ATTESTATION_CREATED, run_id=started.run_id)
    actor = resolve_actor(ws.root)
    for trailer in commit_trailers(
        actor,
        run_id=started.run_id,
        attestation_digest=(attested.body.get("payload_digest") if attested else None),
    ):
        print(trailer)
    return 0


# --------------------------------------------------------------------------- #
# ledger / cache / artifacts
# --------------------------------------------------------------------------- #

def cmd_ledger_show(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    records = Ledger(ws.ledger_dir).read_all()
    if args.run:
        records = [r for r in records if r.run_id == args.run]
    if args.json:
        print(json.dumps([r.to_json() for r in records[-args.limit :]], indent=2, sort_keys=True))
        return 0
    for record in records[-args.limit :]:
        print(record.summary())
    return 0


def cmd_ledger_verify(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    result = Ledger(ws.ledger_dir).verify()
    if args.json:
        print(json.dumps({
            "ok": result.ok, "records": result.count, "head": result.head,
            "broken_at": result.broken_at, "reason": result.reason,
        }, indent=2, sort_keys=True))
    elif result.ok:
        print(f"chain intact: {result.count} record(s), head {result.head}")
    else:
        print(f"CHAIN BROKEN at record {result.broken_at}: {result.reason}", file=sys.stderr)
    return 0 if result.ok else 4


def cmd_ledger_runs(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    rows = Ledger(ws.ledger_dir).runs()
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
        return 0
    for row in rows:
        print(
            f"{row['run_id']:<28} {row.get('status', 'incomplete'):<16} "
            f"gate={row.get('verdict') or '-':<6} {row['records']:>4} record(s)"
        )
    return 0


def cmd_cache_stats(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    store = Store(ws.artifacts_dir)
    cache = Cache(ws.cache_dir, store, enabled=bool(ws.setting("cache.enabled", True)))
    ledger = Ledger(ws.ledger_dir)
    from .ledger import CACHE_HIT, CACHE_MISS

    records = ledger.read_all()
    hits = sum(1 for r in records if r.type == CACHE_HIT)
    misses = sum(1 for r in records if r.type == CACHE_MISS)
    saved = sum(int(r.body.get("saved_ms", 0)) for r in records if r.type == CACHE_HIT)
    blobs, blob_bytes = store.size()
    stats = {
        **cache.stats(),
        # Derived from the ledger rather than a counter file: one source of truth, and
        # the hit rate is auditable against the records that produced it.
        "hits": hits,
        "misses": misses,
        "hit_rate": round(hits / (hits + misses), 3) if (hits + misses) else None,
        "saved_ms": saved,
        "blobs": blobs,
        "blob_bytes": blob_bytes,
    }
    if args.json:
        print(json.dumps(stats, indent=2, sort_keys=True))
        return 0
    print(f"entries    {stats['entries']} ({stats['bytes']} bytes)")
    print(f"blobs      {blobs} ({blob_bytes} bytes)")
    print(f"hits       {hits}  misses {misses}  hit rate {stats['hit_rate']}")
    print(f"time saved {saved} ms of recorded step duration")
    return 0


def cmd_cache_prune(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    cache = Cache(ws.cache_dir, Store(ws.artifacts_dir))
    removed, freed = cache.prune(max_age_days=args.older_than, dry_run=not args.apply)
    verb = "would remove" if not args.apply else "removed"
    print(f"{verb} {removed} cache entr(ies), {freed} bytes")
    if not args.apply:
        print("re-run with --apply to actually delete")
    return 0


def cmd_artifacts_ls(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    store = Store(ws.artifacts_dir)
    count, total = store.size()
    print(f"{count} blob(s), {total} bytes in {store.root}")
    for manifest_path in sorted(ws.runs_dir.glob("*/manifest.json")):
        from .workspace import read_json

        manifest = Manifest.from_json(read_json(manifest_path, what="run manifest"))
        print(f"\nrun {manifest.run_id}  manifest {short(manifest.digest)}  {manifest.total_size} bytes")
        for artifact in sorted(manifest.artifacts, key=lambda a: a.name):
            print(f"  {short(artifact.digest)}  {artifact.size:>9}  {artifact.media_type:<32} {artifact.name}")
    return 0


def cmd_artifacts_export(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    from .workspace import read_json

    manifest_path = ws.runs_dir / args.run / "manifest.json"
    manifest = Manifest.from_json(read_json(manifest_path, what="run manifest"))
    store = Store(ws.artifacts_dir)
    digest = store.export_bundle(manifest, Path(args.output))
    print(f"exported {len(manifest.artifacts)} artifact(s) to {args.output}")
    print(f"  bundle digest   {digest}")
    print(f"  manifest digest {manifest.digest}")
    print("  the same manifest exports byte-identically on any machine")
    return 0


def cmd_artifacts_import(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    store = Store(ws.artifacts_dir)
    manifest = store.import_bundle(Path(args.bundle), scratch=ensure_dir(ws.tmp_dir))
    print(f"imported {len(manifest.artifacts)} artifact(s) from run {manifest.run_id}")
    print(f"  every member re-hashed and matched its manifest entry")
    print(f"  manifest digest {manifest.digest}")
    return 0


def cmd_artifacts_gc(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    from .workspace import read_json

    store = Store(ws.artifacts_dir)
    cache = Cache(ws.cache_dir, store)
    referenced: set[str] = set(cache.referenced_digests())
    for manifest_path in ws.runs_dir.glob("*/manifest.json"):
        manifest = Manifest.from_json(read_json(manifest_path, what="run manifest"))
        referenced.update(a.digest for a in manifest.artifacts)
    count, freed = store.gc(referenced, dry_run=not args.apply)
    verb = "would remove" if not args.apply else "removed"
    print(f"{len(referenced)} referenced blob(s); {verb} {count} unreferenced, {freed} bytes")
    if not args.apply:
        print("re-run with --apply to actually delete")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    ws = Workspace.open()
    path = Path(args.attestation) if args.attestation else _latest_attestation(ws)
    report = verify_attestation(ws, path, check_corpus=not args.no_corpus)
    if args.json:
        print(json.dumps(report.to_json(), indent=2, sort_keys=True))
    else:
        print(report.render())
    if report.failures:
        return 4
    return 0


def _latest_attestation(ws: Workspace) -> Path:
    candidates = sorted(ws.attestations_dir.glob("*.json"))
    if not candidates:
        raise UsageError(
            "no attestations found",
            hint="run `awesome-harness run` first, or pass a path",
        )
    return candidates[-1]


def cmd_approve_token(args: argparse.Namespace) -> int:
    """Print the approval token a phase would require, without running anything."""
    ws = Workspace.open()
    git = Git(ws.root)
    plan = Plan.load(Path(args.plan) if args.plan else ws.root / str(ws.setting("plan", "harness/plans/default.json")))
    pack = load_pack(ws.policy_dir, str(ws.setting("policy.pack", "default")))
    phase = plan.phase(args.phase)
    # A snapshot, not HEAD's tree: the approval must bind to the code as it stands,
    # uncommitted edits included, which is exactly what `run` will snapshot. Taking a
    # snapshot here is cheap and idempotent — identical content yields the same tree.
    ws_snapshot = git.snapshot(
        "approval-probe", message="awesome-harness approval probe", tmp_dir=ws.tmp_dir
    )
    token = approval_token(
        plan_digest=plan.digest, phase=phase.name, tree=ws_snapshot.tree, pack_digest=pack.digest
    )
    # harness:allow AH011 - printing this token is the command's entire purpose; it is a digest
    print(token)
    print(
        f"# bound to plan {plan.name!r} phase {phase.name!r} tree {head_tree[:12]} pack {short(pack.digest)}",
        file=sys.stderr,
    )
    return 0


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awesome-harness",
        description=(
            "A coding harness with six machine-enforced pillars: source control, execution, "
            "artifacts, caching, identity and policy. Policy is compiled from Awesome Reviewers."
        ),
        epilog="exit codes: 0 ok, 2 usage, 3 gate failed, 4 integrity, 5 execution, "
        "6 timeout, 7 backend, 8 approval required, 9 corpus/drift, 78 config",
    )
    parser.add_argument("--version", action="version", version=f"awesome-harness {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create .harness in this repository")
    init.add_argument("--root", help="repository root (default: discovered)")
    init.add_argument("--corpus", help="path to the instruction corpus (default: _reviewers)")
    init.set_defaults(func=cmd_init)

    doctor = sub.add_parser("doctor", help="report what is available and what is not")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    policy = sub.add_parser("policy", help="compile and inspect policy packs").add_subparsers(
        dest="policy_command", required=True
    )

    build = policy.add_parser("build", help="compile a pack from the corpus")
    build.add_argument("--name", default="default")
    build.add_argument("--check", action="append", default=[], metavar="ID", help="machine check to include (default: all)")
    build.add_argument("--topic", action="append", default=[], help="corpus label, e.g. Security")
    build.add_argument("--language", action="append", default=[], help="corpus language, e.g. Python")
    build.add_argument("--repository", action="append", default=[], help="source repository, e.g. awslabs/aidlc-workflows")
    build.add_argument("--slug", action="append", default=[], help="include this instruction explicitly")
    build.add_argument("--limit", type=int, default=0,
                       help="cap advisory rules (0 = the whole corpus, which is the default)")
    build.add_argument("--threshold", default="error", choices=("info", "warning", "error"))
    build.set_defaults(func=cmd_policy_build)

    listing = policy.add_parser("list", help="list committed packs")
    listing.set_defaults(func=cmd_policy_list)

    show = policy.add_parser("show", help="show a pack's rules")
    show.add_argument("name", nargs="?", default="default")
    show.add_argument("--all", action="store_true", help="list every advisory rule")
    show.add_argument("--json", action="store_true")
    show.set_defaults(func=cmd_policy_show)

    checks = policy.add_parser("checks", help="list machine checks and their source instructions")
    checks.add_argument("--json", action="store_true")
    checks.set_defaults(func=cmd_policy_checks)

    pverify = policy.add_parser("verify", help="report drift between a pack and the corpus")
    pverify.add_argument("name", nargs="?", default="default")
    pverify.set_defaults(func=cmd_policy_verify)

    gate = sub.add_parser("gate", help="evaluate the policy gate against a change")
    gate.add_argument("--base", help="compare against this ref (default: HEAD plus working tree)")
    gate.add_argument("--pack")
    gate.add_argument("--threshold", choices=("info", "warning", "error"))
    gate.add_argument("--advisory-only", action="store_true", help="report but never fail")
    gate.add_argument("--verbose", action="store_true", help="include suppressed findings")
    gate.add_argument("--out", help="also write the report as JSON to this path")
    gate.add_argument("--json", action="store_true")
    gate.set_defaults(func=cmd_gate)

    context = sub.add_parser("context", help="emit advisory instructions for the changed files")
    context.add_argument("--base")
    context.add_argument("--pack")
    context.add_argument("--out", help="write to a file instead of stdout")
    context.set_defaults(func=cmd_context)

    run = sub.add_parser("run", help="execute a plan across all six pillars")
    run.add_argument("plan", nargs="?", help="path to a plan JSON (default: config `plan`)")
    run.add_argument("--base")
    run.add_argument("--approve", action="append", default=[], metavar="PHASE")
    run.add_argument("--yes", action="store_true", help="approve every phase that requires it")
    run.add_argument("--advisory-only", action="store_true")
    run.add_argument("--no-cache", action="store_true")
    run.add_argument("--keep-worktree", action="store_true", help="leave the isolated worktree in place")
    run.add_argument("--model", default="", help="record this model id as the acting agent")
    run.add_argument("--json", action="store_true")
    run.set_defaults(func=cmd_run)

    approve = sub.add_parser("approve", help="record a human approval for a phase")
    approve.add_argument("phase")
    approve.add_argument("--token", required=True)
    approve.add_argument("--run-id", default="")
    approve.add_argument("--note", default="")
    approve.set_defaults(func=cmd_approve)

    token = sub.add_parser("approval-token", help="print the token a phase's approval binds to")
    token.add_argument("phase")
    token.add_argument("--plan")
    token.set_defaults(func=cmd_approve_token)

    snapshot = sub.add_parser("snapshot", help="freeze the worktree into immutable git objects")
    snapshot.add_argument("--message", "-m")
    snapshot.add_argument("--id", help="snapshot id (default: a new run id)")
    snapshot.add_argument("--json", action="store_true")
    snapshot.set_defaults(func=cmd_snapshot)

    trailers = sub.add_parser("trailers", help="print commit trailers attributing the last run")
    trailers.set_defaults(func=cmd_trailers)

    ledger = sub.add_parser("ledger", help="inspect the append-only run ledger").add_subparsers(
        dest="ledger_command", required=True
    )
    lshow = ledger.add_parser("show", help="print records")
    lshow.add_argument("--run")
    lshow.add_argument("--limit", type=int, default=40)
    lshow.add_argument("--json", action="store_true")
    lshow.set_defaults(func=cmd_ledger_show)
    lverify = ledger.add_parser("verify", help="recompute the hash chain")
    lverify.add_argument("--json", action="store_true")
    lverify.set_defaults(func=cmd_ledger_verify)
    lruns = ledger.add_parser("runs", help="one row per run")
    lruns.add_argument("--json", action="store_true")
    lruns.set_defaults(func=cmd_ledger_runs)

    cache = sub.add_parser("cache", help="inspect and prune the deterministic cache").add_subparsers(
        dest="cache_command", required=True
    )
    cstats = cache.add_parser("stats", help="entries, blobs and hit rate")
    cstats.add_argument("--json", action="store_true")
    cstats.set_defaults(func=cmd_cache_stats)
    cprune = cache.add_parser("prune", help="drop old entries")
    cprune.add_argument("--older-than", type=float, metavar="DAYS")
    cprune.add_argument("--apply", action="store_true")
    cprune.set_defaults(func=cmd_cache_prune)

    artifacts = sub.add_parser("artifacts", help="content-addressed outputs and bundles").add_subparsers(
        dest="artifacts_command", required=True
    )
    als = artifacts.add_parser("ls", help="list stored artifacts by run")
    als.set_defaults(func=cmd_artifacts_ls)
    aexport = artifacts.add_parser("export", help="write a deterministic bundle")
    aexport.add_argument("run")
    aexport.add_argument("output")
    aexport.set_defaults(func=cmd_artifacts_export)
    aimport = artifacts.add_parser("import", help="ingest and verify a bundle")
    aimport.add_argument("bundle")
    aimport.set_defaults(func=cmd_artifacts_import)
    agc = artifacts.add_parser("gc", help="drop unreferenced blobs")
    agc.add_argument("--apply", action="store_true")
    agc.set_defaults(func=cmd_artifacts_gc)

    verify = sub.add_parser("verify", help="verify an attestation end to end")
    verify.add_argument("attestation", nargs="?", help="default: the most recent one")
    verify.add_argument("--no-corpus", action="store_true", help="skip the corpus drift check")
    verify.add_argument("--json", action="store_true")
    verify.set_defaults(func=cmd_verify)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except HarnessError as exc:
        print(exc.render(), file=sys.stderr)
        return exc.exit_code
    except BrokenPipeError:
        # `| head` is a normal way to use this tool, not an error worth a traceback.
        return 0
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
