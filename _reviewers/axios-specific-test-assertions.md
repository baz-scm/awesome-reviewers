---
title: "Specific test assertions"
description: "When writing tests, explicitly assert specific conditions and expected values rather than relying on general success/failure checks. This prevents tests from silently passing when they should fail and ensures tests verify exactly what they're intended to verify."
repository: "axios/axios"
label: "Testing"
language: "JavaScript"
comments_count: 5
repository_stars: 107000
---

When writing tests, explicitly assert specific conditions and expected values rather than relying on general success/failure checks. This prevents tests from silently passing when they should fail and ensures tests verify exactly what they're intended to verify.

Three key practices to follow:

1. **Handle promise rejections explicitly** - Always include catch clauses in promise chains and pass errors to the done callback:
```javascript
axios.get('http://localhost:4444/')
  .then(function(res) {
    // assertions here
    done();
  }).catch(done); // This ensures test fails if promise rejects
```

2. **Assert specific error conditions** - When testing error cases, verify specific error details rather than just that an error occurred:
```javascript
axios.get('http://localhost:4444/')
  .catch(function(error) {
    assert.equal(error.code, 'ERR_FR_TOO_MANY_REDIRECTS');
    // Test specific error conditions, not just that an error happened
    done();
  });
```

3. **Include explicit expected values** - Use literal expected values in assertions rather than relying on functions with unclear output:
```javascript
// Bad: Hard to see expected value
expect(buildURL('/foo', {date: date})).toEqual('/foo?date=' + date.toISOString());

// Better: Shows exact expected output
expect(buildURL('/foo', {date: date})).toEqual('/foo?date=' + encodeURIComponent(date.toISOString()));
```

Following these practices makes tests more reliable indicators of correct behavior and easier to debug when they fail.