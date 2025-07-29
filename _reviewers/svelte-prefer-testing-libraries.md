---
title: prefer testing libraries
description: When testing components, use established testing libraries like @testing-library/svelte
  instead of low-level DOM manipulation approaches. Low-level testing with direct
  mount/unmount and querySelector calls is brittle and requires frequent updates when
  component structure changes. Testing libraries provide user-focused APIs that are
  more robust to...
repository: sveltejs/svelte
label: Testing
language: Markdown
comments_count: 5
repository_stars: 83580
---

When testing components, use established testing libraries like @testing-library/svelte instead of low-level DOM manipulation approaches. Low-level testing with direct mount/unmount and querySelector calls is brittle and requires frequent updates when component structure changes. Testing libraries provide user-focused APIs that are more robust to implementation changes.

```js
// Avoid: Low-level DOM testing
test('Component', () => {
  const component = mount(Component, {
    target: document.body,
    props: { initial: 0 }
  });
  
  expect(document.body.innerHTML).toBe('<button>0</button>');
  document.body.querySelector('button').click();
  flushSync();
  expect(document.body.innerHTML).toBe('<button>1</button>');
  
  unmount(component);
});

// Prefer: Testing library approach
test('Component', async () => {
  const user = userEvent.setup();
  render(Component, { props: { initial: 0 } });
  
  const button = screen.getByRole('button');
  expect(button).toHaveTextContent('0');
  
  await user.click(button);
  expect(button).toHaveTextContent('1');
});
```

Testing libraries focus on how users interact with your components rather than implementation details, making tests more maintainable and less likely to break when refactoring component structure.