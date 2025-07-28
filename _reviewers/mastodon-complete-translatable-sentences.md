---
title: Complete translatable sentences
description: Use complete sentences in translatable strings rather than breaking them
  into fragments, even if this results in some repetition. Sentence fragments make
  translation difficult or impossible for languages with different grammatical structures,
  and they provide insufficient context for translators.
repository: mastodon/mastodon
label: Documentation
language: TSX
comments_count: 3
repository_stars: 48691
---

Use complete sentences in translatable strings rather than breaking them into fragments, even if this results in some repetition. Sentence fragments make translation difficult or impossible for languages with different grammatical structures, and they provide insufficient context for translators.

When you need rich formatting within translatable text, use placeholder-based approaches with complete sentences rather than splitting the text:

```jsx
// Avoid: Breaking sentences into fragments
<div className='label'>
  <FormattedMessage
    id='report.percentile.top'
    defaultMessage='That puts you in the top'
  />
</div>
<div className='number'>{percentage}</div>
<div className='label'>
  <FormattedMessage
    id='report.percentile.users'
    defaultMessage='of Mastodon users.'
  />
</div>

// Prefer: Complete sentence with rich formatting
<FormattedMessage
  id='report.percentile.complete'
  defaultMessage='<label>That puts you in the top</label><percentage /><label>of Mastodon users.</label>'
  values={{
    label: (text) => <div className='label'>{text}</div>,
    percentage: () => <div className='number'>{percentage}</div>,
  }}
/>
```

This approach gives translators full context and flexibility to restructure the sentence according to their language's grammar while maintaining the desired visual formatting.