---
title: Verify test commands
description: 'Always verify that test commands documented in project guides work exactly
  as written. Test commands should be copy-paste executable without modification.
  When adding or updating test command examples in documentation:'
repository: vercel/turborepo
label: Testing
language: Markdown
comments_count: 2
repository_stars: 28115
---

Always verify that test commands documented in project guides work exactly as written. Test commands should be copy-paste executable without modification. When adding or updating test command examples in documentation:

1. Execute the exact command from a clean environment before committing changes
2. Include complete command syntax with all necessary flags
3. Specify expected behavior or output when relevant

**Example:**
```bash
# ✅ GOOD: Complete, verified command
cargo coverage -- --open  # Runs tests with coverage and opens the report

# ❌ BAD: Incorrect command syntax
cargo run --bin coverage -- --open  # May not work in all environments
```

For integration tests that target specific files or tests:

```bash
# ✅ GOOD: Correctly specifies how to run a specific test
pnpm --filter turborepo-tests-integration test tests/turbo-help.t

# ❌ BAD: Incorrect or platform-dependent command
pnpm test:interactive -F turborepo-tests-integration -- run-summary.t
```

This practice ensures developers can efficiently run tests without debugging documentation issues first.