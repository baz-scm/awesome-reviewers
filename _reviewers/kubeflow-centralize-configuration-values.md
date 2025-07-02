---
title: Centralize configuration values
description: Store all configuration values in dedicated configuration files rather
  than hardcoding them throughout the application. This makes the codebase more maintainable
  and reduces the need for code changes when configurations change.
repository: kubeflow/kubeflow
label: Configurations
language: Typescript
comments_count: 5
repository_stars: 15064
---

Store all configuration values in dedicated configuration files rather than hardcoding them throughout the application. This makes the codebase more maintainable and reduces the need for code changes when configurations change.

Key practices:
- Use environment files to store configuration values
- Move hardcoded patterns, URLs, and paths to configuration constants
- Design configuration with future extensibility in mind
- Use environment variables for feature toggles and configurable behavior

**Example - Before:**
```typescript
constructor(private translate: TranslateService) {
  const currentLanguage = this.translate.getBrowserLang();
  const lang = currentLanguage.match(/en|fr/) ? currentLanguage : 'en';
}

constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
  iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));
}
```

**Example - After:**
```typescript
// In environment.ts
export const environment = {
  supportedLanguages: ['en', 'fr'],
  defaultLanguage: 'en',
  assetPaths: {
    jupyterlab: 'static/assets/jupyterlab-wordmark.svg',
  }
};

// In component
constructor(private translate: TranslateService) {
  const currentLanguage = this.translate.getBrowserLang();
  const lang = environment.supportedLanguages.includes(currentLanguage) ? 
    currentLanguage : environment.defaultLanguage;
}

constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
  iconRegistry.addSvgIcon(
    'jupyterlab', 
    sanitizer.bypassSecurityTrustResourceUrl(environment.assetPaths.jupyterlab)
  );
}
```

This approach makes it easier to add new languages or assets without modifying component code, and keeps configuration organized in central locations.


