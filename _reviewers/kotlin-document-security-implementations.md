---
title: Document security implementations
description: Always document non-obvious security implementations, especially authentication
  mechanisms, with explanatory comments and references to underlying implementation
  details or documentation. Security-related code should be explicit and clear to
  prevent misunderstandings that could lead to vulnerabilities.
repository: JetBrains/kotlin
label: Security
language: Kotlin
comments_count: 1
repository_stars: 50857
---

Always document non-obvious security implementations, especially authentication mechanisms, with explanatory comments and references to underlying implementation details or documentation. Security-related code should be explicit and clear to prevent misunderstandings that could lead to vulnerabilities.

When implementing credential handling or other security features in ways that might not be immediately obvious to other developers, add comments that explain your design decisions and link to relevant documentation or implementation details.

Example:
```kotlin
// Authentication is implemented following the pattern used in org.eclipse.aether.repository.Authentication
// where all credentials are provided to the builder and consumers decide what to use
// See: org.eclipse.aether.transport.wagon.WagonTransporter#getProxy for implementation details
setAuthentication(
    AuthenticationBuilder().apply {
        with(options) {
            addUsername(username?.let(::tryResolveEnvironmentVariable))
            addPassword(password?.let(::tryResolveEnvironmentVariable))
        }
    }
)
```


