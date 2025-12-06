Looking at your login test implementation, I can see you have a good foundation. Here are some suggestions to improve the code structure and maintainability:

## 1. Improved Page Object Model

```typescript
// pageobjects/PageLogin.ts
import { Page, Locator, expect } from '@playwright/test';

export class PageLogin {
  readonly page: Page;
  
  // Locators
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly validationMessages: Locator;
  readonly forgotPasswordLink: Locator;
  readonly socialIcons: Record<string, Locator>;

  constructor(page: Page) {
    this.page = page;
    
    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.oxd-alert-content');
    this.validationMessages = page.locator('.oxd-text--span');
    this.forgotPasswordLink = page.locator('text=Forgot your password?');
    
    this.socialIcons = {
      linkedin: page.locator('[href*="linkedin"]'),
      facebook: page.locator('[href*="facebook"]'),
      twitter: page.locator('[href*="twitter"]'),
      youtube: page.locator('[href*="youtube"]')
    };
  }

  async goto(url: string = 'https://opensource-demo.orangehrmlive.com/'): Promise<void> {
    await this.page.goto(url);
    await this.waitForPageLoad();
  }

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
    await this.usernameInput.waitFor({ state: 'visible' });
  }

  async login(username: string, password: string): Promise<void> {
    await this.fillUsername(username);
    await this.fillPassword(password);
    await this.clickLogin();
  }

  async fillUsername(username: string): Promise<void> {
    await this.usernameInput.fill(username);
  }

  async fillPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
  }

  async clickLogin(): Promise<void> {
    await this.loginButton.click();
  }

  async getUsernamePlaceholder(): Promise<string> {
    return await this.usernameInput.getAttribute('placeholder') || '';
  }

  async getPasswordPlaceholder(): Promise<string> {
    return await this.passwordInput.getAttribute('placeholder') || '';
  }

  async isErrorMessageVisible(expectedMessage: string): Promise<boolean> {
    const errorLocator = this.page.locator(`text=${expectedMessage}`);
    return await errorLocator.isVisible();
  }
}
```

## 2. Enhanced Test Steps with Better Error Handling

```typescript
// support/fixtures.ts
import { test as base } from '@playwright/test';
import { PageManager } from '../pageobjects/PageManager';

export const test = base.extend<{ pageManager: PageManager }>({
  pageManager: async ({ page }, use) => {
    const pageManager = new PageManager(page);
    await use(pageManager);
  },
});

export const { When, Then, Given } = test;

// Updated steps with better error handling
Given('I open the website', async function ({ pageManager }) {
  await pageManager.loginPage.goto();
});

Given('I open the website with JavaScript disabled', async function ({ pageManager }) {
  await pageManager.context.addInitScript(() => {
    // More comprehensive JS disabling
    Object.defineProperty(window, 'eval', { value: () => { throw new Error('JS disabled'); } });
    Object.defineProperty(window, 'Function', { value: () => { throw new Error('JS disabled'); } });
    Object.defineProperty(window, 'setTimeout', { value: () => { throw new Error('JS disabled'); } });
  });
  await pageManager.loginPage.goto();
});

When('I enter the username {string}', async function ({ pageManager }, username: string) {
  await pageManager.loginPage.fillUsername(username);
});

When('I enter the password {string}', async function ({ pageManager }, password: string) {
  await pageManager.loginPage.fillPassword(password);
});

When('I click on the {string} button', async function ({ pageManager }, buttonText: string) {
  const button = pageManager.page.locator('button', { hasText: buttonText }).first();
  await button.click();
});

When('I login with credentials {string} and {string}', async function (
  { pageManager }, 
  username: string, 
  password: string
) {
  await pageManager.loginPage.login(username, password);
});

Then('I should be redirected to the dashboard', async function ({ pageManager }) {
  await pageManager.page.waitForURL(/\/dashboard/);
  await expect(pageManager.page).toHaveURL(/\/dashboard/);
});

Then('I should see an error message {string}', async function ({ pageManager }, expectedMsg: string) {
  await expect(pageManager.loginPage.errorMessage).toContainText(expectedMsg);
});

Then('I should see a validation message {string}', async function ({ pageManager }, expectedMsg: string) {
  const validationLocator = pageManager.loginPage.validationMessages.filter({ hasText: expectedMsg });
  await expect(validationLocator.first()).toBeVisible();
});

Then('I should see validation messages for username and password', async function ({ pageManager }) {
  const validationMessages = pageManager.loginPage.validationMessages;
  await expect(validationMessages).toHaveCount(2);
});

Then('the Username field should display placeholder {string}', async function ({ pageManager }, placeholder: string) {
  const actualPlaceholder = await pageManager.loginPage.getUsernamePlaceholder();
  expect(actualPlaceholder).toBe(placeholder);
});

Then('the Password field should display placeholder {string}', async function ({ pageManager }, placeholder: string) {
  const actualPlaceholder = await pageManager.loginPage.getPasswordPlaceholder();
  expect(actualPlaceholder).toBe(placeholder);
});

Then('a button with text {string} should be displayed', async function ({ pageManager }, buttonText: string) {
  const button = pageManager.page.locator('button', { hasText: buttonText });
  await expect(button).toBeVisible();
});

Then('the {string} link should be displayed', async function ({ pageManager }, linkText: string) {
  const link = pageManager.page.locator('a', { hasText: linkText });
  await expect(link).toBeVisible();
});

Then('all social media links should be displayed', async function ({ pageManager }) {
  for (const [platform, locator] of Object.entries(pageManager.loginPage.socialIcons)) {
    await expect(locator).toBeVisible();
  }
});

Then('the login form should not be functional due to JavaScript being disabled', async function ({ pageManager }) {
  // Attempt to submit form
  await pageManager.loginPage.clickLogin();
  
  // Check if still on login page or showing JS warning
  const currentUrl = pageManager.page.url();
  const isStillOnLoginPage = currentUrl.includes('/auth/login') || !currentUrl.includes('/dashboard');
  
  expect(isStillOnLoginPage).toBe(true);
});
```

## 3. Additional Utility Functions

```typescript
// utils/test-helpers.ts
export class TestHelpers {
  static async waitForNavigation(page: any, action: Function, timeout: number = 5000) {
    await Promise.all([
      page.waitForNavigation({ timeout }),
      action()
    ]);
  }

  static async retryAction(action: Function, maxRetries: number = 3, delay: number = 1000) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        await action();
        return;
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
}
```

## 4. Configuration File

```typescript
// config/test-config.ts
export const TestConfig = {
  baseURL: 'https://opensource-demo.orangehrmlive.com/',
  timeout: 30000,
  viewport: { width: 1280, height: 720 },
  credentials: {
    valid: {
      username: 'Admin',
      password: 'admin123'
    },
    invalid: {
      username: 'invalid',
      password: 'invalid'
    }
  }
};
```

## Key Improvements:

1. **Better TypeScript support** with proper typing
2. **More robust locators** using specific attributes instead of text-only selectors
3. **Improved error handling** with proper assertions
4. **Consistent naming conventions** and structure
5. **Additional utility functions** for common test patterns
6. **Configuration management** for easier maintenance
7. **Better page object methods** with reusable login functionality

These improvements will make your tests more maintainable, reliable, and easier to extend.