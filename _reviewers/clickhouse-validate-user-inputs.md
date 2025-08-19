---
title: validate user inputs
description: Always validate and properly escape user-controlled input before incorporating
  it into structured data formats like JSON, SQL, XML, or command strings. Unescaped
  input can lead to injection vulnerabilities that allow attackers to manipulate application
  logic or access unauthorized data.
repository: ClickHouse/ClickHouse
label: Security
language: C++
comments_count: 3
repository_stars: 42425
---

Always validate and properly escape user-controlled input before incorporating it into structured data formats like JSON, SQL, XML, or command strings. Unescaped input can lead to injection vulnerabilities that allow attackers to manipulate application logic or access unauthorized data.

When building JSON strings programmatically, use proper JSON libraries instead of string concatenation. For example, instead of:

```cpp
// VULNERABLE - direct string concatenation
std::string request_body = "{\"hostname\": \"" + host_str + "\"}";
```

Use a JSON library or proper escaping:

```cpp
// SAFE - using JSON library
Poco::JSON::Object json_obj;
json_obj.set("hostname", host_str);
std::ostringstream oss;
json_obj.stringify(oss);
std::string request_body = oss.str();
```

This principle applies to all contexts where user input is incorporated into structured formats. Additionally, validate authentication parameters completely - reject incomplete credential sets with clear error messages rather than silently choosing defaults or ignoring missing values.