---
title: Config object design clarity
description: 'When designing constructor or configuration APIs, prefer a single, explicit
  options object over positional primitive arguments, since primitives like `new Chalk(false)`
  are ambiguous and hard to extend. Favor `new Chalk({enabled: false})` so the intent
  is self-documenting and new options can be added without breaking the signature.'
repository: chalk/chalk
label: API
language: JavaScript
comments_count: 3
repository_stars: 23342
---

When designing constructor or configuration APIs, prefer a single, explicit options object over positional primitive arguments, since primitives like `new Chalk(false)` are ambiguous and hard to extend. Favor `new Chalk({enabled: false})` so the intent is self-documenting and new options can be added without breaking the signature.

When an API evolves and introduces a new option that overlaps in meaning with an existing one (e.g., adding `level` while keeping `enabled`), avoid storing both as independent state—this allows contradictory inputs like `{level: 0, enabled: true}`. Instead, pick one as the canonical source of truth and expose the other as a derived accessor (getter/setter) that reads/writes through it:

```js
function Chalk(options) {
	options = options || {};
	var level = 'level' in options ? options.level : supportsColor.level;
	this.level = level;
}

Object.defineProperty(Chalk.prototype, 'enabled', {
	get: function () {
		return this.level > 0;
	},
	set: function (value) {
		this.level = value ? (this.level || 1) : 0;
	}
});
```

If conflicting options cannot be reconciled this way, validate the input and throw a clear, well-documented error rather than silently guessing precedence. This keeps the configuration surface predictable, prevents hidden bugs from conflicting flags, and makes backward-compatible aliases safe to maintain.