---
name: nodejs-reviewer
description: "Guidelines for reviewing Node.js core code, highlighting security best practices and modern JavaScript idioms for maintainability."
license: CC-BY-4.0
---

# Node.js Code Review Guidelines

## Input Validation and Security
All network or external inputs in Node.js should be validated and sanitized to prevent security vulnerabilities[25]. Review any code that uses user-supplied data (URLs, headers, query params, etc.) to ensure it restricts or checks those values. For example, when handling URLs, allow only trusted hosts or expected formats – e.g., ensure an incoming URL is a loopback address if that’s required[26]. In Node core, an example is restricting connections to localhost or similar to mitigate SSRF attacks[27]. Also check for header and payload sanitization: ensure the code screens out illegal characters or sequences (like CRLF in headers, to prevent HTTP request smuggling)[28][29]. A good practice is to write utility validators (like a function `validateNoControlChars(value)` that throws an error if forbidden characters are present) and use them on any data that will form part of a request/response protocol[30]. By validating inputs and refusing suspicious values, the Node.js code avoids common injection attacks and improves overall security[31].

## Modern JavaScript Practices
Encourage the use of modern JavaScript features in Node.js code for clarity and reliability. In particular, when dealing with potentially undefined or null values, prefer using optional chaining (`?.`) and nullish coalescing (`??`) instead of lengthy manual checks[32]. These operators make code more concise and less error-prone. For example, instead of:

```js
// Verbose null check
if (obj && obj.prop) {
  value = obj.prop;
} else {
  value = defaultVal;
}
```

```js
value = obj?.prop ?? defaultVal;
```

The latter safely handles the null case in one line[33]. The same goes for setting default values or lazily initializing variables – e.g., use `foo ??= computeFoo()` to only assign if `foo` is nullish[34]. Encourage consistent use of these patterns across the codebase: it improves readability and reduces the chance of forgetting a null check. Also, ensure legacy patterns are updated – e.g., replacing older `||` checks or verbose `if` chains with these new operators where appropriate. Adopting modern syntax not only makes the code cleaner but also clarifies the intent (since `??` won’t treat `0` or `""` as null, for instance, which avoids subtle bugs)[35].
