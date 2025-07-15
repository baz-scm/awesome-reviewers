---
title: Use unique password salts
description: When implementing password hashing, always use unique, randomly generated
  salts for each user. Using constant or shared salts significantly reduces security
  by allowing identical passwords to produce identical hashes, making them vulnerable
  to rainbow table attacks.
repository: expressjs/express
label: Security
language: JavaScript
comments_count: 1
repository_stars: 67300
---

When implementing password hashing, always use unique, randomly generated salts for each user. Using constant or shared salts significantly reduces security by allowing identical passwords to produce identical hashes, making them vulnerable to rainbow table attacks.

Modern hashing libraries like bcrypt handle salt generation automatically. Instead of manually managing salts:

```javascript
// AVOID: Using fixed salt values
var encryPassword = bcrypt.hashSync('foobar', 10); // '10' is not a salt but work factor

// RECOMMENDED: Let bcrypt generate and manage unique salts
const hashedPassword = bcrypt.hashSync('foobar', bcrypt.genSaltSync(10));
// Or with promises
const hashedPassword = await bcrypt.hash('foobar', 10);
```

When verifying passwords, bcrypt automatically handles salt extraction from the stored hash, so no separate salt storage is needed:

```javascript
// Verification is simple
const isMatch = bcrypt.compareSync('foobar', hashedPassword);
// Or with promises
const isMatch = await bcrypt.compare('foobar', hashedPassword);
```

The work factor (10 in the examples) determines the computational complexity and should be adjusted based on your server's performance capabilities.