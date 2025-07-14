---
title: Assert before cast
description: Always validate values before performing unsafe operations like dynamic
  casting. When a value could be null, zero, or undefined, store it in an intermediate
  variable and verify it before proceeding.
repository: oven-sh/bun
label: Null Handling
language: C++
comments_count: 7
repository_stars: 79093
---

Always validate values before performing unsafe operations like dynamic casting. When a value could be null, zero, or undefined, store it in an intermediate variable and verify it before proceeding.

**Bad:**
```cpp
// Risky: jsDynamicCast on a zero value is undefined behavior
auto* existing_tag = jsDynamicCast<Bun::NapiTypeTag*>(globalObject->napiTypeTags()->get(js_object));

// Dangerous: No verification before dereferencing
return handleSlot ? JSC::JSValue::encode(*handleSlot) : JSC::JSValue::encode(JSC::JSValue());
```

**Good:**
```cpp
// Safe: Store the result first, then check before casting
JSValue napiTypeTagValue = globalObject->napiTypeTags()->get(js_object);
auto* existing_tag = jsDynamicCast<Bun::NapiTypeTag*>(napiTypeTagValue);

// Better: Assert your assumptions explicitly
ASSERT(handleSlot);
return JSC::JSValue::encode(*handleSlot);
```

For functions that can return null or trigger exceptions, add appropriate assertions after critical operations:

```cpp
// Assert getDirect doesn't return null
auto value = thisObject->getDirect(vm, builtinNames.statePrivateName());
ASSERT(value);

// Check for exceptions after conversions
auto state = value.toInt32(lexicalGlobalObject);
assertNoExceptionExceptTermination();
```

This approach prevents undefined behavior, makes code intent clearer, and helps catch bugs earlier in the development process.