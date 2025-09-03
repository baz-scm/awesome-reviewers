---
title: Protect sensitive data
description: 'Always identify and properly protect sensitive data fields in your code.
  Sensitive information includes IP addresses, API keys, authentication tokens, personal
  identification data, and high-privilege credentials. '
repository: lobehub/lobe-chat
label: Security
language: TypeScript
comments_count: 3
repository_stars: 65138
---

Always identify and properly protect sensitive data fields in your code. Sensitive information includes IP addresses, API keys, authentication tokens, personal identification data, and high-privilege credentials. 

Key practices:
- Remove unnecessary sensitive fields from storage (like IP addresses in usage records)
- Encrypt sensitive user data before database storage (API keys, tokens)
- Be aware of sensitive data in external payloads (webhooks, API responses)
- Avoid storing high-privilege credentials like accessKey/accessSecret in plaintext
- Treat personal data (ID cards, phone numbers) as highly confidential

Example of proper sensitive data handling:
```typescript
// Bad: Storing IP address unnecessarily
export const usageRecords = pgTable('usage_records', {
  ipAddress: text('ip_address'), // Remove this sensitive field
});

// Good: Encrypt sensitive user data
const encryptedKeyVaults = encrypt(userKeyVaults); // Encrypt API keys before storage

// Good: Be cautious with webhook data containing sensitive fields
const parsed = JSON.parse(payloadString) as CasdoorWebhookPayload;
// Be aware this may contain accessKey, accessSecret, idCard, etc.
```

Always ask: "Does this field contain sensitive information?" and "How can I minimize exposure while maintaining functionality?"