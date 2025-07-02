---
title: Minimize cross-device transfers
description: Data transfers between different compute devices (CPU/host to GPU/accelerator
  and back) can significantly impact performance in heterogeneous computing environments.
  Each transfer introduces latency and can block computation pipelines. Pay special
  attention to round-trip patterns where data moves from device A to B and back to
  A, as these create...
repository: tensorflow/swift
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 6136
---

Data transfers between different compute devices (CPU/host to GPU/accelerator and back) can significantly impact performance in heterogeneous computing environments. Each transfer introduces latency and can block computation pipelines. Pay special attention to round-trip patterns where data moves from device A to B and back to A, as these create synchronization points that stall execution.

For optimal performance:
1. Minimize data movement between host and accelerator during performance-critical sections
2. Batch transfers when possible rather than transferring small pieces repeatedly
3. Be especially wary of transfers inside loops that can repeatedly block computation

Watch for problematic patterns like this:
```
for step in 0...1000 {
  let gradients = ... // on accelerator
  weights += gradients // on accelerator
  if cpuOnlyFunc(weights) == 0 { // forces data transfer to CPU and back
    weights += 1 // continues on accelerator after blocking
  }
}
```

When designing APIs that operate across device boundaries, consider providing asynchronous alternatives that allow computation to continue without blocking while transfers occur in the background.


