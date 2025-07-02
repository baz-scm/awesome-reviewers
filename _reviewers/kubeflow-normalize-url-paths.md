---
title: Normalize URL paths
description: When handling URLs in web applications, consistently normalize path formats
  to prevent routing and service communication issues. This is especially important
  when working with services like Istio that expect specific URL formats (e.g., trailing
  slashes).
repository: kubeflow/kubeflow
label: Networking
language: Typescript
comments_count: 3
repository_stars: 15064
---

When handling URLs in web applications, consistently normalize path formats to prevent routing and service communication issues. This is especially important when working with services like Istio that expect specific URL formats (e.g., trailing slashes).

Key implementation practices:
1. Ensure URLs end with trailing slashes when required by services
2. Create utility functions to normalize URL paths before comparison
3. Document URL format requirements in code comments

Example:
```typescript
// Ensure trailing slash for service URLs that require it (e.g., Istio)
function normalizeServiceUrl(url: string): string {
  return url?.endsWith('/') ? url : url + '/';
}

// When comparing URLs, normalize paths first
function equalUrlPaths(firstUrl: string, secondUrl: string): boolean {
  // Handle sometimes missing '/' from URLs for consistent comparison
  const normalizedFirst = firstUrl?.endsWith('/') ? firstUrl : firstUrl + '/';
  const normalizedSecond = secondUrl?.endsWith('/') ? secondUrl : secondUrl + '/';
  return normalizedFirst === normalizedSecond;
}
```


