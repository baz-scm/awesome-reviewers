---
title: Idempotency Key Completeness
description: When implementing API endpoints/clients that use idempotency keys, ensure
  the idempotency key includes **all request fields that can change the output** (including
  aliases/variants). Otherwise, different calls can collide and incorrectly deduplicate.
repository: calesthio/OpenMontage
label: API
language: Python
comments_count: 2
repository_stars: 46544
---

When implementing API endpoints/clients that use idempotency keys, ensure the idempotency key includes **all request fields that can change the output** (including aliases/variants). Otherwise, different calls can collide and incorrectly deduplicate.

Apply this by:
- Keeping a per-operation `idempotency_key_fields` (or equivalent) that enumerates every output-affecting input.
- Including “indirect” fields like model aliases, operation/mode/resolution/sound settings, negative prompts, reference inputs, multi-shot/elements, watermark, and any selection/timing/volume controls.
- Treating request aliases as equivalent but still keying on the effective value (e.g., audio file/url/path synonyms).
- Adding regression coverage that verifies: for each output-affecting parameter, changing it changes the generated idempotency key.

Example (pattern):
```python
class SomeKlingTool(BaseTool):
    # ...
    idempotency_key_fields = [
        # Identity/variant
        "operation",
        "model_name_or_alias",
        # Content
        "prompt",
        "negative_prompt",
        # Controls
        "duration",
        "aspect_ratio",
        "resolution",
        "mode",
        "sound",
        # References / selection
        "reference_image_url_or_path",
        "face_choose",
        "auto_select_face",
        # Timing / audio
        "sound_start_time",
        "sound_end_time",
        "sound_insert_time",
        "sound_volume",
        "original_audio_volume",
    ]
```
This standard prevents cross-variant API calls (e.g., different operations, reference sets, or audio selection modes) from deduplicating incorrectly.