---
title: defer authentication prompts
description: Defer mounting components that trigger authentication prompts (MFA, per-session
  authentication) until they are actually visible or needed by the user. This prevents
  multiple concurrent authentication requests that can cause failures due to hardware
  token limitations or daemon mutex conflicts.
repository: gravitational/teleport
label: Security
language: TSX
comments_count: 1
repository_stars: 19109
---

Defer mounting components that trigger authentication prompts (MFA, per-session authentication) until they are actually visible or needed by the user. This prevents multiple concurrent authentication requests that can cause failures due to hardware token limitations or daemon mutex conflicts.

Components requiring authentication should implement lazy loading patterns where authentication is only triggered when the component becomes visible or when the user actively interacts with it. This is particularly important for applications that restore multiple tabs or sessions on startup.

Example implementation:
```tsx
function renderDocuments(documentsService: DocumentsService) {
  return documentsService.getDocuments().map(doc => {
    const isActiveDoc = workspacesService.isDocumentActive(doc.uri);
    const { kind } = doc;
    
    // Only mount authentication-requiring components when visible
    switch (kind) {
      case 'doc.terminal':
      case 'doc.desktop_session':
        return (
          <MountOnVisible visible={isActiveDoc}>
            <MemoizedDocument doc={doc} visible={isActiveDoc} />
          </MountOnVisible>
        );
      default:
        return <MemoizedDocument doc={doc} visible={isActiveDoc} />;
    }
  });
}
```

This approach improves both security reliability and user experience by avoiding unnecessary authentication prompts and preventing authentication mechanism failures caused by concurrent requests.