---
title: Cypress test isolation
description: Ensure end-to-end tests are properly isolated and follow best practices
  for reliability. Tests should avoid side effects that can impact other tests and
  eliminate practices that cause flaky results.
repository: appwrite/appwrite
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 51959
---

Ensure end-to-end tests are properly isolated and follow best practices for reliability. Tests should avoid side effects that can impact other tests and eliminate practices that cause flaky results.

**Key practices:**

1. **Avoid fixed waits:**
   ```javascript
   // ❌ Bad: Makes tests slow and potentially flaky
   cy.get('.element').click();
   cy.wait(1000);
   
   // ✅ Good: Cypress automatically waits for elements
   cy.get('.element').click();
   cy.get('.result').should('be.visible');
   ```

2. **Extract common setup code:**
   ```javascript
   // ❌ Bad: Repeating login flow in every test
   it('Test one', () => {
     cy.visit('/login');
     cy.get('#email').type('user@example.com');
     cy.get('#password').type('password');
     cy.get('button').contains('Sign in').click();
     // Test-specific code
   });
   
   // ✅ Good: Using beforeEach for common setup
   beforeEach(() => {
     cy.login('user@example.com', 'password');
   });
   
   it('Test one', () => {
     // Test-specific code only
   });
   ```

3. **Clean up test-created resources:**
   ```javascript
   // ❌ Bad: Files persist between test runs
   it('writes to a file', () => {
     cy.writeFile('cypress/fixtures/users.json', data);
   });
   
   // ✅ Good: Clean up after tests
   it('writes to a file', () => {
     cy.writeFile('cypress/fixtures/users.json', data);
   });
   
   after(() => {
     cy.task('deleteFile', 'cypress/fixtures/users.json');
   });
   ```

4. **Restore modified configurations:**
   ```javascript
   // ❌ Bad: Changes affect other tests
   it('changes timeout', () => {
     Cypress.config('pageLoadTimeout', 20000);
     // Test code
   });
   
   // ✅ Good: Save and restore original config
   it('changes timeout', () => {
     const originalTimeout = Cypress.config('pageLoadTimeout');
     Cypress.config('pageLoadTimeout', 20000);
     // Test code
     Cypress.config('pageLoadTimeout', originalTimeout);
   });
   ```

Following these practices helps create a reliable test suite that provides consistent results regardless of which tests are run or in what order.