namespace InterbankSimulator.Api.Models.Requests;

public class PaymentAuthorizationRequest
{
    public string PhoneNumber { get; set; } = string.Empty;
    public decimal Amount { get; set; }
    public string MerchantId { get; set; } = string.Empty;
    public string TransactionId { get; set; } = string.Empty;
    public string Currency { get; set; } = "PEN";
    public string Description { get; set; } = string.Empty;
}
