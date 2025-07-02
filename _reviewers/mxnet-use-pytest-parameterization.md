---
title: Use pytest parameterization
description: Structure unit tests using pytest's parameterize decorator instead of
  manual loops or wrapper functions. This approach improves test readability, makes
  failure cases easier to identify, and allows individual test cases to be run separately.
repository: apache/mxnet
label: Testing
language: Python
comments_count: 2
repository_stars: 20801
---

Structure unit tests using pytest's parameterize decorator instead of manual loops or wrapper functions. This approach improves test readability, makes failure cases easier to identify, and allows individual test cases to be run separately.

When implementing tests with multiple inputs or configurations:

1. Replace manual iteration through test cases with `@pytest.mark.parametrize()` decorators
2. Use multiple parametrize decorators when testing combinations of parameters
3. Use pytest's built-in exception testing utilities for cleaner code

Example refactoring:

```python
# Before - manual iteration
def test_operation():
    test_cases = [
        (5, 10, True),
        (3, 7, False),
        (0, 1, True)
    ]
    
    for a, b, expected in test_cases:
        result = operation(a, b)
        assert result == expected

# After - pytest parameterization
@pytest.mark.parametrize('a,b,expected', [
    (5, 10, True),
    (3, 7, False),
    (0, 1, True)
])
def test_operation(a, b, expected):
    result = operation(a, b)
    assert result == expected
```

This approach makes tests more maintainable, documents test cases more clearly, and provides better reporting when tests fail by clearly identifying which specific parameter combination caused the failure.


