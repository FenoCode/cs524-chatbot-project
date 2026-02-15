**Single Sign‑On with OIDC (Auth0)**

In the context of the OIDC‑conformant authentication pipeline, single sign‑on (SSO) must happen at the authorization server (i.e., Auth0) rather than the application, which means that you must employ Universal Login and redirect users to the login page. To learn more, read Universal Login and Single Sign‑On. ([Auth0][1])

At a general level, when performing SSO:

1. If the user is not logged in locally, you should redirect them to your Auth0 login page (`/authorize`) for authentication using a redirect‑based flow, such as the Authorization Code Flow or Implicit Flow, depending on the type of application. ([Auth0][1])
2. If the user was already logged in through SSO, Auth0 will immediately authenticate them without needing to re‑enter credentials. ([Auth0][1])

To determine whether users are logged in via SSO, use silent authentication, which either re‑authenticates a user if they are already logged in or returns an error if they need to authenticate. In the legacy authentication pipeline, this could be achieved by using the `/ssodata` endpoint, which is deprecated in the OIDC‑conformant pipeline. ([Auth0][1])
