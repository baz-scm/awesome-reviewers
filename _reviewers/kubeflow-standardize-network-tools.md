---
title: Standardize network tools
description: When performing network operations in build scripts or containers, prefer
  `curl` over `wget` for HTTP requests to standardize dependencies and improve portability.
  Use the specific flags `-fsSL` for silent operation with proper error handling,
  and explicitly specify output destinations.
repository: kubeflow/kubeflow
label: Networking
language: Dockerfile
comments_count: 4
repository_stars: 15064
---

When performing network operations in build scripts or containers, prefer `curl` over `wget` for HTTP requests to standardize dependencies and improve portability. Use the specific flags `-fsSL` for silent operation with proper error handling, and explicitly specify output destinations.

Additionally, ensure network services support both IPv4 and IPv6 addressing by using dual-stack binding configurations rather than binding only to 0.0.0.0 (IPv4).

Example replacing wget with curl:
```bash
# Instead of:
wget -q -O- https://example.com/file.tar.gz | tar xz

# Use:
curl -fsSL https://example.com/file.tar.gz | tar xz
```

Example of dual-stack binding in gunicorn:
```bash
# Instead of:
gunicorn -w 3 --bind 0.0.0.0:5000 app:app

# Use:
gunicorn -w 3 --bind 0.0.0.0:5000 --bind [::]:5000 app:app
```


