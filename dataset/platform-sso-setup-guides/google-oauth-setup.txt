OAuth application integration overview

This page provides an overview of OAuth application integration in Google Cloud.

You can use OAuth application integration to integrate your OAuth‑based applications with Google Cloud. Federated users can use their identity provider (IdP) to sign in to the applications and access their Google Cloud products and data. OAuth application integration is a feature of Workforce Identity Federation. ([Google Cloud Documentation][1])

To use OAuth application integration, you must first create a workforce identity pool and provider. You can then register the OAuth‑based application using OAuth 2.0. Applications must be registered in the organization where your workforce identity pool and provider are configured. ([Google Cloud Documentation][1])

Important: OAuth application integration works only with Identity‑Aware Proxy. ([Google Cloud Documentation][1])

OAuth application registration

To configure an application to access Google Cloud, you register the application with Google Cloud by creating OAuth client credentials. The credential contains a client secret. The application uses the access token to access the Google Cloud products and data. ([Google Cloud Documentation][1])

OAuth client and credential security risks and mitigations

You must secure access to the IAM APIs and the client ID and secret. If the client ID and secret is leaked, security issues can result. These issues include the following: ([Google Cloud Documentation][1])

* **Impersonation:** A malicious user with your client ID and secret can create an application that masquerades as your legitimate application. They can then gain unauthorized access to the user data and permissions that your application is entitled to, perform actions on the user’s behalf such as posting content, making API calls, or modifying user settings, or perform phishing attacks wherein the malicious user creates a fake login page that resembles the OAuth provider and tricks users into entering their credentials. ([Google Cloud Documentation][1])
* **Reputational damage:** A security breach can harm the reputation of your application and organization, causing users to lose trust. ([Google Cloud Documentation][1])

In the event of a breach, to mitigate these and other risks, assess the nature of the breach and do the following: ([Google Cloud Documentation][1])

* Ensure that only trusted users have IAM access to the OAuth client and credential API. ([Google Cloud Documentation][1])
* Rotate the client secret immediately, by rotating the client credential as follows: ([Google Cloud Documentation][1])

  1. Create a new client credential for the OAuth client.
  2. Disable the old client credential.
  3. Delete the old client credential. ([Google Cloud Documentation][1])
