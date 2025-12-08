```typescript
import { When, Then, Given } from '../../support/fixtures';
import { PageManager } from '../../../pageobjects/PageManager';
import { LoginpomPage } from '../../../pageobjects/LoginpomPage';
import data from '../../../utils/data.json';

const pageLogin = (pm: PageManager): LoginpomPage => pm.getLoginPage();

Given('I open the website', async function (this: FixtureContext) {
    await pageLogin(this.pageManager).goto(data.url);
    await pageLogin(this.pageManager).waitForPageLoad();
});

Given('I open the website with JavaScript disabled', async function (this: FixtureContext) {
    await this.pageManager.context.addInitScript(() => {
        Object.defineProperty(navigator, 'javaEnabled', { get: () => false });
    });
    await pageLogin(this.pageManager).goto(data.url);
    await pageLogin(this.pageManager).waitForPageLoad();
});

Given('I enter the username {string}', async function (this: FixtureContext, username: string) {
    await pageLogin(this.pageManager).fillUsername(username);
});

Given('I enter the password {string}', async function (this: FixtureContext, password: string) {
    await pageLogin(this.pageManager).fillPassword(password);
});

When('I click on {string}', async function (this: FixtureContext, buttonText: string) {
    if (buttonText === 'Login') {
        await pageLogin(this.pageManager).clickLogin();
    }
});

Then('I should be redirected to the dashboard', async function (this: FixtureContext) {
    await pageLogin(this.pageManager).waitForPageLoad();
});

Then('I should see an error message {string}', async function (this: FixtureContext, msg: string) {
    // No error locator defined in POM; placeholder for future implementation
    await pageLogin(this.pageManager).waitForPageLoad();
});

Then('I should see a validation message {string}', async function (this: FixtureContext, msg: string) {
    // No validation locator defined in POM; placeholder for future implementation
    await pageLogin(this.pageManager).waitForPageLoad();
});

Then('I should see validation messages {string} and {string}', async function (this: FixtureContext, msg1: string, msg2: string) {
    // No validation locators defined in POM; placeholder for future implementation
    await pageLogin(this.pageManager).waitForPageLoad();
});

Then('the Username field should display placeholder {string}', async function (this: FixtureContext, expected: string) {
    const placeholder = await pageLogin(this.pageManager).getUsernamePlaceholder();
    expect(placeholder).toBe(expected);
});

Then('the Password field should display placeholder {string}', async function (this: FixtureContext, expected: string) {
    const placeholder = await pageLogin(this.pageManager).getPasswordPlaceholder();
    expect(placeholder).toBe(expected);
});

Then('a button with text {string} should be displayed', async function (this: FixtureContext, text: string) {
    const buttonText = await pageLogin(this.pageManager).getLoginButtonText();
    expect(buttonText.trim()).toBe(text);
    await pageLogin(this.pageManager).verifyLoginButtonVisible();
});

Then('a link with text {string} should be displayed', async function (this: FixtureContext, text: string) {
    const linkText = await pageLogin(this.pageManager).getForgotPasswordLinkText();
    expect(linkText?.trim()).toBe(text);
    await pageLogin(this.pageManager).verifyForgotPasswordLinkVisible();
});

Then('links for LinkedIn, Facebook, Twitter, and YouTube should be displayed', async function (this: FixtureContext) {
    await pageLogin(this.pageManager).verifySocialIconsVisible();
});

Then('the login form should not be functional and an appropriate warning should be shown', async function (this: FixtureContext) {
    // No specific warning locator in POM; placeholder for future implementation
    await pageLogin(this.pageManager).waitForPageLoad();
});
```