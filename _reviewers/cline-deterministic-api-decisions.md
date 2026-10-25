---
title: Deterministic API Decisions
description: 'When an app’s behavior depends on an external API, ensure the API call
  is both necessary (authoritative) and deterministic (verifiable). Concretely:


  1) Don’t add “auxiliary” API calls when existing state already determines the outcome
  equivalently'
repository: CLINE/CLINE
label: API
language: TSX
comments_count: 2
repository_stars: 70837
---

When an app’s behavior depends on an external API, ensure the API call is both necessary (authoritative) and deterministic (verifiable). Concretely:

1) Don’t add “auxiliary” API calls when existing state already determines the outcome equivalently
- If the client/provider already decides behavior (e.g., selecting a model family that carries over across local/cloud), avoid extra entitlement/plan lookups that won’t change the decision.

2) Never decide correctness from paginated/partial results
- If an endpoint returns pages and “the first page can’t decide,” design/use a filtered request (e.g., `?query=<exact name>`) so the response can be checked for the specific item.

3) Ensure async persistence writes the latest intended selection
- After an async check (like “does this branch exist?”), persist using the current selection/updater pattern so stale closures don’t overwrite newer user choices.

Example pattern (filtered request + safe persistence):
```ts
const persist = (selection: { branch?: string }) => {
  return CloudServiceClient.setCloudTaskTarget(/* ... */)
}

async function suggestBranchIfExists({ repoId, branchName }: { repoId: number; branchName: string }) {
  // Deterministic: ask the server for the exact branch, not the first page.
  const res = await CloudServiceClient.getRepositoryBranches(
    RepositoryBranchesRequest.create({ repositoryId: repoId, query: branchName })
  )

  const exists = res.branches.includes(branchName)

  // Safe write: base persistence on the current selection, not a captured stale value.
  setSelected((current) =>
    persist({
      ...current,
      branch: exists ? branchName : current.branch,
    })
  )
}
```

Apply this as a standard when touching API-backed state: identify the authoritative source for the decision, use discriminating server queries for correctness, and prevent stale async writes.