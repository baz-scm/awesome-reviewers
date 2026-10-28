---
title: Trust boundaries for automation
description: 'When designing allowlists, hooks, or auto-approval logic that lets an
  agent or CI job execute commands, scripts, or tools automatically, treat these mechanisms
  as security boundaries only if they are actually unbypassable — otherwise document
  and market them as convenience filters, not protections. Concretely:'
repository: cline/cline#`sleep 4`
label: Security
language: Other
comments_count: 3
repository_stars: 70979
---

When designing allowlists, hooks, or auto-approval logic that lets an agent or CI job execute commands, scripts, or tools automatically, treat these mechanisms as security boundaries only if they are actually unbypassable — otherwise document and market them as convenience filters, not protections. Concretely:

- Don't claim a safelist of "safe" commands is secure unless you've verified it can't be subverted by local configuration. For example, matching on `git diff` as "read-only" is unsafe because `diff.external` or `core.fsmonitor` settings in an untrusted repo can make it execute arbitrary programs — no flag combination makes this safe. Prefer explicit guidance like "only auto-approve git commands in repositories you trust" over an illusory safelist.
- If a script or hook is meant only to filter noise (e.g., keep the model from reading minified build output) rather than enforce security, say so explicitly instead of implying it blocks malicious or adversarial behavior it cannot actually stop.
- In CI/CD or any pipeline where untrusted input (e.g., a pull request) is checked out, assume that any repo-committed hooks, plugins, or permission configs can be modified by that same untrusted input and will run with the job's full privileges/secrets (e.g., `GH_TOKEN`). Don't rely on in-repo security controls under these conditions. Instead, either avoid checking out untrusted code before running privileged steps (check out the base branch and fetch the diff via API), strip repo-local hook/plugin directories before the privileged step runs, or enforce restrictions via global/host-level hooks outside the checked-out repo.

The core rule: identify exactly what trust boundary a given control enforces, verify it can't be bypassed by the inputs it's meant to guard against, and never present a bypassable mechanism as a genuine security control.