[
  {
    "discussion_id": "1090491700",
    "pr_number": 6895,
    "pr_file": "components/centraldashboard-angular/frontend/cypress/support/commands.ts",
    "created_at": "2023-01-30T11:17:32+00:00",
    "commented_code": "/// <reference types=\"cypress\" />\n\nimport { equalUrlPaths, removePrefixFrom } from 'src/app/shared/utils';\n\nCypress.Commands.add('getIframeBody', () => {\n  cy.log('getIframeBody');\n  // Cypress yields jQuery element, which has the real\n  // DOM element under property \"0\".\n  // From the real DOM iframe element we can get\n  // the \"document\" element, it is stored in \"contentDocument\" property\n  // Cypress \"its\" command can access deep properties using dot notation\n  // https://on.cypress.io/its\n\n  // get the iframe > document > body\n  // and retry until the body element is not empty\n  return (\n    cy\n      .get('iframe', { log: false })\n      .its('0.contentDocument.body', { log: false })\n      .should('not.be.empty')\n      // wraps \"body\" DOM element to allow\n      // chaining more Cypress commands, like \".find(...)\"\n      // https://on.cypress.io/wrap\n      .then(body => cy.wrap(body, { log: false }))\n  );\n});\n\nCypress.Commands.add('getIframeUrl', () => {\n  cy.log('getIframeLocation');\n  cy.get('iframe', { log: false })\n    .its('0.contentWindow.location', { log: false })\n    .then(iframeLocation => {\n      let iframeUrl: string = iframeLocation.pathname + iframeLocation.search;\n      cy.wrap(iframeUrl, { log: false });\n    });\n});\n\nCypress.Commands.add('equalUrls', () => {\n  cy.log('equalUrls command');\n\n  let iframeUrl: string;\n\n  cy.getIframeUrl().then(url => {\n    iframeUrl = url;\n    cy.location({ log: false }).should(browserLocation => {\n      let browserUrl = browserLocation.pathname + browserLocation.search;\n      browserUrl = removePrefixFrom(browserUrl);\n\n      expect(equalUrlPaths(browserUrl, iframeUrl)).to.be.true;",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1090491700",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6895,
        "pr_file": "components/centraldashboard-angular/frontend/cypress/support/commands.ts",
        "discussion_id": "1090491700",
        "commented_code": "@@ -0,0 +1,91 @@\n+/// <reference types=\"cypress\" />\n+\n+import { equalUrlPaths, removePrefixFrom } from 'src/app/shared/utils';\n+\n+Cypress.Commands.add('getIframeBody', () => {\n+  cy.log('getIframeBody');\n+  // Cypress yields jQuery element, which has the real\n+  // DOM element under property \"0\".\n+  // From the real DOM iframe element we can get\n+  // the \"document\" element, it is stored in \"contentDocument\" property\n+  // Cypress \"its\" command can access deep properties using dot notation\n+  // https://on.cypress.io/its\n+\n+  // get the iframe > document > body\n+  // and retry until the body element is not empty\n+  return (\n+    cy\n+      .get('iframe', { log: false })\n+      .its('0.contentDocument.body', { log: false })\n+      .should('not.be.empty')\n+      // wraps \"body\" DOM element to allow\n+      // chaining more Cypress commands, like \".find(...)\"\n+      // https://on.cypress.io/wrap\n+      .then(body => cy.wrap(body, { log: false }))\n+  );\n+});\n+\n+Cypress.Commands.add('getIframeUrl', () => {\n+  cy.log('getIframeLocation');\n+  cy.get('iframe', { log: false })\n+    .its('0.contentWindow.location', { log: false })\n+    .then(iframeLocation => {\n+      let iframeUrl: string = iframeLocation.pathname + iframeLocation.search;\n+      cy.wrap(iframeUrl, { log: false });\n+    });\n+});\n+\n+Cypress.Commands.add('equalUrls', () => {\n+  cy.log('equalUrls command');\n+\n+  let iframeUrl: string;\n+\n+  cy.getIframeUrl().then(url => {\n+    iframeUrl = url;\n+    cy.location({ log: false }).should(browserLocation => {\n+      let browserUrl = browserLocation.pathname + browserLocation.search;\n+      browserUrl = removePrefixFrom(browserUrl);\n+\n+      expect(equalUrlPaths(browserUrl, iframeUrl)).to.be.true;",
        "comment_created_at": "2023-01-30T11:17:32+00:00",
        "comment_author": "tasos-ale",
        "comment_body": "```suggestion\r\n  cy.getIframeUrl().then(url => {\r\n    cy.location({ log: false }).should(browserLocation => {\r\n      let browserUrl = browserLocation.pathname + browserLocation.search;\r\n      browserUrl = removePrefixFrom(browserUrl);\\\r\n      expect(equalUrlPaths(browserUrl, url)).to.be.true;\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1065779821",
    "pr_number": 6856,
    "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/iframe-wrapper/iframe-wrapper.component.ts",
    "created_at": "2023-01-10T13:23:29+00:00",
    "commented_code": "import {\n  AfterViewInit,\n  Component,\n  ElementRef,\n  OnDestroy,\n  ViewChild,\n} from '@angular/core';\nimport { NavigationEnd, Router } from '@angular/router';\nimport { Subscription } from 'rxjs';\n\n@Component({\n  selector: 'app-iframe-wrapper',\n  templateUrl: './iframe-wrapper.component.html',\n  styleUrls: ['./iframe-wrapper.component.scss'],\n})\nexport class IframeWrapperComponent implements AfterViewInit, OnDestroy {\n  @ViewChild('iframe') iframe: ElementRef<HTMLIFrameElement>;\n\n  public prvSrcPath: string;\n  get srcPath(): string {\n    return this.prvSrcPath;\n  }\n  set srcPath(src: string) {\n    /*\n     * The following hacky logic ensures that the Iframe will reload,\n     * even when it receives values for src that are the same with the\n     * one it already has. This is because, in order to avoid the iframe\n     * reloading constantly, its src is not updated on each navigation\n     * a user does.\n     */\n    if (window.location.origin) {\n      if (!this.prvSrcPath?.includes(window.location.origin)) {\n        src = window.location.origin + src;\n      }\n    }\n\n    this.prvSrcPath = src;\n    // Some KF distributions need a trailing slash \"/\" in order to resolve paths",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1065779821",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6856,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/iframe-wrapper/iframe-wrapper.component.ts",
        "discussion_id": "1065779821",
        "commented_code": "@@ -0,0 +1,121 @@\n+import {\n+  AfterViewInit,\n+  Component,\n+  ElementRef,\n+  OnDestroy,\n+  ViewChild,\n+} from '@angular/core';\n+import { NavigationEnd, Router } from '@angular/router';\n+import { Subscription } from 'rxjs';\n+\n+@Component({\n+  selector: 'app-iframe-wrapper',\n+  templateUrl: './iframe-wrapper.component.html',\n+  styleUrls: ['./iframe-wrapper.component.scss'],\n+})\n+export class IframeWrapperComponent implements AfterViewInit, OnDestroy {\n+  @ViewChild('iframe') iframe: ElementRef<HTMLIFrameElement>;\n+\n+  public prvSrcPath: string;\n+  get srcPath(): string {\n+    return this.prvSrcPath;\n+  }\n+  set srcPath(src: string) {\n+    /*\n+     * The following hacky logic ensures that the Iframe will reload,\n+     * even when it receives values for src that are the same with the\n+     * one it already has. This is because, in order to avoid the iframe\n+     * reloading constantly, its src is not updated on each navigation\n+     * a user does.\n+     */\n+    if (window.location.origin) {\n+      if (!this.prvSrcPath?.includes(window.location.origin)) {\n+        src = window.location.origin + src;\n+      }\n+    }\n+\n+    this.prvSrcPath = src;\n+    // Some KF distributions need a trailing slash \"/\" in order to resolve paths",
        "comment_created_at": "2023-01-10T13:23:29+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's rephrase this to something like the following:\r\n\r\nWhen Istio exports Services it always expects a `/` at the end. SO we'll need to make sure the links propagated to the iframe end with a `/`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1065862401",
    "pr_number": 6856,
    "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/iframe-wrapper/iframe-wrapper.component.ts",
    "created_at": "2023-01-10T14:37:43+00:00",
    "commented_code": "import {\n  AfterViewInit,\n  Component,\n  ElementRef,\n  OnDestroy,\n  ViewChild,\n} from '@angular/core';\nimport { NavigationEnd, Router } from '@angular/router';\nimport { Subscription } from 'rxjs';\n\n@Component({\n  selector: 'app-iframe-wrapper',\n  templateUrl: './iframe-wrapper.component.html',\n  styleUrls: ['./iframe-wrapper.component.scss'],\n})\nexport class IframeWrapperComponent implements AfterViewInit, OnDestroy {\n  @ViewChild('iframe') iframe: ElementRef<HTMLIFrameElement>;\n\n  public prvSrcPath: string;\n  get srcPath(): string {\n    return this.prvSrcPath;\n  }\n  set srcPath(src: string) {\n    /*\n     * The following hacky logic ensures that the Iframe will reload,\n     * even when it receives values for src that are the same with the\n     * one it already has. This is because, in order to avoid the iframe\n     * reloading constantly, its src is not updated on each navigation\n     * a user does.\n     */\n    if (window.location.origin) {\n      if (!this.prvSrcPath?.includes(window.location.origin)) {\n        src = window.location.origin + src;\n      }\n    }\n\n    this.prvSrcPath = src;\n    // Some KF distributions need a trailing slash \"/\" in order to resolve paths\n    this.prvSrcPath += this.prvSrcPath?.endsWith('/') ? '' : '/';\n  }\n  public iframeLocation: string | undefined = 'about:blank';\n  private urlSub: Subscription;\n  private interval: any;\n\n  constructor(private router: Router) {\n    this.urlSub = this.router.events.subscribe(event => {\n      if (!(event instanceof NavigationEnd)) {\n        return;\n      }\n\n      const iframeWindow = this.iframe?.nativeElement?.contentWindow;\n      let iframeUrl = iframeWindow?.location.pathname;\n      if (iframeUrl) {\n        // Include URL's query parameters\n        iframeUrl += iframeWindow?.location.search;\n      }\n\n      if (!this.equalUrlPaths(event.url, iframeUrl)) {\n        this.srcPath = event.url;\n      }\n    });\n  }\n\n  equalUrlPaths(firstUrl: string, secondUrl: string | undefined) {\n    if (!firstUrl && !secondUrl) {",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1065862401",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6856,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/iframe-wrapper/iframe-wrapper.component.ts",
        "discussion_id": "1065862401",
        "commented_code": "@@ -0,0 +1,121 @@\n+import {\n+  AfterViewInit,\n+  Component,\n+  ElementRef,\n+  OnDestroy,\n+  ViewChild,\n+} from '@angular/core';\n+import { NavigationEnd, Router } from '@angular/router';\n+import { Subscription } from 'rxjs';\n+\n+@Component({\n+  selector: 'app-iframe-wrapper',\n+  templateUrl: './iframe-wrapper.component.html',\n+  styleUrls: ['./iframe-wrapper.component.scss'],\n+})\n+export class IframeWrapperComponent implements AfterViewInit, OnDestroy {\n+  @ViewChild('iframe') iframe: ElementRef<HTMLIFrameElement>;\n+\n+  public prvSrcPath: string;\n+  get srcPath(): string {\n+    return this.prvSrcPath;\n+  }\n+  set srcPath(src: string) {\n+    /*\n+     * The following hacky logic ensures that the Iframe will reload,\n+     * even when it receives values for src that are the same with the\n+     * one it already has. This is because, in order to avoid the iframe\n+     * reloading constantly, its src is not updated on each navigation\n+     * a user does.\n+     */\n+    if (window.location.origin) {\n+      if (!this.prvSrcPath?.includes(window.location.origin)) {\n+        src = window.location.origin + src;\n+      }\n+    }\n+\n+    this.prvSrcPath = src;\n+    // Some KF distributions need a trailing slash \"/\" in order to resolve paths\n+    this.prvSrcPath += this.prvSrcPath?.endsWith('/') ? '' : '/';\n+  }\n+  public iframeLocation: string | undefined = 'about:blank';\n+  private urlSub: Subscription;\n+  private interval: any;\n+\n+  constructor(private router: Router) {\n+    this.urlSub = this.router.events.subscribe(event => {\n+      if (!(event instanceof NavigationEnd)) {\n+        return;\n+      }\n+\n+      const iframeWindow = this.iframe?.nativeElement?.contentWindow;\n+      let iframeUrl = iframeWindow?.location.pathname;\n+      if (iframeUrl) {\n+        // Include URL's query parameters\n+        iframeUrl += iframeWindow?.location.search;\n+      }\n+\n+      if (!this.equalUrlPaths(event.url, iframeUrl)) {\n+        this.srcPath = event.url;\n+      }\n+    });\n+  }\n+\n+  equalUrlPaths(firstUrl: string, secondUrl: string | undefined) {\n+    if (!firstUrl && !secondUrl) {",
        "comment_created_at": "2023-01-10T14:37:43+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's add a comment here to explain why we need this function, which is to handle the sometimes missing `/` from some urls",
        "pr_file_module": null
      }
    ]
  }
]
