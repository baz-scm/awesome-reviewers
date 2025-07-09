---
title: Validate environment configurations
description: Ensure that all environment-specific configurations work properly across
  all target environments, particularly when managing multiple architectures or CI
  systems. Test changes thoroughly in the actual environments where code will run.
  Document the purpose of specialized configurations and don't remove configuration
  blocks without verifying they're no longer...
repository: vitessio/vitess
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 19815
---

Ensure that all environment-specific configurations work properly across all target environments, particularly when managing multiple architectures or CI systems. Test changes thoroughly in the actual environments where code will run. Document the purpose of specialized configurations and don't remove configuration blocks without verifying they're no longer needed, even if they appear obsolete.

For example, when handling MySQL installations across different architectures, build packages against the appropriate dependencies for each target architecture. In CI workflows, preserve necessary system configurations like AppArmor settings that might be required for specific environments:

```yaml
# Example: Preserving necessary environment-specific configurations
sudo service mysql stop
sudo service etcd stop
sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
```