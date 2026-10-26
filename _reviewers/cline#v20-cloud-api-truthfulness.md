---
title: Cloud API Truthfulness
description: When cloud UI/API flows make capability or eligibility decisions, ensure
  you’re using the correct source of truth and that async API results are applied
  to the latest state.
repository: cline/cline#v20
label: API
language: TSX
comments_count: 2
repository_stars: 70886
---

When cloud UI/API flows make capability or eligibility decisions, ensure you’re using the correct source of truth and that async API results are applied to the latest state.

Apply these rules:
1) Don’t depend on “plan/capability” endpoints when another system is the authority.
   - If the desktop/local provider already determines what’s available (e.g., carried `cline-pass/*` models), avoid re-checking via `/api/v1/users/me/plan`.
2) Make API calls that can deterministically answer the question.
   - If a list is paginated, don’t infer eligibility from the first page. Prefer targeted queries (e.g., “get branch by name” / search-with-query) so you can reliably decide.
3) Persist async outcomes against current state.
   - After an `await`, don’t write using values captured before the async call; use a state updater pattern so the write uses the latest selection.
4) Prevent out-of-order responses from overwriting newer user intent.

Example pattern (targeted query + latest-state persist):

```ts
const requestIdRef = useRef(0);

const persistSelection = useCallback((updater: (prev: Selection) => Selection) => {
  // write using latest selection
  setSelection((prev) => updater(prev));
}, []);

async function suggestBranch(selectedRepo: Repo | undefined, workspaceBranch: string) {
  if (!selectedRepo) return;

  const requestId = ++requestIdRef.current;
  const result = await CloudServiceClient.getRepositoryBranches(
    RepositoryBranchesRequest.create({
      repositoryId: selectedRepo.id,
      query: workspaceBranch, // targeted by name
    }),
  );

  if (requestId !== requestIdRef.current) return; // ignore stale response

  const canUse = result.branches.includes(workspaceBranch);
  persistSelection((prev) => ({
    ...prev,
    branch: canUse ? workspaceBranch : prev.branch,
  }));
}
```

This prevents incorrect gating (wrong source of truth), unreliable eligibility checks (pagination assumptions), and stale-state persistence after async cloud calls.