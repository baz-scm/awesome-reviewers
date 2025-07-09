---
title: Modern shell syntax
description: 'Prefer double brackets (`[[ ]]`) over single brackets (`[ ]`) in shell
  scripts for improved functionality and consistency. While double brackets don''t
  strictly require quotes around variables, maintaining consistent quoting practice
  is recommended even with double brackets:'
repository: neondatabase/neon
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 19015
---

Prefer double brackets (`[[ ]]`) over single brackets (`[ ]`) in shell scripts for improved functionality and consistency. While double brackets don't strictly require quotes around variables, maintaining consistent quoting practice is recommended even with double brackets:

```bash
# Preferred style
if [[ "$variable" == "value" ]]; then
    # code
fi

# Instead of
if [ $variable == "value" ]; then
    # code
fi
```

This practice enhances readability and offers protection if scripts are later modified to use single brackets or embedded in contexts with stricter requirements.