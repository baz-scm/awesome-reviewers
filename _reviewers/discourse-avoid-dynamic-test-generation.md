---
title: avoid dynamic test generation
description: Avoid using loops (forEach, for, etc.) to dynamically generate tests
  from arrays or objects, as this pattern makes debugging significantly harder. When
  a test fails, it's difficult to set breakpoints on specific cases or identify which
  iteration caused the failure.
repository: discourse/discourse
label: Testing
language: Other
comments_count: 2
repository_stars: 44898
---

Avoid using loops (forEach, for, etc.) to dynamically generate tests from arrays or objects, as this pattern makes debugging significantly harder. When a test fails, it's difficult to set breakpoints on specific cases or identify which iteration caused the failure.

Instead, use one of these approaches:

**Option 1: Individual tests for each case**
```javascript
test("autocompletes black text", async function (assert) {
  await testHexCode(assert, "000", "000000");
});

test("autocompletes white text", async function (assert) {
  await testHexCode(assert, "fff", "ffffff");
});
```

**Option 2: Single test with multiple assertions**
```javascript
test("autocompletes hex codes", async function (assert) {
  let result;
  const autocompleteHex = (color) => (result = color.replace("#", ""));

  await render(
    <template><ColorInput @onChangeColor={{autocompleteHex}} /></template>
  );

  await fillIn(".hex-input", "000");
  assert.strictEqual(result, "000000", "black text");
  
  await fillIn(".hex-input", "fff");
  assert.strictEqual(result, "ffffff", "white text");
  
  await fillIn(".hex-input", "f2f");
  assert.strictEqual(result, "f2f2f2", "2 digit sequence");
}
```

Both approaches allow developers to easily debug specific test cases, set targeted breakpoints, and understand test failures more quickly. Choose individual tests when cases are complex or unrelated, and single tests with multiple assertions when testing variations of the same behavior.