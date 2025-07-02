---
title: Feature flag implementation
description: 'When implementing feature flags, ensure consistency between runtime
  and compiled scenarios. Feature switches marked with `FeatureSwitchDefinition` must
  properly return the AppContext switch value when defined:'
repository: dotnet/runtime
label: Configurations
language: C#
comments_count: 2
repository_stars: 16578
---

When implementing feature flags, ensure consistency between runtime and compiled scenarios. Feature switches marked with `FeatureSwitchDefinition` must properly return the AppContext switch value when defined:

```csharp
// INCORRECT implementation
[FeatureSwitchDefinition("System.Net.SocketsHttpHandler.Http3Support")]
public static bool IsHttp3Supported => SomeDefaultLogic();

// CORRECT implementation - must use the AppContext switch value
[FeatureSwitchDefinition("System.Net.SocketsHttpHandler.Http3Support")]
public static bool IsHttp3Supported => 
    AppContext.TryGetSwitch("System.Net.SocketsHttpHandler.Http3Support", out var ret) ? ret : SomeDefaultLogic();
```

Consider dead code elimination implications when designing feature flags for AOT scenarios, as behavior differences may arise between `dotnet run` and `dotnet publish`. Avoid adding configuration switches preemptively - only introduce them when there's a demonstrated need from users. For platform-specific features, ensure configuration is properly respected across all supported environments.


