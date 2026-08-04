"""Typed failures with distinct exit codes.

A harness is consumed by CI and by agents, so "it failed" is not enough: the
caller has to branch on *why* without parsing prose. Every error carries a stable
exit code, and the CLI never collapses them into 1.

Derived from the corpus:
  aidlc-workflows-fail-loudly-degrade-safely  — a degraded path must be visible,
      never silently substituted for the thing that was asked for.
  aidlc-workflows-defensive-observable-error-handling — failures name the input
      that caused them.
"""

from __future__ import annotations


class HarnessError(Exception):
    """Base class. Anything raised on purpose derives from this."""

    exit_code = 1
    kind = "error"

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.hint = hint

    def render(self) -> str:
        text = f"{self.kind}: {self}"
        if self.hint:
            text += f"\n  hint: {self.hint}"
        return text


class UsageError(HarnessError):
    """The command was called wrongly."""

    exit_code = 2
    kind = "usage"


class ConfigError(HarnessError):
    """`.harness/config.json` is missing, malformed, or contradicts itself."""

    exit_code = 78  # EX_CONFIG, so `if [ $? -eq 78 ]` means "fix your config"
    kind = "config"


class NotInitialized(ConfigError):
    def __init__(self, root: str) -> None:
        super().__init__(
            f"no .harness directory under {root}",
            hint="run `awesome-harness init` in the repository you want to gate",
        )


class GateFailed(HarnessError):
    """Policy gate refused the change. Blocking by default."""

    exit_code = 3
    kind = "gate"


class IntegrityError(HarnessError):
    """A digest, a hash chain, or a signature did not hold.

    Distinct from a gate failure: a gate says the code is wrong, this says the
    record of the code is wrong, which is strictly more serious.
    """

    exit_code = 4
    kind = "integrity"


class CacheCollision(IntegrityError):
    """Two different input sets produced one cache key.

    Never resolved by preferring either side. A colliding key means the key
    function is wrong, and reusing the first entry would silently ship the wrong
    bytes (aidlc-workflows-scoped-hash-based-idempotency).
    """

    kind = "cache-collision"


class ExecutionError(HarnessError):
    """A step could not be run at all — as opposed to running and failing."""

    exit_code = 5
    kind = "execution"


class StepTimeout(ExecutionError):
    exit_code = 6
    kind = "timeout"


class BackendUnavailable(ExecutionError):
    """The requested isolation backend is not present on this machine.

    Raised rather than quietly falling back, unless the caller asked for `auto`.
    """

    exit_code = 7
    kind = "backend"


class ApprovalRequired(HarnessError):
    """A phase declares `approval: true` and no approval is recorded.

    Human-in-the-loop is a gate, not a prompt: the run stops with a distinct code
    so a scheduler can tell "waiting for a person" from "broken".
    """

    exit_code = 8
    kind = "approval"


class CorpusError(HarnessError):
    """The Awesome Reviewers corpus could not be read, or drifted from a pack."""

    exit_code = 9
    kind = "corpus"
