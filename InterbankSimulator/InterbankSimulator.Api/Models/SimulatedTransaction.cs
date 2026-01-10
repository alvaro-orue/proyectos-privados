namespace InterbankSimulator.Api.Models;

public class SimulatedTransaction
{
    public string TransactionId { get; set; } = string.Empty;
    public string PhoneNumber { get; set; } = string.Empty;
    public decimal Amount { get; set; }
    public string Status { get; set; } = "PENDING"; // PENDING, APPROVED, CANCELLED
    public string CodeAuth { get; set; } = string.Empty;
    public string UniqueId { get; set; } = string.Empty;
    public string CreatedAt { get; set; } = DateTime.UtcNow.ToString("o");
}
