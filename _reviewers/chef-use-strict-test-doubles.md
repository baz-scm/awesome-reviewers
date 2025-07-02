---
title: Use strict test doubles
description: Always use strict test doubles (instance_double, class_double) instead
  of basic doubles or OpenStruct in tests. Strict doubles provide compile-time checks
  that prevent tests from passing when the mocked interface changes, improving test
  maintainability and catching integration issues early.
repository: chef/chef
label: Testing
language: Ruby
comments_count: 4
repository_stars: 7860
---

Always use strict test doubles (instance_double, class_double) instead of basic doubles or OpenStruct in tests. Strict doubles provide compile-time checks that prevent tests from passing when the mocked interface changes, improving test maintainability and catching integration issues early.

Example - Instead of:
```ruby
auth_stub = double("vault auth", aws_iam: nil)
dummy = OpenStruct.new(stdout: output, exitstatus: 0)
```

Use:
```ruby
auth_stub = instance_double("VaultAuth", aws_iam: nil)
shell_out = instance_double(Mixlib::ShellOut,
  stdout: output,
  exitstatus: 0,
  error?: false
)
```

This approach:
- Ensures mocks accurately reflect the real interfaces
- Catches interface changes during test execution
- Makes dependencies explicit in test code
- Prevents tests from silently passing with invalid assumptions


