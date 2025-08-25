---
title: Limit plugin outlet APIs
description: When creating plugin outlets or extension points, avoid exposing entire
  component instances, controllers, or large objects. Instead, pass explicit, minimal
  arguments that represent only the data and actions that plugins actually need.
repository: discourse/discourse
label: API
language: Other
comments_count: 2
repository_stars: 44898
---

When creating plugin outlets or extension points, avoid exposing entire component instances, controllers, or large objects. Instead, pass explicit, minimal arguments that represent only the data and actions that plugins actually need.

Exposing entire objects makes them part of the public API, making future refactoring difficult and creating tight coupling between internal implementation and external consumers.

**Bad:**
```gjs
<PluginOutlet
  @name="sub-category-item"
  @outletArgs={{hash subCategoryItem=this}}
/>

<PluginOutlet
  @name="exception-wrapper"
  @outletArgs={{lazyHash controller=@controller}}
/>
```

**Good:**
```gjs
<PluginOutlet
  @name="sub-category-item"
  @outletArgs={{lazyHash 
    category=this.category
    unreadCount=this.unreadTopicsCount
    newCount=this.newTopicsCount
    hideUnread=this.hideUnread
  }}
/>

<PluginOutlet
  @name="exception-wrapper"
  @outletArgs={{lazyHash
    errorHtml=@controller.errorHtml
    isForbidden=@controller.isForbidden
    reason=@controller.reason
    requestUrl=@controller.requestUrl
  }}
/>
```

This approach creates stable, documented interfaces that can evolve independently of internal implementation changes.