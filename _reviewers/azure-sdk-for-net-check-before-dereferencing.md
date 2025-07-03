---
title: Check before dereferencing
description: Always verify objects are not null before dereferencing them, particularly
  when using methods that might return null like FirstOrDefault(), LastOrDefault(),
  or 'as' casts. Prevent NullReferenceExceptions by adding explicit null checks before
  accessing members.
repository: Azure/azure-sdk-for-net
label: Null Handling
language: C#
comments_count: 7
repository_stars: 5809
---

Always verify objects are not null before dereferencing them, particularly when using methods that might return null like FirstOrDefault(), LastOrDefault(), or 'as' casts. Prevent NullReferenceExceptions by adding explicit null checks before accessing members.

// Risky code:
var lastContextualParameter = ContextualParameters.LastOrDefault();
if (parameter.Name.Equals(lastContextualParameter, StringComparison.InvariantCultureIgnoreCase))
{
    // This will throw if lastContextualParameter is null
}

// Safe code:
var lastContextualParameter = ContextualParameters.LastOrDefault();
if (lastContextualParameter != null && parameter.Name.Equals(lastContextualParameter, StringComparison.InvariantCultureIgnoreCase))
{
    // Only executes if lastContextualParameter is not null
}

For type conversions, prefer direct casts over 'as' when you expect the type to be present:

// Risky code:
(content.HttpContent as System.Net.Http.MultipartFormDataContent).Add(_dataStream, "file");

// Safe code - option 1 (direct cast):
((System.Net.Http.MultipartFormDataContent)content.HttpContent).Add(_dataStream, "file");

// Safe code - option 2 (explicit check):
var multipartContent = content.HttpContent as System.Net.Http.MultipartFormDataContent;
if (multipartContent != null)
{
    multipartContent.Add(_dataStream, "file");
}

When using LINQ's Single() method, consider using FirstOrDefault() with null checking instead to handle cases where the element might not exist:

// Risky code:
var resource = convenienceMethod.Signature.Parameters
    .Single(p => p.Type.Equals(ResourceData.Type));

// Safe code:
var resource = convenienceMethod.Signature.Parameters
    .FirstOrDefault(p => p.Type.Equals(ResourceData.Type));
if (resource != null)
{
    // Use resource
}
else
{
    // Handle the case where no matching parameter exists
}
