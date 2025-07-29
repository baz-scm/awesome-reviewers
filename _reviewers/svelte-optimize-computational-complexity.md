---
title: optimize computational complexity
description: When implementing algorithms, especially in runtime or performance-critical
  code, prioritize computational efficiency by minimizing redundant operations and
  simplifying mathematical expressions. Look for opportunities to reduce the number
  of multiplications, divisions, and variable assignments.
repository: sveltejs/svelte
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 83580
---

When implementing algorithms, especially in runtime or performance-critical code, prioritize computational efficiency by minimizing redundant operations and simplifying mathematical expressions. Look for opportunities to reduce the number of multiplications, divisions, and variable assignments.

For example, instead of performing multiple redundant calculations:
```js
const scale = {
    x: to.width / node.clientWidth,
    y: to.height / node.clientHeight
};
const dx = ((from.left / scale.x) + (from.width / scale.x) * ox / (to.width / scale.x)) - ((to.left / scale.x) + ox);
```

Simplify to reduce operations:
```js
const dx = ((from.left - to.left) * node.clientWidth + from.width * ox) / to.width - ox;
```

Similarly, consolidate variable declarations and operations:
```js
// Instead of multiple variables and assignments
export function createSlot(slots) {
    const root_slots = {};
    for (const slot_name in slots) {
        let elements = slots[slot_name];
        if (!Array.isArray(elements)) {
            elements = [elements];
        }
        root_slots[slot_name] = [create_root_slot_fn(elements)];
    }
    return root_slots;
}

// Optimize to fewer operations
export function createSlot(input) {
    var key, tmp, slots={};
    for (key in input) {
        tmp = input[key];
        slots[key] = [create_root_slot_fn(Array.isArray(tmp) ? tmp : [tmp])];
    }
    return slots;
}
```

This approach is particularly important in runtime code where efficiency is paramount, as it directly impacts user experience and application performance.