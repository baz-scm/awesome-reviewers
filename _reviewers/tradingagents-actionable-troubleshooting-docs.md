---
title: Actionable Troubleshooting Docs
description: 'Technical documentation—especially troubleshooting guides—must let contributors
  go from symptom to reproducible diagnosis with minimal guesswork.


  Apply these rules:'
repository: TauricResearch/TradingAgents
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 71953
---

Technical documentation—especially troubleshooting guides—must let contributors go from symptom to reproducible diagnosis with minimal guesswork.

Apply these rules:
1. **Be precise about requirements vs local setup**: state the minimum supported versions/constraints separately from “works locally” details.
2. **Anchor steps to the actual workflow/tools**: link directly to the CLI action that saves the evidence (e.g., “Save report?”) and document the default location/structure where outputs are written (e.g., `reports/<ticker>_<timestamp>/`).
3. **Make the workflow traceable**: when you claim a step, explicitly connect it to a failure pattern (“what to inspect first”), so readers can find the earliest wrong stage quickly.

Example structure to follow:
- **Quick triage**
  - Confirm inputs (exact identifiers, date window)
  - “Save report?” via CLI → inspect `reports/<ticker>_<timestamp>/`
- **Investigation**
  - Choose the matching failure pattern from a table
  - For that pattern, list the first concrete checks (tool call args, time windows, exchange-qualified tickers, etc.)

Result: docs become operational (tool/paths-driven), deterministic (pattern → first inspection), and clear about constraints (compatibility vs local environment).