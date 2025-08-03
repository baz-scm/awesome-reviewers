---
title: Manage database connections
description: 'Always properly manage database connections to prevent resource leaks
  and improve application stability. Implement these key practices:


  1. Release connections back to the pool after use with a try/finally block'
repository: n8n-io/n8n
label: Database
language: TypeScript
comments_count: 5
repository_stars: 122978
---

Always properly manage database connections to prevent resource leaks and improve application stability. Implement these key practices:

1. Release connections back to the pool after use with a try/finally block
2. Implement graceful shutdown for database pools
3. Use connection pooling instead of creating new connections for each request
4. Set appropriate connection pool configuration (size, timeout)

Example:
```typescript
// Connection pool setup with proper configuration
const dbPool = mysql.createPool({
  ...dbConfig,
  connectionLimit: 10,
  queueLimit: 0,
  connectTimeout: 10000,
});

// Function using a connection with proper release
async function queryDatabase() {
  const connection = await dbPool.getConnection();
  try {
    const [results] = await connection.execute('SELECT id, name FROM users WHERE status = ?', ['active']);
    return results;
  } catch (error) {
    console.error('Database query failed:', error);
    throw error;
  } finally {
    // Always release the connection back to the pool
    connection.release();
  }
}

// Graceful shutdown handler
process.on('SIGTERM', async () => {
  console.log('Closing database connections...');
  if (dbPool) {
    await dbPool.end();
    console.log('Database pool closed');
  }
  process.exit(0);
});
```