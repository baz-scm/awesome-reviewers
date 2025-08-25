---
title: Meaningful comment practices
description: Comments should explain the reasoning behind code decisions rather than
  restating what the code obviously does. Focus on the "why" rather than the "what"
  to provide value that isn't immediately apparent from reading the code itself.
repository: bytedance/sonic
label: Documentation
language: C
comments_count: 2
repository_stars: 8532
---

Comments should explain the reasoning behind code decisions rather than restating what the code obviously does. Focus on the "why" rather than the "what" to provide value that isn't immediately apparent from reading the code itself.

For placement, longer explanatory comments should be written on separate lines above the relevant code block. API documentation and function descriptions should be positioned above the function declaration, not inline or scattered throughout the implementation.

Example of poor commenting:
```c
while(isSpace(pos[i])){    // If there is a space before the beginning, eat the space first 
    i++;                           
}
if(pos[i] != '['){         // If the first one is not a left bracket, returning it directly is illegal
    *p = i+1;              // P points to the first position after the error 
    arr->len = 0;
    return ERR_INVAL;
}
```

Example of improved commenting:
```c
// Skip leading whitespace to handle malformed input gracefully
while(isSpace(pos[i])){                                  
    i++;                           
}

// Array format must start with '[' - reject invalid syntax early
if(pos[i] != '['){
    *p = i+1;
    arr->len = 0;
    return ERR_INVAL;
}
```

For API functions, place comprehensive documentation above the function:
```c
// Parses a JSON-like array string into GoIntSlice structure
// Returns error code on invalid format, updates position pointer
long decode_u64_array(const GoString* src, long* p, GoIntSlice* arr){
    // implementation...
}
```