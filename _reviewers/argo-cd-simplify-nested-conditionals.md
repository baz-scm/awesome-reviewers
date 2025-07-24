---
title: simplify nested conditionals
description: Combine multiple nested if statements using logical operators (and/or)
  to improve code readability and reduce unnecessary indentation. Remove redundant
  nil checks when they are unnecessary, especially when subsequent checks would naturally
  handle the nil case.
repository: argoproj/argo-cd
label: Code Style
language: Other
comments_count: 2
repository_stars: 20149
---

Combine multiple nested if statements using logical operators (and/or) to improve code readability and reduce unnecessary indentation. Remove redundant nil checks when they are unnecessary, especially when subsequent checks would naturally handle the nil case.

Instead of deeply nested conditions:
```lua
if obj.status ~= nil then
  if obj.status.conditions ~= nil then
    for i, condition in ipairs(obj.status.conditions) do
      if condition.type ~= nil then
        if condition.type == "Ready" then
          if condition.status ~= nil and condition.reason ~= nil then
            -- logic here
          end
        end
      end
    end
  end
end
```

Consolidate into cleaner, more readable code:
```lua
if obj.status and obj.status.conditions then
  for i, condition in ipairs(obj.status.conditions) do
    if condition.type == "Ready" and condition.status == "True" and condition.reason == "SuccessfulCreateOrUpdate" then
      -- logic here
    end
  end
end
```

This approach reduces cognitive load, eliminates unnecessary nesting levels, and makes the code's intent clearer by focusing on the actual conditions that matter rather than defensive nil checking.