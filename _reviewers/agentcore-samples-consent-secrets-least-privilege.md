---
title: Consent, Secrets, Least Privilege
description: 'Agentic systems that can spend money, handle credentials, or call AWS
  APIs must enforce three controls:


  1) **Require explicit user consent before spending or creating payment sessions**'
repository: awslabs/agentcore-samples
label: Security
language: Markdown
comments_count: 3
repository_stars: 3244
---

Agentic systems that can spend money, handle credentials, or call AWS APIs must enforce three controls:

1) **Require explicit user consent before spending or creating payment sessions**
- The agent MUST prompt and receive approval for each session creation.
- The UI/agent must have the user review **budget** and **duration** every time.
- If the system can create sessions without user approval, treat it as a bug.

2) **Keep secrets out of LLM inputs/parameters**
- Do not pass API keys, wallet secrets, or other credentials as tool arguments to the LLM.
- Store credentials in the user’s local environment (e.g., `.env`, which must be gitignored) and load them at execution time.

3) **Use least-privilege permissions in production**
- Demo environments may use broad access, but production must use scoped IAM policies limited to the exact actions/resources the agent needs.

Example (consent gate + env-based secrets):
```ts
// Pseudocode / integration-style example
function shouldCreatePaymentSession(userMessage) {
  // e.g., ask and require a clear yes/no
  return userMessage.includes("I approve") || userMessage.includes("Yes, create it");
}

async function handleUserRequest(agent, req) {
  if (req.action === "create_payment_session") {
    // 1) Always ask for consent; show budget/duration details.
    const userApproved = await agent.askUserForApproval({
      budget: req.budget,
      duration: req.duration,
    });

    if (!userApproved) return { status: "cancelled" };

    // 2) Load secrets locally (not from the LLM conversation).
    //    .env example:
    //    CDP_API_KEY_ID=...
    //    CDP_API_KEY_SECRET=...
    //    CDP_WALLET_SECRET=...
    const cdpApiKeyId = process.env.CDP_API_KEY_ID!;
    const cdpApiKeySecret = process.env.CDP_API_KEY_SECRET!;
    const cdpWalletSecret = process.env.CDP_WALLET_SECRET!;

    // Tool call with secrets handled by the host process.
    return agent.tools.create_payment_session({
      budget: req.budget,
      duration: req.duration,
      // Do NOT include raw secrets in any LLM messages.
      // Secrets stay in the execution environment / secure host config.
    });
  }
}
```

Adopt this as a standard checklist for any tool the agent can invoke that:
- triggers irreversible external side effects (payments, transfers, purchases),
- uses credentials, or
- calls cloud services (where IAM scope matters).