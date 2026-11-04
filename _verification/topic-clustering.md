---
title: "Topic clustering"
code: "V1037.002"
slug: "topic-clustering"
technique: "Reviewers learned from past reviews"
technique_id: "V1037"
technique_slug: "reviewers-learned-from-past-reviews"
tactic: "Code review"
tactic_id: "VA06"
description: "Cluster comments into themes with a minimum number of supporting discussions."
repos: 0
craft:
  - "Embed each review comment as a vector with a sentence-embedding library."
  - "Cluster the vectors and drop clusters with fewer than the minimum number of independent threads."
  - "Record the cluster size and the threads behind each cluster."
reverse:
  - "A clustering configuration with a min_cluster_size value in the analysis script."
  - "Cluster output files that list the threads supporting each theme."
packages:
  - id: "bertopic"
    name: "BERTopic"
    url: "https://github.com/MaartenGr/BERTopic"
  - id: "hdbscan"
    name: "HDBSCAN"
    url: "https://github.com/scikit-learn-contrib/hdbscan"
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
tools: []
examples: []
---
