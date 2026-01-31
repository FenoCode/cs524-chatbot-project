# Overview
This page contains some of the best resources we have collected that will help you rapidly understand what **OpenID Connect** is and how to integrate it in your application.

*Your friendly IAM (Identity and Access Management) engineer here. Please take a look at the difference between [Authentication vs Authorization](https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization). If you want to level up in your IAM skill, bookmark this for later: [Intro to IAM](https://auth0.com/docs/get-started/identity-fundamentals/identity-and-access-management)* 

## Concepts
Here is the concept roadmap you need to understand **OpenID Connect (OIDC)** to have a great experience with integrating it in your application:

### OpenID Connect Roadmap
::: mermaid
 graph LR;
 A[JSON] --> B[JWT - JSON Web Token] --> C[OAuth 2.0] --> D[OpenID Connect] --> E(OIDC Example Code);
:::

### JSON
This resource is here for completeness, but I am confident you already got this down! :D
[JSON Overview](https://www.w3schools.com/js/js_json.asp)

### JWT - JSON Web Token
JWT is the token standard that oAuth and OpenID Connect use religiously. It is super clean and well defined. Welcome to standards-based authentication!

Auth0 is a great company that provides an excellent resource on understanding what at JWT is: [JWT Overview](https://auth0.com/docs/secure/tokens/json-web-tokens)
- An excellent tool for working with JWTs: [JWT Decoder Tool](https://fusionauth.io/dev-tools/jwt-decoder)


### OAuth 2.0
OAuth (Open Authorization) is the standard for access delegation. Here is a great Medium article that explains it on a high-level: [Understanding OAuth2](https://medium.com/web-security/understanding-oauth2-a50f29f0fbf7).

- Specific guidance on how to use oAuth Scopes to define access within your app on an access token: [oAuth Scopes Best Practices](https://curity.io/resources/learn/scope-best-practices/)

You don't have to implement an OAuth2 client to then understand OpenID Connect. Just make sure the OAuth terminology doesn't confuse you. Here is the big kicker. OAuth2 just has an **Access Token**. OpenID Connect is **ID Token + Access Token**.

What is an **ID Token** you might ask? Jump right into learning **OpenID Connect**!

### OpenID Connect

This resource from Okta explains the difference between OAuth 2.0 and OIDC in a way that builds on your OAuth knowledge nicely: [OAuth 2.0 and OpenID Connect Overview](https://developer.okta.com/docs/concepts/oauth-openid/).
   
- Here is a different Medium article that visualizes the different flow types better: [Diagrams of All the OpenID Connect Flows](https://darutk.medium.com/diagrams-of-all-the-openid-connect-flows-6968e3990660)

_If you are bored of reading_, here is a great video demonstration of what **OAuth2** is and how **OpenID Connect** cleanly builds on top of that: [Illustrated Guide to OAuth and OpenID Connect - 16 min](https://www.youtube.com/watch?v=t18YB3xDfXI&pp=ygUab2F1dGggYW5kIG9wZW5pZCBleHBsYWluZWQ%3D).

Now that you understand the protocol. Dive back into the data to understand what you should expect from the Identity Provider (IdP) in terms of an **Access Token** and **ID Token**: [ID Token vs AccessToken](https://auth0.com/blog/id-token-access-token-what-is-the-difference/)
  - To specifically understand the **claims** that are in an **Access Token** and **ID Token**, see this [Learn about OAuth 2.0 and OpenID Connect claims](https://developer.okta.com/docs/concepts/oauth-claims/)

## **OIDC** Example Code
The moment you have been waiting for is here. Finally some juicy code that shows you how others have implemented OIDC!

Remember, `ID Token == Authentication` and `Access Token == Authorization`. You can use claims from both to fully determine user access, but that is the intention!

### [.NET Example]()
.NET makes it very easy because it is implemented as Middleware. Protecting endpoints is as simple as putting a decorator over an API Endpoint function, and OIDC authentication is required to access it.

### [Python Django Example]()

### [Python FastAPI Example]()

### [Python Flask Example]()
Here are links that provide example code for the implementation:

General Flask SSO Example(s): https://www.squash.io/enterprise-functionalities-with-python-flask-sso-integrations-and-more/

A `flask-oidc` library implementation: https://www.toptal.com/flask/flask-login-tutorial-sso 

