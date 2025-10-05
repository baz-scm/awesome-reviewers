---
title: eliminate unnecessary code
description: Remove redundant code constructs and prefer concise, direct patterns
  that improve readability and maintainability. This includes eliminating unnecessary
  widget/layout creation, using ternary operators for simple conditionals, direct
  initialization patterns, and simplifying complex calculations with named constants.
repository: commaai/openpilot
label: Code Style
language: Other
comments_count: 5
repository_stars: 58214
---

Remove redundant code constructs and prefer concise, direct patterns that improve readability and maintainability. This includes eliminating unnecessary widget/layout creation, using ternary operators for simple conditionals, direct initialization patterns, and simplifying complex calculations with named constants.

Examples of improvements:
- Instead of creating wrapper widgets unnecessarily: `routes_type_selector_->addTab(preserved_route_list_ = new RouteListWidget, tr("&Preserved"));`
- Use ternary operators for simple conditionals: `return routes_type_selector_->currentIndex() == 0 ? route_list_ : preserved_route_list_;`
- Direct layout attachment: `auto layout = new QVBoxLayout(widget)` instead of separate `setLayout()` calls
- Replace complex calculations with named constants: `const QColor ENGAGED_COLOR = QColor::fromRgbF(0.1, 0.945, 0.26);` instead of inline math
- Eliminate unnecessary variable assignments and prefer direct initialization where possible

This approach reduces code bloat, makes intent clearer, and improves maintainability by removing opportunities for errors in redundant code paths.