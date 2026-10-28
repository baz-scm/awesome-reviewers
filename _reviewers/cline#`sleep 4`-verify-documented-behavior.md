---
title: Verify documented behavior
description: Documentation must describe only verified, current behavior. Before publishing,
  confirm that every documented option, flag, path, or example actually works as described
  by testing it against the real CLI/API (e.g., compare with `--help` output or by
  running the command). If a feature is broken, disabled, or has no effect, don't
  document it as if it still...
repository: cline/cline#`sleep 4`
label: Documentation
language: Other
comments_count: 4
repository_stars: 70979
---

Documentation must describe only verified, current behavior. Before publishing, confirm that every documented option, flag, path, or example actually works as described by testing it against the real CLI/API (e.g., compare with `--help` output or by running the command). If a feature is broken, disabled, or has no effect, don't document it as if it still works or as "accepted but ignored" — either remove the entry/row entirely or state the real behavior plainly (e.g., "ignored by `doctor log`; use `CLINE_LOG_PATH` to find your own log file"). Never leave stale or aspirational docs that no longer match the product, since this misleads readers into relying on something that silently fails.

For code examples, make sure the exact invocation shown is one a user could copy-paste and have work, including correct ordering of flags/arguments (e.g., options must precede the sub-command they apply to: `cline connect telegram --restart -k <TOKEN>` fails silently because everything after `telegram` is passed through, so the working form is `cline connect --restart telegram -k <TOKEN>`). When fixing inaccurate docs, add a short note explaining *why* the previous behavior/example was wrong, so future reviewers comparing against the tool's actual help text or source aren't confused by the change.