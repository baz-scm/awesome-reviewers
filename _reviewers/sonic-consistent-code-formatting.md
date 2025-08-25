---
title: consistent code formatting
description: Maintain consistent indentation and brace alignment throughout the codebase
  to improve readability and code organization. Use 4-space indentation consistently
  across all files and align closing braces with their corresponding opening statements.
repository: bytedance/sonic
label: Code Style
language: C
comments_count: 2
repository_stars: 8532
---

Maintain consistent indentation and brace alignment throughout the codebase to improve readability and code organization. Use 4-space indentation consistently across all files and align closing braces with their corresponding opening statements.

Key formatting requirements:
- Use 4 spaces for indentation (no tabs)
- Align closing braces with the statement that opened the block
- Maintain consistent spacing around operators and control structures
- Ensure all code blocks follow the same alignment patterns

Example of proper formatting:
```c
while(pos[i] !='\0'){
    if(k==arr->cap){
        *p = i+1;
        return ERR_RECURSE_MAX;
    }
    while(is_space(pos[i])){
        i++;             
    }
}
```

Consistent formatting makes code easier to read, debug, and maintain. It also helps team members quickly understand code structure and reduces cognitive load when reviewing or modifying code.