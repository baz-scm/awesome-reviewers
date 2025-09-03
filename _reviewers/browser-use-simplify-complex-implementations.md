---
title: Simplify complex implementations
description: Replace verbose, complex code structures with simpler, more readable
  alternatives. Prefer existing methods over inline complex logic, use built-in functions
  instead of manual implementations, and leverage modern Python features for cleaner
  code.
repository: browser-use/browser-use
label: Code Style
language: Python
comments_count: 4
repository_stars: 69139
---

Replace verbose, complex code structures with simpler, more readable alternatives. Prefer existing methods over inline complex logic, use built-in functions instead of manual implementations, and leverage modern Python features for cleaner code.

Examples of improvements:
- Replace complex conditionals with existing methods: `if browser_session.is_file_input(element_node):` instead of multi-line type checking
- Simplify string manipulation: `script_content.replace('```python', '').replace('```', '')` instead of complex split logic with potential IndexError
- Use dictionary dispatch instead of long if/elif chains for action mapping
- Leverage modern Python features like the walrus operator: `if (last_action := self.step_results[-1]['actions'][-1])['is_done']`

This approach reduces code complexity, improves maintainability, and makes the codebase more readable while preventing potential errors from overly complex implementations.