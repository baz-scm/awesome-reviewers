---
title: Proper mocking techniques
description: 'Use appropriate mocking approaches for different dependencies in tests
  to ensure accurate test results and prevent false positives. Different types of
  dependencies require different mocking strategies:'
repository: grafana/grafana
label: Testing
language: TSX
comments_count: 3
repository_stars: 68825
---

Use appropriate mocking approaches for different dependencies in tests to ensure accurate test results and prevent false positives. Different types of dependencies require different mocking strategies:

1. For browser APIs not implemented in JSDOM (like `window.open`):
```javascript
// Define and mock the property before using it
// @ts-expect-error global.open should return a Window, but is not implemented in js-dom.
const openSpy = jest.spyOn(global, 'open').mockReturnValue(true);
```

2. For utility functions like logging, prefer individual method mocks with cleanup:
```javascript
beforeEach(() => {
  jest.spyOn(log, 'error').mockImplementation(() => {});
  jest.spyOn(log, 'warning').mockImplementation(() => {});
  jest.spyOn(log, 'debug').mockImplementation(() => {});
});

afterEach(() => {
  jest.resetAllMocks();
});
```

3. For module dependencies, use dedicated mocks rather than actual imports:
```javascript
// Instead of using setupDataSources which imports actual modules:
const dsServer = new MockDataSourceSrv(datasources) as unknown as DataSourceSrv;
```

Using precise mocking strategies improves test reliability, prevents unexpected behavior from external dependencies, and ensures tests validate exactly what you intend to test.