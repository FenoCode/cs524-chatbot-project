**OAuth 2.0 and OpenID Connect protocols — Microsoft identity platform**

Knowing about OAuth or OpenID Connect (OIDC) at the protocol level isn’t required to use the Microsoft identity platform. However, you’ll encounter protocol terms and concepts as you use the identity platform to add authentication to your apps. Understanding some fundamentals can assist your integration and overall experience. ([Microsoft Learn][1])

**Roles in OAuth 2.0 and OIDC**

Four parties are generally involved in an OAuth 2.0 and OpenID Connect authentication and authorization exchange:

* **Authorization server** — The Microsoft identity platform acts as the authorization server (also called an identity provider or IdP), securely handling the end‑user’s information, access, and trust relationships. It issues security tokens that apps and APIs use to grant or deny access after a user signs in. ([Microsoft Learn][1])
* **Client** — The application requesting access to a protected resource. This can be a web app on a server, a single‑page app in a browser, or a web API calling another web API. ([Microsoft Learn][1])
* **Resource owner** — Usually the end‑user whose data is being protected. They “own” the protected resource and can grant or deny access to it. ([Microsoft Learn][1])
* **Resource server** — Hosts or provides access to the resource owner’s data and relies on the authorization server to authenticate and authorize access based on tokens. ([Microsoft Learn][1])

**Tokens**

Bearer tokens are used in authentication and authorization flows to verify principals and grant access to protected resources. In the Microsoft identity platform, these tokens are formatted as JSON Web Tokens (JWT). ([Microsoft Learn][1])

* **Access tokens** — Issued by the authorization server to a client application; used to access protected APIs. ([Microsoft Learn][1])
* **ID tokens** — Issued to the client to sign in users and obtain basic user information. ([Microsoft Learn][1])
* **Refresh tokens** — Used by clients to request new access and ID tokens from the authorization server. ([Microsoft Learn][1])

**App Registration**

To trust security tokens issued by the identity platform, your app must be registered in the Microsoft Entra admin center. Registration assigns values to the app, including:

* **Application (client) ID** — A unique identifier included in issued tokens. ([Microsoft Learn][1])
* **Redirect URI** — Used by the authorization server after completing interactions like signing in. ([Microsoft Learn][1])

Your app’s registration also stores information about endpoints (like authorization and token endpoints) that your code uses to request tokens. ([Microsoft Learn][1])

**Endpoints**

The Microsoft identity platform implements standards‑compliant OAuth 2.0 and OpenID Connect (OIDC) 1.0 endpoints that support the authentication and authorization flows. Examples include: ([Microsoft Learn][1])

```
Authorization endpoint — https://login.microsoftonline.com/<issuer>/oauth2/v2.0/authorize
Token endpoint — https://login.microsoftonline.com/<issuer>/oauth2/v2.0/token
```

The exact URL formats vary by application type, sign‑in audience, and Azure cloud instance. ([Microsoft Learn][1])

**Next Steps**

To implement authentication flows for various application types, Microsoft recommends using the Microsoft Authentication Library (MSAL) rather than crafting raw HTTP calls. MSAL handles securely acquiring tokens and managing flows like authorization code, client credentials, on‑behalf‑of, and OpenID Connect for user sign‑in and single sign‑on (SSO). ([Microsoft Learn][1])
