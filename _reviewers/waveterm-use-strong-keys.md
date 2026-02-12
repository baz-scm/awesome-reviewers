---
title: use strong keys
description: Always use secure cryptographic algorithms and minimum key sizes—even
  for dummy, test, or helper keys. Avoid generating or shipping 1024-bit RSA keys
  (they are considered weak). Prefer modern algorithms (ed25519) when supported; otherwise
  use at least 2048-bit RSA. Mark any ephemeral/dummy keys clearly in code, avoid
  persisting them, and follow library...
repository: wavetermdev/waveterm
label: Security
language: Go
comments_count: 1
repository_stars: 17328
---

Always use secure cryptographic algorithms and minimum key sizes—even for dummy, test, or helper keys. Avoid generating or shipping 1024-bit RSA keys (they are considered weak). Prefer modern algorithms (ed25519) when supported; otherwise use at least 2048-bit RSA. Mark any ephemeral/dummy keys clearly in code, avoid persisting them, and follow library defaults where possible.

How to apply:
- Prefer ed25519 for SSH signers when the library supports it (smaller, faster, and stronger):
  pub, priv, _ := ed25519.GenerateKey(rand.Reader)
  signer, _ := ssh.NewSignerFromKey(priv)
- If RSA is required, use >=2048 bits (2048 is minimum; 3072+ for higher security):
  // bad: rsa.GenerateKey(rand.Reader, 1024)
  // good:
  key, err := rsa.GenerateKey(rand.Reader, 2048)
  signer, err := ssh.NewSignerFromKey(key)

Additional guidance:
- Do not hard-code weak sizes; use named constants (e.g., RSA2048 = 2048) so they can be audited and updated.
- Keep dummy keys ephemeral (in-memory only) and document why they exist to avoid accidental reuse.
- Prefer library-supplied secure defaults and review cryptographic code during security reviews.

Motivation: Weak keys reduce the security of authentication and can introduce vulnerabilities even in helper code. Using strong defaults prevents accidental weakening of systems and aligns code with current security best practices.