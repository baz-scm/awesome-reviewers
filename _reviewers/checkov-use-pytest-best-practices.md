---
title: Use pytest best practices
description: 'Adopt modern pytest features to create maintainable, isolated, and comprehensive
  tests. This includes:


  1. **Prefer pytest over unittest** for new test development to leverage pytest''s
  rich feature set and simpler syntax.'
repository: bridgecrewio/checkov
label: Testing
language: Python
comments_count: 4
repository_stars: 7668
---

Adopt modern pytest features to create maintainable, isolated, and comprehensive tests. This includes:

1. **Prefer pytest over unittest** for new test development to leverage pytest's rich feature set and simpler syntax.

2. **Use parameterization** for testing multiple scenarios instead of duplicating test code:
```python
# Instead of manual iteration over test cases:
for graph_framework in ["NETWORKX", "RUSTWORKX"]:
    # test code with graph_framework...

# Use pytest's parameterization:
@pytest.mark.parametrize("graph_framework", ["NETWORKX", "RUSTWORKX"])
def test_connected_node_with_framework(graph_framework):
    # test code with graph_framework...
```

3. **Maintain test isolation** by using fixtures like `monkeypatch` to modify environment variables or dependencies for a single test:
```python
# Instead of modifying environment directly:
def test_get_folder_definitions_do_not_ignore_hidden(self):
    os.environ["CKV_IGNORE_HIDDEN_DIRECTORIES"] = "False"
    # test code...

# Use monkeypatch for isolated modifications:
def test_get_folder_definitions_do_not_ignore_hidden(monkeypatch):
    monkeypatch.setenv("CKV_IGNORE_HIDDEN_DIRECTORIES", "False")
    # test code...
```

4. **Write comprehensive assertions** that validate specific properties, not just existence or counts, to ensure complete verification of expected behavior.

Following these practices will result in tests that are easier to maintain, less prone to side effects, and provide clearer failure information.