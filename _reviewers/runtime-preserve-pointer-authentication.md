---
title: Preserve pointer authentication
description: When implementing Pointer Authentication (PAC) for security, maintain
  signed pointers throughout their entire lifecycle to prevent potential security
  vulnerabilities. Avoid unnecessarily stripping PAC signatures from pointers that
  will be stored and later reused. This preserves the security guarantees that PAC
  is designed to provide.
repository: dotnet/runtime
label: Security
language: C++
comments_count: 3
repository_stars: 16578
---

When implementing Pointer Authentication (PAC) for security, maintain signed pointers throughout their entire lifecycle to prevent potential security vulnerabilities. Avoid unnecessarily stripping PAC signatures from pointers that will be stored and later reused. This preserves the security guarantees that PAC is designed to provide.

For example, when storing a return address:

```cpp
// AVOID: Stripping signature before storage creates a security hole
m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);

// BETTER: Store the signed pointer to maintain protection
m_pvHJRetAddr = originalSignedPointer;
// Only strip when absolutely necessary for processing
void* strippedForProcessing = PacStripPtr(m_pvHJRetAddr);
```

This approach ensures that any attempt to manipulate the stored address would fail authentication when the pointer is eventually used, significantly reducing the attack surface against return-oriented programming (ROP) attacks. When you do need to strip the signature for processing, limit the scope of the unsigned pointer and avoid storing it in a longer-lived variable or memory location.


