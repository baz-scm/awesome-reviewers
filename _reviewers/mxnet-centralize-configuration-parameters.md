---
title: Centralize configuration parameters
description: 'Avoid hardcoded paths and duplicated configuration values throughout
  the code. Instead:


  1. Use dedicated configuration files for settings that appear in multiple places'
repository: apache/mxnet
label: Configurations
language: Shell
comments_count: 3
repository_stars: 20801
---

Avoid hardcoded paths and duplicated configuration values throughout the code. Instead:

1. Use dedicated configuration files for settings that appear in multiple places
2. Leverage environment variables for runtime path configurations
3. Implement runtime detection for system-specific paths when possible
4. When environment setup scripts are available (like `source /opt/intel/oneapi/setvars.sh`), prefer them over hardcoding paths

Example of problematic code:
```bash
# Hardcoded path that may not work across installations
export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH
# Duplicated test configuration
pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --verbose tests/python/unittest
```

Better approach:
```bash
# Use environment detection or user configuration
if [[ -d "${ARM_PATH}" ]]; then
    export CPATH=${ARM_PATH}/include_lp64_mp:$CPATH
fi

# Load configuration from a central file
source ./test_config.sh
pytest ${TEST_COMMON_ARGS} ${UNITTEST_ARGS} tests/python/unittest
```

This approach improves portability across different environments and makes maintenance easier when configurations need to change.


