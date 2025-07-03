---
title: Verify automated documentation
description: When using automated tools to generate documentation, always verify the
  output for accuracy and document any additional manual steps required for completion.
  Automated documentation can inherit incorrect properties or miss crucial steps in
  the process.
repository: chef/chef
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 7860
---

When using automated tools to generate documentation, always verify the output for accuracy and document any additional manual steps required for completion. Automated documentation can inherit incorrect properties or miss crucial steps in the process.

For example:
- When running tools like `rake docs_site:resources` that generate resource documentation automatically, review the output to ensure resources that inherit from parent resources don't contain properties or actions that don't apply to them.
- When using scripts like `publish-release-notes.sh` that push content to repositories, document the complete process including any subsequent manual steps (like triggering Netlify rebuilds) required for the documentation to become visible to users.

Document both the automation commands and their limitations to ensure team members understand the complete documentation workflow. This prevents confusion and ensures accurate, complete documentation reaches the end users.
