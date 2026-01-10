namespace InterbankSimulator.Api.Models.Requests;

public class TransactionActionRequest
{
    public string TransactionId { get; set; } = string.Empty;
    public string UniqueId { get; set; } = string.Empty;
    public string CodeAuth { get; set; } = string.Empty;
}
