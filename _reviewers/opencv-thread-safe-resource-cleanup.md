---
title: Thread-safe resource cleanup
description: When implementing resource cleanup in concurrent applications, avoid
  using deprecated finalizers and instead use PhantomReference-based cleanup mechanisms
  that ensure thread safety.
repository: opencv/opencv
label: Concurrency
language: Java
comments_count: 2
repository_stars: 82865
---

When implementing resource cleanup in concurrent applications, avoid using deprecated finalizers and instead use PhantomReference-based cleanup mechanisms that ensure thread safety.

Key considerations:
1. Use PhantomReference with a ReferenceQueue to detect when objects are ready for cleanup
2. Maintain appropriate data structures (e.g., doubly-linked lists) to track references and support efficient removal
3. Implement a dedicated daemon thread to process the cleanup queue
4. Ensure the cleaner object outlives the resources it manages

Example implementation:
```java
public final class SafeResourceCleaner {
    private final ReferenceQueue<Object> queue = new ReferenceQueue<>();
    private final PhantomCleanable phantomCleanableList = new PhantomCleanable();
    
    // Create a single cleaner per application/library component
    public static SafeResourceCleaner create() {
        SafeResourceCleaner cleaner = new SafeResourceCleaner();
        cleaner.startCleanerThread();
        return cleaner;
    }
    
    public Cleanable register(Object resource, Runnable cleanupAction) {
        return new PhantomCleanable(
            Objects.requireNonNull(resource), 
            Objects.requireNonNull(cleanupAction)
        );
    }
    
    private void startCleanerThread() {
        Thread thread = new Thread(() -> {
            while (!isShutdown()) {
                try {
                    // Use reasonable timeout to allow thread termination if needed
                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);
                    if (ref != null) {
                        ref.clean();
                    }
                } catch (Throwable e) {
                    // Handle exceptions gracefully, never let them terminate the cleaner thread
                }
            }
        }, "ResourceCleaner-Thread");
        thread.setDaemon(true);  // Don't prevent JVM shutdown
        thread.start();
    }
}
```

This approach is particularly important for concurrent applications where thread safety must be maintained during resource cleanup, and it provides a more reliable alternative to the deprecated finalize() method.


