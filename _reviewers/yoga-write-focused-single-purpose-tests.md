---
title: Write focused single-purpose tests
description: Tests should focus on validating one specific behavior or scenario rather
  than combining multiple test cases into complex, multi-purpose tests. Each test
  should have a clear, meaningful purpose that actually exercises the code under test.
repository: facebook/yoga
label: Testing
language: Html
comments_count: 2
repository_stars: 18255
---

Tests should focus on validating one specific behavior or scenario rather than combining multiple test cases into complex, multi-purpose tests. Each test should have a clear, meaningful purpose that actually exercises the code under test.

Avoid creating tests that are too complex or that test trivial scenarios where the expected behavior is obvious. When tests fail, focused tests make it much easier to identify and debug the specific issue.

For example, instead of creating one large test case that validates multiple alignment behaviors:

```html
<!-- Avoid: Complex test testing multiple things -->
<div id="complex_alignment_test" style="width: 150px; height: 100px; flex-wrap: wrap; flex-direction: row; align-content: stretch; justify-content: space-between;">
  <div style="width: 50px; height: 10px;"></div>
  <div style="width: 50px; height: 10px;"></div>
  <div style="width: 50px; height: 10px;"></div>
</div>
```

Create separate, focused tests:

```html
<!-- Prefer: Focused test for align-content stretch -->
<div id="align_content_stretch_test" style="width: 130px; height: 100px; flex-wrap: wrap; align-content: stretch;">
  <div style="width: 50px; height: 10px;"></div>
  <div style="width: 50px; height: 10px;"></div>
</div>

<!-- Separate test for justify-content space-between -->
<div id="justify_content_space_between_test" style="width: 130px; height: 100px; justify-content: space-between;">
  <div style="width: 50px; height: 10px;"></div>
  <div style="width: 50px; height: 10px;"></div>
</div>
```

Additionally, ensure tests actually validate meaningful scenarios. Avoid creating tests where the expected behavior is trivial or where there's no actual space to distribute or meaningful layout differences to observe.