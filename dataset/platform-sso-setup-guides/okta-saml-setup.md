Build a Single Sign-On (SSO) integration

This guide teaches you how to integrate your federated SSO application with Okta. This guide assumes that you intend to make this app integration public by publishing it in the Okta Integration Network (OIN). ([developer.okta.com][1])

Learning outcome

Create and test an SSO app integration for OIN submission. ([developer.okta.com][1])

What you need

* Okta Integrator Free Plan org
* An app to integrate SSO with Okta ([developer.okta.com][1])

Overview

Single Sign-On (SSO) is an authentication method that enables end users to sign in to multiple applications with one set of credentials. If you have customers that use Okta as an Identity Provider, you want to publish your SSO app integration to the OIN so customers can easily configure SSO for your app. ([developer.okta.com][1])

To create an SSO integration for the OIN, first sign up for a free Integrator Free Plan org. Next, select the type of SSO protocol to implement. Okta supports two SSO standards for your integration: OpenID Connect (OIDC) (preferred) and Security Assertion Markup Language (SAML). Okta recommends using OIDC for new SSO integrations. ([developer.okta.com][1])

Deployment models

After choosing a protocol, select a deployment model. Okta offers redirect authentication or embedded authentication deployment models. Redirect authentication uses the Okta Sign-In Widget and is the easiest, most secure way to integrate with Okta. Okta recommends the redirect authentication deployment model if your situation meets the requirements. ([developer.okta.com][1])

Build your integration

If you're unfamiliar with SAML 2.0, review SAML concept and Okta SAML FAQs first. ([developer.okta.com][1])

Use SAML toolkits to quickly build your SSO integration. These toolkits help you implement SAML 2.0 and create the Service Provider WebSSO profile. Example toolkits include:

* .NET: Sustainsys.Saml2
* Java: OpenSAML
* Python: PySAML2
* Ruby: Ruby-SAML

Okta does not own or maintain these toolkits. ([developer.okta.com][1])

Gather SAML attributes before creating an app integration instance in Okta. In a SAML integration, Okta is the Identity Provider (IdP), and your app is the Service Provider (SP). You should determine the default Assertion Consumer Service (ACS) URL for your integration (the SP sign-in URL), find your audience URI or SP Entity ID, optionally set up a relay state page, and gather any required SAML attributes your app needs. Okta recommends keeping the number of SAML attributes minimal. SAML integrations must use SHA-256 encryption; if using SHA-1, upgrade to SHA-256. ([developer.okta.com][1])

Create your integration in Okta

This section assumes you already built the SSO integration in your app. Instructions for adding your integration into Okta vary depending on whether you want to provide a public or private integration. ([developer.okta.com][1])

Submit an OIN integration

If you want your integration in the Okta Integration Network, follow the OIN Wizard instructions to add required integration artifacts and metadata, create a test app integration instance, test SSO flows, and submit your integration for verification and publication. Creating a test instance does not automatically make it public; after testing, submit for verification. ([developer.okta.com][1])

Add a private integration

If you want the integration to exist only in your Okta org, use the Application Integration Wizard in the Admin Console to create an app integration instance and test your SSO flows. Once configured, your org users can access the app. Common use cases include testing in a private org or having advanced SAML features not supported by the OIN Wizard. ([developer.okta.com][1])

Next steps

To publish your integration, start the submission process to have your SSO integration included in the OIN by reviewing the publication overview and following the OIN Wizard for submission. ([developer.okta.com][1])
