---
title: Use configuration property providers
description: Always use Gradle's Provider API when accessing project, system, or Gradle
  properties in your build configuration. This ensures proper handling of configuration
  cache and allows for dynamic property updates.
repository: JetBrains/kotlin
label: Configurations
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Always use Gradle's Provider API when accessing project, system, or Gradle properties in your build configuration. This ensures proper handling of configuration cache and allows for dynamic property updates.

Instead of directly accessing properties:

```kotlin
// DON'T
val verbose = (project.hasProperty("kapt.verbose") && 
    project.property("kapt.verbose").toString().toBoolean() == true)

// DO
val verbose = project.providers.gradleProperty("kapt.verbose")
    .map { it.toBoolean() }
    .orElse(false)

// DON'T
val systemProp = System.getProperty("my.property")

// DO
val systemProp = project.providers.systemProperty("my.property")
```

This approach:
- Supports Gradle's configuration cache feature
- Allows for property value changes during build execution
- Provides proper lazy evaluation of properties
- Maintains build configuration stability

When dealing with file paths or build directory locations, use ProjectLayout:
```kotlin
val layout = project.layout
val outputFile = layout.buildDirectory.file("output/file.txt")
```


[
  {
    "discussion_id": "449662023",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/internal/kapt/KaptGenerateStubsTask.kt",
    "created_at": "2020-07-03T17:06:24+00:00",
    "commented_code": "error(\"KaptGenerateStubsTask.useModuleDetection setter should not be called!\")\n        }\n\n    @get:Input\n    val verbose = (project.hasProperty(\"kapt.verbose\") && project.property(\"kapt.verbose\").toString().toBoolean() == true)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "449662023",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/internal/kapt/KaptGenerateStubsTask.kt",
        "discussion_id": "449662023",
        "commented_code": "@@ -69,6 +69,9 @@ open class KaptGenerateStubsTask : KotlinCompile() {\n             error(\"KaptGenerateStubsTask.useModuleDetection setter should not be called!\")\n         }\n \n+    @get:Input\n+    val verbose = (project.hasProperty(\"kapt.verbose\") && project.property(\"kapt.verbose\").toString().toBoolean() == true)",
        "comment_created_at": "2020-07-03T17:06:24+00:00",
        "comment_author": "eskatos",
        "comment_body": ":o: This could be modelled as a `Provider` to account for later changes to that property:\r\n\r\n```kotlin\r\nproject.providers.gradleProperty(\"kapt.verbose\").map { it.toBoolean() }.orElse(false)\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "449666668",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/BuildEventsListenerRegistryHolder.kt",
    "created_at": "2020-07-03T17:29:12+00:00",
    "commented_code": "/*\n * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n */\n\npackage org.jetbrains.kotlin.gradle.plugin\n\nimport org.gradle.api.Project\nimport org.gradle.build.event.BuildEventsListenerRegistry\nimport org.jetbrains.kotlin.gradle.utils.isConfigurationCacheAvailable\nimport javax.inject.Inject\n\nopen class BuildEventsListenerRegistryHolder @Inject constructor(val listenerRegistry: BuildEventsListenerRegistry?) {\n    companion object {\n        fun getInstance(project: Project) = run {\n            if (isConfigurationCacheAvailable(project.gradle)) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "449666668",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/BuildEventsListenerRegistryHolder.kt",
        "discussion_id": "449666668",
        "commented_code": "@@ -0,0 +1,23 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package org.jetbrains.kotlin.gradle.plugin\n+\n+import org.gradle.api.Project\n+import org.gradle.build.event.BuildEventsListenerRegistry\n+import org.jetbrains.kotlin.gradle.utils.isConfigurationCacheAvailable\n+import javax.inject.Inject\n+\n+open class BuildEventsListenerRegistryHolder @Inject constructor(val listenerRegistry: BuildEventsListenerRegistry?) {\n+    companion object {\n+        fun getInstance(project: Project) = run {\n+            if (isConfigurationCacheAvailable(project.gradle)) {",
        "comment_created_at": "2020-07-03T17:29:12+00:00",
        "comment_author": "eskatos",
        "comment_body": ":x: the check should be `gradleVersion >= 6.1` instead where `BuildEventsListenerRegistry` is available",
        "pr_file_module": null
      },
      {
        "comment_id": "454990923",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/BuildEventsListenerRegistryHolder.kt",
        "discussion_id": "449666668",
        "commented_code": "@@ -0,0 +1,23 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package org.jetbrains.kotlin.gradle.plugin\n+\n+import org.gradle.api.Project\n+import org.gradle.build.event.BuildEventsListenerRegistry\n+import org.jetbrains.kotlin.gradle.utils.isConfigurationCacheAvailable\n+import javax.inject.Inject\n+\n+open class BuildEventsListenerRegistryHolder @Inject constructor(val listenerRegistry: BuildEventsListenerRegistry?) {\n+    companion object {\n+        fun getInstance(project: Project) = run {\n+            if (isConfigurationCacheAvailable(project.gradle)) {",
        "comment_created_at": "2020-07-15T11:47:18+00:00",
        "comment_author": "nav-nav",
        "comment_body": "New listener is not ready for configuration cache",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "449666709",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleBuildServices.kt",
    "created_at": "2020-07-03T17:29:28+00:00",
    "commented_code": "val ALREADY_INITIALIZED_MESSAGE = \"$CLASS_NAME is already initialized\"\n\n        @field:Volatile\n        private var instance: KotlinGradleBuildServices? = null\n        internal var instance: KotlinGradleBuildServices? = null\n\n//        @JvmStatic\n//        @Synchronized\n//        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n//            val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n//\n//            if (instance != null) {\n//                log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n//                return instance!!\n//            }\n//\n//            val services = KotlinGradleBuildServices(gradle)\n//            instance = services\n//            if (!isGradleVersionAtLeast(6,1)) {\n//                gradle.addBuildListener(services)\n//                log.kotlinDebug(INIT_MESSAGE)\n//            } else {\n//                BuildEventsListenerRegistry.\n//            }\n//\n//            services.buildStarted()\n//            return services\n//        }\n\n\n        @JvmStatic\n        @Synchronized\n        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n        fun getInstance(project: Project, listenerRegistryHolder: BuildEventsListenerRegistryHolder): KotlinGradleBuildServices {\n            val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n            val kotlinGradleListenerProvider: org.gradle.api.provider.Provider<KotlinGradleBuildListener> = project.provider {\n                KotlinGradleBuildListener(KotlinGradleFinishBuildHandler())\n            }\n\n            if (instance != null) {\n                log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n                return instance!!\n            }\n\n            val gradle = project.gradle\n            val services = KotlinGradleBuildServices(gradle)\n            gradle.addBuildListener(services)\n            instance = services\n            log.kotlinDebug(INIT_MESSAGE)\n            if (isConfigurationCacheAvailable(gradle)) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "449666709",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleBuildServices.kt",
        "discussion_id": "449666709",
        "commented_code": "@@ -34,36 +32,69 @@ internal class KotlinGradleBuildServices private constructor(\n         val ALREADY_INITIALIZED_MESSAGE = \"$CLASS_NAME is already initialized\"\n \n         @field:Volatile\n-        private var instance: KotlinGradleBuildServices? = null\n+        internal var instance: KotlinGradleBuildServices? = null\n+\n+//        @JvmStatic\n+//        @Synchronized\n+//        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n+//            val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n+//\n+//            if (instance != null) {\n+//                log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n+//                return instance!!\n+//            }\n+//\n+//            val services = KotlinGradleBuildServices(gradle)\n+//            instance = services\n+//            if (!isGradleVersionAtLeast(6,1)) {\n+//                gradle.addBuildListener(services)\n+//                log.kotlinDebug(INIT_MESSAGE)\n+//            } else {\n+//                BuildEventsListenerRegistry.\n+//            }\n+//\n+//            services.buildStarted()\n+//            return services\n+//        }\n+\n \n         @JvmStatic\n         @Synchronized\n-        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n+        fun getInstance(project: Project, listenerRegistryHolder: BuildEventsListenerRegistryHolder): KotlinGradleBuildServices {\n             val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n+            val kotlinGradleListenerProvider: org.gradle.api.provider.Provider<KotlinGradleBuildListener> = project.provider {\n+                KotlinGradleBuildListener(KotlinGradleFinishBuildHandler())\n+            }\n \n             if (instance != null) {\n                 log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n                 return instance!!\n             }\n \n+            val gradle = project.gradle\n             val services = KotlinGradleBuildServices(gradle)\n-            gradle.addBuildListener(services)\n-            instance = services\n-            log.kotlinDebug(INIT_MESSAGE)\n+            if (isConfigurationCacheAvailable(gradle)) {",
        "comment_created_at": "2020-07-03T17:29:28+00:00",
        "comment_author": "eskatos",
        "comment_body": ":x: the check should be `gradleVersion >= 6.1` instead where `BuildEventsListenerRegistry` is available",
        "pr_file_module": null
      },
      {
        "comment_id": "454991396",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleBuildServices.kt",
        "discussion_id": "449666709",
        "commented_code": "@@ -34,36 +32,69 @@ internal class KotlinGradleBuildServices private constructor(\n         val ALREADY_INITIALIZED_MESSAGE = \"$CLASS_NAME is already initialized\"\n \n         @field:Volatile\n-        private var instance: KotlinGradleBuildServices? = null\n+        internal var instance: KotlinGradleBuildServices? = null\n+\n+//        @JvmStatic\n+//        @Synchronized\n+//        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n+//            val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n+//\n+//            if (instance != null) {\n+//                log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n+//                return instance!!\n+//            }\n+//\n+//            val services = KotlinGradleBuildServices(gradle)\n+//            instance = services\n+//            if (!isGradleVersionAtLeast(6,1)) {\n+//                gradle.addBuildListener(services)\n+//                log.kotlinDebug(INIT_MESSAGE)\n+//            } else {\n+//                BuildEventsListenerRegistry.\n+//            }\n+//\n+//            services.buildStarted()\n+//            return services\n+//        }\n+\n \n         @JvmStatic\n         @Synchronized\n-        fun getInstance(gradle: Gradle): KotlinGradleBuildServices {\n+        fun getInstance(project: Project, listenerRegistryHolder: BuildEventsListenerRegistryHolder): KotlinGradleBuildServices {\n             val log = Logging.getLogger(KotlinGradleBuildServices::class.java)\n+            val kotlinGradleListenerProvider: org.gradle.api.provider.Provider<KotlinGradleBuildListener> = project.provider {\n+                KotlinGradleBuildListener(KotlinGradleFinishBuildHandler())\n+            }\n \n             if (instance != null) {\n                 log.kotlinDebug(ALREADY_INITIALIZED_MESSAGE)\n                 return instance!!\n             }\n \n+            val gradle = project.gradle\n             val services = KotlinGradleBuildServices(gradle)\n-            gradle.addBuildListener(services)\n-            instance = services\n-            log.kotlinDebug(INIT_MESSAGE)\n+            if (isConfigurationCacheAvailable(gradle)) {",
        "comment_created_at": "2020-07-15T11:48:11+00:00",
        "comment_author": "nav-nav",
        "comment_body": "New listener is not ready for configuration cache ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "449666750",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/statistics/KotlinBuildStatsService.kt",
    "created_at": "2020-07-03T17:29:43+00:00",
    "commented_code": ")\n                            instance = JMXKotlinBuildStatsService(mbs, beanName)\n                        } else {\n                            val kotlinBuildStatProvider = project.provider{ KotlinBuildStatListener(beanName) }\n                            val newInstance = DefaultKotlinBuildStatsService(gradle, beanName)\n\n                            if (isConfigurationCacheAvailable(gradle)) {",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "449666750",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/statistics/KotlinBuildStatsService.kt",
        "discussion_id": "449666750",
        "commented_code": "@@ -106,21 +105,26 @@ internal abstract class KotlinBuildStatsService internal constructor() : BuildAd\n                             )\n                             instance = JMXKotlinBuildStatsService(mbs, beanName)\n                         } else {\n+                            val kotlinBuildStatProvider = project.provider{ KotlinBuildStatListener(beanName) }\n                             val newInstance = DefaultKotlinBuildStatsService(gradle, beanName)\n+\n+                            if (isConfigurationCacheAvailable(gradle)) {",
        "comment_created_at": "2020-07-03T17:29:43+00:00",
        "comment_author": "eskatos",
        "comment_body": ":x: the check should be `gradleVersion >= 6.1` instead where `BuildEventsListenerRegistry` is available",
        "pr_file_module": null
      },
      {
        "comment_id": "454991473",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/statistics/KotlinBuildStatsService.kt",
        "discussion_id": "449666750",
        "commented_code": "@@ -106,21 +105,26 @@ internal abstract class KotlinBuildStatsService internal constructor() : BuildAd\n                             )\n                             instance = JMXKotlinBuildStatsService(mbs, beanName)\n                         } else {\n+                            val kotlinBuildStatProvider = project.provider{ KotlinBuildStatListener(beanName) }\n                             val newInstance = DefaultKotlinBuildStatsService(gradle, beanName)\n+\n+                            if (isConfigurationCacheAvailable(gradle)) {",
        "comment_created_at": "2020-07-15T11:48:19+00:00",
        "comment_author": "nav-nav",
        "comment_body": "New listener is not ready for configuration cache",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "450245646",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleFinishBuildHandler.kt",
    "created_at": "2020-07-06T14:07:53+00:00",
    "commented_code": "/*\n * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n */\n\npackage org.jetbrains.kotlin.gradle.plugin\n\nimport org.gradle.api.invocation.Gradle\nimport org.gradle.api.logging.Logging\nimport org.jetbrains.kotlin.compilerRunner.DELETED_SESSION_FILE_PREFIX\nimport org.jetbrains.kotlin.compilerRunner.GradleCompilerRunner\nimport org.jetbrains.kotlin.gradle.logging.kotlinDebug\nimport org.jetbrains.kotlin.gradle.plugin.internal.state.TaskExecutionResults\nimport org.jetbrains.kotlin.gradle.plugin.internal.state.TaskLoggers\nimport org.jetbrains.kotlin.gradle.utils.relativeToRoot\nimport org.jetbrains.kotlin.utils.addToStdlib.sumByLong\nimport java.lang.management.ManagementFactory\nimport kotlin.math.max\n\n// move to KotlinGradleBuildListener when min supported version is 6.1\nclass KotlinGradleFinishBuildHandler {\n\n    private val log = Logging.getLogger(this.javaClass)\n    private var startMemory: Long? = null\n    private val shouldReportMemoryUsage = System.getProperty(KotlinGradleBuildServices.SHOULD_REPORT_MEMORY_USAGE_PROPERTY) != null",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "450245646",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleFinishBuildHandler.kt",
        "discussion_id": "450245646",
        "commented_code": "@@ -0,0 +1,77 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package org.jetbrains.kotlin.gradle.plugin\n+\n+import org.gradle.api.invocation.Gradle\n+import org.gradle.api.logging.Logging\n+import org.jetbrains.kotlin.compilerRunner.DELETED_SESSION_FILE_PREFIX\n+import org.jetbrains.kotlin.compilerRunner.GradleCompilerRunner\n+import org.jetbrains.kotlin.gradle.logging.kotlinDebug\n+import org.jetbrains.kotlin.gradle.plugin.internal.state.TaskExecutionResults\n+import org.jetbrains.kotlin.gradle.plugin.internal.state.TaskLoggers\n+import org.jetbrains.kotlin.gradle.utils.relativeToRoot\n+import org.jetbrains.kotlin.utils.addToStdlib.sumByLong\n+import java.lang.management.ManagementFactory\n+import kotlin.math.max\n+\n+// move to KotlinGradleBuildListener when min supported version is 6.1\n+class KotlinGradleFinishBuildHandler {\n+\n+    private val log = Logging.getLogger(this.javaClass)\n+    private var startMemory: Long? = null\n+    private val shouldReportMemoryUsage = System.getProperty(KotlinGradleBuildServices.SHOULD_REPORT_MEMORY_USAGE_PROPERTY) != null",
        "comment_created_at": "2020-07-06T14:07:53+00:00",
        "comment_author": "gavra0",
        "comment_body": "Use `ObjectFactory.systemProperty` to get the value to allow reconfiguration if it changes.",
        "pr_file_module": null
      },
      {
        "comment_id": "450265691",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/KotlinGradleFinishBuildHandler.kt",
        "discussion_id": "450245646",
        "commented_code": "@@ -0,0 +1,77 @@\n+/*\n+ * Copyright 2010-2020 JetBrains s.r.o. and Kotlin Programming Language contributors.\n+ * Use of this source code is governed by the Apache 2.0 license that can be found in the license/LICENSE.txt file.\n+ */\n+\n+package org.jetbrains.kotlin.gradle.plugin\n+\n+import org.gradle.api.invocation.Gradle\n+import org.gradle.api.logging.Logging\n+import org.jetbrains.kotlin.compilerRunner.DELETED_SESSION_FILE_PREFIX\n+import org.jetbrains.kotlin.compilerRunner.GradleCompilerRunner\n+import org.jetbrains.kotlin.gradle.logging.kotlinDebug\n+import org.jetbrains.kotlin.gradle.plugin.internal.state.TaskExecutionResults\n+import org.jetbrains.kotlin.gradle.plugin.internal.state.TaskLoggers\n+import org.jetbrains.kotlin.gradle.utils.relativeToRoot\n+import org.jetbrains.kotlin.utils.addToStdlib.sumByLong\n+import java.lang.management.ManagementFactory\n+import kotlin.math.max\n+\n+// move to KotlinGradleBuildListener when min supported version is 6.1\n+class KotlinGradleFinishBuildHandler {\n+\n+    private val log = Logging.getLogger(this.javaClass)\n+    private var startMemory: Long? = null\n+    private val shouldReportMemoryUsage = System.getProperty(KotlinGradleBuildServices.SHOULD_REPORT_MEMORY_USAGE_PROPERTY) != null",
        "comment_created_at": "2020-07-06T14:35:54+00:00",
        "comment_author": "eskatos",
        "comment_body": "Should be `ProviderFactory.systemProperty(name)`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "450262095",
    "pr_number": 3521,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/mpp/TransformKotlinGranularMetadata.kt",
    "created_at": "2020-07-06T14:30:50+00:00",
    "commented_code": "import org.jetbrains.kotlin.gradle.plugin.sources.getSourceSetHierarchy\nimport org.jetbrains.kotlin.gradle.targets.metadata.ALL_COMPILE_METADATA_CONFIGURATION_NAME\nimport org.jetbrains.kotlin.gradle.targets.metadata.KotlinMetadataTargetConfigurator\nimport org.jetbrains.kotlin.gradle.utils.getValue\nimport java.io.File\nimport javax.inject.Inject\n\nopen class TransformKotlinGranularMetadata\n@Inject constructor(\n    @get:Internal\n    @field:Transient\n    val kotlinSourceSet: KotlinSourceSet\n) : DefaultTask() {\n\n    @get:OutputDirectory\n    val outputsDir: File = project.buildDir.resolve(\"kotlinSourceSetMetadata/${kotlinSourceSet.name}\")\n    val outputsDir: File by project.provider {\n        project.buildDir.resolve(\"kotlinSourceSetMetadata/${kotlinSourceSet.name}\")",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "450262095",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3521,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/plugin/mpp/TransformKotlinGranularMetadata.kt",
        "discussion_id": "450262095",
        "commented_code": "@@ -15,22 +15,28 @@ import org.jetbrains.kotlin.gradle.plugin.sources.KotlinDependencyScope.*\n import org.jetbrains.kotlin.gradle.plugin.sources.getSourceSetHierarchy\n import org.jetbrains.kotlin.gradle.targets.metadata.ALL_COMPILE_METADATA_CONFIGURATION_NAME\n import org.jetbrains.kotlin.gradle.targets.metadata.KotlinMetadataTargetConfigurator\n+import org.jetbrains.kotlin.gradle.utils.getValue\n import java.io.File\n import javax.inject.Inject\n \n open class TransformKotlinGranularMetadata\n @Inject constructor(\n     @get:Internal\n+    @field:Transient\n     val kotlinSourceSet: KotlinSourceSet\n ) : DefaultTask() {\n \n     @get:OutputDirectory\n-    val outputsDir: File = project.buildDir.resolve(\"kotlinSourceSetMetadata/${kotlinSourceSet.name}\")\n+    val outputsDir: File by project.provider {\n+        project.buildDir.resolve(\"kotlinSourceSetMetadata/${kotlinSourceSet.name}\")",
        "comment_created_at": "2020-07-06T14:30:50+00:00",
        "comment_author": "gavra0",
        "comment_body": "Use `ProjectLayout` methods to compute this. E.g. this will not detect changes if buildDir changes.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "456298937",
    "pr_number": 3571,
    "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/internal/kapt/KaptGenerateStubsTask.kt",
    "created_at": "2020-07-17T08:29:57+00:00",
    "commented_code": "error(\"KaptGenerateStubsTask.useModuleDetection setter should not be called!\")\n        }\n\n    @get:Input\n    val verbose = (project.hasProperty(\"kapt.verbose\") && project.property(\"kapt.verbose\").toString().toBoolean() == true)",
    "repo_full_name": "JetBrains/kotlin",
    "discussion_comments": [
      {
        "comment_id": "456298937",
        "repo_full_name": "JetBrains/kotlin",
        "pr_number": 3571,
        "pr_file": "libraries/tools/kotlin-gradle-plugin/src/main/kotlin/org/jetbrains/kotlin/gradle/internal/kapt/KaptGenerateStubsTask.kt",
        "discussion_id": "456298937",
        "commented_code": "@@ -69,6 +69,9 @@ open class KaptGenerateStubsTask : KotlinCompile() {\n             error(\"KaptGenerateStubsTask.useModuleDetection setter should not be called!\")\n         }\n \n+    @get:Input\n+    val verbose = (project.hasProperty(\"kapt.verbose\") && project.property(\"kapt.verbose\").toString().toBoolean() == true)",
        "comment_created_at": "2020-07-17T08:29:57+00:00",
        "comment_author": "eskatos",
        "comment_body": ":o: This could be modelled as a `Provider` to account for later changes to that property:\r\n\r\n```kotlin\r\nproject.providers.gradleProperty(\"kapt.verbose\").map { it.toBoolean() }.orElse(false)\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
