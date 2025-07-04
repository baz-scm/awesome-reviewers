---
title: Promote code clarity
description: 'Write code that prioritizes clarity and maintainability over brevity.
  This involves several key practices:


  1. **Extract repeated code blocks into helper functions**'
repository: influxdata/influxdb
label: Code Style
language: Rust
comments_count: 8
repository_stars: 30268
---

Write code that prioritizes clarity and maintainability over brevity. This involves several key practices:

1. **Extract repeated code blocks into helper functions**
   When code is used in multiple places, move it to a dedicated function with a descriptive name:

   ```rust
   // Instead of repeating this logic:
   if let Some(path) = output_file_path {
       let mut f = OpenOptions::new()
           .write(true)
           .create(true)
           .truncate(true)
           .open(path)
           .await?;
       f.write_all_buf(&mut bs).await?;
   } else {
       if output_format.is_parquet() {
           Err(Error::NoOutputFileForParquet)?
       }
       println!("{}", String::from_utf8(bs.as_ref().to_vec()).unwrap());
   }

   // Create a helper function:
   async fn write_output(bs: &mut Bytes, output_format: &OutputFormat, output_path: &Option<PathBuf>) -> Result<()> {
       // ... same logic here ...
   }
   ```

2. **Use constants for hardcoded values**
   Replace magic strings and numbers with named constants:

   ```rust
   // Instead of:
   let python_exe = if cfg!(target_os = "windows") { /* ... */ }
   
   // Use:
   const PYTHON_EXECUTABLE: &str = "python3";
   const PYTHON_EXECUTABLE_WINDOWS: &str = "python";
   
   let python_exe = if cfg!(target_os = "windows") {
       PYTHON_EXECUTABLE_WINDOWS
   } else {
       PYTHON_EXECUTABLE
   };
   ```

3. **Design clear function interfaces**
   Use descriptive parameter names and separate compound parameters when clarity is improved:

   ```rust
   // Instead of:
   async fn cleanup_after_snapshot(&self, cleanup_after_snapshot: Option<(oneshot::Receiver<SnapshotDetails>, SnapshotInfo, OwnedSemaphorePermit)>)

   // Use:
   async fn cleanup_after_snapshot(
       &self,
       snapshot_finished_receiver: oneshot::Receiver<SnapshotDetails>,
       snapshot_info: SnapshotInfo,
       snapshot_permit: OwnedSemaphorePermit,
   )
   ```

4. **Respect encapsulation**
   Create proper accessor methods rather than exposing internals:

   ```rust
   // Instead of:
   let triggers = result.catalog().inner().read().triggers();

   // Add a method to Catalog:
   impl Catalog {
       pub fn triggers(&self) -> Vec<Trigger> {
           self.inner().read().triggers()
       }
   }
   // Then use:
   let triggers = result.catalog().triggers();
   ```

5. **Use clear destructuring**
   Simplify complex destructuring to improve readability:

   ```rust
   // Instead of:
   let Self { data, meta } = self;
   let ObjectMeta {
       location,
       last_modified: _,
       size: _,
       e_tag,
       version,
   } = meta;
   
   // Use:
   let Self { 
       data, 
       meta: ObjectMeta {
           location,
           last_modified: _,
           size: _,
           e_tag,
           version,
       }
   } = self;
   ```

6. **Organize code logically**
   Group related functionality into modules and keep single-purpose code in dedicated files.

By consistently applying these practices, code becomes more readable, maintainable, and less prone to errors.