[
  {
    "discussion_id": "2040023170",
    "pr_number": 110472,
    "pr_file": "src/coreclr/jit/emitarm64.cpp",
    "created_at": "2025-04-11T17:48:13+00:00",
    "commented_code": "// clang-format on\n\n//------------------------------------------------------------------------\n// emitPacInProlog: Sign LR as part of Pointer Authentication (PAC) support\n//\nvoid emitter::emitPacInProlog()\n{\n    if (JitConfig.JitPacEnabled() == 0)\n    {\n        return;\n    }\n    // TODO-PAC: should be paciasp",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2040023170",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/jit/emitarm64.cpp",
        "discussion_id": "2040023170",
        "commented_code": "@@ -1397,6 +1397,34 @@ static const char * const  bRegNames[] =\n \n // clang-format on\n \n+//------------------------------------------------------------------------\n+// emitPacInProlog: Sign LR as part of Pointer Authentication (PAC) support\n+//\n+void emitter::emitPacInProlog()\n+{\n+    if (JitConfig.JitPacEnabled() == 0)\n+    {\n+        return;\n+    }\n+    // TODO-PAC: should be paciasp",
        "comment_created_at": "2025-04-11T17:48:13+00:00",
        "comment_author": "jkotas",
        "comment_body": "I see that you have `Sign with SP` at the end of the list. I am not sure whether you want to wait with tackling it as the last item. I expect that you will need to revisit and retest number of changes in this PR to make signing with SP work. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2040099788",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/jit/emitarm64.cpp",
        "discussion_id": "2040023170",
        "commented_code": "@@ -1397,6 +1397,34 @@ static const char * const  bRegNames[] =\n \n // clang-format on\n \n+//------------------------------------------------------------------------\n+// emitPacInProlog: Sign LR as part of Pointer Authentication (PAC) support\n+//\n+void emitter::emitPacInProlog()\n+{\n+    if (JitConfig.JitPacEnabled() == 0)\n+    {\n+        return;\n+    }\n+    // TODO-PAC: should be paciasp",
        "comment_created_at": "2025-04-11T18:32:47+00:00",
        "comment_author": "kunalspathak",
        "comment_body": "I agree. I don't think we will do signing with `SP` just yet and will be in future PR once we are confident about the basic PAC working we implemented.",
        "pr_file_module": null
      },
      {
        "comment_id": "2046840604",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/jit/emitarm64.cpp",
        "discussion_id": "2040023170",
        "commented_code": "@@ -1397,6 +1397,34 @@ static const char * const  bRegNames[] =\n \n // clang-format on\n \n+//------------------------------------------------------------------------\n+// emitPacInProlog: Sign LR as part of Pointer Authentication (PAC) support\n+//\n+void emitter::emitPacInProlog()\n+{\n+    if (JitConfig.JitPacEnabled() == 0)\n+    {\n+        return;\n+    }\n+    // TODO-PAC: should be paciasp",
        "comment_created_at": "2025-04-16T12:40:43+00:00",
        "comment_author": "jkotas",
        "comment_body": "Signing return addresses with `SP` is required to deliver on security promise of PAC and it changes how things like hijacking need to be handled. I expect that you will need to redo a large part of change to make it work and then retest everything again. You can certainly do that, but I do not think it is the most efficient way to deliver this feature.",
        "pr_file_module": null
      },
      {
        "comment_id": "2048556820",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/jit/emitarm64.cpp",
        "discussion_id": "2040023170",
        "commented_code": "@@ -1397,6 +1397,34 @@ static const char * const  bRegNames[] =\n \n // clang-format on\n \n+//------------------------------------------------------------------------\n+// emitPacInProlog: Sign LR as part of Pointer Authentication (PAC) support\n+//\n+void emitter::emitPacInProlog()\n+{\n+    if (JitConfig.JitPacEnabled() == 0)\n+    {\n+        return;\n+    }\n+    // TODO-PAC: should be paciasp",
        "comment_created_at": "2025-04-17T09:09:44+00:00",
        "comment_author": "a74nh",
        "comment_body": "First, I'm assuming https://github.com/dotnet/runtime/pull/108561 will be merged into this to give PAC across C++ and C# code.\r\n\r\n> Signing return addresses with `SP` is required to deliver on security promise of PAC and it changes how things like hijacking need to be handled.\r\n\r\nThis depends what we're protecting against. In a full ROP attack an attacker wants to write arbitrary addresses to the stack. They want to use small gadgets, typically one or two instructions followed by a ret, that just achieves a single action (eg add + ret). Attackers build up a library of gadgets, which can then be chained together on the stack, and essentially run their own program.\r\n\r\nBy using signing with zero the attacker cannot write arbitrary addresses to the stack (because they would need to be signed and the attacker has no way to sign arbitrary addresses).\r\n\r\nHowever, signing with 0 allows addresses that have already been signed to be used elsewhere. So, the attacker could regularly scan the stack and build up a collection of signed addresses. These will point to the return points of any functions which have previously been called in the running program. There is definitely the potential for there to be useful gadgets here, for example when the return from a function is then very close to a return. Eg the return from foo here gives a gadget to increment r0 assuming the arbitrary code doesn't do much.\r\n```csharp\r\n .....\r\n foo(...);\r\n ..... arbitrary code ....\r\n return ret+1;\r\n ....\r\n```\r\nBut most return locations won't be of practical use. It's much less likely for there to be enough gadgets to string together enough functionality to do what the hacker wants. Also, the attacker needs to rebuild this list of addresses every time the program is run (as the key changes per process).\r\n\r\nSigning with SP will remove the option to use these return point gadgets.\r\n\r\nThe C++ code will be signed with SP (via #108561). Which means with this PR the attacker is restricted to return point gadgets in C# code only.\r\n\r\nHaving written this out, I've convinced myself there still is a potential for attack when using 0, but, it's very impractical.\r\n\r\n\r\n\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2092097683",
    "pr_number": 110472,
    "pr_file": "src/coreclr/vm/threadsuspend.cpp",
    "created_at": "2025-05-15T23:28:42+00:00",
    "commented_code": "// Remember the place that the return would have gone\n    m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n#if defined(TARGET_ARM64)\n    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2092097683",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/vm/threadsuspend.cpp",
        "discussion_id": "2092097683",
        "commented_code": "@@ -4600,6 +4605,9 @@ void Thread::HijackThread(ExecutionState *esb X86_ARG(ReturnKind returnKind) X86\n \n     // Remember the place that the return would have gone\n     m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n+#if defined(TARGET_ARM64)\n+    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
        "comment_created_at": "2025-05-15T23:28:42+00:00",
        "comment_author": "jkotas",
        "comment_body": "Would it make sense to keep the bits on `m_pvHJRetAddr` unstripped so that the original return address is protected at all times? I think stripping the bits here creates a hole in the protection. Should we strip the bits later when we read `m_pvHJRetAddr` for stackwalking, but not when we use it to store/restore the original return address so that the return address is protected for the whole time?",
        "pr_file_module": null
      },
      {
        "comment_id": "2092838931",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/vm/threadsuspend.cpp",
        "discussion_id": "2092097683",
        "commented_code": "@@ -4600,6 +4605,9 @@ void Thread::HijackThread(ExecutionState *esb X86_ARG(ReturnKind returnKind) X86\n \n     // Remember the place that the return would have gone\n     m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n+#if defined(TARGET_ARM64)\n+    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
        "comment_created_at": "2025-05-16T11:04:47+00:00",
        "comment_author": "SwapnilGaikwad",
        "comment_body": "It's a good idea. Ideally, we should authenticate instead of stripping to ensure that we are returning to a valid return address. I'll check how can we do this.",
        "pr_file_module": null
      },
      {
        "comment_id": "2093035611",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/vm/threadsuspend.cpp",
        "discussion_id": "2092097683",
        "commented_code": "@@ -4600,6 +4605,9 @@ void Thread::HijackThread(ExecutionState *esb X86_ARG(ReturnKind returnKind) X86\n \n     // Remember the place that the return would have gone\n     m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n+#if defined(TARGET_ARM64)\n+    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
        "comment_created_at": "2025-05-16T13:18:32+00:00",
        "comment_author": "jkotas",
        "comment_body": "Once the code actually returns to the restored return address, it is going to authenticate. It should not be necessary to do an extra authentication during hijacking.",
        "pr_file_module": null
      },
      {
        "comment_id": "2093136765",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/vm/threadsuspend.cpp",
        "discussion_id": "2092097683",
        "commented_code": "@@ -4600,6 +4605,9 @@ void Thread::HijackThread(ExecutionState *esb X86_ARG(ReturnKind returnKind) X86\n \n     // Remember the place that the return would have gone\n     m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n+#if defined(TARGET_ARM64)\n+    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
        "comment_created_at": "2025-05-16T14:13:43+00:00",
        "comment_author": "SwapnilGaikwad",
        "comment_body": "I may have misunderstood the workings. My though was - the original address is preserved so that after GC we can return to it, and the updated address would take the execution flow to desired new address, e.g., to do GC. The new address (replaced during hijacking) gets authenticated with the `autiaz` in the epilog. Thus, if someone corrupts the original return address, stripping won't affect it. This can lead the GC would return to the malicious address. We can avoid this by authenticating instead of stripping during hijacking.",
        "pr_file_module": null
      },
      {
        "comment_id": "2094681274",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/vm/threadsuspend.cpp",
        "discussion_id": "2092097683",
        "commented_code": "@@ -4600,6 +4605,9 @@ void Thread::HijackThread(ExecutionState *esb X86_ARG(ReturnKind returnKind) X86\n \n     // Remember the place that the return would have gone\n     m_pvHJRetAddr = *esb->m_ppvRetAddrPtr;\n+#if defined(TARGET_ARM64)\n+    m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);",
        "comment_created_at": "2025-05-19T00:50:21+00:00",
        "comment_author": "jkotas",
        "comment_body": "> the original address is preserved so that after GC we can return to it, and the updated address would take the execution flow to desired new address\r\n\r\nRight. My point is that it would be better to keep the signed address intact through the whole process:\r\n- Delete PacStripPtr in Thread::HijackThread and store the original signed address in m_pvHJRetAddr instead \r\n- Delete PacSignPtr in Thread::UnhijackThread\r\n- Add PacStripPtr as necessary to places that read m_pvHJRetAddr and do not expect the signature in the upper bits\r\n\r\nIt will make the original return address protected while it is stored in m_pvHJRetAddr. As implemented currently, the return address is not protected while it is stored in m_pvHJRetAddr.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2065051966",
    "pr_number": 110472,
    "pr_file": "src/coreclr/nativeaot/Runtime/thread.cpp",
    "created_at": "2025-04-28T23:53:14+00:00",
    "commented_code": "#endif\n\n        *ppvRetAddrLocation = (void*)pfnHijackFunction;\n#if defined(TARGET_ARM64) && defined(__GNUC__)\n        *ppvRetAddrLocation = PacSignPtr(*ppvRetAddrLocation);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2065051966",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/nativeaot/Runtime/thread.cpp",
        "discussion_id": "2065051966",
        "commented_code": "@@ -817,6 +839,9 @@ void Thread::HijackReturnAddressWorker(StackFrameIterator* frameIterator, Hijack\n #endif\n \n         *ppvRetAddrLocation = (void*)pfnHijackFunction;\n+#if defined(TARGET_ARM64) && defined(__GNUC__)\n+        *ppvRetAddrLocation = PacSignPtr(*ppvRetAddrLocation);",
        "comment_created_at": "2025-04-28T23:53:14+00:00",
        "comment_author": "kunalspathak",
        "comment_body": "so what happens when we do not sign the addresses? Do they go back on stack where the attacker can hijack?",
        "pr_file_module": null
      },
      {
        "comment_id": "2065065314",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/nativeaot/Runtime/thread.cpp",
        "discussion_id": "2065051966",
        "commented_code": "@@ -817,6 +839,9 @@ void Thread::HijackReturnAddressWorker(StackFrameIterator* frameIterator, Hijack\n #endif\n \n         *ppvRetAddrLocation = (void*)pfnHijackFunction;\n+#if defined(TARGET_ARM64) && defined(__GNUC__)\n+        *ppvRetAddrLocation = PacSignPtr(*ppvRetAddrLocation);",
        "comment_created_at": "2025-04-28T23:57:01+00:00",
        "comment_author": "kunalspathak",
        "comment_body": "Also, why is it just for `__GNUC__`? should also do it for windows, right? Likewise in `threadsuspend.cpp`",
        "pr_file_module": null
      },
      {
        "comment_id": "2070324857",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110472,
        "pr_file": "src/coreclr/nativeaot/Runtime/thread.cpp",
        "discussion_id": "2065051966",
        "commented_code": "@@ -817,6 +839,9 @@ void Thread::HijackReturnAddressWorker(StackFrameIterator* frameIterator, Hijack\n #endif\n \n         *ppvRetAddrLocation = (void*)pfnHijackFunction;\n+#if defined(TARGET_ARM64) && defined(__GNUC__)\n+        *ppvRetAddrLocation = PacSignPtr(*ppvRetAddrLocation);",
        "comment_created_at": "2025-05-01T14:19:17+00:00",
        "comment_author": "SwapnilGaikwad",
        "comment_body": "> so what happens when we do not sign the addresses? Do they go back on stack where the attacker can hijack?\r\n\r\nThe unsigned return addresses would fail at `autiaz` and the program could never return to the desired address after hijacking.\r\n\r\n> Also, why is it just for `__GNUC__`? should also do it for windows, right? Likewise in `threadsuspend.cpp`\r\n\r\nFixed it!\r\n\r\n",
        "pr_file_module": null
      }
    ]
  }
]
