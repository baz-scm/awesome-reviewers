---
title: Prevent async race conditions
description: 'Always guard against race conditions when working with asynchronous
  code. Implement these patterns to avoid unpredictable behavior:


  1. **Always await async operations**'
repository: elie222/inbox-zero
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 8267
---

Always guard against race conditions when working with asynchronous code. Implement these patterns to avoid unpredictable behavior:

1. **Always await async operations**
   ```javascript
   // Incorrect: Potential race condition
   processPreviousSentEmailsAction(emailAccountId);
   
   // Correct: Ensures operation completes before continuing
   await processPreviousSentEmailsAction(emailAccountId);
   ```

2. **Disable interactive elements during async operations**
   ```javascript
   const [isLoading, setIsLoading] = useState(false);
   
   return (
     <Button
       disabled={isLoading}
       onClick={async () => {
         if (isLoading) return;
         setIsLoading(true);
         try {
           await someAsyncAction();
           // Handle success
         } finally {
           setIsLoading(false);
         }
       }}
     >
       {isLoading ? 'Processing...' : 'Submit'}
     </Button>
   );
   ```

3. **Clean up event listeners in useEffect hooks**
   ```javascript
   useEffect(() => {
     if (!api) return;
     
     const handler = () => {
       // Handle event
     };
     api.on("select", handler);
     
     return () => {
       // Clean up to prevent memory leaks
       api.off("select", handler);
     };
   }, [api]);
   ```

These practices prevent issues like duplicate submissions, unhandled promises, memory leaks, and unpredictable UI behavior resulting from concurrent operations interfering with each other.