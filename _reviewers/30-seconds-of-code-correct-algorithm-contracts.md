---
title: Correct Algorithm Contracts
description: 'For algorithm/data-structure snippets, make correctness and the function
  contract explicit: don’t silently break edge cases, validate required input constraints,
  and only mutate inputs when the name/description guarantees it. Also prefer native/built-in
  equivalents when available.'
repository: 30-seconds/30-seconds-of-code
label: Algorithms
language: Markdown
comments_count: 6
repository_stars: 129334
---

For algorithm/data-structure snippets, make correctness and the function contract explicit: don’t silently break edge cases, validate required input constraints, and only mutate inputs when the name/description guarantees it. Also prefer native/built-in equivalents when available.

Apply:
- **Immutability by default**: If the function shouldn’t change the caller’s data, copy first (e.g., `const outputArr = [...inputArr];`) and sort/search in the copy.
- **Validate constraints**: If the algorithm requires certain input shapes (e.g., vector length is even because it’s split in half), check and return an “invalid” result (or throw) when the precondition fails—don’t approximate with truncation.
- **Handle boundary cases**: Verify indexing math for cases like `n=0`, smallest/largest lengths, and off-by-one loops. Add/keep tests for those boundaries.
- **Match the intended API**: Keep the signature/order and semantics consistent with the snippet’s contract.
- **Use built-ins when they exist**: For common behaviors like “first element that passes a predicate,” use `Array.find()` rather than custom duplicates.

Example (non-mutating bubble sort with correct contract):
```js
const bubbleSort = (inputArr) => {
  const outputArr = [...inputArr];
  const len = outputArr.length;

  let swapped;
  do {
    swapped = false;
    for (let i = 0; i < len - 1; i++) {
      if (outputArr[i] > outputArr[i + 1]) {
        const tmp = outputArr[i];
        outputArr[i] = outputArr[i + 1];
        outputArr[i + 1] = tmp;
        swapped = true;
      }
    }
  } while (swapped);

  return outputArr;
};
```

When in doubt, write boundary-focused tests first (e.g., empty array, length 1, `n=0`, invalid preconditions) and only then finalize the implementation.