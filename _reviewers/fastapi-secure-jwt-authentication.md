---
title: Secure JWT authentication
description: 'Implement secure authentication using JWT tokens by following these
  best practices:


  1. **Use secure libraries**: Prefer well-maintained libraries like `PyJWT` for JWT
  handling and `passlib` with bcrypt for password hashing:'
repository: fastapi/fastapi
label: Security
language: Markdown
comments_count: 3
repository_stars: 86871
---

Implement secure authentication using JWT tokens by following these best practices:

1. **Use secure libraries**: Prefer well-maintained libraries like `PyJWT` for JWT handling and `passlib` with bcrypt for password hashing:

```python
from passlib.context import CryptContext
import jwt

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secure-secret-key"  # Generate with: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Functions for security
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    
def get_password_hash(password):
    return pwd_context.hash(password)
    
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

2. **Never store plaintext passwords**: Always hash passwords before storage and compare hashed values during verification.

3. **Set appropriate token expiration**: Balance security with user experience by setting reasonable token expiration times.

4. **Distinguish authentication from authorization**: Authentication verifies user identity while authorization determines their permissions. Implement both correctly.

5. **Configure secure settings**: Avoid security risks in configurations. For example, never use `allow_credentials=True` with `allow_origins=['*']` in CORS settings, as this would allow any third-party origin to access sensitive cookie information.

6. **Protect JWT tokens**: Store tokens securely (HTTP-only cookies or secure client-side storage), validate them on each request, and implement proper token revocation strategies.