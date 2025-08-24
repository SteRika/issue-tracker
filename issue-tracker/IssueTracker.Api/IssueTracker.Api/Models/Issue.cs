namespace IssueTracker.Api.Models
{
    public class Issue
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Status { get; set; } = "open"; // open|in_progress|done
        public string Priority { get; set; } = "medium"; // low|medium|high
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
