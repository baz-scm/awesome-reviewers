---
title: Technical precision matters
description: When documenting AI models, frameworks, and optimization techniques,
  precision in language is as important as precision in your algorithms. Technical
  inaccuracies or unclear explanations can lead to implementation errors and confusion.
repository: apache/mxnet
label: AI
language: Markdown
comments_count: 8
repository_stars: 20801
---

When documenting AI models, frameworks, and optimization techniques, precision in language is as important as precision in your algorithms. Technical inaccuracies or unclear explanations can lead to implementation errors and confusion.

Key practices to follow:

1. Use precise terminology when describing AI operations like quantization, operator fusion, and model optimization:
   - Be specific about performance impacts: "With quantized model there is a tiny accuracy drop, however this is the cost of great performance optimization and memory footprint reduction."
   - Clearly explain technical processes: "Last stage of quantization flow is to perform additional operator fusion."

2. Ensure grammatical correctness, especially when explaining causality in AI systems:
   - Incorrect: "find operator which mostly influence accuracy drops"
   - Correct: "find operator, which caused the most significant accuracy drop"

3. Maintain consistency in technical descriptions:
   - Use correct library names and conventions (e.g., oneDNN not ONEDNN)
   - Be consistent with framework terminology across documentation

4. Use appropriate articles and prepositions in technical explanations:
   - Incorrect: "INC allows automatically find better solution"
   - Correct: "INC allows to automatically find better solution"

Clear documentation directly impacts how effectively developers can implement and optimize AI models, particularly for critical operations like quantization that balance accuracy and performance.
