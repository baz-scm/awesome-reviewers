---
title: Documentation accuracy
description: 'Documentation must describe what the product actually does right now,
  not what it used to do, is planned to do, or is believed to do. Before publishing
  or updating a page: (1) verify every command, config key, or code sample by actually
  running it — e.g. an example like `cline connect telegram --restart -k <BOT-TOKEN>`
  was wrong because the CLI''s argument...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Documentation
language: Other
comments_count: 6
repository_stars: 70984
---

Documentation must describe what the product actually does right now, not what it used to do, is planned to do, or is believed to do. Before publishing or updating a page: (1) verify every command, config key, or code sample by actually running it — e.g. an example like `cline connect telegram --restart -k <BOT-TOKEN>` was wrong because the CLI's argument parser put the flag after the positional channel name and silently dropped it; (2) remove documentation for features that are deprecated, broken, or no longer have any effect rather than leaving a stale description — e.g. a `CLINE_HOOKS_DIR` entry that "has no effect" or a `.clineignore` page describing filtering that isn't actually enforced should either be deleted or the underlying feature should be fixed, not left documented as if it still works; (3) choose precise wording that matches the real level of behavior, such as "supports" vs. "enforces," since a member can still edit files written by a CLI tool until the next session overwrites them, so claiming strict enforcement overstates the guarantee; and (4) when behavior differs across build variants (e.g. Nightly vs. stable, legacy vs. SDK-based extension), make sure any instructions or config keys are correct for each variant, not just the default one. If a broken feature is scheduled for a near-term fix, it's acceptable to document the current caveat alongside the intended behavior, but open-ended "this is currently broken" notes with no fix in sight should be removed instead of normalized as permanent documentation.