[
  {
    "discussion_id": "651645749",
    "pr_number": 5880,
    "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/app.component.ts",
    "created_at": "2021-06-15T10:08:27+00:00",
    "commented_code": "import { Component } from '@angular/core';\nimport { TranslateService } from '@ngx-translate/core';\n\n@Component({\n  selector: 'app-root',\n  templateUrl: './app.component.html',\n  styleUrls: ['./app.component.scss'],\n})\nexport class AppComponent {\n  constructor(private translate: TranslateService) {\n    const currentLanguage = this.translate.getBrowserLang();\n    const lang = currentLanguage.match(/en|fr/) ? currentLanguage : 'en';",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "651645749",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5880,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/app.component.ts",
        "discussion_id": "651645749",
        "commented_code": "@@ -1,10 +1,16 @@\n import { Component } from '@angular/core';\n+import { TranslateService } from '@ngx-translate/core';\n \n @Component({\n   selector: 'app-root',\n   templateUrl: './app.component.html',\n   styleUrls: ['./app.component.scss'],\n })\n export class AppComponent {\n+  constructor(private translate: TranslateService) {\n+    const currentLanguage = this.translate.getBrowserLang();\n+    const lang = currentLanguage.match(/en|fr/) ? currentLanguage : 'en';",
        "comment_created_at": "2021-06-15T10:08:27+00:00",
        "comment_author": "davidspek",
        "comment_body": "Will new languages need to be added to the `currentLanguage.match(/en|fr/)` section once the JSON files are added?",
        "pr_file_module": null
      },
      {
        "comment_id": "651832266",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5880,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/app.component.ts",
        "discussion_id": "651645749",
        "commented_code": "@@ -1,10 +1,16 @@\n import { Component } from '@angular/core';\n+import { TranslateService } from '@ngx-translate/core';\n \n @Component({\n   selector: 'app-root',\n   templateUrl: './app.component.html',\n   styleUrls: ['./app.component.scss'],\n })\n export class AppComponent {\n+  constructor(private translate: TranslateService) {\n+    const currentLanguage = this.translate.getBrowserLang();\n+    const lang = currentLanguage.match(/en|fr/) ? currentLanguage : 'en';",
        "comment_created_at": "2021-06-15T14:12:05+00:00",
        "comment_author": "Jose-Matsuda",
        "comment_body": "That is correct. Once a language's JSON file is added the corresponding `app.component.ts` will need to be updated as well",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "596260211",
    "pr_number": 5646,
    "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
    "created_at": "2021-03-17T17:57:25+00:00",
    "commented_code": "export class FormImageComponent implements OnInit, OnDestroy {\n  @Input() parentForm: FormGroup;\n  @Input() images: string[];\n  @Input() readonly: boolean;\n  @Input() jupyterReadonly: boolean;\n  @Input() imagesVSCode: string[];\n  @Input() vscodeReadonly: boolean;\n  @Input() imagesRStudio: string[];\n  @Input() rstudioReadonly: boolean;\n\n  subs = new Subscription();\n\n  constructor() {}\n  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "596260211",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
        "discussion_id": "596260211",
        "commented_code": "@@ -10,11 +12,19 @@ import { Subscription } from 'rxjs';\n export class FormImageComponent implements OnInit, OnDestroy {\n   @Input() parentForm: FormGroup;\n   @Input() images: string[];\n-  @Input() readonly: boolean;\n+  @Input() jupyterReadonly: boolean;\n+  @Input() imagesVSCode: string[];\n+  @Input() vscodeReadonly: boolean;\n+  @Input() imagesRStudio: string[];\n+  @Input() rstudioReadonly: boolean;\n \n   subs = new Subscription();\n \n-  constructor() {}\n+  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n+    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
        "comment_created_at": "2021-03-17T17:57:25+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Could you add the urls for the icons into the environment files instead? https://github.com/kubeflow/kubeflow/tree/master/components/crud-web-apps/jupyter/frontend/src/environments\r\n\r\nLets keep these links in a central place, where we might also add other links in the future like the svgs for the main page",
        "pr_file_module": null
      },
      {
        "comment_id": "597052809",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
        "discussion_id": "596260211",
        "commented_code": "@@ -10,11 +12,19 @@ import { Subscription } from 'rxjs';\n export class FormImageComponent implements OnInit, OnDestroy {\n   @Input() parentForm: FormGroup;\n   @Input() images: string[];\n-  @Input() readonly: boolean;\n+  @Input() jupyterReadonly: boolean;\n+  @Input() imagesVSCode: string[];\n+  @Input() vscodeReadonly: boolean;\n+  @Input() imagesRStudio: string[];\n+  @Input() rstudioReadonly: boolean;\n \n   subs = new Subscription();\n \n-  constructor() {}\n+  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n+    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
        "comment_created_at": "2021-03-18T16:37:25+00:00",
        "comment_author": "davidspek",
        "comment_body": "Just to be clear from what was discussed above, should the URL in the environment be were the SVG is hosted publicly, or should that first be downloaded by the backend and placed in the `static/assets/` directory, or have we decided to just add the SVGs in the static folder by default? Using the public URL directly means I'll need to deal with CORS. ",
        "pr_file_module": null
      },
      {
        "comment_id": "597147456",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
        "discussion_id": "596260211",
        "commented_code": "@@ -10,11 +12,19 @@ import { Subscription } from 'rxjs';\n export class FormImageComponent implements OnInit, OnDestroy {\n   @Input() parentForm: FormGroup;\n   @Input() images: string[];\n-  @Input() readonly: boolean;\n+  @Input() jupyterReadonly: boolean;\n+  @Input() imagesVSCode: string[];\n+  @Input() vscodeReadonly: boolean;\n+  @Input() imagesRStudio: string[];\n+  @Input() rstudioReadonly: boolean;\n \n   subs = new Subscription();\n \n-  constructor() {}\n+  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n+    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
        "comment_created_at": "2021-03-18T18:42:36+00:00",
        "comment_author": "davidspek",
        "comment_body": "@kimwnasptd Friendly ping on this in case you missed it, so I know what steps I need to take to get this resolved. ",
        "pr_file_module": null
      },
      {
        "comment_id": "597157251",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
        "discussion_id": "596260211",
        "commented_code": "@@ -10,11 +12,19 @@ import { Subscription } from 'rxjs';\n export class FormImageComponent implements OnInit, OnDestroy {\n   @Input() parentForm: FormGroup;\n   @Input() images: string[];\n-  @Input() readonly: boolean;\n+  @Input() jupyterReadonly: boolean;\n+  @Input() imagesVSCode: string[];\n+  @Input() vscodeReadonly: boolean;\n+  @Input() imagesRStudio: string[];\n+  @Input() rstudioReadonly: boolean;\n \n   subs = new Subscription();\n \n-  constructor() {}\n+  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n+    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
        "comment_created_at": "2021-03-18T18:57:18+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Thanks for the ping! \r\n\r\nGood catch on the CORS issue. Lets dump the SVGs in the `static/assets` folder. And also define the links that the frontend will use in the `environment` files as mentioned above.",
        "pr_file_module": null
      },
      {
        "comment_id": "597174913",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.ts",
        "discussion_id": "596260211",
        "commented_code": "@@ -10,11 +12,19 @@ import { Subscription } from 'rxjs';\n export class FormImageComponent implements OnInit, OnDestroy {\n   @Input() parentForm: FormGroup;\n   @Input() images: string[];\n-  @Input() readonly: boolean;\n+  @Input() jupyterReadonly: boolean;\n+  @Input() imagesVSCode: string[];\n+  @Input() vscodeReadonly: boolean;\n+  @Input() imagesRStudio: string[];\n+  @Input() rstudioReadonly: boolean;\n \n   subs = new Subscription();\n \n-  constructor() {}\n+  constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {\n+    iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));",
        "comment_created_at": "2021-03-18T19:23:55+00:00",
        "comment_author": "davidspek",
        "comment_body": "Cool! This shouldn't take long to implement then.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "306063156",
    "pr_number": 3599,
    "pr_file": "components/gcp-click-to-deploy/src/Utils.ts",
    "created_at": "2019-07-22T22:42:07+00:00",
    "commented_code": "import * as bcrypt from 'bcryptjs';\n\nconst GITHUB_BASE_URL =\n    'https://raw.githubusercontent.com/kubeflow/kubeflow/master/';",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "306063156",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 3599,
        "pr_file": "components/gcp-click-to-deploy/src/Utils.ts",
        "discussion_id": "306063156",
        "commented_code": "@@ -1,5 +1,8 @@\n import * as bcrypt from 'bcryptjs';\n \n+const GITHUB_BASE_URL =\n+    'https://raw.githubusercontent.com/kubeflow/kubeflow/master/';\n+",
        "comment_created_at": "2019-07-22T22:42:07+00:00",
        "comment_author": "kunmingg",
        "comment_body": "Config file on kubeflow master (or other branch) might not compatible with kfctl backend.\r\nShall we bake v0.5 & v0.6 config files into image during build?   ",
        "pr_file_module": null
      },
      {
        "comment_id": "306085992",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 3599,
        "pr_file": "components/gcp-click-to-deploy/src/Utils.ts",
        "discussion_id": "306063156",
        "commented_code": "@@ -1,5 +1,8 @@\n import * as bcrypt from 'bcryptjs';\n \n+const GITHUB_BASE_URL =\n+    'https://raw.githubusercontent.com/kubeflow/kubeflow/master/';\n+",
        "comment_created_at": "2019-07-23T00:28:03+00:00",
        "comment_author": "prodonjs",
        "comment_body": "Currently, that's how it's done for the 0.5.0 compatible deployment but Jeremy had a comment to try to fetch it from GitHub. Pulling from master is probably problematic but we can easily point to a branch for each version to ensure that we get a consistent file that should be compatible with the version in question.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1746876292",
    "pr_number": 7639,
    "pr_file": "components/centraldashboard/app/server.ts",
    "created_at": "2024-09-06T10:07:03+00:00",
    "commented_code": "REGISTRATION_FLOW = \"true\",\n  PROMETHEUS_URL = undefined,\n  METRICS_DASHBOARD = undefined,\n  METRICS_PORT = 9100,",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1746876292",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7639,
        "pr_file": "components/centraldashboard/app/server.ts",
        "discussion_id": "1746876292",
        "commented_code": "@@ -33,6 +39,7 @@ const {\n   REGISTRATION_FLOW = \"true\",\n   PROMETHEUS_URL = undefined,\n   METRICS_DASHBOARD = undefined,\n+  METRICS_PORT = 9100,",
        "comment_created_at": "2024-09-06T10:07:03+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "Should we expose this also in the [Dockerfile](https://github.com/rgildein/kubeflow/blob/94995d6a519183fc19a25ba36a5f23cd6b78f681/components/centraldashboard/Dockerfile#L30-L31)?",
        "pr_file_module": null
      },
      {
        "comment_id": "1746910272",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7639,
        "pr_file": "components/centraldashboard/app/server.ts",
        "discussion_id": "1746876292",
        "commented_code": "@@ -33,6 +39,7 @@ const {\n   REGISTRATION_FLOW = \"true\",\n   PROMETHEUS_URL = undefined,\n   METRICS_DASHBOARD = undefined,\n+  METRICS_PORT = 9100,",
        "comment_created_at": "2024-09-06T10:35:09+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "and probably manifests too?\r\nhttps://github.com/kubeflow/kubeflow/blob/54201e3d28e4673d465e47e464e86aa698ca0dfa/components/centraldashboard/manifests/base/deployment.yaml#L29-L31\r\nhttps://github.com/kubeflow/kubeflow/blob/master/components/centraldashboard/manifests/base/service.yaml#L9-L11",
        "pr_file_module": null
      },
      {
        "comment_id": "1746930746",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7639,
        "pr_file": "components/centraldashboard/app/server.ts",
        "discussion_id": "1746876292",
        "commented_code": "@@ -33,6 +39,7 @@ const {\n   REGISTRATION_FLOW = \"true\",\n   PROMETHEUS_URL = undefined,\n   METRICS_DASHBOARD = undefined,\n+  METRICS_PORT = 9100,",
        "comment_created_at": "2024-09-06T10:55:37+00:00",
        "comment_author": "rgildein",
        "comment_body": "What do you say if we change this to be only `METRICS`, which will enable or disable the metrics and port will be always 9100? I don't think there is much need to change the port, but we can use both `METRICS` and `METRICS PORT`. WDYT?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1746905300",
    "pr_number": 7639,
    "pr_file": "components/centraldashboard/app/server.ts",
    "created_at": "2024-09-06T10:30:11+00:00",
    "commented_code": "console.info(`Using Profiles service at ${profilesServiceUrl}`);\n  const profilesService = new DefaultApi(profilesServiceUrl);\n  const metricsPort: number = Number(METRICS_PORT);\n\n  // Custom metrics configuration\n  app.use(\n    responseTime((req: Request, res: Response, time: number) => {\n      restHttpRequestTotal.labels({ method: req.method, status: res.statusCode }).inc();\n      restHttpRequestDuration.labels(\n        { method: req.method, path: req.baseUrl, status: res.statusCode }).observe(time);\n    }),\n  );",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1746905300",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7639,
        "pr_file": "components/centraldashboard/app/server.ts",
        "discussion_id": "1746905300",
        "commented_code": "@@ -52,6 +59,16 @@ async function main() {\n \n   console.info(`Using Profiles service at ${profilesServiceUrl}`);\n   const profilesService = new DefaultApi(profilesServiceUrl);\n+  const metricsPort: number = Number(METRICS_PORT);\n+\n+  // Custom metrics configuration\n+  app.use(\n+    responseTime((req: Request, res: Response, time: number) => {\n+      restHttpRequestTotal.labels({ method: req.method, status: res.statusCode }).inc();\n+      restHttpRequestDuration.labels(\n+        { method: req.method, path: req.baseUrl, status: res.statusCode }).observe(time);\n+    }),\n+  );",
        "comment_created_at": "2024-09-06T10:30:11+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "Would it make sense to enable/disable the feature according to env variables, similar to the crud-web-apps? And then add the required environment variable in this deployment",
        "pr_file_module": null
      }
    ]
  }
]
