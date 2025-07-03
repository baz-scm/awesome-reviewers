---
title: Validate performance metrics
description: 'Always validate performance measurements against expected ranges and
  understand hardware limitations. When implementing performance optimization:


  1. **Verify benchmarks produce reasonable metrics** - Be suspicious of numbers that
  seem too good (>90% utilization) or too poor (<10% utilization)'
repository: pytorch/pytorch
label: Performance Optimization
language: Python
comments_count: 8
repository_stars: 91169
---

Always validate performance measurements against expected ranges and understand hardware limitations. When implementing performance optimization:

1. **Verify benchmarks produce reasonable metrics** - Be suspicious of numbers that seem too good (>90% utilization) or too poor (<10% utilization)
2. **Adjust for hardware specifics** - Consider system limitations like clock-rate throttling and adjust metrics accordingly using `current_clock_rate/default_clock_rate`
3. **Optimize profiling code** - Check if operations need profiling at all (e.g., only profile nodes with `flop_counter` registrations)
4. **Consider all performance factors** - Don't prune configurations automatically (like register spilling) without verifying actual impact
5. **Use efficient performance tooling** - Heavy dependencies like Pandas in performance measurement code can introduce significant overhead

Example:
```python
# Before: Running expensive profiling unconditionally
def count_flops_fx(node):
    success, args, kwargs = get_fake_args_kwargs(node)
    if success:
        with FlopCounterMode(display=False) as flop_counter:
            with fake_mode:
                node.target(*args, **kwargs)
        return flop_counter.get_total_flops()
    return 0

# After: Only profile when needed
def count_flops_fx(node):
    # Check if node has flop counter registration before running
    if node.target.__name__ not in flop_registry:
        return 0
    
    success, args, kwargs = get_fake_args_kwargs(node)
    if success:
        with FlopCounterMode(display=False) as flop_counter:
            with fake_mode:
                node.target(*args, **kwargs)
        return flop_counter.get_total_flops()
    return 0
```
