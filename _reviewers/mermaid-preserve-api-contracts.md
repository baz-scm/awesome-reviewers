---
title: Preserve API Contracts
description: When an endpoint or syntax is already used as a contract (e.g., chart
  grammar shared across features, or a stateful editor URL), avoid creating parallel
  interfaces or polluting the contract with unrelated concerns.
repository: mermaid-js/mermaid
label: API
language: Other
comments_count: 2
repository_stars: 87952
---

When an endpoint or syntax is already used as a contract (e.g., chart grammar shared across features, or a stateful editor URL), avoid creating parallel interfaces or polluting the contract with unrelated concerns.

Apply this as:
- Prefer extending an existing syntax/API instead of adding a separate, parallel one (reduces duplication and client/parser divergence).
- If a URL encodes application state, keep the URL’s state-related parameters clean; don’t add marketing/tracking query params to the same URL the app uses to store/load state.

Example (clean stateful editor URL):
```ts
// Bad: pollutes a stateful URL used by the editor
const liveUrl =
  'https://mermaid.live/edit?utm_source=mermaid_js&utm_medium=editor_selection&utm_campaign=open_source';

// Good: keep only the contract URL; send analytics separately
const liveUrl = 'https://mermaid.live/edit';
```