---
title: organize import groups
description: Imports should be organized into distinct groups with proper spacing
  for better readability. Group all third-party library imports together in one contiguous
  block, followed by a blank line, then group all local/relative imports in another
  block. This separation makes it immediately clear which dependencies are external
  versus internal to the project.
repository: emcie-co/parlant
label: Code Style
language: TSX
comments_count: 2
repository_stars: 12205
---

Imports should be organized into distinct groups with proper spacing for better readability. Group all third-party library imports together in one contiguous block, followed by a blank line, then group all local/relative imports in another block. This separation makes it immediately clear which dependencies are external versus internal to the project.

Example of proper import organization:

```typescript
// Third-party imports (grouped together)
import { describe, expect, it, Mock, vi } from 'vitest';
import { cleanup, fireEvent, render } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// Blank line separator

// Local imports (grouped together)
import AgentsList from './agents-list';
import { NEW_SESSION_ID } from '../chat-header/chat-header';
```

This organization pattern helps developers quickly understand the external dependencies versus internal module relationships, making the code more "polite" to readers and easier to maintain.