---
title: Untrusted Input Workflow Safety
description: Treat all event/comment text used in GitHub Actions as untrusted. Apply
  strict parsing for command gating and prevent shell-evaluation of untrusted or literal
  text.
repository: facebook/react#b15
label: Security
language: Yaml
comments_count: 2
repository_stars: 251891
---

Treat all event/comment text used in GitHub Actions as untrusted. Apply strict parsing for command gating and prevent shell-evaluation of untrusted or literal text.

**How to apply**
- **Control-flow gating:** Avoid broad substring checks like `contains(comment, '/land')` when the trigger could appear inside URLs or other text. Require an exact command form (e.g., starts-with, whitespace/line boundary, or regex-style matching).
- **Shell safety:** When writing messages or instructions in `run:` scripts, escape characters that would change shell semantics (notably backticks, which can trigger command substitution). Use safe quoting (single quotes) or escape sequences.

**Example (safe command gating + safe echo)**
```yaml
jobs:
  ghstack_land:
    if: >-
      ${{
        needs.check_maintainer.outputs.is_core_team == 'true' &&
        github.event.issue.pull_request &&
        startsWith(github.event.comment.body, '/land')
      }}
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo 'Run `yarn generate-inline-fizz-runtime` and check in the result.'
```