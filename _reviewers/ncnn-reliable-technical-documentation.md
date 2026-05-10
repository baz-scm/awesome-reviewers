---
title: Reliable Technical Documentation
description: 'When updating technical docs, ensure they are reliable in both what
  they claim and how developers can apply them:


  - Keep headings/sections aligned with the exact runtime/build parameters shown in
  outputs (e.g., if the benchmark runs with gpu_device=0, reflect “GPU0” in the subsection
  title).'
repository: Tencent/ncnn
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 23205
---

When updating technical docs, ensure they are reliable in both what they claim and how developers can apply them:

- Keep headings/sections aligned with the exact runtime/build parameters shown in outputs (e.g., if the benchmark runs with gpu_device=0, reflect “GPU0” in the subsection title).
- Express requirements as constraints when that’s what’s true (e.g., “CMake >= 3.10” rather than only “CMake 3.10”) and update wording if other tested versions work.
- For troubleshooting, provide a complete, actionable flow: clear cause(s), prerequisites (what to install), concrete commands to run, and warnings about common pitfalls (e.g., avoid installing protobuf into system paths if it breaks version resolution).
- Use robust Markdown for plain URLs—wrap raw links in angle brackets to reduce rendering issues:

```md
参考：<https://zhuanlan.zhihu.com/p/128974102>
```

Practical checklist before merging a doc change:
1) Do section titles/subtitles match the commands and parameters in the text?
2) Are version statements accurate (use >= or range when appropriate)?
3) Can someone follow the steps from a clean environment to a working result?
4) Are there cautions for known failure modes (path conflicts, mismatched shared libraries)?
5) Do external links render consistently in Markdown?