[
  {
    "discussion_id": "209472344",
    "pr_number": 55,
    "pr_file": "proposals/ImplicitCopyWarnings.md",
    "created_at": "2018-08-13T00:04:50+00:00",
    "commented_code": "# Implicit Copy Warning Improvements\n\n* Author: [Marc Rasi](https://github.com/marcrasi)\n\n## Introduction\n\nCurrently, implicit copy warnings are very noisy. For example, [this simple\nmodel] produces [these warnings]. (See the \"Performance Predictability\" section\nof [Graph Program Extraction] for more information about implicit copy\nwarnings).\n\nI propose that we clean up the warnings as follows:\n1. Emit no warnings for data transferred while the program is starting (e.g.\n   training data being copied to the GPU) or ending (e.g. final weights being\n   copied to the CPU).\n2. Within the program, only warn when data makes a round trip between devices:\n   when a piece of data moves from device A to device B, then a computation\n   using that data happens on device B, and then the result of that computation\n   moves back to device A.\n\nConcretely, this proposal eliminates all warnings in [the example].\n\nSince the round-trip-rule might be hard to implement, I also propose that we\ninitially implement a simple heuristic that approximates the round-trip-rule:\nWarn for all transfers from the host to the accelerator, but do not warn for any\ntransfers from the accelerator to the host.",
    "repo_full_name": "tensorflow/swift",
    "discussion_comments": [
      {
        "comment_id": "209472344",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209472344",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.\n+   training data being copied to the GPU) or ending (e.g. final weights being\n+   copied to the CPU).\n+2. Within the program, only warn when data makes a round trip between devices:\n+   when a piece of data moves from device A to device B, then a computation\n+   using that data happens on device B, and then the result of that computation\n+   moves back to device A.\n+\n+Concretely, this proposal eliminates all warnings in [the example].\n+\n+Since the round-trip-rule might be hard to implement, I also propose that we\n+initially implement a simple heuristic that approximates the round-trip-rule:\n+Warn for all transfers from the host to the accelerator, but do not warn for any\n+transfers from the accelerator to the host.",
        "comment_created_at": "2018-08-13T00:04:50+00:00",
        "comment_author": "mhong",
        "comment_body": "arguably warning only on swift->tf transfers can stand on its own right, rather than serving as an approximation due to impl-level convenience. e.g. say swift is running along side TF, and will send various tensors from swift to TF when these tensors are produced -- even without round-trips, such sends can slow down TF, if swift is being slow in producing these tensors.",
        "pr_file_module": null
      },
      {
        "comment_id": "209682817",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209472344",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.\n+   training data being copied to the GPU) or ending (e.g. final weights being\n+   copied to the CPU).\n+2. Within the program, only warn when data makes a round trip between devices:\n+   when a piece of data moves from device A to device B, then a computation\n+   using that data happens on device B, and then the result of that computation\n+   moves back to device A.\n+\n+Concretely, this proposal eliminates all warnings in [the example].\n+\n+Since the round-trip-rule might be hard to implement, I also propose that we\n+initially implement a simple heuristic that approximates the round-trip-rule:\n+Warn for all transfers from the host to the accelerator, but do not warn for any\n+transfers from the accelerator to the host.",
        "comment_created_at": "2018-08-13T16:53:53+00:00",
        "comment_author": "marcrasi",
        "comment_body": "I see this as similar to the tf->swift transfer case -- there are a lot of situations where the user does expect the transfers to happen and where the transfers don't slow anything down. For example, scalar transfers for control flow. Or some kind of CPU loading & preprocessing step that queues up a bunch of training data for the accelerator.\r\n\r\nThinking through scalars is what made me come up with the \"round trip\" idea. We can suppress all scalar warnings, like we do now, but this creates a possibly-bad situation in combination with suppressing tf->swift transfers: what if your program does a really slow tf->swift transfer and then sends it back as a scalar? Something like this:\r\n```\r\nfor step in 0...1000 {\r\n  let gradients = ... // on accelerator\r\n  weights += gradients // on accelerator\r\n  if cpuOnlyFunc(weights) == 0 { // long round-trip transfer that blocks the computation\r\n    weights += 1\r\n  }\r\n}\r\n```\r\n\r\nIf we hide all warnings for scalar transfers and we hide all warnings for tf->swift transfers, then that compiles without warnings. A \"round trip\" rule would catch it though.",
        "pr_file_module": null
      },
      {
        "comment_id": "209813568",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209472344",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.\n+   training data being copied to the GPU) or ending (e.g. final weights being\n+   copied to the CPU).\n+2. Within the program, only warn when data makes a round trip between devices:\n+   when a piece of data moves from device A to device B, then a computation\n+   using that data happens on device B, and then the result of that computation\n+   moves back to device A.\n+\n+Concretely, this proposal eliminates all warnings in [the example].\n+\n+Since the round-trip-rule might be hard to implement, I also propose that we\n+initially implement a simple heuristic that approximates the round-trip-rule:\n+Warn for all transfers from the host to the accelerator, but do not warn for any\n+transfers from the accelerator to the host.",
        "comment_created_at": "2018-08-14T02:31:00+00:00",
        "comment_author": "mhong",
        "comment_body": "If a tf-swift transfer is really slow, it might stall TF compute (due to limited TF RAM buffering) already, without involving a round-trip. :)\r\n\r\nOverall what compiler can warn based on static analysis has limited accuracy, so we might as well go with a fairly simple (explainable / predictible to end users) model. Round-trip involves somewhat more mental calculation than saying \"we warn on all host->tf transfers, other than scalar ones, but that's _still_ just an approximation\". :)\r\n\r\nBut my position is based on some speculation and is just my opinion. I'll let you decide here.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "209473904",
    "pr_number": 55,
    "pr_file": "proposals/ImplicitCopyWarnings.md",
    "created_at": "2018-08-13T00:34:20+00:00",
    "commented_code": "# Implicit Copy Warning Improvements\n\n* Author: [Marc Rasi](https://github.com/marcrasi)\n\n## Introduction\n\nCurrently, implicit copy warnings are very noisy. For example, [this simple\nmodel] produces [these warnings]. (See the \"Performance Predictability\" section\nof [Graph Program Extraction] for more information about implicit copy\nwarnings).\n\nI propose that we clean up the warnings as follows:\n1. Emit no warnings for data transferred while the program is starting (e.g.",
    "repo_full_name": "tensorflow/swift",
    "discussion_comments": [
      {
        "comment_id": "209473904",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209473904",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.",
        "comment_created_at": "2018-08-13T00:34:20+00:00",
        "comment_author": "mhong",
        "comment_body": "agree #1 is a good idea, but how do we implement it (how do we tell whether a swift->tf data transfer happens _before_ the TF graph runs)?\r\n\r\nCurrently our use of \"input args\" and \"result tensors\" of the TF program serve the purpose of differentiating themselves from the sends/recvs, and thus generate no warning.\r\n\r\nIf we convert the input args and result tensors into tensor sends/recvs, i'm not sure how to reliably tell them apart from those other sends/revs that are happening _while_ the tf program is running.\r\n\r\nAlso, if swift is being too slow sending the first tensor to tf, it'd still increase the end-to-end running time, and it might be useful to warn in that case (if possible).",
        "pr_file_module": null
      },
      {
        "comment_id": "209684742",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209473904",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.",
        "comment_created_at": "2018-08-13T16:59:50+00:00",
        "comment_author": "marcrasi",
        "comment_body": "I wanted to capture the current use of \"input args\" and \"result tensors\" in this rule, because it seems like part of the big picture.\r\n\r\nAlso it seems like they currently might be bugged in some way because a lot of the warnings in the example look like they should be input args or result tensors. So a big part of cleaning up the warnings might be debugging those.\r\n\r\nAre we planning to eventually remove input args and result tensors and replace them with send/recv? If we do that, could we keep the logic that currently creates input args and result tensors, and use it to decide whether to warn?",
        "pr_file_module": null
      },
      {
        "comment_id": "209814328",
        "repo_full_name": "tensorflow/swift",
        "pr_number": 55,
        "pr_file": "proposals/ImplicitCopyWarnings.md",
        "discussion_id": "209473904",
        "commented_code": "@@ -0,0 +1,144 @@\n+# Implicit Copy Warning Improvements\n+\n+* Author: [Marc Rasi](https://github.com/marcrasi)\n+\n+## Introduction\n+\n+Currently, implicit copy warnings are very noisy. For example, [this simple\n+model] produces [these warnings]. (See the \"Performance Predictability\" section\n+of [Graph Program Extraction] for more information about implicit copy\n+warnings).\n+\n+I propose that we clean up the warnings as follows:\n+1. Emit no warnings for data transferred while the program is starting (e.g.",
        "comment_created_at": "2018-08-14T02:38:20+00:00",
        "comment_author": "mhong",
        "comment_body": "> Also it seems like they currently might be bugged in some way because a lot of the warnings in the example look like they should be input args or result tensors. So a big part of cleaning up the warnings might be debugging those.\r\n\r\nSGTM.\r\n\r\n> Are we planning to eventually remove input args and result tensors and replace them with send/recv? If we do that, could we keep the logic that currently creates input args and result tensors, and use it to decide whether to warn?\r\n\r\nI think that direction is worth exploration, but it's too early to commit to that. If we do go there, I agree that should probably not affect our warnings policy.",
        "pr_file_module": null
      }
    ]
  }
]
