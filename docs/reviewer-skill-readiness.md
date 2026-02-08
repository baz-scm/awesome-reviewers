# Reviewer Skill Readiness Audit

- Markdown prompts: **4418**
- JSON reviewer datasets: **4308**

## Current quality snapshot

- Prompts with examples: **3121** (70.6%)
- Prompts with bullet lists: **1737** (39.3%)
- Prompts with numbered steps: **1425** (32.3%)
- Prompts with explicit output/response contract keywords: **61** (1.4%)
- Prompts whose first line starts with an imperative verb: **883** (20.0%)
- Median prompt length: **153 words**
- Very short prompts (<80 words): **16**
- Very long prompts (>500 words): **0**

## Why this matters for agent skills

Agent skills work best when prompts include clear trigger conditions, deterministic checklist-style actions, and an expected response format. The current corpus is strong on examples, but weaker on explicit execution contracts (what an agent should output) and standardized structure.

## Recommended improvements

1. **Standardize a skill wrapper section during export**
   - Inject sections like `When to apply`, `Review checklist`, and `Expected output` when converting to SKILL.md.
   - Keep original reviewer text under `Source guidance` to preserve nuance.
2. **Introduce an optional strict mode linter**
   - Fail if prompt lacks imperative guidance, bullets/checklist, or output contract.
3. **Segment by prompt length**
   - Split very long prompts into concise must-follow rules + optional rationale.
4. **Leverage JSON datasets for synthesis**
   - Mine recurring comment patterns and auto-generate candidate checklist statements to backfill weak prompts.
5. **Add confidence metadata**
   - Include metadata like `evidence_count` and `source_repos` in generated skills to help agents prioritize stronger signals.

## JSON dataset signal

- Parsed discussion records: **17175**
- Parsed review comments: **33839**
- Parse failures: **0**
- Top reviewer authors in JSON samples:
  - `coderabbitai[bot]`: 314
  - `ellipsis-dev[bot]`: 221
  - `Copilot`: 220
  - `jasnell`: 198
  - `cubic-dev-ai[bot]`: 178
  - `Darksonn`: 162
  - `spytheman`: 138
  - `vaxerski`: 130
  - `kimwnasptd`: 123
  - `arvinxx`: 120
