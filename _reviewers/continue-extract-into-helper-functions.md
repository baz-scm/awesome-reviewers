---
title: Extract into helper functions
description: 'Break down complex or deeply nested code into smaller, well-named helper
  functions to improve readability and maintainability. Extract code into helpers
  when:'
repository: continuedev/continue
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 27819
---

Break down complex or deeply nested code into smaller, well-named helper functions to improve readability and maintainability. Extract code into helpers when:

1. A function contains deeply nested logic
2. Similar logic is repeated
3. A function handles multiple concerns
4. A block of code is complex enough to benefit from its own descriptive name

Example of improving complex nested code:

Before:
```typescript
function processNextEditData(filePath, beforeContent, afterContent, cursorPosBeforeEdit, ...) {
  // Get the current context data
  const currentData = (global._editAggregator as any).latestContextData || {
    configHandler: data.configHandler,
    getDefsFromLspFunction: data.getDefsFromLspFunction,
    recentlyEditedRanges: [],
    recentlyVisitedRanges: [],
  };

  void processNextEditData(
    beforeAfterdiff.filePath,
    beforeAfterdiff.beforeContent,
    beforeAfterdiff.afterContent,
    cursorPosBeforeEdit,
    cursorPosAfterPrevEdit,
    this.ide,
    currentData.configHandler,
    currentData.getDefsFromLspFunction,
    currentData.recentlyEditedRanges,
    currentData.recentlyVisitedRanges,
    currentData.workspaceDir,
  );
}
```

After:
```typescript
interface ProcessNextEditDataParams {
  filePath: string;
  beforeContent: string;
  afterContent: string;
  cursorPosBeforeEdit: Position;
  cursorPosAfterPrevEdit: Position;
  ide: IDE;
  configHandler: ConfigHandler;
  getDefsFromLspFunction: GetLspDefinitionsFunction;
  recentlyEditedRanges: RecentlyEditedRange[];
  recentlyVisitedRanges: AutocompleteCodeSnippet[];
  workspaceDir: string;
}

function getCurrentContextData(): ContextData {
  return (global._editAggregator as any).latestContextData || {
    configHandler: data.configHandler,
    getDefsFromLspFunction: data.getDefsFromLspFunction,
    recentlyEditedRanges: [],
    recentlyVisitedRanges: [],
  };
}

function processNextEditData(params: ProcessNextEditDataParams) {
  const currentData = getCurrentContextData();
  // Process using structured parameters...
}