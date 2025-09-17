---
title: Make test descriptions specific
description: Test scenarios and steps should use specific, descriptive language that
  clearly communicates what is being tested and what behavior is expected. Avoid vague
  or ambiguous terms that leave room for interpretation.
repository: emcie-co/parlant
label: Documentation
language: Other
comments_count: 2
repository_stars: 12205
---

Test scenarios and steps should use specific, descriptive language that clearly communicates what is being tested and what behavior is expected. Avoid vague or ambiguous terms that leave room for interpretation.

When writing test scenarios, use descriptive names that specify the exact conditions and expected outcomes rather than generic phrases. For test steps, explicitly define all inputs and conditions rather than using undefined references.

Examples of improvements:
- Instead of: "The agent correctly chooses to call the right tool"
- Use: "The agent correctly chooses to call the right overlapping tool based on glossary"

- Instead of: "And a session with a single user message" 
- Use: "And a user message, 'Hi I want to make an appointment with Dr Sara Goodman tomorrow at 19:00'"

This ensures that anyone reading the tests can understand exactly what scenario is being tested without having to make assumptions about undefined or vague references.