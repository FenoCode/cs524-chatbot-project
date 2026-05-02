using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace IamChatbot
{
    public class ConversationLog
    {
        public List<string> Turns { get; set; } = new List<string>();
    }

    public class ConversationLoggingMiddleware : IMiddleware
    {
        private readonly IStatePropertyAccessor<ConversationLog> _logAccessor;

        public ConversationLoggingMiddleware(ConversationState conversationState)
        {
            _logAccessor = conversationState.CreateProperty<ConversationLog>("ConversationLog");
        }

        public async Task OnTurnAsync(
            ITurnContext turnContext,
            NextDelegate next,
            CancellationToken cancellationToken = default)
        {
            var log = await _logAccessor.GetAsync(
                turnContext,
                () => new ConversationLog(),
                cancellationToken);

            // Capture USER message
            if (turnContext.Activity.Type == ActivityTypes.Message &&
                turnContext.Activity.From.Role == "user")
            {
                log.Turns.Add($"User- {turnContext.Activity.Text}");
            }

            // Capture BOT responses
            turnContext.OnSendActivities(async (ctx, activities, nextSend) =>
            {
                foreach (var activity in activities)
                {
                    if (activity.Type == ActivityTypes.Message)
                    {
                        log.Turns.Add($"Bot- {activity.Text}");
                    }
                }

                return await nextSend();
            });

            await next(cancellationToken);
        }
    }
}
