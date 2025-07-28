---
title: Provide contextual explanations
description: Documentation should explain not just what APIs and features do, but
  when, why, and how to use them. Provide sufficient context for developers to understand
  the purpose, appropriate use cases, and practical implementation details.
repository: electron/electron
label: Documentation
language: Markdown
comments_count: 12
repository_stars: 117644
---

Documentation should explain not just what APIs and features do, but when, why, and how to use them. Provide sufficient context for developers to understand the purpose, appropriate use cases, and practical implementation details.

Key practices:
- Explain the motivation and use cases for features ("Useful for showing splash screens that will be swapped for `WebContentsView`s when the content finishes loading")
- Clarify when features apply or are relevant ("for macOS 12.3 and below—the macOS operating systems which don't support the `ScreenCaptureKit` API")
- Provide complete usage examples that show realistic scenarios
- Explain relationships between related APIs when multiple options exist
- Use clear, unambiguous language that avoids confusion

Example of good contextual documentation:
```js
// Instead of just describing the API
win.webContents.on('paint', (event, dirty, image) => {
  // Handle paint event
})

// Provide context about different usage patterns
const win = new BrowserWindow({ 
  webPreferences: { 
    offscreen: true, 
    offscreenUseSharedTexture: true 
  } 
})

win.webContents.on('paint', async (e, dirty, image) => {
  if (e.texture) {
    // When using shared texture for better performance
    await handleTextureAsync(e.texture.textureInfo)
    e.texture.release() // Important: release when done
  } else {
    // When using traditional bitmap approach
    handleBitmap(image.getBitmap())
  }
})
```

This approach helps developers understand not just the mechanics of an API, but how to use it effectively in real applications.