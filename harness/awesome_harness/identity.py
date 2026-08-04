"""Pillar 5 — proving who or what produced code.

The whole pillar turns on one distinction that most provenance tooling blurs:

  a **claim** is what the environment says — `git config user.email`, `CLAUDECODE=1`,
  `GITHUB_ACTOR`. Every one of those is writable by whoever runs the process.

  a **proof** is a signature that verifies against a key listed in an
  allowed-signers file.

An attestation records both, in separate fields, and never promotes one to the
other. `verify` reports `valid`, `invalid`, `unsigned` or `unverifiable`, and there
is no code path that returns `valid` without a signature having been checked. The
harness would rather emit an attestation that admits it is unsigned than one that
implies an identity it cannot demonstrate — an unsigned record is merely weak,
whereas a fabricated one poisons every record beside it.

The statement follows in-toto Statement v1 with a harness-specific predicate, so
the shape is familiar to existing verifiers. Note the digest algorithm labels: git
object ids are `sha1` (or `sha256` in a sha256 repository) and are labelled as such,
while artifact and manifest digests are `sha256`. Mislabelling those would make a
verifier compare a git oid against a content hash and conclude, correctly but
uselessly, that nothing matches.

Derived from the corpus:
  aidlc-workflows-security-trust-boundaries — an environment variable crossing into
      a security decision is untrusted input.
  aidlc-workflows-fail-loudly-degrade-safely — no signer configured is a reported,
      labelled state, not a silent downgrade.
  aidlc-workflows-secure-scope-and-input-validation — verify before trusting: the
      payload is parsed from the envelope it was signed over, never from a
      convenient copy beside it.
"""

from __future__ import annotations

import base64
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from . import SCHEMA_VERSION, __version__
from .digest import canonical_json, digest_bytes, is_digest
from .errors import ConfigError, HarnessError
from .paths import ensure_dir
from .workspace import atomic_write_bytes, read_json

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "https://awesomereviewers.com/harness/provenance/v1"
PAYLOAD_TYPE = "application/vnd.in-toto+json"
DEFAULT_NAMESPACE = "awesome-harness"

SIGNATURE_VALID = "valid"
SIGNATURE_INVALID = "invalid"
SIGNATURE_UNSIGNED = "unsigned"
SIGNATURE_UNVERIFIABLE = "unverifiable"

# Environment variables that indicate an agent is driving. Each is a *claim*; the
# attestation records which variable was observed so a reader can judge it.
AGENT_MARKERS: tuple[tuple[str, str], ...] = (
    ("CLAUDECODE", "claude-code"),
    ("CLAUDE_CODE_SESSION_ID", "claude-code"),
    ("CURSOR_TRACE_ID", "cursor"),
    ("AIDER_MODEL", "aider"),
    ("GITHUB_COPILOT_AGENT", "copilot"),
    ("AMAZON_Q_SESSION", "amazon-q"),
    ("KIRO_SESSION", "kiro"),
    ("AWESOME_HARNESS_AGENT", "declared"),
)

CI_MARKERS: tuple[tuple[str, str], ...] = (
    ("GITHUB_ACTIONS", "github-actions"),
    ("GITLAB_CI", "gitlab-ci"),
    ("BUILDKITE", "buildkite"),
    ("CIRCLECI", "circleci"),
    ("JENKINS_URL", "jenkins"),
)


@dataclass
class Actor:
    """Who or what ran this. Every field is a claim unless a signature says otherwise."""

    kind: str  # "agent" | "ci" | "human"
    id: str
    name: str = ""
    email: str = ""
    agent: dict[str, Any] | None = None
    ci: dict[str, Any] | None = None
    # How each fact was learned, so a reader can weigh it.
    evidence: list[str] = field(default_factory=list)
    harness: str = __version__

    def to_json(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v not in (None, "", [])}


