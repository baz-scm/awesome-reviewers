---
title: Thorough test assertions
description: 'Ensure tests thoroughly validate functionality through comprehensive
  assertions. When writing tests:


  1. Assert all relevant aspects of the expected behavior, not just presence/absence
  or simple success/failure'
repository: bridgecrewio/checkov
label: Testing
language: Python
comments_count: 5
repository_stars: 7667
---

Ensure tests thoroughly validate functionality through comprehensive assertions. When writing tests:

1. Assert all relevant aspects of the expected behavior, not just presence/absence or simple success/failure
2. Verify specific resource properties, not just counts or general outcomes
3. Test critical logic with dedicated unit tests, especially for complex or core functionality
4. Include both normal and edge cases in your test suite

**Example:**
```python
# Incomplete test - only checks summary counts
def test_resource_skips_incomplete():
    report = Runner().run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[]))
    summary = report.get_summary()
    self.assertEqual(summary["skipped"], 3)  # ❌ Missing specific assertions

# Better test - verifies specific resources and their properties
def test_resource_skips_thorough():
    report = Runner().run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[]))
    
    # Assert overall summary
    summary = report.get_summary()
    self.assertEqual(summary["skipped"], 3)
    
    # Assert specific resources and their skip counts
    skipped_resources = report.get_skipped_resources()
    self.assertEqual(len(skipped_resources["default"]), 1)
    self.assertEqual(len(skipped_resources["skip_invalid"]), 1)
    self.assertEqual(len(skipped_resources["skip_more_than_one"]), 2)  # ✅ Thorough validation
```

When implementing new functionality, always add corresponding tests that validate the specific behavior, not just general outcomes. For critical logic, create dedicated unit tests even if the component is tested indirectly elsewhere.