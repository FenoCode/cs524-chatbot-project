
**Question:**
I have a website [www.example.com](http://www.example.com). I have a few clients (businesses) using my website, let's say they are C1 ([www.c1.com](http://www.c1.com)), C2 ([www.c2.com](http://www.c2.com)) and C3 ([www.c3.com](http://www.c3.com)). I want to enable Okta SAML authentication for them so that whenever they come to my website, they can manage their identities through Okta. I already have Google and Microsoft OIDC integrated in my system, but I want to integrate SAML through Okta as well so that new clients who are already using Okta in their system can integrate with my app seamlessly. My application is in Java and infrastructure is hosted on AWS. What are the integration steps for Okta SAML integration? I went through their documentation but the process is still not clear to me. Also, as it's the first time I'm integrating with SAML, I'm not sure about these details. I went through the Okta documentation and even tried by putting dummy values for required fields just to see their positioning in my system but I am unable to get any luck out of this.

---

**Answer:**
You'd need a separate instance of your application for each of the clients, because to enable SAML SSO you have to exchange metadata with each of your clients, as well as have a separate user database for each of them if that matters for your app. I guess you need to also implement SAML response processing in your application to be able to verify it and figure out a user coming to your app. Those are two principal things to be done first, before you can move any further.

---

**Comment (on answer):**
Is there any GitHub repository that can be referred for this? As I'm not sure about the steps you're mentioning. ([Stack Overflow][1])

---