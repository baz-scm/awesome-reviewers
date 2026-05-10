---
title: Concise Performance Guidance
description: 'When writing performance optimization standards/docs, keep the lead
  section brief and immediately actionable: provide a short overview plus a checklist
  of the key techniques, and move any deep technical explanation into linked resources.'
repository: kamranahmedse/developer-roadmap
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 354523
---

When writing performance optimization standards/docs, keep the lead section brief and immediately actionable: provide a short overview plus a checklist of the key techniques, and move any deep technical explanation into linked resources.

How to apply:
- Lead/overview (1 short paragraph): define the goal and mention the major performance dimension(s) you’re addressing (e.g., initial load, rendering/DOM overhead, memory/bundle size, bottlenecks/monitoring).
- Checklist bullets: include the practical “what to do” items relevant to the platform (e.g., lazy loading, avoid unnecessary re-renders, reduce bundle size, virtualize long lists, monitor/profiling, minimize dependencies).
- Learn-more links: detailed “how/why,” step-by-step explanations, and deeper background should live behind links (internal pages or external docs).

Example (Markdown template):
```md
## Performance Optimization (Overview)
To improve performance, focus on reducing initial load time, minimizing unnecessary work during rendering, and identifying bottlenecks early.

- Lazy-load components to reduce upfront cost
- Prevent unnecessary re-renders (use appropriate conditional rendering patterns)
- Reduce bundle size (code splitting, tree shaking)
- Virtualize long lists/tables to cut DOM overhead
- Monitor/profiling to find bottlenecks
- Minimize dependencies that increase payload/work

Learn more:
- [Resource A](https://...)
- [Resource B](https://...)
- [Resource C](https://...)
```

This ensures the document is fast to scan, consistent with performance best practices, and doesn’t bury developers in overly deep content where a quick orientation is expected.