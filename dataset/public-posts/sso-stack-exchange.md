Understand the relationships between SSO, OAuth, OIDC, SAML, Okta

I’m getting confused by those terminologies and how they’re related to others. Many articles on the internet don’t agree on a single view whether those are categorized as protocols, standards or frameworks or even concepts. Some articles call OAuth a standard while some others call it a framework and none explains the differences between a protocol and a framework and a concept (I think protocol means the same as standard).

I’ve used some of them in application development but I still feel like I’m a newbie in this area. I would appreciate if someone can simplify those terms.

---

A standard is anything which some authority like the Internet Engineering Task Force (IETF) has declared to be a standard. That’s it. Standards can specify protocols, algorithms, names and many other things. For example, you find a lot of IETF Internet Standards published through a Request for Comments (RFC). OAuth 2.0 has been standardized in RFC 6749, so it’s clearly a standard. As the title “The OAuth 2.0 Authorization Framework” already suggests, it’s also called a “framework” which is a rather vague term. In addition to that, the RFC refers to OAuth 2.0 as a “protocol”. So you could say it’s all at the same time: a standard by the IETF, a framework and a protocol.

A protocol is a formally defined set of rules which is meant to ensure that, for example, different network hosts can communicate with each other in an unambiguous manner. Without clearly specified protocols like IP, TCP or HTTP, we couldn’t have this discussion because our devices would have no idea which data to transmit at which time to whom. If you read RFC 6749 for OAuth 2.0, you can find a lot of formal descriptions which tell implementers how exactly the messages look like and who is supposed to send which message in which order. This is crucial for the authentication to work because all involved parties have to agree on how to communicate. Not every protocol is a standard. For example, you could invent your own protocol right now, but as long as you don’t convince a recognized authority like the IETF, it won’t be a standard (at least not a widely accepted one).

As I already said, “framework” isn’t a clearly defined term. You could say it’s a generic solution which can be applied to different use cases. For example, in the case of OAuth, the standard explicitly allows custom extensions to define new grant types, access token types etc.

Regarding the relationships between SSO, OAuth, OIDC etc.:

* Single Sign-On is an abstract concept where a user authenticates at some central service and is then allowed to access multiple different systems. This description is of course far too vague for an actual software or hardware implementation, so you need concrete protocols to define the details.
* OAuth is an authorization protocol (or “framework”) which mostly specifies how the owner of a protected resource can allow a third party to access this resource without knowing the owner’s credentials (the Resource Owner Password Credentials grant type deviates from this principle, but it’s largely considered obsolete).
* OpenID Connect is an authentication protocol built on top of OAuth which specifies how a user can authenticate at a service through a third-party identity provider like Google or Amazon. You can use OIDC to implement SSO. Unlike OAuth, OpenID Connect is standardized by the OpenID Foundation.
* SAML is a competing SSO implementation standardized by the Organization for the Advancement of Structured Information Standards (OASIS). So it’s an alternative to OIDC.
* Okta is a company which also happens to be an OIDC provider.

---