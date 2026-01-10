namespace InterbankSimulator.Api.Models.Responses;

public class TransactionActionResponse
{
    public string Status { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string TransactionId { get; set; } = string.Empty;
    public string UniqueId { get; set; } = string.Empty;
}
