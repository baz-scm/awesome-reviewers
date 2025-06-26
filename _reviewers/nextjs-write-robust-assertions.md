---
title: "Write robust assertions"
description: "When writing tests, ensure assertions can handle non-deterministic content while providing clear failure context: use targeted assertions for non-deterministic content, use specialized tools like cheerio for DOM testing, and include contextual information in diagnostic tests."
repository: "vercel/next.js"
label: "Testing"
language: "TypeScript"
comments_count: 5
repository_stars: 133000
---

When writing tests, ensure assertions can handle non-deterministic content while providing clear failure context:

1. **For non-deterministic content** (like absolute paths in error outputs):
    - Use targeted assertions (`toContain()`, `toInclude()`) instead of full snapshots
    - Add explanatory comments about why standard approaches aren't being used

   ```javascript
   // GOOD
   // rspack returns error content that contains absolute paths which are non deterministic
   await session.assertHasRedbox();
   expect(redboxContent).toContain("Module not found: Can't resolve 'dns'");
   expect(redboxLabel).toContain('Build Error');
   
   // AVOID
   await expect(browser).toDisplayRedbox(`
     "error": {
       "message": "[absolute path that will change]",
     }
   `);
   ```

2. **For DOM testing**:
    - Use specialized tools like cheerio instead of string manipulation
    - Add identifiers to tested elements to make assertions more reliable

   ```javascript
   // GOOD
   const $ = await next.render$('/');
   expect($('#server-value').text()).toBe('Server value: foobar');
   
   // AVOID
   const html = (await res.text()).replaceAll(/<!-- -->/g, '');
   expect(html).toContain('Server value: foobar');
   ```

3. **For diagnostic tests**:
    - Include contextual information (e.g., filenames) in assertions
    - Use declarative assertion patterns over iterative approaches

   ```javascript
   // GOOD
   expect(diagnosedFiles).toEqual({
     'page.tsx': { code: NEXT_TS_ERRORS.INVALID_METADATA_EXPORT, /*...*/ },
     'layout.tsx': { code: NEXT_TS_ERRORS.INVALID_METADATA_EXPORT, /*...*/ }
   });
   
   // AVOID
   for (const tsFile of tsFiles) {
     const diagnostics = languageService.getSemanticDiagnostics(tsFile);
     expect(diagnostics.length).toBe(1);
     // No context about which file failed if assertion fails
   }
   ```