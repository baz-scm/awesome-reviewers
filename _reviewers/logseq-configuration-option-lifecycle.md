---
title: Configuration option lifecycle
description: When adding new configuration options, follow a systematic approach to
  ensure consistency and maintainability across the application. This prevents incomplete
  implementations that can break existing functionality or create inconsistent user
  experiences.
repository: logseq/logseq
label: Configurations
language: Other
comments_count: 5
repository_stars: 37695
---

When adding new configuration options, follow a systematic approach to ensure consistency and maintainability across the application. This prevents incomplete implementations that can break existing functionality or create inconsistent user experiences.

The proper lifecycle for configuration options includes:

1. **Add to config schema** - Define the option's structure and validation rules
2. **Update config template** - Add documentation and examples to the default config template
3. **Provide default values** - Add fallback values in the appropriate config module (avoid hardcoding in templates as this breaks global config)
4. **Create accessor functions** - Implement getter and setter functions for the config option
5. **Use accessor functions consistently** - Always access config through the defined functions, never directly

Example of proper config option implementation:
```clojure
;; In config schema
:new-feature/enabled? {:type :boolean :default false}

;; In config template with documentation
;; Enable new feature functionality
;; Default value: false
:new-feature/enabled? false

;; Accessor functions
(defn new-feature-enabled? []
  (get (get-config) :new-feature/enabled? false))

;; Usage
(when (new-feature-enabled?)
  (enable-new-feature))
```

This systematic approach prevents issues like incomplete config implementations, missing documentation, hardcoded defaults that override global settings, and inconsistent access patterns. It also ensures that configuration changes are properly validated and don't silently break existing functionality.