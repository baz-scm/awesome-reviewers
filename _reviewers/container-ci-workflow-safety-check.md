---
title: CI Workflow Safety Check
description: 'When reviewing GitHub Actions used for CI/CD automation, verify three
  things:


  1) Repo context is available

  - If the workflow reads files from the repository (e.g., `.github/labeler.yml`),
  ensure `actions/checkout` is present.'
repository: apple/container
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 48787
---
{% raw %}
When reviewing GitHub Actions used for CI/CD automation, verify three things:

1) Repo context is available
- If the workflow reads files from the repository (e.g., `.github/labeler.yml`), ensure `actions/checkout` is present.

2) Automation is testable without merging
- For workflows that comment/close/alter PRs, add a safe test path so you can validate behavior on a non-merged PR (e.g., gate execution behind a dedicated test label).

3) Permissions match the actual API usage
- Confirm the `permissions` block grants only what’s needed for the specific targets the action touches (e.g., PRs vs issues), and don’t assume old permission requirements won’t resurface.

Example patterns:

- Ensure checkout before reading repo config:
```yaml
- name: Checkout
  uses: actions/checkout@v4

- name: Apply labels using labeler
  uses: actions/labeler@v5
  with:
    pr-number: ${{ steps.pr-number.outputs.number }}
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    configuration-path: .github/labeler.yml
```

- Gate “stale PR” behavior behind a test label (safe dry-run style):
```yaml
# Example approach: trigger on schedule, but only operate when a PR has a specific label.
# (Exact wiring depends on the action version you use.)
- name: Mark stale PRs
  uses: actions/stale@vX
  with:
    only-labels: stale-ci-test
    # keep existing close/comment settings as desired
```

Apply this as a checklist during CI/CD workflow reviews to prevent silent misconfigurations, missing file access, and hard-to-test automation that can impact real PRs.
{% endraw %}
