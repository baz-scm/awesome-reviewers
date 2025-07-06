---
title: Optimize algorithmic complexity
description: Always consider the time and space complexity implications of your code.
  Choose data structures and algorithms that minimize computational overhead and memory
  usage for your specific use cases.
repository: tokio-rs/tokio
label: Algorithms
language: Rust
comments_count: 8
repository_stars: 28989
---

Always consider the time and space complexity implications of your code. Choose data structures and algorithms that minimize computational overhead and memory usage for your specific use cases.

**Watch for hidden complexity issues:**

1. **Avoid nested iterations that create O(n²) behavior**
   
   ```rust
   // Poor: Iterates through all buffers on each call, potentially O(n²) in a loop
   let n = bufs.iter().map(|b| b.len()).sum::<usize>().min(MAX_BUF);
   
   // Better: Calculate incrementally inside a loop to maintain O(n) complexity
   let mut remaining = MAX_BUF;
   let mut total = 0;
   for buf in bufs {
       let to_copy = buf.len().min(remaining);
       total += to_copy;
       remaining -= to_copy;
       if remaining == 0 {
           break;
       }
   }
   ```

2. **Choose efficient operations over expensive ones**
   
   ```rust
   // Poor: Using power operation which is more expensive
   let max_number = 2u64.saturating_pow((8 * length_field_len - 1) as u32);
   
   // Better: Using bit shift which is much faster
   let max_number = match 1.checked_shl(8 * length_field_len) {
       Some(shl) => shl - 1,
       None => u64::MAX,
   };
   ```

3. **Design for fairness when consuming from multiple sources**
   
   ```rust
   // When polling multiple streams, implement rotation strategies to ensure 
   // fair processing and prevent starvation:
   let mut added = 0;
   let mut start = thread_rng_n(entries.len() as u32) as usize;
   
   while added < limit {
       match self.poll_one(cx, start) {
           Poll::Ready(Some((idx, val))) => {
               added += 1;
               // Move the start index to ensure fair rotation
               start = idx.wrapping_add(1) % entries.len();
               // Process val...
           }
           _ => break,
       }
   }
   ```

4. **Use iterators over index-based access when appropriate**
   
   ```rust
   // Poor: Using index-based access in a loop
   let expiration_time = (0..wheel_count)
       .filter_map(|id| wheel.get_sharded_wheel_mut(id).next_expiration_time())
       .min();
   
   // Better: Using iterator methods directly on the collection
   let expiration_time = wheels.iter_mut()
       .filter_map(|wheel| wheel.next_expiration_time())
       .min();
   ```

5. **Avoid code duplication that leads to excessive monomorphization**

   ```rust
   // Poor: Duplicating implementation for each function call type
   pub fn with_func1(cmd: &mut Cmd, with: impl Fn(&mut Cmd) -> Result<Child>) -> Result<Child> {
       // Duplicated implementation
   }
   
   // Better: Extract common logic to avoid recompiling the same code
   pub fn with_func(cmd: &mut Cmd, with: impl Fn(&mut Cmd) -> Result<Child>) -> Result<Child> {
       handle_common(&mut with(cmd)?)
   }
   
   fn handle_common(child: &mut Child) -> Result<Child> {
       // Common implementation that won't be duplicated
   }
   ```

By paying attention to these efficiency concerns, you'll produce code that scales better and uses resources more efficiently.