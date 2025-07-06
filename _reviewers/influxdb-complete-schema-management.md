---
title: Complete schema management
description: When working with database systems that have flexible schemas (like InfluxDB),
  ensure complete schema discovery and proper merging from all data sources before
  processing operations. Incomplete schema handling leads to missing columns, data
  corruption, or export failures.
repository: influxdata/influxdb
label: Database
language: Go
comments_count: 3
repository_stars: 30268
---

When working with database systems that have flexible schemas (like InfluxDB), ensure complete schema discovery and proper merging from all data sources before processing operations. Incomplete schema handling leads to missing columns, data corruption, or export failures.

To properly handle schemas:

1. Gather the complete schema by examining all relevant series or records
2. Merge schemas (tags and fields) from all sources to create a comprehensive union schema
3. Use efficient APIs for schema discovery rather than inferring from data scans
4. Remember that schemas can change within files or between series

For example, in InfluxDB, instead of assuming schema consistency:

```go
// Efficiently gather schema using existing indices
tagKeys, err := e.tsdbStore.TagKeys(context.Background(), query.OpenAuthorizer, []uint64{shard.ID()}, cond)
fields := shard.MeasurementFields([]byte("<measurement name>"))

// When processing mixed tag sets, merge schemas properly:
allTagKeys := make(map[string]struct{})
allFields := make(map[string]influxql.DataType)

// Iterate through all series to build complete schema
for seriesKey, fieldValues := range data {
    tags := models.ParseTags([]byte(seriesKey))
    
    // Add all tags to the complete schema
    for _, tag := range tags {
        allTagKeys[string(tag.Key)] = struct{}{}
    }
    
    // Add all fields to the complete schema
    for fieldName, values := range fieldValues {
        allFields[fieldName] = values[0].Type()
    }
}
```

This approach ensures data integrity when schema varies across records, producing complete and accurate results for queries, exports, and other database operations.