---
title: sanitize filesystem inputs
description: When constructing filesystem paths or filenames from external input (model
  names, user-provided identifiers, etc.), treat those strings as untrusted. Whitelist
  allowed characters, disallow dots and path separators, and verify the final path
  stays inside the intended directory to prevent path traversal or accidental file
  access/deletion.
repository: p-e-w/heretic
label: Security
language: Python
comments_count: 1
repository_stars: 5002
---

When constructing filesystem paths or filenames from external input (model names, user-provided identifiers, etc.), treat those strings as untrusted. Whitelist allowed characters, disallow dots and path separators, and verify the final path stays inside the intended directory to prevent path traversal or accidental file access/deletion.

Why: Allowing '.' or path separators can enable path traversal (e.g., "model/../../path") or surprising behavior later if code changes. This is a security vulnerability and should be mitigated by input validation and path containment checks.

How to apply:
- Prefer a strict whitelist of characters (e.g., letters, digits, underscore, dash). Do not allow '.' or os.path.sep characters.
- After building a path, canonicalize it with os.path.normpath and verify it is a child of the intended directory.
- Consider using a safe mapping (hash or UUID) instead of the raw name when appropriate.

Example (based on the discussion):

# safe sanitizer
import os
import re

ALLOWED = re.compile(r"^[A-Za-z0-9_-]+$")  # note: no dot

def safe_name(name):
    if not ALLOWED.match(name):
        raise ValueError("invalid name")
    return name

base_dir = settings.study_checkpoint_dir
user_name = safe_name(model_name)
filename = os.path.join(base_dir, user_name + ".json")

# defense-in-depth: ensure containment
norm_base = os.path.normpath(base_dir)
norm_path = os.path.normpath(filename)
if not norm_path.startswith(norm_base + os.path.sep) and norm_path != norm_base:
    raise ValueError("resulting path escapes base directory")

References: discussion indices [0].