# cs524-chatbot-project
Repo that contains code for the final project of CS524 Natural Language Processing Course.

## Quickstart Guide
Instructions on how to run the project here...

## Chatbot HLD (High Level Design)
This section defines my personal motivation for this project and the MVP feature set.

### Chatbot Sector
I have chosen the IAM (Identity and Access Management) space for my chatbot project because of its direct relationship to my job title.

### Intended Impact
This chatbot will reduce friction between IAM engineers and customers desiring integrations (SSO, secrets management, identity provisioning) by expediting understanding between the parties and compiling information to inform architectural decisions.

### Chatbot Tone
This chatbot will have the tone of a senior IAM engineer that is patient and mindful of the user's lack of IAM knowledge and driven to creating a positive customer interaction that is satisfactory to the user and the IAM team.

### Chatbot Purpose
The chatbot applies a structured IAM knowledge base to act as a senior intake engineer, guiding users through domain-specific conversations that convert incomplete or unclear requests into engineering-ready integration context. This chatbot will submit a ticket/artifact that provides context needed for a human IAM engineer to finish the integration with the end-customer for a productive and successful engagement. This chatbot's goal is to eliminate the repetitive sync that has to occur for the IAM engineer to understand what the customer needs and expedite the timeline for a functional and satisfactory integration with IAM resources.

It will utilize a hybrid model that primarily relies on structured responses and flows that guides to a final outcome. It will utilize an IAM knowledge base in cases where the flow is unable to continue due to customer concern or lack of knowledge. The knowledgebase responses will be a support mechanism to regain traction and drive to the an outcome that provides an enriched context artifact for the IAM engineer to continue to completion.

### Chatbot Motivation
As an IAM engineer, I constantly have to ask the same questions over and over to receive the correct technical details to know how to properly integrate with their application to provide the best value-added IAM resources that we have. Most of the time, it is SSO (Single-Sign On), but there have been many missed opportunities because the customer simply didn't know our offerings and how it could solve Cybersecurity requirements.

## Chatbox Tech Stack
This chatbot will be using the `Microsoft Bot Framework` to be the primary chat engine for programming the user flow interaction logic and maintaining the chat state with the user. It will utilize a local `GPT4All` server for LLM prompting and RAG (Retrieval Augmented Generation) for knowledgebase retrieval.

The `GPT4All` server will handle responses from the user that are either non-standard or retrieve information about a topic that a user asks about.

*NOTE:* It is still being determined how the custom python NLP pipeline will be introduced into this project because the LLM will be doing much of the heavy lifting, which isn't great for an academic exercise. Things like 'intent analysis' maybe introduced so that a custom NLP pipeline can be populated.

### Layer Diagram
```text
User --> Bot Framework (dialog + state)
         ↕
   GPT4All API Server (LLM responses)
         ↕
      Simple RAG layer or embedding store
         ↕
 Knowledge base (synthetic intake templates, IAM docs)
```

### *Experimental Architecture*
The running idea of integrating a custom NLP pipeline will be offering a REST-API microservice that can determine user intent to drive the interaction flow with the chatbot service. Utilizing the example in the `Natural Language Processing with Python by Cuantum`, we can use a corpus that can determine what category of request the user is talking about.

Examples:
- General IAM help
- SSO Integration (for MVP of chatbot)
- Secrets Onboarding
- Role Onboarding

### References
Links reguarding to repos and docs used to build this project.
#### Bot Framework SDK
- Repo: https://github.com/microsoft/botbuilder-dotnet?tab=readme-ov-file
- Docs: https://learn.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0
- Bot Framework Components: https://github.com/BotBuilderCommunity/botbuilder-community-dotnet
- Bot Examples: https://github.com/microsoft/BotBuilder-Samples/tree/main