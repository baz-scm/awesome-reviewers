---
title: optimize test organization
description: 'Organize tests to minimize factory creation, reduce duplication, and
  improve performance by chaining assertions and extracting common values.


  **Key practices:**'
repository: mastodon/mastodon
label: Testing
language: Ruby
comments_count: 4
repository_stars: 48691
---

Organize tests to minimize factory creation, reduce duplication, and improve performance by chaining assertions and extracting common values.

**Key practices:**
- **Chain assertions** to test multiple aspects of the same response instead of creating separate examples
- **Extract repeated values** to private methods or let blocks to reduce duplication
- **Minimize factory creation** by using single examples with multiple change blocks instead of separate examples
- **Use build over create** when database persistence isn't required

**Example:**
```ruby
# Instead of multiple examples creating many factories:
let!(:invite_unlimited) { Fabricate(:invite, user: user, max_uses: nil, created_at: 10.days.ago) }
let!(:invite_huge_max_uses) { Fabricate(:invite, max_uses: 100, created_at: 10.days.ago) }

# Use single example with chained expectations:
it 'processes invites correctly' do
  expect { subject.perform }
    .to change(Invite.where(max_uses: nil), :count).by(-1)
    .and change(Invite.where('max_uses > ?', retention_max_uses), :count).by(-1)
end

# Extract common datetime values:
let(:default_datetime) { DateTime.new(2024, 11, 28, 16, 20, 0) }

# Chain response assertions:
expect(response)
  .to have_http_status(403)
  .and have_content('error message')
```

This approach reduces test execution time, improves maintainability, and makes test intent clearer by grouping related assertions together.