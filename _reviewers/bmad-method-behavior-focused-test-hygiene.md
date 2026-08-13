---
title: Behavior-Focused Test Hygiene
description: 'Write tests that are (1) behavior-focused rather than implementation-coupled,
  and (2) use safe, consistently cleaned fixtures.


  Do

  - Assert externally observable outcomes/invariants, not “incidental” implementation
  details. If changing internals wouldn’t break the contract, don’t make the test
  fail on that internal change.'
repository: bmad-code-org/bmad-method
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 51859
---

Write tests that are (1) behavior-focused rather than implementation-coupled, and (2) use safe, consistently cleaned fixtures.

Do
- Assert externally observable outcomes/invariants, not “incidental” implementation details. If changing internals wouldn’t break the contract, don’t make the test fail on that internal change.
  - Example pattern (marker-stripping):
    ```js
    const cleaned = await fs.readFile(instructionsPath, 'utf8');
    assert(!cleaned.includes('BMAD:START') && !cleaned.includes('BMAD generated content'), 'markers removed');
    assert(cleaned.includes('User content before') && cleaned.includes('User content after'), 'user content preserved');
    ```
- Use `fs.mkdtemp()` (or equivalent) for temp directories and ensure you clean up the full parent directory you created.
  - Return all necessary paths from fixtures so teardown can delete what was actually created.
    ```js
    async function createXFixture() {
      const root = await fs.mkdtemp(path.join(os.tmpdir(), 'my-suite-'));
      const dir = path.join(root, '_subdir');
      await fs.ensureDir(dir);
      return { root, dir };
    }

    // teardown
    await fs.rm(fixture.root, { recursive: true, force: true });
    ```

Don’t
- Avoid asserting on low-value details like exact HTTP header literals when the test’s purpose is cascade/behavior logic.
- Avoid exact whole-string comparisons when simpler invariant checks provide equivalent coverage; exact matches often introduce brittleness with negligible benefit.

Result: tests remain stable under refactors, and temp resources don’t leak or create flaky behavior across suites.