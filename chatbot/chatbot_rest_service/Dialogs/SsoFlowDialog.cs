using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using IamChatbot.Model;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Builder.Dialogs.Choices;
using Microsoft.Bot.Schema;
using Microsoft.Extensions.Logging;

namespace IamChatbot.Dialogs
{
    public class SsoFlowDialog : ComponentDialog
    {
        protected readonly ILogger _logger;
        private UserInteractionRequestSummary interactionSummary;
        private readonly ConversationState _conversationState;

        public SsoFlowDialog(ILogger<SsoFlowDialog> logger, ConversationState conversationState) : base(nameof(SsoFlowDialog))
        {
            _logger = logger;
            _conversationState = conversationState;
            interactionSummary = new UserInteractionRequestSummary();

            AddDialog(new TextPrompt("TextPrompt"));
            AddDialog(new ChoicePrompt(nameof(ChoicePrompt)));
            AddDialog(new WaterfallDialog("MainFlow", new WaterfallStep[]
            {
                AskInteractionType,
                SelectInteractionAsync,
                SummaryStepAsync
            }));

            // Primary SSO question dialog flow
            AddDialog(new WaterfallDialog("SsoIntegrationRequestFlow", new WaterfallStep[]
            {
                AskApplicationName,
                AskApplicationDescription,
                AskApplicationType,
                HandleAppTypeStepAsync,
            }));

            // Dialog questions for COTS applications
            AddDialog(new WaterfallDialog("CustomAppSsoQuestionFlow", new WaterfallStep[]
            {
                AskTechStack,
                AskCurrentAuthMethod,
                AskOidcRequirements,
                FinalizeCustomApplicationInformation
            }));

            // Dialog questions for Custom Developed applications
            AddDialog(new WaterfallDialog("CotsSsoQuestionFlow", new WaterfallStep[]
            {
                AskSoftwareVersion,
                AskSoftwareVendorInformation,
                FinalizeCotsApplicationInformation
            }));

            InitialDialogId = "MainFlow";
        }

        /// <summary>
        /// Override to identify when help is needed for a particular step of a user. Can be activated at any time
        /// </summary>
        /// <param name="innerDc"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        protected override async Task<DialogTurnResult> OnContinueDialogAsync(
            DialogContext innerDc,
            CancellationToken cancellationToken)
        {
            var text = innerDc.Context.Activity.Text?.ToLowerInvariant();

            // If already in HelpDialog loop, skip to avoid recursive "HelpDialog" context pushes to stack
            if (innerDc.ActiveDialog?.Id == nameof(HelpDialog))
            {
                return await base.OnContinueDialogAsync(innerDc, cancellationToken);
            }

            if (!string.IsNullOrEmpty(text) && IsHelpIntent(text))
            {
                await innerDc.Context.SendActivityAsync("Pausing current flow to help you...");

                return await innerDc.BeginDialogAsync(nameof(HelpDialog), null, cancellationToken);
            }

            return await base.OnContinueDialogAsync(innerDc, cancellationToken);
        }

        private async Task<DialogTurnResult> AskInteractionType(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskStep] Result={stepContext.Result ?? "NULL"}");

            _logger.LogInformation("SsoFlowDialog.AskInteractionType");

            var options = new PromptOptions()
            {
                Prompt = MessageFactory.Text("What would you like me to help you with?"),
                RetryPrompt = MessageFactory.Text("That was not a valid choice, please select a card or type in a key word of any option"),
                Choices = GetUserDialogChoices(),
            };

