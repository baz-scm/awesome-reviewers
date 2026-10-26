---
title: Targeted API Decisions
description: When an API call is made to decide what to show/enable or what to persist,
  ensure the API usage is precise, consistent with the correct source of truth, and
  race-safe.
repository: Cline/Cline
label: API
language: TSX
comments_count: 2
repository_stars: 70840
---

When an API call is made to decide what to show/enable or what to persist, ensure the API usage is precise, consistent with the correct source of truth, and race-safe.

**1) Avoid redundant entitlement/plan calls**
- If the client already has a deterministic local source (e.g., a local provider/model registry) that yields the same user-visible behavior and failure mode as the entitlement check, don’t add a server “plan” lookup just to gate the UI.

**2) Use filtered/parameterized API queries for membership decisions**
- Don’t infer “exists/available” from an unfiltered, paginated first page.
- Prefer endpoints that support query-by-identifier (e.g., branch name, repo id) and only suggest/commit when the targeted query confirms the item.

**3) Prevent stale writes after async calls**
- If persistence happens after an async request, use an updater/functional write so the commit uses the latest selection state rather than a captured one.

**Example pattern (branch/target suggestion):**
```ts
const branchRequestId = useRef(0);

async function loadAndSuggestBranch({ repo, workspaceBranch }: {
  repo: { id: number } | undefined;
  workspaceBranch: string | undefined;
}) {
  if (!repo || !workspaceBranch) return undefined;

  const requestId = ++branchRequestId.current;
  // Query precisely by branch name; avoid paginated first-page ambiguity.
  const res = await CloudServiceClient.getRepositoryBranches(
    RepositoryBranchesRequest.create({
      repositoryId: repo.id,
      query: workspaceBranch,
    })
  );

  if (requestId !== branchRequestId.current) return undefined;
  const exists = res.branches.includes(workspaceBranch);
  return exists ? workspaceBranch : undefined;
}

// When persisting after async confirmation, use an updater
// so the saved selection matches the current UI state.
```
