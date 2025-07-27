---
title: Write actionable documentation
description: Documentation should be written in active voice with concrete examples
  and clear context. Avoid passive constructions and vague references that leave readers
  guessing about implementation details or expectations.
repository: snyk/cli
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 5178
---

Documentation should be written in active voice with concrete examples and clear context. Avoid passive constructions and vague references that leave readers guessing about implementation details or expectations.

Use active voice to make instructions direct and actionable:
```markdown
❌ Should be used when using `--sarif`. Will remove the `markdown` field...
✅ Removes the `markdown` field from the `result.message` object. Should be used when using `--sarif`.
```

Provide concrete examples when referencing technical concepts:
```markdown
❌ Add the replace directives you need in `cliv2/go.mod`
✅ Add the replace directives you need in `cliv2/go.mod`:
    replace github.com/snyk/go-application-framework => ../go-application-framework
```

Include context about purpose and expectations, especially in templates and guides:
```markdown
❌ ## Pull Request Submission
✅ ## Pull Request Submission
    Thanks for your interest in improving Snyk CLI. To ensure all our users have a great experience, please carefully complete all following fields.
```

This approach ensures documentation is immediately useful and reduces back-and-forth clarification requests during reviews.