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

namespace IamChatbot.Dialogs
{
    public class HelpDialog : ComponentDialog
    {
        private uint questionCount = 0;
        public HelpDialog() : base(nameof(HelpDialog))
        {
            AddDialog(new TextPrompt("TextPrompt"));
            AddDialog(new ChoicePrompt(nameof(ChoicePrompt)));

            AddDialog(new WaterfallDialog("HelpFlow", new WaterfallStep[]
            {
                AskQuestionStepAsync,
                ProcessQuestionStepAsync,
                ContinueStepAsync,
                LoopDecisionStepAsync
            }));

            InitialDialogId = "HelpFlow";
        }

        // STEP 1: Ask what user needs help with
        private async Task<DialogTurnResult> AskQuestionStepAsync(
            WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            //await stepContext.Context.SendActivityAsync($"[HelpDialog][AskQuestionStep] ENTER");

            return await stepContext.PromptAsync("TextPrompt",
                new PromptOptions
                {
                    Prompt = MessageFactory.Text("I'm seeing that you are confused or have a question. How can I help?")
                }, cancellationToken);
        }

        // STEP 2: Call LLM (live)
        private async Task<DialogTurnResult> ProcessQuestionStepAsync(
            WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            var question = stepContext.Result?.ToString();
            questionCount++;
            //await stepContext.Context.SendActivityAsync("Retrieving Response");
            var answer = await GetChatbotAnswerForQuestion(question, cancellationToken);

            await stepContext.Context.SendActivityAsync(answer);

            return await stepContext.NextAsync();
        }

        // STEP 3: Ask if they want to continue or exit
        private async Task<DialogTurnResult> ContinueStepAsync(
            WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            return await stepContext.PromptAsync(nameof(ChoicePrompt),
                new PromptOptions
                {
                    Prompt = MessageFactory.Text("Do you need more help? (yes/no)"),
                    RetryPrompt = MessageFactory.Text("That was not a valid choice, please select a card or type in a key word of any option"),
                    Choices = GetUserDialogChoices()
                }, cancellationToken);
        }

        // STEP 4: Loop or Exit
        private async Task<DialogTurnResult> LoopDecisionStepAsync(
            WaterfallStepContext stepContext, CancellationToken cancellationToken)
        {
            string replyText = string.Empty;

            //await stepContext.Context.SendActivityAsync($"[HelpDialog][LoopDecisionStep] Input={((FoundChoice)stepContext.Result).Value}");

            switch (((FoundChoice)stepContext.Result).Value)
            {
                case "Yes":
                    return await stepContext.ReplaceDialogAsync(nameof(HelpDialog));

                case "No":
                    return await stepContext.EndDialogAsync("resume", cancellationToken);

                case "Contact Engineer":
                    replyText = "Summarizing our conversation and submitting artifact to the IAM engineering team.";
                    await stepContext.Context.SendActivityAsync(replyText);
                    return await stepContext.EndDialogAsync();

                default:
                    replyText = "I could not determine your selection. Please try again.";
                    await stepContext.Context.SendActivityAsync(replyText);
                    return await stepContext.EndDialogAsync();
            }
        }

        private async Task<string> GetChatbotAnswerForQuestion(string question, CancellationToken cancellationToken)
        {
            var options = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            var jsonData = JsonSerializer.Serialize(new
            {
                Question = question
            }, options);

            using (var httpClient = new HttpClient())
            {
                httpClient.BaseAddress = new Uri("http://127.0.0.1:8000");
                httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                using (var response = await httpClient.PostAsync("/generate_answer", new StringContent(jsonData, Encoding.UTF8, "application/json"), cancellationToken))
                {
                    using (var content = response.Content)
                    {
                        var result = await content.ReadAsStringAsync(cancellationToken);
                        options = new JsonSerializerOptions
                        {
                            PropertyNameCaseInsensitive = true
                        };
                        var ans = JsonSerializer.Deserialize<ChatbotQuestionAnswerResponse>(result, options);
                        return ans.Answer;
                    }
                }
            }
        }
        private IList<Choice> GetUserDialogChoices()
        {
            var cardOptions = new List<Choice>()
            {
                new Choice() { Value = "Yes", Synonyms = new List<string>() {"yes"}},
                new Choice() { Value = "No", Synonyms = new List<string>() {"no"}},
            };

            // If the user has been asking about a bunch of IAM questions, they might need to contact an engineer
            if (questionCount > 2)
            {
                cardOptions.Add(new Choice() { Value = "Contact Engineer", Synonyms = new List<string>() { "contact", "engineer" } });
            }
            return cardOptions;
        }
    }
}
