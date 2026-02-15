AWS IAM Identity Center is the AWS solution for connecting your workforce users to AWS managed applications such as Amazon Q Developer and Amazon Quick Suite and other AWS resources. You can connect your existing identity provider and synchronize users and groups from your directory, or create and manage your users directly in IAM Identity Center. You can then use IAM Identity Center for either or both of the following:

* User access to applications
* User access to AWS accounts ([AWS Documentation][1])

You don’t need to change your current AWS account workflows to use IAM Identity Center for access to AWS managed applications. If you’re using federation with IAM for AWS account access, your users can continue to access AWS accounts in the same way they always have, and you can continue to use your existing workflows to manage that access. ([AWS Documentation][1])

IAM Identity Center streamlines and simplifies workforce user access to applications or AWS accounts, or both, through the following key capabilities: ([AWS Documentation][1])

* **Integration with AWS managed applications:** AWS managed applications such as Amazon Q Developer and Amazon Redshift integrate with IAM Identity Center, which provides a common view of users and groups. ([AWS Documentation][1])
* **Trusted identity propagation across applications:** With trusted identity propagation, AWS managed applications can securely share a user’s identity with other AWS managed applications and authorize access to AWS resources based on the user’s identity. ([AWS Documentation][1])
* **One place to assign permissions to multiple AWS accounts:** IAM Identity Center provides a single place to assign permissions to groups of users in multiple AWS accounts based on common job functions or custom permissions. ([AWS Documentation][1])
* **One point of federation to simplify user access to AWS:** IAM Identity Center reduces administrative effort by providing one point of federation, so you only federate once and manage a single certificate when using a SAML 2.0 identity provider. ([AWS Documentation][1])
* **User‑friendly web portal access:** The AWS access portal is a web portal that provides users with seamless access to all their assigned applications, AWS accounts, or both. ([AWS Documentation][1])

IAM Identity Center supports two deployment types: **organization instances** (the recommended production configuration, deployed in the AWS Organizations management account to centrally manage user access across AWS) and **account instances** (bound to a single AWS account for isolated use cases). ([AWS Documentation][1])

On July 26, 2022, AWS Single Sign‑On was renamed to **AWS IAM Identity Center**. Legacy API namespaces and related CLI commands remain unchanged for backward compatibility. ([AWS Documentation][1])

[1]: https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html?utm_source=chatgpt.com "What is IAM Identity Center? - AWS IAM Identity Center"