[
  {
    "discussion_id": "725211061",
    "pr_number": 20474,
    "pr_file": "tools/staticbuild/build_lib.sh",
    "created_at": "2021-10-08T18:09:55+00:00",
    "commented_code": "-DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \\\n      ..\nninja\nif [[ ! $PLATFORM == 'darwin' ]] && [[ $BLAS == 'mkl' ]]; then\n    patchelf --set-rpath \"/opt/intel/oneapi/mkl/${INTEL_MKL}/lib/intel64/:\\$ORIGIN\" --force-rpath libmxnet.so",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "725211061",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20474,
        "pr_file": "tools/staticbuild/build_lib.sh",
        "discussion_id": "725211061",
        "commented_code": "@@ -36,13 +40,18 @@ cmake -GNinja -C $cmake_config \\\n       -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \\\n       ..\n ninja\n+if [[ ! $PLATFORM == 'darwin' ]] && [[ $BLAS == 'mkl' ]]; then\n+    patchelf --set-rpath \"/opt/intel/oneapi/mkl/${INTEL_MKL}/lib/intel64/:\\$ORIGIN\" --force-rpath libmxnet.so",
        "comment_created_at": "2021-10-08T18:09:55+00:00",
        "comment_author": "leezu",
        "comment_body": "Will oneapi/mkl always be in `/opt/intel`? Is there a reason for not asking users to fix their run-time search path environment variables instead (which ideally would automatically be set correctly upon installation of oneapi/mkl)?",
        "pr_file_module": null
      },
      {
        "comment_id": "725240417",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20474,
        "pr_file": "tools/staticbuild/build_lib.sh",
        "discussion_id": "725211061",
        "commented_code": "@@ -36,13 +40,18 @@ cmake -GNinja -C $cmake_config \\\n       -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \\\n       ..\n ninja\n+if [[ ! $PLATFORM == 'darwin' ]] && [[ $BLAS == 'mkl' ]]; then\n+    patchelf --set-rpath \"/opt/intel/oneapi/mkl/${INTEL_MKL}/lib/intel64/:\\$ORIGIN\" --force-rpath libmxnet.so",
        "comment_created_at": "2021-10-08T19:02:59+00:00",
        "comment_author": "akarbown",
        "comment_body": "_> Will oneapi/mkl always be in /opt/intel?_ \r\nI think that if the user do not define explicitly other location, the default location for oneMKL supposed to be /opt/intel/oneapi/ at least the way it was installed in the way as it is in the mkl.sh file. \r\n_> Is there a reason for not asking users to fix their run-time search path environment variables instead (which ideally would automatically be set correctly upon installation of oneapi/mkl)?_\r\nI've added it for the sake of the tests so that while running them (in the runtime) libmxnet.dylib could see the MKL libraries. It's not the best solution. Now, I think that maybe it would be better to ``source /opt/intel/oneapi/setvars.sh`` script just before the test execution (in the *.yml file). What do you think? Or did you have something else in mind?",
        "pr_file_module": null
      },
      {
        "comment_id": "725695236",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20474,
        "pr_file": "tools/staticbuild/build_lib.sh",
        "discussion_id": "725211061",
        "commented_code": "@@ -36,13 +40,18 @@ cmake -GNinja -C $cmake_config \\\n       -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \\\n       ..\n ninja\n+if [[ ! $PLATFORM == 'darwin' ]] && [[ $BLAS == 'mkl' ]]; then\n+    patchelf --set-rpath \"/opt/intel/oneapi/mkl/${INTEL_MKL}/lib/intel64/:\\$ORIGIN\" --force-rpath libmxnet.so",
        "comment_created_at": "2021-10-10T20:41:27+00:00",
        "comment_author": "leezu",
        "comment_body": "I assume `source /opt/intel/oneapi/setvars.sh` is also what users would be expected to do if they install MKL on Mac? If so, I think that'll be more robust than hardcoding the rpath ",
        "pr_file_module": null
      },
      {
        "comment_id": "725708632",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20474,
        "pr_file": "tools/staticbuild/build_lib.sh",
        "discussion_id": "725211061",
        "commented_code": "@@ -36,13 +40,18 @@ cmake -GNinja -C $cmake_config \\\n       -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \\\n       ..\n ninja\n+if [[ ! $PLATFORM == 'darwin' ]] && [[ $BLAS == 'mkl' ]]; then\n+    patchelf --set-rpath \"/opt/intel/oneapi/mkl/${INTEL_MKL}/lib/intel64/:\\$ORIGIN\" --force-rpath libmxnet.so",
        "comment_created_at": "2021-10-10T22:29:39+00:00",
        "comment_author": "akarbown",
        "comment_body": "Yes, sure. However, I've just realized that when linking with MKL static libraries there is no need to ``source /opt/intel/oneapi/setvars.sh``. It's mandatory in case of linking with MKL dynamic libraries. Thanks for pointing that out!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "610025602",
    "pr_number": 20138,
    "pr_file": "ci/docker/runtime_functions.sh",
    "created_at": "2021-04-08T19:21:08+00:00",
    "commented_code": "export MXNET_SUBGRAPH_VERBOSE=0\n    export MXNET_ENABLE_CYTHON=0\n    export DMLC_LOG_STACK_TRACE_DEPTH=100\n    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n    MXNET_ENGINE_TYPE=NaiveEngine \\\n                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n    pytest -m 'serial' --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n    pytest --durations=50 --cov-report xml:tests_mkl.xml --verbose tests/python/mkl\n                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n    pytest -m 'serial' --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n    pytest --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_mkl.xml --verbose tests/python/mkl",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "610025602",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20138,
        "pr_file": "ci/docker/runtime_functions.sh",
        "discussion_id": "610025602",
        "commented_code": "@@ -783,11 +783,11 @@ unittest_ubuntu_python3_cpu_onednn() {\n     export MXNET_SUBGRAPH_VERBOSE=0\n     export MXNET_ENABLE_CYTHON=0\n     export DMLC_LOG_STACK_TRACE_DEPTH=100\n-    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n+    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n     MXNET_ENGINE_TYPE=NaiveEngine \\\n-                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n-    pytest -m 'serial' --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n-    pytest --durations=50 --cov-report xml:tests_mkl.xml --verbose tests/python/mkl\n+                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n+    pytest -m 'serial' --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n+    pytest --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_mkl.xml --verbose tests/python/mkl",
        "comment_created_at": "2021-04-08T19:21:08+00:00",
        "comment_author": "marcoabreu",
        "comment_body": "Can't we have this in some configuration file instead of inlining it everywhere?",
        "pr_file_module": null
      },
      {
        "comment_id": "610034846",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20138,
        "pr_file": "ci/docker/runtime_functions.sh",
        "discussion_id": "610025602",
        "commented_code": "@@ -783,11 +783,11 @@ unittest_ubuntu_python3_cpu_onednn() {\n     export MXNET_SUBGRAPH_VERBOSE=0\n     export MXNET_ENABLE_CYTHON=0\n     export DMLC_LOG_STACK_TRACE_DEPTH=100\n-    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n+    OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --verbose tests/python/unittest\n     MXNET_ENGINE_TYPE=NaiveEngine \\\n-                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n-    pytest -m 'serial' --durations=50 --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n-    pytest --durations=50 --cov-report xml:tests_mkl.xml --verbose tests/python/mkl\n+                     OMP_NUM_THREADS=$(expr $(nproc) / 4) pytest -m 'not serial' -k 'test_operator' -n 4 --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n+    pytest -m 'serial' --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_unittest.xml --cov-append --verbose tests/python/unittest\n+    pytest --durations=50 --cov=./contrib --cov=./python/mxnet --cov-report xml:tests_mkl.xml --verbose tests/python/mkl",
        "comment_created_at": "2021-04-08T19:32:54+00:00",
        "comment_author": "barry-jin",
        "comment_body": "Thanks for the suggestion. I will update it. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "651362257",
    "pr_number": 20342,
    "pr_file": "tools/staticbuild/build.sh",
    "created_at": "2021-06-15T00:26:44+00:00",
    "commented_code": "export PKG_CONFIG_PATH=$DEPS_PATH/lib/pkgconfig:$DEPS_PATH/lib64/pkgconfig:$DEPS_PATH/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH\nfi\nexport FC=\"gfortran\"\nexport CPATH=$DEPS_PATH/include:$CPATH\nif [[ $ARCH == 'aarch64' ]]; then\n    export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "651362257",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20342,
        "pr_file": "tools/staticbuild/build.sh",
        "discussion_id": "651362257",
        "commented_code": "@@ -59,7 +59,11 @@ else\n     export PKG_CONFIG_PATH=$DEPS_PATH/lib/pkgconfig:$DEPS_PATH/lib64/pkgconfig:$DEPS_PATH/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH\n fi\n export FC=\"gfortran\"\n-export CPATH=$DEPS_PATH/include:$CPATH\n+if [[ $ARCH == 'aarch64' ]]; then\n+    export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH",
        "comment_created_at": "2021-06-15T00:26:44+00:00",
        "comment_author": "Zha0q1",
        "comment_body": "If the user installed a different armpl package then this will not work, is there a way to automatically detect the armpl path?",
        "pr_file_module": null
      },
      {
        "comment_id": "651363271",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20342,
        "pr_file": "tools/staticbuild/build.sh",
        "discussion_id": "651362257",
        "commented_code": "@@ -59,7 +59,11 @@ else\n     export PKG_CONFIG_PATH=$DEPS_PATH/lib/pkgconfig:$DEPS_PATH/lib64/pkgconfig:$DEPS_PATH/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH\n fi\n export FC=\"gfortran\"\n-export CPATH=$DEPS_PATH/include:$CPATH\n+if [[ $ARCH == 'aarch64' ]]; then\n+    export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH",
        "comment_created_at": "2021-06-15T00:29:53+00:00",
        "comment_author": "mseth10",
        "comment_body": "does it work with other armpl versions? didn't we see an error when we were using gcc-10 armpl?",
        "pr_file_module": null
      },
      {
        "comment_id": "651370471",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20342,
        "pr_file": "tools/staticbuild/build.sh",
        "discussion_id": "651362257",
        "commented_code": "@@ -59,7 +59,11 @@ else\n     export PKG_CONFIG_PATH=$DEPS_PATH/lib/pkgconfig:$DEPS_PATH/lib64/pkgconfig:$DEPS_PATH/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH\n fi\n export FC=\"gfortran\"\n-export CPATH=$DEPS_PATH/include:$CPATH\n+if [[ $ARCH == 'aarch64' ]]; then\n+    export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH",
        "comment_created_at": "2021-06-15T00:53:03+00:00",
        "comment_author": "mseth10",
        "comment_body": "we can ask users to specifically install `armpl_21.0_gcc-8.2` before installing mxnet wheel",
        "pr_file_module": null
      }
    ]
  }
]
