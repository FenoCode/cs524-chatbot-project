using IamChatbot.Model;

namespace IamChatbot
{
    public class UserInteractionRequestSummary
    {

        public string ApplicationType { get; set; }
        public string ApplicationName { get; set; }
        public string ApplicationDescription { get; set; }
        public string ApplicationEnvironment { get; set; } // On-Premise / Cloud / Hybrid / Custom Description
        public string ApplicationVendorInfomation { get; set; }
        public string ApplicationTechStack { get; set; }
        public string ApplicationVersion { get; set; } = "1.0";
        public string ApplicationCurrentAuthenticationMethod { get; set; }
        public string OidcRequirements { get; set; }
        public string TicketSubmissionId { get; set; }
        public string TicketSubmissionLink { get; set; }
        public string ChatLog { get; set; }
        public ChatbotSummaryResponse ChatLogSummary { get; set; }
    }
}