[
  {
    "discussion_id": "2166465965",
    "pr_number": 117012,
    "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
    "created_at": "2025-06-25T11:17:26+00:00",
    "commented_code": "_http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                }\n\n                if (IsHttp3Supported() && _http3Enabled)\n                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2166465965",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117012,
        "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
        "discussion_id": "2166465965",
        "commented_code": "@@ -227,7 +227,7 @@ public HttpConnectionPool(HttpConnectionPoolManager poolManager, HttpConnectionK\n                     _http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                 }\n \n-                if (IsHttp3Supported() && _http3Enabled)\n+                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
        "comment_created_at": "2025-06-25T11:17:26+00:00",
        "comment_author": "MihaZupan",
        "comment_body": "> we have both IsHttp3Supported and AllowHttp3, so now some places need to check both\r\n\r\nAny reason we couldn't check for both the OS and `GlobalHttpSettings.SocketsHttpHandler.AllowHttp3` inside of `IsHttp3Supported`?",
        "pr_file_module": null
      },
      {
        "comment_id": "2166740034",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117012,
        "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
        "discussion_id": "2166465965",
        "commented_code": "@@ -227,7 +227,7 @@ public HttpConnectionPool(HttpConnectionPoolManager poolManager, HttpConnectionK\n                     _http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                 }\n \n-                if (IsHttp3Supported() && _http3Enabled)\n+                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
        "comment_created_at": "2025-06-25T13:35:53+00:00",
        "comment_author": "MichalStrehovsky",
        "comment_body": "The constant expression evaluator gets iffy when inlining is involded. This would not inline. We'd need to put the FeatureSwitchDefinition on IsHttp3Supportee as well.",
        "pr_file_module": null
      },
      {
        "comment_id": "2167432970",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117012,
        "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
        "discussion_id": "2166465965",
        "commented_code": "@@ -227,7 +227,7 @@ public HttpConnectionPool(HttpConnectionPoolManager poolManager, HttpConnectionK\n                     _http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                 }\n \n-                if (IsHttp3Supported() && _http3Enabled)\n+                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
        "comment_created_at": "2025-06-25T19:11:05+00:00",
        "comment_author": "MihaZupan",
        "comment_body": "I think that would be my preference over duplicating checks.\r\nAlternatively, move the `FeatureSwitchDefinition` only on the `IsHttp3Supported` since that's the flag that's already used everywhere. The `AllowHttp3` only controls a bool field.",
        "pr_file_module": null
      },
      {
        "comment_id": "2168135782",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117012,
        "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
        "discussion_id": "2166465965",
        "commented_code": "@@ -227,7 +227,7 @@ public HttpConnectionPool(HttpConnectionPoolManager poolManager, HttpConnectionK\n                     _http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                 }\n \n-                if (IsHttp3Supported() && _http3Enabled)\n+                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
        "comment_created_at": "2025-06-26T05:22:43+00:00",
        "comment_author": "MichalStrehovsky",
        "comment_body": "Okay, gave it a shot. One thing that might be necessary to understand for reviewing is that a property marked `FeatureSwitchDefinition` _must_ return the value of the same named AppContext switch (if the AppContext switch has a value defined). It is a bug not to return that. The reason is this:\r\n\r\n```csharp\r\nConsole.WriteLine(Blah.IsIs);\r\n\r\nclass Blah\r\n{\r\n    [FeatureSwitchDefinition(\"System.Net.SocketsHttpHandler.Http3Support\")]\r\n    public static bool IsIs => throw new Exception();\r\n\r\n   // Above implementation is wrong. Correct implementation is:\r\n   // AppContext.TryGetSwitch(\"System.Net.SocketsHttpHandler.Http3Support\", out var ret) ? ret : throw new Exception()\r\n}\r\n```\r\n\r\nThis would throw an exception with `dotnet run` no matter what is specified in a `RuntimeHostConfigurationOption`. It would print true/false in a trimmed app depending on what is XXX in this: `<RuntimeHostConfigurationOption Include=\"System.Net.SocketsHttpHandler.Http3Support\" Value=\"XXX\" Trim=\"true\" />`.\r\n\r\nIt is a bug to have behavioral differences between `dotnet run` and `dotnet publish`.\r\n\r\nSo that should explain the change I had to make to `IsHttp3Supported`. However, this breaks dead code elimination _unless a value for Http3Support is specified_. So before this can merge, we need to update Android/iOS/etc. SDKs to specify a value for the feature switch, or we'll see a size regression.\r\n\r\nOne more thing to point out: Now that Http3Support is a feature switch, someone could go and flip this to true _even on Android_. We need to be fine with that. If we're not fine, we need duplicated checks like I originally had, there's no way around that with the dead code elimination we currently have.",
        "pr_file_module": null
      },
      {
        "comment_id": "2169194070",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117012,
        "pr_file": "src/libraries/System.Net.Http/src/System/Net/Http/SocketsHttpHandler/ConnectionPool/HttpConnectionPool.cs",
        "discussion_id": "2166465965",
        "commented_code": "@@ -227,7 +227,7 @@ public HttpConnectionPool(HttpConnectionPoolManager poolManager, HttpConnectionK\n                     _http2EncodedAuthorityHostHeader = HPackEncoder.EncodeLiteralHeaderFieldWithoutIndexingToAllocatedArray(H2StaticTable.Authority, hostHeader);\n                 }\n \n-                if (IsHttp3Supported() && _http3Enabled)\n+                if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled)",
        "comment_created_at": "2025-06-26T14:20:07+00:00",
        "comment_author": "ManickaP",
        "comment_body": "> to true even on Android.\r\n\r\nIt will make the binary bigger. But unless someone deploys it with manually compiled libmsquic.so for android, it won't get past `Quic.IsSupported`. And if someone is **that** adventurous, why stop them (well https://github.com/dotnet/runtime/issues/111019 will likely stop them instead :smiley:)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2150943523",
    "pr_number": 116677,
    "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
    "created_at": "2025-06-16T21:41:38+00:00",
    "commented_code": "private const string TrimmingWarningMessage = \"In case the type is non-primitive, the trimmer cannot statically analyze the object's type so its members may be trimmed.\";\n        private const string InstanceGetTypeTrimmingWarningMessage = \"Cannot statically analyze the type of instance so its members may be trimmed\";\n        private const string PropertyTrimmingWarningMessage = \"Cannot statically analyze property.PropertyType so its members may be trimmed.\";\n        private static bool DisallowNullConfigSwitch { get; } = AppContextSwitchHelper.GetBooleanConfig(\"Microsoft.Configuration.DisallowNull\", \"DOTNET_MICROSOFT_CONFIGURATION_DISALLOWNULL\");",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2150943523",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116677,
        "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
        "discussion_id": "2150943523",
        "commented_code": "@@ -23,6 +23,7 @@ public static class ConfigurationBinder\n         private const string TrimmingWarningMessage = \"In case the type is non-primitive, the trimmer cannot statically analyze the object's type so its members may be trimmed.\";\n         private const string InstanceGetTypeTrimmingWarningMessage = \"Cannot statically analyze the type of instance so its members may be trimmed\";\n         private const string PropertyTrimmingWarningMessage = \"Cannot statically analyze property.PropertyType so its members may be trimmed.\";\n+        private static bool DisallowNullConfigSwitch { get; } = AppContextSwitchHelper.GetBooleanConfig(\"Microsoft.Configuration.DisallowNull\", \"DOTNET_MICROSOFT_CONFIGURATION_DISALLOWNULL\");",
        "comment_created_at": "2025-06-16T21:41:38+00:00",
        "comment_author": "ericstj",
        "comment_body": "nit: we typically don't add these switches until folks ask for them.  Do we expect the null handling here to break folks?  I wouldn't have expected a lot of \"nulls\" in configuration if it didn't work.  If it simplifies the code, consider omitting this and documenting that folks just modify the source to workaround.",
        "pr_file_module": null
      },
      {
        "comment_id": "2151054054",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116677,
        "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
        "discussion_id": "2150943523",
        "commented_code": "@@ -23,6 +23,7 @@ public static class ConfigurationBinder\n         private const string TrimmingWarningMessage = \"In case the type is non-primitive, the trimmer cannot statically analyze the object's type so its members may be trimmed.\";\n         private const string InstanceGetTypeTrimmingWarningMessage = \"Cannot statically analyze the type of instance so its members may be trimmed\";\n         private const string PropertyTrimmingWarningMessage = \"Cannot statically analyze property.PropertyType so its members may be trimmed.\";\n+        private static bool DisallowNullConfigSwitch { get; } = AppContextSwitchHelper.GetBooleanConfig(\"Microsoft.Configuration.DisallowNull\", \"DOTNET_MICROSOFT_CONFIGURATION_DISALLOWNULL\");",
        "comment_created_at": "2025-06-16T23:24:05+00:00",
        "comment_author": "tarekgh",
        "comment_body": "Alright, I\u2019ll consider removing the switch. We\u2019ll document the breaking change regardless, and hopefully the provided workaround will address any issues users might raise.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2153442132",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116677,
        "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
        "discussion_id": "2150943523",
        "commented_code": "@@ -23,6 +23,7 @@ public static class ConfigurationBinder\n         private const string TrimmingWarningMessage = \"In case the type is non-primitive, the trimmer cannot statically analyze the object's type so its members may be trimmed.\";\n         private const string InstanceGetTypeTrimmingWarningMessage = \"Cannot statically analyze the type of instance so its members may be trimmed\";\n         private const string PropertyTrimmingWarningMessage = \"Cannot statically analyze property.PropertyType so its members may be trimmed.\";\n+        private static bool DisallowNullConfigSwitch { get; } = AppContextSwitchHelper.GetBooleanConfig(\"Microsoft.Configuration.DisallowNull\", \"DOTNET_MICROSOFT_CONFIGURATION_DISALLOWNULL\");",
        "comment_created_at": "2025-06-18T01:26:42+00:00",
        "comment_author": "tarekgh",
        "comment_body": "Now the config switch has been removed.",
        "pr_file_module": null
      }
    ]
  }
]
