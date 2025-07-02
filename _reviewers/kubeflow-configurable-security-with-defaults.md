---
title: Configurable security with defaults
description: Make security features configurable through environment variables or
  configuration files, but always implement secure defaults. This allows teams to
  adapt security controls to their specific deployment environments while maintaining
  a secure baseline.
repository: kubeflow/kubeflow
label: Security
language: Python
comments_count: 1
repository_stars: 15064
---

Make security features configurable through environment variables or configuration files, but always implement secure defaults. This allows teams to adapt security controls to their specific deployment environments while maintaining a secure baseline.

When implementing configurable security features:
1. Use secure default values that prioritize security (e.g., "Strict" for SameSite cookies)
2. Validate input configurations and fallback to secure defaults when invalid
3. Document all security configurations and their implications

Example from CSRF implementation:
```python
# Read SameSite configuration from environment with secure default
samesite = os.environ.get("CSRF_SAMESITE", "Strict")

# Validate the input to ensure only secure options are accepted
if samesite not in ["Strict", "Lax", "None"]:
    samesite = "Strict"  # Fallback to secure default

# Apply the configuration to the cookie
response.set_cookie(
    "CSRF_COOKIE", 
    csrf_token,
    httponly=True,
    secure=True,
    samesite=samesite
)
```

Document this configuration in your README:
```markdown
## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| CSRF_SAMESITE | SameSite attribute for CSRF cookies (Strict, Lax, None) | Strict |
```

This approach balances security with flexibility, allowing secure operation in various environments while maintaining strong defaults.


