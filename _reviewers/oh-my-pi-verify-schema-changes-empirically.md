---
title: Verify schema changes empirically
description: Treat every index, upsert, or trigger change as unproven until you show,
  with evidence, that it does what it's meant to. For a new index, run EXPLAIN QUERY
  PLAN against the query it's supposed to help and confirm the planner actually picks
  it — an index SQLite never selects (e.g. a composite like `idx_edges_type_source_target`
  superseded by a UNIQUE...
repository: can1357/oh-my-pi
label: Database
language: TypeScript
comments_count: 6
repository_stars: 37317
---

Treat every index, upsert, or trigger change as unproven until you show, with evidence, that it does what it's meant to. For a new index, run EXPLAIN QUERY PLAN against the query it's supposed to help and confirm the planner actually picks it — an index SQLite never selects (e.g. a composite like `idx_edges_type_source_target` superseded by a UNIQUE autoindex, or `LOWER(subject)`/`LOWER(object)` indexes with no matching query) only adds write cost and should be dropped or tied to a real query path. Keep one authoritative definition per table/index set; don't let the same `CREATE TABLE`/index DDL live in two files (e.g. duplicated `graph_edges` setup in both `episodic-graph.ts` and `beam/schema.ts`), since that invites drift and breaks invariants other code relies on (like "this table only exists once X has initialized"). When converting an insert to `INSERT ... ON CONFLICT DO UPDATE`, audit every dependent structure: external-content FTS tables need UPDATE triggers in addition to INSERT/DELETE, or re-stored rows go stale in search while still matching old content. Also verify the conflict resolution can't regress data — an "idempotent" upsert that unconditionally does `DO UPDATE SET content = excluded.content` can overwrite newer rows with stale ones on a re-run; guard with `DO NOTHING` or a `WHERE excluded.updated_at > table.updated_at` condition instead of blind replacement. Finally, remove computed columns or duplicate queries that nothing consumes (e.g. a `COUNT(...)` aggregate column computed but never read because the same value is fetched by a separate query) — wire it into the one path that needs it and delete the redundant computation. In short: don't merge a database change on the strength of what it's "supposed to" do — show the plan, the trigger coverage, and the conflict behavior that prove it.