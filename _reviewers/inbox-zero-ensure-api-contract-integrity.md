---
title: Ensure API contract integrity
description: 'Maintain strict consistency between API implementation and contract
  by ensuring:

  1. Request/response schemas match exactly between client and server

  2. All required parameters are validated and documented'
repository: elie222/inbox-zero
label: API
language: TypeScript
comments_count: 4
repository_stars: 8267
---

Maintain strict consistency between API implementation and contract by ensuring:
1. Request/response schemas match exactly between client and server
2. All required parameters are validated and documented
3. HTTP status codes accurately reflect response types
4. OpenAPI documentation stays synchronized with implementation

Example of proper implementation:

```typescript
// API Route implementation
export const POST = withError(async (request: Request) => {
  // 1. Validate request against documented schema
  const body = checkoutSessionSchema.parse(await request.json());
  
  // 2. Return appropriate status codes
  if (!session?.user?.email) {
    return NextResponse.json(
      { error: "Not authenticated" }, 
      { status: 401 }
    );
  }

  // 3. Include all required parameters
  const checkout = await stripe.checkout.sessions.create({
    customer: stripeCustomerId,
    success_url: `${env.NEXT_PUBLIC_BASE_URL}/api/stripe/success`,
    mode: "subscription",
    line_items: [{
      price: env.STRIPE_PRICE_ID,
      quantity: 1
    }]
  });

  return NextResponse.json({ checkout });
});

// OpenAPI documentation
registry.registerPath({
  method: "post",
  path: "/checkout",
  description: "Create checkout session",
  request: {
    body: {
      content: {
        "application/json": {
          schema: checkoutSessionSchema
        }
      }
    }
  },
  responses: {
    200: { description: "Success" },
    401: { description: "Not authenticated" }
  }
});
```

This ensures reliable API behavior, reduces runtime errors, and maintains clear contracts with API consumers.