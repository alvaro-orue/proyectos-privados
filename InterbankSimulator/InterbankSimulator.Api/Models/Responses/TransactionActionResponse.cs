using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Responses;

/// <summary>
/// Response generico para confirmTransactionPayment y cancelationPaymentAuthorization
/// Estructura real de Interbank Pago Push
/// </summary>
public class TransactionActionResponse
{
    [JsonPropertyName("code")]
    public string Code { get; set; } = "00";

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;

    [JsonPropertyName("response")]
    public TransactionActionResponseData? Response { get; set; }
}

public class TransactionActionResponseData
{
    [JsonPropertyName("idTransactionInterbank")]
    public string IdTransactionInterbank { get; set; } = string.Empty;
}
