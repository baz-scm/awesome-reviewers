---
title: Documentation translation guidelines
description: Maintain consistency and accuracy when translating documentation. Ensure
  technical terms and special formatting elements are handled properly according to
  project guidelines.
repository: fastapi/fastapi
label: Documentation
language: Markdown
comments_count: 9
repository_stars: 86871
---

Maintain consistency and accuracy when translating documentation. Ensure technical terms and special formatting elements are handled properly according to project guidelines.

When translating documentation:
1. **Preserve special formatting**: Keep formatting elements like admonitions intact, following project-specific patterns. For example with info boxes:
   ```markdown
   /// tip | Dica
   Content goes here
   ///
   ```
   Don't change the word immediately after `///` as it determines the box's styling.

2. **Handle technical terms appropriately**: Consider whether technical terms should be translated or kept in their original form based on common usage in the target language.
   ```python
   # In Korean translation
   # Better: "오버헤드" (keeping technical term "overhead")
   # Instead of: "추가적인 시간" (translating as "additional time")
   ```

3. **Maintain consistent terminology**: Use the same translation for recurring terms throughout the documentation.

4. **Add context when needed**: Include examples for abbreviations or technical concepts to improve clarity.

5. **Don't modify original content**: When translating, avoid changing the source code examples unless translating comments.