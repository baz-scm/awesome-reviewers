---
title: Explicit configuration over implicit
description: 'Always define explicit configuration defaults rather than relying on
  implicit behavior or autovivification. Configuration values should:


  1. Use explicit nil defaults instead of undefined values'
repository: chef/chef
label: Configurations
language: Ruby
comments_count: 5
repository_stars: 7860
---

Always define explicit configuration defaults rather than relying on implicit behavior or autovivification. Configuration values should:

1. Use explicit nil defaults instead of undefined values
2. Document default values clearly in property descriptions
3. Use Chef::Config for global settings rather than environment variables
4. Consider platform-specific variations when defining defaults

Example:
```ruby
# Bad - Implicit default
property :store_location, String

# Good - Explicit default with clear documentation
property :store_location, String,
  default: nil,
  description: "Use the `CurrentUser` store instead of the default `LocalMachine` store."

# Bad - Environment variable configuration
default :use_s3_cache, ENV['USE_S3_CACHE'] == 'true'

# Good - Chef::Config configuration
config_context :caching do
  default :use_s3, false
end
```

This approach improves code clarity, makes behavior more predictable, and ensures proper documentation of configuration options. It also facilitates better testing and maintenance by making all possible states explicit.


[
  {
    "discussion_id": "392394938",
    "pr_number": 9480,
    "pr_file": "chef-config/lib/chef-config/config.rb",
    "created_at": "2020-03-13T18:17:13+00:00",
    "commented_code": "# can be set to a string or array of strings for URIs to set as rubygems sources\n    default :rubygems_url, \"https://www.rubygems.org\"\n\n    # globally sets the default of the clear_sources property on the gem_package and chef_gem resources\n    default :clear_gem_sources, false",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "392394938",
        "repo_full_name": "chef/chef",
        "pr_number": 9480,
        "pr_file": "chef-config/lib/chef-config/config.rb",
        "discussion_id": "392394938",
        "commented_code": "@@ -1221,9 +1221,6 @@ def self.guess_internal_locale\n     # can be set to a string or array of strings for URIs to set as rubygems sources\n     default :rubygems_url, \"https://www.rubygems.org\"\n \n-    # globally sets the default of the clear_sources property on the gem_package and chef_gem resources\n-    default :clear_gem_sources, false",
        "comment_created_at": "2020-03-13T18:17:13+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "this should probably be changed to an explicit nil default rather than relying on chef-config autovivification (for documentation purposes if nothing else, but i think we actually consume chef-config and turn on strict checking for something like berkshelf as well -- we always intended to turn on strict checking in chef-client but never did)",
        "pr_file_module": null
      },
      {
        "comment_id": "392397904",
        "repo_full_name": "chef/chef",
        "pr_number": 9480,
        "pr_file": "chef-config/lib/chef-config/config.rb",
        "discussion_id": "392394938",
        "commented_code": "@@ -1221,9 +1221,6 @@ def self.guess_internal_locale\n     # can be set to a string or array of strings for URIs to set as rubygems sources\n     default :rubygems_url, \"https://www.rubygems.org\"\n \n-    # globally sets the default of the clear_sources property on the gem_package and chef_gem resources\n-    default :clear_gem_sources, false",
        "comment_created_at": "2020-03-13T18:23:01+00:00",
        "comment_author": "phiggins",
        "comment_body": "I wondered about that, I agree it makes sense to be more explicit.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1369663852",
    "pr_number": 14043,
    "pr_file": "lib/chef/resource/chocolatey_installer.rb",
    "created_at": "2023-10-24T06:04:17+00:00",
    "commented_code": "class Chef\n  class Resource\n    class ChocolateyInstaller < Chef::Resource\n      provides :chocolatey_installer\n\n      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n      introduced \"18.3\"\n      examples <<~DOC\n          **Install Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n          end\n          ```\n\n          **Uninstall Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'Some random verbiage' do\n            action :uninstall\n          end\n          ```\n\n          **Install Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n            download_url \"https://www.contoso.com/foo\"\n            chocolatey_version '2.12.24'\n          end\n          ```\n\n          **Upgrade Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :upgrade\n            chocolatey_version '2.12.24'\n          end\n          ```\n      DOC\n\n      allowed_actions :install, :uninstall, :upgrade\n\n      property :download_url, String,\n        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1369663852",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369663852",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
        "comment_created_at": "2023-10-24T06:04:17+00:00",
        "comment_author": "jaymzh",
        "comment_body": "We don't usually consult env vars from cookbooks.  It breaks idempotency... Two prior with different environments running this could move the install back and forth between different versions. I highly highly recommend against this.",
        "pr_file_module": null
      },
      {
        "comment_id": "1370132968",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369663852",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
        "comment_created_at": "2023-10-24T13:11:30+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "I have a question - this defaults to a choco repo if you specify nothing. The point of this url is the use case where a random update needs to be downloaded from an alternate source. It does not need to be idempotent. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1370782643",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369663852",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
        "comment_created_at": "2023-10-24T20:34:50+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Per our discussion, this is actually being used directly by the Chocolatey `install.ps1` script and the environment variable can be used to redirect the standard installer to an alternate location.",
        "pr_file_module": null
      },
      {
        "comment_id": "1373353325",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369663852",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
        "comment_created_at": "2023-10-26T15:21:37+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "@johnmccrae can we made the description more clear that it's the choco installer itself looking at these variables?",
        "pr_file_module": null
      },
      {
        "comment_id": "1376478178",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1369663852",
        "commented_code": "@@ -0,0 +1,198 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the Chocolatey Installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"",
        "comment_created_at": "2023-10-30T16:10:07+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "done and spelling error corrected too",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "596231507",
    "pr_number": 11189,
    "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
    "created_at": "2021-03-17T17:21:24+00:00",
    "commented_code": "end\n\n          unless chef_config[:file_cache_path].nil?\n            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "596231507",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-03-17T17:21:24+00:00",
        "comment_author": "marcparadise",
        "comment_body": "is it safe to use `windows: false` here? Shouldn't that depend on the remote OS? ",
        "pr_file_module": null
      },
      {
        "comment_id": "596244553",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-03-17T17:37:22+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "we've got the windows_bootstrap_context which handles bootstrapping a windows node.  this should properly be called unix_bootstrap_context or something, but history.",
        "pr_file_module": null
      },
      {
        "comment_id": "596245747",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-03-17T17:38:44+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "whats a bit more concerning is this is now hardcoding the last bit of this path.",
        "pr_file_module": null
      },
      {
        "comment_id": "596250612",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-03-17T17:45:07+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "we probably need to introduce new config variables `unix_bootstrap_file_cache_path` and `unix_bootstrap_file_backup_path` which should default to these values and allow the user to override them.  then should probably do the same for windows.",
        "pr_file_module": null
      },
      {
        "comment_id": "600197351",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-03-24T06:07:36+00:00",
        "comment_author": "snehaldwivedi",
        "comment_body": "@lamont-granquist I have tried adding the new variable and separate definitions  for defining  `chef_dir`, `root_dir` & `cache_path` for Linux  in [config.rb](https://github.com/chef/chef/blob/master/chef-config/lib/chef-config/config.rb). But I got stuck [here](https://github.com/chef/chef/blob/master/chef-config/lib/chef-config/config.rb#L372), where we need to get a home path of the remote node. I think we need to update `ChefUtils` to get the object of the remote OS.\r\n\r\nPlease let me know your suggestion on this.",
        "pr_file_module": null
      },
      {
        "comment_id": "626866599",
        "repo_full_name": "chef/chef",
        "pr_number": 11189,
        "pr_file": "lib/chef/knife/core/bootstrap_context.rb",
        "discussion_id": "596231507",
        "commented_code": "@@ -172,11 +172,11 @@ def config_content\n           end\n \n           unless chef_config[:file_cache_path].nil?\n-            client_rb << \"file_cache_path \\\"#{chef_config[:file_cache_path]}\\\"\\n\"\n+            client_rb << \"file_cache_path \\\"#{ChefConfig::PathHelper.escapepath(ChefConfig::Config.var_chef_dir(windows: false))}/cache\\\"\\n\"",
        "comment_created_at": "2021-05-05T20:13:08+00:00",
        "comment_author": "btm",
        "comment_body": "@snehaldwivedi ChefUtils does have a little bit of train in it and can get the remote OS, but it is for target mode, knife bootstrap has its own use of train.\r\n\r\n`ChefConfig::Mixin::TrainTransport` is used for target mode, not bootstrap.\r\n`ChefUtils::DSL::TrainHelpers` ultimately uses the train connection off the run_context for target mode\r\n`Chef::Knife::Bootstrap::TrainConnector` is used for knife bootstrap.\r\n\r\nThe amount of complexity that ChefConfig has around switching for windows or linux, local mode or target mode, and changing path names for the official or community distributions is already a lot and easy to break one of the many scenarios. Trying to add knife bootstrap or not knife bootstrap to that list is over the top.\r\n\r\nFor just knife bootstrap use in chef-config we could add something like this:\r\n```\r\ndefault(:unix_bootstrap_file_cache_path) do\r\n    PathHelper.join(\"/var\", ChefUtils::Dist::Infra::DIR_SUFFIX, \"cache\", windows: false)\r\nend\r\n\r\ndefault(:windows_bootstrap_file_cache_path) do\r\n  PathHelper.join(\"C:\", ChefUtils::Dist::Infra::DIR_SUFFIX, \"cache\", windows: true)\r\nend\r\n```\r\n\r\nIf someone needed something special (like probably we leave C: hardcoded) then they could put a different `windows_bootstrap_file_cache_path` in their config.rb.\r\n\r\nThen we mostly need to go through `bootstrap_context.rb` and `windows_bootstrap_context.rb` and make them use the appropriate new variable instead of `file_cache_path`, and update the tests. And do a little manual testing.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1893160030",
    "pr_number": 14131,
    "pr_file": "lib/chef/resource/apt_repository.rb",
    "created_at": "2024-12-19T21:18:33+00:00",
    "commented_code": "property :key_proxy, [String, nil, FalseClass],\n        description: \"If set, a specified proxy is passed to GPG via `http-proxy=`.\"\n\n      property :signed_by, [String, true, false, nil],\n        description: \"If a string, specify the file and/or fingerprint the repo is signed with. If true, set Signed-With to use the specified key\",\n        default: nil",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1893160030",
        "repo_full_name": "chef/chef",
        "pr_number": 14131,
        "pr_file": "lib/chef/resource/apt_repository.rb",
        "discussion_id": "1893160030",
        "commented_code": "@@ -164,6 +164,10 @@ class AptRepository < Chef::Resource\n       property :key_proxy, [String, nil, FalseClass],\n         description: \"If set, a specified proxy is passed to GPG via `http-proxy=`.\"\n \n+      property :signed_by, [String, true, false, nil],\n+        description: \"If a string, specify the file and/or fingerprint the repo is signed with. If true, set Signed-With to use the specified key\",\n+        default: nil",
        "comment_created_at": "2024-12-19T21:18:33+00:00",
        "comment_author": "tmccombs",
        "comment_body": "Should this default to true, or conditionally default to true?",
        "pr_file_module": null
      },
      {
        "comment_id": "1894307957",
        "repo_full_name": "chef/chef",
        "pr_number": 14131,
        "pr_file": "lib/chef/resource/apt_repository.rb",
        "discussion_id": "1893160030",
        "commented_code": "@@ -164,6 +164,10 @@ class AptRepository < Chef::Resource\n       property :key_proxy, [String, nil, FalseClass],\n         description: \"If set, a specified proxy is passed to GPG via `http-proxy=`.\"\n \n+      property :signed_by, [String, true, false, nil],\n+        description: \"If a string, specify the file and/or fingerprint the repo is signed with. If true, set Signed-With to use the specified key\",\n+        default: nil",
        "comment_created_at": "2024-12-20T19:21:44+00:00",
        "comment_author": "williamtheaker",
        "comment_body": "Since 16.04 is the oldest version currently supported, I think this should be true by default.\r\nhttps://docs.chef.io/platforms/#commercial-support-4",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "561415718",
    "pr_number": 10909,
    "pr_file": "lib/chef/resource/windows_certificate.rb",
    "created_at": "2021-01-21T00:14:29+00:00",
    "commented_code": "default: \"MY\", equal_to: [\"TRUSTEDPUBLISHER\", \"TrustedPublisher\", \"CLIENTAUTHISSUER\", \"REMOTE DESKTOP\", \"ROOT\", \"TRUSTEDDEVICES\", \"WEBHOSTING\", \"CA\", \"AUTHROOT\", \"TRUSTEDPEOPLE\", \"MY\", \"SMARTCARDROOT\", \"TRUST\", \"DISALLOWED\"]\n\n      property :user_store, [TrueClass, FalseClass],\n        description: \"Use the user store of the local machine store if set to false.\",\n        description: \"Use the CurrentUser store if set to true or the LocalMachine store if set to false.\",",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "561415718",
        "repo_full_name": "chef/chef",
        "pr_number": 10909,
        "pr_file": "lib/chef/resource/windows_certificate.rb",
        "discussion_id": "561415718",
        "commented_code": "@@ -76,7 +76,7 @@ class WindowsCertificate < Chef::Resource\n         default: \"MY\", equal_to: [\"TRUSTEDPUBLISHER\", \"TrustedPublisher\", \"CLIENTAUTHISSUER\", \"REMOTE DESKTOP\", \"ROOT\", \"TRUSTEDDEVICES\", \"WEBHOSTING\", \"CA\", \"AUTHROOT\", \"TRUSTEDPEOPLE\", \"MY\", \"SMARTCARDROOT\", \"TRUST\", \"DISALLOWED\"]\n \n       property :user_store, [TrueClass, FalseClass],\n-        description: \"Use the user store of the local machine store if set to false.\",\n+        description: \"Use the CurrentUser store if set to true or the LocalMachine store if set to false.\",",
        "comment_created_at": "2021-01-21T00:14:29+00:00",
        "comment_author": "tas50",
        "comment_body": "```suggestion\r\n        description: \"Use the `CurrentUser` store instead of the default `LocalMachine` store.\",\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
