---
title: Avoid logic duplication
description: Create reusable scripts or functions for common CI operations instead
  of duplicating the same logic across multiple CI files. Duplicated logic leads to
  maintenance challenges and inconsistency when one copy is updated but others aren't.
repository: pytorch/pytorch
label: CI/CD
language: Shell
comments_count: 3
repository_stars: 91169
---

Create reusable scripts or functions for common CI operations instead of duplicating the same logic across multiple CI files. Duplicated logic leads to maintenance challenges and inconsistency when one copy is updated but others aren't.

For example, instead of copying installation steps:
```bash
# Don't do this in multiple places:
export CMAKE_ARGS="-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON"

# Instead, create a shared script that can be called from multiple places:
# shared_script.sh
setup_executorch_build() {
  export CMAKE_ARGS="-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON"
}
```

This approach is particularly important for installation routines, environment setup, and build configurations across Docker containers. When logic changes are needed, you only need to update in one place. Additionally, clearly document any intentional deviations or environment-specific adjustments to help reviewers understand why certain scripts may differ from the standard pattern.


[
  {
    "discussion_id": "2119470927",
    "pr_number": 154198,
    "pr_file": ".ci/docker/common/install_conda.sh",
    "created_at": "2025-06-01T19:15:56+00:00",
    "commented_code": "# Install some other packages, including those needed for Python test reporting\n  pip_install -r /opt/conda/requirements-ci.txt\n\n  # Install PyTorch mkl deps, as per https://github.com/pytorch/pytorch README\n  if [[ $(uname -m) != \"aarch64\" ]]; then\n    pip_install mkl-static==2024.2.0 mkl-include==2024.2.0",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2119470927",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154198,
        "pr_file": ".ci/docker/common/install_conda.sh",
        "discussion_id": "2119470927",
        "commented_code": "@@ -85,6 +83,11 @@ if [ -n \"$ANACONDA_PYTHON_VERSION\" ]; then\n   # Install some other packages, including those needed for Python test reporting\n   pip_install -r /opt/conda/requirements-ci.txt\n \n+  # Install PyTorch mkl deps, as per https://github.com/pytorch/pytorch README\n+  if [[ $(uname -m) != \"aarch64\" ]]; then\n+    pip_install mkl-static==2024.2.0 mkl-include==2024.2.0",
        "comment_created_at": "2025-06-01T19:15:56+00:00",
        "comment_author": "Skylion007",
        "comment_body": "This logic is duplicated here right?: https://github.com/pytorch/pytorch/blob/c2e91157575a6064e19f2701e85af4035d33a23a/.ci/docker/common/install_mkl.sh#L5\r\n\r\nAlso, does mkl-static reallly distribute static libs? Won't that cause toolchain issues, especially if we want to enable Link Time Optimization on PyTorch at some point?",
        "pr_file_module": null
      },
      {
        "comment_id": "2120298162",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154198,
        "pr_file": ".ci/docker/common/install_conda.sh",
        "discussion_id": "2119470927",
        "commented_code": "@@ -85,6 +83,11 @@ if [ -n \"$ANACONDA_PYTHON_VERSION\" ]; then\n   # Install some other packages, including those needed for Python test reporting\n   pip_install -r /opt/conda/requirements-ci.txt\n \n+  # Install PyTorch mkl deps, as per https://github.com/pytorch/pytorch README\n+  if [[ $(uname -m) != \"aarch64\" ]]; then\n+    pip_install mkl-static==2024.2.0 mkl-include==2024.2.0",
        "comment_created_at": "2025-06-02T07:30:48+00:00",
        "comment_author": "CaoE",
        "comment_body": "Thanks for your comments. I don't know the relationship between `pytorch/.ci/docker/common/install_mkl.sh` and the MKL version of the CI environment. Does `pytorch/.ci/docker/common/install_mkl.sh` selects the MKL version for the pytorch releases ? I'm not sure whether such changes will cause the issues you mentioned. I tried to update MKL according to https://github.com/pytorch/pytorch README. Could you please give me some advice to upgrade MKL in CI? Thanks.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176199626",
    "pr_number": 157298,
    "pr_file": ".ci/docker/common/install_executorch.sh",
    "created_at": "2025-07-01T00:56:46+00:00",
    "commented_code": "pushd executorch\n\n  export PYTHON_EXECUTABLE=python\n  export CMAKE_ARGS=\"-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON\"\n  export CMAKE_ARGS=\"-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON -DEXECUTORCH_BUILD_TESTS=ON\"",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2176199626",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157298,
        "pr_file": ".ci/docker/common/install_executorch.sh",
        "discussion_id": "2176199626",
        "commented_code": "@@ -50,7 +50,7 @@ setup_executorch() {\n   pushd executorch\n \n   export PYTHON_EXECUTABLE=python\n-  export CMAKE_ARGS=\"-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON\"\n+  export CMAKE_ARGS=\"-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON -DEXECUTORCH_BUILD_TESTS=ON\"",
        "comment_created_at": "2025-07-01T00:56:46+00:00",
        "comment_author": "huydhn",
        "comment_body": "A follow-up AI here I think is to create a short script on ExecuTorch CI to do this step https://github.com/pytorch/executorch/blob/main/.ci/scripts/unittest-linux.sh#L20-L26 so that we could just call it here instead of copying the logic over, which could get out of sync when ET is updated",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2109566628",
    "pr_number": 148419,
    "pr_file": ".ci/docker/common/install_cache.sh",
    "created_at": "2025-05-27T15:49:12+00:00",
    "commented_code": "set -ex\n\ninstall_ubuntu() {\n  echo \"Preparing to build sccache from source\"\nSCCACHE_VERSION=\"0.9.1\"\n\nCARGO_FLAGS=\"\"\n\ninstall_prereqs_ubuntu() {\n  apt-get update\n  # libssl-dev will not work as it is upgraded to libssl3 in Ubuntu-22.04.\n  # Instead use lib and headers from OpenSSL1.1 installed in `install_openssl.sh``\n  apt-get install -y cargo\n  echo \"Checking out sccache repo\"\n  git clone https://github.com/mozilla/sccache -b v0.9.1\n  cd sccache\n  echo \"Building sccache\"\n  cargo build --release\n  cp target/release/sccache /opt/cache/bin\n  echo \"Cleaning up\"\n  cd ..\n  rm -rf sccache\n  apt-get remove -y cargo rustc\n  apt-get autoclean && apt-get clean\n\n  # cleanup after ourselves\n  trap 'cleanup_ubuntu' EXIT",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2109566628",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 148419,
        "pr_file": ".ci/docker/common/install_cache.sh",
        "discussion_id": "2109566628",
        "commented_code": "@@ -2,29 +2,45 @@\n \n set -ex\n \n-install_ubuntu() {\n-  echo \"Preparing to build sccache from source\"\n+SCCACHE_VERSION=\"0.9.1\"\n+\n+CARGO_FLAGS=\"\"\n+\n+install_prereqs_ubuntu() {\n   apt-get update\n   # libssl-dev will not work as it is upgraded to libssl3 in Ubuntu-22.04.\n   # Instead use lib and headers from OpenSSL1.1 installed in `install_openssl.sh``\n   apt-get install -y cargo\n-  echo \"Checking out sccache repo\"\n-  git clone https://github.com/mozilla/sccache -b v0.9.1\n-  cd sccache\n-  echo \"Building sccache\"\n-  cargo build --release\n-  cp target/release/sccache /opt/cache/bin\n-  echo \"Cleaning up\"\n-  cd ..\n-  rm -rf sccache\n-  apt-get remove -y cargo rustc\n-  apt-get autoclean && apt-get clean\n+\n+  # cleanup after ourselves\n+  trap 'cleanup_ubuntu' EXIT",
        "comment_created_at": "2025-05-27T15:49:12+00:00",
        "comment_author": "ZainRizvi",
        "comment_body": "Don't you want to do a similar cleanup for almalinux?",
        "pr_file_module": null
      },
      {
        "comment_id": "2110614106",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 148419,
        "pr_file": ".ci/docker/common/install_cache.sh",
        "discussion_id": "2109566628",
        "commented_code": "@@ -2,29 +2,45 @@\n \n set -ex\n \n-install_ubuntu() {\n-  echo \"Preparing to build sccache from source\"\n+SCCACHE_VERSION=\"0.9.1\"\n+\n+CARGO_FLAGS=\"\"\n+\n+install_prereqs_ubuntu() {\n   apt-get update\n   # libssl-dev will not work as it is upgraded to libssl3 in Ubuntu-22.04.\n   # Instead use lib and headers from OpenSSL1.1 installed in `install_openssl.sh``\n   apt-get install -y cargo\n-  echo \"Checking out sccache repo\"\n-  git clone https://github.com/mozilla/sccache -b v0.9.1\n-  cd sccache\n-  echo \"Building sccache\"\n-  cargo build --release\n-  cp target/release/sccache /opt/cache/bin\n-  echo \"Cleaning up\"\n-  cd ..\n-  rm -rf sccache\n-  apt-get remove -y cargo rustc\n-  apt-get autoclean && apt-get clean\n+\n+  # cleanup after ourselves\n+  trap 'cleanup_ubuntu' EXIT",
        "comment_created_at": "2025-05-28T00:43:52+00:00",
        "comment_author": "seemethere",
        "comment_body": "No because we do the build in a multi-stage build meaning it'll automatically get cleaned up!",
        "pr_file_module": null
      },
      {
        "comment_id": "2116890998",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 148419,
        "pr_file": ".ci/docker/common/install_cache.sh",
        "discussion_id": "2109566628",
        "commented_code": "@@ -2,29 +2,45 @@\n \n set -ex\n \n-install_ubuntu() {\n-  echo \"Preparing to build sccache from source\"\n+SCCACHE_VERSION=\"0.9.1\"\n+\n+CARGO_FLAGS=\"\"\n+\n+install_prereqs_ubuntu() {\n   apt-get update\n   # libssl-dev will not work as it is upgraded to libssl3 in Ubuntu-22.04.\n   # Instead use lib and headers from OpenSSL1.1 installed in `install_openssl.sh``\n   apt-get install -y cargo\n-  echo \"Checking out sccache repo\"\n-  git clone https://github.com/mozilla/sccache -b v0.9.1\n-  cd sccache\n-  echo \"Building sccache\"\n-  cargo build --release\n-  cp target/release/sccache /opt/cache/bin\n-  echo \"Cleaning up\"\n-  cd ..\n-  rm -rf sccache\n-  apt-get remove -y cargo rustc\n-  apt-get autoclean && apt-get clean\n+\n+  # cleanup after ourselves\n+  trap 'cleanup_ubuntu' EXIT",
        "comment_created_at": "2025-05-31T00:16:04+00:00",
        "comment_author": "ZainRizvi",
        "comment_body": "Why does one use a multi-stage build but the other doesn't? Is that tech debt or does it need to be done that way?",
        "pr_file_module": null
      }
    ]
  }
]
