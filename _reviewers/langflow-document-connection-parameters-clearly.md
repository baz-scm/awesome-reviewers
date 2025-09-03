---
title: Document connection parameters clearly
description: When documenting network connections (SSH, HTTP, database, etc.), provide
  clear explanations of all connection parameters, their security implications, and
  their relationships. Don't just list placeholders - explain what each parameter
  represents and why it's needed.
repository: langflow-ai/langflow
label: Networking
language: Other
comments_count: 3
repository_stars: 111046
---

When documenting network connections (SSH, HTTP, database, etc.), provide clear explanations of all connection parameters, their security implications, and their relationships. Don't just list placeholders - explain what each parameter represents and why it's needed.

For connection commands, structure parameter explanations as bulleted lists after the command block. Clarify security-sensitive distinctions (like public vs private keys) and include context about how parameters work together in the network protocol.

Example:
```bash
ssh -i PATH_TO_PRIVATE_KEY/PRIVATE_KEY_NAME root@SERVER_IP_ADDRESS
```

Replace the following:
* `PATH_TO_PRIVATE_KEY/PRIVATE_KEY_NAME`: The path to your private SSH key file that matches the public key you added to your server
* `SERVER_IP_ADDRESS`: Your server's IP address

This approach helps developers understand the security model and connection flow, not just the syntax to copy-paste.