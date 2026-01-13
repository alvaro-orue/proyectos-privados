using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Requests;

/// <summary>
/// Request para confirmTransactionPayment
/// Estructura real de Interbank Pago Push
/// </summary>
public class ConfirmPaymentRequest
{
    [JsonPropertyName("idPasarela")]
    public string IdPasarela { get; set; } = "01";

    [JsonPropertyName("idOrder")]
    public string IdOrder { get; set; } = string.Empty;

    [JsonPropertyName("idTransactionPasarela")]
    public string IdTransactionPasarela { get; set; } = string.Empty;

    [JsonPropertyName("commerce")]
    public CommerceInfo Commerce { get; set; } = new();

    [JsonPropertyName("transaction")]
    public TransactionInfo Transaction { get; set; } = new();

    [JsonPropertyName("device")]
    public DeviceInfo Device { get; set; } = new();
}

public class TransactionInfo
{
    [JsonPropertyName("resultCode")]
    public string ResultCode { get; set; } = string.Empty;

    [JsonPropertyName("resultMessage")]
    public string ResultMessage { get; set; } = string.Empty;

    [JsonPropertyName("result")]
    public string Result { get; set; } = string.Empty;

    [JsonPropertyName("currency")]
    public string Currency { get; set; } = string.Empty;

    [JsonPropertyName("amount")]
    public string Amount { get; set; } = string.Empty;

    [JsonPropertyName("authorizationDate")]
    public string AuthorizationDate { get; set; } = string.Empty;

    [JsonPropertyName("authorizationTime")]
    public string AuthorizationTime { get; set; } = string.Empty;

    [JsonPropertyName("authorizationCode")]
    public string AuthorizationCode { get; set; } = string.Empty;
}