            return await stepContext.PromptAsync(nameof(ChoicePrompt), options, cancellationToken);
        }

        private async Task<DialogTurnResult> SelectInteractionAsync(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            string replyText = "";

            // Selects which sub-flow to use depending on user's request
            switch (((FoundChoice)stepContext.Result).Value)
            {
                // NOTE: Can refactor so that the case statement flows to different dialogue names rather than writing them in-line
                case "SSO Request":
                    replyText = "Initializing SSO Request";
                    return await stepContext.BeginDialogAsync("SsoIntegrationRequestFlow", null, cancellationToken);
                case "Ask A Question":
                    replyText = "Transferring to Chatbot LLM";
                    return await stepContext.BeginDialogAsync(nameof(HelpDialog), null, cancellationToken);
                case "Contact Engineer":
                    // Display an Adaptive Card
                    replyText = "Submitting artifact to engineers";
                    break;

                default:
                    replyText = "I could not determine your selection. Please try again.";
                    break;
            }

            await stepContext.Context.SendActivityAsync(MessageFactory.Text(replyText), cancellationToken);
            return await stepContext.NextAsync();
        }

        private async Task<DialogTurnResult> AskApplicationName(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
           //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskApplicationName] Result={stepContext.Result ?? "NULL"}");

            await stepContext.Context.SendActivityAsync("Let's start with some basics so I can build a baseline for our engineers to work with.");

            string question = "Provide the full name of the application you want to integrate SSO with (e.g. \"Data Processing System (DPS)\")";
            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(question) },
                cancellationToken);
        }
        private async Task<DialogTurnResult> AskApplicationDescription(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            stepContext.Values["applicationName"] = (string)stepContext.Result;
            interactionSummary.ApplicationName = (string)stepContext.Result;

           //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskApplicationDescription] Result={stepContext.Result ?? "NULL"}");

            string question = "Provide a brief but informative description about the business use-case for this application.";

            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(question) },
                cancellationToken);
        }

        private async Task<DialogTurnResult> AskApplicationType(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskApplicationType] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["applicationDescription"] = (string)stepContext.Result;
            interactionSummary.ApplicationDescription = (string)stepContext.Result;

            var options = new PromptOptions()
            {
                Prompt = MessageFactory.Text("Is your application COTS (Customer Off the Shelf) or is it a custom developed application?"),
                RetryPrompt = MessageFactory.Text("That was not a valid choice, please select a card or type in a key word of any option"),
                Choices = GetApplicationTypeChoices(),
            };

            return await stepContext.PromptAsync(nameof(ChoicePrompt), options, cancellationToken);
        }

        private async Task<DialogTurnResult> HandleAppTypeStepAsync(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][HandleAppTypeStepAsync] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["applicationType"] = (string)((FoundChoice)stepContext.Result).Value;
            interactionSummary.ApplicationType = (string)((FoundChoice)stepContext.Result).Value;

            switch (((FoundChoice)stepContext.Result).Value)
            {
                case "COTS":
                    // Because it is COTS, we don't know the tech stack at this stage.
                    interactionSummary.ApplicationTechStack = "N/A";
                    return await stepContext.BeginDialogAsync("CotsSsoQuestionFlow", null, cancellationToken);

                case "Custom Developed":
                    // Because it is custom developed, there is not a vendor and version doesn't matter.
                    interactionSummary.ApplicationVendorInfomation = "N/A";
                    interactionSummary.ApplicationVersion = "N/A";
                    return await stepContext.BeginDialogAsync("CustomAppSsoQuestionFlow", null, cancellationToken);
                default:
                    string replyText = "I could not determine your selection. Please try again.";
                    await stepContext.Context.SendActivityAsync(replyText);
                    return await stepContext.EndDialogAsync();
            }
        }

        /* Series of questions for "CustomAppSsoQuestionFlow" waterfall dialog */
        private async Task<DialogTurnResult> AskTechStack(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskTechStack] Result={stepContext.Result ?? "NULL"}");

            await stepContext.Context.SendActivityAsync("Next, let's identify what tech stack your application is using. "+
                "The primary reason for asking this is to correctly identify what libraries and developer resources are available to decrease implementation complexity.");

            string question = "What is your application's tech stack? (e.g. [React + NextJS + SQL], [Vue + .NET + PostgresSQL]) ?";

            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(question) },
                cancellationToken);
        }

        private async Task<DialogTurnResult> AskCurrentAuthMethod(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskCurrentAuthMethod] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["applicationTechStack"] = (string)stepContext.Result;
            interactionSummary.ApplicationTechStack = (string)stepContext.Result;

            await stepContext.Context.SendActivityAsync("Now, I need to understand how users are currently authenticating (a.k.a. logging in). " +
                "Provide a brief description how it is done. If there are no authentication methods currently, please specify 'None'");

            string question = "So, how are users authenticating?";

            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(question) },
                cancellationToken);
        }

        private async Task<DialogTurnResult> AskOidcRequirements(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskOidcRequirements] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["authMethod"] = (string)stepContext.Result;
            interactionSummary.ApplicationCurrentAuthenticationMethod = (string)stepContext.Result;

            string prompt = $"For your application '{interactionSummary.ApplicationName}', we recommend OIDC (OpenId Connect). " +
                "At this stage, please provide a brief statement about your familiarity with OIDC and specify any up-front requirements you may already have such as scopes and redirect URL(s)";

            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(prompt) },
                cancellationToken);
        }
        private async Task<DialogTurnResult> FinalizeCustomApplicationInformation(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][FinalizeCustomApplicationInformation] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["oidcRequirements"] = (string)stepContext.Result;
            interactionSummary.OidcRequirements = (string)stepContext.Result;

            return await stepContext.NextAsync();
        }

        /* Series of questions for the CotsSsoQuestionFlow dialog */
        private async Task<DialogTurnResult> AskSoftwareVersion(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskSoftwareVersion] Result={stepContext.Result ?? "NULL"}");

            await stepContext.Context.SendActivityAsync($"For your application '{interactionSummary.ApplicationName}', we recommend the SAML protocol for your SSO integration. " +
                "An important piece of information is the current software version.");

            string prompt = "Please specify the software version if possible. Otherwise, put 'Unknown'";
            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(prompt) },
                cancellationToken);
        }

        private async Task<DialogTurnResult> AskSoftwareVendorInformation(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][AskSoftwareVendor] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["appVersion"] = (string)stepContext.Result;
            interactionSummary.ApplicationVersion = (string)stepContext.Result;

            await stepContext.Context.SendActivityAsync($"In order to best inform our engineers about your product, we need to know the software vendor and the primary website for '{interactionSummary.ApplicationName}'.");

            string prompt =$"Please specify the software vendor and the main website link. (e.g. Vendor Name - https://<vendor_product_site>.com";
            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions { Prompt = MessageFactory.Text(prompt) },
                cancellationToken);
        }
        private async Task<DialogTurnResult> FinalizeCotsApplicationInformation(WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][FinalizeCotsApplicationInformation] Result={stepContext.Result ?? "NULL"}");

            stepContext.Values["vendorName"] = (string)stepContext.Result;
            interactionSummary.ApplicationVendorInfomation = (string)stepContext.Result;

            return await stepContext.NextAsync();
        }

        private async Task<DialogTurnResult> SummaryStepAsync(
            WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[SsoFlowDialog][SummaryStep] Result={stepContext.Result ?? "NULL"}");

            await stepContext.Context.SendActivityAsync($"Thank you for providing information concerning your SSO integration for '{interactionSummary.ApplicationName}'. I am compiling the information and submitting a ticket to our IAM engineering team.");
            // Generate BERT summary of the conversation
            // 1. Build chat log string
            var logAccessor = _conversationState.CreateProperty<ConversationLog>("ConversationLog");
            var log = await logAccessor.GetAsync(stepContext.Context, () => new ConversationLog());
            var transcript = string.Join("\n", log.Turns);
            interactionSummary.ChatLog = transcript;

            var options = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            var jsonData = JsonSerializer.Serialize(new
            {
                Text = transcript
            }, options);

            // 2. Submit to BERT summarizer API service
            using (var httpClient = new HttpClient())
            {
                httpClient.BaseAddress = new Uri("http://127.0.0.1:8000");
                httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                
                using (var response = await httpClient.PostAsync("/generate_summary", new StringContent(jsonData, Encoding.UTF8, "application/json"), cancellationToken))
                {
                    using (var content = response.Content)
                    {
                        var result = await content.ReadAsStringAsync(cancellationToken);
                        await stepContext.Context.SendActivityAsync(result);
                        interactionSummary.ChatLogSummary = JsonSerializer.Deserialize<ChatbotSummaryResponse>(result);
                    }
                }
            }

            // Submit artifact to engineers in ths step
            /* Magic logc */
            interactionSummary.TicketSubmissionId = "INC234578";
            interactionSummary.TicketSubmissionLink = $"https://servicenow.com/id={interactionSummary.TicketSubmissionId}";

            // Generate user facing summary card
            var attachments = new List<Attachment>();
            var reply = MessageFactory.Attachment(attachments);
            reply.Attachments.Add(UserInteractionCardBuilder.CreateUserInteractionCard(interactionSummary));
            await stepContext.Context.SendActivityAsync(reply);

            return await stepContext.EndDialogAsync();
        }

        private bool IsHelpIntent(string input)
        {
            input = input.ToLower();
            return input.Contains("i need help")
                || input.Contains("i am confused")
                || input.Contains("i don't understand")
                || input.Contains("what does this mean");
        }

        private IList<Choice> GetUserDialogChoices()
        {
            var cardOptions = new List<Choice>()
            {
                new Choice() { Value = "SSO Request", Synonyms = new List<string>() { "sso", "integration", "request" }},
                new Choice() { Value = "Ask A Question", Synonyms = new List<string>() { "ask", "question" } },
                new Choice() { Value = "Contact Engineer", Synonyms = new List<string>() {"contact", "engineer"}},
            };
            return cardOptions;
        }

        private IList<Choice> GetApplicationTypeChoices()
        {
            var cardOptions = new List<Choice>()
            {
                new Choice() { Value = "COTS", Synonyms = new List<string>() {"shelf"}},
                new Choice() { Value = "Custom Developed", Synonyms = new List<string>() {"custom", "developed"}},
            };

            return cardOptions;
        }
    }
}
