"""awesome-harness — machine-enforced substrate for AI-driven coding.

Six pillars, each a module in this package:

    ledger.py + scm.py   source control  durable, immutable history of how code evolved
    execution.py         execution       isolated, performant compute for changes
    artifacts.py         artifacts       reproducible outputs, movable across systems
    cache.py             caching         reuse of deterministic work
    identity.py          identity        proving who or what produced code
    policy/              policy          machine-enforceable quality/security/compliance

The policy corpus is Awesome Reviewers: instructions distilled from review
discussions in production repositories. A policy pack pins a selection of them by
content digest, so a run can prove which version of which rule gated it.

Only the Python standard library is used. There is no build step.
"""

from __future__ import annotations

__all__ = ["__version__", "SCHEMA_VERSION", "USER_AGENT", "CORPUS_SITE"]

__version__ = "0.1.0"

# Bumped when the on-disk shape of the ledger, packs, manifests, cache entries or
# attestations changes. Every persisted record carries it so a reader can refuse
# a record it does not understand instead of misreading it.
SCHEMA_VERSION = 1

CORPUS_SITE = "https://awesomereviewers.com"
USER_AGENT = f"awesome-harness/{__version__}"
