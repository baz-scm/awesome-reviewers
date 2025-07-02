---
title: Choose semantic algorithms
description: Select algorithms and data operations that match the semantic intent
  of your code rather than using convenient but potentially problematic approaches.
  For operations like version comparisons, string parsing, and collection filtering,
  choose specialized methods over generic ones.
repository: chef/chef
label: Algorithms
language: Ruby
comments_count: 6
repository_stars: 7860
---

Select algorithms and data operations that match the semantic intent of your code rather than using convenient but potentially problematic approaches. For operations like version comparisons, string parsing, and collection filtering, choose specialized methods over generic ones.

For version comparisons:
```ruby
# Avoid unreliable approaches like timestamp comparison
# BAD
latest_version_dir = versions.max_by { |v| File.mtime(v) } 

# GOOD - Use semantic version comparison
latest_version_dir = versions.max_by { |v| Gem::Version.new(File.basename(v)) }
```

For string parsing, prefer structured operations over complex regex when appropriate:
```ruby
# Overly complex regex
z = t.match(/(^pub:.?:\d*:\d*:\w*:[\d-]*):/)

# More maintainable approach
fields = t.split(':')
z = fields[0..4].join(':') if fields.size >= 5
```

For collection operations, choose methods that properly handle the data structure:
```ruby
# Limited to checking a single action
options[:required].include?(action)

# Properly handles multiple actions
(options[:required] & Array(action)).any?
```

Remember that algorithm selection significantly impacts code reliability, maintainability, and performance. Choose algorithms that reflect the true intent of the operation rather than just what seems convenient.


