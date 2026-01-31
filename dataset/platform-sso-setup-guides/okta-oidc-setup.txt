**Build a Single Sign-On (SSO) integration — OpenID Connect**

This guide teaches you how to integrate your federated SSO application with Okta, assuming you want to publish this app integration in the Okta Integration Network (OIN). ([Okta Developer][1])

### Overview

Single Sign-On (SSO) enables end users to sign in to multiple applications with one set of credentials. Okta supports two SSO standards for integration: OpenID Connect (OIDC) (preferred) and SAML. Okta recommends using OIDC for new SSO integrations. ([Okta Developer][1])

After choosing a protocol, select a deployment model. Okta offers redirect or embedded authentication models. Redirect authentication uses the Okta Sign-In Widget and is generally the easiest and most secure way to integrate. ([Okta Developer][1])

### Build your integration

If your app hasn’t implemented OIDC yet, review OAuth 2.0 and OpenID Connect fundamentals. For OIN-ready integrations:

1. Use the Authorization Code flow with client secrets.
2. Determine required scopes for your OIDC client.
3. Decide how your app stores customer client credentials.
4. Implement token validation logic.
5. Support automatic credential rotation.
6. Determine your sign-in redirect URIs.
7. Consider Okta API rate limits when building your integration. ([Okta Developer][1])

Okta uses a multi-tenant credential system for OIDC integrations: each customer org instance generates a unique set of client credentials that your app must track. ([Okta Developer][1])

### Determine the OAuth 2.0 flow to use

For web applications, Okta mandates the Authorization Code flow. SPAs and mobile apps must use a backend service to manage authentication securely. The OIN does not support direct authentication from SPAs or native apps; instead, use a backend to interact with Okta. ([Okta Developer][1])

For OIN integrations you must use the org authorization server (not custom ones), and refresh tokens aren’t supported for OIN OIDC apps. ([Okta Developer][1])

### Token validation

To check access tokens, use the `/introspect` endpoint to verify token status. For OIN integrations, access tokens require remote validation, while ID tokens can be validated locally. ([Okta Developer][1])

### Key rotation

Okta rotates signing keys regularly. Your OIDC client should periodically fetch the public keys (`/keys` endpoint) used to verify token signatures and handle key changes gracefully. ([Okta Developer][1])

### Rate limits

Pay attention to Okta API rate limits and monitor headers (like `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining`, and `X-Rate-Limit-Reset`) in responses. Public metadata endpoints are not subject to rate limiting. ([Okta Developer][1])

---

### Create your integration in Okta

After building your app integration:

**Submit an OIN integration:**
Follow the OIN Wizard to add required artifacts, create a testing instance, verify SSO flows, and submit for verification and publication. ([Okta Developer][1])

**Add a private integration:**
Use the Admin Console’s App Integration Wizard to create a private app instance for your Okta org and test its SSO flows. ([Okta Developer][1])
