---
title: Normalize Before Compare
description: When implementing validation, duplicate detection, or search over structured
  inputs, first canonicalize (normalize) the representations and make comparisons
  match the domain semantics (case-insensitive, order-insensitive, whitespace-tolerant,
  etc.). Never compare raw strings/fields directly when the same meaning can be represented
  in multiple equivalent...
repository: Azure/azure-cli
label: Algorithms
language: Python
comments_count: 4
repository_stars: 4592
---

When implementing validation, duplicate detection, or search over structured inputs, first canonicalize (normalize) the representations and make comparisons match the domain semantics (case-insensitive, order-insensitive, whitespace-tolerant, etc.). Never compare raw strings/fields directly when the same meaning can be represented in multiple equivalent forms.

Apply this pattern:
1) **Normalize inputs** into a canonical form (e.g., lowercased names, frozenset for unordered collections, trimmed CIDRs, dict-vs-list unified structure).
2) **Detect structure variants** before deriving results (e.g., single manifest vs manifest list; choose the correct layer/digest derivation path).
3) **Use tolerant parsing** for algorithmic extraction (e.g., regex that accepts whitespace variations) and ensure search-string/tokenization is constructed deterministically.

Example (duplicate detection by canonicalizing unordered CIDRs + header filters):
```python
def normalize_ip_list(ip_address: str | None):
    if not ip_address:
        return frozenset()
    return frozenset(part.strip() for part in ip_address.split(',') if part.strip())

def normalize_headers(headers):
    # Supports both CLI list form and SDK/dict form.
    if not headers:
        return {}
    if isinstance(headers, dict):
        out = {}
        for k, vals in headers.items():
            name = (k or '').strip().lower()
            if not name or not vals:
                continue
            if isinstance(vals, str):
                vals = [vals]
            vset = frozenset(v for v in vals if v)
            if vset:
                out[name] = vset
        return out
    out = {}
    for s in headers:  # list of "name=value"
        if not s or '=' not in s:
            continue
        n, _, v = s.partition('=')
        n = n.strip().lower(); v = v.strip()
        if n and v:
            out.setdefault(n, frozenset())
            out[n] = out[n] | frozenset([v])
    return out

new_ip = normalize_ip_list(namespace.ip_address)
new_headers = normalize_headers(getattr(namespace, 'http_headers', None))
for rule in access_rules or []:
    if normalize_ip_list(rule.ip_address) == new_ip and normalize_headers(rule.headers) == new_headers:
        raise ArgumentUsageError("duplicate rule")
```

If you can’t normalize safely, branch based on detected structure (e.g., handle manifest lists before selecting a smallest blob; build search inputs with deterministic tokenization).