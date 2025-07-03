---
title: Clarity over uncertainty
description: Technical documentation should use precise language that clearly differentiates
  between product behavior and user configuration options. Frame explanations from
  the user's perspective, emphasizing capabilities rather than limitations.
repository: elastic/elasticsearch
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 73104
---

Technical documentation should use precise language that clearly differentiates between product behavior and user configuration options. Frame explanations from the user's perspective, emphasizing capabilities rather than limitations.

When describing configurable functionality:
- Replace phrases that suggest uncertainty (like "this is not guaranteed") with empowering language ("you may choose to adjust this behavior").
- Use specific examples to illustrate options rather than vague statements.
- Structure information as actionable items when possible.

For performance-related documentation:
- Be explicit about cause-effect relationships.
- Use bullet points for clarity when listing multiple scenarios.
- Consider how language around limitations will be perceived by users.

Example improvement:
```diff
- Force merging will be performed by the nodes within the current phase of the index. 
- A forcemerge in the `hot` phase will use hot nodes with potentially faster nodes, 
- while impacting ingestion more. A forcemerge in the `warm` phase will use warm 
- nodes and potentially take longer to perform, but without impacting ingestion in 
- the `hot` tier.

+ Force merging will be performed by the node hosting the shard. Usually, the node's 
+ role matches the data tier of the ILM phase that the index is in. For example:
+ * A force merge in the `hot` phase will use hot nodes. Merges may be faster on this 
+   potentially higher performance hardware but may impact ingestion.
+ * A force merge in the `warm` phase will use warm nodes. Merges may take longer to 
+   perform on potentially lower performance hardware but will avoid impacting 
+   ingestion in the `hot` tier.
```

Remember that marketing/positioning around limitations is particularly sensitive - always emphasize what users can do rather than what they cannot do.
