---
title: Descriptive balanced naming
description: "Choose identifier names that clearly communicate their purpose while\
  \ maintaining an appropriate balance between brevity and clarity. \n\n**Guidelines:**"
repository: ollama/ollama
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 145704
---

Choose identifier names that clearly communicate their purpose while maintaining an appropriate balance between brevity and clarity. 

**Guidelines:**

1. **Use descriptive names that reflect types and purpose:**
   ```go
   // Poor: Using abbreviated or generic names
   cap, err := GetModel(n.String())
   
   // Good: Name reflects the actual type
   model, err := GetModel(n.String())
   ```

2. **Avoid abbreviations unless universally understood:**
   ```go
   // Poor: Unnecessary abbreviation
   type RopeOpts struct {}
   
   // Good: Full word for clarity
   type RopeOptions struct {}
   ```

3. **Balance verbosity - aim for 1-2 word components:**
   ```go
   // Too verbose
   var templateToolPrefix, templateToolPrefixFound := ToolPrefix(model.Template.Template)
   
   // Better balance
   prefix, found := toolPrefix(model.Template.Template)
   ```

4. **Be consistent with naming patterns:**
   ```go
   // Inconsistent with other handlers
   func (s *Server) version(w http.ResponseWriter, r *http.Request)
   
   // Consistent with other handler naming
   func (s *Server) VersionHandler(c *gin.Context)
   ```

5. **Avoid single-letter variables** outside of short-lived scopes like simple loops.

6. **In environment variables and constants**, spell words completely:
   ```go
   // Poor: Ambiguous abbreviation
   OLLAMA_GPU_DEVS
   
   // Good: Clear, fully spelled out
   OLLAMA_GPU_DEVICES
   ```

When choosing names, prioritize clarity for future readers over saving a few keystrokes now.