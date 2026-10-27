---
title: Deliberate, consistent naming
description: Choose identifier names deliberately and apply naming patterns consistently,
  since names often become semi-public contracts or convey important semantic distinctions.
repository: facebook/react#b19
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 251893
---

Choose identifier names deliberately and apply naming patterns consistently, since names often become semi-public contracts or convey important semantic distinctions.

- For exported/public types, follow an established, predictable convention (e.g. `${PascalCase(functionName)}Options` for an options param, so `renderToReadableStream` gets `RenderToReadableStreamOptions`). Treat these names as part of the API surface: even unexported types get referenced by downstream consumers (e.g. DefinitelyTyped), so renaming later is a breaking change. Decide on and document the convention before shipping, and don't assume a convention used for one kind of type (e.g. "Options") automatically applies to others.
- Only add disambiguating suffixes (e.g. a "Static" suffix on a flag) when there's an actual counterpart that needs distinguishing. If no render-specific version of a flag exists, don't force a suffix just to match sibling constants—keep the simpler name.
- When naming properties that will be read/written dynamically (e.g. `dataset['ri']`), prefer bracket-string access over dot notation so the identifier survives property minification (e.g. Closure Compiler advanced mode) and encode information compactly (e.g. put the instruction into the attribute name itself rather than spreading it across many attributes).
- For user-facing strings/messages, pick wording that is unambiguous about the actual state (e.g. prefer "Selected element wasn't rendered with React." over a vaguer "No element rendered by React selected." when a selection always exists).

In short: pick names up front with their long-term, external-facing implications in mind, keep naming patterns consistent across similar constructs, and make names as unambiguous as possible for both humans and tooling.