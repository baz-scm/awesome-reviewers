---
title: Least-privilege Actions tokens
description: 'Treat CI workflow tokens as sensitive credentials: configure GitHub
  Actions `permissions` explicitly and keep token usage minimal.


  Apply this standard when workflows need to create PR comments/reviews:'
repository: EbookFoundation/free-programming-books
label: Security
language: Yaml
comments_count: 2
repository_stars: 388003
---

Treat CI workflow tokens as sensitive credentials: configure GitHub Actions `permissions` explicitly and keep token usage minimal.

Apply this standard when workflows need to create PR comments/reviews:
1) **Do not use insecure token workarounds** that broaden or misuse `GITHUB_TOKEN`.
2) **Split producer/consumer logic into separate workflows**: have one workflow generate the content and upload it as an **artifact**, then a second workflow reads that artifact and performs the PR write.
3) **Declare least-privilege permissions at the job level**. If a job comments on PRs, set only what’s needed (e.g., `pull-requests: write`). Avoid “write by default” repo settings for public repos.

Example (job-level permissions + artifact-based handoff):
```yaml
# consumer workflow: posts PR comment/review
on:
  workflow_run:
    workflows: ["free-programming-books-lint"]
    types: [completed]

jobs:
  post:
    permissions:
      pull-requests: write
    steps:
      - name: Download artifact from producer
        uses: actions/download-artifact@v4
        with:
          name: pr-message
      - name: Post message to PR
        run: |
          # read file produced earlier and use it to comment
          MSG_FILE=./message.txt
          cat "$MSG_FILE"
          # call GitHub API using default GITHUB_TOKEN with only PR write permission
```
This prevents authorization failures while reducing the blast radius of the token in CI/CD (a core security best practice for authentication/authorization in workflows).