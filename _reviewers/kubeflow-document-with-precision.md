---
title: Document with precision
description: 'Write informative, consistent, and precise code comments throughout
  your codebase. When documenting code:


  1. **Be specific with references** - When referencing external repositories or sources,
  link to specific versions and files, not just directories. Use precise language
  to describe the relationship between your code and external sources.'
repository: kubeflow/kubeflow
label: Documentation
language: Dockerfile
comments_count: 3
repository_stars: 15064
---

Write informative, consistent, and precise code comments throughout your codebase. When documenting code:

1. **Be specific with references** - When referencing external repositories or sources, link to specific versions and files, not just directories. Use precise language to describe the relationship between your code and external sources.

```
# AVOID:
# Content below is extracted from scripts/Dockerfiles here:
# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base

# BETTER:
# Content below is based on:
# https://github.com/HabanaAI/Setup_and_Install/blob/1.17.0/dockerfiles/base/Dockerfile.ubuntu22.04
```

2. **Add explanatory comments** - Include brief descriptions for significant code blocks, especially when installing components or defining important configurations.

```
# AVOID:
RUN python3 -m pip install habana_media_loader=="${VERSION}"."${REVISION}"

# BETTER:
# Install Habana media loader library for PyTorch integration
RUN python3 -m pip install habana_media_loader=="${VERSION}"."${REVISION}"
```

3. **Maintain consistent styles** - Use consistent comment headers and styles across similar files to improve readability and maintainability.

```
# AVOID mixing styles:
# version details
# and elsewhere:
# args - software versions

# BETTER: Use consistent headers:
# args - software versions
```

Well-documented code improves comprehension, facilitates maintenance, and enhances collaboration among team members.


