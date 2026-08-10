---
title: Secure env lookup
description: 'When writing security-sensitive shell hooks/scripts, resolve credential
  *presence* safely: don’t read or print secret values, avoid `eval` for variable
  indirection, and enforce a deterministic, documented precedence order between `ENV_<KEY>`
  and raw env vars, falling back to OS keychain presence checks.'
repository: mvanhorn/last30days-skill
label: Security
language: Shell
comments_count: 1
repository_stars: 57799
---

When writing security-sensitive shell hooks/scripts, resolve credential *presence* safely: don’t read or print secret values, avoid `eval` for variable indirection, and enforce a deterministic, documented precedence order between `ENV_<KEY>` and raw env vars, falling back to OS keychain presence checks.

Example pattern (macOS presence-only, no secret retrieval):
```bash
load_keychain_presence() {
  case "$(uname -s 2>/dev/null)" in
    Darwin*) ;; *) return 0 ;;
  esac
  command -v security >/dev/null 2>&1 || return 0

  local user key current
  user="${USER:-}"
  [[ -z "$user" ]] && user="$(id -un 2>/dev/null || true)"
  [[ -n "$user" ]] || return 0

  for key in SETUP_COMPLETE OPENAI_API_KEY SCRAPECREATORS_API_KEY AUTH_TOKEN CT0 XAI_API_KEY BSKY_HANDLE EXA_API_KEY; do
    # Precedence: ENV_<KEY> first, then raw <KEY>.
    current="${!"ENV_${key}"}"
    [[ -z "$current" ]] && current="${!key}"
    [[ -n "$current" ]] && continue

    # Presence-only: do not retrieve the secret value.
    if security find-generic-password -a "$user" -s "last30days-${key}" >/dev/null 2>&1; then
      printf -v "ENV_${key}" '%s' "keychain"
    fi
  done
}
```

Adopt this as a standard: if you need credential-driven status, implement presence checks and safe indirection without `eval`, and write the precedence rules to avoid ambiguous behavior across environments.