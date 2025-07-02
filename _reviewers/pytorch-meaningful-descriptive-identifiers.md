---
title: Meaningful descriptive identifiers
description: Choose identifiers (variable/function/class names) that clearly convey
  their purpose and follow established conventions. Variable names should be semantically
  meaningful, accurately reflecting their content and usage throughout their lifecycle.
repository: pytorch/pytorch
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 91169
---

Choose identifiers (variable/function/class names) that clearly convey their purpose and follow established conventions. Variable names should be semantically meaningful, accurately reflecting their content and usage throughout their lifecycle.

Key guidelines:
- Use descriptive names over vague ones (e.g., `zip_path` instead of `new_path` when handling zip files)
- Avoid Python reserved keywords (e.g., use `input_` instead of `input`)
- Prefix internal/private functions with a single underscore (e.g., `_detect_linux_pkg_manager`)
- Avoid redundant prefixes in nested namespaces (e.g., no `cpp_` prefix for members already in a `cpp` class)
- Choose more descriptive method names that clearly express their purpose:
  ```python
  # Less clear:
  self.skip_mutation(var)
  self.remove_skip_mutation(var)
  
  # More clear:
  self.ignore_mutations_on(var)
  self.stop_ignoring_mutations_on(var)
  ```
- Prefer objective, technical terms over subjective descriptors (e.g., `topk` rather than `fast`)

When variable usage changes during implementation, rename accordingly to maintain semantic clarity.


