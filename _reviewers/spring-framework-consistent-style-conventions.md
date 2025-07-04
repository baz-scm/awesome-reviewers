---
title: Consistent style conventions
description: 'Apply consistent formatting and organization conventions throughout
  the codebase to enhance readability and maintainability:


  1. Follow the project''s `.editorconfig` settings for indentation style (tabs vs
  spaces) and other formatting rules.'
repository: spring-projects/spring-framework
label: Code Style
language: Other
comments_count: 4
repository_stars: 58382
---

Apply consistent formatting and organization conventions throughout the codebase to enhance readability and maintainability:

1. Follow the project's `.editorconfig` settings for indentation style (tabs vs spaces) and other formatting rules.

2. Sort dependencies alphabetically in build scripts:
   ```gradle
   dependencies {
     optional("io.micrometer:context-propagation")
     optional("io.micrometer:micrometer-observation")
     optional("io.projectreactor:reactor-test")
     optional("org.jetbrains.kotlinx:kotlinx-coroutines-core")
     optional("org.jetbrains.kotlinx:kotlinx-coroutines-reactor")
   }
   ```

3. Store stateless implementations as final fields rather than creating getter methods:
   ```java
   // Preferred:
   private final RowMapper<Actor> actorRowMapper = (rs, rowNum) -> {
       Actor actor = new Actor();
       actor.setFirstName(rs.getString("first_name"));
       actor.setLastName(rs.getString("last_name"));
       return actor;
   };
   
   // Not preferred:
   private RowMapper<Actor> getActorMapper() {
       return (rs, rowNum) -> {
           // implementation
       };
   }
   ```

4. Prefer inline lambda expressions for simple operations rather than creating separate variables:
   ```java
   // Preferred:
   jdbcTemplate.update(connection -> {
       PreparedStatement ps = connection.prepareStatement(INSERT_SQL, new String[] { "id" });
       ps.setString(1, name);
       return ps;
   }, keyHolder);
   
   // Not preferred:
   PreparedStatementCreator statementCreator = connection -> {
       // implementation
   };
   jdbcTemplate.update(statementCreator, keyHolder);
   ```