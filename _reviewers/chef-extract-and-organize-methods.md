---
title: Extract and organize methods
description: Break down large, complex methods into smaller, focused methods with
  clear names that describe their purpose. This improves code readability, maintainability,
  and testability.
repository: chef/chef
label: Code Style
language: Ruby
comments_count: 8
repository_stars: 7860
---

Break down large, complex methods into smaller, focused methods with clear names that describe their purpose. This improves code readability, maintainability, and testability.

When methods grow too long or handle multiple concerns:
- Extract separate behaviors into dedicated methods
- Use descriptive method names that explain their purpose
- Avoid duplicating logic across methods

For example, instead of:

```ruby
def wrapper_script
  # 50+ lines of complex code with slight variations
  if new_resource.use_inline_powershell
    # inline powershell version
  else
    # regular shell out version
  end
end
```

Refactor to:

```ruby
def wrapper_script
  if new_resource.use_inline_powershell
    inline_powershell_wrapper_script
  else
    shell_out_wrapper_script
  end
end

def inline_powershell_wrapper_script
  # inline powershell implementation
end

def shell_out_wrapper_script
  # regular shell out implementation
end
```

Or when logic is repeated:

```ruby
def resolved_package(pkg)
  new_resource.anchor_package_regex ? "^#{pkg}$" : pkg
end
```

This approach reduces cognitive load, improves reusability, and makes code easier to understand and modify.


