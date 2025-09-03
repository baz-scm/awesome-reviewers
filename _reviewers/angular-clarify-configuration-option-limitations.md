---
title: Clarify configuration option limitations
description: When documenting or designing configuration options, explicitly state
  both what the option does AND what it doesn't do, including any limitations or side
  effects. Users often make incorrect assumptions about configuration behavior based
  on names alone.
repository: angular/angular
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 98611
---

When documenting or designing configuration options, explicitly state both what the option does AND what it doesn't do, including any limitations or side effects. Users often make incorrect assumptions about configuration behavior based on names alone.

For example, avoid ambiguous descriptions like "Only register tools that do not make changes" and instead be specific about scope and limitations: "Only register Angular MCP tools that don't modify your code. Your editor or coding agent may still perform edits."

Similarly, when explaining optional configuration properties, clarify the implications of omitting them:

```ts
// ❌ Unclear: "you need to provide a configuration object"
@Injectable({ providedIn: 'root' })

// ✅ Clear: explain what happens when omitted
// providedIn isn't required; if omitted, the service isn't automatically 
// provided and must be added to the providers array of bootstrapApplication 
// or a component/directive
@Injectable()
```

This prevents developers from misunderstanding configuration behavior and helps them make informed decisions about which options to use in different contexts.