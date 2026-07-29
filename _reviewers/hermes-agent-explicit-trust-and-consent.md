---
title: Explicit Trust and Consent
description: When a security-related skill or script causes any external effect (sending
  data to third parties, spending funds, changing auth, or modifying security config),
  the implementation and docs must be explicit about (a) trust boundaries, (b) user-controlled/bounded
  authorization, and (c) safe, targeted, verifiable changes.
repository: nousresearch/hermes-agent
label: Security
language: Markdown
comments_count: 5
repository_stars: 221948
---

When a security-related skill or script causes any external effect (sending data to third parties, spending funds, changing auth, or modifying security config), the implementation and docs must be explicit about (a) trust boundaries, (b) user-controlled/bounded authorization, and (c) safe, targeted, verifiable changes.

Apply this standard:
- Trust boundary accuracy (data/transform): If raw input is transmitted anywhere before redaction/transformation, do not claim it “protects before reaching an LLM.” Reframe as “hosted transformation” and clearly state what is sent, what is returned, and what is stored.
- Explicit consent for irreversible actions (funds/automation): Never present unattended/agent-executed spending as “autonomous quota management.” If an action can transfer value or has irreversible external impact:
  - require a user approval step,
  - bound it (amount/assets/trigger/expiry),
  - and keep signing/payment guidance user-controlled or outside the skill procedure.
- Safe, targeted security modifications (ops hardening): Prefer directive-specific, reviewable edits and verify before reload/restart.
  - Avoid broad substitutions (e.g., `sed` that rewrites any enabled `* yes` directive).
  - For firewall changes, preserve current SSH access/management rules before enabling default-deny.
- Consistent authentication path: Document and implement exactly one supported auth method for the main flow; ensure references and primary instructions match.

Example patterns (illustrative):

1) Don’t overclaim trust boundary
```md
Wrong: “Redacts PII before it reaches your LLM provider.”
Right: “Hosted transformation: the skill sends input text to TrustBoost for processing, then returns sanitized output.”
```

2) Require bounded user approval before external spend
```text
Before executing a swap: show {wallet, assets, amount, trigger, expiry} and require explicit user confirmation.
Reject or pause if running from a cron/unattended path without an approval token/state.
```

3) Use directive-scoped config edits
```bash
# Instead of rewriting any '* yes' line, edit only the intended directive.
# Then verify with sshd -T or grep before reloading.
sudoedit /etc/ssh/sshd_config
# Verify: sshd -T | grep -E 'passwordauthentication|permitrootlogin'
# Reload only after verification.
```

4) Firewall enable with lockout-safe rule preservation
```text
Before ufw enable: ensure existing SSH allow rule is present (source/port as configured), then enable.
Never enable default-deny without preserving active SSH management access.
```

Outcome: fewer security “false assurances,” fewer accidental lockouts, and no silent/unauthorized irreversible actions.