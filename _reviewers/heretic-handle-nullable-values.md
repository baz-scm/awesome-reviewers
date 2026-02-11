---
title: Handle nullable values
description: 'Treat None/absent values explicitly and guard attribute access.


  Motivation: user input, storage APIs, optional configuration, and runtime objects
  can all produce None or lack expected attributes. Implicitly assuming presence leads
  to data loss (e.g., deleting checkpoints on a cancelled prompt), brittle logic,
  and runtime errors.'
repository: p-e-w/heretic
label: Null Handling
language: Python
comments_count: 7
repository_stars: 5002
---

Treat None/absent values explicitly and guard attribute access.

Motivation: user input, storage APIs, optional configuration, and runtime objects can all produce None or lack expected attributes. Implicitly assuming presence leads to data loss (e.g., deleting checkpoints on a cancelled prompt), brittle logic, and runtime errors.

Rules and how to apply them:
- Use Optional typing to model nullable semantics and document what None means. Prefer existing option types over ad-hoc enums/sentinels.
  Example: ObjectiveDirection: use optuna.StudyDirection | None where None = "do not optimize".

- Always check return values that can be None before acting. For interactive prompts or library calls that may return None (e.g., user cancels), handle the None case explicitly instead of treating it as a valid choice.
  Example:
  choice = prompt_select("What do you want to do?", choices)
  if choice is None:
      print("Operation cancelled")
      return
  if choice == "continue":
      ...

- When reading from storage/APIs, distinguish between None and empty collections and fail fast if invariants are violated. Prefer explicit checks over assumptions like "there is always one study".
  Example:
  try:
      study_id = storage.get_study_id_from_name("heretic")
  except KeyError:
      study_id = None
  if study_id is None:
      # no study — handle cleanly

- Guard attribute access on heterogeneous runtime objects. Use hasattr/isinstance checks or explicit casting/typing before accessing .weight, .device, or plugin class attributes.
  Example:
  if hasattr(module, "weight"):
      v = layer_refusal_direction.to(module.weight.device)
  else:
      # handle tensor or non-weight module path

- Rely on framework validation (e.g., pydantic.model_validate) for defaults, but still verify the validated object is present and of the expected type before use.
  Example:
  settings_obj = Settings.model_validate_json(maybe_previous_settings)
  if settings_obj is None:
      # handle missing or invalid settings

- Fail fast and be explicit: if an assumption about presence/shape/type is critical and violated, raise a clear error instead of proceeding silently.

Benefits: reduces accidental data loss, prevents unexpected None-driven behavior, makes control flow explicit, and improves safety when interacting with external APIs and heterogeneous objects.