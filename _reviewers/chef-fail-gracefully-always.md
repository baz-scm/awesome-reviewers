---
title: Fail gracefully always
description: 'Ensure code handles errors robustly by using protective patterns that
  prevent resource leaks, provide clear diagnostics, and degrade gracefully when possible:'
repository: chef/chef
label: Error Handling
language: Ruby
comments_count: 9
repository_stars: 7860
---

Ensure code handles errors robustly by using protective patterns that prevent resource leaks, provide clear diagnostics, and degrade gracefully when possible:

1. **Use resource cleanup patterns** - Prefer block forms for resource management to ensure cleanup happens even during exceptions:

```ruby
# Good: Resources automatically closed after block
TargetIO::File.open(tempname, "w") do |tempfile|
  tempfile.write(crontab)
end

# Bad: Manual cleanup may be missed on exception paths
tempfile = TargetIO::File.open(tempname, "w") 
tempfile.write(crontab)
tempfile.close # Might never execute if an exception occurs
```

2. **Validate related parameters together** - Check parameter dependencies upfront:

```ruby
# Good: Clear validation of dependent parameters
def define_resource_requirements
  requirements.assert(:install, :upgrade) do |a|
    a.assertion { new_resource.proxy_user.nil? == new_resource.proxy_password.nil? }
    a.failure_message("Both proxy_user and proxy_password must be specified together")
  end
end
```

3. **Handle expected failures gracefully** - Catch specific exceptions to provide fallbacks:

```ruby
# Good: Handle missing command gracefully
def loop_mount_points
  @loop_mount_points ||= shell_out!("losetup -a").stdout
rescue Errno::ENOENT
  "" # Return empty string if command doesn't exist
end
```

4. **Use appropriate exception types** - Choose domain-specific exceptions to accurately represent errors:

```ruby
# Good: Domain-specific exception
raise Chef::Exceptions::Service, "systemctl show not reporting status for #{service_name}!"

# Bad: Using generic or misleading exception type
raise Mixlib::ShellOut::ShellCommandFailed, "Error message" # Implies shell command failed
```

5. **Provide clear, actionable error messages** - Check specific conditions and give targeted feedback:

```ruby
# Good: Check existence before permissions
if !File.directory?(File.dirname(file))
  ui.fatal "Directory #{File.dirname(file)} does not exist"
  exit 1
elsif !File.writable?(File.dirname(file))
  ui.fatal "Directory #{File.dirname(file)} is not writable. Check permissions."
  exit 1
end
```

Following these patterns will create more resilient code that fails predictably, provides clear diagnostics, and properly manages resources even during failures.