[
  {
    "discussion_id": "2098810301",
    "pr_number": 14794,
    "pr_file": "lib/chef/resource/helpers/path_helpers.rb",
    "created_at": "2025-05-20T20:24:51+00:00",
    "commented_code": "require \"chef-utils/dist\" unless defined?(ChefUtils::Dist)\nclass Chef\n  module ResourceHelpers\n    # Helpers for path manipulation\n    module PathHelpers\n      extend self\n      # The habitat binary path for Infra Client\n      # @return [String]\n      def chef_client_hab_binary_path\n        # Find the most recent version by listing directories\n        # This is heavy operation and should be avoided but currently habitat does not create a symlink by default\n        # and binlink will be created only if `binlink` option is passed so we cannot assume binlink will be present.\n        windows = RUBY_PLATFORM =~ /mswin|mingw|windows/ || defined?(ChefUtils) && ChefUtils.windows?\n        base_path = \"/hab/pkgs/chef/#{ChefUtils::Dist::Infra::HABITAT_PKG}\"\n        base_path = \"C:/#{base_path}\" if windows\n        if File.directory?(base_path)\n          # Get all version directories\n          versions = Dir.glob(\"#{base_path}/*\").select { |d| File.directory?(d) }\n\n          if versions.any?\n            # Get the latest version (based on modification time)\n            latest_version_dir = versions.max_by { |v| File.mtime(v) }",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2098810301",
        "repo_full_name": "chef/chef",
        "pr_number": 14794,
        "pr_file": "lib/chef/resource/helpers/path_helpers.rb",
        "discussion_id": "2098810301",
        "commented_code": "@@ -0,0 +1,41 @@\n+require \"chef-utils/dist\" unless defined?(ChefUtils::Dist)\n+class Chef\n+  module ResourceHelpers\n+    # Helpers for path manipulation\n+    module PathHelpers\n+      extend self\n+      # The habitat binary path for Infra Client\n+      # @return [String]\n+      def chef_client_hab_binary_path\n+        # Find the most recent version by listing directories\n+        # This is heavy operation and should be avoided but currently habitat does not create a symlink by default\n+        # and binlink will be created only if `binlink` option is passed so we cannot assume binlink will be present.\n+        windows = RUBY_PLATFORM =~ /mswin|mingw|windows/ || defined?(ChefUtils) && ChefUtils.windows?\n+        base_path = \"/hab/pkgs/chef/#{ChefUtils::Dist::Infra::HABITAT_PKG}\"\n+        base_path = \"C:/#{base_path}\" if windows\n+        if File.directory?(base_path)\n+          # Get all version directories\n+          versions = Dir.glob(\"#{base_path}/*\").select { |d| File.directory?(d) }\n+\n+          if versions.any?\n+            # Get the latest version (based on modification time)\n+            latest_version_dir = versions.max_by { |v| File.mtime(v) }",
        "comment_created_at": "2025-05-20T20:24:51+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "This is potentially problematic and not necessarily deterministic in that it will likely pick the most recent install vs. probably the intended \"most recent version\" for this logic. Further, although unlikely, any mtime update of the base package directory will place that package at the front of the line for being chosen, so if you renamed the directory or something for a test, you might end up forcing that version to always be chosen?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1688678713",
    "pr_number": 14462,
    "pr_file": "lib/chef/provider/package/chocolatey.rb",
    "created_at": "2024-07-23T20:29:24+00:00",
    "commented_code": "# Choco V2 uses 'Search' for remote repositories and 'List' for local packages\n        def query_command\n          return \"list\" if get_choco_version.match?(/^1/)\n          return \"list\" if get_choco_version.match?(/^1/) && !get_choco_version.match?(/^1.4/)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1688678713",
        "repo_full_name": "chef/chef",
        "pr_number": 14462,
        "pr_file": "lib/chef/provider/package/chocolatey.rb",
        "discussion_id": "1688678713",
        "commented_code": "@@ -153,7 +153,7 @@ def get_choco_version\n \n         # Choco V2 uses 'Search' for remote repositories and 'List' for local packages\n         def query_command\n-          return \"list\" if get_choco_version.match?(/^1/)\n+          return \"list\" if get_choco_version.match?(/^1/) && !get_choco_version.match?(/^1.4/)",
        "comment_created_at": "2024-07-23T20:29:24+00:00",
        "comment_author": "jaymzh",
        "comment_body": "This will break again when 1.5 comes out. We should be a bit more thorough here. Maybe something like...\r\n\r\n```suggestion\r\n          v_bits = get_choco_version.split('.')\r\n          # 1.4+ and 2+\r\n          if v_bits[0].to_i > 1 || v_bits[1] > 3\r\n            return \"search\"\r\n          end\r\n          \"list\"\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1693325682",
        "repo_full_name": "chef/chef",
        "pr_number": 14462,
        "pr_file": "lib/chef/provider/package/chocolatey.rb",
        "discussion_id": "1688678713",
        "commented_code": "@@ -153,7 +153,7 @@ def get_choco_version\n \n         # Choco V2 uses 'Search' for remote repositories and 'List' for local packages\n         def query_command\n-          return \"list\" if get_choco_version.match?(/^1/)\n+          return \"list\" if get_choco_version.match?(/^1/) && !get_choco_version.match?(/^1.4/)",
        "comment_created_at": "2024-07-26T16:29:48+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "@jaymzh I'll raise you a `Gem::Dependency.new('', '< 1.4.0').match?('', get_choco_version)`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1369665177",
    "pr_number": 14043,
    "pr_file": "lib/chef/resource/chocolatey_installer.rb",
    "created_at": "2023-10-24T06:06:30+00:00",
    "commented_code": "class Chef\n  class Resource\n    class ChocolateyInstaller < Chef::Resource\n      provides :chocolatey_installer\n\n      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n      introduced \"18.3\"\n      examples <<~DOC\n          **Install Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n          end\n          ```\n\n          **Uninstall Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'Some random verbiage' do\n            action :uninstall\n          end\n          ```\n\n          **Install Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n            download_url \"https://www.contoso.com/foo\"\n            chocolatey_version '2.12.24'\n          end\n          ```\n\n          **Upgrade Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :upgrade\n            chocolatey_version '2.12.24'\n          end\n          ```\n      DOC\n\n      allowed_actions :install, :uninstall, :upgrade\n\n      property :download_url, String,\n        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n\n      property :chocolatey_version, String,\n        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n\n      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n\n      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n\n      property :proxy_url, String,\n        description: \"Specifies the proxy URL to use during the download.\"\n\n      property :proxy_user, String,\n        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n\n      property :proxy_password, String,\n        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n\n      load_current_value do\n        current_state = is_choco_installed?\n        current_value_does_not_exist! if current_state == false\n        current_state\n      end\n\n      def is_choco_installed?\n        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n      end\n\n      def get_choco_version\n        powershell_exec(\"choco --version\").result\n      end\n\n      def existing_version",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1369665177",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369665177",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version",
        "comment_created_at": "2023-10-24T06:06:30+00:00",
        "comment_author": "jaymzh",
        "comment_body": "Does it conform to gem versions? We have other version helpers if not. Gem versions are very strict.",
        "pr_file_module": null
      },
      {
        "comment_id": "1370147997",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369665177",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version",
        "comment_created_at": "2023-10-24T13:22:33+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "I will convert that over then, I was just using that to have a consistent way of matching versions",
        "pr_file_module": null
      },
      {
        "comment_id": "1370235896",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369665177",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version",
        "comment_created_at": "2023-10-24T14:05:49+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "BTW, got a pointer for me? Everything I read says to use Gem::Version",
        "pr_file_module": null
      },
      {
        "comment_id": "1370368983",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369665177",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version",
        "comment_created_at": "2023-10-24T15:06:29+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "If we're just comparing two *specific* gem versions, `Gem::Version` sounds good to me. If we're looking to have more general version specifiers (`~>`, etc...), it might still work, but we might want to consider how the user would expect things to work in context.",
        "pr_file_module": null
      },
      {
        "comment_id": "1370489394",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369665177",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version",
        "comment_created_at": "2023-10-24T16:23:19+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "I'm a total dork, ignore me. I understand now. I was overthinking this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1092455427",
    "pr_number": 13535,
    "pr_file": "lib/chef/resource/apt_repository.rb",
    "created_at": "2023-01-31T20:37:07+00:00",
    "commented_code": "end.compact\n        end\n\n        # run the specified command and extract the public key ids\n        # accepts the command so it can be used to extract both the current keys\n        # and the new keys\n        # @param [Array<String>] cmd the command to run\n        #\n        # @return [Array] an array of key ids\n        def extract_public_keys_from_cmd(*cmd)\n          so = shell_out(*cmd)\n          # Sample output\n          # pub:-:4096:1:D94AA3F0EFE21092:1336774248:::-:::scSC::::::23::0:\n          so.stdout.split(/\\n/).map do |t|\n            z = t.match(/(^pub:.?:\\d*:\\d*:\\w*:[\\d-]*):/)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1092455427",
        "repo_full_name": "chef/chef",
        "pr_number": 13535,
        "pr_file": "lib/chef/resource/apt_repository.rb",
        "discussion_id": "1092455427",
        "commented_code": "@@ -187,6 +187,22 @@ def extract_fingerprints_from_cmd(*cmd)\n           end.compact\n         end\n \n+        # run the specified command and extract the public key ids\n+        # accepts the command so it can be used to extract both the current keys\n+        # and the new keys\n+        # @param [Array<String>] cmd the command to run\n+        #\n+        # @return [Array] an array of key ids\n+        def extract_public_keys_from_cmd(*cmd)\n+          so = shell_out(*cmd)\n+          # Sample output\n+          # pub:-:4096:1:D94AA3F0EFE21092:1336774248:::-:::scSC::::::23::0:\n+          so.stdout.split(/\\n/).map do |t|\n+            z = t.match(/(^pub:.?:\\d*:\\d*:\\w*:[\\d-]*):/)",
        "comment_created_at": "2023-01-31T20:37:07+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Suggest splitting on the `':'` and grabbing the first `n` fields rejoined with `':'` ... It's a little bit harder to sort out how many fields are being grabbed with the regex especially with most of this under the capture group, and the regex isn't performing significant validation, etc...",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "930358767",
    "pr_number": 13069,
    "pr_file": "lib/chef/property.rb",
    "created_at": "2022-07-26T19:56:06+00:00",
    "commented_code": "#\n    def required?(action = nil)\n      if !action.nil? && options[:required].is_a?(Array)\n        options[:required].include?(action)\n        (options[:required] & Array(action)).any?",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "930358767",
        "repo_full_name": "chef/chef",
        "pr_number": 13069,
        "pr_file": "lib/chef/property.rb",
        "discussion_id": "930358767",
        "commented_code": "@@ -305,7 +305,7 @@ def has_default?\n     #\n     def required?(action = nil)\n       if !action.nil? && options[:required].is_a?(Array)\n-        options[:required].include?(action)\n+        (options[:required] & Array(action)).any?",
        "comment_created_at": "2022-07-26T19:56:06+00:00",
        "comment_author": "marcparadise",
        "comment_body": "How does this functionally differ from the original check? When running through some scenarios, I can't come up with one that returns a different result given pre-conditions of  a non-nil action and :required having an Array. ",
        "pr_file_module": null
      },
      {
        "comment_id": "934692971",
        "repo_full_name": "chef/chef",
        "pr_number": 13069,
        "pr_file": "lib/chef/property.rb",
        "discussion_id": "930358767",
        "commented_code": "@@ -305,7 +305,7 @@ def has_default?\n     #\n     def required?(action = nil)\n       if !action.nil? && options[:required].is_a?(Array)\n-        options[:required].include?(action)\n+        (options[:required] & Array(action)).any?",
        "comment_created_at": "2022-08-01T16:05:49+00:00",
        "comment_author": "sabat",
        "comment_body": "> How does this functionally differ from the original check?\r\n\r\nThe original cannot handle a check for multiple actions. It's fine if it's checking for just :create for example, but if `action` is an array with both :create and :delete it would fail with a simple `include?` test. I wrote this over a year ago and the details of the context now escape me, but IIRC there are situations where this needs to test for multiple actions\u2014where `action` is going to be an array of actions, and `include?` only tests for the presence of a single object.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "438615154",
    "pr_number": 9976,
    "pr_file": "lib/chef/provider/package/apt.rb",
    "created_at": "2020-06-11T08:09:39+00:00",
    "commented_code": "end\n\n        def install_package(name, version)\n          name = check_availability(name)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "438615154",
        "repo_full_name": "chef/chef",
        "pr_number": 9976,
        "pr_file": "lib/chef/provider/package/apt.rb",
        "discussion_id": "438615154",
        "commented_code": "@@ -89,6 +89,7 @@ def locked_packages\n         end\n \n         def install_package(name, version)\n+          name = check_availability(name)",
        "comment_created_at": "2020-06-11T08:09:39+00:00",
        "comment_author": "jaymzh",
        "comment_body": "This only fixes... part of the bug.\r\n\r\nIt will ensure that if you try to purge `['a', 'b', 'c']` and `c` isn't a known package, that it won't try to purge `c`... which is good...\r\n\r\nBut the actual bug is that if `a` is installed, it'll automatically try to uninstall `b`, and `c` even if they are not installed.\r\n\r\nSo imagine:\r\n* a - installed\r\n* b - uninstalled, but available\r\n* c - uninstalled and unavailable\r\n\r\nCurrent behavior is Chef will try to purge `a`, `b` and `c`\r\n\r\nWith your PR it'll just try to purge `a` and `b`\r\n\r\nBut the *right* behavior is that it should only try to purge `a`.",
        "pr_file_module": null
      }
    ]
  }
]
