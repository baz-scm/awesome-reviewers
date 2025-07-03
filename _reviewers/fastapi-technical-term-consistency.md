---
title: Technical term consistency
description: 'When working with multilingual codebases or documentation, maintain
  consistent naming conventions for technical terms across all languages. Consider
  the following practices:'
repository: fastapi/fastapi
label: Naming Conventions
language: Markdown
comments_count: 7
repository_stars: 86871
---

When working with multilingual codebases or documentation, maintain consistent naming conventions for technical terms across all languages. Consider the following practices:

1. **Context over literalism**: Translate technical terms based on their semantic meaning in context rather than word-for-word. For example, in Korean, JWT's "subject" field should be translated as "주체" (entity/subject) rather than "주제" (topic) because it refers to the entity who owns the token.

2. **Preserve framework terminology**: For framework-specific concepts or methods, consider keeping the original term or providing a consistent translation. Treat them as proper nouns (e.g., Pydantic's "Configuration").

3. **Be consistent with existing translations**: If a technical term has already been translated in your codebase (e.g., "issue" → "이슈"), maintain that translation throughout.

4. **Programming keywords**: Consider whether programming language keywords (like Python's `import`) should be translated or kept in their original form for clarity.

```python
# Example of consistent technical terminology in comments
# 경로 작업 (path operation)
@app.get("/items/")
async def read_items():
    # 토큰의 주체(subject)를 확인
    return {"message": "Consistent terminology helps users understand your API"}
```

Maintaining terminology consistency helps users build a mental model of your API and prevents confusion when switching between languages.