[
  {
    "discussion_id": "739428844",
    "pr_number": 20692,
    "pr_file": "tests/python/unittest/test_numpy_op.py",
    "created_at": "2021-10-29T17:48:25+00:00",
    "commented_code": "@use_np\ndef test_np_argmin_argmax():\n    workloads = [\n        ((), 0, False),\n        ((), -1, False),\n        ((), 1, True),\n        ((5, 3), None, False),\n        ((5, 3), -1, False),\n        ((5, 3), 1, False),\n        ((5, 3), 3, True),\n        ((5, 0, 3), 0, False),\n        ((5, 0, 3), -1, False),\n        ((5, 0, 3), None, True),\n        ((5, 0, 3), 1, True),\n        ((3, 5, 7), None, False),\n        ((3, 5, 7), 0, False),\n        ((3, 5, 7), 1, False),\n        ((3, 5, 7), 2, False),\n        ((3, 5, 7, 9, 11), -3, False),\n    ]\n    dtypes = ['float16', 'float32', 'float64', 'bool', 'int32']\n    ops = ['argmin', 'argmax']\n\n@pytest.mark.parametrize('shape,axis,throw_exception', [\n    ((), 0, False),\n    ((), -1, False),\n    ((), 1, True),\n    ((5, 3), None, False),\n    ((5, 3), -1, False),\n    ((5, 3), 1, False),\n    ((5, 3), 3, True),\n    ((5, 0, 3), 0, False),\n    ((5, 0, 3), -1, False),\n    ((5, 0, 3), None, True),\n    ((5, 0, 3), 1, True),\n    ((3, 5, 7), None, False),\n    ((3, 5, 7), 0, False),\n    ((3, 5, 7), 1, False),\n    ((3, 5, 7), 2, False),\n    ((3, 5, 7, 9, 11), -3, False),\n])\n@pytest.mark.parametrize('dtype', ['float16', 'float32', 'float64', 'bool', 'int32'])\n@pytest.mark.parametrize('op_name', ['argmin', 'argmax'])\n@pytest.mark.parametrize('keepdims', [True, False])\ndef test_np_argmin_argmax(shape, axis, throw_exception, dtype, op_name, keepdims):\n    class TestArgExtreme(HybridBlock):\n        def __init__(self, op_name, axis=None):\n        def __init__(self, op_name, axis=None, keepdims=False):\n            super(TestArgExtreme, self).__init__()\n            self._op_name = op_name\n            self._axis = axis\n            self.keepdims = keepdims\n\n        def forward(self, x):\n            return getattr(x, self._op_name)(self._axis)\n\n    for op_name in ops:\n        for shape, axis, throw_exception in workloads:\n            for dtype in dtypes:\n                a = np.random.uniform(low=0, high=100, size=shape).astype(dtype)\n                if throw_exception:\n                    # Cannot use assert_exception because sometimes the main thread\n                    # proceeds to `assert False` before the exception is thrown\n                    # in the worker thread. Have to use mx.nd.waitall() here\n                    # to block the main thread.\n                    try:\n                        getattr(np, op_name)(a, axis)\n                        mx.nd.waitall()\n                        assert False\n                    except mx.MXNetError:\n                        pass\n                else:\n                    mx_ret = getattr(np, op_name)(a, axis=axis)\n                    np_ret = getattr(onp, op_name)(a.asnumpy(), axis=axis)\n                    assert mx_ret.dtype == np_ret.dtype\n                    assert same(mx_ret.asnumpy(), np_ret)\n            return getattr(x, self._op_name)(self._axis, keepdims=self.keepdims)\n\n    a = np.random.uniform(low=0, high=100, size=shape).astype(dtype)\n    if throw_exception:\n        # Cannot use assert_exception because sometimes the main thread\n        # proceeds to `assert False` before the exception is thrown\n        # in the worker thread. Have to use mx.nd.waitall() here\n        # to block the main thread.\n        try:\n            getattr(np, op_name)(a, axis)\n            mx.nd.waitall()\n            assert False\n        except mx.MXNetError:\n            pass",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "739428844",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20692,
        "pr_file": "tests/python/unittest/test_numpy_op.py",
        "discussion_id": "739428844",
        "commented_code": "@@ -4437,73 +4437,84 @@ def GetDimSize(shp, axis):\n \n \n @use_np\n-def test_np_argmin_argmax():\n-    workloads = [\n-        ((), 0, False),\n-        ((), -1, False),\n-        ((), 1, True),\n-        ((5, 3), None, False),\n-        ((5, 3), -1, False),\n-        ((5, 3), 1, False),\n-        ((5, 3), 3, True),\n-        ((5, 0, 3), 0, False),\n-        ((5, 0, 3), -1, False),\n-        ((5, 0, 3), None, True),\n-        ((5, 0, 3), 1, True),\n-        ((3, 5, 7), None, False),\n-        ((3, 5, 7), 0, False),\n-        ((3, 5, 7), 1, False),\n-        ((3, 5, 7), 2, False),\n-        ((3, 5, 7, 9, 11), -3, False),\n-    ]\n-    dtypes = ['float16', 'float32', 'float64', 'bool', 'int32']\n-    ops = ['argmin', 'argmax']\n-\n+@pytest.mark.parametrize('shape,axis,throw_exception', [\n+    ((), 0, False),\n+    ((), -1, False),\n+    ((), 1, True),\n+    ((5, 3), None, False),\n+    ((5, 3), -1, False),\n+    ((5, 3), 1, False),\n+    ((5, 3), 3, True),\n+    ((5, 0, 3), 0, False),\n+    ((5, 0, 3), -1, False),\n+    ((5, 0, 3), None, True),\n+    ((5, 0, 3), 1, True),\n+    ((3, 5, 7), None, False),\n+    ((3, 5, 7), 0, False),\n+    ((3, 5, 7), 1, False),\n+    ((3, 5, 7), 2, False),\n+    ((3, 5, 7, 9, 11), -3, False),\n+])\n+@pytest.mark.parametrize('dtype', ['float16', 'float32', 'float64', 'bool', 'int32'])\n+@pytest.mark.parametrize('op_name', ['argmin', 'argmax'])\n+@pytest.mark.parametrize('keepdims', [True, False])\n+def test_np_argmin_argmax(shape, axis, throw_exception, dtype, op_name, keepdims):\n     class TestArgExtreme(HybridBlock):\n-        def __init__(self, op_name, axis=None):\n+        def __init__(self, op_name, axis=None, keepdims=False):\n             super(TestArgExtreme, self).__init__()\n             self._op_name = op_name\n             self._axis = axis\n+            self.keepdims = keepdims\n \n         def forward(self, x):\n-            return getattr(x, self._op_name)(self._axis)\n-\n-    for op_name in ops:\n-        for shape, axis, throw_exception in workloads:\n-            for dtype in dtypes:\n-                a = np.random.uniform(low=0, high=100, size=shape).astype(dtype)\n-                if throw_exception:\n-                    # Cannot use assert_exception because sometimes the main thread\n-                    # proceeds to `assert False` before the exception is thrown\n-                    # in the worker thread. Have to use mx.nd.waitall() here\n-                    # to block the main thread.\n-                    try:\n-                        getattr(np, op_name)(a, axis)\n-                        mx.nd.waitall()\n-                        assert False\n-                    except mx.MXNetError:\n-                        pass\n-                else:\n-                    mx_ret = getattr(np, op_name)(a, axis=axis)\n-                    np_ret = getattr(onp, op_name)(a.asnumpy(), axis=axis)\n-                    assert mx_ret.dtype == np_ret.dtype\n-                    assert same(mx_ret.asnumpy(), np_ret)\n+            return getattr(x, self._op_name)(self._axis, keepdims=self.keepdims)\n+\n+    a = np.random.uniform(low=0, high=100, size=shape).astype(dtype)\n+    if throw_exception:\n+        # Cannot use assert_exception because sometimes the main thread\n+        # proceeds to `assert False` before the exception is thrown\n+        # in the worker thread. Have to use mx.nd.waitall() here\n+        # to block the main thread.\n+        try:\n+            getattr(np, op_name)(a, axis)\n+            mx.nd.waitall()\n+            assert False\n+        except mx.MXNetError:\n+            pass",
        "comment_created_at": "2021-10-29T17:48:25+00:00",
        "comment_author": "szha",
        "comment_body": "This can be simplified https://docs.pytest.org/en/6.2.x/assert.html#assertions-about-expected-exceptions",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "610247827",
    "pr_number": 20105,
    "pr_file": "tests/python/unittest/test_numpy_gluon.py",
    "created_at": "2021-04-09T00:58:33+00:00",
    "commented_code": "[64, 88, 65, 89, 66, 90, 67, 91],\n            [68, 92, 69, 93, 70, 94, 71, 95]]]]]\n    )\n\n@use_np\ndef test_embedding():\n    def check_embedding():\n        layer = gluon.nn.Embedding(10, 100)\n        layer.initialize()\n        x = mx.np.array([3,4,2,0,1])\n        with mx.autograd.record():\n            y = layer(x)\n            y.backward()\n        assert (layer.weight.grad().asnumpy()[:5] == 1).all()\n        assert (layer.weight.grad().asnumpy()[5:] == 0).all()\n\n    def check_embedding_large_input():\n        embedding = mx.gluon.nn.Embedding(10, 1)\n        embedding.initialize()\n        embedding.hybridize()\n        shape = (20481,)\n        with mx.autograd.record():\n            emb_in = embedding(mx.np.ones(shape))\n            loss = emb_in.sum()\n        loss.backward()\n        assert embedding.weight.grad().sum().item() == 20481\n\n    check_embedding()\n    check_embedding_large_input()\n\n@use_np\ndef test_layernorm():\n    layer = nn.LayerNorm(in_channels=10)\n    check_layer_forward(layer, (2, 10, 10, 10))\n\ndef check_layer_forward(layer, dshape):",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "610247827",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20105,
        "pr_file": "tests/python/unittest/test_numpy_gluon.py",
        "discussion_id": "610247827",
        "commented_code": "@@ -602,3 +602,57 @@ def test_pixelshuffle3d():\n             [64, 88, 65, 89, 66, 90, 67, 91],\n             [68, 92, 69, 93, 70, 94, 71, 95]]]]]\n     )\n+\n+@use_np\n+def test_embedding():\n+    def check_embedding():\n+        layer = gluon.nn.Embedding(10, 100)\n+        layer.initialize()\n+        x = mx.np.array([3,4,2,0,1])\n+        with mx.autograd.record():\n+            y = layer(x)\n+            y.backward()\n+        assert (layer.weight.grad().asnumpy()[:5] == 1).all()\n+        assert (layer.weight.grad().asnumpy()[5:] == 0).all()\n+\n+    def check_embedding_large_input():\n+        embedding = mx.gluon.nn.Embedding(10, 1)\n+        embedding.initialize()\n+        embedding.hybridize()\n+        shape = (20481,)\n+        with mx.autograd.record():\n+            emb_in = embedding(mx.np.ones(shape))\n+            loss = emb_in.sum()\n+        loss.backward()\n+        assert embedding.weight.grad().sum().item() == 20481\n+\n+    check_embedding()\n+    check_embedding_large_input()\n+\n+@use_np\n+def test_layernorm():\n+    layer = nn.LayerNorm(in_channels=10)\n+    check_layer_forward(layer, (2, 10, 10, 10))\n+\n+def check_layer_forward(layer, dshape):",
        "comment_created_at": "2021-04-09T00:58:33+00:00",
        "comment_author": "szha",
        "comment_body": "you can use `@pytest.mark.parametrize('arg1,arg2', [(arg1_val, arg2_val)])` to parameterize the test instead of having a wrapper test function.",
        "pr_file_module": null
      }
    ]
  }
]
