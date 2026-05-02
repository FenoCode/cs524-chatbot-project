using System.Collections.Generic;
using AdaptiveCards;
using Microsoft.Bot.Schema;

namespace IamChatbot
{
    public static class UserInteractionCardBuilder
    {
        public static Attachment CreateUserInteractionCard(UserInteractionRequestSummary data)
        {
            var facts = new List<AdaptiveFact>();

            void AddFact(string title, string value)
            {
                if (!string.IsNullOrWhiteSpace(value))
                {
                    facts.Add(new AdaptiveFact(title, value));
                }
            }

            // Data mapping (easy to maintain)
            AddFact("Application Type", data.ApplicationType);
            AddFact("Application Name", data.ApplicationName);
            AddFact("Description", data.ApplicationDescription);
            AddFact("Environment", data.ApplicationEnvironment);
            AddFact("Vendor", data.ApplicationVendorInfomation);
            AddFact("Tech Stack", data.ApplicationTechStack);
            AddFact("Version", data.ApplicationVersion);
            AddFact("Authentication", data.ApplicationCurrentAuthenticationMethod);
            AddFact("OIDC Requirements", data.OidcRequirements);
            AddFact("ChatLog Summary", data.ChatLogSummary.Summary);

            var body = new List<AdaptiveElement>
        {
            // Header
            new AdaptiveContainer
            {
                Style = AdaptiveContainerStyle.Emphasis,
                Items = new List<AdaptiveElement>
                {
                    new AdaptiveTextBlock
                    {
                        Text = "Application Summary",
                        Weight = AdaptiveTextWeight.Bolder,
                        Size = AdaptiveTextSize.Large,
                        Wrap = true
                    },
                    new AdaptiveTextBlock
                    {
                        Text = "User-provided onboarding details",
                        IsSubtle = true,
                        Wrap = true,
                        Spacing = AdaptiveSpacing.Small
                    }
                }
            },

            // Main content
            new AdaptiveContainer
            {
                Spacing = AdaptiveSpacing.Medium,
                Items = new List<AdaptiveElement>
                {
                    new AdaptiveFactSet
                    {
                        Facts = facts
                    }
                }
            }
        };

            // Actions (button)
            var actions = new List<AdaptiveAction>();

            if (!string.IsNullOrWhiteSpace(data.TicketSubmissionId) &&
                !string.IsNullOrWhiteSpace(data.TicketSubmissionLink))
            {
                actions.Add(new AdaptiveOpenUrlAction
                {
                    Title = $"View Ticket: {data.TicketSubmissionId}",
                    Url = new System.Uri(data.TicketSubmissionLink)
                });
            }

            var card = new AdaptiveCard(new AdaptiveSchemaVersion(1, 4))
            {
                Body = body,
                Actions = actions
            };

            return new Attachment
            {
                ContentType = "application/vnd.microsoft.card.adaptive",
                Content = card
            };
        }
    }
}
