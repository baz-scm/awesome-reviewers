---
layout: page
title: About
permalink: /about/
description: What Awesome Reviewers is, where the material comes from, who maintains it, and what it does not claim to be.
lead: A public library of engineering instructions distilled from code review discussions in production open-source repositories, maintained by the team at Baz.
---

## What this is

Awesome Reviewers is a library of expert engineering instructions for AI and infrastructure domains.
Each entry is one instruction — a rule, why it exists, and usually an example of the shape being
asked for — written up from recurring reviewer feedback in a single open-source repository. Every
instruction is plain markdown, so it drops into an agent's system prompt, a code review harness, a
skill or a context broker without conversion.

The corpus spans agent frameworks, inference servers and model gateways, ML frameworks, container
orchestration, cloud infrastructure and IaC, databases and data platforms, observability, security
tooling, language runtimes and compilers, developer tooling, application frameworks and
documentation. Current counts, per domain and for the whole corpus, are published in
[/v1/version.json](/v1/version.json) and [/v1/domains.json](/v1/domains.json) rather than written
into this page, so they cannot go stale.

## Where the material comes from

The input is code review discussion on public pull requests: the diff under review, the reviewer's
comment, and the replies that resolved it. Review comments are where standards get stated
explicitly — a maintainer explaining why a change is unsafe is usually more specific than the same
project's documentation. Threads that repeat the same point across a repository are grouped, and the
recurring requirement is written up as one instruction.

Provenance travels with everything. Each instruction names the repository it came from, carries the
number of review threads and comments behind it, and links the discussions themselves, so a claim can
be traced back to the comments that produced it. Dates are derived from those comments rather than
declared: the newest comment behind an instruction is its last-updated date. The
[method](/methodology/) page describes the whole pipeline, including how domains are assigned and
what the known gaps are.

## How it is built and published

The repository is the product. `_reviewers/` holds one markdown instruction per file plus a sibling
JSON file of the review discussions it was derived from, and everything else — the indexes, the raw
endpoints, the domain bundles, `llms.txt`, the OpenAPI description and the versioned JSON surface —
is derived from it by one standard-library Python script and published as static files. There is no
database, no server-side rendering and no build step beyond Jekyll and that script, which is why
every endpoint can be a plain file with a stable URL.

That also means anyone can reproduce the whole thing: clone the repository, run `python
build_data.py`, and you have byte-for-byte what the site serves. See
[developers](/developers/) for the commands.

## Who maintains it

Awesome Reviewers is maintained by the team at [Baz](https://baz.co), which builds AI code review
tooling. The corpus is Apache-2.0 and lives in
[baz-scm/awesome-reviewers](https://github.com/baz-scm/awesome-reviewers) on GitHub; corrections and
new source repositories arrive as issues and pull requests there. Reviewers whose public comments the
corpus is derived from are credited by handle on the [sources](/sources/) page.

## What it is not

These instructions are distilled from public review threads. They are not official guidance from the
projects they were derived from, not a specification, and not guaranteed to be correct for your
codebase — two repositories in the same domain can disagree, and both are in the corpus. Nothing here
is a substitute for a linter, a test suite or a human reviewer; it is the domain knowledge those
tools do not carry. Anything harmful or wrong is worth an
[issue](https://github.com/baz-scm/awesome-reviewers/issues), and it gets fixed at the source.
