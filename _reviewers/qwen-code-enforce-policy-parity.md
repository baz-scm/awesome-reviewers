---
title: Enforce Policy Parity
description: 'When changing CI routing/guardrails (workflows, CODEOWNERS, rulesets),
  ensure the *policy intent* is still enforced in the same way.


  **Standard**

  1) **Never replace enforced approvals with “request reviewers”**: reviewer requests
  do not block merges. If your repo relies on `require_code_owner_review: true`, keep
  CODEOWNERS entries (or explicitly update the...'
repository: QwenLM/qwen-code
label: CI/CD
language: Other
comments_count: 4
repository_stars: 26407
---

When changing CI routing/guardrails (workflows, CODEOWNERS, rulesets), ensure the *policy intent* is still enforced in the same way.

**Standard**
1) **Never replace enforced approvals with “request reviewers”**: reviewer requests do not block merges. If your repo relies on `require_code_owner_review: true`, keep CODEOWNERS entries (or explicitly update the ruleset) rather than assuming the workflow will gate merges.
2) **Eliminate config drift**: any canonical routing list (e.g., maintainer allow/skip lists used by scripts) must not be duplicated across script + workflow YAML without a sync check.
3) **Ensure routing logic is tested in CI**: if a test file exists but is not included in the workflow’s test selection list, CI coverage is illusory—add it to the workflow selector.

**Practical implementation**
- Keep one canonical source (e.g., in the script) and add a CI test that validates workflow YAML (and any skip/apply lists) matches that source.
- Also ensure the routing script’s own tests are included in the workflow’s test matrix/selector.

**Example (workflow/YAML config sync test pattern)**
```js
import fs from 'node:fs';
import yaml from 'js-yaml';

// Canonical list lives in one place (e.g., imported from the routing script)
const MAINTAINERS = ['wenshao', 'tanzhenxin', 'yiliang114', 'LaZzyMan'];

const workflow = fs.readFileSync('.github/workflows/ci.yml', 'utf8');
const doc = yaml.load(workflow);

// TODO: locate the step/yaml expression that defines the maintainer skip-list
// and extract it into `skipList` deterministically.
const skipList = /* parse from doc */ [];

if (JSON.stringify(skipList.sort()) !== JSON.stringify([...MAINTAINERS].sort())) {
  throw new Error('CI workflow maintainer skip-list is out of sync with canonical MAINTAINERS');
}
```

**Checklist before merging changes to routing/guardrails**
- Does the repo still *enforce* approval (ruleset/code-owner review) the same way?
- Is there a CI check preventing script↔YAML drift for routing lists?
- Are all routing-related tests actually executed by CI (not just present in the repo)?
