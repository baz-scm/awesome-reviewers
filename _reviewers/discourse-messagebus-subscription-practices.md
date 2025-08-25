---
title: MessageBus subscription practices
description: 'When using MessageBus for network communication, follow these essential
  practices to ensure reliable message handling and prevent memory leaks:


  1. **Use consistent channel names** between subscribe and unsubscribe calls to avoid
  subscription leaks'
repository: discourse/discourse
label: Networking
language: Other
comments_count: 2
repository_stars: 44898
---

When using MessageBus for network communication, follow these essential practices to ensure reliable message handling and prevent memory leaks:

1. **Use consistent channel names** between subscribe and unsubscribe calls to avoid subscription leaks
2. **Include the third argument** when subscribing for better message bus practices
3. **Always pair subscriptions with unsubscriptions** in component lifecycle methods

Example of proper MessageBus usage:

```javascript
constructor() {
  super(...arguments);
  const settingName = this.setting.setting;
  
  if (this.canSubscribeToSettingsJobs) {
    // Use third argument for better practice
    this.messageBus.subscribe(`/site_setting/${settingName}/process`, this.onMessage, this);
  }
}

willDestroy() {
  super.willDestroy(...arguments);
  const settingName = this.setting.setting;
  
  if (this.canSubscribeToSettingsJobs) {
    // Ensure channel name matches subscription exactly
    this.messageBus.unsubscribe(`/site_setting/${settingName}/process`, this.onMessage);
  }
}
```

This prevents subscription leaks, improves message handling reliability, and follows MessageBus best practices for network communication management.