---
title: Vue component test requirement
description: Every Vue component (.vue file) that is created or modified must have
  at least one corresponding unit test file. The test must import the component, mount
  it, and include assertions that validate its behavior.
repository: n8n-io/n8n
label: Testing
language: Other
comments_count: 9
repository_stars: 122978
---

Every Vue component (.vue file) that is created or modified must have at least one corresponding unit test file. The test must import the component, mount it, and include assertions that validate its behavior.

When modifying an existing component, check for an existing test file (e.g., ComponentName.spec.ts or ComponentName.test.ts) in the same directory or in a dedicated __tests__ directory. If a test exists, update it to cover your changes. If no test exists, create one.

Example test structure:
```typescript
import { mount } from '@vue/test-utils';
import ComponentName from './ComponentName.vue';

describe('ComponentName', () => {
  it('renders correctly', () => {
    const wrapper = mount(ComponentName, {
      props: {
        // required props
      }
    });
    
    // Assert component renders correctly
    expect(wrapper.exists()).toBe(true);
    
    // Assert on specific behavior
    expect(wrapper.find('.some-class').exists()).toBe(true);
  });
  
  // Additional tests for component behavior
});
```

This requirement ensures that all Vue components are tested, making the codebase more maintainable and reducing the risk of regressions when components are modified. Tests should verify both rendering and functional aspects of components, particularly focusing on any new or modified features.