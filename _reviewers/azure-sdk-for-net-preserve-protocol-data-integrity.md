---
title: Preserve protocol data integrity
description: When working with network protocols (like AMQP, NFS, or SMB), maintain
  the integrity of the original protocol data structures during serialization, deserialization,
  and transformation operations. Modifying protocol-specific data can lead to unintended
  changes in the service contract and unexpected behavior for clients.
repository: Azure/azure-sdk-for-net
label: Networking
language: Markdown
comments_count: 2
repository_stars: 5809
---

When working with network protocols (like AMQP, NFS, or SMB), maintain the integrity of the original protocol data structures during serialization, deserialization, and transformation operations. Modifying protocol-specific data can lead to unintended changes in the service contract and unexpected behavior for clients.

For message-based protocols:
- Avoid mutating the underlying protocol representation when converting to language-specific objects
- Perform type normalization only on your application's representation of the data, not on the protocol layer
- Document how special cases are handled when converting between protocol formats

Example from AMQP handling:
```csharp
// Incorrect: Directly modifying protocol data
amqpMessage.Properties.ContentType = normalizedContentType; // Mutates original AMQP data

// Correct: Keep protocol representation intact, normalize only in your model
EventData eventData = new EventData(amqpMessage);
eventData.ContentType = normalizedContentType; // Only the .NET projection is affected
```

For file transfer protocols:
- Clearly document how specialized elements (like symbolic links, hard links) are handled
- Ensure consistent behavior across different transfer operations
- Preserve protocol-specific properties where possible to maintain compatibility


[
  {
    "discussion_id": "2151028592",
    "pr_number": 50645,
    "pr_file": "sdk/eventhub/Microsoft.Azure.WebJobs.Extensions.EventHubs/CHANGELOG.md",
    "created_at": "2025-06-16T22:56:02+00:00",
    "commented_code": "# Release History\n\n## 6.5.2 (2025-06-12)\n## 6.5.2 (2025-06-16)\n\n### Bugs Fixed\n\n- Fixed a bug where the data types of broker-owned properties were being adjusted when an event was read by the client, causing the underlying AMQP data to be mutated.  This resulted in binary changes when the AMQP message was serialized and unintentionally altered the service contract.  Going forward, the original data types will be preserved on the AMQP representation of the message and type normalization only applied to the .NET `EventData` projection.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2151028592",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50645,
        "pr_file": "sdk/eventhub/Microsoft.Azure.WebJobs.Extensions.EventHubs/CHANGELOG.md",
        "discussion_id": "2151028592",
        "commented_code": "@@ -1,14 +1,16 @@\n # Release History\n \n-## 6.5.2 (2025-06-12)\n+## 6.5.2 (2025-06-16)\n \n ### Bugs Fixed\n \n - Fixed a bug where the data types of broker-owned properties were being adjusted when an event was read by the client, causing the underlying AMQP data to be mutated.  This resulted in binary changes when the AMQP message was serialized and unintentionally altered the service contract.  Going forward, the original data types will be preserved on the AMQP representation of the message and type normalization only applied to the .NET `EventData` projection.\n-\n+ ",
        "comment_created_at": "2025-06-16T22:56:02+00:00",
        "comment_author": "jsquire",
        "comment_body": "```suggestion\r\n\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2124515823",
    "pr_number": 50369,
    "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/CHANGELOG.md",
    "created_at": "2025-06-03T17:43:55+00:00",
    "commented_code": "## 12.2.0-beta.1 (Unreleased)\n\n### Features Added\n- Added support for preserving NFS properties and permissions in ShareFiles and ShareDirectories for Share-to-Share copy transfers.\n- Added support for preserving SMB properties and permissions in ShareDirectories for Share-to-Share copy transfers.\n- For Copy and Download transfers, Hard links are copied as regular files and Symbolic links are skipped.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2124515823",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50369,
        "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/CHANGELOG.md",
        "discussion_id": "2124515823",
        "commented_code": "@@ -3,8 +3,12 @@\n ## 12.2.0-beta.1 (Unreleased)\n \n ### Features Added\n+- Added support for preserving NFS properties and permissions in ShareFiles and ShareDirectories for Share-to-Share copy transfers.\n+- Added support for preserving SMB properties and permissions in ShareDirectories for Share-to-Share copy transfers.\n+- For Copy and Download transfers, Hard links are copied as regular files and Symbolic links are skipped.",
        "comment_created_at": "2025-06-03T17:43:55+00:00",
        "comment_author": "amnguye",
        "comment_body": "I'm not sure if this is where we want to document that hardlinks are supported as regular files and symbolic links are skipped. I think it's better that we add that symbolic links are skipped in the regular documentation or known issues, and not in our changelog, since changelog is what we've changed. Unless we were copying symbolic links initially and now we no longer do.\r\n\r\nI think this should be changed to \"Added support for transferring hard links for downloading Share Files and Share-to-Share copy transfers\"",
        "pr_file_module": null
      },
      {
        "comment_id": "2124596172",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50369,
        "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/CHANGELOG.md",
        "discussion_id": "2124515823",
        "commented_code": "@@ -3,8 +3,12 @@\n ## 12.2.0-beta.1 (Unreleased)\n \n ### Features Added\n+- Added support for preserving NFS properties and permissions in ShareFiles and ShareDirectories for Share-to-Share copy transfers.\n+- Added support for preserving SMB properties and permissions in ShareDirectories for Share-to-Share copy transfers.\n+- For Copy and Download transfers, Hard links are copied as regular files and Symbolic links are skipped.",
        "comment_created_at": "2025-06-03T18:21:10+00:00",
        "comment_author": "nickliu-msft",
        "comment_body": "@amnguye I see your point, my main thing is \"adding support for transferring hard links\" might be a little misleading since we are not actually creating a hardlink in the destination for phase 1 (only copying over as regular file) thus not FULL support. \r\n\r\nAs for softlinks, today if the customer tries to transfer a softlink, the transfer will fail (since you need to resolve the reference). So in phase 1 by skipping, we are kinda changing the behavior. (hardlinks and softlinks are only for NFS so customers should not be doing this today anyways).\r\n\r\nExactly how hard links and soft links are handled is documented already. I think this might be the best for the changelog:\r\n\r\n\"Added basic support for handling hard links and soft links in NFS Share-to-Share copy and Share-to-local download transfers.\"",
        "pr_file_module": null
      }
    ]
  }
]
