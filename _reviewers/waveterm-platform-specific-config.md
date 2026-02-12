---
title: platform-specific config
description: 'Centralize OS-specific configuration and modifier mappings in a dedicated
  config/adapter module and document global declaration files. Motivation: key modifiers
  (Cmd/Meta/Alt/Option), global shortcuts, and shared types behave differently across
  platforms; putting the logic in one place avoids inconsistent handling, duplicate
  OS checks, and brittle startup...'
repository: wavetermdev/waveterm
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 17328
---

Centralize OS-specific configuration and modifier mappings in a dedicated config/adapter module and document global declaration files. Motivation: key modifiers (Cmd/Meta/Alt/Option), global shortcuts, and shared types behave differently across platforms; putting the logic in one place avoids inconsistent handling, duplicate OS checks, and brittle startup code.

Rules and how to apply:
- Create a single platform config module (e.g., src/config/platform.ts) that exports: current OS flags, a modifier mapping helper, and shortcut-registration helpers. Use this module everywhere for pretty-printing, key matching, and registering global shortcuts.
- Implement default platform semantics but allow explicit overrides: treat logical modifiers (Cmd, Meta, Option) as mapped to actual keys per OS, but if a keybind explicitly specifies Meta or Alt, respect that override.
- Make global .d.ts declaration files the canonical place for shared ambient types and document them (custom.d.ts, gotypes.d.ts). Do not scatter duplicate imports for those globally declared types.
- Ensure startup registration is OS-aware and idempotent: perform OS checks before registering platform-specific shortcuts and make registration reset/re-register safe on restart.

Code examples (patterns to follow):
- Platform mapping helper (conceptual)
const isMac = process.platform === "darwin";
export function mapLogicalModifier(mod: 'Cmd' | 'Meta' | 'Option') {
    if (mod === 'Cmd') return isMac ? 'Meta' : 'Alt';
    if (mod === 'Option') return isMac ? 'Alt' : 'Alt';
    return 'Meta'; // fallback
}

- Use mapping in prettyPrintKeybind:
function prettyPrintKeybind(keyDescription: string): string {
    const keyPress = parseKeyDescription(keyDescription);
    const mappedMods = {
        Cmd: mapLogicalModifier('Cmd'),
        Option: mapLogicalModifier('Option'),
        // respect explicit Meta/Alt in keyPress.mods if present
    };
    // build display string using mappedMods and platform symbols
}

- OS-aware global shortcut registration:
if (isMac) {
    reregisterGlobalShortcut('Cmd+F4');
} else if (process.platform === 'linux' || process.platform === 'win32') {
    reregisterGlobalShortcut('Alt+F4');
}

Practical checklist for PRs:
- Add or update platform mapping only in the config/adapter module, not inline in multiple files.
- Document any global types in custom.d.ts/gotypes.d.ts and reference them in code reviews.
- If a binding explicitly includes Meta/Alt, ensure the handler honors that instead of applying the default mapping.
- Confirm global shortcut registration is guarded by OS checks and that startup re-registration is safe and intentional.

This ensures consistent cross-platform behavior, easier testing and maintenance, and a single place to update OS-specific settings.