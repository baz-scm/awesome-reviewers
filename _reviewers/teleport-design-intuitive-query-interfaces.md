---
title: Design intuitive query interfaces
description: When designing algorithms for querying, filtering, or data manipulation,
  prioritize user-friendly function names and interfaces over technically precise
  but obscure terminology. Users should be able to understand and use your algorithmic
  interfaces without deep technical knowledge of the underlying implementation.
repository: gravitational/teleport
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 19109
---

When designing algorithms for querying, filtering, or data manipulation, prioritize user-friendly function names and interfaces over technically precise but obscure terminology. Users should be able to understand and use your algorithmic interfaces without deep technical knowledge of the underlying implementation.

Consider how your algorithm's public interface will be consumed by developers who may not be familiar with technical concepts like semantic versioning, predicate logic, or domain-specific terminology. Choose function names that align with users' mental models and existing familiar tools.

For example, when designing version comparison functions:
- Instead of `semver_lt(version, "18.1")` (technically precise but requires semver knowledge)
- Use `older_than(version, "18.1")` (intuitive and self-explanatory)
- Or even better, `between(version, "18.0.0", "18.1.0")` (clear intent, familiar pattern)

This principle applies to all algorithmic interfaces: sorting functions, search predicates, data transformation operations, and filtering mechanisms. The goal is to make complex algorithms accessible through simple, intuitive interfaces that reduce cognitive load and minimize the need for documentation lookup.