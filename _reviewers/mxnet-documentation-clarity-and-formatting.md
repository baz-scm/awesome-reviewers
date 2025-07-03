---
title: Documentation clarity and formatting
description: 'When writing documentation (README files, tutorials, API docs), ensure
  clarity and proper formatting:


  1. **Define technical terms and concepts** - Don''t assume readers are familiar
  with specialized terminology. Include brief explanations and relevant links for
  reference.'
repository: apache/mxnet
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 20801
---

When writing documentation (README files, tutorials, API docs), ensure clarity and proper formatting:

1. **Define technical terms and concepts** - Don't assume readers are familiar with specialized terminology. Include brief explanations and relevant links for reference.

```markdown
# Arguments
- batch_size: Define batch size (default=64)
- epochs: Define total epochs (default=1000)
- mu: Define μ in μ-Law encoding for audio quantization (see https://en.wikipedia.org/wiki/μ-law_algorithm)
```

2. **Understand markdown formatting rules** - Be aware that formatting details like trailing spaces affect rendering. Double spaces at line ends create line breaks in markdown.

3. **Preview rendered output** - Always check how documentation will actually appear to users before committing changes.

4. **Keep technical references current** - When documenting code structures, ensure descriptions match the actual implementation. Update documentation when code interfaces change.

Following these practices ensures documentation is both technically accurate and genuinely helpful to other developers.
