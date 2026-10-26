---
title: Decision-Aligned API Queries
description: When your UI/business logic depends on an API-driven decision (eligibility,
  availability, or “should we suggest X?”), ensure the API interaction is **decision-aligned**
  and uses the **correct source of truth**—don’t rely on redundant endpoints, partial
  pagination, or async results applied to stale state.
repository: cline/cline#v14
label: API
language: TSX
comments_count: 2
repository_stars: 70876
---

When your UI/business logic depends on an API-driven decision (eligibility, availability, or “should we suggest X?”), ensure the API interaction is **decision-aligned** and uses the **correct source of truth**—don’t rely on redundant endpoints, partial pagination, or async results applied to stale state.

Apply this as a checklist:
1. **Pick the correct source of truth for the decision boundary.** If the system can decide locally (e.g., provider capability), avoid calling an API that duplicates or contradicts that boundary.
2. **Ask the API the exact question you need.** For “does branch/record X exist?”, call endpoints with a query/filter for X rather than inferring from the first page of a paginated list.
3. **Don’t apply API results to outdated UI state.** When persisting selection after async checks, ensure the write reads the latest selection (e.g., via an updater) or is guarded by a request id.

Example pattern (existence/suggestion via query):
```ts
async function suggestIfExists({ repoId, branchName, listBranches }: {
  repoId: number;
  branchName: string;
  listBranches: (args: { repositoryId: number; query?: string }) => Promise<{ branches: string[] }>;
}) {
  // Decision-aligned: explicitly query for the branch name.
  const result = await listBranches({ repositoryId: repoId, query: branchName });
  const exists = result.branches.includes(branchName);
  return exists ? branchName : undefined;
}
```

Example pattern (avoid redundant endpoint for eligibility):
- If eligibility/behavior is determined by the local provider’s model set, prefer that local truth over making a separate API call solely to restate the same eligibility, especially when the carried model behavior matches the local failure modes.