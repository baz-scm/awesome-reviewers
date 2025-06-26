---
title: "Benchmark before choosing methods"
description: "Always benchmark different implementation approaches for performance-critical operations before selecting a method. Different approaches (like array operations, string parsing, or data iteration) can have significant performance implications that may not be intuitive."
repository: "fastify/fastify"
label: "Performance Optimization"
language: "JavaScript"
comments_count: 4
repository_stars: 34000
---

Always benchmark different implementation approaches for performance-critical operations before selecting a method. Different approaches (like array operations, string parsing, or data iteration) can have significant performance implications that may not be intuitive.

Example comparing array operations:
```javascript
const Benchmark = require('benchmark')
const suite = new Benchmark.Suite()

suite
  .add('concat', function() {
    return ['cookie'].concat(['cookie2', 'cookie3'])
  })
  .add('push', function() {
    return Array.prototype.push.apply(['cookie'], ['cookie2', 'cookie3'])
  })
  .on('cycle', function(event) {
    console.log(String(event.target))
  })
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'))
  })
  .run()
```

Key considerations:
- Use appropriate sample sizes and realistic test data
- Test in your target environment
- Consider memory implications alongside pure speed
- Document benchmark results to justify implementation choices