[
  {
    "discussion_id": "632319980",
    "pr_number": 4383,
    "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
    "created_at": "2021-05-14T06:43:17+00:00",
    "commented_code": "val url = repositoryCoordinates.toRepositoryUrlOrNull()\n            ?: return false.asSuccess()\n        val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n            if (username != null) {\n                val auth = AuthenticationBuilder().apply {\n                    addUsername(username)\n                    if (password != null) {\n                        addPassword(password)\n        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n            setAuthentication(\n                AuthenticationBuilder().apply {\n                    with(options) {\n                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "632319980",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
        "discussion_id": "632319980",
        "commented_code": "@@ -89,21 +90,22 @@ class MavenDependenciesResolver : ExternalDependenciesResolver {\n         val url = repositoryCoordinates.toRepositoryUrlOrNull()\n             ?: return false.asSuccess()\n         val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n-        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n-        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n-            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n-            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n-            if (username != null) {\n-                val auth = AuthenticationBuilder().apply {\n-                    addUsername(username)\n-                    if (password != null) {\n-                        addPassword(password)\n+        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n+            setAuthentication(\n+                AuthenticationBuilder().apply {\n+                    with(options) {\n+                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
        "comment_created_at": "2021-05-14T06:43:17+00:00",
        "comment_author": "ligee",
        "comment_body": "I suspect that the logic should be similar to the previous variant - first, we check if any option is set and only then add an auth for only one variant. (And if both are set, prefer the key/passphrase).",
        "pr_file_module": null
      },
      {
        "comment_id": "632499749",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
        "discussion_id": "632319980",
        "commented_code": "@@ -89,21 +90,22 @@ class MavenDependenciesResolver : ExternalDependenciesResolver {\n         val url = repositoryCoordinates.toRepositoryUrlOrNull()\n             ?: return false.asSuccess()\n         val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n-        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n-        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n-            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n-            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n-            if (username != null) {\n-                val auth = AuthenticationBuilder().apply {\n-                    addUsername(username)\n-                    if (password != null) {\n-                        addPassword(password)\n+        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n+            setAuthentication(\n+                AuthenticationBuilder().apply {\n+                    with(options) {\n+                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
        "comment_created_at": "2021-05-14T12:41:06+00:00",
        "comment_author": "ileasile",
        "comment_body": "I think that implemented approach is more in style of `org.eclipse.aether.repository.Authentication` interface: we simply put into the container all that we have, and consumers in the resolver internals decide what they will use. I think that this logic is more clear and more correct. Empty authorization doesn't differ (in logic) from null one, the cost here is insignificant",
        "pr_file_module": null
      },
      {
        "comment_id": "632525443",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
        "discussion_id": "632319980",
        "commented_code": "@@ -89,21 +90,22 @@ class MavenDependenciesResolver : ExternalDependenciesResolver {\n         val url = repositoryCoordinates.toRepositoryUrlOrNull()\n             ?: return false.asSuccess()\n         val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n-        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n-        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n-            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n-            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n-            if (username != null) {\n-                val auth = AuthenticationBuilder().apply {\n-                    addUsername(username)\n-                    if (password != null) {\n-                        addPassword(password)\n+        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n+            setAuthentication(\n+                AuthenticationBuilder().apply {\n+                    with(options) {\n+                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
        "comment_created_at": "2021-05-14T13:25:09+00:00",
        "comment_author": "ligee",
        "comment_body": "I do not see any \"style\" in the `org.eclipse.aether.repository.Authentication` that would suggest such implementation. Can you please show, what you mean? Or maybe it is documented somewhere?\r\nWithout some examples or explicit recommendations, I would consider this approach ambiguous, and therefore not desirable.",
        "pr_file_module": null
      },
      {
        "comment_id": "632598089",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
        "discussion_id": "632319980",
        "commented_code": "@@ -89,21 +90,22 @@ class MavenDependenciesResolver : ExternalDependenciesResolver {\n         val url = repositoryCoordinates.toRepositoryUrlOrNull()\n             ?: return false.asSuccess()\n         val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n-        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n-        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n-            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n-            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n-            if (username != null) {\n-                val auth = AuthenticationBuilder().apply {\n-                    addUsername(username)\n-                    if (password != null) {\n-                        addPassword(password)\n+        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n+            setAuthentication(\n+                AuthenticationBuilder().apply {\n+                    with(options) {\n+                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
        "comment_created_at": "2021-05-14T15:13:14+00:00",
        "comment_author": "ileasile",
        "comment_body": "Each Authentication populates AuthenticationContext in the `fill` method. `AuthenticationContext` has all the data in the raw map `org.eclipse.aether.repository.AuthenticationContext#authData`, and then each consumer uses it in its own way. I mean that all the logic about nullability and emptiness is on the lower level, these checks will be performed anyway.\r\nFor example, see how authorization is used in wagon transporter: it is first converted to another instance (`org.eclipse.aether.transport.wagon.WagonTransporter#getProxy`) and then these values are used with all the checks performed here: `org.apache.maven.wagon.shared.http.AbstractHttpClientWagon#openConnectionInternal`. I don't think we should care about it: some implementations may use password without username or username without password, it should not be solved here",
        "pr_file_module": null
      },
      {
        "comment_id": "633291461",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 4383,
        "pr_file": "libraries/scripting/dependencies-maven/src/kotlin/script/experimental/dependencies/maven/MavenDependenciesResolver.kt",
        "discussion_id": "632319980",
        "commented_code": "@@ -89,21 +90,22 @@ class MavenDependenciesResolver : ExternalDependenciesResolver {\n         val url = repositoryCoordinates.toRepositoryUrlOrNull()\n             ?: return false.asSuccess()\n         val repoId = repositoryCoordinates.string.replace(FORBIDDEN_CHARS, \"_\")\n-        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString())\n-        if (repositoryCoordinates is MavenRepositoryCoordinates) {\n-            val username = repositoryCoordinates.username?.let(::tryResolveEnvironmentVariable)\n-            val password = repositoryCoordinates.password?.let(::tryResolveEnvironmentVariable)\n-            if (username != null) {\n-                val auth = AuthenticationBuilder().apply {\n-                    addUsername(username)\n-                    if (password != null) {\n-                        addPassword(password)\n+        val repo = RemoteRepository.Builder(repoId, \"default\", url.toString()).apply {\n+            setAuthentication(\n+                AuthenticationBuilder().apply {\n+                    with(options) {\n+                        addUsername(username?.let(::tryResolveEnvironmentVariable))",
        "comment_created_at": "2021-05-17T07:38:52+00:00",
        "comment_author": "ligee",
        "comment_body": "Since it is a place that I stumbled upon, it may look suspicious to others in the future too. I'd suggest at least adding an appropriate comment with the link to implementation (and/or documentation) as an explanation.",
        "pr_file_module": null
      }
    ]
  }
]