[
  {
    "discussion_id": "1942571100",
    "pr_number": 23467,
    "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
    "created_at": "2025-02-05T09:59:55+00:00",
    "commented_code": "package org.opencv.core;\n\nimport java.lang.ref.PhantomReference;\nimport java.lang.ref.ReferenceQueue;\nimport java.util.Objects;\nimport java.util.concurrent.atomic.AtomicInteger;\n\n/**\n * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n * from Java 9.\n * <p>\n * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n * since Java 18\n * <p>\n * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n */\npublic final class CustomCleaner {\n\n    final PhantomCleanable phantomCleanableList;\n\n    // The ReferenceQueue of pending cleaning actions\n    final ReferenceQueue<Object> queue;\n\n    private CustomCleaner() {\n        queue = new ReferenceQueue<>();\n        phantomCleanableList = new PhantomCleanable();\n    }\n\n    public static CustomCleaner create() {\n        CustomCleaner customCleaner = new CustomCleaner();\n        customCleaner.start();\n        return customCleaner;\n    }\n\n    public Cleanable register(Object obj, Runnable action) {\n        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n    }\n\n    private void start() {\n        new PhantomCleanable(this, null);\n        Thread thread = new CleanerThread(() -> {\n            while (!phantomCleanableList.isListEmpty()) {\n                try {\n                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1942571100",
        "repo_full_name": "opencv/opencv",
        "pr_number": 23467,
        "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
        "discussion_id": "1942571100",
        "commented_code": "@@ -0,0 +1,149 @@\n+package org.opencv.core;\n+\n+import java.lang.ref.PhantomReference;\n+import java.lang.ref.ReferenceQueue;\n+import java.util.Objects;\n+import java.util.concurrent.atomic.AtomicInteger;\n+\n+/**\n+ * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n+ * from Java 9.\n+ * <p>\n+ * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n+ * since Java 18\n+ * <p>\n+ * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n+ * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n+ */\n+public final class CustomCleaner {\n+\n+    final PhantomCleanable phantomCleanableList;\n+\n+    // The ReferenceQueue of pending cleaning actions\n+    final ReferenceQueue<Object> queue;\n+\n+    private CustomCleaner() {\n+        queue = new ReferenceQueue<>();\n+        phantomCleanableList = new PhantomCleanable();\n+    }\n+\n+    public static CustomCleaner create() {\n+        CustomCleaner customCleaner = new CustomCleaner();\n+        customCleaner.start();\n+        return customCleaner;\n+    }\n+\n+    public Cleanable register(Object obj, Runnable action) {\n+        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n+    }\n+\n+    private void start() {\n+        new PhantomCleanable(this, null);\n+        Thread thread = new CleanerThread(() -> {\n+            while (!phantomCleanableList.isListEmpty()) {\n+                try {\n+                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);",
        "comment_created_at": "2025-02-05T09:59:55+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "Why do we need timeout?",
        "pr_file_module": null
      },
      {
        "comment_id": "1998331173",
        "repo_full_name": "opencv/opencv",
        "pr_number": 23467,
        "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
        "discussion_id": "1942571100",
        "commented_code": "@@ -0,0 +1,149 @@\n+package org.opencv.core;\n+\n+import java.lang.ref.PhantomReference;\n+import java.lang.ref.ReferenceQueue;\n+import java.util.Objects;\n+import java.util.concurrent.atomic.AtomicInteger;\n+\n+/**\n+ * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n+ * from Java 9.\n+ * <p>\n+ * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n+ * since Java 18\n+ * <p>\n+ * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n+ * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n+ */\n+public final class CustomCleaner {\n+\n+    final PhantomCleanable phantomCleanableList;\n+\n+    // The ReferenceQueue of pending cleaning actions\n+    final ReferenceQueue<Object> queue;\n+\n+    private CustomCleaner() {\n+        queue = new ReferenceQueue<>();\n+        phantomCleanableList = new PhantomCleanable();\n+    }\n+\n+    public static CustomCleaner create() {\n+        CustomCleaner customCleaner = new CustomCleaner();\n+        customCleaner.start();\n+        return customCleaner;\n+    }\n+\n+    public Cleanable register(Object obj, Runnable action) {\n+        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n+    }\n+\n+    private void start() {\n+        new PhantomCleanable(this, null);\n+        Thread thread = new CleanerThread(() -> {\n+            while (!phantomCleanableList.isListEmpty()) {\n+                try {\n+                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);",
        "comment_created_at": "2025-03-17T09:39:27+00:00",
        "comment_author": "AlexanderSchuetz97",
        "comment_body": "Nroduit uses a long polling pattern here. Basically as explained above phantomCleanableList.isListEmpty() is only true when no reference to CustomCleaner exists. And if that is the case then the thread should stop because without a reference to the CustomerCleaner object enquening further cleaners is impossible.\r\n\r\nMy thoughts on this implementation:\r\nIts not how I would have implemented this, but its a valid way of doing it, possibly even the better way.\r\nNroduit has implemented this entire thing in a way that multiple cleaners and therefore multiple cleaner threads can be created. Openjdk/Oracle? recommends (somewhere in the jdk 9 'Cleaner' javadoc, which is what we are trying to re-create here) to only use exactly 1 cleaner per library. I would have not bothered with this complexity of implementing \"stopping\" of the cleaner and made it never stop once started. Then you wouldnt need a timeout. The only scenario I can think of where stopping would theoretically be required is if you wanted to support class unloading of opencv. I highly doubt that this would be a good idea as I dont think you guys properly implemented JNI_OnUnload on the native side to not leak memory. I think 95% of people dont use class unloading in their applications anyways, so its not really a problem.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1943671042",
    "pr_number": 23467,
    "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
    "created_at": "2025-02-05T21:14:46+00:00",
    "commented_code": "package org.opencv.core;\n\nimport java.lang.ref.PhantomReference;\nimport java.lang.ref.ReferenceQueue;\nimport java.util.Objects;\nimport java.util.concurrent.atomic.AtomicInteger;\n\n/**\n * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n * from Java 9.\n * <p>\n * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n * since Java 18\n * <p>\n * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n */\npublic final class CustomCleaner {\n\n    final PhantomCleanable phantomCleanableList;\n\n    // The ReferenceQueue of pending cleaning actions\n    final ReferenceQueue<Object> queue;\n\n    private CustomCleaner() {\n        queue = new ReferenceQueue<>();\n        phantomCleanableList = new PhantomCleanable();\n    }\n\n    public static CustomCleaner create() {\n        CustomCleaner customCleaner = new CustomCleaner();\n        customCleaner.start();\n        return customCleaner;\n    }\n\n    public Cleanable register(Object obj, Runnable action) {\n        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n    }\n\n    private void start() {\n        new PhantomCleanable(this, null);\n        Thread thread = new CleanerThread(() -> {\n            while (!phantomCleanableList.isListEmpty()) {\n                try {\n                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);\n                    if (ref != null) {\n                        ref.clean();\n                    }\n                } catch (Throwable e) {\n                    // ignore exceptions\n                }\n            }\n        } );\n        thread.setDaemon(true);\n        thread.start();\n    }\n\n    static final class CleanerThread extends Thread {\n\n        private static final AtomicInteger threadNumber = new AtomicInteger(1);\n\n        // ensure run method is run only once\n        private volatile boolean hasRun;\n\n        public CleanerThread(Runnable runnable) {\n            super(runnable, \"CustomCleaner-\" + threadNumber.getAndIncrement());\n        }\n\n        @Override\n        public void run() {\n            if (Thread.currentThread() == this && !hasRun) {\n                hasRun = true;\n                super.run();\n            }\n        }\n    }\n\n\n    public interface Cleanable {\n        void clean();\n    }\n\n    class PhantomCleanable extends PhantomReference<Object> implements Cleanable {\n\n        private final Runnable action;\n       PhantomCleanable prev = this;\n       PhantomCleanable next = this;\n\n        private final PhantomCleanable list;\n\n        public PhantomCleanable(Object referent, Runnable action) {\n            super(Objects.requireNonNull(referent), queue);\n            this.list = phantomCleanableList;",
    "repo_full_name": "opencv/opencv",
    "discussion_comments": [
      {
        "comment_id": "1943671042",
        "repo_full_name": "opencv/opencv",
        "pr_number": 23467,
        "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
        "discussion_id": "1943671042",
        "commented_code": "@@ -0,0 +1,149 @@\n+package org.opencv.core;\n+\n+import java.lang.ref.PhantomReference;\n+import java.lang.ref.ReferenceQueue;\n+import java.util.Objects;\n+import java.util.concurrent.atomic.AtomicInteger;\n+\n+/**\n+ * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n+ * from Java 9.\n+ * <p>\n+ * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n+ * since Java 18\n+ * <p>\n+ * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n+ * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n+ */\n+public final class CustomCleaner {\n+\n+    final PhantomCleanable phantomCleanableList;\n+\n+    // The ReferenceQueue of pending cleaning actions\n+    final ReferenceQueue<Object> queue;\n+\n+    private CustomCleaner() {\n+        queue = new ReferenceQueue<>();\n+        phantomCleanableList = new PhantomCleanable();\n+    }\n+\n+    public static CustomCleaner create() {\n+        CustomCleaner customCleaner = new CustomCleaner();\n+        customCleaner.start();\n+        return customCleaner;\n+    }\n+\n+    public Cleanable register(Object obj, Runnable action) {\n+        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n+    }\n+\n+    private void start() {\n+        new PhantomCleanable(this, null);\n+        Thread thread = new CleanerThread(() -> {\n+            while (!phantomCleanableList.isListEmpty()) {\n+                try {\n+                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);\n+                    if (ref != null) {\n+                        ref.clean();\n+                    }\n+                } catch (Throwable e) {\n+                    // ignore exceptions\n+                }\n+            }\n+        } );\n+        thread.setDaemon(true);\n+        thread.start();\n+    }\n+\n+    static final class CleanerThread extends Thread {\n+\n+        private static final AtomicInteger threadNumber = new AtomicInteger(1);\n+\n+        // ensure run method is run only once\n+        private volatile boolean hasRun;\n+\n+        public CleanerThread(Runnable runnable) {\n+            super(runnable, \"CustomCleaner-\" + threadNumber.getAndIncrement());\n+        }\n+\n+        @Override\n+        public void run() {\n+            if (Thread.currentThread() == this && !hasRun) {\n+                hasRun = true;\n+                super.run();\n+            }\n+        }\n+    }\n+\n+\n+    public interface Cleanable {\n+        void clean();\n+    }\n+\n+    class PhantomCleanable extends PhantomReference<Object> implements Cleanable {\n+\n+        private final Runnable action;\n+       PhantomCleanable prev = this;\n+       PhantomCleanable next = this;\n+\n+        private final PhantomCleanable list;\n+\n+        public PhantomCleanable(Object referent, Runnable action) {\n+            super(Objects.requireNonNull(referent), queue);\n+            this.list = phantomCleanableList;",
        "comment_created_at": "2025-02-05T21:14:46+00:00",
        "comment_author": "opencv-alalek",
        "comment_body": "Why do we need additional \"list\" if there is already \"queue\"?\r\n\r\nAny link on \"reference implementation code\"?\r\n\r\n**UPD**: E.g,  https://stackoverflow.com/a/14450693 - there are no any extra lists.",
        "pr_file_module": null
      },
      {
        "comment_id": "1998301635",
        "repo_full_name": "opencv/opencv",
        "pr_number": 23467,
        "pr_file": "modules/core/misc/java/src/java/CustomCleaner.java",
        "discussion_id": "1943671042",
        "commented_code": "@@ -0,0 +1,149 @@\n+package org.opencv.core;\n+\n+import java.lang.ref.PhantomReference;\n+import java.lang.ref.ReferenceQueue;\n+import java.util.Objects;\n+import java.util.concurrent.atomic.AtomicInteger;\n+\n+/**\n+ * This class is a Java 8+ implementation Cleaner similar to java.lang.ref.Cleaner available\n+ * from Java 9.\n+ * <p>\n+ * This implementation replace finalize() method that is deprecated since Java 9 and for removal\n+ * since Java 18\n+ * <p>\n+ * When OpenCV has Java 8 as its minimum version, this class can be removed and replaced by java.lang.ref.Cleaner.\n+ * In Mat, <code>public static final Cleaner cleaner = Cleaner.create();</code>\n+ */\n+public final class CustomCleaner {\n+\n+    final PhantomCleanable phantomCleanableList;\n+\n+    // The ReferenceQueue of pending cleaning actions\n+    final ReferenceQueue<Object> queue;\n+\n+    private CustomCleaner() {\n+        queue = new ReferenceQueue<>();\n+        phantomCleanableList = new PhantomCleanable();\n+    }\n+\n+    public static CustomCleaner create() {\n+        CustomCleaner customCleaner = new CustomCleaner();\n+        customCleaner.start();\n+        return customCleaner;\n+    }\n+\n+    public Cleanable register(Object obj, Runnable action) {\n+        return new PhantomCleanable(Objects.requireNonNull(obj), Objects.requireNonNull(action));\n+    }\n+\n+    private void start() {\n+        new PhantomCleanable(this, null);\n+        Thread thread = new CleanerThread(() -> {\n+            while (!phantomCleanableList.isListEmpty()) {\n+                try {\n+                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);\n+                    if (ref != null) {\n+                        ref.clean();\n+                    }\n+                } catch (Throwable e) {\n+                    // ignore exceptions\n+                }\n+            }\n+        } );\n+        thread.setDaemon(true);\n+        thread.start();\n+    }\n+\n+    static final class CleanerThread extends Thread {\n+\n+        private static final AtomicInteger threadNumber = new AtomicInteger(1);\n+\n+        // ensure run method is run only once\n+        private volatile boolean hasRun;\n+\n+        public CleanerThread(Runnable runnable) {\n+            super(runnable, \"CustomCleaner-\" + threadNumber.getAndIncrement());\n+        }\n+\n+        @Override\n+        public void run() {\n+            if (Thread.currentThread() == this && !hasRun) {\n+                hasRun = true;\n+                super.run();\n+            }\n+        }\n+    }\n+\n+\n+    public interface Cleanable {\n+        void clean();\n+    }\n+\n+    class PhantomCleanable extends PhantomReference<Object> implements Cleanable {\n+\n+        private final Runnable action;\n+       PhantomCleanable prev = this;\n+       PhantomCleanable next = this;\n+\n+        private final PhantomCleanable list;\n+\n+        public PhantomCleanable(Object referent, Runnable action) {\n+            super(Objects.requireNonNull(referent), queue);\n+            this.list = phantomCleanableList;",
        "comment_created_at": "2025-03-17T09:23:00+00:00",
        "comment_author": "AlexanderSchuetz97",
        "comment_body": "I am not the Author of this code, but I feel qualified to comment anyways.\r\n\r\nThis is the correct way to implement this.\r\n\r\nYou need to ensure that the cleaner itself outlives the resource you want to clean.\r\nThe \"ReferenceQueue\" itself does not do that. Therefore you need a different datastructure like a list or hashmap.\r\nIt needs to be a double linked list or hashmap because you have no idea in what order the elements are to be removed. So you need to support fast removal of elements in the center. Making the cleaners themselves (they know when to be removed) the node in a  list as done here is the canonical way to do it.\r\n\r\nIn the link you posted, which is a short example, the caller ensures that the cleaner reference remains on the stack and thereforce not garbage collected. This approch is fine if you know how many elements you need to clean (in the case of the example that number is 1.) However this is not possible for opencv's case you have no knowledge on how many mat's are create and you also do not want to force ever user of opencv to change their code to also keep the cleaner alive for longer than the mat.",
        "pr_file_module": null
      }
    ]
  }
]
