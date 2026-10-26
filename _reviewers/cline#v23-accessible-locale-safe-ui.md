---
title: Accessible, locale-safe UI
description: 'When implementing UI components, treat accessibility semantics and localization
  as first-class code style constraints:


  - Accessibility: Any interactive UI control (e.g., resize handles, sliders, separators)
  must use correct semantic roles/attributes, be keyboard-focusable, and support expected
  keyboard actions.'
repository: cline/cline#v23
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70889
---

When implementing UI components, treat accessibility semantics and localization as first-class code style constraints:

- Accessibility: Any interactive UI control (e.g., resize handles, sliders, separators) must use correct semantic roles/attributes, be keyboard-focusable, and support expected keyboard actions.
  - Example pattern:
    ```tsx
    <div
      role="separator"
      tabIndex={0}
      aria-valuemin={0}
      aria-valuenow={height}
      aria-orientation="horizontal"
      onKeyDown={(e) => {
        if (e.key === "ArrowUp" || e.key === "ArrowDown") {
          const delta = e.shiftKey ? 20 : 5;
          onHeightChange(
            clampTerminalPanelHeight(height + (e.key === "ArrowDown" ? delta : -delta), window.innerHeight),
          );
        }
      }}
    />
    ```

- Localization: Do not hardcode locale-hostile joining like `", "` or assume the same word order across languages.
  - Build each translatable “part” as a self-contained phrase (so the translator controls grammar), and join items using locale-aware formatting (e.g., `Intl.ListFormat`).
  - Example pattern:
    ```ts
    const parts = [
      t("chatView:toolGroup.files", { count: readCount }),
      t("chatView:toolGroup.folders", { count: listCount }),
    ].filter(Boolean);

    const items = new Intl.ListFormat(i18nLocale, { type: "conjunction" }).format(parts);
    const summary = items
      ? t("chatView:toolGroup.contextPrefix", { items })
      : t("chatView:toolGroup.contextFallback");
    ```

Applying this standard prevents “works in English only” UI output and ensures interactive controls behave correctly for keyboard and assistive technologies.