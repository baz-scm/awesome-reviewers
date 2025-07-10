---
title: Avoid variable name abbreviations
description: Use complete, descriptive variable names instead of abbreviations to
  enhance code readability and maintainability. Short abbreviations like `dir`, `repo`,
  and single-letter variables often obscure the purpose of the variable and make code
  harder to understand for new contributors.
repository: Homebrew/brew
label: Naming Conventions
language: Shell
comments_count: 4
repository_stars: 44168
---

Use complete, descriptive variable names instead of abbreviations to enhance code readability and maintainability. Short abbreviations like `dir`, `repo`, and single-letter variables often obscure the purpose of the variable and make code harder to understand for new contributors.

Good:
```bash
normalise_tap_name() {
  local directory="$1"
  local user
  local repository

  user="$(tr '[:upper:]' '[:lower:]' <<<"${directory%%/*}")"
  repository="$(tr '[:upper:]' '[:lower:]' <<<"${directory#*/}")"
  repository="${repository#@(home|linux)brew-}"
  echo "${user}/${repository}"
}
```

Bad:
```bash
normalise_tap_name() {
  local dir="$1"
  local u
  local repo

  u="$(tr '[:upper:]' '[:lower:]' <<<"${dir%%/*}")"
  repo="$(tr '[:upper:]' '[:lower:]' <<<"${dir#*/}")"
  repo="${repo#@(home|linux)brew-}"
  echo "${u}/${repo}"
}
```

Exceptions: Standard abbreviations that are widely understood within the domain or temporary variables with extremely limited scope and obvious context.