[
  {
    "discussion_id": "2116854356",
    "pr_number": 154770,
    "pr_file": ".github/actions/reuse-old-whl/reuse_old_whl.py",
    "created_at": "2025-05-30T23:19:38+00:00",
    "commented_code": "subprocess.check_output(\n            [\"unzip\", \"-o\", new_path, \"-d\", f\"artifacts/dist/{new_path.stem}\"],\n        )\n\n        # Remove the old wheel (which is now a zip file)\n        os.remove(new_path)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2116854356",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154770,
        "pr_file": ".github/actions/reuse-old-whl/reuse_old_whl.py",
        "discussion_id": "2116854356",
        "commented_code": "@@ -190,6 +190,10 @@ def unzip_artifact_and_replace_files() -> None:\n         subprocess.check_output(\n             [\"unzip\", \"-o\", new_path, \"-d\", f\"artifacts/dist/{new_path.stem}\"],\n         )\n+\n+        # Remove the old wheel (which is now a zip file)\n+        os.remove(new_path)",
        "comment_created_at": "2025-05-30T23:19:38+00:00",
        "comment_author": "ZainRizvi",
        "comment_body": "minor nit: consider renaming `new_path` to `zip_path` for clarity",
        "pr_file_module": null
      },
      {
        "comment_id": "2116888961",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154770,
        "pr_file": ".github/actions/reuse-old-whl/reuse_old_whl.py",
        "discussion_id": "2116854356",
        "commented_code": "@@ -190,6 +190,10 @@ def unzip_artifact_and_replace_files() -> None:\n         subprocess.check_output(\n             [\"unzip\", \"-o\", new_path, \"-d\", f\"artifacts/dist/{new_path.stem}\"],\n         )\n+\n+        # Remove the old wheel (which is now a zip file)\n+        os.remove(new_path)",
        "comment_created_at": "2025-05-31T00:11:20+00:00",
        "comment_author": "clee2000",
        "comment_body": "probably a later pr, new_path is used in a bunch of places that are unrelated to this specific change",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1976180681",
    "pr_number": 147881,
    "pr_file": "torch/export/dynamic_shapes.py",
    "created_at": "2025-03-01T00:45:12+00:00",
    "commented_code": "- AUTO means automatic inference of shape (static or dynamic).\n    - STATIC means static shape (always specialized).\n    - DYNAMIC means dynamic, will error out if specialized.\n    - _OBLIVIOUS allocates an backed symbol with size-oblivious semantics.",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "1976180681",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 147881,
        "pr_file": "torch/export/dynamic_shapes.py",
        "discussion_id": "1976180681",
        "commented_code": "@@ -46,11 +46,13 @@ class _DimHint(Enum):\n     - AUTO means automatic inference of shape (static or dynamic).\n     - STATIC means static shape (always specialized).\n     - DYNAMIC means dynamic, will error out if specialized.\n+    - _OBLIVIOUS allocates an backed symbol with size-oblivious semantics.",
        "comment_created_at": "2025-03-01T00:45:12+00:00",
        "comment_author": "avikchaudhuri",
        "comment_body": "It's probably good to pick a name that is more meaningful here. I guess the `_` means you're not committing to the name lol.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2071453448",
    "pr_number": 151780,
    "pr_file": "torch/_inductor/config.py",
    "created_at": "2025-05-02T11:03:55+00:00",
    "commented_code": "# decomposed into 7x4x2 thread blocks along MxNxK of a GEMM.\n    gemm_thread_factors = os.environ.get(\"TORCHINDUCTOR_CPP_GEMM_THREAD_FACTORS\", None)\n\n    # Set GEMM Transverse strategy: support VERTICAL, HORIZONTAL\n    # If both are enabled, the strategy will be selected based on the heuristic.\n    cpp_gemm_transverse_strategy = os.environ.get(",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2071453448",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 151780,
        "pr_file": "torch/_inductor/config.py",
        "discussion_id": "2071453448",
        "commented_code": "@@ -997,6 +997,12 @@ class cpp:\n     # decomposed into 7x4x2 thread blocks along MxNxK of a GEMM.\n     gemm_thread_factors = os.environ.get(\"TORCHINDUCTOR_CPP_GEMM_THREAD_FACTORS\", None)\n \n+    # Set GEMM Transverse strategy: support VERTICAL, HORIZONTAL\n+    # If both are enabled, the strategy will be selected based on the heuristic.\n+    cpp_gemm_transverse_strategy = os.environ.get(",
        "comment_created_at": "2025-05-02T11:03:55+00:00",
        "comment_author": "jgong5",
        "comment_body": " nit: you don't have to add \"cpp_\" prefix to the configuration name since it is already inside the `cpp` class.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2159742806",
    "pr_number": 156312,
    "pr_file": "torch/_functorch/eager_transforms.py",
    "created_at": "2025-06-20T22:52:41+00:00",
    "commented_code": "...     c.add_(1)\n        ...     return b\n        ...\n        >>> inpt = torch.randn(2)\n        >>> input = torch.randn(2)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2159742806",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156312,
        "pr_file": "torch/_functorch/eager_transforms.py",
        "discussion_id": "2159742806",
        "commented_code": "@@ -1516,18 +1516,18 @@ def functionalize(func: Callable, *, remove: str = \"mutations\") -> Callable:\n         ...     c.add_(1)\n         ...     return b\n         ...\n-        >>> inpt = torch.randn(2)\n+        >>> input = torch.randn(2)",
        "comment_created_at": "2025-06-20T22:52:41+00:00",
        "comment_author": "albanD",
        "comment_body": "This is done on purpose as \"input\" is a reserved keyword in python",
        "pr_file_module": null
      },
      {
        "comment_id": "2161678229",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156312,
        "pr_file": "torch/_functorch/eager_transforms.py",
        "discussion_id": "2159742806",
        "commented_code": "@@ -1516,18 +1516,18 @@ def functionalize(func: Callable, *, remove: str = \"mutations\") -> Callable:\n         ...     c.add_(1)\n         ...     return b\n         ...\n-        >>> inpt = torch.randn(2)\n+        >>> input = torch.randn(2)",
        "comment_created_at": "2025-06-23T13:45:01+00:00",
        "comment_author": "XuehaiPan",
        "comment_body": "Changed to `input_` as a common practice.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2161539521",
    "pr_number": 156312,
    "pr_file": "torch/_functorch/_aot_autograd/runtime_wrappers.py",
    "created_at": "2025-06-23T12:46:40+00:00",
    "commented_code": "storage_ref_to_idx: dict[StorageWeakRef, list[int]] = collections.defaultdict(list)\n    base_args = []\n    other_args = []\n    for i, inpt in enumerate(fwd_inputs):\n        if isinstance(inpt, Tensor):\n            storage_ref = StorageWeakRef(inpt.untyped_storage())\n    for i, input in enumerate(fwd_inputs):",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2161539521",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156312,
        "pr_file": "torch/_functorch/_aot_autograd/runtime_wrappers.py",
        "discussion_id": "2161539521",
        "commented_code": "@@ -1344,12 +1344,12 @@ def _same_dtype_views(view1, view2):\n     storage_ref_to_idx: dict[StorageWeakRef, list[int]] = collections.defaultdict(list)\n     base_args = []\n     other_args = []\n-    for i, inpt in enumerate(fwd_inputs):\n-        if isinstance(inpt, Tensor):\n-            storage_ref = StorageWeakRef(inpt.untyped_storage())\n+    for i, input in enumerate(fwd_inputs):",
        "comment_created_at": "2025-06-23T12:46:40+00:00",
        "comment_author": "albanD",
        "comment_body": "These are not really ok either. We shouldn't override the builtin input wherever possible",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2131477194",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2025-06-06T04:32:11+00:00",
    "commented_code": "return smi\n\n\ndef detect_linux_pkg_manager():",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2131477194",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "2131477194",
        "commented_code": "@@ -243,6 +269,149 @@ def get_nvidia_smi():\n     return smi\n \n \n+def detect_linux_pkg_manager():",
        "comment_created_at": "2025-06-06T04:32:11+00:00",
        "comment_author": "malfet",
        "comment_body": "```suggestion\r\ndef _detect_linux_pkg_manager():\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2165261508",
    "pr_number": 156683,
    "pr_file": "torch/_inductor/config.py",
    "created_at": "2025-06-25T01:34:57+00:00",
    "commented_code": ").upper()\n\n\n# Specify the size of the benchmarking space for GEMM autotuning with the neural network model.\n# SAME     - There should be no functional difference between this and max_autotune_gemm_search_space\n# DEFAULT  - Benchmark the same number of configs as max_autotune, but search over a larger space using the model\n# <number> - Use the top <number> configs as predicted by the model.\ndef parse_matmul_gemm_autotune_benchmark_space() -> Union[\n    int, Literal[\"SAME\", \"DEFAULT\"]\n]:\n    value = os.environ.get(\"TORCHINDUCTOR_MATMUL_GEMM_AUTOTUNE_BENCHMARK_SPACE\")\n    if value is not None:\n        # Try to parse as an integer first\n        try:\n            return int(value)\n        except ValueError:\n            if os.environ.get(\"TORCHINDUCTOR_FAST_AUTOTUNE\") == \"1\":\n                return 1\n            return \"DEFAULT\"\n    # just keep the search space the same as\n    return \"SAME\"\n\n\nmatmul_gemm_autotune_benchmark_space: Union[int, Literal[\"SAME\", \"DEFAULT\"]] = (\n    parse_matmul_gemm_autotune_benchmark_space()\n)\n\n\ndef parse_matmul_gemm_autotune_search_space() -> Literal[\"DEFAULT\", \"EXHAUSTIVE\"]:\n    benchmarking_space = parse_matmul_gemm_autotune_benchmark_space()\n    if benchmarking_space == \"SAME\":\n        val = os.environ.get(\n            \"TORCHINDUCTOR_MATMUL_GEMM_AUTOTUNE_BENCHMARK_SPACE\", \"DEFAULT\"\n        ).upper()\n        if val in [\"DEFAULT\", \"EXHAUSTIVE\"]:\n            return val  # type: ignore[return-value]\n        return \"DEFAULT\"\n    # If we are using the model, the configs we're considering should be exhaustive\n    return \"EXHAUSTIVE\"\n\n\n# Specify the size of the search space for GEMM autotuning.\n# DEFAULT     - balance between compile time overhead and performance\n# EXHAUSTIVE  - maximize performance\nmax_autotune_gemm_search_space: Literal[\"DEFAULT\", \"EXHAUSTIVE\"] = os.environ.get(\n    \"TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE\", \"DEFAULT\"\n).upper()  # type: ignore[assignment]\nmax_autotune_gemm_search_space: Literal[\"DEFAULT\", \"EXHAUSTIVE\"] = (",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2165261508",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156683,
        "pr_file": "torch/_inductor/config.py",
        "discussion_id": "2165261508",
        "commented_code": "@@ -443,12 +443,61 @@ def prologue_fusion_enabled() -> bool:\n ).upper()\n \n \n+# Specify the size of the benchmarking space for GEMM autotuning with the neural network model.\n+# SAME     - There should be no functional difference between this and max_autotune_gemm_search_space\n+# DEFAULT  - Benchmark the same number of configs as max_autotune, but search over a larger space using the model\n+# <number> - Use the top <number> configs as predicted by the model.\n+def parse_matmul_gemm_autotune_benchmark_space() -> Union[\n+    int, Literal[\"SAME\", \"DEFAULT\"]\n+]:\n+    value = os.environ.get(\"TORCHINDUCTOR_MATMUL_GEMM_AUTOTUNE_BENCHMARK_SPACE\")\n+    if value is not None:\n+        # Try to parse as an integer first\n+        try:\n+            return int(value)\n+        except ValueError:\n+            if os.environ.get(\"TORCHINDUCTOR_FAST_AUTOTUNE\") == \"1\":\n+                return 1\n+            return \"DEFAULT\"\n+    # just keep the search space the same as\n+    return \"SAME\"\n+\n+\n+matmul_gemm_autotune_benchmark_space: Union[int, Literal[\"SAME\", \"DEFAULT\"]] = (\n+    parse_matmul_gemm_autotune_benchmark_space()\n+)\n+\n+\n+def parse_matmul_gemm_autotune_search_space() -> Literal[\"DEFAULT\", \"EXHAUSTIVE\"]:\n+    benchmarking_space = parse_matmul_gemm_autotune_benchmark_space()\n+    if benchmarking_space == \"SAME\":\n+        val = os.environ.get(\n+            \"TORCHINDUCTOR_MATMUL_GEMM_AUTOTUNE_BENCHMARK_SPACE\", \"DEFAULT\"\n+        ).upper()\n+        if val in [\"DEFAULT\", \"EXHAUSTIVE\"]:\n+            return val  # type: ignore[return-value]\n+        return \"DEFAULT\"\n+    # If we are using the model, the configs we're considering should be exhaustive\n+    return \"EXHAUSTIVE\"\n+\n+\n # Specify the size of the search space for GEMM autotuning.\n # DEFAULT     - balance between compile time overhead and performance\n # EXHAUSTIVE  - maximize performance\n-max_autotune_gemm_search_space: Literal[\"DEFAULT\", \"EXHAUSTIVE\"] = os.environ.get(\n-    \"TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE\", \"DEFAULT\"\n-).upper()  # type: ignore[assignment]\n+max_autotune_gemm_search_space: Literal[\"DEFAULT\", \"EXHAUSTIVE\"] = (",
        "comment_created_at": "2025-06-25T01:34:57+00:00",
        "comment_author": "coconutruben",
        "comment_body": "I would why away from subjective names like fast for now and rather do more sterile things until we have a better idea about usability, topk, etc, but that's more of a nit, not a blocker",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2170703508",
    "pr_number": 155886,
    "pr_file": "torch/_dynamo/side_effects.py",
    "created_at": "2025-06-27T03:52:41+00:00",
    "commented_code": "# Only applicable if this graph is created from Dynamo tracing in Compiled Autograd.\n        self.ca_final_callbacks_var = None\n\n        # Tracks VariableTracker objects whose mutations can be skipped.\n        # For normal mutated variables, Dynamo generates code to replay/reconstruct\n        # the mutations after graph execution. However, variables in this set have\n        # their mutations ignored - the mutations happen during\n        # execution but don't need to be replayed in the generated code.\n        # Used for temporary mutations in contexts like torch.func.functional_call,\n        # where module parameters/buffers are modified but later restored.\n        self.skip_mutation_variables = set()\n\n    def skip_mutation(self, var):\n        \"\"\"Mutations to this variable will be executed but not not tracked,\n        typically used for temporary mutations that are later restored.\"\"\"\n        self.skip_mutation_variables.add(var)\n\n    def remove_skip_mutation(self, var):\n        \"\"\"Remove a variable from the skip mutation set, restoring normal mutation tracking.\"\"\"\n        if var in self.skip_mutation_variables:\n            self.skip_mutation_variables.remove(var)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2170703508",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155886,
        "pr_file": "torch/_dynamo/side_effects.py",
        "discussion_id": "2170703508",
        "commented_code": "@@ -124,6 +124,25 @@ def __init__(\n         # Only applicable if this graph is created from Dynamo tracing in Compiled Autograd.\n         self.ca_final_callbacks_var = None\n \n+        # Tracks VariableTracker objects whose mutations can be skipped.\n+        # For normal mutated variables, Dynamo generates code to replay/reconstruct\n+        # the mutations after graph execution. However, variables in this set have\n+        # their mutations ignored - the mutations happen during\n+        # execution but don't need to be replayed in the generated code.\n+        # Used for temporary mutations in contexts like torch.func.functional_call,\n+        # where module parameters/buffers are modified but later restored.\n+        self.skip_mutation_variables = set()\n+\n+    def skip_mutation(self, var):\n+        \"\"\"Mutations to this variable will be executed but not not tracked,\n+        typically used for temporary mutations that are later restored.\"\"\"\n+        self.skip_mutation_variables.add(var)\n+\n+    def remove_skip_mutation(self, var):\n+        \"\"\"Remove a variable from the skip mutation set, restoring normal mutation tracking.\"\"\"\n+        if var in self.skip_mutation_variables:\n+            self.skip_mutation_variables.remove(var)",
        "comment_created_at": "2025-06-27T03:52:41+00:00",
        "comment_author": "zou3519",
        "comment_body": "Nit: some more descriptive names please. More words is fine.\r\n\r\nself.skip_mutation(var)  -> self.ignore_mutations_on(var)\r\nself.remove_skip_mutation(var) -> self.stop_ignoring_mutations_on(var)\r\nself.skip_mutation_variables -> self.ignore_mutation_on_these_variables = set()",
        "pr_file_module": null
      }
    ]
  }
]
