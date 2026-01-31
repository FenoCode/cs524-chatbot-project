how to enable EntraID SSO on a github enterprise #169189

Hello
we have a github enterprise, because it needed to be in a european data residency it was created for us by the github support team
i am now trying to implement SSO on the enterprise, but i need to login with the setup user account, i have never created or received this
when the enterprise was created by the github support team, just got a invitation to become owner with and i used my reguler github account for that, i am listed as enterprise owner.
any idea of what i am missing? i cannot seem to find any reference to this setup user anywhere and i am unable to follow the steps provided with my owner account (the settings are missing)

---

Resolving Entra ID SSO Setup for GitHub Enterprise

Issue:
You're unable to configure Entra ID SSO because:

1. The enterprise was provisioned by GitHub Support (EU data residency)
2. You never received "setup user" credentials
3. Your owner account doesn't see the required settings

Step-by-Step Solution:

1. Verify Your Access
   Confirm you're logged into the GitHub account that's listed as Enterprise Owner
   Navigate to: [https://github.com/enterprises/YOUR-ENTERPRISE-NAME](https://github.com/enterprises/YOUR-ENTERPRISE-NAME) (replace with your enterprise name)

2. Required Permissions
   You need both:
   • Enterprise Owner role in GitHub
   • Global Admin in Entra ID (Azure AD)

3. Alternative Access Methods
   If settings are missing:
   Try accessing via direct URL:
   [https://github.com/enterprises/YOUR-ENTERPRISE-NAME/settings/security](https://github.com/enterprises/YOUR-ENTERPRISE-NAME/settings/security)
   Use GitHub's API to check configuration:
   bash
   curl -H "Authorization: Bearer YOUR_PAT" [https://api.github.com/enterprises/YOUR-ENTERPRISE-NAME](https://api.github.com/enterprises/YOUR-ENTERPRISE-NAME)

4. Recover Setup User
   Since GitHub Support created the instance:
   Contact GitHub Support directly via:
   [https://support.github.com/contact](https://support.github.com/contact)
   Reference your enterprise name and EU data residency request
   Request either:
   a) The setup user credentials
   b) Temporary elevation of your owner permissions
   c) A reset of the SSO configuration portal

5. Temporary Workaround
   Ask GitHub Support to:
   …

Post-Setup
Once SSO is enabled:
• Configure team synchronization: [https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management/using-enterprise-managed-users-for-iam/about-enterprise-managed-users](https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management/using-enterprise-managed-users-for-iam/about-enterprise-managed-users)
Key Notes:
• The "setup user" is typically only used during initial configuration
• GitHub's EU-hosted enterprises sometimes have different provisioning workflows
• Enterprise Owners should normally have all required permissions — this appears to be a provisioning oversight

---

Hello, thanks for the response
i just saw that github support has sent me the setup _admin users credentials, solving the issue,
thank you for your time

---

It's alright. I'm happy to help you