---
title: Explicit null checks
description: Always use explicit null checks (`value is None` or `value is not None`)
  rather than implicit truthiness evaluations when testing for null/None values. Implicit
  boolean checks can invoke `__bool__` methods leading to unexpected behavior.
repository: apache/mxnet
label: Null Handling
language: Python
comments_count: 4
repository_stars: 20801
---

Always use explicit null checks (`value is None` or `value is not None`) rather than implicit truthiness evaluations when testing for null/None values. Implicit boolean checks can invoke `__bool__` methods leading to unexpected behavior.

**Do this:**
```python
# Explicitly check if out is not None
if out is not None:
    # Use out
    process(out)
```

**Not this:**
```python
# Don't rely on truthiness which may call __bool__
if out:
    # May not behave as expected if __bool__ is implemented
    process(out)
```

For complex types that can represent optional values, use proper optional type wrappers:

In C++:
```cpp
// Use optional wrappers for nullable types
'float or None': 'dmlc::optional<float>'  // Instead of just 'mx_float'
```

When handling values that might have multiple return types or be null:
```python
# Check the specific type before processing
if isinstance(out, NDArrayBase):
    return out
return list(out)  # Convert if needed
```


[
  {
    "discussion_id": "308052505",
    "pr_number": 15678,
    "pr_file": "cpp-package/scripts/OpWrapperGenerator.py",
    "created_at": "2019-07-29T04:33:37+00:00",
    "commented_code": "'caffe-layer-parameter':'::caffe::LayerParameter',\\\n        'NDArray-or-Symbol[]':'const std::vector<Symbol>&',\\\n        'float':'mx_float',\\\n        'float or None':'mx_float',\\",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "308052505",
        "repo_full_name": "apache/mxnet",
        "pr_number": 15678,
        "pr_file": "cpp-package/scripts/OpWrapperGenerator.py",
        "discussion_id": "308052505",
        "commented_code": "@@ -88,8 +88,10 @@ class Arg:\n         'caffe-layer-parameter':'::caffe::LayerParameter',\\\n         'NDArray-or-Symbol[]':'const std::vector<Symbol>&',\\\n         'float':'mx_float',\\\n+        'float or None':'mx_float',\\",
        "comment_created_at": "2019-07-29T04:33:37+00:00",
        "comment_author": "ZhennanQin",
        "comment_body": "Why not `'float or None':'dmlc::optional<float>',\\`?",
        "pr_file_module": null
      },
      {
        "comment_id": "308065098",
        "repo_full_name": "apache/mxnet",
        "pr_number": 15678,
        "pr_file": "cpp-package/scripts/OpWrapperGenerator.py",
        "discussion_id": "308052505",
        "commented_code": "@@ -88,8 +88,10 @@ class Arg:\n         'caffe-layer-parameter':'::caffe::LayerParameter',\\\n         'NDArray-or-Symbol[]':'const std::vector<Symbol>&',\\\n         'float':'mx_float',\\\n+        'float or None':'mx_float',\\",
        "comment_created_at": "2019-07-29T05:58:45+00:00",
        "comment_author": "wkcn",
        "comment_body": "Thank you for pointing it! I will fix it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "853066594",
    "pr_number": 20983,
    "pr_file": "python/mxnet/amp/amp.py",
    "created_at": "2022-04-19T13:20:43+00:00",
    "commented_code": "\"conditional_fp32_ops should be a list of (str, str, list of str)\"\n        cond_ops[op_name].setdefault(attr_name, []).extend(attr_vals)\n\n    nodes_attr = sym.attr_dict()\n    nodes_attrs = sym.attr_dict()\n    nodes_op = {n['name']: n['op'] for n in json.loads(sym.tojson())['nodes']}\n    if not set(excluded_sym_names).issubset(set(nodes_op.keys())):\n        logging.warning(\"excluded_sym_names are not present in the network. Missing layers: {}\".format(\n            set(excluded_sym_names) - set(nodes_op.keys())))\n\n    for node_name, node_op in nodes_op.items():\n        if node_op not in cond_ops:\n            continue\n        node_attrs = nodes_attr[node_name]\n        node_attrs = nodes_attrs[node_name]\n        for attr_name, attr_vals in cond_ops[node_op].items():\n            assert attr_name in node_attrs\n            if node_attrs[attr_name] in attr_vals:\n                excluded_sym_names += node_name\n                excluded_sym_names.append(node_name)\n                break\n    excluded_sym_names = list(set(excluded_sym_names))\n\n    excluded_sym_names = set(excluded_sym_names)\n    for node in sym.get_internals():\n        if node.name in excluded_sym_names:\n            excluded_sym_names.remove(node.name)\n            opt_constraints = node.attr('__opt_constraint__')\n            opt_constraints = 0 if opt_constraints is None else opt_constraints",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "853066594",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20983,
        "pr_file": "python/mxnet/amp/amp.py",
        "discussion_id": "853066594",
        "commented_code": "@@ -497,22 +495,30 @@ def convert_symbol(sym, input_dtypes, param_dtypes, target_dtype=\"float16\", targ\n             \"conditional_fp32_ops should be a list of (str, str, list of str)\"\n         cond_ops[op_name].setdefault(attr_name, []).extend(attr_vals)\n \n-    nodes_attr = sym.attr_dict()\n+    nodes_attrs = sym.attr_dict()\n     nodes_op = {n['name']: n['op'] for n in json.loads(sym.tojson())['nodes']}\n-    if not set(excluded_sym_names).issubset(set(nodes_op.keys())):\n-        logging.warning(\"excluded_sym_names are not present in the network. Missing layers: {}\".format(\n-            set(excluded_sym_names) - set(nodes_op.keys())))\n-\n     for node_name, node_op in nodes_op.items():\n         if node_op not in cond_ops:\n             continue\n-        node_attrs = nodes_attr[node_name]\n+        node_attrs = nodes_attrs[node_name]\n         for attr_name, attr_vals in cond_ops[node_op].items():\n             assert attr_name in node_attrs\n             if node_attrs[attr_name] in attr_vals:\n-                excluded_sym_names += node_name\n+                excluded_sym_names.append(node_name)\n                 break\n-    excluded_sym_names = list(set(excluded_sym_names))\n+\n+    excluded_sym_names = set(excluded_sym_names)\n+    for node in sym.get_internals():\n+        if node.name in excluded_sym_names:\n+            excluded_sym_names.remove(node.name)\n+            opt_constraints = node.attr('__opt_constraint__')\n+            opt_constraints = 0 if opt_constraints is None else opt_constraints",
        "comment_created_at": "2022-04-19T13:20:43+00:00",
        "comment_author": "bgawrych",
        "comment_body": "Does node.attr(...) returns always value in proper type? Is it possible it will return number as string in some case? If yes then |= operator may not work",
        "pr_file_module": null
      },
      {
        "comment_id": "853259275",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20983,
        "pr_file": "python/mxnet/amp/amp.py",
        "discussion_id": "853066594",
        "commented_code": "@@ -497,22 +495,30 @@ def convert_symbol(sym, input_dtypes, param_dtypes, target_dtype=\"float16\", targ\n             \"conditional_fp32_ops should be a list of (str, str, list of str)\"\n         cond_ops[op_name].setdefault(attr_name, []).extend(attr_vals)\n \n-    nodes_attr = sym.attr_dict()\n+    nodes_attrs = sym.attr_dict()\n     nodes_op = {n['name']: n['op'] for n in json.loads(sym.tojson())['nodes']}\n-    if not set(excluded_sym_names).issubset(set(nodes_op.keys())):\n-        logging.warning(\"excluded_sym_names are not present in the network. Missing layers: {}\".format(\n-            set(excluded_sym_names) - set(nodes_op.keys())))\n-\n     for node_name, node_op in nodes_op.items():\n         if node_op not in cond_ops:\n             continue\n-        node_attrs = nodes_attr[node_name]\n+        node_attrs = nodes_attrs[node_name]\n         for attr_name, attr_vals in cond_ops[node_op].items():\n             assert attr_name in node_attrs\n             if node_attrs[attr_name] in attr_vals:\n-                excluded_sym_names += node_name\n+                excluded_sym_names.append(node_name)\n                 break\n-    excluded_sym_names = list(set(excluded_sym_names))\n+\n+    excluded_sym_names = set(excluded_sym_names)\n+    for node in sym.get_internals():\n+        if node.name in excluded_sym_names:\n+            excluded_sym_names.remove(node.name)\n+            opt_constraints = node.attr('__opt_constraint__')\n+            opt_constraints = 0 if opt_constraints is None else opt_constraints",
        "comment_created_at": "2022-04-19T16:18:15+00:00",
        "comment_author": "PawelGlomski-Intel",
        "comment_body": "Good catch! I believe all attributes are strings actually. I added a test covering this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "610245192",
    "pr_number": 20105,
    "pr_file": "python/mxnet/ndarray/numpy_extension/_op.py",
    "created_at": "2021-04-09T00:53:38+00:00",
    "commented_code": "out : NDArray or list of NDArrays\n        The output of this function.\n    \"\"\"\n    return _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n                                    fix_gamma, use_global_stats, output_mean_var, axis,\n                                    cudnn_off, min_calib_range, max_calib_range)\n    out = _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n                                   fix_gamma, use_global_stats, output_mean_var, axis,\n                                   cudnn_off, min_calib_range, max_calib_range)\n    if isinstance(out, NDArrayBase):\n        return out\n    return list(out)",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "610245192",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20105,
        "pr_file": "python/mxnet/ndarray/numpy_extension/_op.py",
        "discussion_id": "610245192",
        "commented_code": "@@ -354,9 +355,12 @@ def batch_norm(x, gamma, beta, running_mean, running_var, eps=1e-3, momentum=0.9\n     out : NDArray or list of NDArrays\n         The output of this function.\n     \"\"\"\n-    return _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n-                                    fix_gamma, use_global_stats, output_mean_var, axis,\n-                                    cudnn_off, min_calib_range, max_calib_range)\n+    out = _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n+                                   fix_gamma, use_global_stats, output_mean_var, axis,\n+                                   cudnn_off, min_calib_range, max_calib_range)\n+    if isinstance(out, NDArrayBase):\n+        return out\n+    return list(out)",
        "comment_created_at": "2021-04-09T00:53:38+00:00",
        "comment_author": "szha",
        "comment_body": "what does this branch handle?",
        "pr_file_module": null
      },
      {
        "comment_id": "610245572",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20105,
        "pr_file": "python/mxnet/ndarray/numpy_extension/_op.py",
        "discussion_id": "610245192",
        "commented_code": "@@ -354,9 +355,12 @@ def batch_norm(x, gamma, beta, running_mean, running_var, eps=1e-3, momentum=0.9\n     out : NDArray or list of NDArrays\n         The output of this function.\n     \"\"\"\n-    return _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n-                                    fix_gamma, use_global_stats, output_mean_var, axis,\n-                                    cudnn_off, min_calib_range, max_calib_range)\n+    out = _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n+                                   fix_gamma, use_global_stats, output_mean_var, axis,\n+                                   cudnn_off, min_calib_range, max_calib_range)\n+    if isinstance(out, NDArrayBase):\n+        return out\n+    return list(out)",
        "comment_created_at": "2021-04-09T00:54:22+00:00",
        "comment_author": "szha",
        "comment_body": "this seems to be a common pattern",
        "pr_file_module": null
      },
      {
        "comment_id": "610274484",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20105,
        "pr_file": "python/mxnet/ndarray/numpy_extension/_op.py",
        "discussion_id": "610245192",
        "commented_code": "@@ -354,9 +355,12 @@ def batch_norm(x, gamma, beta, running_mean, running_var, eps=1e-3, momentum=0.9\n     out : NDArray or list of NDArrays\n         The output of this function.\n     \"\"\"\n-    return _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n-                                    fix_gamma, use_global_stats, output_mean_var, axis,\n-                                    cudnn_off, min_calib_range, max_calib_range)\n+    out = _api_internal.batch_norm(x, gamma, beta, running_mean, running_var, eps, momentum,\n+                                   fix_gamma, use_global_stats, output_mean_var, axis,\n+                                   cudnn_off, min_calib_range, max_calib_range)\n+    if isinstance(out, NDArrayBase):\n+        return out\n+    return list(out)",
        "comment_created_at": "2021-04-09T01:50:34+00:00",
        "comment_author": "barry-jin",
        "comment_body": "Because the out can be NDArraBase type or ADT type. This branch will return out directly if its NDArray, otherwise convert ADT to python list and return list of NDArrays. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "577027310",
    "pr_number": 19685,
    "pr_file": "python/mxnet/_ctypes/cached_op.py",
    "created_at": "2021-02-16T18:01:48+00:00",
    "commented_code": "\"\"\"ctypes implementation of imperative invoke wrapper\"\"\"\n        # New FFI only supports numpy ndarray\n        default_ctx = kwargs.pop('default_ctx', None)\n        out = kwargs.pop('out', None)\n        if kwargs:\n            raise TypeError(\n                \"CachedOp.__call__ got unexpected keyword argument(s): \" + \\\n                ', '.join(kwargs.keys()))\n        if self.is_np_sym:\n            if len(args) == 1 and args[0] is None:\n                args = []\n            type_id = default_ctx.device_typeid if default_ctx else None\n            device_id = default_ctx.device_id if default_ctx else None\n            out_arg = out if out and not isinstance(out, NDArrayBase) else (out, )",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "577027310",
        "repo_full_name": "apache/mxnet",
        "pr_number": 19685,
        "pr_file": "python/mxnet/_ctypes/cached_op.py",
        "discussion_id": "577027310",
        "commented_code": "@@ -74,27 +74,32 @@ def __call__(self, *args, **kwargs):\n         \"\"\"ctypes implementation of imperative invoke wrapper\"\"\"\n         # New FFI only supports numpy ndarray\n         default_ctx = kwargs.pop('default_ctx', None)\n+        out = kwargs.pop('out', None)\n+        if kwargs:\n+            raise TypeError(\n+                \"CachedOp.__call__ got unexpected keyword argument(s): \" + \\\n+                ', '.join(kwargs.keys()))\n         if self.is_np_sym:\n             if len(args) == 1 and args[0] is None:\n                 args = []\n             type_id = default_ctx.device_typeid if default_ctx else None\n             device_id = default_ctx.device_id if default_ctx else None\n+            out_arg = out if out and not isinstance(out, NDArrayBase) else (out, )",
        "comment_created_at": "2021-02-16T18:01:48+00:00",
        "comment_author": "szha",
        "comment_body": "if the intention is to check whether `out` is not None, it's probably better to write it that way. Otherwise, `if NDArray` will call `__bool__` of NDArray",
        "pr_file_module": null
      }
    ]
  }
]