[
  {
    "discussion_id": "477494373",
    "pr_number": 10171,
    "pr_file": "spec/unit/provider/mount/linux_spec.rb",
    "created_at": "2020-08-26T18:13:37+00:00",
    "commented_code": "require \"spec_helper\"\nrequire \"ostruct\"\n\ndescribe Chef::Provider::Mount::Linux do\n  before(:each) do\n    @node = Chef::Node.new\n    @events = Chef::EventDispatch::Dispatcher.new\n    @run_context = Chef::RunContext.new(@node, {}, @events)\n\n    @new_resource = Chef::Resource::Mount.new(\"/tmp/foo\")\n    @new_resource.device      \"/dev/sdz1\"\n    @new_resource.device_type :device\n    @new_resource.fstype      \"ext3\"\n\n    @new_resource.supports remount: false\n\n    @provider = Chef::Provider::Mount::Linux.new(@new_resource, @run_context)\n\n    allow(::File).to receive(:exists?).with(\"/dev/sdz1\").and_return true\n    allow(::File).to receive(:exists?).with(\"/tmp/foo\").and_return true\n    allow(::File).to receive(:realpath).with(\"/dev/sdz1\").and_return \"/dev/sdz1\"\n    allow(::File).to receive(:realpath).with(\"/tmp/foo\").and_return \"/tmp/foo\"\n  end\n\n  context \"to see if the volume is mounted\" do\n\n    it \"should set mounted true if the mount point is found in the mounts list\" do\n      allow(@provider).to receive(:shell_out!).and_return(OpenStruct.new(stdout: \"/tmp/foo /dev/sdz1 type ext3 (rw)\\n\"))",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "477494373",
        "repo_full_name": "chef/chef",
        "pr_number": 10171,
        "pr_file": "spec/unit/provider/mount/linux_spec.rb",
        "discussion_id": "477494373",
        "commented_code": "@@ -0,0 +1,91 @@\n+require \"spec_helper\"\n+require \"ostruct\"\n+\n+describe Chef::Provider::Mount::Linux do\n+  before(:each) do\n+    @node = Chef::Node.new\n+    @events = Chef::EventDispatch::Dispatcher.new\n+    @run_context = Chef::RunContext.new(@node, {}, @events)\n+\n+    @new_resource = Chef::Resource::Mount.new(\"/tmp/foo\")\n+    @new_resource.device      \"/dev/sdz1\"\n+    @new_resource.device_type :device\n+    @new_resource.fstype      \"ext3\"\n+\n+    @new_resource.supports remount: false\n+\n+    @provider = Chef::Provider::Mount::Linux.new(@new_resource, @run_context)\n+\n+    allow(::File).to receive(:exists?).with(\"/dev/sdz1\").and_return true\n+    allow(::File).to receive(:exists?).with(\"/tmp/foo\").and_return true\n+    allow(::File).to receive(:realpath).with(\"/dev/sdz1\").and_return \"/dev/sdz1\"\n+    allow(::File).to receive(:realpath).with(\"/tmp/foo\").and_return \"/tmp/foo\"\n+  end\n+\n+  context \"to see if the volume is mounted\" do\n+\n+    it \"should set mounted true if the mount point is found in the mounts list\" do\n+      allow(@provider).to receive(:shell_out!).and_return(OpenStruct.new(stdout: \"/tmp/foo /dev/sdz1 type ext3 (rw)\\n\"))",
        "comment_created_at": "2020-08-26T18:13:37+00:00",
        "comment_author": "phiggins",
        "comment_body": "```suggestion\r\n      allow(@provider).to receive(:shell_out!).and_return(double(stdout: \"/tmp/foo /dev/sdz1 type ext3 (rw)\\n\"))\r\n```\r\n\r\nSince an OpenStruct instance will respond to any method, this can cause problems in the future when the code changes in unexpected ways. Instead these tests should be explicit about what behavior is expected of the test objects.",
        "pr_file_module": null
      },
      {
        "comment_id": "478256789",
        "repo_full_name": "chef/chef",
        "pr_number": 10171,
        "pr_file": "spec/unit/provider/mount/linux_spec.rb",
        "discussion_id": "477494373",
        "commented_code": "@@ -0,0 +1,91 @@\n+require \"spec_helper\"\n+require \"ostruct\"\n+\n+describe Chef::Provider::Mount::Linux do\n+  before(:each) do\n+    @node = Chef::Node.new\n+    @events = Chef::EventDispatch::Dispatcher.new\n+    @run_context = Chef::RunContext.new(@node, {}, @events)\n+\n+    @new_resource = Chef::Resource::Mount.new(\"/tmp/foo\")\n+    @new_resource.device      \"/dev/sdz1\"\n+    @new_resource.device_type :device\n+    @new_resource.fstype      \"ext3\"\n+\n+    @new_resource.supports remount: false\n+\n+    @provider = Chef::Provider::Mount::Linux.new(@new_resource, @run_context)\n+\n+    allow(::File).to receive(:exists?).with(\"/dev/sdz1\").and_return true\n+    allow(::File).to receive(:exists?).with(\"/tmp/foo\").and_return true\n+    allow(::File).to receive(:realpath).with(\"/dev/sdz1\").and_return \"/dev/sdz1\"\n+    allow(::File).to receive(:realpath).with(\"/tmp/foo\").and_return \"/tmp/foo\"\n+  end\n+\n+  context \"to see if the volume is mounted\" do\n+\n+    it \"should set mounted true if the mount point is found in the mounts list\" do\n+      allow(@provider).to receive(:shell_out!).and_return(OpenStruct.new(stdout: \"/tmp/foo /dev/sdz1 type ext3 (rw)\\n\"))",
        "comment_created_at": "2020-08-27T08:45:09+00:00",
        "comment_author": "antima-gupta",
        "comment_body": "Agreed, I have updated the changes.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "696936306",
    "pr_number": 11942,
    "pr_file": "spec/unit/secret_fetcher/hashi_vault_spec.rb",
    "created_at": "2021-08-26T19:57:05+00:00",
    "commented_code": "#\n# Author:: Marc Paradise <marc@chef.io>\n# Copyright:: Copyright (c) Chef Software Inc.\n# License:: Apache License, Version 2.0\n#\n# Licensed under the Apache License, Version 2.0 (the \"License\");\n# you may not use this file except in compliance with the License.\n# You may obtain a copy of the License at\n#\n#     http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing, software\n# distributed under the License is distributed on an \"AS IS\" BASIS,\n# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n# See the License for the specific language governing permissions and\n# limitations under the License.\n#\n#\n\nrequire_relative \"../../spec_helper\"\nrequire \"chef/secret_fetcher/hashi_vault\"\n\ndescribe Chef::SecretFetcher::HashiVault do\n  let(:node) { {} }\n  let(:run_context) { double(\"run_context\", node: node) }\n  let(:fetcher_config) { {} }\n  let(:fetcher) {\n    Chef::SecretFetcher::HashiVault.new( fetcher_config, run_context )\n  }\n\n  context \"when validating HashiVault provided configuration\" do\n    context \"and role_name is not provided\" do\n      let(:fetcher_config) { { vault_addr: \"vault.example.com\" } }\n      it \"raises ConfigurationInvalid\" do\n        expect { fetcher.validate! }.to raise_error(Chef::Exceptions::Secret::ConfigurationInvalid)\n      end\n    end\n    context \"and vault_addr is not provided\" do\n      let(:fetcher_config) { { role_name: \"example-role\" } }\n      it \"raises ConfigurationInvalid\" do\n        expect { fetcher.validate! }.to raise_error(Chef::Exceptions::Secret::ConfigurationInvalid)\n      end\n    end\n  end\n\n  context \"when all required config is provided\" do\n    let(:fetcher_config) { { vault_addr: \"vault.example.com\", role_name: \"example-role\" } }\n    it \"obtains a token via AWS IAM auth\" do\n      auth_stub = double(\"vault auth\", aws_iam: nil)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "696936306",
        "repo_full_name": "chef/chef",
        "pr_number": 11942,
        "pr_file": "spec/unit/secret_fetcher/hashi_vault_spec.rb",
        "discussion_id": "696936306",
        "commented_code": "@@ -0,0 +1,57 @@\n+#\n+# Author:: Marc Paradise <marc@chef.io>\n+# Copyright:: Copyright (c) Chef Software Inc.\n+# License:: Apache License, Version 2.0\n+#\n+# Licensed under the Apache License, Version 2.0 (the \"License\");\n+# you may not use this file except in compliance with the License.\n+# You may obtain a copy of the License at\n+#\n+#     http://www.apache.org/licenses/LICENSE-2.0\n+#\n+# Unless required by applicable law or agreed to in writing, software\n+# distributed under the License is distributed on an \"AS IS\" BASIS,\n+# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+# See the License for the specific language governing permissions and\n+# limitations under the License.\n+#\n+#\n+\n+require_relative \"../../spec_helper\"\n+require \"chef/secret_fetcher/hashi_vault\"\n+\n+describe Chef::SecretFetcher::HashiVault do\n+  let(:node) { {} }\n+  let(:run_context) { double(\"run_context\", node: node) }\n+  let(:fetcher_config) { {} }\n+  let(:fetcher) {\n+    Chef::SecretFetcher::HashiVault.new( fetcher_config, run_context )\n+  }\n+\n+  context \"when validating HashiVault provided configuration\" do\n+    context \"and role_name is not provided\" do\n+      let(:fetcher_config) { { vault_addr: \"vault.example.com\" } }\n+      it \"raises ConfigurationInvalid\" do\n+        expect { fetcher.validate! }.to raise_error(Chef::Exceptions::Secret::ConfigurationInvalid)\n+      end\n+    end\n+    context \"and vault_addr is not provided\" do\n+      let(:fetcher_config) { { role_name: \"example-role\" } }\n+      it \"raises ConfigurationInvalid\" do\n+        expect { fetcher.validate! }.to raise_error(Chef::Exceptions::Secret::ConfigurationInvalid)\n+      end\n+    end\n+  end\n+\n+  context \"when all required config is provided\" do\n+    let(:fetcher_config) { { vault_addr: \"vault.example.com\", role_name: \"example-role\" } }\n+    it \"obtains a token via AWS IAM auth\" do\n+      auth_stub = double(\"vault auth\", aws_iam: nil)",
        "comment_created_at": "2021-08-26T19:57:05+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "that should really be an `instance_double` of the appropriate type",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "662629591",
    "pr_number": 11534,
    "pr_file": "spec/unit/resource/rhsm_subscription_spec.rb",
    "created_at": "2021-07-01T22:35:49+00:00",
    "commented_code": "expect { resource.action :remove }.not_to raise_error\n  end\n\n  describe \"#action_attach\" do\n    before do\n      dummy = Mixlib::ShellOut.new\n      allow_any_instance_of(Chef::Mixin::ShellOut).to receive(:shell_out!).with(\"subscription-manager attach --pool=#{resource.pool_id}\").and_return(dummy)\n      allow(dummy).to receive(:stdout).and_return(\"Successfully attached a subscription for: My Subscription\")\n      allow(dummy).to receive(:exitstatus).and_return(0)\n      allow(dummy).to receive(:error?).and_return(false)\n      node.automatic_attrs[:platform_family] = \"rhel\"\n      node.automatic_attrs[:platform_version] = \"7.3\"\n      allow_any_instance_of(Chef::Provider::Package::Yum).to receive(:installed_version).with(0).and_return(Chef::Provider::Package::Yum::Version.new(nil, nil, nil))\n      allow_any_instance_of(Chef::Provider::Package::Yum).to receive(:available_version).with(0).and_return(Chef::Provider::Package::Yum::Version.new(nil, nil, nil))\n      allow_any_instance_of(Chef::Provider::Package::Yum::PythonHelper).to receive(:close_rpmdb)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "662629591",
        "repo_full_name": "chef/chef",
        "pr_number": 11534,
        "pr_file": "spec/unit/resource/rhsm_subscription_spec.rb",
        "discussion_id": "662629591",
        "commented_code": "@@ -38,6 +43,46 @@\n     expect { resource.action :remove }.not_to raise_error\n   end\n \n+  describe \"#action_attach\" do\n+    before do\n+      dummy = Mixlib::ShellOut.new\n+      allow_any_instance_of(Chef::Mixin::ShellOut).to receive(:shell_out!).with(\"subscription-manager attach --pool=#{resource.pool_id}\").and_return(dummy)\n+      allow(dummy).to receive(:stdout).and_return(\"Successfully attached a subscription for: My Subscription\")\n+      allow(dummy).to receive(:exitstatus).and_return(0)\n+      allow(dummy).to receive(:error?).and_return(false)\n+      node.automatic_attrs[:platform_family] = \"rhel\"\n+      node.automatic_attrs[:platform_version] = \"7.3\"\n+      allow_any_instance_of(Chef::Provider::Package::Yum).to receive(:installed_version).with(0).and_return(Chef::Provider::Package::Yum::Version.new(nil, nil, nil))\n+      allow_any_instance_of(Chef::Provider::Package::Yum).to receive(:available_version).with(0).and_return(Chef::Provider::Package::Yum::Version.new(nil, nil, nil))\n+      allow_any_instance_of(Chef::Provider::Package::Yum::PythonHelper).to receive(:close_rpmdb)",
        "comment_created_at": "2021-07-01T22:35:49+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "You're trying way too hard here.  You're testing that the details of the ResourceResolver correctly give back a Chef::Package::Provider::Yum when you're forcing the distro version, which is duplicating all the testing which goes on already to prove that happens.\r\n\r\nI'd just create a double object and:\r\n\r\n```\r\nexpect(provider).to receive(:build_resource).with(<stuff>).and_return(mydouble)\r\nexpect(mydouble).to receive(:run_action).with(:flush_cache)\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "662633326",
    "pr_number": 11534,
    "pr_file": "spec/unit/resource/rhsm_subscription_spec.rb",
    "created_at": "2021-07-01T22:46:57+00:00",
    "commented_code": "expect { resource.action :remove }.not_to raise_error\n  end\n\n  describe \"#action_attach\" do\n    before do\n      dummy = Mixlib::ShellOut.new\n      allow_any_instance_of(Chef::Mixin::ShellOut).to receive(:shell_out!).with(\"subscription-manager attach --pool=#{resource.pool_id}\").and_return(dummy)\n      allow(dummy).to receive(:stdout).and_return(\"Successfully attached a subscription for: My Subscription\")\n      allow(dummy).to receive(:exitstatus).and_return(0)\n      allow(dummy).to receive(:error?).and_return(false)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "662633326",
        "repo_full_name": "chef/chef",
        "pr_number": 11534,
        "pr_file": "spec/unit/resource/rhsm_subscription_spec.rb",
        "discussion_id": "662633326",
        "commented_code": "@@ -38,6 +43,46 @@\n     expect { resource.action :remove }.not_to raise_error\n   end\n \n+  describe \"#action_attach\" do\n+    before do\n+      dummy = Mixlib::ShellOut.new\n+      allow_any_instance_of(Chef::Mixin::ShellOut).to receive(:shell_out!).with(\"subscription-manager attach --pool=#{resource.pool_id}\").and_return(dummy)\n+      allow(dummy).to receive(:stdout).and_return(\"Successfully attached a subscription for: My Subscription\")\n+      allow(dummy).to receive(:exitstatus).and_return(0)\n+      allow(dummy).to receive(:error?).and_return(false)",
        "comment_created_at": "2021-07-01T22:46:57+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "Here also you should stub at the level of:\r\n\r\n```\r\nso = instance_double(Mixlib::ShellOut)\r\nexpect(provider).to receive(:shell_out!).with(<...>).and_return(so)\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
