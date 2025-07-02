---
title: Standardize installation directory paths
description: Maintain consistent and separate installation paths for different build
  types to prevent conflicts and improve system organization. Use `/hab` directory
  for Habitat builds and `/opt/chef` for Omnibus installations.
repository: chef/chef
label: Configurations
language: Other
comments_count: 4
repository_stars: 7860
---

Maintain consistent and separate installation paths for different build types to prevent conflicts and improve system organization. Use `/hab` directory for Habitat builds and `/opt/chef` for Omnibus installations.

Key guidelines:
- Place Habitat-built components under `/hab/` directory
- Keep Omnibus installations under `/opt/chef/`
- Use distinct directories for migration tools (e.g., `/hab/migration/`)
- Avoid mixing paths between build types

Example directory structure:
```
# Habitat builds
/hab/
  ├── chef/
  │   └── bin/
  └── migration/
      ├── bin/
      └── bundle/

# Omnibus installations
/opt/chef/
  ├── bin/
  └── bundle/
```

This separation enables:
- Clear distinction between installation types
- Easier cookbook checks and compatibility verification
- Simplified upgrade paths
- Prevention of file conflicts between different versions


[
  {
    "discussion_id": "1928142368",
    "pr_number": 14820,
    "pr_file": "knife/Gemfile",
    "created_at": "2025-01-24T06:18:23+00:00",
    "commented_code": "gem \"crack\", \"< 0.4.6\" # due to https://github.com/jnunemaker/crack/pull/75\n  gem \"rake\", \">= 12.3.3\"\n  gem \"rspec\"\n  gem \"chef-bin\", path: \"../chef-bin\"\n  gem \"chef-bin\", \"~> 18.6\" #path: \"../chef-bin\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1928142368",
        "repo_full_name": "chef/chef",
        "pr_number": 14820,
        "pr_file": "knife/Gemfile",
        "discussion_id": "1928142368",
        "commented_code": "@@ -8,7 +8,7 @@ group(:development, :test) do\n   gem \"crack\", \"< 0.4.6\" # due to https://github.com/jnunemaker/crack/pull/75\n   gem \"rake\", \">= 12.3.3\"\n   gem \"rspec\"\n-  gem \"chef-bin\", path: \"../chef-bin\"\n+  gem \"chef-bin\", \"~> 18.6\" #path: \"../chef-bin\"",
        "comment_created_at": "2025-01-24T06:18:23+00:00",
        "comment_author": "neha-p6",
        "comment_body": "move this to gemspec as well.",
        "pr_file_module": null
      },
      {
        "comment_id": "1928166319",
        "repo_full_name": "chef/chef",
        "pr_number": 14820,
        "pr_file": "knife/Gemfile",
        "discussion_id": "1928142368",
        "commented_code": "@@ -8,7 +8,7 @@ group(:development, :test) do\n   gem \"crack\", \"< 0.4.6\" # due to https://github.com/jnunemaker/crack/pull/75\n   gem \"rake\", \">= 12.3.3\"\n   gem \"rspec\"\n-  gem \"chef-bin\", path: \"../chef-bin\"\n+  gem \"chef-bin\", \"~> 18.6\" #path: \"../chef-bin\"",
        "comment_created_at": "2025-01-24T06:50:44+00:00",
        "comment_author": "ashiqueps",
        "comment_body": "Done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1776206090",
    "pr_number": 14605,
    "pr_file": ".expeditor/scripts/infra-hab.spec",
    "created_at": "2024-09-26T02:02:16+00:00",
    "commented_code": "# Disable any shell actions, replace them with simply 'true'\n%define __spec_prep_post true\n%define __spec_prep_pre true\n%define __spec_build_post true\n%define __spec_build_pre true\n%define __spec_install_post true\n%define __spec_install_pre true\n%define __spec_clean_post true\n%define __spec_clean_pre true\n\n# Use SHA256 checksums for all files\n%define _binary_filedigest_algorithm 8\n\n%define _binary_payload w1.xzdio\n\n# Disable creation of build-id links\n%define _build_id_links none\n\n# Metadata\nName: chef\nVersion: %{VERSION}\nRelease: 1%{?dist}\nSummary:  The full stack of chef\nAutoReqProv: no\nBuildRoot: %buildroot\nPrefix: /\nGroup: default\nLicense: Chef EULA\nVendor: Omnibus <omnibus@getchef.com>\nURL: https://www.chef.io\nPackager: Chef Software, Inc. <maintainers@chef.io>\n%description\nThe full stack of chef\n\n%prep\n# noop\n\n%build\n# noop\n\n%install\n# noop\n\n%clean\n# noop\n\n%pre\n#!/bin/sh\n#\n# Perform necessary inspec setup steps\n# before package is installed.\n#\n\necho \"You're about to install Chef Infra Client!\"\n\n%post\n#!/bin/sh\n# WARNING: REQUIRES /bin/sh\n#\n# - must run on /bin/sh on solaris 9\n# - must run on /bin/sh on AIX 6.x\n# - this file is sh not bash so do not introduce bash-isms\n# - if you are under 40, get peer review from your elders.\n#\n# Install Chef Infra Client\n#\n\n# Create wrapper binaries into /hab/chef directory\nmkdir -p /hab/chef/bin",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1776206090",
        "repo_full_name": "chef/chef",
        "pr_number": 14605,
        "pr_file": ".expeditor/scripts/infra-hab.spec",
        "discussion_id": "1776206090",
        "commented_code": "@@ -0,0 +1,243 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+# Metadata\n+Name: chef\n+Version: %{VERSION}\n+Release: 1%{?dist}\n+Summary:  The full stack of chef\n+AutoReqProv: no\n+BuildRoot: %buildroot\n+Prefix: /\n+Group: default\n+License: Chef EULA\n+Vendor: Omnibus <omnibus@getchef.com>\n+URL: https://www.chef.io\n+Packager: Chef Software, Inc. <maintainers@chef.io>\n+%description\n+The full stack of chef\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# noop\n+\n+%clean\n+# noop\n+\n+%pre\n+#!/bin/sh\n+#\n+# Perform necessary inspec setup steps\n+# before package is installed.\n+#\n+\n+echo \"You're about to install Chef Infra Client!\"\n+\n+%post\n+#!/bin/sh\n+# WARNING: REQUIRES /bin/sh\n+#\n+# - must run on /bin/sh on solaris 9\n+# - must run on /bin/sh on AIX 6.x\n+# - this file is sh not bash so do not introduce bash-isms\n+# - if you are under 40, get peer review from your elders.\n+#\n+# Install Chef Infra Client\n+#\n+\n+# Create wrapper binaries into /hab/chef directory\n+mkdir -p /hab/chef/bin",
        "comment_created_at": "2024-09-26T02:02:16+00:00",
        "comment_author": "mwrock",
        "comment_body": "I think we want to put these in `/opt/chef` or wherever they exist today.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1907297240",
    "pr_number": 14772,
    "pr_file": ".expeditor/scripts/chef-infra-client.spec",
    "created_at": "2025-01-08T14:45:22+00:00",
    "commented_code": "# Disable any shell actions, replace them with simply 'true'\n%define __spec_prep_post true\n%define __spec_prep_pre true\n%define __spec_build_post true\n%define __spec_build_pre true\n%define __spec_install_post true\n%define __spec_install_pre true\n%define __spec_clean_post true\n%define __spec_clean_pre true\n\n# Use SHA256 checksums for all files\n%define _binary_filedigest_algorithm 8\n\n%define _binary_payload w1.xzdio\n\n# Disable creation of build-id links\n%define _build_id_links none\n\nName:           chef-infra-client\nVersion:        %{VERSION}\nRelease:        1%{?dist}\nSummary:        The full stack of Chef Infra Client\nAutoReqProv: \tno\nBuildRoot: \t    %buildroot\nPrefix: \t    /\nGroup: \t\t    default\nLicense:        Chef EULA\nURL: \t\t    https://www.chef.io\nPackager: \t    Chef Software, Inc. <maintainers@chef.io>\nSource0:        %{CHEF_INFRA_TAR}\nSource1:        %{CHEF_MIGRATE_TAR}\n\n%description\nThe full stack of Chef Infra Client\n\n%prep\n# noop\n\n%build\n# noop\n\n%install\n# Create the installation directory for the migration tools\n#mkdir -p %{buildroot}/opt/chef\nmkdir -p %{buildroot}/opt/chef/{bin,bundle}\n\n# Untar the migration tools into /opt/chef/bin\ntar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n\n# Copy the chef infra tarball into /opt/chef/bundle\ncp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n\n%files\n/opt/chef\n/opt/chef/bin",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1907297240",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907297240",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin",
        "comment_created_at": "2025-01-08T14:45:22+00:00",
        "comment_author": "marcparadise",
        "comment_body": "Because /opt/chef/bin is already owned by the chef-infra package, we probably don't want to install anything here. \r\nCould we instead use a different directory, something like '/opt/chef/migration' or even include it in '/opt/chef/bundle\"? ",
        "pr_file_module": null
      },
      {
        "comment_id": "1907382449",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907297240",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin",
        "comment_created_at": "2025-01-08T15:34:21+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "Would it be a good idea to unpack the migration tool into /opt/chef/migration/bin instead?",
        "pr_file_module": null
      },
      {
        "comment_id": "1907395853",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907297240",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin",
        "comment_created_at": "2025-01-08T15:42:48+00:00",
        "comment_author": "Stromweld",
        "comment_body": "since new install lives in /hab why aren't we using that directory and in the end there shouldn't be any /opt/chef anything unless using omnibus version. That'll make it easier for customers to understand anything related to hab builds lives in /hab/somewhere and omnibus in /opt/chef instead of 1 tool over here and all others over there. This also then makes Cookbook checks easy to accommodate both by simply checking for the existence of /opt/chef.",
        "pr_file_module": null
      },
      {
        "comment_id": "1908191760",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907297240",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin",
        "comment_created_at": "2025-01-09T05:34:40+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "@marcparadise @Stromweld It appears that using /opt/chef or /hab may have similar drawbacks, as it could interfere with their structures. Could we use a separate directory, /opt/chef-migrate, instead, where bin would hold the binary of the migration tool and bundle would hold the tar file?",
        "pr_file_module": null
      },
      {
        "comment_id": "1917826273",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907297240",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin",
        "comment_created_at": "2025-01-16T06:41:20+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "Changed the directory to place the migration binary and bundle into `/hab/migration`. The binary is now located in `/hab/migration/bin`, and the infra tarball is stored in `/hab/migration/bundle`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1907298683",
    "pr_number": 14772,
    "pr_file": ".expeditor/scripts/chef-infra-client.spec",
    "created_at": "2025-01-08T14:46:21+00:00",
    "commented_code": "# Disable any shell actions, replace them with simply 'true'\n%define __spec_prep_post true\n%define __spec_prep_pre true\n%define __spec_build_post true\n%define __spec_build_pre true\n%define __spec_install_post true\n%define __spec_install_pre true\n%define __spec_clean_post true\n%define __spec_clean_pre true\n\n# Use SHA256 checksums for all files\n%define _binary_filedigest_algorithm 8\n\n%define _binary_payload w1.xzdio\n\n# Disable creation of build-id links\n%define _build_id_links none\n\nName:           chef-infra-client\nVersion:        %{VERSION}\nRelease:        1%{?dist}\nSummary:        The full stack of Chef Infra Client\nAutoReqProv: \tno\nBuildRoot: \t    %buildroot\nPrefix: \t    /\nGroup: \t\t    default\nLicense:        Chef EULA\nURL: \t\t    https://www.chef.io\nPackager: \t    Chef Software, Inc. <maintainers@chef.io>\nSource0:        %{CHEF_INFRA_TAR}\nSource1:        %{CHEF_MIGRATE_TAR}\n\n%description\nThe full stack of Chef Infra Client\n\n%prep\n# noop\n\n%build\n# noop\n\n%install\n# Create the installation directory for the migration tools\n#mkdir -p %{buildroot}/opt/chef\nmkdir -p %{buildroot}/opt/chef/{bin,bundle}\n\n# Untar the migration tools into /opt/chef/bin\ntar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n\n# Copy the chef infra tarball into /opt/chef/bundle\ncp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n\n%files\n/opt/chef\n/opt/chef/bin\n/opt/chef/bin/*\n/opt/chef/bundle\n/opt/chef/bundle/*\n\n%post\n\n# Determine if --fresh_install needs to be passed based on the existence of the /opt/chef directory\nMIGRATE_CMD=\"/opt/chef/bin/chef-migrate apply airgap\"\nif [ ! -f /opt/chef/bin/chef-client ]; then",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1907298683",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907298683",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin\n+/opt/chef/bin/*\n+/opt/chef/bundle\n+/opt/chef/bundle/*\n+\n+%post\n+\n+# Determine if --fresh_install needs to be passed based on the existence of the /opt/chef directory\n+MIGRATE_CMD=\"/opt/chef/bin/chef-migrate apply airgap\"\n+if [ ! -f /opt/chef/bin/chef-client ]; then",
        "comment_created_at": "2025-01-08T14:46:21+00:00",
        "comment_author": "marcparadise",
        "comment_body": "/opt/chef/bin/chef-client may not exist, but chef-client could still be installed on the system and available int he path via workstation. In that case, is 'fresh-install' still correct? ",
        "pr_file_module": null
      },
      {
        "comment_id": "1907375809",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907298683",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin\n+/opt/chef/bin/*\n+/opt/chef/bundle\n+/opt/chef/bundle/*\n+\n+%post\n+\n+# Determine if --fresh_install needs to be passed based on the existence of the /opt/chef directory\n+MIGRATE_CMD=\"/opt/chef/bin/chef-migrate apply airgap\"\n+if [ ! -f /opt/chef/bin/chef-client ]; then",
        "comment_created_at": "2025-01-08T15:29:59+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "The migration tool has an option to uninstall the Omnibus installation during migration. However, I am not sure whether it accounts for the Workstation. Therefore, I am specifically checking the Omnibus installation here",
        "pr_file_module": null
      },
      {
        "comment_id": "1917069354",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907298683",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin\n+/opt/chef/bin/*\n+/opt/chef/bundle\n+/opt/chef/bundle/*\n+\n+%post\n+\n+# Determine if --fresh_install needs to be passed based on the existence of the /opt/chef directory\n+MIGRATE_CMD=\"/opt/chef/bin/chef-migrate apply airgap\"\n+if [ ! -f /opt/chef/bin/chef-client ]; then",
        "comment_created_at": "2025-01-15T17:25:10+00:00",
        "comment_author": "marcparadise",
        "comment_body": "Let's instead look at declaring a package-level conflict, so that we can't install infra-19 when chef-workstation 'legacy' is installed.  \r\nThat will let us avoid the entire class of problems that arise trying to manually manage conflicting files across packages. \r\n\r\nThis can be better supported once workstation itself is released with habitat. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1917787320",
        "repo_full_name": "chef/chef",
        "pr_number": 14772,
        "pr_file": ".expeditor/scripts/chef-infra-client.spec",
        "discussion_id": "1907298683",
        "commented_code": "@@ -0,0 +1,89 @@\n+# Disable any shell actions, replace them with simply 'true'\n+%define __spec_prep_post true\n+%define __spec_prep_pre true\n+%define __spec_build_post true\n+%define __spec_build_pre true\n+%define __spec_install_post true\n+%define __spec_install_pre true\n+%define __spec_clean_post true\n+%define __spec_clean_pre true\n+\n+# Use SHA256 checksums for all files\n+%define _binary_filedigest_algorithm 8\n+\n+%define _binary_payload w1.xzdio\n+\n+# Disable creation of build-id links\n+%define _build_id_links none\n+\n+Name:           chef-infra-client\n+Version:        %{VERSION}\n+Release:        1%{?dist}\n+Summary:        The full stack of Chef Infra Client\n+AutoReqProv: \tno\n+BuildRoot: \t    %buildroot\n+Prefix: \t    /\n+Group: \t\t    default\n+License:        Chef EULA\n+URL: \t\t    https://www.chef.io\n+Packager: \t    Chef Software, Inc. <maintainers@chef.io>\n+Source0:        %{CHEF_INFRA_TAR}\n+Source1:        %{CHEF_MIGRATE_TAR}\n+\n+%description\n+The full stack of Chef Infra Client\n+\n+%prep\n+# noop\n+\n+%build\n+# noop\n+\n+%install\n+# Create the installation directory for the migration tools\n+#mkdir -p %{buildroot}/opt/chef\n+mkdir -p %{buildroot}/opt/chef/{bin,bundle}\n+\n+# Untar the migration tools into /opt/chef/bin\n+tar -xf %{SOURCE1} -C %{buildroot}/opt/chef/bin\n+\n+# Copy the chef infra tarball into /opt/chef/bundle\n+cp %{SOURCE0} %{buildroot}/opt/chef/bundle/\n+\n+%files\n+/opt/chef\n+/opt/chef/bin\n+/opt/chef/bin/*\n+/opt/chef/bundle\n+/opt/chef/bundle/*\n+\n+%post\n+\n+# Determine if --fresh_install needs to be passed based on the existence of the /opt/chef directory\n+MIGRATE_CMD=\"/opt/chef/bin/chef-migrate apply airgap\"\n+if [ ! -f /opt/chef/bin/chef-client ]; then",
        "comment_created_at": "2025-01-16T05:52:15+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "Prevents to proceed if chef-workstation is installed: https://github.com/chef/chef/pull/14772/commits/10c403f58b4e4d08c26484cb5b461cae0b7e2983",
        "pr_file_module": null
      }
    ]
  }
]
