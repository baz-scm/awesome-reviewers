---
title: Specific exception handling
description: 'Always catch specific exception types rather than using generic `except
  Exception` blocks when you know which exceptions to expect. Using specific exception
  types:'
repository: pytorch/pytorch
label: Error Handling
language: Python
comments_count: 4
repository_stars: 91169
---

Always catch specific exception types rather than using generic `except Exception` blocks when you know which exceptions to expect. Using specific exception types:

1. Improves code clarity by making the expected failure modes explicit
2. Prevents accidentally masking unexpected errors that should be propagated
3. Makes debugging easier by allowing unrelated errors to surface properly

When catching exceptions:

```python
# Bad practice
try:
    value = int(some_float)
except Exception as exc:  # Too broad, catches everything
    handle_error()

# Good practice
try:
    value = int(some_float)
except (ValueError, OverflowError) as exc:  # Specific exceptions
    # Now we handle only the errors we expect
    handle_error()
```

If you're logging errors before re-raising, include both stdout and stderr for better debugging:

```python
try:
    subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed:\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}", file=sys.stderr)
    raise  # Re-raise to propagate the error
```

Only catch generic exceptions when you have a compelling reason, such as protecting critical cleanup operations, and even then consider whether specific exception types would be more appropriate.


[
  {
    "discussion_id": "2169092276",
    "pr_number": 155978,
    "pr_file": "torch/_dynamo/variables/constant.py",
    "created_at": "2025-06-26T13:34:37+00:00",
    "commented_code": "raise_observed_exception(type(e), tx)\n        elif isinstance(self.value, (float, int)):\n            if not (args or kwargs):\n                return ConstantVariable.create(getattr(self.value, name)())\n                try:\n                    return ConstantVariable.create(getattr(self.value, name)())\n                except Exception as exc:",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2169092276",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155978,
        "pr_file": "torch/_dynamo/variables/constant.py",
        "discussion_id": "2169092276",
        "commented_code": "@@ -173,7 +173,14 @@ def call_method(\n                 raise_observed_exception(type(e), tx)\n         elif isinstance(self.value, (float, int)):\n             if not (args or kwargs):\n-                return ConstantVariable.create(getattr(self.value, name)())\n+                try:\n+                    return ConstantVariable.create(getattr(self.value, name)())\n+                except Exception as exc:",
        "comment_created_at": "2025-06-26T13:34:37+00:00",
        "comment_author": "zou3519",
        "comment_body": "Is there a specific exception we're looking for here?",
        "pr_file_module": null
      },
      {
        "comment_id": "2169149235",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155978,
        "pr_file": "torch/_dynamo/variables/constant.py",
        "discussion_id": "2169092276",
        "commented_code": "@@ -173,7 +173,14 @@ def call_method(\n                 raise_observed_exception(type(e), tx)\n         elif isinstance(self.value, (float, int)):\n             if not (args or kwargs):\n-                return ConstantVariable.create(getattr(self.value, name)())\n+                try:\n+                    return ConstantVariable.create(getattr(self.value, name)())\n+                except Exception as exc:",
        "comment_created_at": "2025-06-26T14:00:02+00:00",
        "comment_author": "guilhermeleobas",
        "comment_body": "OverflowError and ValueError. The last one appears when one tries to convert a NaN to an int.\r\n\r\n```python\r\nIn [5]: int(math.nan)\r\n---------------------------------------------------------------------------\r\nValueError                                Traceback (most recent call last)\r\nCell In[5], line 1\r\n----> 1 int(math.nan)\r\n\r\nValueError: cannot convert float NaN to integer\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2049250850",
    "pr_number": 149697,
    "pr_file": "torch/_inductor/utils.py",
    "created_at": "2025-04-17T15:57:52+00:00",
    "commented_code": "@functools.lru_cache(None)\ndef get_device_tflops(dtype: torch.dtype) -> int:\ndef get_device_tflops(dtype: torch.dtype) -> float:\n    \"\"\"\n    We don't want to throw errors in this function. First check to see if the device is in device_info.py,\n    then fall back to the inaccurate triton estimation.\n    \"\"\"\n    try:",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2049250850",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 149697,
        "pr_file": "torch/_inductor/utils.py",
        "discussion_id": "2049250850",
        "commented_code": "@@ -1887,16 +1895,26 @@ def get_backend_num_stages() -> int:\n \n \n @functools.lru_cache(None)\n-def get_device_tflops(dtype: torch.dtype) -> int:\n+def get_device_tflops(dtype: torch.dtype) -> float:\n+    \"\"\"\n+    We don't want to throw errors in this function. First check to see if the device is in device_info.py,\n+    then fall back to the inaccurate triton estimation.\n+    \"\"\"\n+    try:",
        "comment_created_at": "2025-04-17T15:57:52+00:00",
        "comment_author": "eellison",
        "comment_body": "Can we have datasheet_tops just return None if unsuccessful ? I prefer to avoid pattern where we're catching arbitrary exceptions. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2159235161",
    "pr_number": 156148,
    "pr_file": "torch/_dynamo/variables/builtin.py",
    "created_at": "2025-06-20T15:24:28+00:00",
    "commented_code": "def expand_list_like(tx: \"InstructionTranslator\", lst, const):\n            if isinstance(lst, ConstantVariable):\n                lst, const = const, lst\n            return lst.__class__(\n                items=lst.items * const.as_python_constant(),\n                mutation_type=ValueMutationNew(),\n            )\n            try:\n                return lst.__class__(\n                    items=lst.items * const.as_python_constant(),\n                    mutation_type=ValueMutationNew(),\n                )\n            except Exception as exc:\n                # MemoryError\n                raise_observed_exception(\n                    type(exc),\n                    tx,\n                    args=list(map(ConstantVariable.create, exc.args)),\n                )",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2159235161",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156148,
        "pr_file": "torch/_dynamo/variables/builtin.py",
        "discussion_id": "2159235161",
        "commented_code": "@@ -542,10 +542,18 @@ def list_iadd_handler(tx: \"InstructionTranslator\", a, b):\n         def expand_list_like(tx: \"InstructionTranslator\", lst, const):\n             if isinstance(lst, ConstantVariable):\n                 lst, const = const, lst\n-            return lst.__class__(\n-                items=lst.items * const.as_python_constant(),\n-                mutation_type=ValueMutationNew(),\n-            )\n+            try:\n+                return lst.__class__(\n+                    items=lst.items * const.as_python_constant(),\n+                    mutation_type=ValueMutationNew(),\n+                )\n+            except Exception as exc:\n+                # MemoryError\n+                raise_observed_exception(\n+                    type(exc),\n+                    tx,\n+                    args=list(map(ConstantVariable.create, exc.args)),\n+                )",
        "comment_created_at": "2025-06-20T15:24:28+00:00",
        "comment_author": "zou3519",
        "comment_body": "What exceptions are we trying to catch here? If it's just MemoryError then we should use that in the except block.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2173506878",
    "pr_number": 157203,
    "pr_file": "torch/_inductor/codecache.py",
    "created_at": "2025-06-28T19:48:33+00:00",
    "commented_code": "# Include SASS for the current specific arch\n                        f\"-gencode arch=compute_{current_arch},code=sm_{current_arch} \"\n                    )\n                    subprocess.run(\n                        cmd.split(), capture_output=True, text=True, check=True\n                    )\n                    try:\n                        subprocess.run(\n                            cmd.split(),\n                            capture_output=True,\n                            text=True,\n                            check=True,\n                        )\n                    except subprocess.CalledProcessError as e:\n                        print(f\"{cmd} failed with: {e.stderr}\")",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2173506878",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157203,
        "pr_file": "torch/_inductor/codecache.py",
        "discussion_id": "2173506878",
        "commented_code": "@@ -2143,9 +2143,15 @@ def _pad_to_alignment(raw_bytes: bytes) -> bytes:\n                         # Include SASS for the current specific arch\n                         f\"-gencode arch=compute_{current_arch},code=sm_{current_arch} \"\n                     )\n-                    subprocess.run(\n-                        cmd.split(), capture_output=True, text=True, check=True\n-                    )\n+                    try:\n+                        subprocess.run(\n+                            cmd.split(),\n+                            capture_output=True,\n+                            text=True,\n+                            check=True,\n+                        )\n+                    except subprocess.CalledProcessError as e:\n+                        print(f\"{cmd} failed with: {e.stderr}\")",
        "comment_created_at": "2025-06-28T19:48:33+00:00",
        "comment_author": "jansel",
        "comment_body": "```suggestion\r\n                        print(f\"{cmd} failed with:\\nstdout:\\n{e.stdout}\\nstderr:\\n{e.stderr}\", file=sys.stderr)\r\n                        raise\r\n```\r\n\r\nI assume you want to re-raise here?",
        "pr_file_module": null
      }
    ]
  }
]
