---
title: accessibility interaction security
description: Ensure that accessibility features do not create security vulnerabilities
  by allowing unintended interactions or providing misleading information to assistive
  technologies. This includes proper ARIA attribute usage and ensuring hidden or inactive
  elements are truly inaccessible.
repository: mastodon/mastodon
label: Security
language: TSX
comments_count: 2
repository_stars: 48691
---

Ensure that accessibility features do not create security vulnerabilities by allowing unintended interactions or providing misleading information to assistive technologies. This includes proper ARIA attribute usage and ensuring hidden or inactive elements are truly inaccessible.

Key practices:
1. **Choose appropriate ARIA attributes**: Use `aria-describedby` for plain text descriptions and `aria-details` for complex content that requires navigation
2. **Make inactive elements inert**: Use the `inert` attribute on hidden or inactive UI elements (like carousel slides) to prevent screen reader interaction
3. **Test with assistive technologies**: Verify that custom emojis, images, and interactive elements provide appropriate feedback to screen readers

Example of proper implementation:
```tsx
// Good: Inactive carousel slides are made inert
<animated.div
  className='featured-carousel__slide'
  data-index={index}
  inert={index !== slideIndex}
>
  <StatusContainer id={statusId} />
</animated.div>

// Good: Appropriate ARIA attribute for text content
<button
  aria-describedby={descriptionId}
  onClick={onClick}
>
  Show content
</button>
<p id={descriptionId}>{textContent}</p>
```

This prevents accessibility-related security issues where users might inadvertently interact with hidden elements or receive incorrect information through assistive technologies.