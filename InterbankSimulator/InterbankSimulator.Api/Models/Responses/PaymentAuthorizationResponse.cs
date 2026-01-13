using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Responses;

/// <summary>
/// Response de sendPaymentAuthorizationRequestNotification
/// Estructura real de Interbank Pago Push
/// </summary>
public class PaymentAuthorizationResponse
{
    [JsonPropertyName("code")]
    public string Code { get; set; } = "00";

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;

    [JsonPropertyName("response")]
    public PaymentAuthorizationResponseData Response { get; set; } = new();
}

public class PaymentAuthorizationResponseData
{
    [JsonPropertyName("device")]
    public object Device { get; set; } = new { };

    [JsonPropertyName("idTransactionInterbank")]
    public string IdTransactionInterbank { get; set; } = string.Empty;
}
