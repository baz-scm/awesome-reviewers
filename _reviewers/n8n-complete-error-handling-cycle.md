---
title: Complete error handling cycle
description: 'Implement comprehensive error handling that covers prevention, recovery,
  and diagnosis:


  1. **Prevent errors** through thorough validation before enabling actions'
repository: n8n-io/n8n
label: Error Handling
language: Other
comments_count: 3
repository_stars: 122978
---

Implement comprehensive error handling that covers prevention, recovery, and diagnosis:

1. **Prevent errors** through thorough validation before enabling actions
   - Validate that all required data exists before allowing operations
   ```js
   // Instead of just checking mime type and filename
   function isDownloadable(index, key) {
     const { mimeType, fileName } = binaryData[index][key];
     return !!(mimeType && fileName && (binaryData[index][key].id || binaryData[index][key].data));
   }
   ```

2. **Ensure recovery** by properly resetting state flags in finally blocks
   - Don't leave UI in disabled states after operations complete or fail
   ```js
   try {
     cancellingTestRun.value = true;
     await evaluationStore.cancelTestRun(workflowId, runId);
   } catch (error) {
     // Error handling
   } finally {
     cancellingTestRun.value = false;
   }
   ```

3. **Enable diagnosis** by preserving and exposing error details
   - Log complete error objects, not just generic messages
   ```js
   } catch (error) {
     console.error(chalk.red(`An error occurred during the build process: ${error}`));
   }
   ```

Each layer of error handling contributes to a more robust application that prevents user frustration and simplifies troubleshooting.