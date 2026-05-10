---
title: Documentation clarity rules
description: When writing technical curriculum/docs, ensure the content is (a) accurate,
  (b) unambiguous about what learners must do and what the expected output/input is,
  and (c) consistent in formatting and tone.
repository: freeCodeCamp/freeCodeCamp
label: Documentation
language: Markdown
comments_count: 10
repository_stars: 444449
---

When writing technical curriculum/docs, ensure the content is (a) accurate, (b) unambiguous about what learners must do and what the expected output/input is, and (c) consistent in formatting and tone.

Apply these rules:
- Fix correctness issues before merging: verify command/API names and options; avoid typos (e.g., `express.urlencoded`).
- Separate responsibilities:
  - `--description` teaches the concept/skill.
  - `--explanation` justifies the correct answer (don’t blend explanation/translation into description).
- Avoid redundant instructions (e.g., remove “There’s just one correct answer.” from multiple-choice tasks).
- Use house-style for inline code and typography:
  - Wrap code/terms in backticks (and use consistent straight quotes/backticks, not mixed typographic variants).
  - Put English punctuation outside closing quotes.
- Keep learner-facing tone neutral: avoid “we” when addressing learners.
- Make required user output expectations explicit with examples when the prompt depends on a specific shape (e.g., show the expected prop/type signature or object structure).
- Ensure lists/structure follow the intended format (e.g., user stories should be an ordered list) and that input/output expectations are clear from the text.

Example pattern (description vs explanation):
```md
# --description--
To run the program, use:
```bash
python main.py
```

# --explanation--
The command must be run from the folder that contains `main.py`.
```