[
  {
    "discussion_id": "2110148468",
    "pr_number": 15015,
    "pr_file": "lib/chef/provider/cron.rb",
    "created_at": "2025-05-27T20:24:45+00:00",
    "commented_code": "write_exception = false\n\n        tempname = Dir::Tmpname.create([\"crontab-\"]) {}\n        TargetIO::File.open(tempname, \"w\") do |tempfile|\n        io = TargetIO::File.open(tempname, \"w\") do |tempfile|\n          tempfile.write(crontab)\n        end\n\n        tempname = io.path if ChefConfig::Config.target_mode?\n\n        so = shell_out!(\"crontab -u #{new_resource.user} #{tempname}\")\n\n        TargetIO::File.unlink(tempname)\n        TargetIO::File.unlink(tempname) if ChefConfig::Config.target_mode?",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2110148468",
        "repo_full_name": "chef/chef",
        "pr_number": 15015,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "2110148468",
        "commented_code": "@@ -206,13 +206,15 @@ def write_crontab(crontab)\n         write_exception = false\n \n         tempname = Dir::Tmpname.create([\"crontab-\"]) {}\n-        TargetIO::File.open(tempname, \"w\") do |tempfile|\n+        io = TargetIO::File.open(tempname, \"w\") do |tempfile|\n           tempfile.write(crontab)\n         end\n \n+        tempname = io.path if ChefConfig::Config.target_mode?\n+\n         so = shell_out!(\"crontab -u #{new_resource.user} #{tempname}\")\n \n-        TargetIO::File.unlink(tempname)\n+        TargetIO::File.unlink(tempname) if ChefConfig::Config.target_mode?",
        "comment_created_at": "2025-05-27T20:24:45+00:00",
        "comment_author": "jaymzh",
        "comment_body": "we still need to remove the local tmpfile, even if we're not in targetmode, just like we did before. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2115981160",
        "repo_full_name": "chef/chef",
        "pr_number": 15015,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "2110148468",
        "commented_code": "@@ -206,13 +206,15 @@ def write_crontab(crontab)\n         write_exception = false\n \n         tempname = Dir::Tmpname.create([\"crontab-\"]) {}\n-        TargetIO::File.open(tempname, \"w\") do |tempfile|\n+        io = TargetIO::File.open(tempname, \"w\") do |tempfile|\n           tempfile.write(crontab)\n         end\n \n+        tempname = io.path if ChefConfig::Config.target_mode?\n+\n         so = shell_out!(\"crontab -u #{new_resource.user} #{tempname}\")\n \n-        TargetIO::File.unlink(tempname)\n+        TargetIO::File.unlink(tempname) if ChefConfig::Config.target_mode?",
        "comment_created_at": "2025-05-30T13:56:30+00:00",
        "comment_author": "thheinen",
        "comment_body": "Ouch! Good catch, thanks.",
        "pr_file_module": null
      },
      {
        "comment_id": "2121703656",
        "repo_full_name": "chef/chef",
        "pr_number": 15015,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "2110148468",
        "commented_code": "@@ -206,13 +206,15 @@ def write_crontab(crontab)\n         write_exception = false\n \n         tempname = Dir::Tmpname.create([\"crontab-\"]) {}\n-        TargetIO::File.open(tempname, \"w\") do |tempfile|\n+        io = TargetIO::File.open(tempname, \"w\") do |tempfile|\n           tempfile.write(crontab)\n         end\n \n+        tempname = io.path if ChefConfig::Config.target_mode?\n+\n         so = shell_out!(\"crontab -u #{new_resource.user} #{tempname}\")\n \n-        TargetIO::File.unlink(tempname)\n+        TargetIO::File.unlink(tempname) if ChefConfig::Config.target_mode?",
        "comment_created_at": "2025-06-02T16:56:12+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "@thheinen is this updated per Phil's last comment, or can we merge it?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1906074481",
    "pr_number": 14770,
    "pr_file": "lib/chef/resource/archive_file.rb",
    "created_at": "2025-01-07T21:40:32+00:00",
    "commented_code": "archive.each_entry do |e|\n              FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n            end\n            archive.close",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1906074481",
        "repo_full_name": "chef/chef",
        "pr_number": 14770,
        "pr_file": "lib/chef/resource/archive_file.rb",
        "discussion_id": "1906074481",
        "commented_code": "@@ -129,6 +129,7 @@ class ArchiveFile < Chef::Resource\n             archive.each_entry do |e|\n               FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n             end\n+            archive.close",
        "comment_created_at": "2025-01-07T21:40:32+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Looks like [`open_filename`](https://github.com/chef/ffi-libarchive/blob/545d3948e7a78835da48737c1490516905fad2e6/lib/ffi-libarchive/writer.rb#L5) takes a block, and so this would be cleaner and automatically `ensure` closure if these calls were converted to that pattern.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1371767924",
    "pr_number": 14043,
    "pr_file": "lib/chef/resource/chocolatey_installer.rb",
    "created_at": "2023-10-25T13:30:41+00:00",
    "commented_code": "class Chef\n  class Resource\n    class ChocolateyInstaller < Chef::Resource\n      provides :chocolatey_installer\n\n      description \"Use the chocolatey_installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n      introduced \"18.3\"\n      examples <<~DOC\n          **Install Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n          end\n          ```\n\n          **Uninstall Chocolatey**\n\n          ```ruby\n          chocolatey_installer 'Some random verbiage' do\n            action :uninstall\n          end\n          ```\n\n          **Install Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :install\n            download_url \"https://www.contoso.com/foo\"\n            chocolatey_version '2.12.24'\n          end\n          ```\n\n          **Upgrade Chocolatey with Parameters**\n\n          ```ruby\n          chocolatey_installer 'latest' do\n            action :upgrade\n            chocolatey_version '2.12.24'\n          end\n          ```\n      DOC\n\n      allowed_actions :install, :uninstall, :upgrade\n\n      property :download_url, String,\n        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n\n      property :chocolatey_version, String,\n        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n\n      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n\n      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n\n      property :proxy_url, String,\n        description: \"Specifies the proxy URL to use during the download.\"\n\n      property :proxy_user, String,\n        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n\n      property :proxy_password, String,\n        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n\n      load_current_value do\n        current_state = is_choco_installed?\n        current_value_does_not_exist! if current_state == false\n        current_state\n      end\n\n      def is_choco_installed?\n        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n      end\n\n      def get_choco_version\n        powershell_exec(\"choco --version\").result\n      end\n\n      def existing_version\n        Gem::Version.new(get_choco_version)\n      end\n\n      def define_resource_requirements\n        requirements.assert(:install, :upgrade).each do |a|\n          a.assertion do\n            (new_resource.proxy_user.nil? != new_resource.proxy_password.nil?)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1371767924",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1371767924",
        "commented_code": "@@ -0,0 +1,195 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the chocolatey_installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version\n+        Gem::Version.new(get_choco_version)\n+      end\n+\n+      def define_resource_requirements\n+        requirements.assert(:install, :upgrade).each do |a|\n+          a.assertion do\n+            (new_resource.proxy_user.nil? != new_resource.proxy_password.nil?)",
        "comment_created_at": "2023-10-25T13:30:41+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Go ahead and remove the parens and comment that we want an error if only one of (proxy_user, proxy_password) are true.",
        "pr_file_module": null
      },
      {
        "comment_id": "1376479210",
        "repo_full_name": "chef/chef",
        "pr_number": 14043,
        "pr_file": "lib/chef/resource/chocolatey_installer.rb",
        "discussion_id": "1371767924",
        "commented_code": "@@ -0,0 +1,195 @@\n+class Chef\n+  class Resource\n+    class ChocolateyInstaller < Chef::Resource\n+      provides :chocolatey_installer\n+\n+      description \"Use the chocolatey_installer resource to ensure that Choco is installed to your specification. Use the Chocolatey Feature resource to customize your install\"\n+      introduced \"18.3\"\n+      examples <<~DOC\n+          **Install Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+          end\n+          ```\n+\n+          **Uninstall Chocolatey**\n+\n+          ```ruby\n+          chocolatey_installer 'Some random verbiage' do\n+            action :uninstall\n+          end\n+          ```\n+\n+          **Install Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :install\n+            download_url \"https://www.contoso.com/foo\"\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+\n+          **Upgrade Chocolatey with Parameters**\n+\n+          ```ruby\n+          chocolatey_installer 'latest' do\n+            action :upgrade\n+            chocolatey_version '2.12.24'\n+          end\n+          ```\n+      DOC\n+\n+      allowed_actions :install, :uninstall, :upgrade\n+\n+      property :download_url, String,\n+        description: \"The URL to download Chocolatey from. This defaults to the value of $env:ChocolateyDownloadUrl, if it is set, and otherwise falls back to the official Chocolatey community repository to download the Chocolatey package. It can be used for offline installation by providing a path to a Chocolatey.nupkg.\"\n+\n+      property :chocolatey_version, String,\n+        description: \"Specifies a target version of Chocolatey to install. By default, the latest stable version is installed. This will use the value in $env:ChocolateyVersion by default, if that environment variable is present. This parameter is ignored if download_url is set.\"\n+\n+      property :use_native_unzip, [TrueClass, FalseClass], default: false,\n+        description: \"If set, uses built-in Windows decompression tools instead of 7zip when unpacking the downloaded nupkg. This will be set by default if use_native_unzip is set to a value other than 'false' or '0'. This parameter will be ignored in PS 5+ in favour of using the Expand-Archive built in PowerShell cmdlet directly.\"\n+\n+      property :ignore_proxy, [TrueClass, FalseClass], default: false,\n+        description: \"If set, ignores any configured proxy. This will override any proxy environment variables or parameters. This will be set by default if ignore_proxy is set to a value other than 'false' or '0'.\"\n+\n+      property :proxy_url, String,\n+        description: \"Specifies the proxy URL to use during the download.\"\n+\n+      property :proxy_user, String,\n+        description: \"The username to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_password are set\"\n+\n+      property :proxy_password, String,\n+        description: \"The password to use to build a proxy credential with. Will be consumed by the proxy_credential property if both this property and proxy_user are set\"\n+\n+      load_current_value do\n+        current_state = is_choco_installed?\n+        current_value_does_not_exist! if current_state == false\n+        current_state\n+      end\n+\n+      def is_choco_installed?\n+        ::File.exist?(\"#{ENV[\"ALLUSERSPROFILE\"]}\\\\chocolatey\\\\bin\\\\choco.exe\")\n+      end\n+\n+      def get_choco_version\n+        powershell_exec(\"choco --version\").result\n+      end\n+\n+      def existing_version\n+        Gem::Version.new(get_choco_version)\n+      end\n+\n+      def define_resource_requirements\n+        requirements.assert(:install, :upgrade).each do |a|\n+          a.assertion do\n+            (new_resource.proxy_user.nil? != new_resource.proxy_password.nil?)",
        "comment_created_at": "2023-10-30T16:10:54+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1004881372",
    "pr_number": 13107,
    "pr_file": "lib/chef/chef_fs/file_system.rb",
    "created_at": "2022-10-25T19:23:01+00:00",
    "commented_code": "ui.output \"Would update #{dest_path}\" if ui\n                    else\n                      src_value = src_entry.read if src_value.nil?\n                      result[\"total\"] += 1\n                      dest_entry.write(src_value)\n                      result[\"success_count\"] += 1\n                      ui.output \"Updated #{dest_path}\" if ui\n                    end\n                  end\n                end\n              end\n            end\n          rescue RubyFileError => e\n            # result[\"failed\"].append(username)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1004881372",
        "repo_full_name": "chef/chef",
        "pr_number": 13107,
        "pr_file": "lib/chef/chef_fs/file_system.rb",
        "discussion_id": "1004881372",
        "commented_code": "@@ -389,14 +391,17 @@ def copy_entries(src_entry, dest_entry, new_dest_parent, recurse_depth, options,\n                       ui.output \"Would update #{dest_path}\" if ui\n                     else\n                       src_value = src_entry.read if src_value.nil?\n+                      result[\"total\"] += 1\n                       dest_entry.write(src_value)\n+                      result[\"success_count\"] += 1\n                       ui.output \"Updated #{dest_path}\" if ui\n                     end\n                   end\n                 end\n               end\n             end\n           rescue RubyFileError => e\n+            # result[\"failed\"].append(username)",
        "comment_created_at": "2022-10-25T19:23:01+00:00",
        "comment_author": "marcparadise",
        "comment_body": "We should be capturing failures here and in the other exception cases, so that we can return failure information (file and error) as well. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "986222711",
    "pr_number": 13223,
    "pr_file": "lib/chef/provider/user/linux.rb",
    "created_at": "2022-10-03T20:57:22+00:00",
    "commented_code": "@change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"\n            end\n          end\n\n          !@change_desc.empty?",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "986222711",
        "repo_full_name": "chef/chef",
        "pr_number": 13223,
        "pr_file": "lib/chef/provider/user/linux.rb",
        "discussion_id": "986222711",
        "commented_code": "@@ -37,6 +37,8 @@ def compare_user\n               @change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"\n             end\n           end\n+\n+          !@change_desc.empty?",
        "comment_created_at": "2022-10-03T20:57:22+00:00",
        "comment_author": "marcparadise",
        "comment_body": "This is a little opaque - this function relies on the fact that super also modifies `@change_desc`. That's internal to the base class though, and not something that we should rely on.\r\n\r\nCould we instead do something like: \r\n```\r\nuser_changed  = super\r\n...\r\n-snip-\r\n...\r\nuser_changed || !change_desc.empty? \r\n```\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "986726796",
        "repo_full_name": "chef/chef",
        "pr_number": 13223,
        "pr_file": "lib/chef/provider/user/linux.rb",
        "discussion_id": "986222711",
        "commented_code": "@@ -37,6 +37,8 @@ def compare_user\n               @change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"\n             end\n           end\n+\n+          !@change_desc.empty?",
        "comment_created_at": "2022-10-04T11:01:54+00:00",
        "comment_author": "fretb",
        "comment_body": "Hi Marc, good input, I changed it.",
        "pr_file_module": null
      },
      {
        "comment_id": "987630641",
        "repo_full_name": "chef/chef",
        "pr_number": 13223,
        "pr_file": "lib/chef/provider/user/linux.rb",
        "discussion_id": "986222711",
        "commented_code": "@@ -37,6 +37,8 @@ def compare_user\n               @change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"\n             end\n           end\n+\n+          !@change_desc.empty?",
        "comment_created_at": "2022-10-05T07:52:13+00:00",
        "comment_author": "Tensibai",
        "comment_body": "In this case @change_desc should be initialized after the call to super too or the risk is that super didn't create the change_desc property and ` @change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"` will raise a no method error for << on nil.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "987720632",
        "repo_full_name": "chef/chef",
        "pr_number": 13223,
        "pr_file": "lib/chef/provider/user/linux.rb",
        "discussion_id": "986222711",
        "commented_code": "@@ -37,6 +37,8 @@ def compare_user\n               @change_desc << \"change #{user_attrib} from #{cur_val} to #{new_val}\"\n             end\n           end\n+\n+          !@change_desc.empty?",
        "comment_created_at": "2022-10-05T09:29:20+00:00",
        "comment_author": "Tensibai",
        "comment_body": "Another approach could be as in the mac user provider to rewrite the whole method: https://github.com/chef/chef/blob/main/lib/chef/provider/user/mac.rb#L222-L234 ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "377245838",
    "pr_number": 8340,
    "pr_file": "lib/chef/provider/cron.rb",
    "created_at": "2020-02-10T18:43:32+00:00",
    "commented_code": "end\n      attr_accessor :cron_exists, :cron_empty\n\n      def check_resource_semantics!\n        return if Process.euid == 0\n\n        etype = Chef::Exceptions::Cron\n        begin\n          nuid = Etc.getpwnam(new_resource.user).uid\n        rescue ArgumentError\n          emessage = \"Error in #{new_resource.name}, #{new_resource.user} does not exists on this system.\"\n          events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n          if why_run?\n            events.whyrun_assumption(new_resource.action, new_resource.name, \"Assuming user #{new_resource.user} would have been acted upon.\")\n          else\n            raise etype, emessage\n          end\n        end\n        return if nuid == Process.euid\n\n        emessage = \"Error in #{new_resource.name}, Chef can't modify another user crontab when not running as root.\"\n        events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n        raise etype, emessage\n      end",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "377245838",
        "repo_full_name": "chef/chef",
        "pr_number": 8340,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "377245838",
        "commented_code": "@@ -41,11 +41,34 @@ def initialize(new_resource, run_context)\n       end\n       attr_accessor :cron_exists, :cron_empty\n \n+      def check_resource_semantics!\n+        return if Process.euid == 0\n+\n+        etype = Chef::Exceptions::Cron\n+        begin\n+          nuid = Etc.getpwnam(new_resource.user).uid\n+        rescue ArgumentError\n+          emessage = \"Error in #{new_resource.name}, #{new_resource.user} does not exists on this system.\"\n+          events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+          if why_run?\n+            events.whyrun_assumption(new_resource.action, new_resource.name, \"Assuming user #{new_resource.user} would have been acted upon.\")\n+          else\n+            raise etype, emessage\n+          end\n+        end\n+        return if nuid == Process.euid\n+\n+        emessage = \"Error in #{new_resource.name}, Chef can't modify another user crontab when not running as root.\"\n+        events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+        raise etype, emessage\n+      end",
        "comment_created_at": "2020-02-10T18:43:32+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "this should probably be moved to `defined_resource_requirements` and use the typical assertion syntax there.  if the point is to protect load_current_resource from exploding, then LCR really needs to be made 'safe' for the cases when the user doesn't exist and/or the thing isn't being run as root (should just return a bunch of nil stuff for what it can't get at).\r\n\r\nwhat you're doing here with directly handling your own why run assertions is waaaaaay too complicated to follow for 99% of humans.",
        "pr_file_module": null
      },
      {
        "comment_id": "377363770",
        "repo_full_name": "chef/chef",
        "pr_number": 8340,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "377245838",
        "commented_code": "@@ -41,11 +41,34 @@ def initialize(new_resource, run_context)\n       end\n       attr_accessor :cron_exists, :cron_empty\n \n+      def check_resource_semantics!\n+        return if Process.euid == 0\n+\n+        etype = Chef::Exceptions::Cron\n+        begin\n+          nuid = Etc.getpwnam(new_resource.user).uid\n+        rescue ArgumentError\n+          emessage = \"Error in #{new_resource.name}, #{new_resource.user} does not exists on this system.\"\n+          events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+          if why_run?\n+            events.whyrun_assumption(new_resource.action, new_resource.name, \"Assuming user #{new_resource.user} would have been acted upon.\")\n+          else\n+            raise etype, emessage\n+          end\n+        end\n+        return if nuid == Process.euid\n+\n+        emessage = \"Error in #{new_resource.name}, Chef can't modify another user crontab when not running as root.\"\n+        events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+        raise etype, emessage\n+      end",
        "comment_created_at": "2020-02-10T22:48:27+00:00",
        "comment_author": "Tensibai",
        "comment_body": "Well, it's starting to be quite old :) I think this was made on 13 codebase at first.\r\n\r\nI'll see to understand the define_resource_requirement then, any hint to bootstrap me? ",
        "pr_file_module": null
      },
      {
        "comment_id": "377364666",
        "repo_full_name": "chef/chef",
        "pr_number": 8340,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "377245838",
        "commented_code": "@@ -41,11 +41,34 @@ def initialize(new_resource, run_context)\n       end\n       attr_accessor :cron_exists, :cron_empty\n \n+      def check_resource_semantics!\n+        return if Process.euid == 0\n+\n+        etype = Chef::Exceptions::Cron\n+        begin\n+          nuid = Etc.getpwnam(new_resource.user).uid\n+        rescue ArgumentError\n+          emessage = \"Error in #{new_resource.name}, #{new_resource.user} does not exists on this system.\"\n+          events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+          if why_run?\n+            events.whyrun_assumption(new_resource.action, new_resource.name, \"Assuming user #{new_resource.user} would have been acted upon.\")\n+          else\n+            raise etype, emessage\n+          end\n+        end\n+        return if nuid == Process.euid\n+\n+        emessage = \"Error in #{new_resource.name}, Chef can't modify another user crontab when not running as root.\"\n+        events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+        raise etype, emessage\n+      end",
        "comment_created_at": "2020-02-10T22:50:38+00:00",
        "comment_author": "Tensibai",
        "comment_body": "BTW, the goal is to fail the run with an informative message if the user doesn't exist as the resource can't do it's job. ",
        "pr_file_module": null
      },
      {
        "comment_id": "694170633",
        "repo_full_name": "chef/chef",
        "pr_number": 8340,
        "pr_file": "lib/chef/provider/cron.rb",
        "discussion_id": "377245838",
        "commented_code": "@@ -41,11 +41,34 @@ def initialize(new_resource, run_context)\n       end\n       attr_accessor :cron_exists, :cron_empty\n \n+      def check_resource_semantics!\n+        return if Process.euid == 0\n+\n+        etype = Chef::Exceptions::Cron\n+        begin\n+          nuid = Etc.getpwnam(new_resource.user).uid\n+        rescue ArgumentError\n+          emessage = \"Error in #{new_resource.name}, #{new_resource.user} does not exists on this system.\"\n+          events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+          if why_run?\n+            events.whyrun_assumption(new_resource.action, new_resource.name, \"Assuming user #{new_resource.user} would have been acted upon.\")\n+          else\n+            raise etype, emessage\n+          end\n+        end\n+        return if nuid == Process.euid\n+\n+        emessage = \"Error in #{new_resource.name}, Chef can't modify another user crontab when not running as root.\"\n+        events.provider_requirement_failed(new_resource.action, new_resource.name, etype, emessage)\n+        raise etype, emessage\n+      end",
        "comment_created_at": "2021-08-23T17:29:03+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "here's an example of trying to modify a group that doesn't exist, which is the closest i could find offhand:\r\n\r\nhttps://github.com/chef/chef/blob/master/lib/chef/provider/group.rb#L54-L59",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "755499124",
    "pr_number": 11579,
    "pr_file": "lib/chef/provider/mount/linux.rb",
    "created_at": "2021-11-23T20:59:26+00:00",
    "commented_code": "# \"findmnt\" outputs the mount points with volume.\n        # Convert the mount_point of the resource to a real path in case it\n        # contains symlinks in its parents dirs.\n        def loop_mount_points\n          # get loop_mount_points only if not initialized earlier\n          @loop_mount_points ||= shell_out!(\"losetup -a\").stdout",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "755499124",
        "repo_full_name": "chef/chef",
        "pr_number": 11579,
        "pr_file": "lib/chef/provider/mount/linux.rb",
        "discussion_id": "755499124",
        "commented_code": "@@ -29,10 +29,13 @@ class Linux < Chef::Provider::Mount::Mount\n         # \"findmnt\" outputs the mount points with volume.\n         # Convert the mount_point of the resource to a real path in case it\n         # contains symlinks in its parents dirs.\n+        def loop_mount_points\n+          # get loop_mount_points only if not initialized earlier\n+          @loop_mount_points ||= shell_out!(\"losetup -a\").stdout",
        "comment_created_at": "2021-11-23T20:59:26+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "We should probably `rescue Errno::ENOENT` and then return empty string here so that processing can continue without matching if losetup doesn't exist.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "759195679",
        "repo_full_name": "chef/chef",
        "pr_number": 11579,
        "pr_file": "lib/chef/provider/mount/linux.rb",
        "discussion_id": "755499124",
        "commented_code": "@@ -29,10 +29,13 @@ class Linux < Chef::Provider::Mount::Mount\n         # \"findmnt\" outputs the mount points with volume.\n         # Convert the mount_point of the resource to a real path in case it\n         # contains symlinks in its parents dirs.\n+        def loop_mount_points\n+          # get loop_mount_points only if not initialized earlier\n+          @loop_mount_points ||= shell_out!(\"losetup -a\").stdout",
        "comment_created_at": "2021-11-30T11:41:43+00:00",
        "comment_author": "msys-sgarg",
        "comment_body": "did the change please check",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "549525942",
    "pr_number": 10776,
    "pr_file": "lib/chef/provider/service/systemd.rb",
    "created_at": "2020-12-29T00:21:18+00:00",
    "commented_code": "end\n  end\n\n  def systemd_service_status\n    # If the status has already been collected, return that\n    return @service_status unless @service_status.nil?\n\n    # Collect all the status information for a service and returns it at once\n    options, args = get_systemctl_options_args\n    s = shell_out!(\"#{systemctl_path} #{args} show -p UnitFileState -p ActiveState #{new_resource.service_name}\", options)\n    # e.g. /bin/systemctl --system show  -p UnitFileState -p ActiveState sshd.service\n    # Returns something like:\n    # ActiveState=active\n    # UnitFileState=enabled\n    status = {}\n    s.stdout.each_line do |line|\n      k, v = line.strip.split(\"=\")\n      status[k] = v\n    end\n    # Assert requisite keys exist\n    unless status.key?(\"UnitFileState\") && status.key?(\"ActiveState\")\n      raise Mixlib::ShellOut::ShellCommandFailed, \"'#{systemctl_path} show' not reporting status for #{new_resource.service_name}!\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "549525942",
        "repo_full_name": "chef/chef",
        "pr_number": 10776,
        "pr_file": "lib/chef/provider/service/systemd.rb",
        "discussion_id": "549525942",
        "commented_code": "@@ -76,6 +76,31 @@ def define_resource_requirements\n     end\n   end\n \n+  def systemd_service_status\n+    # If the status has already been collected, return that\n+    return @service_status unless @service_status.nil?\n+\n+    # Collect all the status information for a service and returns it at once\n+    options, args = get_systemctl_options_args\n+    s = shell_out!(\"#{systemctl_path} #{args} show -p UnitFileState -p ActiveState #{new_resource.service_name}\", options)\n+    # e.g. /bin/systemctl --system show  -p UnitFileState -p ActiveState sshd.service\n+    # Returns something like:\n+    # ActiveState=active\n+    # UnitFileState=enabled\n+    status = {}\n+    s.stdout.each_line do |line|\n+      k, v = line.strip.split(\"=\")\n+      status[k] = v\n+    end\n+    # Assert requisite keys exist\n+    unless status.key?(\"UnitFileState\") && status.key?(\"ActiveState\")\n+      raise Mixlib::ShellOut::ShellCommandFailed, \"'#{systemctl_path} show' not reporting status for #{new_resource.service_name}!\"",
        "comment_created_at": "2020-12-29T00:21:18+00:00",
        "comment_author": "phiggins",
        "comment_body": "I don't think raising a Mixlib::Shellout exception here is the right thing to do. Using that exception class implies that the error came from Mixlib::Shellout which isn't the case. With no better option, a RuntimeException (ie, a bare call to `raise` is probably what you want here.",
        "pr_file_module": null
      },
      {
        "comment_id": "549538933",
        "repo_full_name": "chef/chef",
        "pr_number": 10776,
        "pr_file": "lib/chef/provider/service/systemd.rb",
        "discussion_id": "549525942",
        "commented_code": "@@ -76,6 +76,31 @@ def define_resource_requirements\n     end\n   end\n \n+  def systemd_service_status\n+    # If the status has already been collected, return that\n+    return @service_status unless @service_status.nil?\n+\n+    # Collect all the status information for a service and returns it at once\n+    options, args = get_systemctl_options_args\n+    s = shell_out!(\"#{systemctl_path} #{args} show -p UnitFileState -p ActiveState #{new_resource.service_name}\", options)\n+    # e.g. /bin/systemctl --system show  -p UnitFileState -p ActiveState sshd.service\n+    # Returns something like:\n+    # ActiveState=active\n+    # UnitFileState=enabled\n+    status = {}\n+    s.stdout.each_line do |line|\n+      k, v = line.strip.split(\"=\")\n+      status[k] = v\n+    end\n+    # Assert requisite keys exist\n+    unless status.key?(\"UnitFileState\") && status.key?(\"ActiveState\")\n+      raise Mixlib::ShellOut::ShellCommandFailed, \"'#{systemctl_path} show' not reporting status for #{new_resource.service_name}!\"",
        "comment_created_at": "2020-12-29T01:44:45+00:00",
        "comment_author": "joshuamiller01",
        "comment_body": "My intent here is to surface that the shellout to systemctl failed; if `RuntimeException` is the preference, that works for me.",
        "pr_file_module": null
      },
      {
        "comment_id": "549540924",
        "repo_full_name": "chef/chef",
        "pr_number": 10776,
        "pr_file": "lib/chef/provider/service/systemd.rb",
        "discussion_id": "549525942",
        "commented_code": "@@ -76,6 +76,31 @@ def define_resource_requirements\n     end\n   end\n \n+  def systemd_service_status\n+    # If the status has already been collected, return that\n+    return @service_status unless @service_status.nil?\n+\n+    # Collect all the status information for a service and returns it at once\n+    options, args = get_systemctl_options_args\n+    s = shell_out!(\"#{systemctl_path} #{args} show -p UnitFileState -p ActiveState #{new_resource.service_name}\", options)\n+    # e.g. /bin/systemctl --system show  -p UnitFileState -p ActiveState sshd.service\n+    # Returns something like:\n+    # ActiveState=active\n+    # UnitFileState=enabled\n+    status = {}\n+    s.stdout.each_line do |line|\n+      k, v = line.strip.split(\"=\")\n+      status[k] = v\n+    end\n+    # Assert requisite keys exist\n+    unless status.key?(\"UnitFileState\") && status.key?(\"ActiveState\")\n+      raise Mixlib::ShellOut::ShellCommandFailed, \"'#{systemctl_path} show' not reporting status for #{new_resource.service_name}!\"",
        "comment_created_at": "2020-12-29T01:57:02+00:00",
        "comment_author": "phiggins",
        "comment_body": "@tas50 @lamont-granquist thoughts on this?",
        "pr_file_module": null
      },
      {
        "comment_id": "551562835",
        "repo_full_name": "chef/chef",
        "pr_number": 10776,
        "pr_file": "lib/chef/provider/service/systemd.rb",
        "discussion_id": "549525942",
        "commented_code": "@@ -76,6 +76,31 @@ def define_resource_requirements\n     end\n   end\n \n+  def systemd_service_status\n+    # If the status has already been collected, return that\n+    return @service_status unless @service_status.nil?\n+\n+    # Collect all the status information for a service and returns it at once\n+    options, args = get_systemctl_options_args\n+    s = shell_out!(\"#{systemctl_path} #{args} show -p UnitFileState -p ActiveState #{new_resource.service_name}\", options)\n+    # e.g. /bin/systemctl --system show  -p UnitFileState -p ActiveState sshd.service\n+    # Returns something like:\n+    # ActiveState=active\n+    # UnitFileState=enabled\n+    status = {}\n+    s.stdout.each_line do |line|\n+      k, v = line.strip.split(\"=\")\n+      status[k] = v\n+    end\n+    # Assert requisite keys exist\n+    unless status.key?(\"UnitFileState\") && status.key?(\"ActiveState\")\n+      raise Mixlib::ShellOut::ShellCommandFailed, \"'#{systemctl_path} show' not reporting status for #{new_resource.service_name}!\"",
        "comment_created_at": "2021-01-04T20:54:02+00:00",
        "comment_author": "joshuamiller01",
        "comment_body": "I'm going to change this to `raise Chef::Exceptions::Service` per Lamont's suggestion",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "644955836",
    "pr_number": 11241,
    "pr_file": "knife/lib/chef/knife/client_create.rb",
    "created_at": "2021-06-03T16:35:17+00:00",
    "commented_code": "client.public_key File.read(File.expand_path(config[:public_key]))\n        end\n\n        # Check the file before creating the client so the api is more transactional.\n        if config[:file]\n          file = config[:file]\n\n          unless File.writable?(File.dirname(file))\n            ui.fatal \"Dir #{File.dirname(file)} is not writable. Check permissions.\"\n            exit 1\n          end\n\n          unless File.writable?(file)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "644955836",
        "repo_full_name": "chef/chef",
        "pr_number": 11241,
        "pr_file": "knife/lib/chef/knife/client_create.rb",
        "discussion_id": "644955836",
        "commented_code": "@@ -81,6 +81,21 @@ def run\n           client.public_key File.read(File.expand_path(config[:public_key]))\n         end\n \n+        # Check the file before creating the client so the api is more transactional.\n+        if config[:file]\n+          file = config[:file]\n+\n+          unless File.writable?(File.dirname(file))\n+            ui.fatal \"Dir #{File.dirname(file)} is not writable. Check permissions.\"\n+            exit 1\n+          end\n+\n+          unless File.writable?(file)",
        "comment_created_at": "2021-06-03T16:35:17+00:00",
        "comment_author": "marcparadise",
        "comment_body": "If the file does not exist, the File.writable? will return false: \r\n\r\n![capture_036](https://user-images.githubusercontent.com/1130204/120680301-2321e980-c468-11eb-8d11-9f81b8fcdd04.png)",
        "pr_file_module": null
      },
      {
        "comment_id": "645288328",
        "repo_full_name": "chef/chef",
        "pr_number": 11241,
        "pr_file": "knife/lib/chef/knife/client_create.rb",
        "discussion_id": "644955836",
        "commented_code": "@@ -81,6 +81,21 @@ def run\n           client.public_key File.read(File.expand_path(config[:public_key]))\n         end\n \n+        # Check the file before creating the client so the api is more transactional.\n+        if config[:file]\n+          file = config[:file]\n+\n+          unless File.writable?(File.dirname(file))\n+            ui.fatal \"Dir #{File.dirname(file)} is not writable. Check permissions.\"\n+            exit 1\n+          end\n+\n+          unless File.writable?(file)",
        "comment_created_at": "2021-06-04T04:55:44+00:00",
        "comment_author": "snehaldwivedi",
        "comment_body": "yes, if the file is writable then only it will return true else false. You can also go through documentation [here](https://ruby-doc.org/core-2.5.0/File.html). Now as per your example:\r\n1. ` File.writable?(\"does-not-exist\")` it has checked if the given file is writable or not and returns `false` as it doesn't exist.\r\n2. `File.write(\"does-not-exist\", \"blah\")` it returns 4. Here it will create a new file \"does-not-exist\" and add a content \"blah\" can returns length of the content.\r\n3. ` File.writable?(\"does-not-exist\")` now after 2nd point where the file is not created now ` File.writable?` is return `true`.",
        "pr_file_module": null
      },
      {
        "comment_id": "655453068",
        "repo_full_name": "chef/chef",
        "pr_number": 11241,
        "pr_file": "knife/lib/chef/knife/client_create.rb",
        "discussion_id": "644955836",
        "commented_code": "@@ -81,6 +81,21 @@ def run\n           client.public_key File.read(File.expand_path(config[:public_key]))\n         end\n \n+        # Check the file before creating the client so the api is more transactional.\n+        if config[:file]\n+          file = config[:file]\n+\n+          unless File.writable?(File.dirname(file))\n+            ui.fatal \"Dir #{File.dirname(file)} is not writable. Check permissions.\"\n+            exit 1\n+          end\n+\n+          unless File.writable?(file)",
        "comment_created_at": "2021-06-21T14:57:09+00:00",
        "comment_author": "marcparadise",
        "comment_body": "My concern is less functional, and more user experience - it is correct that the directory is not writable and the action should fail. \r\n\r\nBut in the case where the directory for `/tmp/test/afile.out`  does not exist, we will report an error that `Dir '/tmp/test/' is not writable. Check permissions`.  This is misleading, and we could provide  more actionable feedback than \"check permissions\".  It would be better to specifically verify that the directory exists and report that error independently of permissions-related errors. ",
        "pr_file_module": null
      },
      {
        "comment_id": "655869743",
        "repo_full_name": "chef/chef",
        "pr_number": 11241,
        "pr_file": "knife/lib/chef/knife/client_create.rb",
        "discussion_id": "644955836",
        "commented_code": "@@ -81,6 +81,21 @@ def run\n           client.public_key File.read(File.expand_path(config[:public_key]))\n         end\n \n+        # Check the file before creating the client so the api is more transactional.\n+        if config[:file]\n+          file = config[:file]\n+\n+          unless File.writable?(File.dirname(file))\n+            ui.fatal \"Dir #{File.dirname(file)} is not writable. Check permissions.\"\n+            exit 1\n+          end\n+\n+          unless File.writable?(file)",
        "comment_created_at": "2021-06-22T04:39:00+00:00",
        "comment_author": "snehaldwivedi",
        "comment_body": "@marcparadise Got your point. I Will update the condition accordingly. ",
        "pr_file_module": null
      }
    ]
  }
]
