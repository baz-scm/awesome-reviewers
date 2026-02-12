---
title: Type-safe focused tests
description: Write tests that are both type-safe and narrowly focused on supported
  behavior. Use small, typed test helpers or fixtures to eliminate repeated casts
  and noisy "as any"/"as T" in tests, and ensure test cases reflect the product's
  validation rules (don’t test unsupported scenarios).
repository: likec4/likec4
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 2582
---

Write tests that are both type-safe and narrowly focused on supported behavior. Use small, typed test helpers or fixtures to eliminate repeated casts and noisy "as any"/"as T" in tests, and ensure test cases reflect the product's validation rules (don’t test unsupported scenarios).

Why: Cleaner, safer tests are easier to read and maintain; helpers reduce boilerplate and prevent hiding type problems with casts. Keeping tests aligned with validation prevents brittle or misleading coverage.

How to apply:
- Add tiny helper functions or fixtures in test files that construct inputs with the correct shapes, so callers don't need to sprinkle type casts.
- Prefer positive tests that exercise only supported/valid cases. If a validation forbids a scenario (e.g., parent-child same-rank), don’t write a positive test that expects it to pass; instead write a negative test asserting the validation behavior.
- Keep test cases minimal — test one behavior per test and use helpers to reduce repetition.

Example helper (from discussion):

```ts
function testFindNodeByElementFqn(
  nodes: Array<{ id: string; data: { modelFqn?: string | null } }>,
  modelFqn: string
) {
  return findNodeByElementFqn(nodes as any, modelFqn as any)
}
```

Use it to remove casts in many tests and keep the test intent clear.

Example simplified rank test (only supported sibling case):

```ts
it('parses element view rank rules for siblings', async ({ expect }) => {
  const { parse, services } = createTestServices()
  const langiumDocument = await parse(`
    specification { element block }
    model {
      block root {
        block childA {}
        block childB {}
      }
    }
    views {
      view index {
        include *
        {rank=same; root childA childB}
      }
    }
  `)
  const doc = services.likec4.ModelParser.parse(langiumDocument)
  const ranks = doc.c4Views[0]!.rules.filter(rule => 'rank' in rule)
  expect(ranks).toHaveLength(1)
})
```

Checklist for PRs/tests:
- Add a helper when you find repeating casts or verbose mock construction.
- Confirm the test encodes supported behavior; if validation rejects a case, write a test asserting rejection instead of a positive success case.
- Keep tests small and readable; helpers should be local to the test file unless reusable across suites.