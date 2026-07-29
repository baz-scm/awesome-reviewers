---
title: Consistent Accessible UI
description: When adding expandable/conditional UI in React/TSX, keep the structure
  consistent within the surrounding component *and* ensure accessibility attributes
  are applied uniformly.
repository: diegosouzapw/OmniRoute
label: Code Style
language: TSX
comments_count: 2
repository_stars: 33162
---

When adding expandable/conditional UI in React/TSX, keep the structure consistent within the surrounding component *and* ensure accessibility attributes are applied uniformly.

Apply this standard:
- If the same “advanced settings” pattern appears multiple times, consider extracting a reusable component (e.g., `AdvancedPathSettings`) to reduce duplication once it’s repeated.
- Regardless of whether you inline or extract, interactive toggles must include the correct ARIA wiring, and decorative indicators (like a chevron) must be marked as non-informative.

Example (toggle + conditional section, with consistent ARIA):
```tsx
function AdvancedToggle({ showAdvanced, setShowAdvanced }: {
  showAdvanced: boolean;
  setShowAdvanced: (v: boolean) => void;
}) {
  const id = "advanced-settings";

  return (
    <>
      <button
        type="button"
        className="text-sm text-text-muted hover:text-text-primary flex items-center gap-1"
        aria-expanded={showAdvanced}
        aria-controls={id}
        onClick={() => setShowAdvanced(!showAdvanced)}
      >
        <span
          className={`transition-transform ${showAdvanced ? "rotate-90" : ""}`}
          aria-hidden="true"
        >
          ▶
        </span>
        advanced settings
      </button>

      {showAdvanced && (
        <div id={id} className="flex flex-col gap-3 pl-2 border-l-2 border-border">
          {/* advanced inputs here */}
        </div>
      )}
    </>
  );
}
```