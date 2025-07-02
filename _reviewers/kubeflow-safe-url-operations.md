---
title: Safe URL operations
description: 'When handling URLs for API interactions and navigation, use precise
  methods for both comparison and construction to avoid subtle bugs:


  1. For URL path comparison, use `startsWith()` instead of `includes()` to prevent
  false positives from substring matches:'
repository: kubeflow/kubeflow
label: API
language: Typescript
comments_count: 2
repository_stars: 15064
---

When handling URLs for API interactions and navigation, use precise methods for both comparison and construction to avoid subtle bugs:

1. For URL path comparison, use `startsWith()` instead of `includes()` to prevent false positives from substring matches:

```typescript
// AVOID: May lead to incorrect matches
return browserUrl.includes(url);

// BETTER: More precise path matching
return browserUrl.startsWith(url);
```

2. When constructing URLs, use the URL constructor with proper base parameter rather than manual string concatenation:

```typescript
// AVOID: Potential issues with relative paths
const href = window.location.origin + url;
const urlObject = new URL(href);

// BETTER: Robust URL construction
const urlObject = new URL(url, window.location.origin);
```

These practices ensure reliable API interactions and prevent navigation edge cases when handling routes and endpoints.


[
  {
    "discussion_id": "1116709963",
    "pr_number": 6953,
    "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/main-page/main-page.component.ts",
    "created_at": "2023-02-24T09:20:02+00:00",
    "commented_code": "computeBuildValue(label: string, buildValue: string): string {\n    return `${label} ${buildValue}`;\n  }\n\n  handleDashboardLinks(links: DashboardLinks) {\n    const { menuLinks, externalLinks, quickLinks, documentationItems } = links;\n    this.menuLinks = menuLinks || [];\n    this.externalLinks = externalLinks || [];\n    this.quickLinks = quickLinks || [];\n    this.documentationItems = documentationItems || [];\n  }\n\n  getUrlPath(url: string) {\n    const urlWithoutFragment = url.split('#')[0];\n    return this.appendPrefix(urlWithoutFragment);\n  }\n\n  getUrlFragment(url: string): string {\n    const fragment = url.split('#')[1];\n    return fragment;\n  }\n\n  appendPrefix(url: string): string {\n    return '/_' + url;\n  }\n\n  isLinkActive(url: string): boolean {\n    let browserUrl = this.router.url;\n    browserUrl = appendBackslash(browserUrl);\n    url = appendBackslash(url);\n    /**\n     * We need this condition because Pipelines Web App removes\n     * the 's' from its path when navigating inside a Recurring\n     * Run's details page\n     */\n    if (\n      browserUrl.includes('pipeline/#/recurringrun') &&\n      url.includes('/pipeline/#/recurringruns')\n    ) {\n      return true;\n    }\n\n    return browserUrl.includes(url);",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1116709963",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6953,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/main-page/main-page.component.ts",
        "discussion_id": "1116709963",
        "commented_code": "@@ -63,4 +83,45 @@ export class MainPageComponent implements OnInit, OnDestroy {\n   computeBuildValue(label: string, buildValue: string): string {\n     return `${label} ${buildValue}`;\n   }\n+\n+  handleDashboardLinks(links: DashboardLinks) {\n+    const { menuLinks, externalLinks, quickLinks, documentationItems } = links;\n+    this.menuLinks = menuLinks || [];\n+    this.externalLinks = externalLinks || [];\n+    this.quickLinks = quickLinks || [];\n+    this.documentationItems = documentationItems || [];\n+  }\n+\n+  getUrlPath(url: string) {\n+    const urlWithoutFragment = url.split('#')[0];\n+    return this.appendPrefix(urlWithoutFragment);\n+  }\n+\n+  getUrlFragment(url: string): string {\n+    const fragment = url.split('#')[1];\n+    return fragment;\n+  }\n+\n+  appendPrefix(url: string): string {\n+    return '/_' + url;\n+  }\n+\n+  isLinkActive(url: string): boolean {\n+    let browserUrl = this.router.url;\n+    browserUrl = appendBackslash(browserUrl);\n+    url = appendBackslash(url);\n+    /**\n+     * We need this condition because Pipelines Web App removes\n+     * the 's' from its path when navigating inside a Recurring\n+     * Run's details page\n+     */\n+    if (\n+      browserUrl.includes('pipeline/#/recurringrun') &&\n+      url.includes('/pipeline/#/recurringruns')\n+    ) {\n+      return true;\n+    }\n+\n+    return browserUrl.includes(url);",
        "comment_created_at": "2023-02-24T09:20:02+00:00",
        "comment_author": "tasos-ale",
        "comment_body": "It works, but it will be safer to use `startsWith()` in case we end up with a `url` inside the `browserUrl` that we don't want to match ",
        "pr_file_module": null
      },
      {
        "comment_id": "1117244598",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6953,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/main-page/main-page.component.ts",
        "discussion_id": "1116709963",
        "commented_code": "@@ -63,4 +83,45 @@ export class MainPageComponent implements OnInit, OnDestroy {\n   computeBuildValue(label: string, buildValue: string): string {\n     return `${label} ${buildValue}`;\n   }\n+\n+  handleDashboardLinks(links: DashboardLinks) {\n+    const { menuLinks, externalLinks, quickLinks, documentationItems } = links;\n+    this.menuLinks = menuLinks || [];\n+    this.externalLinks = externalLinks || [];\n+    this.quickLinks = quickLinks || [];\n+    this.documentationItems = documentationItems || [];\n+  }\n+\n+  getUrlPath(url: string) {\n+    const urlWithoutFragment = url.split('#')[0];\n+    return this.appendPrefix(urlWithoutFragment);\n+  }\n+\n+  getUrlFragment(url: string): string {\n+    const fragment = url.split('#')[1];\n+    return fragment;\n+  }\n+\n+  appendPrefix(url: string): string {\n+    return '/_' + url;\n+  }\n+\n+  isLinkActive(url: string): boolean {\n+    let browserUrl = this.router.url;\n+    browserUrl = appendBackslash(browserUrl);\n+    url = appendBackslash(url);\n+    /**\n+     * We need this condition because Pipelines Web App removes\n+     * the 's' from its path when navigating inside a Recurring\n+     * Run's details page\n+     */\n+    if (\n+      browserUrl.includes('pipeline/#/recurringrun') &&\n+      url.includes('/pipeline/#/recurringruns')\n+    ) {\n+      return true;\n+    }\n+\n+    return browserUrl.includes(url);",
        "comment_created_at": "2023-02-24T16:08:55+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "Sure, I removed the prefix from browser's URL and changed that to `startsWith()`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1090461801",
    "pr_number": 6895,
    "pr_file": "components/centraldashboard-angular/frontend/src/app/shared/utils.ts",
    "created_at": "2023-01-30T10:51:33+00:00",
    "commented_code": "/**\n * We treat URLs with or without a trailing slash as the same\n * URL. Thus, in order to compare URLs, we need to use\n * appendBackslash for both URLS to avoid false statements\n * in cases where they only differ in the trailing slash.\n */\nexport function equalUrlPaths(firstUrl: string, secondUrl: string | undefined) {\n  if (!firstUrl && !secondUrl) {\n    console.warn(`Got undefined URLs ${firstUrl} and ${secondUrl}`);\n    return true;\n  }\n  if (!firstUrl || !secondUrl) {\n    return false;\n  }\n  firstUrl = appendBackslash(firstUrl);\n  secondUrl = appendBackslash(secondUrl);\n  return firstUrl === secondUrl;\n}\n\n/**\n * Appends a trailing slash either at the end of the URL\n * or at the end of path, just before query parameters\n */\nexport function appendBackslash(url: string): string {\n  const href = window.location.origin + url;\n  const urlObject = new URL(href);",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1090461801",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6895,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/shared/utils.ts",
        "discussion_id": "1090461801",
        "commented_code": "@@ -0,0 +1,37 @@\n+/**\n+ * We treat URLs with or without a trailing slash as the same\n+ * URL. Thus, in order to compare URLs, we need to use\n+ * appendBackslash for both URLS to avoid false statements\n+ * in cases where they only differ in the trailing slash.\n+ */\n+export function equalUrlPaths(firstUrl: string, secondUrl: string | undefined) {\n+  if (!firstUrl && !secondUrl) {\n+    console.warn(`Got undefined URLs ${firstUrl} and ${secondUrl}`);\n+    return true;\n+  }\n+  if (!firstUrl || !secondUrl) {\n+    return false;\n+  }\n+  firstUrl = appendBackslash(firstUrl);\n+  secondUrl = appendBackslash(secondUrl);\n+  return firstUrl === secondUrl;\n+}\n+\n+/**\n+ * Appends a trailing slash either at the end of the URL\n+ * or at the end of path, just before query parameters\n+ */\n+export function appendBackslash(url: string): string {\n+  const href = window.location.origin + url;\n+  const urlObject = new URL(href);",
        "comment_created_at": "2023-01-30T10:51:33+00:00",
        "comment_author": "tasos-ale",
        "comment_body": "We can make that change in case `url` does not start with `/`.\r\n```suggestion\r\n  const urlObject = new URL(url, window.location.origin);\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
