---
title: Doc accuracy and conformance
description: 'Require every documentation change to pass two gates: (1) strict doc-schema
  conformance, and (2) factual/behavioral accuracy against the implementation and
  shipped artifacts.'
repository: nousresearch/hermes-agent
label: Documentation
language: Markdown
comments_count: 18
repository_stars: 221948
---

Require every documentation change to pass two gates: (1) strict doc-schema conformance, and (2) factual/behavioral accuracy against the implementation and shipped artifacts.

**Gate 1: Conformance**
- Follow the required doc template/section structure (e.g., include standard `When to Use` / `Prerequisites` sections).
- Ensure skill frontmatter/metadata and descriptions meet hard limits (e.g., description must be exactly one short sentence per the team’s agent-skill rules).
- Keep platform lists accurate (only claim `windows` if commands/guidance are cross-platform).

**Gate 2: Accuracy & consistency**
- Commands/steps must match what the product actually does (e.g., don’t suggest `hf` if prerequisites still install `huggingface-cli`; don’t present CLI-only commands like `/reload` as gateway/user-session steps).
- Align environment variables, ports, and paths with the shipped behavior (e.g., if the server runs on 8001, link users to 8001 and only mention frontend dashboards when static assets exist).
- Avoid overstating templating/rendering behavior (state only what is actually rendered; if nested keys aren’t rendered, document that limitation).
- Reflect real tool/capability behavior (capabilities in docs must match implementation dispatch and limitations).
- Ensure generated docs reflect the actual source files (if a bundle/source folder is missing, the derived site page must not advertise that installable skill).
- Include required safety/approval steps for user-data writes (don’t document write commands without the explicit confirmation rule).

**Example checklist (apply to every PR):**
1. Does the doc (or skill `SKILL.md`) meet all formatting/limit rules (one-sentence/≤60-char description, required sections, required metadata)?
2. Do all commands match what is installed/configured in the same patch?
3. Are any steps tool-scope-specific (CLI vs gateway) and documented accordingly?
4. Are ports/URLs/paths consistent with the actual runtime and build artifacts?
5. Are templating/rendering claims precise (including nested objects)?
6. Do capability/mode descriptions match the actual implementation behavior?
7. Are install/discovery instructions aligned with where the runtime actually scans?

If any item fails, the doc must be corrected (or the claim narrowed) before merge.