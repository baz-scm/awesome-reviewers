# awesome-harness

A coding harness with six machine-enforced pillars, whose policy is compiled from
[Awesome Reviewers](https://awesomereviewers.com) — instructions distilled from code review
discussions in production repositories.

Inspired by [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows), which gives an AI
coding agent a three-phase workflow with blocking review gates. AI-DLC's gates are prose the model is
asked to honour. This is the substrate underneath: the gate is code, the history is hash-chained, the
approval binds to a tree digest, and the run ends in a signed statement.

Python 3.9+, standard library only. No install step, no dependencies, no build.

```bash
harness/awesome-harness init
harness/awesome-harness policy build --topic Security --topic CI/CD --language Python
harness/awesome-harness gate                      # evaluate your working change
harness/awesome-harness run harness/plans/gate-only.json
harness/awesome-harness verify
```

## The six pillars

| Pillar | What it provides | Where it lives |
| --- | --- | --- |
| Source control | Durable, immutable history of how code evolved | `scm.py`, `ledger.py` |
| Execution | Isolated, performant compute for building, testing, validating | `execution.py` |
| Artifacts | Reproducible outputs that move across systems | `artifacts.py` |
| Caching | Reuse of deterministic work | `cache.py` |
| Identity | Proving who or what produced code | `identity.py`, `verify.py` |
| Policy | Machine-enforceable rules for quality, security, compliance | `policy/` |

### 1. Source control

Git already is the immutable history. Two things it does not give you:

**Snapshots of work that is not a commit yet.** An agent's output exists as a dirty worktree long
before it is a commit, and that is precisely the window you want recorded. `snapshot` writes the
working tree into real git objects through a *temporary index* — `write-tree` then `commit-tree` —
and anchors the result at `refs/harness/snapshots/<run-id>`. Nothing is staged, no branch moves, no
commit lands on any branch, and the state becomes a content-addressed object git will not collect.

```bash
$ harness/awesome-harness snapshot
tree    f8226ff2f902bd4a...      # content identity: same content, same tree, always
commit  5e6fcc6e4d82a1c9...      # anchor a human can `git show`
ref     refs/harness/snapshots/20260804T121035Z-aea4fe
```

`.harness` is excluded from snapshots deliberately: the ledger lives there, so including it would
make the tree digest change every time a record is appended — and a content identity that moves with
the harness's own bookkeeping cannot pin a cache key or hold an approval.

**A record of the process.** The ledger is append-only JSONL where every record's digest covers the
previous record's digest. Editing or removing record *n* invalidates every record after it, and
`verify` says exactly which one.

```
$ harness/awesome-harness ledger verify
CHAIN BROKEN at record 3: record 3 was modified: contents hash to sha256:9c1f4a2, record claims sha256:2b77e10
```

Records carry a monotonic `seq`; the wall-clock stamp is for humans and orders nothing. Appends take
an exclusive `flock` around *read-tail-then-write*, because splitting that pair lets two writers
build two chains from one predecessor.

The ledger is committed to git. The record of how the code was made is as durable as the code.

### 2. Execution

Steps run against a detached worktree of an immutable commit, with an environment that was declared
rather than inherited, under resource limits, with a timeout that kills the whole process group, and
with output scrubbed before it is written down.

- **container** — `docker run --cap-drop=ALL --security-opt=no-new-privileges --read-only
  --network=none --user=uid:gid --pids-limit --memory`, secrets passed by `--env-file` and not `-e`
  (which `docker inspect` exposes).
- **local** — new session, `setrlimit` on address space, CPU, file descriptors, processes and file
  size, allowlisted environment, confined cwd.

`auto` picks container when a runtime is present. Which one ran is recorded in the ledger and the
attestation, never inferred from configuration — and the local backend's isolation report says
`"network": "host (not isolated)"`, because claiming otherwise in a provenance record would make the
record a lie. Asking for `container` on a machine without one is an error, not a silent downgrade.

### 3. Artifacts

Content-addressed store, plus manifests, plus bundles that are byte-identical anywhere:

```bash
$ harness/awesome-harness artifacts export <run> a.tar && harness/awesome-harness artifacts export <run> b.tar
$ cmp a.tar b.tar && echo identical
identical
```

Every tar field a writer would otherwise take from the ambient system is pinned: `mtime=0`, uid/gid
`0`, empty uname/gname, member order sorted, permissions normalised to 0644/0755. `harness/tools/determinism_check.py`
re-proves it on every run under a changed umask, changed mtimes, a changed timezone and a different
working directory — a documented guarantee that nothing executes is a guarantee that quietly stops
being true.

Import treats the bundle's manifest as a claim: every member is re-hashed, and a member the manifest
does not list is rejected rather than ignored. Publishing a zero-byte artifact is an error unless the
step declared `allow_empty`.

### 4. Caching

The key covers the step's argv, cwd, declared env and outputs; the digest of every declared input
file; a fingerprint of every declared tool version; a digest per environment value; the policy pack
digest; the platform; and the resolved isolation backend — for a container, the image **digest**,
never the tag.

Deliberately excluded: the run id, timestamps, the actor, the ledger head, the hostname, absolute
paths, and `HOME`/`TMPDIR`, whose values are per-run by construction. Each of those changes between
two runs that should hit, so including any one would produce a cache with a permanent 0% hit rate —
which looks exactly like a working cache until someone measures it.

Four refusals worth knowing about:

- A step declaring **no inputs cannot be cached**, and says so. Without inputs the key cannot observe
  the code, so the first result would be replayed forever.
- A **container whose image digest cannot be resolved** cannot be cached either. Keying on the tag
  would span every image that tag ever pointed at; keying on the *absence* of a digest is worse, since
  `docker run` pulls the image and supplies the digest that was missing, so the next run computes a
  different key from identical inputs. The digest is resolved once per process for the same reason.
- One key addressing **two different input sets** raises, and never resolves by preferring a side.
- A hit whose blobs have been evicted is a **miss**, not an empty result.

A miss is explained rather than merely reported:

```
CACHE_MISS  unit-tests  reason=miss  why=["input harness/awesome_harness/cache.py changed"]
```

### 5. Identity

One distinction the pillar rests on. A **claim** is what the environment says — `git config
user.email`, `CLAUDECODE=1`, `GITHUB_ACTOR` — all writable by whoever runs the process. A **proof** is
a signature verifying against a key in an allowed-signers file. An attestation records both, in
separate fields, and never promotes one to the other:

```
$ harness/awesome-harness verify
INTACT BUT UNSIGNED  .harness/attestations/20260804T121035Z-aea4fe.json
  [ok  ] envelope        payload d67615db3179
  [ok  ] ledger-chain    18 record(s), head 0f034a3ae367
  [ok  ] ledger-anchor   head anchored at record 16
  [ok  ] subjects        4 artifact subject(s) present and intact
  [ok  ] policy-pack     pack 'default' digest matches
  [ok  ] corpus-drift    every pinned instruction is unchanged
  [ok  ] policy-verdict  gate verdict 'pass'
  [ok  ] signature       unsigned — ssh-keygen is not on PATH
```

There is no code path that reports `verified` without a signature having been checked. `unsigned`,
`unverifiable` and `invalid` are three different answers and stay three different answers.

The statement is in-toto Statement v1 with a harness predicate, signed via `ssh-keygen -Y sign` over
canonical bytes. Git object ids are labelled `sha1`; artifact digests are labelled `sha256`. The
verifier takes the signing principal from the statement, never from a flag — otherwise the caller
chooses whose signature counts. The recorded ledger head is accompanied by a record **count**,
because a truncated-and-rechained ledger can reproduce a head but not its sequence number.

### 6. Policy

Rules are compiled from the corpus into a pack that pins each one by the digest of the instruction
body, and the pack's own digest feeds the cache key and the attestation. Given an attestation you can
say which version of which rule, sourced from which review discussion, gated this change — and check
it, because the pack is committed and the corpus is public.

```
$ harness/awesome-harness policy show
pack 'default'  digest sha256:37b98e56ad6a…  threshold error

machine rules — a coded check, bound to the instruction it enforces
  AH005  error    Confine paths with Path.is_relative_to, not a string prefix check.
        from aidlc-workflows-secure-path-confinement (awslabs/aidlc-workflows) efb0aebc6609
  AH008  warning  Every network call needs an explicit timeout, or it hangs forever by default.
        from waveterm-use-network-timeouts (wavetermdev/waveterm) d9881a273cf5
```

Two tiers:

**machine** — sixteen coded checks. Python is analysed with `ast`, not regexes: `subprocess.run(cmd,
shell=True)` split over four lines, a `requests.get` whose `timeout=` arrives via `**kwargs`, a
mutable default on a decorated async method — a regex gets all three wrong in both directions. YAML,
Dockerfiles and requirements files are matched textually, because parsing them would mean a
dependency.

**advisory** — the instruction body, delivered as review context for changed files matching its
language. This is the honest tier, not the lesser one: about five thousand instructions exist and
roughly a dozen can be decided by a checker. The rest is expertise a reviewer applies, and the
harness's job is to put the right ones in front of whoever reviews next.

```bash
harness/awesome-harness context --out review-context.md
```

Findings are scoped to **added lines**. A gate that reported whole files would blame every change for
the state of the repository and be switched off within a week. Fingerprints exclude the line number,
so inserting an import above a violation does not present it as a new one.

`policy build` **refuses to compile a check whose slug does not resolve** to a real instruction file,
and offers near-matches. A rule citing an instruction that does not exist enforces nothing while
looking identical to one that does; `test_policy.py` asserts every shipped slug resolves against the
real corpus.

#### The checks

| id | enforces | from |
| --- | --- | --- |
| AH001 | no credential literals in source | `checkov-avoid-hardcoded-secrets` |
| AH002 | pin GitHub Actions to a commit SHA | `angular-pin-github-actions-sha` |
| AH003 | least-privilege workflow `permissions:` | `grafana-workflow-permission-boundaries` |
| AH004 | never run a composed string through a shell | `codex-prevent-command-injection` |
| AH005 | confine paths with `is_relative_to` | `aidlc-workflows-secure-path-confinement` |
| AH006 | validate archive members before extraction | `comfyui-prevent-path-traversal` |
| AH007 | catch specific exceptions, never swallow | `airflow-handle-exceptions-with-specificity` |
| AH008 | explicit timeout on network calls | `waveterm-use-network-timeouts` |
| AH009 | explicit timeout on subprocess calls | `cline-set-evidence-based-timeouts` |
| AH010 | validate environment variables at startup | `cli-validate-environment-variables-early` |
| AH011 | do not log secret-named values | `azure-sentinel-avoid-logging-sensitive-data` |
| AH012 | pin dependency versions exactly | `ant-design-pin-ci-dependencies-securely` |
| AH013 | no mutable default arguments | `compose-avoid-mutable-defaults` |
| AH014 | guards and raised errors, not `assert` | `airflow-use-guards-over-assertions` |
| AH015 | containers declare a non-root `USER` | `comfyui-container-security-best-practices` |
| AH016 | pin base images to a digest or version | `lobe-chat-pin-docker-base-versions` |

Every check ships a positive **and** a negative fixture. A check with only a positive fixture is one
nobody has shown to be quiet on correct code, and false positives are how gates get switched off.

#### Suppression

Inline, with a mandatory reason — an unexplained suppression is a finding that was hidden rather than
decided:

```python
# harness:allow AH011 - an approval token is a public digest of the thing approved, not a credential
print(f"approved {short(args.token)}")
```

Or path-scoped in `.harness/waivers.json`, requiring `check`, `path` and `reason`. An expired waiver
stops suppressing and is reported — a permanent exemption is a policy change and should have to look
like one.

## Plans

Phases, after AI-DLC's inception → construction → operations. A phase can carry a gate, an approval,
or both.

```json
{
  "name": "construction",
  "gate": true,
  "steps": [{
    "id": "unit-tests",
    "run": ["python3", "-m", "unittest", "discover", "-s", "harness/tests", "-t", "harness"],
    "inputs": ["harness/awesome_harness/*.py", "harness/tests/*.py"],
    "tools": ["python3 --version"],
    "outputs": [{"path": "junit.xml", "allow_empty": false}]
  }]
}
```

An approval binds to `(plan digest, phase, snapshot tree, pack digest)`. Change any one and the
approval no longer applies — which is the difference between a sign-off and a checkbox.

```
$ harness/awesome-harness run harness/plans/default.json
approval: phase 'operations' requires approval for tree f8226ff2f902
  hint: record it with: awesome-harness approve operations --token sha256:4c8a…
        (or re-run with --approve operations)
$ echo $?
8
```

Order of operations for one run:

1. resolve actor, load and digest the policy pack, report corpus drift
2. `RUN_STARTED` — git facts, plan digest, pack digest, actor, chosen backend
3. snapshot the worktree into immutable git objects, anchored to a ref
4. detached worktree of that snapshot: the isolated compute for every step
5. per phase — approval → steps (cache lookup, execute, publish) → gate
6. attest: subjects are the artifacts, predicate names the policy that gated them
7. `RUN_FINISHED`, then tear down the worktree

The attestation is written **whether or not the run passed**. The run someone most wants provenance
for is the one that failed.

## Exit codes

CI and agents branch on the reason, so failures never collapse to 1.

| code | meaning |
| --- | --- |
| 0 | ok |
| 2 | usage |
| 3 | policy gate failed |
| 4 | integrity — digest, chain or signature did not hold |
| 5 | execution — a step could not be run |
| 6 | timeout |
| 7 | isolation backend unavailable |
| 8 | approval required (waiting on a person, not broken) |
| 9 | corpus missing, or a pack drifted from it |
| 78 | configuration |

## Layout

```
harness/
  awesome-harness              executable entry point; no install needed
  awesome_harness/
    digest.py                  one hash function, one canonical serialization
    scrub.py                   credential scrubbing, high-confidence and broad tiers
    paths.py                   confinement and safe archive extraction
    workspace.py               on-disk layout, atomic writes, the one lock
    errors.py                  typed failures with distinct exit codes
    scm.py ledger.py           pillar 1
    execution.py               pillar 2
    artifacts.py               pillar 3
    cache.py                   pillar 4
    identity.py verify.py      pillar 5
    policy/                    pillar 6 — corpus, findings, checks, pack, engine
    plan.py                    the runner: all six pillars in order
    cli.py                     one entry point per pillar
  plans/                       default.json, gate-only.json
  tools/determinism_check.py   re-proves bundle determinism as a plan step
  tests/                       173 tests, stdlib unittest
```

Repository state lives in `.harness/`. Committed: `config.json`, `policy/*.pack.json`, `waivers.json`,
`ledger/`, `attestations/` — the durable history and the pinned policy. Gitignored: `runs/`,
`artifacts/`, `cache/`, `tmp/`, `snapshots/` — reproducible by re-running.

## Tests

```bash
python3 -m unittest discover -s harness/tests -t harness
```

The two that matter most are the ones that attack the harness rather than exercise it:
`TestTamperMatrix` rewrites a ledger record, truncates and re-chains the ledger, corrupts an artifact
blob, edits the policy pack, swaps in a differently-built pack, and edits the signed payload — each
must be caught by a named check. `TestBundleDeterminism` builds the same bundle under a different
umask and different mtimes and demands identical bytes.

## Using it from an agent

See `AGENTS.md` in this directory.
