---
name: reviewer-onboarding
description: Teach new contributors how to get value from Awesome Reviewers in their first 30 minutes.
metadata:
  primary-reviewer: rust-prefer-intent-expressive-apis
  focus: onboarding
layout: skill
title: Reviewer Onboarding Sprint
summary: Step-by-step flow for teaching contributors how to wield reviewer prompts, interpret discussions, and record their own workflows.
---

## Overview

This onboarding sprint walks a contributor through:

1. Loading a reviewer prompt and understanding its target outcomes.
2. Opening historical discussions to see how the reviewer evolved.
3. Documenting a new scenario to extend the reviewer library.

## Preparation Checklist

- Share access to the `awesome-reviewers` repository.
- Provide a sample pull request URL that needs attention.
- Confirm the contributor has a preferred AI IDE or agent runner.

## Session Plan

### 1. Inspect the Reviewer Prompt

```markdown
{{ load_reviewer "rust-prefer-intent-expressive-apis" }}
```

Ask the contributor to read the evaluation heuristics out loud and call out anything that aligns with their repo.

### 2. Review Supporting Discussions

```http
GET https://awesomereviewers.com/reviewers/rust-prefer-intent-expressive-apis/discussions.json
```

Guide them through the most recent regression to illustrate how the reviewer learns from feedback.

### 3. Capture a New Scenario

1. Run the reviewer prompt against the sample pull request.
2. Collect code snippets that triggered specific guidance.
3. Draft a new discussion summary and store it alongside the reviewer JSON.

## Follow-up

- Encourage the contributor to author a new reviewer pull request.
- Schedule a retro to refine the onboarding prompts based on their feedback.
- Capture any new scripts in the skill folder for future sessions.

