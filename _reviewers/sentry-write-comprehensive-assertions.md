---
title: Write comprehensive assertions
description: 'When writing tests, ensure your assertions thoroughly verify all relevant
  aspects of the functionality being tested. Go beyond the basic "happy path" checks
  and include assertions that verify:'
repository: getsentry/sentry
label: Testing
language: TSX
comments_count: 3
repository_stars: 41297
---

When writing tests, ensure your assertions thoroughly verify all relevant aspects of the functionality being tested. Go beyond the basic "happy path" checks and include assertions that verify:

1. **Presence of expected elements**: Test that required UI elements or data are present
2. **Absence of unexpected elements**: Explicitly check that certain elements are NOT rendered when they shouldn't be
3. **Specific properties and states**: Test ordering, formatting, and other properties beyond mere existence

**Example 1**: When testing a component that shouldn't render certain elements:
```typescript
// Instead of only checking that one text element isn't present:
expect(
  screen.queryByText('Select from one of these suggestions')
).not.toBeInTheDocument();

// Also verify that no suggestion elements are rendered:
expect(screen.queryByText(/https:\/\/github\.com/)).not.toBeInTheDocument();
```

**Example 2**: When testing tabular data, verify column ordering:
```typescript
// Don't just check that columns exist
expect(screen.getByText('http request_method')).toBeInTheDocument();
expect(screen.getByText('count span.duration')).toBeInTheDocument();

// Also verify the columns appear in the expected order
const headers = screen.getAllByRole('columnheader');
expect(headers[0].textContent).toBe('http request_method');
expect(headers[1].textContent).toBe('count span.duration');
```

**Example 3**: Use realistic test data rather than undefined values:
```typescript
// Instead of letting values be undefined in tests
expect(screen.getByText('/settings/')).toHaveAttribute(
  'href',
  '/organizations/org-slug/traces/trace/undefined/?referrer=breadcrumbs'
);

// Provide valid mock data
const traceId = 'abcd1234efgh5678';
expect(screen.getByText('/settings/')).toHaveAttribute(
  'href',
  `/organizations/org-slug/traces/trace/${traceId}/?referrer=breadcrumbs`
);
```

Comprehensive assertions make tests more meaningful by ensuring they actually verify the intended behavior, catch regressions, and serve as documentation of expected functionality.