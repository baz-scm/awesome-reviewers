---
title: Optimize iteration patterns
description: 'When iterating through collections, choose the most efficient iteration
  pattern based on what information you actually need. If you only need the elements
  without using their indices, use direct iteration instead of enumerate:'
repository: apache/mxnet
label: Algorithms
language: Python
comments_count: 6
repository_stars: 20801
---

When iterating through collections, choose the most efficient iteration pattern based on what information you actually need. If you only need the elements without using their indices, use direct iteration instead of enumerate:

```python
# Instead of this (inefficient):
for _, item in enumerate(collection):
    process(item)

# Do this (efficient and clearer):
for item in collection:
    process(item)
```

This optimization removes unnecessary index variable allocation and makes the code more readable. The principle applies to any iterative algorithm - don't compute values you won't use. Similarly, when testing object capabilities (like whether an object is iterable), check for specific attributes (`hasattr(obj, '__iter__')`) rather than calling functions that might have side effects like prefetching data.


[
  {
    "discussion_id": "360245337",
    "pr_number": 17129,
    "pr_file": "python/mxnet/gluon/contrib/estimator/estimator.py",
    "created_at": "2019-12-20T06:45:46+00:00",
    "commented_code": "batch_axis : int, default 0\n            Batch axis to split the training data into devices.\n        \"\"\"\n        if not isinstance(train_data, DataLoader):\n            raise ValueError(\"Estimator only support input as Gluon DataLoader. Alternatively, you \"\n                             \"can transform your DataIter or any NDArray into Gluon DataLoader. \"\n                             \"Refer to gluon.data.dataloader\")\n        try:\n            is_iterable = iter(train_data)",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "360245337",
        "repo_full_name": "apache/mxnet",
        "pr_number": 17129,
        "pr_file": "python/mxnet/gluon/contrib/estimator/estimator.py",
        "discussion_id": "360245337",
        "commented_code": "@@ -358,10 +359,11 @@ def fit(self, train_data,\n         batch_axis : int, default 0\n             Batch axis to split the training data into devices.\n         \"\"\"\n-        if not isinstance(train_data, DataLoader):\n-            raise ValueError(\"Estimator only support input as Gluon DataLoader. Alternatively, you \"\n-                             \"can transform your DataIter or any NDArray into Gluon DataLoader. \"\n-                             \"Refer to gluon.data.dataloader\")\n+        try:\n+            is_iterable = iter(train_data)",
        "comment_created_at": "2019-12-20T06:45:46+00:00",
        "comment_author": "leezu",
        "comment_body": "Calling `iter(train_data)` can have side-effects, such as starting prefetching. See https://github.com/dmlc/gluon-nlp/blob/297e14732849f2b8025de6e2bf80ac05cab82b44/src/gluonnlp/data/stream.py#L341\r\n\r\nThus `iter` must only be invoked once. The enumerate call below invokes `iter` a second time implicitly. If you want to invoke `iter` manually, you need to use a while loop and `next` to iterate over the elements until `StopIteration` is raised.",
        "pr_file_module": null
      },
      {
        "comment_id": "360251070",
        "repo_full_name": "apache/mxnet",
        "pr_number": 17129,
        "pr_file": "python/mxnet/gluon/contrib/estimator/estimator.py",
        "discussion_id": "360245337",
        "commented_code": "@@ -358,10 +359,11 @@ def fit(self, train_data,\n         batch_axis : int, default 0\n             Batch axis to split the training data into devices.\n         \"\"\"\n-        if not isinstance(train_data, DataLoader):\n-            raise ValueError(\"Estimator only support input as Gluon DataLoader. Alternatively, you \"\n-                             \"can transform your DataIter or any NDArray into Gluon DataLoader. \"\n-                             \"Refer to gluon.data.dataloader\")\n+        try:\n+            is_iterable = iter(train_data)",
        "comment_created_at": "2019-12-20T07:14:42+00:00",
        "comment_author": "liuzh47",
        "comment_body": "what about using `hasattr(train_data, '__iter__')` to check if the `train_data` is iterable or not? Do we need to cover the case if `train_data` has implemented `__getitem__`?",
        "pr_file_module": null
      },
      {
        "comment_id": "360254544",
        "repo_full_name": "apache/mxnet",
        "pr_number": 17129,
        "pr_file": "python/mxnet/gluon/contrib/estimator/estimator.py",
        "discussion_id": "360245337",
        "commented_code": "@@ -358,10 +359,11 @@ def fit(self, train_data,\n         batch_axis : int, default 0\n             Batch axis to split the training data into devices.\n         \"\"\"\n-        if not isinstance(train_data, DataLoader):\n-            raise ValueError(\"Estimator only support input as Gluon DataLoader. Alternatively, you \"\n-                             \"can transform your DataIter or any NDArray into Gluon DataLoader. \"\n-                             \"Refer to gluon.data.dataloader\")\n+        try:\n+            is_iterable = iter(train_data)",
        "comment_created_at": "2019-12-20T07:30:58+00:00",
        "comment_author": "leezu",
        "comment_body": "You need to check both. Thus `hasattr(train_data, '__iter__') or hasattr(train_data, '__getitem__')` should be fine.\r\n\r\nSee \r\n\r\n> An object capable of returning its members one at a time. Examples of iterables include all sequence types (such as list, str, and tuple) and some non-sequence types like dict, file objects, and objects of any classes you define with an `__iter__()` method or with a `__getitem__()` method that implements Sequence semantics.\r\n\r\nhttps://docs.python.org/3/glossary.html",
        "pr_file_module": null
      },
      {
        "comment_id": "360256284",
        "repo_full_name": "apache/mxnet",
        "pr_number": 17129,
        "pr_file": "python/mxnet/gluon/contrib/estimator/estimator.py",
        "discussion_id": "360245337",
        "commented_code": "@@ -358,10 +359,11 @@ def fit(self, train_data,\n         batch_axis : int, default 0\n             Batch axis to split the training data into devices.\n         \"\"\"\n-        if not isinstance(train_data, DataLoader):\n-            raise ValueError(\"Estimator only support input as Gluon DataLoader. Alternatively, you \"\n-                             \"can transform your DataIter or any NDArray into Gluon DataLoader. \"\n-                             \"Refer to gluon.data.dataloader\")\n+        try:\n+            is_iterable = iter(train_data)",
        "comment_created_at": "2019-12-20T07:38:45+00:00",
        "comment_author": "liuzh47",
        "comment_body": "ok, it makes sense to me.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695846029",
    "pr_number": 20505,
    "pr_file": "tests/python/unittest/test_gluon_data.py",
    "created_at": "2021-08-25T15:05:11+00:00",
    "commented_code": "def test_multi_worker_forked_data_loader():\n    data = _Dummy(False)\n    loader = DataLoader(data, batch_size=40, batchify_fn=_batchify, num_workers=2)\n    for epoch in range(1):\n        for i, data in enumerate(loader):\n    for _ in range(1):\n        for _ in enumerate(loader):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "695846029",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20505,
        "pr_file": "tests/python/unittest/test_gluon_data.py",
        "discussion_id": "695846029",
        "commented_code": "@@ -325,14 +325,14 @@ def _batchify(data):\n def test_multi_worker_forked_data_loader():\n     data = _Dummy(False)\n     loader = DataLoader(data, batch_size=40, batchify_fn=_batchify, num_workers=2)\n-    for epoch in range(1):\n-        for i, data in enumerate(loader):\n+    for _ in range(1):\n+        for _ in enumerate(loader):",
        "comment_created_at": "2021-08-25T15:05:11+00:00",
        "comment_author": "szha",
        "comment_body": "```suggestion\r\n        for _ in loader:\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695846617",
    "pr_number": 20505,
    "pr_file": "tests/python/unittest/test_gluon_data.py",
    "created_at": "2021-08-25T15:05:50+00:00",
    "commented_code": "a = mx.gluon.data.SimpleDataset([i for i in range(length)])\n    a_filtered = a.filter(lambda x: x % 10 == 0)\n    assert(len(a_filtered) == 10)\n    for idx, sample in enumerate(a_filtered):\n    for _, sample in enumerate(a_filtered):\n        assert sample % 10 == 0\n    a_xform_filtered = a.transform(lambda x: x + 1).filter(lambda x: x % 10 == 0)\n    assert(len(a_xform_filtered) == 10)\n    # the filtered data is already transformed\n    for idx, sample in enumerate(a_xform_filtered):\n    for _, sample in enumerate(a_xform_filtered):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "695846617",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20505,
        "pr_file": "tests/python/unittest/test_gluon_data.py",
        "discussion_id": "695846617",
        "commented_code": "@@ -382,25 +382,25 @@ def test_dataset_filter():\n     a = mx.gluon.data.SimpleDataset([i for i in range(length)])\n     a_filtered = a.filter(lambda x: x % 10 == 0)\n     assert(len(a_filtered) == 10)\n-    for idx, sample in enumerate(a_filtered):\n+    for _, sample in enumerate(a_filtered):\n         assert sample % 10 == 0\n     a_xform_filtered = a.transform(lambda x: x + 1).filter(lambda x: x % 10 == 0)\n     assert(len(a_xform_filtered) == 10)\n     # the filtered data is already transformed\n-    for idx, sample in enumerate(a_xform_filtered):\n+    for _, sample in enumerate(a_xform_filtered):",
        "comment_created_at": "2021-08-25T15:05:50+00:00",
        "comment_author": "szha",
        "comment_body": "```suggestion\r\n    for sample in a_xform_filtered:\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695847352",
    "pr_number": 20505,
    "pr_file": "tests/python/unittest/test_gluon_data.py",
    "created_at": "2021-08-25T15:06:36+00:00",
    "commented_code": "assert len(shard_3) == 2\n    total = 0\n    for shard in [shard_0, shard_1, shard_2, shard_3]:\n        for idx, sample in enumerate(shard):\n        for _, sample in enumerate(shard):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "695847352",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20505,
        "pr_file": "tests/python/unittest/test_gluon_data.py",
        "discussion_id": "695847352",
        "commented_code": "@@ -417,7 +417,7 @@ def test_dataset_shard():\n     assert len(shard_3) == 2\n     total = 0\n     for shard in [shard_0, shard_1, shard_2, shard_3]:\n-        for idx, sample in enumerate(shard):\n+        for _, sample in enumerate(shard):",
        "comment_created_at": "2021-08-25T15:06:36+00:00",
        "comment_author": "szha",
        "comment_body": "```suggestion\r\n        for sample in shard:\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695847543",
    "pr_number": 20505,
    "pr_file": "tests/python/unittest/test_gluon_data.py",
    "created_at": "2021-08-25T15:06:48+00:00",
    "commented_code": "assert len(shard_3) == 2\n    total = 0\n    for shard in [shard_0, shard_1, shard_2, shard_3]:\n        for idx, sample in enumerate(shard):\n        for _, sample in enumerate(shard):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "695847543",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20505,
        "pr_file": "tests/python/unittest/test_gluon_data.py",
        "discussion_id": "695847543",
        "commented_code": "@@ -435,7 +435,7 @@ def test_dataset_shard_handle():\n     assert len(shard_3) == 2\n     total = 0\n     for shard in [shard_0, shard_1, shard_2, shard_3]:\n-        for idx, sample in enumerate(shard):\n+        for _, sample in enumerate(shard):",
        "comment_created_at": "2021-08-25T15:06:48+00:00",
        "comment_author": "szha",
        "comment_body": "```suggestion\r\n        for sample in shard:\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "695855964",
    "pr_number": 20505,
    "pr_file": "tests/python/unittest/test_numpy_op.py",
    "created_at": "2021-08-25T15:15:41+00:00",
    "commented_code": "dtype=dtype))\n                for optimize in [False, True]:\n                    x = []\n                    for (iop, op) in enumerate(operands):\n                    for (iop, _) in enumerate(operands):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "695855964",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20505,
        "pr_file": "tests/python/unittest/test_numpy_op.py",
        "discussion_id": "695855964",
        "commented_code": "@@ -8396,7 +8396,7 @@ def dbg(name, data):\n                                           dtype=dtype))\n                 for optimize in [False, True]:\n                     x = []\n-                    for (iop, op) in enumerate(operands):\n+                    for (iop, _) in enumerate(operands):",
        "comment_created_at": "2021-08-25T15:15:41+00:00",
        "comment_author": "szha",
        "comment_body": "```suggestion\r\n                    for iop in range(len(operands)):\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
