// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

using System.Threading;
using System.Threading.Tasks;
using IamChatbot.Dialogs;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Dialogs;

namespace Microsoft.BotBuilderSamples
{
    public class MainDialog : ComponentDialog
    {
        public MainDialog(SsoFlowDialog ssoFlowDialog, HelpDialog helpDialog) : base(nameof(MainDialog))
        {
            AddDialog(ssoFlowDialog);
            AddDialog(helpDialog); // Q/A Chatbot help dialogue. Can be thrown to when user is confused or requests information

            InitialDialogId = nameof(SsoFlowDialog);
        }
    }
}