[
  {
    "discussion_id": "547897084",
    "pr_number": 5472,
    "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
    "created_at": "2020-12-23T10:49:30+00:00",
    "commented_code": "\"\"\"\nCross Site Request Forgery Blueprint.\n\nThis module provides a Flask blueprint that implements protection against\nrequest forgeries from other sites. Currently, it is only meant to be used with\nan AJAX frontend, not with server-side rendered forms.\n\nThe module implements the following protecting measures against CSRF:\n- Double Submit Cookie.\n- Custom HTTP Headers.\n- SameSite cookie attribute.\n\nTo elaborate, the `Double Submit Cookie` procedure looks like the following:\n1. Browser requests `index.html`, which contains the compiled Javascript.\n2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n   already exists, `set_cookie` overrides it with a new one. The cookie\n   contains a random value.\n3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n   `CSRF_HEADER` with the same value.\n4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n\nCustom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\ncross-origin requests cannot include custom headers (assuming CORS is not\nmisconfigured) because of the Same-Origin policy.\n\nThe SameSite cookie attribute provides another layer of protection, but may\nimpede usability so it is configurable. This attribute controls whether a",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "547897084",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5472,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
        "discussion_id": "547897084",
        "commented_code": "@@ -0,0 +1,108 @@\n+\"\"\"\n+Cross Site Request Forgery Blueprint.\n+\n+This module provides a Flask blueprint that implements protection against\n+request forgeries from other sites. Currently, it is only meant to be used with\n+an AJAX frontend, not with server-side rendered forms.\n+\n+The module implements the following protecting measures against CSRF:\n+- Double Submit Cookie.\n+- Custom HTTP Headers.\n+- SameSite cookie attribute.\n+\n+To elaborate, the `Double Submit Cookie` procedure looks like the following:\n+1. Browser requests `index.html`, which contains the compiled Javascript.\n+2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n+   already exists, `set_cookie` overrides it with a new one. The cookie\n+   contains a random value.\n+3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n+   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n+   `CSRF_HEADER` with the same value.\n+4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n+   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n+   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n+\n+Custom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\n+cross-origin requests cannot include custom headers (assuming CORS is not\n+misconfigured) because of the Same-Origin policy.\n+\n+The SameSite cookie attribute provides another layer of protection, but may\n+impede usability so it is configurable. This attribute controls whether a",
        "comment_created_at": "2020-12-23T10:49:30+00:00",
        "comment_author": "yanniszark",
        "comment_body": "The SameSite attribute is currently not configurable. Should we change the docstring to reflect that? I see that you've added a note that we may need to make it configurable in the future.",
        "pr_file_module": null
      },
      {
        "comment_id": "547931071",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5472,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
        "discussion_id": "547897084",
        "commented_code": "@@ -0,0 +1,108 @@\n+\"\"\"\n+Cross Site Request Forgery Blueprint.\n+\n+This module provides a Flask blueprint that implements protection against\n+request forgeries from other sites. Currently, it is only meant to be used with\n+an AJAX frontend, not with server-side rendered forms.\n+\n+The module implements the following protecting measures against CSRF:\n+- Double Submit Cookie.\n+- Custom HTTP Headers.\n+- SameSite cookie attribute.\n+\n+To elaborate, the `Double Submit Cookie` procedure looks like the following:\n+1. Browser requests `index.html`, which contains the compiled Javascript.\n+2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n+   already exists, `set_cookie` overrides it with a new one. The cookie\n+   contains a random value.\n+3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n+   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n+   `CSRF_HEADER` with the same value.\n+4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n+   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n+   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n+\n+Custom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\n+cross-origin requests cannot include custom headers (assuming CORS is not\n+misconfigured) because of the Same-Origin policy.\n+\n+The SameSite cookie attribute provides another layer of protection, but may\n+impede usability so it is configurable. This attribute controls whether a",
        "comment_created_at": "2020-12-23T12:17:56+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Lets make it configurable then, it should be a small change.\r\n\r\nI'll make it look for a `CSRF_SAMESITE` env var with a default value to `Strict`. If the value provided by the user is not `Strict`, `Lax` or `None` then again it will default to `Strict`\r\nhttps://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#SameSite",
        "pr_file_module": null
      },
      {
        "comment_id": "547936642",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5472,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
        "discussion_id": "547897084",
        "commented_code": "@@ -0,0 +1,108 @@\n+\"\"\"\n+Cross Site Request Forgery Blueprint.\n+\n+This module provides a Flask blueprint that implements protection against\n+request forgeries from other sites. Currently, it is only meant to be used with\n+an AJAX frontend, not with server-side rendered forms.\n+\n+The module implements the following protecting measures against CSRF:\n+- Double Submit Cookie.\n+- Custom HTTP Headers.\n+- SameSite cookie attribute.\n+\n+To elaborate, the `Double Submit Cookie` procedure looks like the following:\n+1. Browser requests `index.html`, which contains the compiled Javascript.\n+2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n+   already exists, `set_cookie` overrides it with a new one. The cookie\n+   contains a random value.\n+3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n+   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n+   `CSRF_HEADER` with the same value.\n+4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n+   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n+   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n+\n+Custom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\n+cross-origin requests cannot include custom headers (assuming CORS is not\n+misconfigured) because of the Same-Origin policy.\n+\n+The SameSite cookie attribute provides another layer of protection, but may\n+impede usability so it is configurable. This attribute controls whether a",
        "comment_created_at": "2020-12-23T12:32:18+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "force pushed. The PR should only contain one commit responsible for the CSRF functionality.\r\nI also made the `SameSite` attribute of the cookie configurable via the `CSRF_SAMESITE` variable.\r\n\r\nI also think a good next step would be to document the ENV Vars that each web app uses in the respective READMEs. This will make clear to the users how they can configure each app.",
        "pr_file_module": null
      },
      {
        "comment_id": "548001562",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5472,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
        "discussion_id": "547897084",
        "commented_code": "@@ -0,0 +1,108 @@\n+\"\"\"\n+Cross Site Request Forgery Blueprint.\n+\n+This module provides a Flask blueprint that implements protection against\n+request forgeries from other sites. Currently, it is only meant to be used with\n+an AJAX frontend, not with server-side rendered forms.\n+\n+The module implements the following protecting measures against CSRF:\n+- Double Submit Cookie.\n+- Custom HTTP Headers.\n+- SameSite cookie attribute.\n+\n+To elaborate, the `Double Submit Cookie` procedure looks like the following:\n+1. Browser requests `index.html`, which contains the compiled Javascript.\n+2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n+   already exists, `set_cookie` overrides it with a new one. The cookie\n+   contains a random value.\n+3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n+   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n+   `CSRF_HEADER` with the same value.\n+4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n+   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n+   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n+\n+Custom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\n+cross-origin requests cannot include custom headers (assuming CORS is not\n+misconfigured) because of the Same-Origin policy.\n+\n+The SameSite cookie attribute provides another layer of protection, but may\n+impede usability so it is configurable. This attribute controls whether a",
        "comment_created_at": "2020-12-23T15:04:14+00:00",
        "comment_author": "yanniszark",
        "comment_body": "That's great! One question: maybe it's better to start the env var section in the README now and document this specific settings with this PR, which introduces it. You can add a note that the section is a work in-progress so that readers don't get confused. What do you think?\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "548016953",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5472,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/csrf.py",
        "discussion_id": "547897084",
        "commented_code": "@@ -0,0 +1,108 @@\n+\"\"\"\n+Cross Site Request Forgery Blueprint.\n+\n+This module provides a Flask blueprint that implements protection against\n+request forgeries from other sites. Currently, it is only meant to be used with\n+an AJAX frontend, not with server-side rendered forms.\n+\n+The module implements the following protecting measures against CSRF:\n+- Double Submit Cookie.\n+- Custom HTTP Headers.\n+- SameSite cookie attribute.\n+\n+To elaborate, the `Double Submit Cookie` procedure looks like the following:\n+1. Browser requests `index.html`, which contains the compiled Javascript.\n+2. Backend sets the `CSRF_COOKIE` by calling `set_cookie`. If the cookie\n+   already exists, `set_cookie` overrides it with a new one. The cookie\n+   contains a random value.\n+3. Frontend (`index.html`) is loaded and starts making requests to the backend.\n+   For every request, the frontend reads the `CSRF_COOKIE` value and adds a\n+   `CSRF_HEADER` with the same value.\n+4. Backend checks that the value of `CSRF_COOKIE` matches the value of\n+   `CSRF_HEADER`. All endpoints are checked, except the index endpoint and\n+   endpoints with safe methods (GET, HEAD, OPTIONS, TRACE).\n+\n+Custom Headers (`CSRF_HEADER`) provide an extra layer of protection, as\n+cross-origin requests cannot include custom headers (assuming CORS is not\n+misconfigured) because of the Same-Origin policy.\n+\n+The SameSite cookie attribute provides another layer of protection, but may\n+impede usability so it is configurable. This attribute controls whether a",
        "comment_created_at": "2020-12-23T15:36:34+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "ACK! I modified the README of the common code.\r\nI also created #5483 as an umbrella issue for the web apps",
        "pr_file_module": null
      }
    ]
  }
]
