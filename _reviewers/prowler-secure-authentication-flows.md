---
title: Secure authentication flows
description: 'Implement authentication flows that protect sensitive information and
  follow secure credential management practices:


  1. **Prevent domain enumeration attacks** by returning consistent responses regardless
  of whether the input (like domain name) is valid:'
repository: prowler-cloud/prowler
label: Security
language: Markdown
comments_count: 5
repository_stars: 11834
---

Implement authentication flows that protect sensitive information and follow secure credential management practices:

1. **Prevent domain enumeration attacks** by returning consistent responses regardless of whether the input (like domain name) is valid:

```javascript
// INSECURE: Different responses reveal valid domains
if (domainExists) {
  return redirect('/saml_login');
} else {
  return notFound();
}

// SECURE: Consistent responses prevent enumeration
// Always redirect to SAML endpoint, handle invalid domains later
return redirect('/saml_login'); 
// Handle invalid domains in the login page itself
```

2. **Use short-lived credentials** instead of long-term static access keys when possible:
   - For AWS, prefer temporary session tokens or role assumption over permanent API keys
   - Use service principal authentication with appropriate permission scopes
   - Consider identity federation (SSO) where available

3. **Verify tenant identity** in multi-tenant environments to ensure users and applications belong to the same tenant:
   - Validate domains match between service principals and user accounts
   - Use default/primary domains when tenant verification is critical

4. **Use correct environment variables** when implementing authentication:
   - For Azure/M365: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
   - Document security implications and proper usage of authentication methods

These practices help mitigate common authentication vulnerabilities while maintaining proper security boundaries between tenants and users.