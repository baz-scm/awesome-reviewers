---
title: Config/version compatibility
description: When configuration depends on specific tool/library behavior, keep versions
  and config in sync, and separate shared configuration from user/environment-specific
  overrides.
repository: facebook/react#b11
label: Configurations
language: Json
comments_count: 3
repository_stars: 251894
---

When configuration depends on specific tool/library behavior, keep versions and config in sync, and separate shared configuration from user/environment-specific overrides.

Apply these rules:
1) **Match major versions to the config API**
   - If a dependency upgrade changes a config surface (e.g., RuleTester behavior), update the test harness/config, or import/use the compatible implementation for the expected major version.

   Example pattern:
   ```js
   // If your tests expect v8 RuleTester semantics:
   const { RuleTester: RuleTesterV8 } = require('eslint-v8');
   const ruleTester = new RuleTesterV8({ parserOptions: { ecmaVersion: 2020 } });
   ```

2) **Scope environment-specific dependencies**
   - Add fixture-only tooling in `devDependencies` and mark OS-specific packages as `optionalDependencies`.
   - Document any required install/workarounds (e.g., use `yarn install --ignore-optional` when that’s the known fix).

3) **Separate shared vs user-local config**
   - Don’t commit user-specific files like `settings.local.json`; gitignore them.
   - Keep shareable defaults/settings in a non-local file (e.g., `settings.json`).

Net effect: fewer “works on my machine” failures and fewer test breaks after dependency/major-version changes.