[
  {
    "discussion_id": "1720450533",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-16T23:15:07+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720450533",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720450533",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch",
        "comment_created_at": "2024-08-16T23:15:07+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "Can we update these links to be to a specific version, and file, e.g.:\r\n\r\n- https://github.com/HabanaAI/Setup_and_Install/blob/1.17.0/dockerfiles/base/Dockerfile.ubuntu22.04\r\n- https://github.com/HabanaAI/Setup_and_Install/blob/1.17.0/dockerfiles/pytorch/Dockerfile.ubuntu\r\n\r\nPlease also say \"based on\" because the content is not the same.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1720480710",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-17T00:02:29+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n\n# version details\nARG ARTIFACTORY_URL=vault.habana.ai\nARG VERSION=1.16.2\nARG REVISION=2\nARG PYTORCH_VERSION=2.2.2\nARG OS_NUMBER=2204\n\n# runtime variables\nENV DEBIAN_FRONTEND=noninteractive\nENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\nENV HABANA_LOGS=/var/log/habana_logs/\nENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\nENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\nENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\nENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n\n# There is no need to store pip installation files inside docker image\nENV PIP_NO_CACHE_DIR=on\nENV PIP_DISABLE_PIP_VERSION_CHECK=1\n\n# libfabric and scaling variables\nENV LIBFABRIC_VERSION=\"1.20.0\"\nENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\nENV MPI_ROOT=/opt/amazon/openmpi\nENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\nENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\nENV MPICC=${MPI_ROOT}/bin/mpicc\nENV OPAL_PREFIX=${MPI_ROOT}\nENV RDMAV_FORK_SAFE=1\nENV FI_EFA_USE_DEVICE_RDMA=1\nENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\nENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n\n# Gaudi stack doesn't (yet) support 3.11, thus\n# downgrade python from 3.11.x to 3.10.14\nRUN source /opt/conda/etc/profile.d/conda.sh \\\n && conda activate base \\\n && conda install -y -q --no-pin python=3.10.14 \\\n && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n && conda clean -a -f -y\n\nUSER root\n\n# install various support libraries\nRUN apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    apt-utils \\\n    bc \\\n    build-essential \\\n    graphviz \\\n    iproute2 \\\n    libcairo2-dev \\\n    libgl1 \\\n    libglib2.0-dev \\\n    libgnutls30 \\\n    libgoogle-glog0v5 \\\n    libgoogle-perftools-dev \\\n    libhdf5-dev \\\n    libjemalloc2 \\\n    libjpeg-dev \\\n    liblapack-dev \\\n    libmkl-dev \\\n    libnuma-dev \\\n    libopenblas-dev \\\n    libpcre2-dev \\\n    libpq-dev \\\n    libselinux1-dev \\\n    lsof \\\n    moreutils \\\n    numactl \\\n    protobuf-compiler \\\n && apt-get autoremove \\\n && apt-get clean \\\n && rm -rf /var/lib/apt/lists/*\n\n# install elastic fabric adapter\nRUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n\n# install habana packages\nRUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\\n && chown root:root /usr/share/keyrings/habana-artifactory.gpg \\\n && chmod 644 /usr/share/keyrings/habana-artifactory.gpg \\\n && echo \"deb [signed-by=/usr/share/keyrings/habana-artifactory.gpg] https://${ARTIFACTORY_URL}/artifactory/debian jammy main\" | tee -a /etc/apt/sources.list \\\n && apt-get update \\\n && apt-get install -y --no-install-recommends \\\n    habanalabs-rdma-core=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-thunk=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-firmware-tools=\"$VERSION\"-\"$REVISION\" \\\n    habanalabs-graph=\"$VERSION\"-\"$REVISION\" \\\n && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/* \\\n && sed --in-place \"/$ARTIFACTORY_URL/d\" /etc/apt/sources.list\n\n# install libfabric\nRUN wget -nv -O /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 https://github.com/ofiwg/libfabric/releases/download/v${LIBFABRIC_VERSION}/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n && cd /tmp/ && tar xf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n && cd /tmp/libfabric-${LIBFABRIC_VERSION} \\\n && ./configure --prefix=$LIBFABRIC_ROOT --enable-psm3-verbs --enable-verbs=yes --with-synapseai=/usr \\\n && make -j && make install && cd / && rm -rf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 /tmp/libfabric-${LIBFABRIC_VERSION}\n\n# install hccl wrapper for ofi\nRUN wget -nv -O /tmp/main.zip https://github.com/HabanaAI/hccl_ofi_wrapper/archive/refs/heads/main.zip \\\n && unzip /tmp/main.zip -d /tmp \\\n && cd /tmp/hccl_ofi_wrapper-main \\\n && make \\\n && cp -f libhccl_ofi_wrapper.so /usr/lib/habanalabs/libhccl_ofi_wrapper.so \\\n && cd / \\\n && rm -rf /tmp/main.zip /tmp/hccl_ofi_wrapper-main\n\nRUN /sbin/ldconfig\n\nUSER $NB_UID\n\n# install habana pytorch and media python libraries\nRUN python3 -m pip install habana_media_loader==\"${VERSION}\".\"${REVISION}\"\n\nRUN mkdir /tmp/gaudipt \\",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720480710",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720480710",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details\n+ARG ARTIFACTORY_URL=vault.habana.ai\n+ARG VERSION=1.16.2\n+ARG REVISION=2\n+ARG PYTORCH_VERSION=2.2.2\n+ARG OS_NUMBER=2204\n+\n+# runtime variables\n+ENV DEBIAN_FRONTEND=noninteractive\n+ENV GC_KERNEL_PATH=/usr/lib/habanalabs/libtpc_kernels.so\n+ENV HABANA_LOGS=/var/log/habana_logs/\n+ENV HABANA_SCAL_BIN_PATH=/opt/habanalabs/engines_fw\n+ENV HABANA_PLUGINS_LIB_PATH=/opt/habanalabs/habana_plugins\n+ENV TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD=7516192768\n+ENV PYTHONPATH=/home/$NB_UID:/usr/lib/habanalabs/\n+\n+# There is no need to store pip installation files inside docker image\n+ENV PIP_NO_CACHE_DIR=on\n+ENV PIP_DISABLE_PIP_VERSION_CHECK=1\n+\n+# libfabric and scaling variables\n+ENV LIBFABRIC_VERSION=\"1.20.0\"\n+ENV LIBFABRIC_ROOT=\"/opt/habanalabs/libfabric-${LIBFABRIC_VERSION}\"\n+ENV MPI_ROOT=/opt/amazon/openmpi\n+ENV LD_LIBRARY_PATH=$LIBFABRIC_ROOT/lib:${MPI_ROOT}/lib:/usr/lib/habanalabs:$LD_LIBRARY_PATH\n+ENV PATH=${LIBFABRIC_ROOT}/bin:${MPI_ROOT}/bin:$PATH\n+ENV MPICC=${MPI_ROOT}/bin/mpicc\n+ENV OPAL_PREFIX=${MPI_ROOT}\n+ENV RDMAV_FORK_SAFE=1\n+ENV FI_EFA_USE_DEVICE_RDMA=1\n+ENV RDMA_CORE_ROOT=/opt/habanalabs/rdma-core/src\n+ENV RDMA_CORE_LIB=${RDMA_CORE_ROOT}/build/lib\n+\n+# Gaudi stack doesn't (yet) support 3.11, thus\n+# downgrade python from 3.11.x to 3.10.14\n+RUN source /opt/conda/etc/profile.d/conda.sh \\\n+ && conda activate base \\\n+ && conda install -y -q --no-pin python=3.10.14 \\\n+ && sed -i 's/python ==.*/python ==3.10.14/' /opt/conda/conda-meta/pinned \\\n+ && conda clean -a -f -y\n+\n+USER root\n+\n+# install various support libraries\n+RUN apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    apt-utils \\\n+    bc \\\n+    build-essential \\\n+    graphviz \\\n+    iproute2 \\\n+    libcairo2-dev \\\n+    libgl1 \\\n+    libglib2.0-dev \\\n+    libgnutls30 \\\n+    libgoogle-glog0v5 \\\n+    libgoogle-perftools-dev \\\n+    libhdf5-dev \\\n+    libjemalloc2 \\\n+    libjpeg-dev \\\n+    liblapack-dev \\\n+    libmkl-dev \\\n+    libnuma-dev \\\n+    libopenblas-dev \\\n+    libpcre2-dev \\\n+    libpq-dev \\\n+    libselinux1-dev \\\n+    lsof \\\n+    moreutils \\\n+    numactl \\\n+    protobuf-compiler \\\n+ && apt-get autoremove \\\n+ && apt-get clean \\\n+ && rm -rf /var/lib/apt/lists/*\n+\n+# install elastic fabric adapter\n+RUN apt-get update && export EFA_VERSION=1.29.0 && mkdir /tmp/efa \\\n+ && wget -q -O- https://efa-installer.amazonaws.com/aws-efa-installer-$EFA_VERSION.tar.gz | tar xz -C /tmp/efa \\\n+ && cd /tmp/efa/aws-efa-installer && ./efa_installer.sh -y --skip-kmod --skip-limit-conf --no-verify \\\n+ && rm -rf /tmp/efa && rm -rf /etc/ld.so.conf.d/efa.conf /etc/profile.d/efa.sh \\\n+ && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*\n+\n+# install habana packages\n+RUN wget -O- https://${ARTIFACTORY_URL}/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chown root:root /usr/share/keyrings/habana-artifactory.gpg \\\n+ && chmod 644 /usr/share/keyrings/habana-artifactory.gpg \\\n+ && echo \"deb [signed-by=/usr/share/keyrings/habana-artifactory.gpg] https://${ARTIFACTORY_URL}/artifactory/debian jammy main\" | tee -a /etc/apt/sources.list \\\n+ && apt-get update \\\n+ && apt-get install -y --no-install-recommends \\\n+    habanalabs-rdma-core=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-thunk=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-firmware-tools=\"$VERSION\"-\"$REVISION\" \\\n+    habanalabs-graph=\"$VERSION\"-\"$REVISION\" \\\n+ && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/* \\\n+ && sed --in-place \"/$ARTIFACTORY_URL/d\" /etc/apt/sources.list\n+\n+# install libfabric\n+RUN wget -nv -O /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 https://github.com/ofiwg/libfabric/releases/download/v${LIBFABRIC_VERSION}/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/ && tar xf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 \\\n+ && cd /tmp/libfabric-${LIBFABRIC_VERSION} \\\n+ && ./configure --prefix=$LIBFABRIC_ROOT --enable-psm3-verbs --enable-verbs=yes --with-synapseai=/usr \\\n+ && make -j && make install && cd / && rm -rf /tmp/libfabric-${LIBFABRIC_VERSION}.tar.bz2 /tmp/libfabric-${LIBFABRIC_VERSION}\n+\n+# install hccl wrapper for ofi\n+RUN wget -nv -O /tmp/main.zip https://github.com/HabanaAI/hccl_ofi_wrapper/archive/refs/heads/main.zip \\\n+ && unzip /tmp/main.zip -d /tmp \\\n+ && cd /tmp/hccl_ofi_wrapper-main \\\n+ && make \\\n+ && cp -f libhccl_ofi_wrapper.so /usr/lib/habanalabs/libhccl_ofi_wrapper.so \\\n+ && cd / \\\n+ && rm -rf /tmp/main.zip /tmp/hccl_ofi_wrapper-main\n+\n+RUN /sbin/ldconfig\n+\n+USER $NB_UID\n+\n+# install habana pytorch and media python libraries\n+RUN python3 -m pip install habana_media_loader==\"${VERSION}\".\"${REVISION}\"\n+\n+RUN mkdir /tmp/gaudipt \\",
        "comment_created_at": "2024-08-17T00:02:29+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "Please add a breif `#` comment explaining what is being installed.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1720488570",
    "pr_number": 7635,
    "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
    "created_at": "2024-08-17T00:25:48+00:00",
    "commented_code": "#\n# NOTE: Use the Makefiles to build this image correctly.\n#\n\nARG BASE_IMG=<jupyter>\nFROM $BASE_IMG\n\n# Content below is extracted from scripts/Dockerfiles here:\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n\n# version details",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1720488570",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7635,
        "pr_file": "components/example-notebook-servers/jupyter-pytorch-gaudi/Dockerfile",
        "discussion_id": "1720488570",
        "commented_code": "@@ -0,0 +1,143 @@\n+#\n+# NOTE: Use the Makefiles to build this image correctly.\n+#\n+\n+ARG BASE_IMG=<jupyter>\n+FROM $BASE_IMG\n+\n+# Content below is extracted from scripts/Dockerfiles here:\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base\n+# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/pytorch\n+\n+# version details",
        "comment_created_at": "2024-08-17T00:25:48+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "For consistency with other images:\r\n\r\n```suggestion\r\n# args - software versions\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
