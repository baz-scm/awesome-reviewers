---
title: Parameterize configuration scripts
description: Configuration scripts should use variables for values that might change
  or are used in multiple places, such as paths, versions, and environment-specific
  settings. This improves maintainability, makes updates easier, and facilitates cross-platform
  support.
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 14036
---

Configuration scripts should use variables for values that might change or are used in multiple places, such as paths, versions, and environment-specific settings. This improves maintainability, makes updates easier, and facilitates cross-platform support.

When writing configuration or installation scripts:
1. Extract repeated values into variables defined at the top of the script
2. Use these variables throughout the script with appropriate syntax (${VARIABLE})
3. Consolidate related commands where possible (e.g., combine multiple package installations)
4. Use appropriate command-line options for intended usage (e.g., `-y` for non-interactive execution)

Example:
```bash
# Bad approach - hardcoded values, separate commands
sudo wget http://example.org/dist/maven/3.6.0/apache-maven-3.6.0-bin.tar.gz
sudo tar -xf apache-maven-3.6.0-bin.tar.gz
sudo rm -f apache-maven-3.6.0-bin.tar.gz
sudo mv apache-maven-3.6.0/ apache-maven/
sudo apt-get install python-pip
sudo apt-get install python-wheel
sudo apt-get install python-dev

# Good approach - parameterized and consolidated
MAVEN_VERSION=3.6.0
cd /usr/local/src
sudo wget http://example.org/dist/maven/${MAVEN_VERSION}/apache-maven-${MAVEN_VERSION}-bin.tar.gz
sudo tar -xf apache-maven-${MAVEN_VERSION}-bin.tar.gz
sudo rm -f apache-maven-${MAVEN_VERSION}-bin.tar.gz
sudo mv apache-maven-${MAVEN_VERSION}/ apache-maven/
sudo apt-get install -y python-pip python-wheel python-dev python-setuptools
```