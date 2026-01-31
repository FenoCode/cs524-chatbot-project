# Overview
This page contains some of the best resources we have collected that will help you rapidly understand what **SCIM 2.0** is and how to integrate it in your application.


**SCIM 2.0** is an amazing API standard because it allows for Identity Governance systems to manage **account provisioning** and **permission management** for you. It is able to do this because the APIs you expose allow for a standardized method of creating and managing user data for your application.

## Concepts
Here is a basic concept roadmap you need to understand **SCIM 2.0** to have a great experience programming this standardized identity provisioning interface in your application.

### SCIM 2.0 Connect Roadmap
::: mermaid
 graph LR;
 A[HTTP] --> B[Web Programming] -->  C[REST API] --> D[SCIM 2.0] --> E(SCIM 2.0 Example Code);
:::

### HTTP Basics
While this is incredibly fundamental, you can learn HTTP and all things web programming at **W3 Schools** here: [What is HTTP](https://www.w3schools.com/whatis/whatis_http.asp)

### Web Programming
If you are primarily a front-end developer, backend developer, mix of both, or don't know what I'm talking about, get the gist from **W3 Schools**: [FullStack Development](https://www.w3schools.com/whatis/whatis_fullstack.asp).

### REST API Basics
**W3 Schools** has it again! You can quickly **understand** and **play** with REST APIs here: [Web API Introduction](https://www.w3schools.com/js/js_api_intro.asp).

### SCIM 2.0 Primer
Best thing is to understand the brief history of the protocol. Get the gist of what SCIM is and how its changed to really know what it is designed to do: [SCIM 1.0 vs SCIM 2.0](https://workos.com/blog/scim2-vs-scim1)

# SCIM Planning Resources
1. SCIM 2.0 Guide from Okta: [Okta and SCIM Version 2.0](https://developer.okta.com/docs/api/openapi/okta-scim/guides/scim-20/)
2. SCIM 2.0 Guide from Microsoft [Tutorial: Develop and plan provisioning for a SCIM endpoint in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups)

# Example Code
These two examples are based on .NET, but the logic presented here can be translated to implement the same REST APIs in any backend REST API framekwork.

1. [How to Manage User Lifecycle with .NET and SCIM](https://developer.okta.com/blog/2024/02/29/net-scim)
    - Best to help understanding the implementation piece of SCIM 2.0
2. [Using Microsoft’s SCIM sample](https://medium.com/the-new-control-plane/using-microsofts-scim-sample-a6e7dddbca71)
    - Great tutorial to walk through example code and interact with the SCIM APIs on your own machine
    - *NOTE:* You will have to retrieve the example code from GitHub. A common way to do this is through **KiteWorks**!