namespace InterbankSimulator.Api.Models.Responses;

public class PaymentAuthorizationResponse
{
    public string UniqueId { get; set; } = string.Empty;
    public string CodeAuth { get; set; } = string.Empty;
    public string Status { get; set; } = "PENDING";
    public string Message { get; set; } = "Solicitud de pago enviada correctamente";
    public string TransactionId { get; set; } = string.Empty;
}
