---
title: validate external input safely
description: Always validate and sanitize external input using established libraries
  rather than manual string manipulation or custom parsing. External input includes
  user data, environment variables, command line arguments, and data from untrusted
  sources. Manual construction of structured data (like JSON) with user input creates
  injection vulnerabilities.
repository: electron/electron
label: Security
language: Other
comments_count: 3
repository_stars: 117644
---

Always validate and sanitize external input using established libraries rather than manual string manipulation or custom parsing. External input includes user data, environment variables, command line arguments, and data from untrusted sources. Manual construction of structured data (like JSON) with user input creates injection vulnerabilities.

Use proper validation libraries from //base or //v8 instead of manual string operations. For example, instead of manually constructing JSON:

```cpp
// UNSAFE - Manual JSON construction
std::wstringstream stm;
stm << L"[";
std::for_each(data, data + dataCount, [&](const auto& item) {
  stm << item << L",";  // No escaping, injection risk
});
stm << L"]";

// SAFE - Use proper JSON library
base::Value::List json_array;
for (const auto& item : data) {
  json_array.Append(base::Value(SanitizeInput(item)));
}
```

This principle applies to all external data sources: environment variables that could bypass security controls, user input in notifications, permission callbacks, and any data crossing trust boundaries. The goal is to prevent injection attacks and ensure data integrity through proper validation and sanitization.