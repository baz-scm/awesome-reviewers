---
title: Service contract clarity
description: Prefer explicit, responsibility-aligned service APIs with well-defined
  contracts for (a) what callers should expect synchronously/async, (b) how caching
  vs live validation behaves, and (c) how events supersede in-flight work.
repository: microsoft/VSCode
label: API
language: TypeScript
comments_count: 5
repository_stars: 194303
---

Prefer explicit, responsibility-aligned service APIs with well-defined contracts for (a) what callers should expect synchronously/async, (b) how caching vs live validation behaves, and (c) how events supersede in-flight work.

Concretely:
- Keep services narrowly scoped: e.g., an “account/access” service returns an access verdict (and maybe identity context) but does not also fetch/materialize unrelated data (like the manifest). Let the manifest service fetch/publish.
- Make result semantics unambiguous: define explicit states (e.g., SignInRequired/Denied/Available/Misconfigured/Unreachable) instead of overloading `undefined` with multiple meanings.
- Specify whether a method can hit the network and whether it may return cached data first, then re-validate and publish changes via events.
- Ensure in-flight results can’t corrupt newer cache: use supersession/reset logic and document it in the API contract.

Example shape (access-verdict contract):
```ts
type AccessVerdict =
  | { kind: 'SignInRequired' }
  | { kind: 'Denied' }
  | { kind: 'Available'; manifest: IExtensionGalleryManifest } // only if this service owns fetching
  | { kind: 'Misconfigured' }
  | { kind: 'Unreachable' };

interface IMarketplaceAccessService {
  // Returns a verdict based on durable cache + (optionally) live validation.
  // If live validation is deferred, publish updates via onDidChangeAccess.
  resolveAccess(serviceUrl: string): Promise<AccessVerdict>;

  // Fires when a later validation supersedes the earlier verdict.
  onDidChangeAccess: Event<AccessVerdict>;

  // Clears cached verdicts + memoized indices so late results can’t repopulate.
  reset(): void;
}
```

Applying this consistently reduces ambiguity for consumers, prevents stale-cache races, and keeps API ownership and security boundaries clear.