[
  {
    "discussion_id": "1720474884",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-16T23:41:52+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n\n# version details\nARG ARTIFACTORY_URL=vault.habana.ai\nARG VERSION=1.16.2\nARG REVISION=2\nARG PYTORCH_VERSION=2.2.2\nARG OS_NUMBER=2204\n\n# runtime variables\nENV DEBIAN_FRONTEND=noninteractive\nENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\nENV HABANA_LOGS=/var/log/habana_logs/\nENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\nENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\nENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\nENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n\n# There is no need to store pip installation files inside docker image\nENV PIP_NO_CACHE_DIR=on\nENV PIP_DISABLE_PIP_VERSION_CHECK=1\n\n# libfabric and scaling variables\nENV LIBFABRIC_VERSION=\"1.20.0\"\nENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\nENV MPI_ROOT=/opt/amazon/openmpi\nENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\nENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\nENV MPICC=${MPI_ROOT}/bin/mpicc\nENV OPAL_PREFIX=${MPI_ROOT}\nENV RDMAV_FORK_SAFE=1\nENV FI_EFA_USE_DEVICE_RDMA=1\nENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\nENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n\n# Gaudi stack doesn't (yet) support 3.11, thus\n# downgrade python from 3.11.x to 3.10.14\nRUN source /opt/conda/etc/profile.d/conda.sh \\\n && conda activate base \\\n && conda install -y -q --no-pin python=3.10.14 \\\n && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n && conda clean -a -f -y\n\nUSER root\n\n# install various support libraries\nRUN apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    apt-utils \\\n    bc \\\n    build-essential \\\n    graphviz \\\n    iproute2 \\\n    libcairo2-dev \\\n    libgl1 \\\n    libglib2.0-dev \\\n    libgnutls30 \\\n    libgoogle-glog0v5 \\\n    libgoogle-perftools-dev \\\n    libhdf5-dev \\\n    libjemalloc2 \\\n    libjpeg-dev \\\n    liblapack-dev \\\n    libmkl-dev \\\n    libnuma-dev \\\n    libopenblas-dev \\\n    libpcre2-dev \\\n    libpq-dev \\\n    libselinux1-dev \\\n    lsof \\\n    moreutils \\\n    numactl \\\n    protobuf-compiler \\\n && apt-get autoremove \\\n && apt-get clean \\\n && rm -rf /var/lib/apt/lists/*\n\n# install elastic fabric adapter\nRUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n\n# install habana packages\nRUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720474884",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720474884",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details\n+ARG ARTIFACTORY_URL=vault.habana.ai\n+ARG VERSION=1.16.2\n+ARG REVISION=2\n+ARG PYTORCH_VERSION=2.2.2\n+ARG OS_NUMBER=2204\n+\n+# runtime variables\n+ENV DEBIAN_FRONTEND=noninteractive\n+ENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\n+ENV HABANA_LOGS=/var/log/habana_logs/\n+ENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\n+ENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\n+ENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\n+ENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n+\n+# There is no need to store pip installation files inside docker image\n+ENV PIP_NO_CACHE_DIR=on\n+ENV PIP_DISABLE_PIP_VERSION_CHECK=1\n+\n+# libfabric and scaling variables\n+ENV LIBFABRIC_VERSION=\"1.20.0\"\n+ENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\n+ENV MPI_ROOT=/opt/amazon/openmpi\n+ENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\n+ENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\n+ENV MPICC=${MPI_ROOT}/bin/mpicc\n+ENV OPAL_PREFIX=${MPI_ROOT}\n+ENV RDMAV_FORK_SAFE=1\n+ENV FI_EFA_USE_DEVICE_RDMA=1\n+ENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\n+ENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n+\n+# Gaudi stack doesn't (yet) support 3.11, thus\n+# downgrade python from 3.11.x to 3.10.14\n+RUN source /opt/conda/etc/profile.d/conda.sh \\\n+ && conda activate base \\\n+ && conda install -y -q --no-pin python=3.10.14 \\\n+ && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n+ && conda clean -a -f -y\n+\n+USER root\n+\n+# install various support libraries\n+RUN apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    apt-utils \\\n+    bc \\\n+    build-essential \\\n+    graphviz \\\n+    iproute2 \\\n+    libcairo2-dev \\\n+    libgl1 \\\n+    libglib2.0-dev \\\n+    libgnutls30 \\\n+    libgoogle-glog0v5 \\\n+    libgoogle-perftools-dev \\\n+    libhdf5-dev \\\n+    libjemalloc2 \\\n+    libjpeg-dev \\\n+    liblapack-dev \\\n+    libmkl-dev \\\n+    libnuma-dev \\\n+    libopenblas-dev \\\n+    libpcre2-dev \\\n+    libpq-dev \\\n+    libselinux1-dev \\\n+    lsof \\\n+    moreutils \\\n+    numactl \\\n+    protobuf-compiler \\\n+ && apt-get autoremove \\\n+ && apt-get clean \\\n+ && rm -rf /var/lib/apt/lists/*\n+\n+# install elastic fabric adapter\n+RUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n+ && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n+ && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n+ && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n+ && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n+\n+# install habana packages\n+RUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\",
        "comment_created_at": "2024-08-16T23:41:52+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "Where possible, please use `curl -fsSL URL -o TARGET` so we don't need to require `wget`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1720474977",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-16T23:42:14+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n\n# version details\nARG ARTIFACTORY_URL=vault.habana.ai\nARG VERSION=1.16.2\nARG REVISION=2\nARG PYTORCH_VERSION=2.2.2\nARG OS_NUMBER=2204\n\n# runtime variables\nENV DEBIAN_FRONTEND=noninteractive\nENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\nENV HABANA_LOGS=/var/log/habana_logs/\nENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\nENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\nENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\nENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n\n# There is no need to store pip installation files inside docker image\nENV PIP_NO_CACHE_DIR=on\nENV PIP_DISABLE_PIP_VERSION_CHECK=1\n\n# libfabric and scaling variables\nENV LIBFABRIC_VERSION=\"1.20.0\"\nENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\nENV MPI_ROOT=/opt/amazon/openmpi\nENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\nENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\nENV MPICC=${MPI_ROOT}/bin/mpicc\nENV OPAL_PREFIX=${MPI_ROOT}\nENV RDMAV_FORK_SAFE=1\nENV FI_EFA_USE_DEVICE_RDMA=1\nENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\nENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n\n# Gaudi stack doesn't (yet) support 3.11, thus\n# downgrade python from 3.11.x to 3.10.14\nRUN source /opt/conda/etc/profile.d/conda.sh \\\n && conda activate base \\\n && conda install -y -q --no-pin python=3.10.14 \\\n && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n && conda clean -a -f -y\n\nUSER root\n\n# install various support libraries\nRUN apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    apt-utils \\\n    bc \\\n    build-essential \\\n    graphviz \\\n    iproute2 \\\n    libcairo2-dev \\\n    libgl1 \\\n    libglib2.0-dev \\\n    libgnutls30 \\\n    libgoogle-glog0v5 \\\n    libgoogle-perftools-dev \\\n    libhdf5-dev \\\n    libjemalloc2 \\\n    libjpeg-dev \\\n    liblapack-dev \\\n    libmkl-dev \\\n    libnuma-dev \\\n    libopenblas-dev \\\n    libpcre2-dev \\\n    libpq-dev \\\n    libselinux1-dev \\\n    lsof \\\n    moreutils \\\n    numactl \\\n    protobuf-compiler \\\n && apt-get autoremove \\\n && apt-get clean \\\n && rm -rf /var/lib/apt/lists/*\n\n# install elastic fabric adapter\nRUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720474977",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720474977",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details\n+ARG ARTIFACTORY_URL=vault.habana.ai\n+ARG VERSION=1.16.2\n+ARG REVISION=2\n+ARG PYTORCH_VERSION=2.2.2\n+ARG OS_NUMBER=2204\n+\n+# runtime variables\n+ENV DEBIAN_FRONTEND=noninteractive\n+ENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\n+ENV HABANA_LOGS=/var/log/habana_logs/\n+ENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\n+ENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\n+ENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\n+ENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n+\n+# There is no need to store pip installation files inside docker image\n+ENV PIP_NO_CACHE_DIR=on\n+ENV PIP_DISABLE_PIP_VERSION_CHECK=1\n+\n+# libfabric and scaling variables\n+ENV LIBFABRIC_VERSION=\"1.20.0\"\n+ENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\n+ENV MPI_ROOT=/opt/amazon/openmpi\n+ENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\n+ENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\n+ENV MPICC=${MPI_ROOT}/bin/mpicc\n+ENV OPAL_PREFIX=${MPI_ROOT}\n+ENV RDMAV_FORK_SAFE=1\n+ENV FI_EFA_USE_DEVICE_RDMA=1\n+ENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\n+ENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n+\n+# Gaudi stack doesn't (yet) support 3.11, thus\n+# downgrade python from 3.11.x to 3.10.14\n+RUN source /opt/conda/etc/profile.d/conda.sh \\\n+ && conda activate base \\\n+ && conda install -y -q --no-pin python=3.10.14 \\\n+ && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n+ && conda clean -a -f -y\n+\n+USER root\n+\n+# install various support libraries\n+RUN apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    apt-utils \\\n+    bc \\\n+    build-essential \\\n+    graphviz \\\n+    iproute2 \\\n+    libcairo2-dev \\\n+    libgl1 \\\n+    libglib2.0-dev \\\n+    libgnutls30 \\\n+    libgoogle-glog0v5 \\\n+    libgoogle-perftools-dev \\\n+    libhdf5-dev \\\n+    libjemalloc2 \\\n+    libjpeg-dev \\\n+    liblapack-dev \\\n+    libmkl-dev \\\n+    libnuma-dev \\\n+    libopenblas-dev \\\n+    libpcre2-dev \\\n+    libpq-dev \\\n+    libselinux1-dev \\\n+    lsof \\\n+    moreutils \\\n+    numactl \\\n+    protobuf-compiler \\\n+ && apt-get autoremove \\\n+ && apt-get clean \\\n+ && rm -rf /var/lib/apt/lists/*\n+\n+# install elastic fabric adapter\n+RUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n+ && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\",
        "comment_created_at": "2024-08-16T23:42:14+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "Where possible, please use `curl -fsSL URL -o TARGET` so we don't need to require `wget`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1720475020",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-16T23:42:24+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n\n# version details\nARG ARTIFACTORY_URL=vault.habana.ai\nARG VERSION=1.16.2\nARG REVISION=2\nARG PYTORCH_VERSION=2.2.2\nARG OS_NUMBER=2204\n\n# runtime variables\nENV DEBIAN_FRONTEND=noninteractive\nENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\nENV HABANA_LOGS=/var/log/habana_logs/\nENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\nENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\nENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\nENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n\n# There is no need to store pip installation files inside docker image\nENV PIP_NO_CACHE_DIR=on\nENV PIP_DISABLE_PIP_VERSION_CHECK=1\n\n# libfabric and scaling variables\nENV LIBFABRIC_VERSION=\"1.20.0\"\nENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\nENV MPI_ROOT=/opt/amazon/openmpi\nENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\nENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\nENV MPICC=${MPI_ROOT}/bin/mpicc\nENV OPAL_PREFIX=${MPI_ROOT}\nENV RDMAV_FORK_SAFE=1\nENV FI_EFA_USE_DEVICE_RDMA=1\nENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\nENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n\n# Gaudi stack doesn't (yet) support 3.11, thus\n# downgrade python from 3.11.x to 3.10.14\nRUN source /opt/conda/etc/profile.d/conda.sh \\\n && conda activate base \\\n && conda install -y -q --no-pin python=3.10.14 \\\n && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n && conda clean -a -f -y\n\nUSER root\n\n# install various support libraries\nRUN apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    apt-utils \\\n    bc \\\n    build-essential \\\n    graphviz \\\n    iproute2 \\\n    libcairo2-dev \\\n    libgl1 \\\n    libglib2.0-dev \\\n    libgnutls30 \\\n    libgoogle-glog0v5 \\\n    libgoogle-perftools-dev \\\n    libhdf5-dev \\\n    libjemalloc2 \\\n    libjpeg-dev \\\n    liblapack-dev \\\n    libmkl-dev \\\n    libnuma-dev \\\n    libopenblas-dev \\\n    libpcre2-dev \\\n    libpq-dev \\\n    libselinux1-dev \\\n    lsof \\\n    moreutils \\\n    numactl \\\n    protobuf-compiler \\\n && apt-get autoremove \\\n && apt-get clean \\\n && rm -rf /var/lib/apt/lists/*\n\n# install elastic fabric adapter\nRUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n\n# install habana packages\nRUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\\n && chown root:root /usr/share/keyrings/habana-artifactory.gpg \\\n && chmod 644 /usr/share/keyrings/habana-artifactory.gpg \\\n && echo \"deb [signed-by=/usr/share/keyrings/habana-artifactory.gpg] https://${ARTIFACTORY_URL}/artifactory/debian jammy main\" | tee -a /etc/apt/sources.list \\\n && apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    habanalabs-rdma-core=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-thunk=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-firmware-tools=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-graph=\"$VERSION\"-\"$REVISION\" \\\n && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/* \\\n && sed --in-place \"/$ARTIFACTORY_URL/d\" /etc/apt/sources.list\n\n# install libfabric\nRUN wget -nv -O /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 https://github.com/ofiwg/libfabric/releases/download/v${LIBFABRIC_VERSION}/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n && cd /tmp/ && tar xf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n && cd /tmp/libfabric-${LIBFABRIC_VERSION} \\\n && ./configure --prefix=$LIBFABRIC_ROOT --enable-psm3-verbs --enable-verbs=yes --with-synapseai=/usr \\\n && make -j && make install && cd / && rm -rf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 /tmp/libfabric-${LIBFABRIC_VERSION}\n\n# install hccl wrapper for ofi\nRUN wget -nv -O /tmp/main.zip https://github.com/HabanaAI/hccl_ofi_wrapper/archive/refs/heads/main.zip \\",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720475020",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720475020",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details\n+ARG ARTIFACTORY_URL=vault.habana.ai\n+ARG VERSION=1.16.2\n+ARG REVISION=2\n+ARG PYTORCH_VERSION=2.2.2\n+ARG OS_NUMBER=2204\n+\n+# runtime variables\n+ENV DEBIAN_FRONTEND=noninteractive\n+ENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\n+ENV HABANA_LOGS=/var/log/habana_logs/\n+ENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\n+ENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\n+ENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\n+ENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n+\n+# There is no need to store pip installation files inside docker image\n+ENV PIP_NO_CACHE_DIR=on\n+ENV PIP_DISABLE_PIP_VERSION_CHECK=1\n+\n+# libfabric and scaling variables\n+ENV LIBFABRIC_VERSION=\"1.20.0\"\n+ENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\n+ENV MPI_ROOT=/opt/amazon/openmpi\n+ENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\n+ENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\n+ENV MPICC=${MPI_ROOT}/bin/mpicc\n+ENV OPAL_PREFIX=${MPI_ROOT}\n+ENV RDMAV_FORK_SAFE=1\n+ENV FI_EFA_USE_DEVICE_RDMA=1\n+ENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\n+ENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n+\n+# Gaudi stack doesn't (yet) support 3.11, thus\n+# downgrade python from 3.11.x to 3.10.14\n+RUN source /opt/conda/etc/profile.d/conda.sh \\\n+ && conda activate base \\\n+ && conda install -y -q --no-pin python=3.10.14 \\\n+ && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n+ && conda clean -a -f -y\n+\n+USER root\n+\n+# install various support libraries\n+RUN apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    apt-utils \\\n+    bc \\\n+    build-essential \\\n+    graphviz \\\n+    iproute2 \\\n+    libcairo2-dev \\\n+    libgl1 \\\n+    libglib2.0-dev \\\n+    libgnutls30 \\\n+    libgoogle-glog0v5 \\\n+    libgoogle-perftools-dev \\\n+    libhdf5-dev \\\n+    libjemalloc2 \\\n+    libjpeg-dev \\\n+    liblapack-dev \\\n+    libmkl-dev \\\n+    libnuma-dev \\\n+    libopenblas-dev \\\n+    libpcre2-dev \\\n+    libpq-dev \\\n+    libselinux1-dev \\\n+    lsof \\\n+    moreutils \\\n+    numactl \\\n+    protobuf-compiler \\\n+ && apt-get autoremove \\\n+ && apt-get clean \\\n+ && rm -rf /var/lib/apt/lists/*\n+\n+# install elastic fabric adapter\n+RUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n+ && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n+ && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n+ && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n+ && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n+\n+# install habana packages\n+RUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chown root:root /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chmod 644 /usr/share/keyrings/habana-artifactory.gpg \\\n+ && echo \"deb [signed-by=/usr/share/keyrings/habana-artifactory.gpg] https://${ARTIFACTORY_URL}/artifactory/debian jammy main\" | tee -a /etc/apt/sources.list \\\n+ && apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    habanalabs-rdma-core=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-thunk=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-firmware-tools=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-graph=\"$VERSION\"-\"$REVISION\" \\\n+ && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/* \\\n+ && sed --in-place \"/$ARTIFACTORY_URL/d\" /etc/apt/sources.list\n+\n+# install libfabric\n+RUN wget -nv -O /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 https://github.com/ofiwg/libfabric/releases/download/v${LIBFABRIC_VERSION}/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/ && tar xf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/libfabric-${LIBFABRIC_VERSION} \\\n+ && ./configure --prefix=$LIBFABRIC_ROOT --enable-psm3-verbs --enable-verbs=yes --with-synapseai=/usr \\\n+ && make -j && make install && cd / && rm -rf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 /tmp/libfabric-${LIBFABRIC_VERSION}\n+\n+# install hccl wrapper for ofi\n+RUN wget -nv -O /tmp/main.zip https://github.com/HabanaAI/hccl_ofi_wrapper/archive/refs/heads/main.zip \\",
        "comment_created_at": "2024-08-16T23:42:24+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "Where possible, please use `curl -fsSL URL -o TARGET` so we don't need to require `wget`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1724998664",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720475020",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details\n+ARG ARTIFACTORY_URL=vault.habana.ai\n+ARG VERSION=1.16.2\n+ARG REVISION=2\n+ARG PYTORCH_VERSION=2.2.2\n+ARG OS_NUMBER=2204\n+\n+# runtime variables\n+ENV DEBIAN_FRONTEND=noninteractive\n+ENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\n+ENV HABANA_LOGS=/var/log/habana_logs/\n+ENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\n+ENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\n+ENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\n+ENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n+\n+# There is no need to store pip installation files inside docker image\n+ENV PIP_NO_CACHE_DIR=on\n+ENV PIP_DISABLE_PIP_VERSION_CHECK=1\n+\n+# libfabric and scaling variables\n+ENV LIBFABRIC_VERSION=\"1.20.0\"\n+ENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\n+ENV MPI_ROOT=/opt/amazon/openmpi\n+ENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\n+ENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\n+ENV MPICC=${MPI_ROOT}/bin/mpicc\n+ENV OPAL_PREFIX=${MPI_ROOT}\n+ENV RDMAV_FORK_SAFE=1\n+ENV FI_EFA_USE_DEVICE_RDMA=1\n+ENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\n+ENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n+\n+# Gaudi stack doesn't (yet) support 3.11, thus\n+# downgrade python from 3.11.x to 3.10.14\n+RUN source /opt/conda/etc/profile.d/conda.sh \\\n+ && conda activate base \\\n+ && conda install -y -q --no-pin python=3.10.14 \\\n+ && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n+ && conda clean -a -f -y\n+\n+USER root\n+\n+# install various support libraries\n+RUN apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    apt-utils \\\n+    bc \\\n+    build-essential \\\n+    graphviz \\\n+    iproute2 \\\n+    libcairo2-dev \\\n+    libgl1 \\\n+    libglib2.0-dev \\\n+    libgnutls30 \\\n+    libgoogle-glog0v5 \\\n+    libgoogle-perftools-dev \\\n+    libhdf5-dev \\\n+    libjemalloc2 \\\n+    libjpeg-dev \\\n+    liblapack-dev \\\n+    libmkl-dev \\\n+    libnuma-dev \\\n+    libopenblas-dev \\\n+    libpcre2-dev \\\n+    libpq-dev \\\n+    libselinux1-dev \\\n+    lsof \\\n+    moreutils \\\n+    numactl \\\n+    protobuf-compiler \\\n+ && apt-get autoremove \\\n+ && apt-get clean \\\n+ && rm -rf /var/lib/apt/lists/*\n+\n+# install elastic fabric adapter\n+RUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n+ && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n+ && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n+ && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n+ && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n+\n+# install habana packages\n+RUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chown root:root /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chmod 644 /usr/share/keyrings/habana-artifactory.gpg \\\n+ && echo \"deb [signed-by=/usr/share/keyrings/habana-artifactory.gpg] https://${ARTIFACTORY_URL}/artifactory/debian jammy main\" | tee -a /etc/apt/sources.list \\\n+ && apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    habanalabs-rdma-core=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-thunk=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-firmware-tools=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-graph=\"$VERSION\"-\"$REVISION\" \\\n+ && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/* \\\n+ && sed --in-place \"/$ARTIFACTORY_URL/d\" /etc/apt/sources.list\n+\n+# install libfabric\n+RUN wget -nv -O /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 https://github.com/ofiwg/libfabric/releases/download/v${LIBFABRIC_VERSION}/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/ && tar xf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/libfabric-${LIBFABRIC_VERSION} \\\n+ && ./configure --prefix=$LIBFABRIC_ROOT --enable-psm3-verbs --enable-verbs=yes --with-synapseai=/usr \\\n+ && make -j && make install && cd / && rm -rf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 /tmp/libfabric-${LIBFABRIC_VERSION}\n+\n+# install hccl wrapper for ofi\n+RUN wget -nv -O /tmp/main.zip https://github.com/HabanaAI/hccl_ofi_wrapper/archive/refs/heads/main.zip \\",
        "comment_created_at": "2024-08-21T12:51:02+00:00",
        "comment_author": "tkatila",
        "comment_body": "roger",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "594100126",
    "pr_number": 5693,
    "pr_file": "components/crud-web-apps/tensorboards/Dockerfile",
    "created_at": "2021-03-15T07:27:00+00:00",
    "commented_code": "COPY --from=frontend /src/dist/ /src/app/static/\r\n\r\nENTRYPOINT make run\r\nENTRYPOINT gunicorn -w 3 --bind 0.0.0.0:5000 --access-logfile - entrypoint:app",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "594100126",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/Dockerfile",
        "discussion_id": "594100126",
        "commented_code": "@@ -48,4 +48,4 @@ COPY ./tensorboards/backend/Makefile .\n \r\n COPY --from=frontend /src/dist/ /src/app/static/\r\n \r\n-ENTRYPOINT make run\r\n+ENTRYPOINT gunicorn -w 3 --bind 0.0.0.0:5000 --access-logfile - entrypoint:app\r",
        "comment_created_at": "2021-03-15T07:27:00+00:00",
        "comment_author": "nrchakradhar",
        "comment_body": "Will this have any incompatibilities for IPv6?",
        "pr_file_module": null
      },
      {
        "comment_id": "594201616",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/Dockerfile",
        "discussion_id": "594100126",
        "commented_code": "@@ -48,4 +48,4 @@ COPY ./tensorboards/backend/Makefile .\n \r\n COPY --from=frontend /src/dist/ /src/app/static/\r\n \r\n-ENTRYPOINT make run\r\n+ENTRYPOINT gunicorn -w 3 --bind 0.0.0.0:5000 --access-logfile - entrypoint:app\r",
        "comment_created_at": "2021-03-15T10:07:46+00:00",
        "comment_author": "davidspek",
        "comment_body": "@nrchakradhar Good point. These same entrypoint is being used by the Jupyter-Web-App. Do you have suggestions how to make this IPv6 compatible?",
        "pr_file_module": null
      },
      {
        "comment_id": "594277714",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/Dockerfile",
        "discussion_id": "594100126",
        "commented_code": "@@ -48,4 +48,4 @@ COPY ./tensorboards/backend/Makefile .\n \r\n COPY --from=frontend /src/dist/ /src/app/static/\r\n \r\n-ENTRYPOINT make run\r\n+ENTRYPOINT gunicorn -w 3 --bind 0.0.0.0:5000 --access-logfile - entrypoint:app\r",
        "comment_created_at": "2021-03-15T12:04:49+00:00",
        "comment_author": "nrchakradhar",
        "comment_body": "I do not know anything about gunicorn, but from its documentation, the following may work:\r\nhttps://docs.gunicorn.org/en/stable/settings.html\r\nMultiple addresses can be bound. ex.:\r\n\r\n$ gunicorn -b 127.0.0.1:8000 -b [::1]:8000 test:app\r\nwill bind the test:app application on localhost both on ipv6 and ipv4 interfaces.\r\n\r\nI found an interesting observation here(its quite old though)\r\nhttps://github.com/benoitc/gunicorn/issues/1138#issuecomment-158358666\r\n\r\nCan we make this configurable from manifests so that IPv6 support is provided. There are few issues created already for IPv6 support: #5615 #5605 ",
        "pr_file_module": null
      },
      {
        "comment_id": "595368484",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/Dockerfile",
        "discussion_id": "594100126",
        "commented_code": "@@ -48,4 +48,4 @@ COPY ./tensorboards/backend/Makefile .\n \r\n COPY --from=frontend /src/dist/ /src/app/static/\r\n \r\n-ENTRYPOINT make run\r\n+ENTRYPOINT gunicorn -w 3 --bind 0.0.0.0:5000 --access-logfile - entrypoint:app\r",
        "comment_created_at": "2021-03-16T17:01:39+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "@nrchakradhar thank you for your comments. I'm planning on tackling the IPv6 support for all the web apps after 1.3.\r\n\r\nThe first step is to bind the IPv6 equivalent addresses as well, as you've pointed out in your links. But I want to do a good deep dive on this and test some edge cases for which I don't have the cycles right now. ",
        "pr_file_module": null
      }
    ]
  }
]
