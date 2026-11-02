---
title: Mandate precise security mitigations
description: 'Security-related configuration and documentation must be prescriptive
  and technically accurate, not vague suggestions. When a mitigation is required to
  close a vulnerability, state it as a requirement rather than an option: e.g. for
  Host header injection, docs should say "set SERVER_NAME and/or trusted_hosts" rather
  than "consider using trusted_hosts",...'
repository: pallets/flask#x
label: Security
language: Other
comments_count: 2
repository_stars: 75163
---

Security-related configuration and documentation must be prescriptive and technically accurate, not vague suggestions. When a mitigation is required to close a vulnerability, state it as a requirement rather than an option: e.g. for Host header injection, docs should say "set SERVER_NAME and/or trusted_hosts" rather than "consider using trusted_hosts", since this is the only effective protection against the issue. Similarly, when documenting security headers, ensure the semantics are correct per spec—for example, the HSTS `preload` directive is only valid when combined with `includeSubDomains`, so examples like `Strict-Transport-Security: max-age=<expire-time>; preload` without `includeSubDomains` are misleading and should not be presented as valid on their own. Before merging security guidance or configuration code, verify: (1) the mitigation is stated as mandatory when it is the only real defense, and (2) any protocol/header directives shown are complete and correct, so developers don't end up with a false sense of security from incomplete or optional-sounding advice.