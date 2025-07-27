---
title: Document intent and reasoning
description: Add comments that explain the reasoning, intent, or context behind code
  decisions, especially for non-obvious logic, workarounds, or business requirements.
  Focus on the "why" rather than just the "what" to help future maintainers understand
  the decision-making process.
repository: snyk/cli
label: Documentation
language: TypeScript
comments_count: 7
repository_stars: 5178
---

Add comments that explain the reasoning, intent, or context behind code decisions, especially for non-obvious logic, workarounds, or business requirements. Focus on the "why" rather than just the "what" to help future maintainers understand the decision-making process.

Examples of good explanatory comments:
- Explain why specific workarounds were chosen: `// GitHub Code Scanning requires locations even when no file is provided, so we fall back to the path`
- Clarify the purpose of parameters: `// bufferOutput: when true, captures raw buffer data for binary content processing`
- Document vendor-specific requirements: `// AWS uses cvssv3_baseScore, GitHub uses security-severity for CVSS scoring`
- Explain business logic: `// We only filter displayed results to avoid affecting internal processing while cleaning up user-facing output`
- Add TODO comments for future work: `// TODO: Make this optional once custom rules are implemented`

Avoid comments that simply restate what the code does. Instead, provide context about why certain approaches were taken, what constraints influenced the design, or what future considerations should be kept in mind.