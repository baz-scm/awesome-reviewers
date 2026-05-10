---
title: Avoid Duplication Magic
description: When updating code, prioritize maintainability and readability by removing
  duplicated blocks, eliminating magic numbers, and keeping formatting/imports tooling-friendly.
repository: mermaid-js/mermaid
label: Code Style
language: TypeScript
comments_count: 9
repository_stars: 87952
---

When updating code, prioritize maintainability and readability by removing duplicated blocks, eliminating magic numbers, and keeping formatting/imports tooling-friendly.

Apply these rules:
- DRY duplicated logic: if the same algorithm/parameter set is repeated (e.g., measuring, wrapping, then shrinking/redrawing), extract it into a single helper/variable so future changes happen in one place.
- Remove magic numbers: replace unexplained numeric literals with named constants (ideally sourced from existing config/theme). This makes intent clear and prevents silent breakage if related limits change.
- Improve readability: use template literals instead of string concatenation where it clarifies intent, and keep import grouping consistent so auto-import tools don’t mis-group files.

Example (extract repeated wrap/shrink into one function):
```ts
const MAX_AVAILABLE_WIDTH = pieWidth - MARGIN;
const START_FONT_SIZE = 25;
const MIN_FONT_SIZE = 8;

function renderWrappedTitle(svg: any, titleText: string) {
  let fontSize = START_FONT_SIZE;
  let wrapped = wrapLabel(titleText, MAX_AVAILABLE_WIDTH, {
    fontSize,
    fontFamily: 'Arial',
    fontWeight: 400,
    joinWith: '<br/>',
  });

  // measure once per fontSize change
  let tempTitle = svg.append('text')
    .attr('x', pieWidth / 2)
    .attr('y', 30)
    .attr('class', 'pieTitleText')
    .style('text-anchor', 'middle')
    .style('white-space', 'pre-line')
    .style('font-size', fontSize + 'px');

  while (tempTitle.node()?.getBBox().width > MAX_AVAILABLE_WIDTH && fontSize > MIN_FONT_SIZE) {
    tempTitle.remove();
    fontSize -= 1;
    wrapped = wrapLabel(titleText, MAX_AVAILABLE_WIDTH, {
      fontSize,
      fontFamily: 'Arial',
      fontWeight: 400,
      joinWith: '<br/>',
    });

    tempTitle = svg.append('text')
      .attr('x', pieWidth / 2)
      .attr('y', 30)
      .attr('class', 'pieTitleText')
      .style('text-anchor', 'middle')
      .style('white-space', 'pre-line')
      .style('font-size', `${fontSize}px`);
  }

  const lines = wrapped.split('<br/>');
  lines.forEach((line, idx) => {
    tempTitle.append('tspan')
      .attr('x', pieWidth / 2)
      .attr('dy', idx === 0 ? 0 : '1.2em')
      .text(line);
  });

  return tempTitle;
}
```

Following this standard reduces duplicated maintenance work, makes “why” obvious (constants), and keeps code easier to review and debug.