typescript
import { Page, Locator, expect } from '@playwright/test';

export class PageLogin {
    private readonly page: Page;
    private readonly inputUsername: Locator;
    private readonly inputPassword: Locator;
    private readonly buttonLogin: Locator;
    private readonly linkForgotPassword: Locator;
    private readonly textLoginTitle: Locator;
    private readonly textDemoUsername: Locator;
    private readonly textDemoPassword: Locator;
    private readonly textErrorMessage: Locator;
    private readonly linkLinkedIn: Locator;
    private readonly linkFacebook: Locator;
    private readonly linkTwitter: Locator;
    private readonly linkYouTube: Locator;
    private readonly textCopyright: Locator;

    constructor(page: Page) {
        this.page = page;
        this.inputUsername = page.locator('input[name="username"]');
        this.inputPassword = page.locator('input[name="password"]');
        this.buttonLogin = page.locator('button[type="submit"]');
        this.linkForgotPassword = page.locator('.orangehrm-login-forgot-header');
        this.textLoginTitle = page.locator('.orangehrm-login-title');
        this.textDemoUsername = page.locator('.orangehrm-demo-credentials p:first-child');
        this.textDemoPassword = page.locator('.orangehrm-demo-credentials p:last-child');
        this.textErrorMessage = page.locator('.orangehrm-login-error');
        this.linkLinkedIn = page.locator('a[href*="linkedin.com"]');
        this.linkFacebook = page.locator('a[href*="facebook.com"]');
        this.linkTwitter = page.locator('a[href*="twitter.com"]');
        this.linkYouTube = page.locator('a[href*="youtube.com"]');
        this.textCopyright = page.locator('.orangehrm-copyright');
    }

    async goto(): Promise<void> {
        await this.page.goto('/web/index.php/auth/login');
    }

    async navigateToLoginPage(): Promise<void> {
        await this.goto();
    }

    async fillUsername(username: string): Promise<void> {
        await this.inputUsername.fill(username);
    }

    async fillPassword(password: string): Promise<void> {
        await this.inputPassword.fill(password);
    }

    async clickLoginButton(): Promise<void> {
        await this.buttonLogin.click();
    }

    async clickForgotPasswordLink(): Promise<void> {
        await this.linkForgotPassword.click();
    }

    async clickLinkedInLink(): Promise<void> {
        await this.linkLinkedIn.click();
    }

    async clickFacebookLink(): Promise<void> {
        await this.linkFacebook.click();
    }

    async clickTwitterLink(): Promise<void> {
        await this.linkTwitter.click();
    }

    async clickYouTubeLink(): Promise<void> {
        await this.linkYouTube.click();
    }

    async loginWithCredentials(username: string, password: string): Promise<void> {
        await this.fillUsername(username);
        await this.fillPassword(password);
        await this.clickLoginButton();
    }

    async verifyLoginTitleVisible(): Promise<void> {
        await expect(this.textLoginTitle).toBeVisible();
    }

    async verifyLoginTitleText(): Promise<void> {
        await expect(this.textLoginTitle).toHaveText('Login');
    }

    async verifyDemoCredentialsVisible(): Promise<void> {
        await expect(this.textDemoUsername).toBeVisible();
        await expect(this.textDemoPassword).toBeVisible();
    }

    async verifyDemoCredentialsText(): Promise<void> {
        await expect(this.textDemoUsername).toContainText('Admin');
        await expect(this.textDemoPassword).toContainText('admin123');
    }

    async verifyUsernameInputVisible(): Promise<void> {
        await expect(this.inputUsername).toBeVisible();
    }

    async verifyPasswordInputVisible(): Promise<void> {
        await expect(this.inputPassword).toBeVisible();
    }

    async verifyLoginButtonVisible(): Promise<void> {
        await expect(this.buttonLogin).toBeVisible();
    }

    async verifyForgotPasswordLinkVisible(): Promise<void> {
        await expect(this.linkForgotPassword).toBeVisible();
    }

    async verifySocialLinksVisible(): Promise<void> {
        await expect(this.linkLinkedIn).toBeVisible();
        await expect(this.linkFacebook).toBeVisible();
        await expect(this.linkTwitter).toBeVisible();
        await expect(this.linkYouTube).toBeVisible();
    }

    async verifyCopyrightTextVisible(): Promise<void> {
        await expect(this.textCopyright).toBeVisible();
    }

    async verifyErrorMessageVisible(): Promise<void> {
        await expect(this.textErrorMessage).toBeVisible();
    }

    async assertLoginTitleVisible(): Promise<void> {
        await expect(this.textLoginTitle).toBeVisible();
    }

    async assertLoginTitleText(): Promise<void> {
        await expect(this.textLoginTitle).toHaveText('Login');
    }

    async assertDemoCredentialsVisible(): Promise<void> {
        await expect(this.textDemoUsername).toBeVisible();
        await expect(this.textDemoPassword).toBeVisible();
    }

    async assertDemoCredentialsText(): Promise<void> {
        await expect(this.textDemoUsername).toContainText('Admin');
        await expect(this.textDemoPassword).toContainText('admin123');
    }

    async assertUsernameInputVisible(): Promise<void> {
        await expect(this.inputUsername).toBeVisible();
    }

    async assertPasswordInputVisible(): Promise<void> {
        await expect(this.inputPassword).toBeVisible();
    }

    async assertLoginButtonVisible(): Promise<void> {
        await expect(this.buttonLogin).toBeVisible();
    }

    async assertLoginButtonEnabled(): Promise<void> {
        await expect(this.buttonLogin).toBeEnabled();
    }

    async assertErrorMessageVisible(): Promise<void> {
        await expect(this.textErrorMessage).toBeVisible();
    }

    async assertErrorMessageText(expectedText: string): Promise<void> {
        await expect(this.textErrorMessage).toContainText(expectedText);
    }

    async isLoginTitleVisible(): Promise<boolean> {
        return await this.textLoginTitle.isVisible();
    }

    async isUsernameInputVisible(): Promise<boolean> {
        return await this.inputUsername.isVisible();
    }

    async isPasswordInputVisible(): Promise<boolean> {
        return await this.inputPassword.isVisible();
    }

    async isLoginButtonVisible(): Promise<boolean> {
        return await this.buttonLogin.isVisible();
    }

    async isLoginButtonEnabled(): Promise<boolean> {
        return await this.buttonLogin.isEnabled();
    }

    async isErrorMessageVisible(): Promise<boolean> {
        return await this.textErrorMessage.isVisible();
    }

    async getLoginTitleText(): Promise<string> {
        return await this.textLoginTitle.textContent() ?? '';
    }

    async getDemoUsernameText(): Promise<string> {
        return await this.textDemoUsername.textContent() ?? '';
    }

    async getDemoPasswordText(): Promise<string> {
        return await this.textDemoPassword.textContent() ?? '';
    }

    async getErrorMessageText(): Promise<string> {
        return await this.textErrorMessage.textContent() ?? '';
    }

    async getCopyrightText(): Promise<string> {
        return await this.textCopyright.textContent() ?? '';
    }
}