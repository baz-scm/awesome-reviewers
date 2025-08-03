---
title: Avoid hardcoded configurations
description: Always extract configuration values from appropriate sources (config
  files, environment variables, etc.) rather than hardcoding them in your code. Include
  validation to ensure the configuration is valid before use, and provide sensible
  defaults with the ability to override when needed.
repository: RooCodeInc/Roo-Code
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 17288
---

Always extract configuration values from appropriate sources (config files, environment variables, etc.) rather than hardcoding them in your code. Include validation to ensure the configuration is valid before use, and provide sensible defaults with the ability to override when needed.

**Bad practice:**
```javascript
// Hardcoded values that are difficult to maintain
execSync(`code --uninstall-extension rooveterinaryinc.roo-cline`, { stdio: "inherit" })
```

**Good practice:**
```javascript
// Dynamic configuration from package.json
const packageJson = JSON.parse(fs.readFileSync("./src/package.json", "utf-8"))
const publisher = packageJson.publisher
const name = packageJson.name
const extensionId = `${publisher}.${name}`

// Validation before use
const vsixFileName = `./bin/${name}-${version}.vsix`
if (!fs.existsSync(vsixFileName)) {
  console.error(`VSIX file not found: ${vsixFileName}`)
  process.exit(1)
}

// Allow for overriding defaults
const editorCommand = process.env.EDITOR_COMMAND || "code"
execSync(`${editorCommand} --uninstall-extension ${extensionId}`, { stdio: "inherit" })
```

This approach improves maintainability, prevents errors when configurations change, and allows your code to work in different environments without modification.