```gherkin
Feature: User Authentication
  As an employee of the organization
  I want to authenticate securely into the OrangeHRM system
  So that I can access my HR information and perform work-related tasks

  Background:
    Given I am on the login page
    And the login form is displayed in a centered white box on a colored background

  Scenario: Successful login with valid credentials
    When I enter my registered username "test.employee" into the username field
    And I enter my correct password "securePassword123" into the password field
    And I click the Login button
    Then I should be redirected to the Dashboard page
    And I should have access to HR functions like attendance, leave, and payroll

  Scenario: Failed login due to incorrect password
    When I enter my registered username "test.employee" into the username field
    And I enter an incorrect password "wrongPassword" into the password field
    And I click the Login button
    Then I should see an error message "Invalid credentials"
    And the username field should remain populated with "test.employee"
    And I should remain on the login page

  Scenario: Login attempt with empty username
    When I leave the username field empty
    And I enter a password "somePassword" into the password field
    And I click the Login button
    Then I should see a validation error "Username is required"
    And the form should not be submitted

  Scenario: Login attempt with empty password
    When I enter a username "test.employee" into the username field
    And I leave the password field empty
    And I click the Login button
    Then I should see a validation error "Password is required"
    And the form should not be submitted

  Scenario: Toggle password visibility
    When I enter a password "mySecretPassword" into the password field
    And I click the password visibility toggle icon
    Then the password characters should become visible as plain text
    When I click the password visibility toggle icon again
    Then the password characters should be masked

  Scenario: Mobile responsive layout
    Given I am viewing the login page on a mobile device
    Then I should see the mobile-specific OrangeHRM logo
    And the login form elements should be stacked vertically
    And all functionality should work identically to desktop

  Scenario: Language change functionality
    When I select "Spanish" from the language selector dropdown
    Then the page should reload with all text translated to Spanish
    And the login form labels should be in Spanish
    And the Login button should display "Iniciar Sesión"

  Scenario: Network failure during login
    When I enter valid credentials "test.employee" and "securePassword123"
    And the network connection fails after clicking Login
    Then I should see a connection error message "Unable to connect, please try again"
    And my entered credentials should be retained in the form

  Scenario: JavaScript disabled warning
    Given JavaScript is disabled in my browser
    When I load the login page
    Then I should see a noscript warning message
    And the warning should inform me that JavaScript is required

  Scenario: Rapid failed login attempts trigger security measures
    When I attempt to login with incorrect credentials 5 times within 2 minutes
    Then I should see a rate limiting message or captcha challenge
    And further login attempts should be temporarily blocked

  Scenario: Brand identity confirmation
    When I view the login page
    Then I should see the company branding image at the top of the login box
    And I should see the OrangeHRM logo
    And this should reinforce that I am on the legitimate corporate system

  Scenario: Form clearance and reset
    When I enter "test.user" into the username field
    And I enter "password123" into the password field
    And I refresh the page
    Then both username and password fields should be empty
    And any previous error messages should be cleared

  Scenario: Login via keyboard shortcut
    When I enter valid credentials "test.employee" and "securePassword123"
    And I press the Enter key while focused on a form field
    Then I should be redirected to the Dashboard page
    And the login should be successful

  Scenario: International character support
    When I enter a username with international characters "用户123"
    And I enter a password with special characters "P@sswörd!"
    And I click the Login button
    Then the system should handle the Unicode characters properly
    And authentication should proceed normally

  Scenario: Session continuity after login
    Given I was redirected to login after trying to access a protected page "/leave/request"
    When I successfully login with valid credentials
    Then I should be redirected to "/leave/request" instead of the default dashboard
    And my session should be established correctly
```

```gherkin
Feature: Login Form Security and Validation
  As a system security administrator
  I want the login form to handle edge cases and security threats appropriately
  So that the organization's HR data remains protected from unauthorized access

  Background:
    Given I am on the login page
    And the login form is ready for interaction

  Scenario: Input length validation for username
    When I enter a username exceeding 255 characters into the username field
    And I click the Login button
    Then I should see a validation error "Username too long"
    Or the input should be truncated to the maximum allowed length

  Scenario: SQL injection attempt handling
    When I enter a SQL injection attempt "admin' OR '1'='1" into the username field
    And I enter any password "test123"
    And I click the Login button
    Then I should see a generic error message "Invalid credentials"
    And the system should not reveal any database structure information

  Scenario: XSS attack attempt handling
    When I enter a script tag "<script>alert('xss')</script>" into the username field
    And I enter a password "test123"
    And I click the Login button
    Then I should see a generic error message "Invalid credentials"
    And no JavaScript should be executed from the input

  Scenario: Case sensitivity consistency
    Given a user account with username "Test.Employee"
    When I enter "test.employee" (lowercase) into the username field
    And I enter the correct password
    And I click the Login button
    Then the authentication should either consistently succeed or fail based on system policy
    And the error message should not hint at case sensitivity rules

  Scenario: Autocomplete behavior
    When I view the password field
    Then it should have autocomplete attribute set to "current-password"
    And the browser should be able to suggest password autofill appropriately

  Scenario: Session timeout handling
    Given I successfully logged in
    And my session expires due to inactivity
    When I try to access a protected page
    Then I should be redirected to the login page
    And I should see a "Session expired" notification message

  Scenario: Right-to-left language layout
    When I select Arabic from the language selector
    Then the page should reload with right-to-left text direction
    And all form elements should be properly aligned for RTL display
    And the login functionality should work correctly

  Scenario: Browser back button behavior after login
    Given I successfully logged in and reached the dashboard
    When I click the browser back button
    Then I should not be returned to the login page with my credentials exposed
    And I should remain authenticated in the system

  Scenario: Password field security
    When I type in the password field
    Then the characters should be masked by default
    And the password value should not be exposed in page source or DOM
```

These feature files provide comprehensive coverage of the login functionality including:
- Positive authentication flows
- Validation and error handling
- Security considerations
- Internationalization support
- Edge cases and error conditions
- Mobile responsiveness
- User experience aspects

The scenarios are written following BDD best practices with clear, testable steps that can be directly implemented as automated tests.