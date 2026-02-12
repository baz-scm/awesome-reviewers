---
title: Config precedence
description: 'Establish a clear configuration precedence and control policy: explicit
  user-supplied settings take priority over automatic detection, unless a centralized
  policy (e.g., cloud/service-side limits or security constraints) explicitly disallows
  client overrides. Motivation: prevents surprising behavior while allowing deliberate
  overrides and enforcing...'
repository: wavetermdev/waveterm
label: Configurations
language: Go
comments_count: 2
repository_stars: 17328
---

Establish a clear configuration precedence and control policy: explicit user-supplied settings take priority over automatic detection, unless a centralized policy (e.g., cloud/service-side limits or security constraints) explicitly disallows client overrides. Motivation: prevents surprising behavior while allowing deliberate overrides and enforcing safety/consistency where needed.

How to apply:
- Rule order: 1) explicit per-request or per-call arguments (when present) 2) persisted configuration (env vars/config files/feature flags) 3) automatic detection/fallbacks.
- Exception: for managed/cloud/back-end operations, enforce server-side defaults for sensitive or quota-related parameters and ignore client attempts to override them.

Examples:
- Respect explicit kwarg, otherwise detect:
  if _, ok := pk.Kwargs[KwArgSudo]; ok {
      runPacket.IsSudo = sudoArg // explicit override
  } else {
      runPacket.IsSudo = IsSudoCommand(cmdStr) // fallback detection
  }

- Enforce cloud defaults server-side (ignore client-specified tokens/choices):
  // do not trust opts.MaxTokens for cloud; set fixed values before sending
  cloudReq.MaxTokens = cloudDefaultMaxTokens
  cloudReq.MaxChoices = cloudDefaultMaxChoices

Documentation: record the precedence rules in the project config guide and call out contexts where server-side policies override client inputs. When changing behavior, log or document when a client-supplied value was ignored so callers can diagnose differences.