def _git_config(root: Path, key: str) -> str:
    try:
        probe = subprocess.run(  # noqa: S603
            ["git", "config", "--get", key], cwd=root, capture_output=True, text=True, timeout=15
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    return probe.stdout.strip() if probe.returncode == 0 else ""


def resolve_actor(root: Path, *, declared_model: str = "", declared_kind: str = "") -> Actor:
    """Work out the actor from the environment, recording the evidence for each fact.

    Precedence is agent, then CI, then human, because an agent running inside CI is
    still the thing that wrote the code — and that is the question this pillar
    exists to answer.
    """
    evidence: list[str] = []
    name = _git_config(root, "user.name")
    email = _git_config(root, "user.email")
    if name or email:
        evidence.append("git config user.name/user.email")

    agent: dict[str, Any] | None = None
    for variable, tool in AGENT_MARKERS:
        if os.environ.get(variable):
            agent = {
                "tool": tool,
                "model": declared_model or os.environ.get("AWESOME_HARNESS_MODEL", ""),
                "session": os.environ.get("CLAUDE_CODE_SESSION_ID", "") or os.environ.get("AWESOME_HARNESS_SESSION", ""),
                "observed_via": variable,
            }
            evidence.append(f"environment marker {variable}")
            break
    if declared_model and agent is None:
        agent = {"tool": "declared", "model": declared_model, "observed_via": "--model"}
        evidence.append("--model on the command line")

    ci: dict[str, Any] | None = None
    for variable, provider in CI_MARKERS:
        if os.environ.get(variable):
            ci = {
                "provider": provider,
                "run_id": os.environ.get("GITHUB_RUN_ID") or os.environ.get("CI_PIPELINE_ID", ""),
                "workflow": os.environ.get("GITHUB_WORKFLOW") or os.environ.get("CI_JOB_NAME", ""),
                "ref": os.environ.get("GITHUB_REF") or os.environ.get("CI_COMMIT_REF_NAME", ""),
                "repository": os.environ.get("GITHUB_REPOSITORY") or os.environ.get("CI_PROJECT_PATH", ""),
                "actor": os.environ.get("GITHUB_ACTOR") or os.environ.get("GITLAB_USER_LOGIN", ""),
                # Presence only. A token's *value* never enters an attestation, and
                # its presence is the only part that is safe to record.
                "oidc_available": bool(os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")),
                "observed_via": variable,
            }
            evidence.append(f"environment marker {variable}")
            break

    kind = declared_kind or ("agent" if agent else "ci" if ci else "human")
    if declared_kind:
        evidence.append("--actor-kind on the command line")

    identifier = (
        f"agent:{agent['tool']}"
        if kind == "agent" and agent
        else f"ci:{ci['provider']}:{ci.get('actor') or '?'}"
        if kind == "ci" and ci
        else f"human:{email or name or 'unknown'}"
    )
    return Actor(kind=kind, id=identifier, name=name, email=email, agent=agent, ci=ci, evidence=evidence)


def commit_trailers(actor: Actor, *, run_id: str, attestation_digest: str | None = None) -> list[str]:
    """Trailers to attach to a commit so attribution survives in git itself.

    Trailers and not a commit-message convention: `git interpret-trailers` parses
    them, forges and hosts display them, and `git log --format=%(trailers)` can
    audit them years later.
    """
    trailers = [f"Harness-Run-Id: {run_id}", f"Harness-Actor: {actor.id}"]
    if actor.agent and actor.agent.get("model"):
        trailers.append(f"Harness-Agent-Model: {actor.agent['model']}")
    if attestation_digest:
        trailers.append(f"Harness-Attestation: {attestation_digest}")
    return trailers


# --------------------------------------------------------------------------- #
# Statement
# --------------------------------------------------------------------------- #

def build_statement(
    *,
    run_id: str,
    subjects: list[dict[str, Any]],
    plan: dict[str, Any],
    actor: Actor,
    scm: dict[str, Any],
    policy: dict[str, Any],
    steps: list[dict[str, Any]],
    isolation: dict[str, Any],
    ledger_head: str,
    started: str,
    finished: str | None = None,
) -> dict[str, Any]:
    """Assemble the in-toto statement. Pure: no clock, no filesystem, no environment.

    Pure on purpose. This is the object that gets signed, so it must be a function of
    values the caller already recorded in the ledger; if it reached for the clock or
    the environment itself, the signed statement could describe a world different
    from the one the ledger witnessed.
    """
    return {
        "_type": STATEMENT_TYPE,
        "subject": subjects,
        "predicateType": PREDICATE_TYPE,
        "predicate": {
            "schema": SCHEMA_VERSION,
            "buildDefinition": {
                "buildType": "https://awesomereviewers.com/harness/plan/v1",
                "externalParameters": plan,
                "internalParameters": {
                    "harness": __version__,
                    "isolation": isolation,
                },
                "resolvedDependencies": _dependencies(scm),
            },
            "runDetails": {
                "builder": {"id": "https://awesomereviewers.com/harness", "version": {"awesome-harness": __version__}},
                "metadata": {"invocationId": run_id, "startedOn": started, "finishedOn": finished or ""},
                "byproducts": [{"name": "ledger-head", "digest": {"sha256": _bare(ledger_head)}}],
            },
            # First-class, not a byproduct: the point of the harness is that the
            # policy version which gated the change is part of its provenance.
            "policy": policy,
            "actor": actor.to_json(),
            "steps": steps,
        },
    }


def _bare(digest: str) -> str:
    return digest.split(":", 1)[1] if ":" in digest else digest


def _dependencies(scm: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolved dependencies, with git oids labelled by their real algorithm.

    A git commit id is sha1 in almost every repository in existence. Labelling it
    `sha256` because everything else here is sha256 would produce a statement that
    is syntactically fine and semantically nonsense.
    """
    deps: list[dict[str, Any]] = []
    algorithm = "sha256" if len(str(scm.get("head") or "")) == 64 else "sha1"
    if scm.get("head"):
        deps.append(
            {
                "uri": scm.get("origin") or "git+file://.",
                "digest": {algorithm: scm["head"]},
                "annotations": {"role": "head", "branch": scm.get("branch", "")},
            }
        )
    if scm.get("snapshot_commit"):
        deps.append(
            {
                "uri": f"git+file://.#{scm.get('snapshot_ref', '')}",
                "digest": {algorithm: scm["snapshot_commit"]},
                "annotations": {"role": "snapshot", "tree": scm.get("snapshot_tree", "")},
            }
        )
    return deps


# --------------------------------------------------------------------------- #
# Envelope and signing
# --------------------------------------------------------------------------- #

@dataclass
class Envelope:
    """DSSE-shaped envelope: the signature covers the payload bytes, not a re-render."""

    payload: bytes
    signatures: list[dict[str, str]] = field(default_factory=list)
    unsigned_reason: str = ""

    @property
    def digest(self) -> str:
        return digest_bytes(self.payload)

    def to_json(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "payloadType": PAYLOAD_TYPE,
            "payload": base64.b64encode(self.payload).decode("ascii"),
            "signatures": self.signatures,
            "payloadDigest": self.digest,
        }
        if not self.signatures:
            # Stated in the file itself, so a reader who never runs `verify` still
            # cannot mistake this for a signed record.
            body["signatureStatus"] = SIGNATURE_UNSIGNED
            body["unsignedReason"] = self.unsigned_reason or "no signer configured"
        return body

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "Envelope":
        if raw.get("payloadType") != PAYLOAD_TYPE:
            raise ConfigError(f"unexpected payloadType {raw.get('payloadType')!r}")
        try:
            payload = base64.b64decode(str(raw["payload"]), validate=True)
        except (KeyError, ValueError) as exc:
            raise ConfigError(f"attestation payload is not valid base64: {exc}") from exc
        claimed = raw.get("payloadDigest")
        envelope = cls(
            payload=payload,
            signatures=list(raw.get("signatures") or []),
            unsigned_reason=str(raw.get("unsignedReason", "")),
        )
        if claimed and is_digest(str(claimed)) and str(claimed) != envelope.digest:
            from .errors import IntegrityError

            raise IntegrityError(
                f"attestation payloadDigest {str(claimed)[:19]} does not match its payload "
                f"({envelope.digest[:19]})"
            )
        return envelope

    def statement(self) -> dict[str, Any]:
        import json

        return json.loads(self.payload.decode("utf-8"))


class Signer:
    """`ssh-keygen -Y` based signing. The only signer, and it either works or says so."""

    def __init__(self, *, key: str = "", namespace: str = DEFAULT_NAMESPACE) -> None:
        self.key = os.path.expanduser(key) if key else ""
        self.namespace = namespace or DEFAULT_NAMESPACE

    def available(self) -> tuple[bool, str]:
        if not shutil.which("ssh-keygen"):
            return False, "ssh-keygen is not on PATH"
        if not self.key:
            return False, "identity.key is not configured"
        if not Path(self.key).is_file():
            return False, f"signing key not found: {self.key}"
        return True, f"ssh-keygen with {self.key}"

    def fingerprint(self) -> str:
        probe = subprocess.run(  # noqa: S603
            ["ssh-keygen", "-lf", self.key], capture_output=True, text=True, timeout=20
        )
        if probe.returncode != 0:
            return ""
        parts = probe.stdout.split()
        return parts[1] if len(parts) > 1 else ""

    def sign(self, payload: bytes, *, scratch: Path) -> Envelope:
        available, reason = self.available()
        if not available:
            return Envelope(payload=payload, unsigned_reason=reason)
        ensure_dir(scratch)
        target = scratch / "attestation.payload"
        atomic_write_bytes(target, payload, mode=0o600)
        signature_path = Path(f"{target}.sig")
        signature_path.unlink(missing_ok=True)
        probe = subprocess.run(  # noqa: S603
            ["ssh-keygen", "-Y", "sign", "-f", self.key, "-n", self.namespace, str(target)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if probe.returncode != 0 or not signature_path.is_file():
            detail = (probe.stderr or probe.stdout or "").strip().splitlines()
            # Failing to sign does not fail the run, but it does downgrade the
            # record, visibly and with the reason attached.
            return Envelope(
                payload=payload,
                unsigned_reason=f"ssh-keygen sign failed: {detail[0] if detail else '?'}",
            )
        armored = signature_path.read_text(encoding="utf-8")
        signature_path.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        return Envelope(
            payload=payload,
            signatures=[
                {
                    "format": "ssh-signature",
                    "namespace": self.namespace,
                    "keyid": self.fingerprint(),
                    "sig": armored,
                }
            ],
        )


@dataclass
class Verification:
    signature: str
    checks: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.signature == SIGNATURE_VALID and all(c.get("ok") for c in self.checks)

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"check": name, "ok": ok, "detail": detail})


def verify_signature(
    envelope: Envelope,
    *,
    allowed_signers: Path,
    identity: str,
    namespace: str = DEFAULT_NAMESPACE,
    scratch: Path,
) -> tuple[str, str]:
    """Check the envelope's signature. Returns `(status, detail)`.

    `unverifiable` and `invalid` are different answers and are kept different:
    "I cannot check this" must never be reported as "this is fine", and it must
    equally never be reported as "this is forged".
    """
    if not envelope.signatures:
        return SIGNATURE_UNSIGNED, envelope.unsigned_reason or "no signatures present"
    if not shutil.which("ssh-keygen"):
        return SIGNATURE_UNVERIFIABLE, "ssh-keygen is not on PATH"
    if not allowed_signers.is_file():
        return SIGNATURE_UNVERIFIABLE, f"allowed signers file not found: {allowed_signers}"

    ensure_dir(scratch)
    signature_path = scratch / "verify.sig"
    atomic_write_bytes(signature_path, envelope.signatures[0].get("sig", "").encode("utf-8"))
    try:
        probe = subprocess.run(  # noqa: S603
            [
                "ssh-keygen",
                "-Y",
                "verify",
                "-f",
                str(allowed_signers),
                "-I",
                identity,
                "-n",
                namespace,
                "-s",
                str(signature_path),
            ],
            input=envelope.payload,
            capture_output=True,
            timeout=60,
        )
    finally:
        signature_path.unlink(missing_ok=True)
    if probe.returncode == 0:
        return SIGNATURE_VALID, (probe.stdout or b"").decode("utf-8", errors="replace").strip()
    detail = (probe.stderr or probe.stdout or b"").decode("utf-8", errors="replace").strip()
    return SIGNATURE_INVALID, detail.splitlines()[0] if detail else "ssh-keygen rejected the signature"


def load_attestation(path: Path) -> Envelope:
    return Envelope.from_json(read_json(path, what="attestation"))


def statement_bytes(statement: dict[str, Any]) -> bytes:
    """Canonical bytes of the statement — what gets signed and what gets hashed."""
    return canonical_json(statement)


class SigningUnavailable(HarnessError):
    exit_code = 12
    kind = "signing"
