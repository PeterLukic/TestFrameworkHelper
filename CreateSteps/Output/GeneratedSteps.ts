import { Given, When, Then } from '../../support/fixtures';

const pageLogin = (pageManager: FixtureContext['pageManager']) => pageManager.getPageLogin();

Given('I am on the login page', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).navigateToLoginPage();
});

Given('I was redirected to login after trying to access a protected page', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).navigateToLoginPage();
});

When('I load the login page', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).navigateToLoginPage();
});

When('I view the login page', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).navigateToLoginPage();
});

When('I enter my registered username {string} into the username field', async ({ pageManager }: FixtureContext, username: string) => {
  await pageLogin(pageManager).fillUsername(username);
});

When('I enter my correct password {string} into the password field', async ({ pageManager }: FixtureContext, password: string) => {
  await pageLogin(pageManager).fillPassword(password);
});

When('I enter an incorrect password {string}', async ({ pageManager }: FixtureContext, password: string) => {
  await pageLogin(pageManager).fillPassword(password);
});

When('I enter a password {string} into the password field', async ({ pageManager }: FixtureContext, password: string) => {
  await pageLogin(pageManager).fillPassword(password);
});

When('I leave the username field empty', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).fillUsername('');
});

When('I leave the password field empty', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).fillPassword('');
});

When('I click the Login button', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).clickLoginButton();
});

When('I enter valid credentials {string} and {string}', async ({ pageManager }: FixtureContext, user: string, pass: string) => {
  await pageLogin(pageManager).loginWithCredentials(user, pass);
});

When('I enter a username with international characters {string}', async ({ pageManager }: FixtureContext, username: string) => {
  await pageLogin(pageManager).fillUsername(username);
});

When('I enter a password with special characters {string}', async ({ pageManager }: FixtureContext, password: string) => {
  await pageLogin(pageManager).fillPassword(password);
});

Then('I should see an error message {string}', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyErrorMessageVisible();
});

Then('I should remain on the login page', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyLoginTitleVisible();
});

Then('I should see a validation error {string}', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyErrorMessageVisible();
});

Then('I should see a connection error message {string}', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyErrorMessageVisible();
});

Then('I should see a rate limiting message or captcha challenge', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyErrorMessageVisible();
});

Then('the login title should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyLoginTitleVisible();
});

Then('the login title text should be {string}', async ({ pageManager }: FixtureContext, text: string) => {
  await pageLogin(pageManager).verifyLoginTitleText(text);
});

Then('demo credentials should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyDemoCredentialsVisible();
});

Then('demo credentials should contain {string}', async ({ pageManager }: FixtureContext, text: string) => {
  await pageLogin(pageManager).verifyDemoCredentialsText(text);
});

Then('username input should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyUsernameInputVisible();
});

Then('password input should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyPasswordInputVisible();
});

Then('login button should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyLoginButtonVisible();
});

Then('forgot-password link should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyForgotPasswordLinkVisible();
});

Then('social media links should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifySocialLinksVisible();
});

Then('copyright text should be visible', async ({ pageManager }: FixtureContext) => {
  await pageLogin(pageManager).verifyCopyrightTextVisible();
});