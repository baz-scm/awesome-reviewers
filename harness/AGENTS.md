# Driving awesome-harness from an agent

Written for an AI coding agent working in a repository that has `.harness/` initialized. Every command
here takes `--json`, and every failure has its own exit code, so you can branch without parsing prose.

## The loop

After each meaningful edit, before claiming the work is done:

```bash
harness/awesome-harness gate --json
```

Exit 0 means no finding at or above the pack's threshold. Exit 3 means the gate refused the change;
`findings[]` gives `path`, `line`, `message`, `slug` and a `fingerprint`. Fix the finding — do not
suppress it to get to green. Suppression is for the case where the check is deciding something the
rule does not say, and it requires a written reason that a reviewer will read.

Before writing code in an area you have not touched yet:

```bash
harness/awesome-harness context --out review-context.md
```

That is the advisory tier: instructions distilled from review discussions in production repositories,
selected for the files you have actually changed. Read it as guidance for the code you are about to
write, not as a checklist to satisfy. It is an input to your work; the gate is the verdict on it.

## Recording a whole session

```bash
harness/awesome-harness run harness/plans/gate-only.json --json
```

This snapshots your working tree into immutable git objects, evaluates the gate, and writes a signed
(or explicitly unsigned) attestation. Do it before handing work back, and quote the run id and the
attestation path in your summary. Two consequences worth understanding:

- Your uncommitted work becomes a real git object at `refs/harness/snapshots/<run-id>`. If the user
  discards your changes, `git show <commit>` still has them.
- The run is in the ledger whether it passed or failed. You cannot make a failed attempt disappear by
  trying again, and you should not want to.

## Attribution

Declare the model when you run, so the provenance record says what produced the code:

```bash
harness/awesome-harness run harness/plans/gate-only.json --model <your-model-id>
```

The harness also detects agent markers in the environment (`CLAUDECODE`, `CURSOR_TRACE_ID`,
`AIDER_MODEL`, …) and records **which variable it observed**, because an environment variable is a
claim rather than proof. Only a signature verifying against the committed allowed-signers file makes
an identity provable, and the record says plainly which of the two it has.

When you commit, attach the trailers so attribution survives in git itself:

```bash
harness/awesome-harness trailers   # Harness-Run-Id, Harness-Actor, Harness-Agent-Model, Harness-Attestation
```

## Phases that need a person

A phase with `"approval": true` stops the run with **exit 8** and prints the exact command that
records the approval. Exit 8 means *waiting for a human*, not *broken*. Do not pass `--yes` or
`--approve` on the user's behalf: the approval binds to the plan, the phase, the snapshot tree and the
policy pack, and approving for them would put their name on a decision they did not make. Report the
token and stop.

## Reading a cache miss

`cache_key` and the miss explanation are in the run JSON and the ledger:

```
CACHE_MISS  unit-tests  reason=miss  why=["input harness/awesome_harness/cache.py changed"]
```

If a step you expected to replay did not, the explanation names the input that moved. A step that
reports `not cached: step declares no inputs` needs an `inputs` list in the plan — the harness refuses
to cache what it cannot key to content, rather than replaying a stale result forever.

## What not to do

- **Do not edit `.harness/ledger/ledger.jsonl`.** It is hash-chained; any edit is detected and
  localised to a record, and the repair is impossible rather than merely tedious.
- **Do not edit `.harness/policy/*.pack.json` by hand.** The file carries its own digest and will be
  refused on load. Rebuild with `policy build` so the new digest is recorded deliberately.
- **Do not add a waiver to make the gate pass.** A waiver needs a reason a reviewer will accept, and
  ideally an expiry. If you believe a check is wrong, say so in your summary and let a person decide.
- **Do not run `artifacts gc --apply` or `cache prune --apply`** unless asked. Both default to a dry
  run for a reason.

## Adding a check

Only when the user asks for one. A check must cite a real corpus instruction, and `policy build` will
refuse a slug that does not resolve:

1. Find the instruction the rule comes from: `grep -l "…" _reviewers/*.md`, then read it.
2. Register the check in `awesome_harness/policy/checks.py` with that slug.
3. Add a positive **and** a negative fixture to `FIXTURES` in `tests/test_policy.py`.
   `test_every_check_is_covered_by_a_fixture` fails without both.
4. Rebuild and commit the pack.

The negative fixture is the important one. A check that fires on correct code gets the whole gate
switched off, which costs more than the rule was worth.
