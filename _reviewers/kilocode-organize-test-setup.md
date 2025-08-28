---
title: organize test setup
description: Reduce test code duplication by organizing common setup logic and grouping
  related tests appropriately. Move repeated setup code into beforeEach hooks and
  use describe blocks to group tests that share similar setup or test the same feature
  area.
repository: kilo-org/kilocode
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 7302
---

Reduce test code duplication by organizing common setup logic and grouping related tests appropriately. Move repeated setup code into beforeEach hooks and use describe blocks to group tests that share similar setup or test the same feature area.

When tests have repeated setup code, extract it to beforeEach to improve maintainability. For feature-specific tests, group them in dedicated describe blocks with their own setup:

```javascript
describe("AutocompleteProvider whitespace handling", () => {
    let mockContext: any
    let mockProvider: any
    let provideInlineCompletionItems: any

    beforeEach(() => {
        vi.clearAllMocks()
        
        mockContext = {
            subscriptions: [],
        }
        
        // Common setup for all whitespace tests
        vi.mocked(ContextProxy.instance.getGlobalState).mockReturnValue({
            autocomplete: true,
        })
    })

    // Individual tests here...
})
```

For test utilities that need global access, provide clear documentation explaining their purpose and scope, especially when exposing APIs for testing convenience.