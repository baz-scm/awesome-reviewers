---
title: Document implementation rationale
description: Add comments that explain the reasoning behind non-obvious code decisions,
  technical constraints, or complex logic, while avoiding over-documentation of self-evident
  functionality. Focus on the "why" rather than the "what" - document implementation
  choices that future developers (including yourself) might need to rediscover.
repository: microsoft/terminal
label: Documentation
language: C++
comments_count: 3
repository_stars: 99242
---

Add comments that explain the reasoning behind non-obvious code decisions, technical constraints, or complex logic, while avoiding over-documentation of self-evident functionality. Focus on the "why" rather than the "what" - document implementation choices that future developers (including yourself) might need to rediscover.

Examples of good rationale documentation:
- Complex conditional logic: "// An icon path is considered an emoji if it contains a zero-width joiner (U+200D) or ends with a Unicode Variation Selector"
- Implementation decisions: "// We create temporary hstrings here to avoid deep copying the entire text in the no-match case"
- Technical constraints: "// BODGY - The XAML compiler emits a boxed int32, but the dependency property expects a boxed FontWeight"

Avoid over-documenting obvious boolean returns or simple getters. Instead of "// Returns: true if successful, false otherwise", prefer concise descriptions like "// indicates the operation succeeded" when the return value needs explanation at all.