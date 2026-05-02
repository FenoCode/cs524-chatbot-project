# Overview
This markdown defines the different domains of knowledge/information defined in this dataset for the NLP pipeline that will produce a model for the chatbot.

## Source Overview
1. Layer 1: General Technical Conversation Corpus
  - Teach the bot how people talk about technical questions, showing confusion, and the incompleteness of requirements
2. Layer 2: IAM Domain Knowledgebase
  - Provide authoritative, structured AIM knowledge that supports accurate guidance and clarification
  - Protocol explainations (SSO, SAML, OIDC)
3. Layer 3: Synthetic IAM Intake Dataset
  - Models structured conversations that transform vague requests into engineering-ready context

## Source References

1. General Technical Conversation Corpus
  - Helpdesk Ticket datasets
    - https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset [removed] (bad text/ticket content)
    - https://www.kaggle.com/datasets/tobiasbueck/multilingual-customer-support-tickets
    - http://data.mendeley.com/datasets/btm76zndnt/2 [removed] (no text data available, just ticket statistics/features)

2. IAM-related form posts corpus
  - https://security.stackexchange.com/questions/281987/understand-the-relationships-between-sso-oauth-oidc-saml-okta
  - https://github.com/orgs/community/discussions/169189
  - https://stackoverflow.com/questions/78964197/okta-saml-integration-for-single-sign-on

3. SSO Setup Guides
  - https://developer.okta.com/docs/guides/build-sso-integration/saml2/main/
  - https://developer.okta.com/docs/guides/build-sso-integration/openidconnect/main/
  - https://auth0.com/docs/authenticate/login/oidc-conformant-authentication/oidc-adoption-sso
  - https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols
  - https://docs.cloud.google.com/iam/docs/workforce-oauth-app

4. Integration Guides
  - https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html
  - https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html

5. IAM-related book PDFs

## Generated Datasets (`/generated_datasets`)

1. `iam-qa-dataset.jsonl`
  - Collection of Q/A pairs generated from source documents included in `/dataset` (excluding any CSVs)
2. `/generated_datasets/qa_split`
  - Q/A pairs associated from each source document
