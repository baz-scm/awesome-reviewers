---
title: disable sensitive data defaults
description: Features that handle sensitive data such as credit card information,
  passwords, or personal details should never be enabled by default. These features
  must require explicit user opt-in to ensure users consciously consent to the handling
  of their sensitive information.
repository: zen-browser/desktop
label: Security
language: JavaScript
comments_count: 1
repository_stars: 34711
---

Features that handle sensitive data such as credit card information, passwords, or personal details should never be enabled by default. These features must require explicit user opt-in to ensure users consciously consent to the handling of their sensitive information.

Enabling sensitive data features by default creates security risks because users may unknowingly have their sensitive information stored, transmitted, or processed without their explicit consent. This violates the principle of informed consent and can lead to data breaches or privacy violations.

Example of problematic code:
```javascript
// BAD: Enabling credit card autofill by default for all countries
pref("extensions.formautofill.creditCards.supported", true);
pref("extensions.formautofill.creditCards.supportedCountries", 'AF,AX,AL,DZ...');
```

Instead, such features should be disabled by default and require user action to enable:
```javascript
// GOOD: Sensitive features disabled by default
pref("extensions.formautofill.creditCards.supported", false);
// Only enable after explicit user consent through settings UI
```

This principle applies to any feature handling sensitive data including payment information, authentication credentials, personal identifiers, or private communications.