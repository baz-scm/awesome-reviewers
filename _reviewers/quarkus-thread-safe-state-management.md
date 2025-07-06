---
title: Thread-safe state management
description: 'When managing state accessed by multiple threads, ensure thread safety
  through appropriate synchronization mechanisms:


  1. **Use thread-safe collections** for multi-threaded access:'
repository: quarkusio/quarkus
label: Concurrency
language: Java
comments_count: 6
repository_stars: 14667
---

When managing state accessed by multiple threads, ensure thread safety through appropriate synchronization mechanisms:

1. **Use thread-safe collections** for multi-threaded access:
   ```java
   // Incorrect
   private List<TraceListener> listeners;
   
   // Correct
   private final List<TraceListener> listeners = new CopyOnWriteArrayList<>();
   ```

2. **Implement proper lazy initialization** with either:
   - Volatile fields with double-checked locking
   - The `LazyValue` abstraction
   - Initialization at construction time with final fields
   ```java
   // Incorrect - not thread-safe
   private TraceManager traceManager;
   
   public TraceManager getTraceManager() {
       if (traceManager == null) {
           traceManager = new TraceManager(); // Race condition!
       }
       return traceManager;
   }
   
   // Correct - thread-safe with volatile
   private volatile TraceManager traceManager;
   
   public TraceManager getTraceManager() {
       TraceManager result = traceManager;
       if (result == null) {
           synchronized (this) {
               result = traceManager;
               if (result == null) {
                   traceManager = result = new TraceManager();
               }
           }
       }
       return result;
   }
   ```

3. **For bit flag operations**, use atomic operations rather than separate atomic fields:
   ```java
   // Correct pattern for concurrent bit flag operations
   private boolean set(byte bitMask) {
       byte state = this.state;
       for (;;) {
           if ((state & bitMask) != 0) {
               return false;
           }
           final byte newState = (byte) (state | bitMask);
           // Use compareAndExchange for atomicity
           byte oldState = STATE_UPDATER.compareAndExchange(this, state, newState);
           if (oldState == state) {
               return true;
           }
           state = oldState;
       }
   }
   ```

4. **Avoid storing shared mutable state** in fields accessed by concurrent operations:
   ```java
   // Incorrect - potential race condition
   private static AuthDevUIRecorder recorder;
   
   @BuildStep
   void doSomething(AuthDevUIRecorder recorder) {
       AuthProcessor.recorder = recorder; // Multiple build steps might race
   }
   
   // Correct - pass local parameters
   @BuildStep
   void doSomething(AuthDevUIRecorder recorder) {
       performOperation(recorder);
   }
   ```