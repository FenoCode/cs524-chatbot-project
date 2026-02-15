Secrets Manager uses AWS Identity and Access Management (IAM) to secure access to secrets. IAM provides authentication and access control. Authentication verifies the identity of a requester using sign‑in credentials such as passwords, access keys, and multi‑factor authentication (MFA) tokens. Access control ensures only authorized identities can perform operations on AWS Secrets Manager resources. Secrets Manager uses IAM policies to define which identities can access which secrets and what actions they can perform. ([AWS Documentation][1])

You can grant Secrets Manager permissions and control access in several ways:

* **Secrets Manager administrator permissions:** To grant administrator permissions, attach the `SecretsManagerReadWrite` and `IAMFullAccess` IAM policies. Granting full administrator permissions to end users is not recommended because broad permissions like `IAMFullAccess` are not appropriate for most users. ([AWS Documentation][1])
* **Permissions to access secrets:** Identity‑based policies specify which IAM users, groups, or roles can perform actions on specific secrets. Resource‑based policies attached directly to a secret can also define who can access that secret. ([AWS Documentation][1])
* **Permissions for Lambda rotation functions:** For automated secret rotation, the Lambda function must have IAM permissions to access the secret and the service or database for which the secret contains credentials. ([AWS Documentation][1])
* **Permissions for encryption keys:** Secrets Manager uses AWS Key Management Service (KMS) to encrypt secrets. The default AWS managed key `aws/secretsmanager` has the correct permissions. If you use a customer‑managed KMS key, Secrets Manager must be granted permissions to use that key. ([AWS Documentation][1])
* **Permissions for replication:** You can control which identities are allowed to replicate secrets across AWS Regions using IAM policies. ([AWS Documentation][1])

Access control can also be refined using tag‑based (attribute‑based) access control (ABAC), where permissions are based on tags associated with identities and secrets. ([AWS Documentation][2])

Identity‑based policies can be attached to IAM identities (users, groups, roles) to specify allowed actions on secrets such as reading values, listing secrets, or creating new secrets. ([AWS Documentation][3])

For cross‑account access, both a resource policy on the secret and appropriate identity permissions in the requesting account are required to allow access from a different AWS account. ([AWS Documentation][4])

Secrets Manager also supports access from on‑premises environments using IAM Roles Anywhere to obtain temporary security credentials that follow IAM policies. ([AWS Documentation][5])

[1]: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html?utm_source=chatgpt.com "Authentication and access control for AWS Secrets Manager - AWS Secrets Manager"
[2]: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access-abac.html?utm_source=chatgpt.com "Control access to secrets using attribute-based access control (ABAC) - AWS Secrets Manager"
[3]: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_iam-policies.html?utm_source=chatgpt.com "Identity-based policies - AWS Secrets Manager"
[4]: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples_cross.html?utm_source=chatgpt.com "Access AWS Secrets Manager secrets from a different account - AWS Secrets Manager"
[5]: https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access-on-prem.html?utm_source=chatgpt.com "Access secrets from an on-premises environment - AWS Secrets Manager"
