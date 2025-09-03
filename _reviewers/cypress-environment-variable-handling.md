---
title: Environment variable handling
description: Environment variables should be properly validated, parsed, and documented
  with clear override mechanisms. Always validate that environment variable names
  are non-empty strings before processing. When parsing environment variable values,
  trim whitespace and remove surrounding quotes to handle cross-platform differences,
  especially on Windows where quotes...
repository: cypress-io/cypress
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 48850
---

Environment variables should be properly validated, parsed, and documented with clear override mechanisms. Always validate that environment variable names are non-empty strings before processing. When parsing environment variable values, trim whitespace and remove surrounding quotes to handle cross-platform differences, especially on Windows where quotes may be preserved. Provide meaningful override mechanisms using descriptive environment variable names rather than hardcoding values.

Example of proper environment variable handling:
```javascript
function getEnv(varName, trim = false) {
  la(is.unemptyString(varName), 'expected environment variable name, not', varName)
  
  const envVar = process.env[varName]
  const configVar = process.env[`npm_config_${varName}`]
  
  let result = envVar || configVar
  
  // Handle Windows quote preservation and whitespace
  return trim ? dequote(_.trim(result)) : result
}

// Provide override mechanisms with descriptive names
if (process.env.CYPRESS_DOCKER_DEV_INSPECT_OVERRIDE) {
  argv.unshift(`--inspect-brk=${process.env.CYPRESS_DOCKER_DEV_INSPECT_OVERRIDE}`)
} else {
  argv.unshift('--inspect-brk=5566')
}

// Platform-specific environment setup
function getOpenModeEnv() {
  if (os.platform() !== 'linux') return
  
  // Document why this environment variable is needed
  return { GTK_USE_PORTAL: '1' }
}
```

This approach ensures configuration is flexible, well-documented, and handles cross-platform differences gracefully while providing clear override paths for different deployment scenarios.