---
title: testing best practices
description: Choose testing methods, configurations, and approaches that prioritize
  user experience and reliability over theoretical completeness. Consider the practical
  needs of your development team and testing environment when making decisions.
repository: microsoft/playwright
label: Testing
language: Markdown
comments_count: 4
repository_stars: 76113
---

Choose testing methods, configurations, and approaches that prioritize user experience and reliability over theoretical completeness. Consider the practical needs of your development team and testing environment when making decisions.

Key principles:
- **Prefer user-friendly options**: Choose testing flags and commands that developers actually use. For example, prefer `--ui` over `--list` for better developer experience when exploring tests.
- **Select appropriate assertion methods**: Use `toEqual` for most equality checks rather than `toStrictEqual`, as it provides sufficient validation without unnecessary strictness.
- **Configure based on context**: Adapt testing configurations to your specific environment. For test sharding, `round-robin` may provide better distribution than `partition` depending on your test organization. For flaky test handling, consider stricter settings in CI environments.
- **Balance stability with flexibility**: When choosing between testing approaches, consider both immediate usability and long-term maintenance. Evaluate whether more complex solutions actually solve real problems your team faces.

Example of contextual configuration:
```js
// playwright.config.ts
export default defineConfig({
  // Stricter flaky test handling in CI
  failOnFlakyTests: !!process.env.CI,
  // Better test distribution for organized test suites
  shardingMode: 'round-robin'
});
```

This approach ensures your testing setup serves your team's actual workflow rather than following rigid theoretical ideals.