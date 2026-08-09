---
title: Precision Resize and Singleton Style
description: 'When performance or visual stability matters (e.g., zoom/antialiasing),
  prefer precision-first measurement and avoid expensive DOM churn.


  Apply these rules:'
repository: paper-design/shaders
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 3286
---

When performance or visual stability matters (e.g., zoom/antialiasing), prefer precision-first measurement and avoid expensive DOM churn.

Apply these rules:
1) Use high-precision resize measurements
- Avoid rounded CSS pixel APIs like `clientWidth/clientHeight` when jitter appears during zoom.
- Prefer `ResizeObserver` and read `borderBoxSize` (more stable than layout-derived rounded values).
- Also handle `visualViewport` resize when zoom changes affect rendering.

2) Inject shared resources only once (or reference-count)
- If multiple component instances need the same `<style>`, `<canvas>`, or other shared DOM/CSS, create/inject it a single time.
- Do not repeatedly add/remove shared `<style>` nodes on mount/unmount; it’s often more expensive than keeping them.
- If you must remove on final unmount, track usage (reference counting) rather than blindly removing.

Example pattern:
```ts
class ExampleMount {
  private parentWidth = 0;
  private parentHeight = 0;
  private resizeObserver: ResizeObserver | null = null;

  constructor(private parentElement: HTMLElement) {
    // Singleton style injection
    if (!document.querySelector('style[data-my-component]')) {
      const style = document.createElement('style');
      style.setAttribute('data-my-component', '');
      style.textContent = '/* shared styles */';
      document.head.prepend(style);
    }

    this.resizeObserver = new ResizeObserver(([entry]) => {
      const size = entry?.borderBoxSize?.[0];
      if (size) {
        this.parentWidth = size.inlineSize;
        this.parentHeight = size.blockSize;
      }
      // recompute render scale / canvas size using parentWidth/parentHeight
    });

    this.resizeObserver.observe(this.parentElement);

    // Optional: visual viewport changes can affect zoom-related rendering
    visualViewport?.addEventListener('resize', () => {
      // recompute render scale / canvas size
      // (avoid clientWidth/clientHeight if jitter is observed)
    });
  }
}
```
This standard reduces resize jitter and prevents unnecessary DOM operations—both common sources of UI performance regressions.