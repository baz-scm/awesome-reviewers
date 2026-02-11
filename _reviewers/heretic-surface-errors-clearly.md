---
title: Surface errors clearly
description: 'Rule: Fail fast, validate assumptions, and distinguish user cancellation.


  Motivation

  - Hidden or silently handled errors lead to incorrect behavior, confusing UX, and
  hard-to-debug failures (e.g., silently ignoring invalid saved study settings, treating
  Ctrl+C as a legitimate choice, or swallowing invalid split specs).'
repository: p-e-w/heretic
label: Error Handling
language: Python
comments_count: 11
repository_stars: 5002
---

Rule: Fail fast, validate assumptions, and distinguish user cancellation.

Motivation
- Hidden or silently handled errors lead to incorrect behavior, confusing UX, and hard-to-debug failures (e.g., silently ignoring invalid saved study settings, treating Ctrl+C as a legitimate choice, or swallowing invalid split specs).

How to apply
1. Don’t swallow exceptions silently. If a library call or validation can fail, either let the exception propagate or catch it and re-raise with additional context. Only catch exceptions when you can meaningfully handle or recover; otherwise surface them to the caller/user.
   Example: remove broad try/except that hides JSON validation errors and instead let it fail with context.
   Bad:
   try:
       old_settings = Settings.model_validate_json(previous_settings)
       can_resume = True
   except ValidationError:
       can_resume = False

   Good:
   old_settings = Settings.model_validate_json(previous_settings)  # raises on error — user sees the problem

2. Validate inputs and runtime assumptions before use. Check types, existence, and object state rather than assuming a shape or presence. If an assumption is violated, raise a clear error explaining the mismatch.
   - Verify fields are tensors/modules before using or indexing them.
   - When computing slices from user-provided split strings, validate and raise instead of silently using the whole dataset.
   Example (slice parsing):
   start, end = _get_split_slice(split_str, len(prompts), "_")  # raise on invalid spec

3. Treat user cancellation distinctly. Do not conflate None/empty input with a legitimate selection. If a prompt returns None (e.g., Ctrl+C), cancel the current operation or surface that the user aborted instead of picking a default value or exiting the program unexpectedly.
   Example:
   merge_choice = prompt_select(...)
   if merge_choice is None:
       # user cancelled — abort or ask again, do not treat as "adapter"
       raise UserCancelledError("merge aborted by user")

4. Explicitly handle partial or incomplete state. Detect incomplete trials or partial writes using explicit state/flags (e.g., trial.state or a user_attr), and decide one clear behavior: ignore incomplete entries when computing results, extend target counts to account for incomplete trials, or remove incomplete records during resume — but do not silently miscount trials.
   - Use trial.state to check completeness before counting toward n_trials.

5. Provide clear, contextual error messages. When re-raising or failing, include what failed and why, and if appropriate, how to recover (e.g., suggest correcting a split spec or re-running with a different study checkpoint).

Why this matters
- Users need actionable errors (not silent defaults) to fix configuration or data issues.
- Distinguishing cancellation prevents accidental destructive behavior and bad UX.
- Validations prevent downstream crashes and nonsensical output.

Follow-up checklist for code reviewers
- Is there any broad try/except that hides failures? If yes, remove or narrow it and add context when re-raising.
- Are user inputs validated or silently defaulted? If defaulting, is that explicit and documented? If not, raise an error.
- Is Ctrl+C / prompt cancellation handled explicitly (None vs selection)?
- Are runtime assumptions (types, states) checked before use?

References: 1,2,3,4,5,6,7,8,9,10,11