// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Schema;
using Microsoft.Extensions.Logging;

namespace Microsoft.BotBuilderSamples
{
    public class DialogAndWelcomeBot<T> : DialogBot<T> where T : Dialog
    {
        public DialogAndWelcomeBot(ConversationState conversationState, UserState userState, T dialog, ILogger<DialogBot<T>> logger)
            : base(conversationState, userState, dialog, logger)
        {
        }

        protected override async Task OnMembersAddedAsync(
            IList<ChannelAccount> membersAdded,
            ITurnContext<IConversationUpdateActivity> turnContext,
            CancellationToken cancellationToken)
        {
            foreach (var member in membersAdded)
            {
                // Greet anyone that was not the target (recipient) of this message.
                // To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    var intro = MessageFactory.Text($"Hello, Alex. I am here to help with IAM (Identity and Access Management) requests.");

                    var functionOverview = MessageFactory.Text(
                        "My primary responsibility is to help you submit a SSO (Single-Sign On) integration request for you application. " +
                        "My secondary responsibility is to answer any IAM concept-related questions. "
                        );

                    var userExpectation = MessageFactory.Text(
                        "I'm here to ask you the right questions and direct you to the engineers who can make it happen. " +
                        "At any time, you can say things like 'I don't understand' where I will pause our interaction, divert to answering your question, and resume right back to where we were."
                        );

                    var userAction = MessageFactory.Text("Let me know when you are ready to begin.");
                    await turnContext.SendActivityAsync(intro, cancellationToken);
                    await turnContext.SendActivityAsync(functionOverview, cancellationToken);
                    await turnContext.SendActivityAsync(userExpectation, cancellationToken);
                    await turnContext.SendActivityAsync(userAction, cancellationToken);
                }
            }
        }
    }
}
