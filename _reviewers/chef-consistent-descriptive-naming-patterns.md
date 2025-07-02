---
title: Consistent descriptive naming patterns
description: 'Use clear, descriptive names that follow consistent patterns across
  the codebase. For methods and properties:


  1. Use intention-revealing names that clearly indicate purpose'
repository: chef/chef
label: Naming Conventions
language: Ruby
comments_count: 7
repository_stars: 7860
---

Use clear, descriptive names that follow consistent patterns across the codebase. For methods and properties:

1. Use intention-revealing names that clearly indicate purpose
2. For boolean methods, use question-mark suffixes and appropriate prefixes
3. Maintain consistent naming patterns across similar properties
4. Use lowercase for variables unless they are true constants

Examples:
```ruby
# Poor naming
def compare_users  # unclear if returns boolean
def detect_certificate_key  # verb is ambiguous
property :certpassword  # inconsistent with other properties

# Good naming
def users_changed?  # clear boolean return
def certificate_key_exist?  # clear boolean check
property :cert_password  # consistent with other properties

# Property naming consistency
property :user      # preferred over user_name
property :password  # preferred over pass
```

This pattern improves code readability, maintains consistency, and reduces cognitive load when working across different parts of the codebase.


[
  {
    "discussion_id": "1733480952",
    "pr_number": 14352,
    "pr_file": "chef-config/lib/chef-config/path_helper.rb",
    "created_at": "2024-08-27T20:34:11+00:00",
    "commented_code": "end\n\n    def self.relative_path_from(from, to, windows: ChefUtils.windows?)\n      Pathname.new(cleanpath(to, windows: windows)).relative_path_from(Pathname.new(cleanpath(from, windows: windows)))\n      if windows\n        Pathname.new(cleanpath(to, windows: windows)).relative_path_from(Pathname.new(cleanpath(from, windows: windows)))\n      else\n        # On non-Windows we can halve the number of cleanpath calls by doing a\n        # single gsub! call here\n\n        path = Pathname.new(to).relative_path_from(Pathname.new(from)).to_s\n        # ensure all backslashes are forward slashes\n        path.gsub!(BACKSLASH, File::SEPARATOR)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1733480952",
        "repo_full_name": "chef/chef",
        "pr_number": 14352,
        "pr_file": "chef-config/lib/chef-config/path_helper.rb",
        "discussion_id": "1733480952",
        "commented_code": "@@ -200,7 +200,17 @@ def self.escape_glob_dir(*parts)\n     end\n \n     def self.relative_path_from(from, to, windows: ChefUtils.windows?)\n-      Pathname.new(cleanpath(to, windows: windows)).relative_path_from(Pathname.new(cleanpath(from, windows: windows)))\n+      if windows\n+        Pathname.new(cleanpath(to, windows: windows)).relative_path_from(Pathname.new(cleanpath(from, windows: windows)))\n+      else\n+        # On non-Windows we can halve the number of cleanpath calls by doing a\n+        # single gsub! call here\n+\n+        path = Pathname.new(to).relative_path_from(Pathname.new(from)).to_s\n+        # ensure all backslashes are forward slashes\n+        path.gsub!(BACKSLASH, File::SEPARATOR)",
        "comment_created_at": "2024-08-27T20:34:11+00:00",
        "comment_author": "jaymzh",
        "comment_body": "this _is_ cleanpath, so just call cleanpath.\r\n\r\nAnd you can add the ! there if you want.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "492231182",
    "pr_number": 10122,
    "pr_file": "lib/chef/resource/windows_share.rb",
    "created_at": "2020-09-21T17:33:02+00:00",
    "commented_code": "# bool ? 1 : 0\n          bool ? \"$true\" : \"$false\"\n        end\n\n        # Grant-SmbShareAccess sets only one permission to one user so we need to remove from the lower permission access\n        # For change_users remove common full_users from it\n        # For read_users remove common full_users as well as change_users\n        def new_resource_users\n          users = {}\n          users[\"full_users\"] = new_resource.full_users\n\n          users[\"change_users\"] = new_resource.change_users - new_resource.full_users\n          users[\"read_users\"] = new_resource.read_users - (new_resource.full_users + new_resource.change_users)\n          users\n        end\n\n        # Compare the full_users, change_users and read_users from current_resource and new_resource\n        # @returns boolean True/False\n        def compare_users",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "492231182",
        "repo_full_name": "chef/chef",
        "pr_number": 10122,
        "pr_file": "lib/chef/resource/windows_share.rb",
        "discussion_id": "492231182",
        "commented_code": "@@ -338,8 +335,38 @@ def bool_string(bool)\n           # bool ? 1 : 0\n           bool ? \"$true\" : \"$false\"\n         end\n+\n+        # Grant-SmbShareAccess sets only one permission to one user so we need to remove from the lower permission access\n+        # For change_users remove common full_users from it\n+        # For read_users remove common full_users as well as change_users\n+        def new_resource_users\n+          users = {}\n+          users[\"full_users\"] = new_resource.full_users\n+\n+          users[\"change_users\"] = new_resource.change_users - new_resource.full_users\n+          users[\"read_users\"] = new_resource.read_users - (new_resource.full_users + new_resource.change_users)\n+          users\n+        end\n+\n+        # Compare the full_users, change_users and read_users from current_resource and new_resource\n+        # @returns boolean True/False\n+        def compare_users",
        "comment_created_at": "2020-09-21T17:33:02+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "This should be named something like `def users_changed?` and the sense of it should be inverted (this makes it read nicer without the NOT when it gets used above)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "877456722",
    "pr_number": 12859,
    "pr_file": "lib/chef/resource/windows_certificate.rb",
    "created_at": "2022-05-19T19:22:21+00:00",
    "commented_code": "end\n\n      action :delete, description: \"Deletes a certificate.\" do\n        cert_obj = fetch_cert\n        cert_obj = verify_cert\n\n        if cert_obj\n        if cert_obj == true || cert_obj == \"Certificate Has Expired\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "877456722",
        "repo_full_name": "chef/chef",
        "pr_number": 12859,
        "pr_file": "lib/chef/resource/windows_certificate.rb",
        "discussion_id": "877456722",
        "commented_code": "@@ -128,14 +128,14 @@ class WindowsCertificate < Chef::Resource\n       end\n \n       action :delete, description: \"Deletes a certificate.\" do\n-        cert_obj = fetch_cert\n+        cert_obj = verify_cert\n \n-        if cert_obj\n+        if cert_obj == true || cert_obj == \"Certificate Has Expired\"",
        "comment_created_at": "2022-05-19T19:22:21+00:00",
        "comment_author": "marcparadise",
        "comment_body": "`verify_cert` only returns a `true` or `false`, so this condition can never be met. \r\n\r\nGiven that, can we change `cert_obj` name to something like `cert_is_valid`? ",
        "pr_file_module": null
      },
      {
        "comment_id": "878788518",
        "repo_full_name": "chef/chef",
        "pr_number": 12859,
        "pr_file": "lib/chef/resource/windows_certificate.rb",
        "discussion_id": "877456722",
        "commented_code": "@@ -128,14 +128,14 @@ class WindowsCertificate < Chef::Resource\n       end\n \n       action :delete, description: \"Deletes a certificate.\" do\n-        cert_obj = fetch_cert\n+        cert_obj = verify_cert\n \n-        if cert_obj\n+        if cert_obj == true || cert_obj == \"Certificate Has Expired\"",
        "comment_created_at": "2022-05-22T03:45:50+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "ooh, good catch. Thanks. Done and done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "540443869",
    "pr_number": 10621,
    "pr_file": "lib/chef/resource/homebrew_install.rb",
    "created_at": "2020-12-10T19:37:23+00:00",
    "commented_code": "#\n# Copyright:: Copyright (c) Chef Software Inc.\n#\n# Licensed under the Apache License, Version 2.0 (the \"License\");\n# you may not use this file except in compliance with the License.\n# You may obtain a copy of the License at\n#\n#     http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing, software\n# distributed under the License is distributed on an \"AS IS\" BASIS,\n# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n# See the License for the specific language governing permissions and\n# limitations under the License.\n#\n\nrequire_relative \"../resource\"\n\nclass Chef\n  class Resource\n    class HomebrewInstall < Chef::Resource\n      unified_mode true\n\n      provides :homebrew_install\n\n      description \"Use the **homebrew_install** resource to install the Homebrew package manager on macOS systems.\"\n      introduced \"16.8\"\n      examples <<~DOC\n      **Install Homebrew using the Internet to download Command Line Tools for Xcode**:\n      ```ruby\n      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n        user 'someuser'\n        action :install\n      end\n      ```\n      **Install Homebrew using a customer-managed source to download Command Line Tools for Xcode from**:\n      ```ruby\n      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n        xcode_tools_url 'https://somewhere.something.com/downloads/command_line_tools.dmg'\n        xcode_tools_pkg_name 'Command Line Tools.pkg'\n        user 'someuser'\n        action :install\n      end\n      ```\n      DOC\n\n      property :xcode_tools_url, String,\n        description: \"A url pointing to a 'Command Line Tools for Xcode' dmg file\"\n\n      property :xcode_tools_pkg_name, String,\n        description: \"The name of the pkg inside the dmg located at the xcode_tools_url\"\n\n      property :brew_source_url, String,\n        description: \"A url pointing to a Homebrew installer\",\n        default: \"https://codeload.github.com/Homebrew/brew/zip/master\"\n\n      property :user, String,\n        description: \"The user to install Homebrew as. Note: Homebrew cannot be installed as root.\",\n        required: true\n\n      action :install do\n        # Avoid all the work in the below resources if homebrew is already installed\n        return if ::File.exist?(\"/usr/local/bin/brew\")\n\n        # check if 'user' is root and raise an exception if so\n        if Etc.getpwnam(new_resource.user).uid == 0\n          msg = \"You are attempting to install Homebrew as Root. This is not permitted by Homebrew. Please run this as a standard user with admin rights\"\n          raise Chef::Exceptions::InsufficientPermissions, msg\n        end\n\n        USER_HOME = Dir.home(new_resource.user).freeze",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "540443869",
        "repo_full_name": "chef/chef",
        "pr_number": 10621,
        "pr_file": "lib/chef/resource/homebrew_install.rb",
        "discussion_id": "540443869",
        "commented_code": "@@ -0,0 +1,148 @@\n+#\n+# Copyright:: Copyright (c) Chef Software Inc.\n+#\n+# Licensed under the Apache License, Version 2.0 (the \"License\");\n+# you may not use this file except in compliance with the License.\n+# You may obtain a copy of the License at\n+#\n+#     http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing, software\n+# distributed under the License is distributed on an \"AS IS\" BASIS,\n+# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+# See the License for the specific language governing permissions and\n+# limitations under the License.\n+#\n+\n+require_relative \"../resource\"\n+\n+class Chef\n+  class Resource\n+    class HomebrewInstall < Chef::Resource\n+      unified_mode true\n+\n+      provides :homebrew_install\n+\n+      description \"Use the **homebrew_install** resource to install the Homebrew package manager on macOS systems.\"\n+      introduced \"16.8\"\n+      examples <<~DOC\n+      **Install Homebrew using the Internet to download Command Line Tools for Xcode**:\n+      ```ruby\n+      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n+        user 'someuser'\n+        action :install\n+      end\n+      ```\n+      **Install Homebrew using a customer-managed source to download Command Line Tools for Xcode from**:\n+      ```ruby\n+      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n+        xcode_tools_url 'https://somewhere.something.com/downloads/command_line_tools.dmg'\n+        xcode_tools_pkg_name 'Command Line Tools.pkg'\n+        user 'someuser'\n+        action :install\n+      end\n+      ```\n+      DOC\n+\n+      property :xcode_tools_url, String,\n+        description: \"A url pointing to a 'Command Line Tools for Xcode' dmg file\"\n+\n+      property :xcode_tools_pkg_name, String,\n+        description: \"The name of the pkg inside the dmg located at the xcode_tools_url\"\n+\n+      property :brew_source_url, String,\n+        description: \"A url pointing to a Homebrew installer\",\n+        default: \"https://codeload.github.com/Homebrew/brew/zip/master\"\n+\n+      property :user, String,\n+        description: \"The user to install Homebrew as. Note: Homebrew cannot be installed as root.\",\n+        required: true\n+\n+      action :install do\n+        # Avoid all the work in the below resources if homebrew is already installed\n+        return if ::File.exist?(\"/usr/local/bin/brew\")\n+\n+        # check if 'user' is root and raise an exception if so\n+        if Etc.getpwnam(new_resource.user).uid == 0\n+          msg = \"You are attempting to install Homebrew as Root. This is not permitted by Homebrew. Please run this as a standard user with admin rights\"\n+          raise Chef::Exceptions::InsufficientPermissions, msg\n+        end\n+\n+        USER_HOME = Dir.home(new_resource.user).freeze",
        "comment_created_at": "2020-12-10T19:37:23+00:00",
        "comment_author": "tas50",
        "comment_body": "we should make these lowercase since they're not really constants and that gets confusing",
        "pr_file_module": null
      },
      {
        "comment_id": "540525347",
        "repo_full_name": "chef/chef",
        "pr_number": 10621,
        "pr_file": "lib/chef/resource/homebrew_install.rb",
        "discussion_id": "540443869",
        "commented_code": "@@ -0,0 +1,148 @@\n+#\n+# Copyright:: Copyright (c) Chef Software Inc.\n+#\n+# Licensed under the Apache License, Version 2.0 (the \"License\");\n+# you may not use this file except in compliance with the License.\n+# You may obtain a copy of the License at\n+#\n+#     http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing, software\n+# distributed under the License is distributed on an \"AS IS\" BASIS,\n+# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+# See the License for the specific language governing permissions and\n+# limitations under the License.\n+#\n+\n+require_relative \"../resource\"\n+\n+class Chef\n+  class Resource\n+    class HomebrewInstall < Chef::Resource\n+      unified_mode true\n+\n+      provides :homebrew_install\n+\n+      description \"Use the **homebrew_install** resource to install the Homebrew package manager on macOS systems.\"\n+      introduced \"16.8\"\n+      examples <<~DOC\n+      **Install Homebrew using the Internet to download Command Line Tools for Xcode**:\n+      ```ruby\n+      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n+        user 'someuser'\n+        action :install\n+      end\n+      ```\n+      **Install Homebrew using a customer-managed source to download Command Line Tools for Xcode from**:\n+      ```ruby\n+      homebrew_install 'Install Homebrew and xcode command line tools if necessary' do\n+        xcode_tools_url 'https://somewhere.something.com/downloads/command_line_tools.dmg'\n+        xcode_tools_pkg_name 'Command Line Tools.pkg'\n+        user 'someuser'\n+        action :install\n+      end\n+      ```\n+      DOC\n+\n+      property :xcode_tools_url, String,\n+        description: \"A url pointing to a 'Command Line Tools for Xcode' dmg file\"\n+\n+      property :xcode_tools_pkg_name, String,\n+        description: \"The name of the pkg inside the dmg located at the xcode_tools_url\"\n+\n+      property :brew_source_url, String,\n+        description: \"A url pointing to a Homebrew installer\",\n+        default: \"https://codeload.github.com/Homebrew/brew/zip/master\"\n+\n+      property :user, String,\n+        description: \"The user to install Homebrew as. Note: Homebrew cannot be installed as root.\",\n+        required: true\n+\n+      action :install do\n+        # Avoid all the work in the below resources if homebrew is already installed\n+        return if ::File.exist?(\"/usr/local/bin/brew\")\n+\n+        # check if 'user' is root and raise an exception if so\n+        if Etc.getpwnam(new_resource.user).uid == 0\n+          msg = \"You are attempting to install Homebrew as Root. This is not permitted by Homebrew. Please run this as a standard user with admin rights\"\n+          raise Chef::Exceptions::InsufficientPermissions, msg\n+        end\n+\n+        USER_HOME = Dir.home(new_resource.user).freeze",
        "comment_created_at": "2020-12-10T21:55:45+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "706317185",
    "pr_number": 11834,
    "pr_file": "lib/chef/http/authenticator.rb",
    "created_at": "2021-09-10T16:30:00+00:00",
    "commented_code": "@auth_credentials.client_name\n      end\n\n      def detect_certificate_key(client_name)\n        self.class.detect_certificate_key(client_name)\n      end\n\n      def check_certstore_for_key(client_name)\n        self.class.check_certstore_for_key(client_name)\n      end\n\n      def retrieve_certificate_key(client_name)\n        self.class.retrieve_certificate_key(client_name)\n      end\n\n      # Detects if a private key exists in a certificate repository like Keychain (macOS) or Certificate Store (Windows)\n      #\n      # @param client_name - we're using the node name to store and retrieve any keys\n      # Returns true if a key is found, false if not. False will trigger a registration event which will lead to a certificate based key being created\n      #\n      #\n      def self.detect_certificate_key(client_name)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "706317185",
        "repo_full_name": "chef/chef",
        "pr_number": 11834,
        "pr_file": "lib/chef/http/authenticator.rb",
        "discussion_id": "706317185",
        "commented_code": "@@ -83,8 +85,54 @@ def client_name\n         @auth_credentials.client_name\n       end\n \n+      def detect_certificate_key(client_name)\n+        self.class.detect_certificate_key(client_name)\n+      end\n+\n+      def check_certstore_for_key(client_name)\n+        self.class.check_certstore_for_key(client_name)\n+      end\n+\n+      def retrieve_certificate_key(client_name)\n+        self.class.retrieve_certificate_key(client_name)\n+      end\n+\n+      # Detects if a private key exists in a certificate repository like Keychain (macOS) or Certificate Store (Windows)\n+      #\n+      # @param client_name - we're using the node name to store and retrieve any keys\n+      # Returns true if a key is found, false if not. False will trigger a registration event which will lead to a certificate based key being created\n+      #\n+      #\n+      def self.detect_certificate_key(client_name)",
        "comment_created_at": "2021-09-10T16:30:00+00:00",
        "comment_author": "marcparadise",
        "comment_body": "Could we use `certificate_key_exist?` instead of `detect_certificate_key`? ",
        "pr_file_module": null
      },
      {
        "comment_id": "717020015",
        "repo_full_name": "chef/chef",
        "pr_number": 11834,
        "pr_file": "lib/chef/http/authenticator.rb",
        "discussion_id": "706317185",
        "commented_code": "@@ -83,8 +85,54 @@ def client_name\n         @auth_credentials.client_name\n       end\n \n+      def detect_certificate_key(client_name)\n+        self.class.detect_certificate_key(client_name)\n+      end\n+\n+      def check_certstore_for_key(client_name)\n+        self.class.check_certstore_for_key(client_name)\n+      end\n+\n+      def retrieve_certificate_key(client_name)\n+        self.class.retrieve_certificate_key(client_name)\n+      end\n+\n+      # Detects if a private key exists in a certificate repository like Keychain (macOS) or Certificate Store (Windows)\n+      #\n+      # @param client_name - we're using the node name to store and retrieve any keys\n+      # Returns true if a key is found, false if not. False will trigger a registration event which will lead to a certificate based key being created\n+      #\n+      #\n+      def self.detect_certificate_key(client_name)",
        "comment_created_at": "2021-09-27T20:26:24+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "726525272",
    "pr_number": 12159,
    "pr_file": "lib/chef/resource/chocolatey_source.rb",
    "created_at": "2021-10-11T19:38:40+00:00",
    "commented_code": "property :disabled, [TrueClass, FalseClass], default: false, desired_state: false, skip_docs: true\n\n      property :username, String,\n               description: \"The username to use when authenticating against the source\",\n               introduced: \"17.8\"\n\n      property :password, String, sensitive: true, desired_state: false,\n               description: \"The password to use when authenticating against the source\",\n               introduced: \"17.8\"\n\n      property :cert, String,\n               description: \"The certificate to use when authenticating against the source\",\n               introduced: \"17.8\"\n\n      property :certpassword, String, sensitive: true, desired_state: false,",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "726525272",
        "repo_full_name": "chef/chef",
        "pr_number": 12159,
        "pr_file": "lib/chef/resource/chocolatey_source.rb",
        "discussion_id": "726525272",
        "commented_code": "@@ -63,6 +63,22 @@ class ChocolateySource < Chef::Resource\n \n       property :disabled, [TrueClass, FalseClass], default: false, desired_state: false, skip_docs: true\n \n+      property :username, String,\n+               description: \"The username to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :password, String, sensitive: true, desired_state: false,\n+               description: \"The password to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :cert, String,\n+               description: \"The certificate to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :certpassword, String, sensitive: true, desired_state: false,",
        "comment_created_at": "2021-10-11T19:38:40+00:00",
        "comment_author": "tas50",
        "comment_body": "This should probably be `cert_password` for readability ",
        "pr_file_module": null
      },
      {
        "comment_id": "726555644",
        "repo_full_name": "chef/chef",
        "pr_number": 12159,
        "pr_file": "lib/chef/resource/chocolatey_source.rb",
        "discussion_id": "726525272",
        "commented_code": "@@ -63,6 +63,22 @@ class ChocolateySource < Chef::Resource\n \n       property :disabled, [TrueClass, FalseClass], default: false, desired_state: false, skip_docs: true\n \n+      property :username, String,\n+               description: \"The username to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :password, String, sensitive: true, desired_state: false,\n+               description: \"The password to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :cert, String,\n+               description: \"The certificate to use when authenticating against the source\",\n+               introduced: \"17.8\"\n+\n+      property :certpassword, String, sensitive: true, desired_state: false,",
        "comment_created_at": "2021-10-11T20:41:06+00:00",
        "comment_author": "gep13",
        "comment_body": "I will get that updated :+1:",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "716147106",
    "pr_number": 12029,
    "pr_file": "lib/chef/resource/powershell_package_source.rb",
    "created_at": "2021-09-26T05:58:36+00:00",
    "commented_code": "provides :powershell_package_source\n\n      description \"Use the **powershell_package_source** resource to register a PowerShell package repository.\"\n      description \"Use the **powershell_package_source** resource to register a PowerShell Repository or other Package Source type with. There are 2 distinct objects we care about here. The first is a Package Source like a PowerShell Repository or a Nuget Source. The second object is a provider that PowerShell uses to get to that source with, like PowerShellGet, Nuget, Chocolatey, etc. \"\n      introduced \"14.3\"\n      examples <<~DOC\n        **Add a new PSRepository that is not trusted and which requires credentials to connect to**:\n\n        ```ruby\n        powershell_package_source 'PowerShellModules' do\n          source_name                  \"PowerShellModules\"\n          source_location              \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n          publish_location             \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n          trusted                      false\n          user_name                    \"someuser@somelocation.io\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "716147106",
        "repo_full_name": "chef/chef",
        "pr_number": 12029,
        "pr_file": "lib/chef/resource/powershell_package_source.rb",
        "discussion_id": "716147106",
        "commented_code": "@@ -24,36 +25,131 @@ class PowershellPackageSource < Chef::Resource\n \n       provides :powershell_package_source\n \n-      description \"Use the **powershell_package_source** resource to register a PowerShell package repository.\"\n+      description \"Use the **powershell_package_source** resource to register a PowerShell Repository or other Package Source type with. There are 2 distinct objects we care about here. The first is a Package Source like a PowerShell Repository or a Nuget Source. The second object is a provider that PowerShell uses to get to that source with, like PowerShellGet, Nuget, Chocolatey, etc. \"\n       introduced \"14.3\"\n+      examples <<~DOC\n+        **Add a new PSRepository that is not trusted and which requires credentials to connect to**:\n+\n+        ```ruby\n+        powershell_package_source 'PowerShellModules' do\n+          source_name                  \"PowerShellModules\"\n+          source_location              \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n+          publish_location             \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n+          trusted                      false\n+          user_name                    \"someuser@somelocation.io\"",
        "comment_created_at": "2021-09-26T05:58:36+00:00",
        "comment_author": "tas50",
        "comment_body": "In our other resources we use 'user' and 'password'. We should be consistent here.",
        "pr_file_module": null
      },
      {
        "comment_id": "719671548",
        "repo_full_name": "chef/chef",
        "pr_number": 12029,
        "pr_file": "lib/chef/resource/powershell_package_source.rb",
        "discussion_id": "716147106",
        "commented_code": "@@ -24,36 +25,131 @@ class PowershellPackageSource < Chef::Resource\n \n       provides :powershell_package_source\n \n-      description \"Use the **powershell_package_source** resource to register a PowerShell package repository.\"\n+      description \"Use the **powershell_package_source** resource to register a PowerShell Repository or other Package Source type with. There are 2 distinct objects we care about here. The first is a Package Source like a PowerShell Repository or a Nuget Source. The second object is a provider that PowerShell uses to get to that source with, like PowerShellGet, Nuget, Chocolatey, etc. \"\n       introduced \"14.3\"\n+      examples <<~DOC\n+        **Add a new PSRepository that is not trusted and which requires credentials to connect to**:\n+\n+        ```ruby\n+        powershell_package_source 'PowerShellModules' do\n+          source_name                  \"PowerShellModules\"\n+          source_location              \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n+          publish_location             \"https://pkgs.dev.azure.com/some-org/some-project/_packaging/some_feed/nuget/v2\"\n+          trusted                      false\n+          user_name                    \"someuser@somelocation.io\"",
        "comment_created_at": "2021-09-30T18:47:31+00:00",
        "comment_author": "johnmccrae",
        "comment_body": "corrected",
        "pr_file_module": null
      }
    ]
  }
]
