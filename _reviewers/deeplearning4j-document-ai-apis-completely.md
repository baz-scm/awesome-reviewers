---
title: Document AI APIs completely
description: 'When developing AI libraries and tools, provide comprehensive and accurate
  API documentation that helps users navigate complex functionality. Documentation
  should:'
repository: deeplearning4j/deeplearning4j
label: AI
language: Markdown
comments_count: 4
repository_stars: 14036
---

When developing AI libraries and tools, provide comprehensive and accurate API documentation that helps users navigate complex functionality. Documentation should:

1. **Be explicit about method status and lifecycle:**
   - Clearly mark deprecated methods and provide better alternatives
   - Example from discussions:
   ```java
   // AVOID documenting only:
   List<String> outputs = sd.outputs(); // Will be removed in future versions
   
   // BETTER documentation:
   // Finding outputs: Use sd.summary() to examine the graph structure
   // The outputs() method will be deprecated as it's not robust enough
   sd.summary(); // Examine to find outputs (variables that are inputs to no ops)
   ```

2. **Document all execution patterns:**
   - Show both simple and advanced usage patterns
   - Explain alternatives for different scenarios
   - Example:
   ```java
   // For single output:
   INDArray out = sd.batchOutput()
       .input(inputs, inputArray)
       .output(outputs)
       .execSingle();
       
   // For multiple outputs:
   Map<String,INDArray> results = sd.batchOutput()
       .input(inputs, inputArray)
       .output(outputs)
       .exec();
   ```

3. **Be transparent about limitations:**
   - Clearly document supported and unsupported features
   - Example: "SameDiff's TensorFlow import is still being developed, and does not yet have support for every single operation and datatype in TensorFlow. Almost all of the common/standard operations are importable and tested, however..."

4. **Hide implementation details:**
   - Focus on what users need to know, not internal mechanisms
   - Avoid mentioning internal components like "differential function factory" that most users will never need to interact with

Structure documentation with common use cases first, followed by advanced topics, making it easy for users to find the information most relevant to their needs.