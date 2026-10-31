---
title: Changelog entry conventions
description: 'Changelog entries follow a consistent, repo-wide convention, since many
  PRs were flagged for violating it:


  1. **Placement**: New entries always go under `## [Unreleased]`, under the correct
  `### Added`/`### Changed`/`### Fixed`/`### Removed` subsection matching the nature
  of the change. Never add or edit content under an already-released version heading
  —...'
repository: can1357/oh-my-pi
label: Documentation
language: Markdown
comments_count: 21
repository_stars: 37317
---

Changelog entries follow a consistent, repo-wide convention, since many PRs were flagged for violating it:

1. **Placement**: New entries always go under `## [Unreleased]`, under the correct `### Added`/`### Changed`/`### Fixed`/`### Removed` subsection matching the nature of the change. Never add or edit content under an already-released version heading — released sections are immutable. If a change has no user-visible effect (internal cleanup, test-tree changes, unused exports with no consumers), it needs no changelog entry at all.

2. **Correct package/file**: The entry belongs in the `CHANGELOG.md` of the package whose code actually changed. Don't bundle entries for unrelated commits/issues together, and don't let an entry drift into the wrong package file.

3. **Attribution for external contributions**: Every externally contributed, user-facing fix/feature must credit the PR and author using the exact convention: `([#NNNNN](https://github.com/<org>/<repo>/pull/NNNNN) by [@username](https://github.com/username))`. An issue link alone, or a bare PR number, is not sufficient — e.g.:

```md
- Fixed `/usage` showing Cursor's "Other Models" meter as an inflated dollar amount; it now shows the percentage Cursor reports, like Cursor Models ([#17462](https://github.com/can1357/oh-my-pi/pull/17462) by [@eggpeat](https://github.com/eggpeat))
```

If the change also tracks an internal issue, keep both links (issue first, then the PR with attribution).

4. **User-facing wording**: Entries describe the observable behavior change, not the implementation (no internal function/variable names, data-structure details, or root-cause mechanics). Keep the root-cause explanation in the PR description instead. Example: prefer `Fixed blob URL index loading blocking startup` over a sentence describing the `fs.readFileSync`-to-async refactor. Avoid overselling impact (e.g., don't claim a minor allocation reduction makes requests "noticeably faster").

Before merging, verify the diff touches only `## [Unreleased]` in the right package's `CHANGELOG.md`, the entry has correct attribution, and the wording is a concise, user-facing summary.