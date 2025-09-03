---
title: Provider-based interface design
description: When designing interfaces that handle multiple providers or services,
  organize the API structure around provider-specific logic rather than mixing different
  provider handling in generic components. Use provider-based props structures and
  create dedicated components or methods for each provider type.
repository: lobehub/lobe-chat
label: API
language: TSX
comments_count: 4
repository_stars: 65138
---

When designing interfaces that handle multiple providers or services, organize the API structure around provider-specific logic rather than mixing different provider handling in generic components. Use provider-based props structures and create dedicated components or methods for each provider type.

For props design, structure them by provider with clear typing:
```typescript
// Instead of flat props mixing all providers
interface Props {
  posthogHost?: string;
  posthogToken?: string;
  ga4MeasurementId?: string;
}

// Use provider-based structure
interface Props {
  posthog?: { host: string; token: string } | false;
  ga4?: { measurementId: string } | false;
}
```

For component design, separate provider-specific logic:
```typescript
// Instead of mixing provider logic in generic component
const GenericChecker = ({ provider, model }) => {
  if (provider === 'ollama') {
    // ollama-specific logic
  } else {
    // generic logic
  }
};

// Create dedicated components or methods
const OllamaChecker = ({ model }) => { /* ollama-specific logic */ };
const GenericChecker = ({ model }) => { /* generic logic */ };
```

This approach improves maintainability, reduces conflicts between different provider implementations, and makes the interface more predictable for consumers.