[
  {
    "discussion_id": "1377760869",
    "pr_number": 14052,
    "pr_file": "lib/chef/provider/powershell_script.rb",
    "created_at": "2023-10-31T15:17:16+00:00",
    "commented_code": "# executed, otherwise 0 or 1 based on whether $? is set to true\n      # (success, where we return 0) or false (where we return 1).\n      def wrapper_script\n        <<~EOH\n        # The script looks very slightly different with inline powershell since",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1377760869",
        "repo_full_name": "chef/chef",
        "pr_number": 14052,
        "pr_file": "lib/chef/provider/powershell_script.rb",
        "discussion_id": "1377760869",
        "commented_code": "@@ -130,7 +193,78 @@ def validate_script_syntax!\n       # executed, otherwise 0 or 1 based on whether $? is set to true\n       # (success, where we return 0) or false (where we return 1).\n       def wrapper_script\n-        <<~EOH\n+        # The script looks very slightly different with inline powershell since",
        "comment_created_at": "2023-10-31T15:17:16+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Can we extract these two options into their own methods? Maybe something like `inline_powershell_wrapper...` and `shell_out_wrapper...`? The method is a bit long to start with, so the if/else is harder to read due to the length.",
        "pr_file_module": null
      },
      {
        "comment_id": "1377894471",
        "repo_full_name": "chef/chef",
        "pr_number": 14052,
        "pr_file": "lib/chef/provider/powershell_script.rb",
        "discussion_id": "1377760869",
        "commented_code": "@@ -130,7 +193,78 @@ def validate_script_syntax!\n       # executed, otherwise 0 or 1 based on whether $? is set to true\n       # (success, where we return 0) or false (where we return 1).\n       def wrapper_script\n-        <<~EOH\n+        # The script looks very slightly different with inline powershell since",
        "comment_created_at": "2023-10-31T16:49:14+00:00",
        "comment_author": "jaymzjulian",
        "comment_body": "absolutely can.  Retested with both traditional and inline powershell to ensure that didn't break things",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1385630851",
    "pr_number": 14052,
    "pr_file": "lib/chef/provider/powershell_script.rb",
    "created_at": "2023-11-07T21:53:27+00:00",
    "commented_code": "# last process run in the script if it is the last command\n      # executed, otherwise 0 or 1 based on whether $? is set to true\n      # (success, where we return 0) or false (where we return 1).\n      def wrapper_script\n      def inline_powershell_wrapper_script",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1385630851",
        "repo_full_name": "chef/chef",
        "pr_number": 14052,
        "pr_file": "lib/chef/provider/powershell_script.rb",
        "discussion_id": "1385630851",
        "commented_code": "@@ -129,7 +192,80 @@ def validate_script_syntax!\n       # last process run in the script if it is the last command\n       # executed, otherwise 0 or 1 based on whether $? is set to true\n       # (success, where we return 0) or false (where we return 1).\n-      def wrapper_script\n+      def inline_powershell_wrapper_script",
        "comment_created_at": "2023-11-07T21:53:27+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Thinking this can potentially be deduplicated by some sort of templating or builder logic so that the behavior stays consistent between them.  h/t: @dafyddcrosby ",
        "pr_file_module": null
      },
      {
        "comment_id": "1385691294",
        "repo_full_name": "chef/chef",
        "pr_number": 14052,
        "pr_file": "lib/chef/provider/powershell_script.rb",
        "discussion_id": "1385630851",
        "commented_code": "@@ -129,7 +192,80 @@ def validate_script_syntax!\n       # last process run in the script if it is the last command\n       # executed, otherwise 0 or 1 based on whether $? is set to true\n       # (success, where we return 0) or false (where we return 1).\n-      def wrapper_script\n+      def inline_powershell_wrapper_script",
        "comment_created_at": "2023-11-07T22:51:22+00:00",
        "comment_author": "jaymzjulian",
        "comment_body": "yeah, i think that's sane to do - i'll make that happen",
        "pr_file_module": null
      },
      {
        "comment_id": "1393521546",
        "repo_full_name": "chef/chef",
        "pr_number": 14052,
        "pr_file": "lib/chef/provider/powershell_script.rb",
        "discussion_id": "1385630851",
        "commented_code": "@@ -129,7 +192,80 @@ def validate_script_syntax!\n       # last process run in the script if it is the last command\n       # executed, otherwise 0 or 1 based on whether $? is set to true\n       # (success, where we return 0) or false (where we return 1).\n-      def wrapper_script\n+      def inline_powershell_wrapper_script",
        "comment_created_at": "2023-11-15T01:32:53+00:00",
        "comment_author": "jaymzjulian",
        "comment_body": "In the latest push, this is simplified to a single function with the two changes as simple conditions at those line points, which seemed much easier to read to my eye.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1297860584",
    "pr_number": 13873,
    "pr_file": "lib/chef/provider/package/apt.rb",
    "created_at": "2023-08-18T00:00:50+00:00",
    "commented_code": "end\n\n        def resolve_virtual_package_name(pkg)\n          showpkg = run_noninteractive(\"apt-cache\", \"showpkg\", pkg).stdout\n          # apt-cache considers package names as regex by default. The anchor flag will decide whether to match name exact string or not\n          resolved_pkg = new_resource.anchor_package_name_patterns ? pkg : \"^#{pkg}$\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1297860584",
        "repo_full_name": "chef/chef",
        "pr_number": 13873,
        "pr_file": "lib/chef/provider/package/apt.rb",
        "discussion_id": "1297860584",
        "commented_code": "@@ -216,7 +218,9 @@ def resolve_package_versions(pkg)\n         end\n \n         def resolve_virtual_package_name(pkg)\n-          showpkg = run_noninteractive(\"apt-cache\", \"showpkg\", pkg).stdout\n+          # apt-cache considers package names as regex by default. The anchor flag will decide whether to match name exact string or not\n+          resolved_pkg = new_resource.anchor_package_name_patterns ? pkg : \"^#{pkg}$\"",
        "comment_created_at": "2023-08-18T00:00:50+00:00",
        "comment_author": "jaymzh",
        "comment_body": "rather than repeat this line/logic over and over, please extract this to a method (and I\"m reversing the log here per my previous comment):\r\n\r\n```ruby\r\ndef resolved_package(pkg)\r\n  new_resource.anchor_package_regex ? \"^#{pkg}$\" : pkg\r\nend\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "755493907",
    "pr_number": 11910,
    "pr_file": "lib/chef/provider/package/apt.rb",
    "created_at": "2021-11-23T20:51:09+00:00",
    "commented_code": "}\n        end\n\n        # Helper to construct Hash of names-to-package-information.",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "755493907",
        "repo_full_name": "chef/chef",
        "pr_number": 11910,
        "pr_file": "lib/chef/provider/package/apt.rb",
        "discussion_id": "755493907",
        "commented_code": "@@ -255,6 +273,81 @@ def package_data_for(pkg)\n           }\n         end\n \n+        # Helper to construct Hash of names-to-package-information.",
        "comment_created_at": "2021-11-23T20:51:09+00:00",
        "comment_author": "btm",
        "comment_body": "Everything from here down looks like its copied from `Package::Dpkg`. We don't want to duplicate that. We already have the shared `Package::Deb` mixin between the Dpkg and Apt providers that we'd want to refactor this into.",
        "pr_file_module": null
      },
      {
        "comment_id": "758063083",
        "repo_full_name": "chef/chef",
        "pr_number": 11910,
        "pr_file": "lib/chef/provider/package/apt.rb",
        "discussion_id": "755493907",
        "commented_code": "@@ -255,6 +273,81 @@ def package_data_for(pkg)\n           }\n         end\n \n+        # Helper to construct Hash of names-to-package-information.",
        "comment_created_at": "2021-11-29T06:15:14+00:00",
        "comment_author": "manick-vel-11",
        "comment_body": "I understand that most of the implementation is being referred from dpkg package. I will make use of `Package::Deb` and will separate out commonly used code by having a mixin between dpkg and apt providers.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "755494818",
    "pr_number": 11910,
    "pr_file": "lib/chef/provider/package/apt.rb",
    "created_at": "2021-11-23T20:52:41+00:00",
    "commented_code": "}\n        end\n\n        # Helper to construct Hash of names-to-package-information.\n        #\n        # @return [Hash] Mapping of package names to package information\n        def name_pkginfo\n          @name_pkginfo ||=\n            begin\n              pkginfos = resolved_source_array.map do |src|\n                logger.trace(\"#{new_resource} checking #{src} dpkg status\")\n                status = shell_out(\"dpkg-deb\", \"-W\", src)\n                status.stdout\n              end\n              Hash[*package_name_array.zip(pkginfos).flatten]\n            end\n        end\n\n        def name_package_name\n          @name_package_name ||= name_pkginfo.transform_values { |v| v ? v.split(\"\\t\")[0] : nil }\n        end\n\n        # Return package names from the candidate source file(s).\n        #\n        # @return [Array] Array of actual package names read from the source files\n        def get_package_name\n          package_name_array.map { |name| name_package_name[name] }\n        end\n\n        def read_current_version_of_package(package_name)\n          logger.trace(\"#{new_resource} checking install state of #{package_name}\")\n          status = shell_out!(\"dpkg\", \"-s\", package_name, returns: [0, 1])\n          package_installed = false\n          status.stdout.each_line do |line|\n            case line\n            when /^Status: deinstall ok config-files/.freeze",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "755494818",
        "repo_full_name": "chef/chef",
        "pr_number": 11910,
        "pr_file": "lib/chef/provider/package/apt.rb",
        "discussion_id": "755494818",
        "commented_code": "@@ -255,6 +273,81 @@ def package_data_for(pkg)\n           }\n         end\n \n+        # Helper to construct Hash of names-to-package-information.\n+        #\n+        # @return [Hash] Mapping of package names to package information\n+        def name_pkginfo\n+          @name_pkginfo ||=\n+            begin\n+              pkginfos = resolved_source_array.map do |src|\n+                logger.trace(\"#{new_resource} checking #{src} dpkg status\")\n+                status = shell_out(\"dpkg-deb\", \"-W\", src)\n+                status.stdout\n+              end\n+              Hash[*package_name_array.zip(pkginfos).flatten]\n+            end\n+        end\n+\n+        def name_package_name\n+          @name_package_name ||= name_pkginfo.transform_values { |v| v ? v.split(\"\\t\")[0] : nil }\n+        end\n+\n+        # Return package names from the candidate source file(s).\n+        #\n+        # @return [Array] Array of actual package names read from the source files\n+        def get_package_name\n+          package_name_array.map { |name| name_package_name[name] }\n+        end\n+\n+        def read_current_version_of_package(package_name)\n+          logger.trace(\"#{new_resource} checking install state of #{package_name}\")\n+          status = shell_out!(\"dpkg\", \"-s\", package_name, returns: [0, 1])\n+          package_installed = false\n+          status.stdout.each_line do |line|\n+            case line\n+            when /^Status: deinstall ok config-files/.freeze",
        "comment_created_at": "2021-11-23T20:52:41+00:00",
        "comment_author": "btm",
        "comment_body": "We especially don't want to duplicate these regexes. The pattern we use for defining these over in https://github.com/chef/chef/blob/main/lib/chef/provider/package/dpkg.rb#L28-L30 is intentional. But duplicating these, if there was a bug we needed to fix in one provider we'd have to remember that we duplicated this code in another provider and fix the same regex. We'd likely forget that and miss the fix.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "792112012",
    "pr_number": 12182,
    "pr_file": "lib/chef/provider/package/zypper.rb",
    "created_at": "2022-01-25T20:55:32+00:00",
    "commented_code": "end\n\n        def candidate_version\n          @candidate_version ||= package_name_array.each_with_index.map { |pkg, i| available_version(i) }\n          if source_files_exist?\n            logger.trace(\"#{new_resource} checking rpm status\")\n            shell_out!(\"rpm\", \"-qp\", \"--queryformat\", \"%{NAME} %{VERSION}-%{RELEASE}\\n\", new_resource.source).stdout.each_line do |line|\n              case line\n              when /^(\\S+)\\s(\\S+)$/\n                current_resource.package_name($1)\n                new_resource.version($2)\n                @candidate_version = $2\n              end\n            end",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "792112012",
        "repo_full_name": "chef/chef",
        "pr_number": 12182,
        "pr_file": "lib/chef/provider/package/zypper.rb",
        "discussion_id": "792112012",
        "commented_code": "@@ -70,7 +71,20 @@ def get_current_versions\n         end\n \n         def candidate_version\n-          @candidate_version ||= package_name_array.each_with_index.map { |pkg, i| available_version(i) }\n+          if source_files_exist?\n+            logger.trace(\"#{new_resource} checking rpm status\")\n+            shell_out!(\"rpm\", \"-qp\", \"--queryformat\", \"%{NAME} %{VERSION}-%{RELEASE}\\n\", new_resource.source).stdout.each_line do |line|\n+              case line\n+              when /^(\\S+)\\s(\\S+)$/\n+                current_resource.package_name($1)\n+                new_resource.version($2)\n+                @candidate_version = $2\n+              end\n+            end",
        "comment_created_at": "2022-01-25T20:55:32+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "the shell_out and its parsing here should probably be extracted out to its own method, see `resolve_source_to_version_obj` in the dnf or yum providers (although you don't have a version obj in this case so probably `resolve_source_to_version`.",
        "pr_file_module": null
      },
      {
        "comment_id": "792118493",
        "repo_full_name": "chef/chef",
        "pr_number": 12182,
        "pr_file": "lib/chef/provider/package/zypper.rb",
        "discussion_id": "792112012",
        "commented_code": "@@ -70,7 +71,20 @@ def get_current_versions\n         end\n \n         def candidate_version\n-          @candidate_version ||= package_name_array.each_with_index.map { |pkg, i| available_version(i) }\n+          if source_files_exist?\n+            logger.trace(\"#{new_resource} checking rpm status\")\n+            shell_out!(\"rpm\", \"-qp\", \"--queryformat\", \"%{NAME} %{VERSION}-%{RELEASE}\\n\", new_resource.source).stdout.each_line do |line|\n+              case line\n+              when /^(\\S+)\\s(\\S+)$/\n+                current_resource.package_name($1)\n+                new_resource.version($2)\n+                @candidate_version = $2\n+              end\n+            end",
        "comment_created_at": "2022-01-25T21:04:59+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "(in general the dnf provider is a reasonably good template for how the code change should look)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "718895310",
    "pr_number": 11898,
    "pr_file": "lib/chef/resource/macos_userdefaults.rb",
    "created_at": "2021-09-29T21:23:01+00:00",
    "commented_code": "required: true\n\n      property :host, [String, Symbol],\n        description: \"Set either :current or a hostname to set the user default at the host level.\",\n        description: \"Set either :current, :all or a hostname to set the user default at the host level.\",\n        desired_state: false,\n        introduced: \"16.3\"\n        introduced: \"16.3\",\n        coerce: proc { |value| to_cf_host(value) }\n\n      property :value, [Integer, Float, String, TrueClass, FalseClass, Hash, Array],\n        description: \"The value of the key. Note: With the `type` property set to `bool`, `String` forms of Boolean true/false values that Apple accepts in the defaults command will be coerced: 0/1, 'TRUE'/'FALSE,' 'true'/false', 'YES'/'NO', or 'yes'/'no'.\",\n        required: [:write],\n        coerce: proc { |v| v.is_a?(Hash) ? v.transform_keys(&:to_s) : v } # make sure keys are all strings for comparison\n        required: [:write]\n\n      property :type, String,\n        description: \"The value type of the preference key.\",\n        equal_to: %w{bool string int float array dict},\n        desired_state: false\n        desired_state: false,\n        deprecated: true\n\n      property :user, String,\n        description: \"The system user that the default will be applied to.\",\n        desired_state: false\n      property :user, [String, Symbol],\n        description: \"The system user that the default will be applied to. Set :current for current user, :all for all users or pass a valid username\",\n        desired_state: false,\n        coerce: proc { |value| to_cf_user(value) }\n\n      property :sudo, [TrueClass, FalseClass],\n        description: \"Set to true if the setting you wish to modify requires privileged access. This requires passwordless sudo for the `/usr/bin/defaults` command to be setup for the user running #{ChefUtils::Dist::Infra::PRODUCT}.\",\n        default: false,\n        desired_state: false\n        desired_state: false,\n        deprecated: true\n\n      load_current_value do |new_resource|\n        Chef::Log.debug \"#load_current_value: shelling out \\\"#{defaults_export_cmd(new_resource).join(\" \")}\\\" to determine state\"\n        state = shell_out(defaults_export_cmd(new_resource), user: new_resource.user)\n        Chef::Log.debug \"#load_current_value: attempting to read \\\"#{new_resource.domain}\\\" value from preferences to determine state\"\n\n        if state.error? || state.stdout.empty?\n          Chef::Log.debug \"#load_current_value: #{defaults_export_cmd(new_resource).join(\" \")} returned stdout: #{state.stdout} and stderr: #{state.stderr}\"\n          current_value_does_not_exist!\n        end\n        pref = get_preference(new_resource)\n        current_value_does_not_exist! if pref.nil?\n\n        plist_data = ::Plist.parse_xml(state.stdout)\n\n        # handle the situation where the key doesn't exist in the domain\n        if plist_data.key?(new_resource.key)\n          key new_resource.key\n        else\n          current_value_does_not_exist!\n        end\n\n        value plist_data[new_resource.key]\n      end\n\n      #\n      # The defaults command to export a domain\n      #\n      # @return [Array] defaults command\n      #\n      def defaults_export_cmd(resource)\n        state_cmd = [\"/usr/bin/defaults\"]\n\n        if resource.host == \"current\"\n          state_cmd.concat([\"-currentHost\"])\n        elsif resource.host # they specified a non-nil value, which is a hostname\n          state_cmd.concat([\"-host\", resource.host])\n        end\n\n        state_cmd.concat([\"export\", resource.domain, \"-\"])\n        state_cmd\n        key new_resource.key\n        value pref\n      end\n\n      action :write, description: \"Write the value to the specified domain/key.\" do\n        converge_if_changed do\n          cmd = defaults_modify_cmd\n          Chef::Log.debug(\"Updating defaults value by shelling out: #{cmd.join(\" \")}\")\n\n          shell_out!(cmd, user: new_resource.user)\n          Chef::Log.debug(\"Updating defaults value for #{new_resource.key} in #{new_resource.domain}\")\n          set_preference(new_resource)\n        end\n      end\n\n      action :delete, description: \"Delete a key from a domain.\" do\n        # if it's not there there's nothing to remove\n        return unless current_resource\n        return if current_resource.nil?\n\n        converge_by(\"delete domain:#{new_resource.domain} key:#{new_resource.key}\") do\n\n          cmd = defaults_modify_cmd\n          Chef::Log.debug(\"Removing defaults key by shelling out: #{cmd.join(\" \")}\")\n\n          shell_out!(cmd, user: new_resource.user)\n          Chef::Log.debug(\"Removing defaults key: #{new_resource.key}\")\n          CF::Preferences.set!(new_resource.key, nil, new_resource.domain, new_resource.user, new_resource.host)\n        end\n      end\n\n      action_class do\n        #\n        # The command used to write or delete delete values from domains\n        #\n        # @return [Array] Array representation of defaults command to run\n        #\n        def defaults_modify_cmd\n          cmd = [\"/usr/bin/defaults\"]\n\n          if new_resource.host == :current\n            cmd.concat([\"-currentHost\"])\n          elsif new_resource.host # they specified a non-nil value, which is a hostname\n            cmd.concat([\"-host\", new_resource.host])\n          end\n\n          cmd.concat([action.to_s, new_resource.domain, new_resource.key])\n          cmd.concat(processed_value) if action == :write\n          cmd.prepend(\"sudo\") if new_resource.sudo\n          cmd\n        end\n      def get_preference(new_resource)\n        CF::Preferences.get(new_resource.key, new_resource.domain, new_resource.user, new_resource.host)\n      end\n\n        #\n        # convert the provided value into the format defaults expects\n        #\n        # @return [array] array of values starting with the type if applicable\n        #\n        def processed_value\n          type = new_resource.type || value_type(new_resource.value)\n\n          # when dict this creates an array of values [\"Key1\", \"Value1\", \"Key2\", \"Value2\" ...]\n          cmd_values = [\"-#{type}\"]\n\n          case type\n          when \"dict\"\n            cmd_values.concat(new_resource.value.flatten)\n          when \"array\"\n            cmd_values.concat(new_resource.value)\n          when \"bool\"\n            cmd_values.concat(bool_to_defaults_bool(new_resource.value))\n          else\n            cmd_values.concat([new_resource.value])\n          end\n\n          cmd_values\n        end\n      def set_preference(new_resource)\n        CF::Preferences.set!(new_resource.key, new_resource.value, new_resource.domain, new_resource.user, new_resource.host)\n      end",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "718895310",
        "repo_full_name": "chef/chef",
        "pr_number": 11898,
        "pr_file": "lib/chef/resource/macos_userdefaults.rb",
        "discussion_id": "718895310",
        "commented_code": "@@ -78,173 +79,88 @@ class MacosUserDefaults < Chef::Resource\n         required: true\n \n       property :host, [String, Symbol],\n-        description: \"Set either :current or a hostname to set the user default at the host level.\",\n+        description: \"Set either :current, :all or a hostname to set the user default at the host level.\",\n         desired_state: false,\n-        introduced: \"16.3\"\n+        introduced: \"16.3\",\n+        coerce: proc { |value| to_cf_host(value) }\n \n       property :value, [Integer, Float, String, TrueClass, FalseClass, Hash, Array],\n         description: \"The value of the key. Note: With the `type` property set to `bool`, `String` forms of Boolean true/false values that Apple accepts in the defaults command will be coerced: 0/1, 'TRUE'/'FALSE,' 'true'/false', 'YES'/'NO', or 'yes'/'no'.\",\n-        required: [:write],\n-        coerce: proc { |v| v.is_a?(Hash) ? v.transform_keys(&:to_s) : v } # make sure keys are all strings for comparison\n+        required: [:write]\n \n       property :type, String,\n         description: \"The value type of the preference key.\",\n         equal_to: %w{bool string int float array dict},\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n-      property :user, String,\n-        description: \"The system user that the default will be applied to.\",\n-        desired_state: false\n+      property :user, [String, Symbol],\n+        description: \"The system user that the default will be applied to. Set :current for current user, :all for all users or pass a valid username\",\n+        desired_state: false,\n+        coerce: proc { |value| to_cf_user(value) }\n \n       property :sudo, [TrueClass, FalseClass],\n         description: \"Set to true if the setting you wish to modify requires privileged access. This requires passwordless sudo for the `/usr/bin/defaults` command to be setup for the user running #{ChefUtils::Dist::Infra::PRODUCT}.\",\n         default: false,\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n       load_current_value do |new_resource|\n-        Chef::Log.debug \"#load_current_value: shelling out \\\"#{defaults_export_cmd(new_resource).join(\" \")}\\\" to determine state\"\n-        state = shell_out(defaults_export_cmd(new_resource), user: new_resource.user)\n+        Chef::Log.debug \"#load_current_value: attempting to read \\\"#{new_resource.domain}\\\" value from preferences to determine state\"\n \n-        if state.error? || state.stdout.empty?\n-          Chef::Log.debug \"#load_current_value: #{defaults_export_cmd(new_resource).join(\" \")} returned stdout: #{state.stdout} and stderr: #{state.stderr}\"\n-          current_value_does_not_exist!\n-        end\n+        pref = get_preference(new_resource)\n+        current_value_does_not_exist! if pref.nil?\n \n-        plist_data = ::Plist.parse_xml(state.stdout)\n-\n-        # handle the situation where the key doesn't exist in the domain\n-        if plist_data.key?(new_resource.key)\n-          key new_resource.key\n-        else\n-          current_value_does_not_exist!\n-        end\n-\n-        value plist_data[new_resource.key]\n-      end\n-\n-      #\n-      # The defaults command to export a domain\n-      #\n-      # @return [Array] defaults command\n-      #\n-      def defaults_export_cmd(resource)\n-        state_cmd = [\"/usr/bin/defaults\"]\n-\n-        if resource.host == \"current\"\n-          state_cmd.concat([\"-currentHost\"])\n-        elsif resource.host # they specified a non-nil value, which is a hostname\n-          state_cmd.concat([\"-host\", resource.host])\n-        end\n-\n-        state_cmd.concat([\"export\", resource.domain, \"-\"])\n-        state_cmd\n+        key new_resource.key\n+        value pref\n       end\n \n       action :write, description: \"Write the value to the specified domain/key.\" do\n         converge_if_changed do\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Updating defaults value by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Updating defaults value for #{new_resource.key} in #{new_resource.domain}\")\n+          set_preference(new_resource)\n         end\n       end\n \n       action :delete, description: \"Delete a key from a domain.\" do\n         # if it's not there there's nothing to remove\n-        return unless current_resource\n+        return if current_resource.nil?\n \n         converge_by(\"delete domain:#{new_resource.domain} key:#{new_resource.key}\") do\n-\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Removing defaults key by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Removing defaults key: #{new_resource.key}\")\n+          CF::Preferences.set!(new_resource.key, nil, new_resource.domain, new_resource.user, new_resource.host)\n         end\n       end\n \n-      action_class do\n-        #\n-        # The command used to write or delete delete values from domains\n-        #\n-        # @return [Array] Array representation of defaults command to run\n-        #\n-        def defaults_modify_cmd\n-          cmd = [\"/usr/bin/defaults\"]\n-\n-          if new_resource.host == :current\n-            cmd.concat([\"-currentHost\"])\n-          elsif new_resource.host # they specified a non-nil value, which is a hostname\n-            cmd.concat([\"-host\", new_resource.host])\n-          end\n-\n-          cmd.concat([action.to_s, new_resource.domain, new_resource.key])\n-          cmd.concat(processed_value) if action == :write\n-          cmd.prepend(\"sudo\") if new_resource.sudo\n-          cmd\n-        end\n+      def get_preference(new_resource)\n+        CF::Preferences.get(new_resource.key, new_resource.domain, new_resource.user, new_resource.host)\n+      end\n \n-        #\n-        # convert the provided value into the format defaults expects\n-        #\n-        # @return [array] array of values starting with the type if applicable\n-        #\n-        def processed_value\n-          type = new_resource.type || value_type(new_resource.value)\n-\n-          # when dict this creates an array of values [\"Key1\", \"Value1\", \"Key2\", \"Value2\" ...]\n-          cmd_values = [\"-#{type}\"]\n-\n-          case type\n-          when \"dict\"\n-            cmd_values.concat(new_resource.value.flatten)\n-          when \"array\"\n-            cmd_values.concat(new_resource.value)\n-          when \"bool\"\n-            cmd_values.concat(bool_to_defaults_bool(new_resource.value))\n-          else\n-            cmd_values.concat([new_resource.value])\n-          end\n-\n-          cmd_values\n-        end\n+      def set_preference(new_resource)\n+        CF::Preferences.set!(new_resource.key, new_resource.value, new_resource.domain, new_resource.user, new_resource.host)\n+      end",
        "comment_created_at": "2021-09-29T21:23:01+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "don't think this method is getting used (might be causing some confusion over the action_class block)",
        "pr_file_module": null
      },
      {
        "comment_id": "719066530",
        "repo_full_name": "chef/chef",
        "pr_number": 11898,
        "pr_file": "lib/chef/resource/macos_userdefaults.rb",
        "discussion_id": "718895310",
        "commented_code": "@@ -78,173 +79,88 @@ class MacosUserDefaults < Chef::Resource\n         required: true\n \n       property :host, [String, Symbol],\n-        description: \"Set either :current or a hostname to set the user default at the host level.\",\n+        description: \"Set either :current, :all or a hostname to set the user default at the host level.\",\n         desired_state: false,\n-        introduced: \"16.3\"\n+        introduced: \"16.3\",\n+        coerce: proc { |value| to_cf_host(value) }\n \n       property :value, [Integer, Float, String, TrueClass, FalseClass, Hash, Array],\n         description: \"The value of the key. Note: With the `type` property set to `bool`, `String` forms of Boolean true/false values that Apple accepts in the defaults command will be coerced: 0/1, 'TRUE'/'FALSE,' 'true'/false', 'YES'/'NO', or 'yes'/'no'.\",\n-        required: [:write],\n-        coerce: proc { |v| v.is_a?(Hash) ? v.transform_keys(&:to_s) : v } # make sure keys are all strings for comparison\n+        required: [:write]\n \n       property :type, String,\n         description: \"The value type of the preference key.\",\n         equal_to: %w{bool string int float array dict},\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n-      property :user, String,\n-        description: \"The system user that the default will be applied to.\",\n-        desired_state: false\n+      property :user, [String, Symbol],\n+        description: \"The system user that the default will be applied to. Set :current for current user, :all for all users or pass a valid username\",\n+        desired_state: false,\n+        coerce: proc { |value| to_cf_user(value) }\n \n       property :sudo, [TrueClass, FalseClass],\n         description: \"Set to true if the setting you wish to modify requires privileged access. This requires passwordless sudo for the `/usr/bin/defaults` command to be setup for the user running #{ChefUtils::Dist::Infra::PRODUCT}.\",\n         default: false,\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n       load_current_value do |new_resource|\n-        Chef::Log.debug \"#load_current_value: shelling out \\\"#{defaults_export_cmd(new_resource).join(\" \")}\\\" to determine state\"\n-        state = shell_out(defaults_export_cmd(new_resource), user: new_resource.user)\n+        Chef::Log.debug \"#load_current_value: attempting to read \\\"#{new_resource.domain}\\\" value from preferences to determine state\"\n \n-        if state.error? || state.stdout.empty?\n-          Chef::Log.debug \"#load_current_value: #{defaults_export_cmd(new_resource).join(\" \")} returned stdout: #{state.stdout} and stderr: #{state.stderr}\"\n-          current_value_does_not_exist!\n-        end\n+        pref = get_preference(new_resource)\n+        current_value_does_not_exist! if pref.nil?\n \n-        plist_data = ::Plist.parse_xml(state.stdout)\n-\n-        # handle the situation where the key doesn't exist in the domain\n-        if plist_data.key?(new_resource.key)\n-          key new_resource.key\n-        else\n-          current_value_does_not_exist!\n-        end\n-\n-        value plist_data[new_resource.key]\n-      end\n-\n-      #\n-      # The defaults command to export a domain\n-      #\n-      # @return [Array] defaults command\n-      #\n-      def defaults_export_cmd(resource)\n-        state_cmd = [\"/usr/bin/defaults\"]\n-\n-        if resource.host == \"current\"\n-          state_cmd.concat([\"-currentHost\"])\n-        elsif resource.host # they specified a non-nil value, which is a hostname\n-          state_cmd.concat([\"-host\", resource.host])\n-        end\n-\n-        state_cmd.concat([\"export\", resource.domain, \"-\"])\n-        state_cmd\n+        key new_resource.key\n+        value pref\n       end\n \n       action :write, description: \"Write the value to the specified domain/key.\" do\n         converge_if_changed do\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Updating defaults value by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Updating defaults value for #{new_resource.key} in #{new_resource.domain}\")\n+          set_preference(new_resource)\n         end\n       end\n \n       action :delete, description: \"Delete a key from a domain.\" do\n         # if it's not there there's nothing to remove\n-        return unless current_resource\n+        return if current_resource.nil?\n \n         converge_by(\"delete domain:#{new_resource.domain} key:#{new_resource.key}\") do\n-\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Removing defaults key by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Removing defaults key: #{new_resource.key}\")\n+          CF::Preferences.set!(new_resource.key, nil, new_resource.domain, new_resource.user, new_resource.host)\n         end\n       end\n \n-      action_class do\n-        #\n-        # The command used to write or delete delete values from domains\n-        #\n-        # @return [Array] Array representation of defaults command to run\n-        #\n-        def defaults_modify_cmd\n-          cmd = [\"/usr/bin/defaults\"]\n-\n-          if new_resource.host == :current\n-            cmd.concat([\"-currentHost\"])\n-          elsif new_resource.host # they specified a non-nil value, which is a hostname\n-            cmd.concat([\"-host\", new_resource.host])\n-          end\n-\n-          cmd.concat([action.to_s, new_resource.domain, new_resource.key])\n-          cmd.concat(processed_value) if action == :write\n-          cmd.prepend(\"sudo\") if new_resource.sudo\n-          cmd\n-        end\n+      def get_preference(new_resource)\n+        CF::Preferences.get(new_resource.key, new_resource.domain, new_resource.user, new_resource.host)\n+      end\n \n-        #\n-        # convert the provided value into the format defaults expects\n-        #\n-        # @return [array] array of values starting with the type if applicable\n-        #\n-        def processed_value\n-          type = new_resource.type || value_type(new_resource.value)\n-\n-          # when dict this creates an array of values [\"Key1\", \"Value1\", \"Key2\", \"Value2\" ...]\n-          cmd_values = [\"-#{type}\"]\n-\n-          case type\n-          when \"dict\"\n-            cmd_values.concat(new_resource.value.flatten)\n-          when \"array\"\n-            cmd_values.concat(new_resource.value)\n-          when \"bool\"\n-            cmd_values.concat(bool_to_defaults_bool(new_resource.value))\n-          else\n-            cmd_values.concat([new_resource.value])\n-          end\n-\n-          cmd_values\n-        end\n+      def set_preference(new_resource)\n+        CF::Preferences.set!(new_resource.key, new_resource.value, new_resource.domain, new_resource.user, new_resource.host)\n+      end",
        "comment_created_at": "2021-09-30T05:22:36+00:00",
        "comment_author": "rishichawda",
        "comment_body": "oh yeah I might have overlooked this after I moved the call directly inside the action.. will remove this now.. Thank you! ",
        "pr_file_module": null
      },
      {
        "comment_id": "719069595",
        "repo_full_name": "chef/chef",
        "pr_number": 11898,
        "pr_file": "lib/chef/resource/macos_userdefaults.rb",
        "discussion_id": "718895310",
        "commented_code": "@@ -78,173 +79,88 @@ class MacosUserDefaults < Chef::Resource\n         required: true\n \n       property :host, [String, Symbol],\n-        description: \"Set either :current or a hostname to set the user default at the host level.\",\n+        description: \"Set either :current, :all or a hostname to set the user default at the host level.\",\n         desired_state: false,\n-        introduced: \"16.3\"\n+        introduced: \"16.3\",\n+        coerce: proc { |value| to_cf_host(value) }\n \n       property :value, [Integer, Float, String, TrueClass, FalseClass, Hash, Array],\n         description: \"The value of the key. Note: With the `type` property set to `bool`, `String` forms of Boolean true/false values that Apple accepts in the defaults command will be coerced: 0/1, 'TRUE'/'FALSE,' 'true'/false', 'YES'/'NO', or 'yes'/'no'.\",\n-        required: [:write],\n-        coerce: proc { |v| v.is_a?(Hash) ? v.transform_keys(&:to_s) : v } # make sure keys are all strings for comparison\n+        required: [:write]\n \n       property :type, String,\n         description: \"The value type of the preference key.\",\n         equal_to: %w{bool string int float array dict},\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n-      property :user, String,\n-        description: \"The system user that the default will be applied to.\",\n-        desired_state: false\n+      property :user, [String, Symbol],\n+        description: \"The system user that the default will be applied to. Set :current for current user, :all for all users or pass a valid username\",\n+        desired_state: false,\n+        coerce: proc { |value| to_cf_user(value) }\n \n       property :sudo, [TrueClass, FalseClass],\n         description: \"Set to true if the setting you wish to modify requires privileged access. This requires passwordless sudo for the `/usr/bin/defaults` command to be setup for the user running #{ChefUtils::Dist::Infra::PRODUCT}.\",\n         default: false,\n-        desired_state: false\n+        desired_state: false,\n+        deprecated: true\n \n       load_current_value do |new_resource|\n-        Chef::Log.debug \"#load_current_value: shelling out \\\"#{defaults_export_cmd(new_resource).join(\" \")}\\\" to determine state\"\n-        state = shell_out(defaults_export_cmd(new_resource), user: new_resource.user)\n+        Chef::Log.debug \"#load_current_value: attempting to read \\\"#{new_resource.domain}\\\" value from preferences to determine state\"\n \n-        if state.error? || state.stdout.empty?\n-          Chef::Log.debug \"#load_current_value: #{defaults_export_cmd(new_resource).join(\" \")} returned stdout: #{state.stdout} and stderr: #{state.stderr}\"\n-          current_value_does_not_exist!\n-        end\n+        pref = get_preference(new_resource)\n+        current_value_does_not_exist! if pref.nil?\n \n-        plist_data = ::Plist.parse_xml(state.stdout)\n-\n-        # handle the situation where the key doesn't exist in the domain\n-        if plist_data.key?(new_resource.key)\n-          key new_resource.key\n-        else\n-          current_value_does_not_exist!\n-        end\n-\n-        value plist_data[new_resource.key]\n-      end\n-\n-      #\n-      # The defaults command to export a domain\n-      #\n-      # @return [Array] defaults command\n-      #\n-      def defaults_export_cmd(resource)\n-        state_cmd = [\"/usr/bin/defaults\"]\n-\n-        if resource.host == \"current\"\n-          state_cmd.concat([\"-currentHost\"])\n-        elsif resource.host # they specified a non-nil value, which is a hostname\n-          state_cmd.concat([\"-host\", resource.host])\n-        end\n-\n-        state_cmd.concat([\"export\", resource.domain, \"-\"])\n-        state_cmd\n+        key new_resource.key\n+        value pref\n       end\n \n       action :write, description: \"Write the value to the specified domain/key.\" do\n         converge_if_changed do\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Updating defaults value by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Updating defaults value for #{new_resource.key} in #{new_resource.domain}\")\n+          set_preference(new_resource)\n         end\n       end\n \n       action :delete, description: \"Delete a key from a domain.\" do\n         # if it's not there there's nothing to remove\n-        return unless current_resource\n+        return if current_resource.nil?\n \n         converge_by(\"delete domain:#{new_resource.domain} key:#{new_resource.key}\") do\n-\n-          cmd = defaults_modify_cmd\n-          Chef::Log.debug(\"Removing defaults key by shelling out: #{cmd.join(\" \")}\")\n-\n-          shell_out!(cmd, user: new_resource.user)\n+          Chef::Log.debug(\"Removing defaults key: #{new_resource.key}\")\n+          CF::Preferences.set!(new_resource.key, nil, new_resource.domain, new_resource.user, new_resource.host)\n         end\n       end\n \n-      action_class do\n-        #\n-        # The command used to write or delete delete values from domains\n-        #\n-        # @return [Array] Array representation of defaults command to run\n-        #\n-        def defaults_modify_cmd\n-          cmd = [\"/usr/bin/defaults\"]\n-\n-          if new_resource.host == :current\n-            cmd.concat([\"-currentHost\"])\n-          elsif new_resource.host # they specified a non-nil value, which is a hostname\n-            cmd.concat([\"-host\", new_resource.host])\n-          end\n-\n-          cmd.concat([action.to_s, new_resource.domain, new_resource.key])\n-          cmd.concat(processed_value) if action == :write\n-          cmd.prepend(\"sudo\") if new_resource.sudo\n-          cmd\n-        end\n+      def get_preference(new_resource)\n+        CF::Preferences.get(new_resource.key, new_resource.domain, new_resource.user, new_resource.host)\n+      end\n \n-        #\n-        # convert the provided value into the format defaults expects\n-        #\n-        # @return [array] array of values starting with the type if applicable\n-        #\n-        def processed_value\n-          type = new_resource.type || value_type(new_resource.value)\n-\n-          # when dict this creates an array of values [\"Key1\", \"Value1\", \"Key2\", \"Value2\" ...]\n-          cmd_values = [\"-#{type}\"]\n-\n-          case type\n-          when \"dict\"\n-            cmd_values.concat(new_resource.value.flatten)\n-          when \"array\"\n-            cmd_values.concat(new_resource.value)\n-          when \"bool\"\n-            cmd_values.concat(bool_to_defaults_bool(new_resource.value))\n-          else\n-            cmd_values.concat([new_resource.value])\n-          end\n-\n-          cmd_values\n-        end\n+      def set_preference(new_resource)\n+        CF::Preferences.set!(new_resource.key, new_resource.value, new_resource.domain, new_resource.user, new_resource.host)\n+      end",
        "comment_created_at": "2021-09-30T05:30:21+00:00",
        "comment_author": "rishichawda",
        "comment_body": "the `:write` action was using this function but `:delete` was using the `.set!` method from `CF` directly. Changed the `:write` to also use `set!` method in https://github.com/chef/chef/pull/11898/commits/858cc2258c6b0ad8add05c3dd011c986164b90e2. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "688705114",
    "pr_number": 11907,
    "pr_file": "lib/chef/resource/archive_file.rb",
    "created_at": "2021-08-13T18:28:12+00:00",
    "commented_code": "converge_by(\"set owner of files extracted in #{new_resource.destination} to #{new_resource.owner}:#{new_resource.group}\") do\n            archive = Archive::Reader.open_filename(new_resource.path)\n            archive.each_entry do |e|\n              FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n              file_dest = strip_components_from_path(e.pathname)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "688705114",
        "repo_full_name": "chef/chef",
        "pr_number": 11907,
        "pr_file": "lib/chef/resource/archive_file.rb",
        "discussion_id": "688705114",
        "commented_code": "@@ -119,7 +123,8 @@ class ArchiveFile < Chef::Resource\n           converge_by(\"set owner of files extracted in #{new_resource.destination} to #{new_resource.owner}:#{new_resource.group}\") do\n             archive = Archive::Reader.open_filename(new_resource.path)\n             archive.each_entry do |e|\n-              FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n+              file_dest = strip_components_from_path(e.pathname)",
        "comment_created_at": "2021-08-13T18:28:12+00:00",
        "comment_author": "jasonwbarnett",
        "comment_body": "This seems to be repeated 3 times in this resource which is screaming for some sort of abstraction. \"This\" being stripping the component from the path and then a guard clause (if/unless) to do something. Thinking a small class responsible for taking in an artifact and both stripping components and then returning a list of files that are applicable. Anyhow, I need to think about it more and I don't think it should hold this up given the unit test coverage but just wanted to dump what was in my brain.",
        "pr_file_module": null
      },
      {
        "comment_id": "689730505",
        "repo_full_name": "chef/chef",
        "pr_number": 11907,
        "pr_file": "lib/chef/resource/archive_file.rb",
        "discussion_id": "688705114",
        "commented_code": "@@ -119,7 +123,8 @@ class ArchiveFile < Chef::Resource\n           converge_by(\"set owner of files extracted in #{new_resource.destination} to #{new_resource.owner}:#{new_resource.group}\") do\n             archive = Archive::Reader.open_filename(new_resource.path)\n             archive.each_entry do |e|\n-              FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n+              file_dest = strip_components_from_path(e.pathname)",
        "comment_created_at": "2021-08-16T17:36:17+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "It looks to me like this functionality should go into `archive.each_entry(strip_components: new_resource.strip_components)` and the work should get done in ffi-libarchive and/or libarchive directly (no idea if libarchive supports that or not)",
        "pr_file_module": null
      },
      {
        "comment_id": "689784245",
        "repo_full_name": "chef/chef",
        "pr_number": 11907,
        "pr_file": "lib/chef/resource/archive_file.rb",
        "discussion_id": "688705114",
        "commented_code": "@@ -119,7 +123,8 @@ class ArchiveFile < Chef::Resource\n           converge_by(\"set owner of files extracted in #{new_resource.destination} to #{new_resource.owner}:#{new_resource.group}\") do\n             archive = Archive::Reader.open_filename(new_resource.path)\n             archive.each_entry do |e|\n-              FileUtils.chown(new_resource.owner, new_resource.group, \"#{new_resource.destination}/#{e.pathname}\")\n+              file_dest = strip_components_from_path(e.pathname)",
        "comment_created_at": "2021-08-16T18:59:48+00:00",
        "comment_author": "jasonwbarnett",
        "comment_body": "Completely agree with that in a pure OO sense, but I didn't know if that was violating any other principles for FFI specifically. Are you good with a PR to extend functionality on top of libarchive?",
        "pr_file_module": null
      }
    ]
  }
]
