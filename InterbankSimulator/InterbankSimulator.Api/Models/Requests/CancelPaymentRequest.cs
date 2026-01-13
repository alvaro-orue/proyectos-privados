using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Requests;

/// <summary>
/// Request para cancelationPaymentAuthorization
/// Estructura real de Interbank Pago Push
/// </summary>
public class CancelPaymentRequest
{
    [JsonPropertyName("idPasarela")]
    public string IdPasarela { get; set; } = "01";

    [JsonPropertyName("idOrder")]
    public string IdOrder { get; set; } = string.Empty;

    [JsonPropertyName("idTransactionPasarela")]
    public string IdTransactionPasarela { get; set; } = string.Empty;

    [JsonPropertyName("commerce")]
    public CommerceInfo Commerce { get; set; } = new();

    [JsonPropertyName("action")]
    public ActionInfo Action { get; set; } = new();

    [JsonPropertyName("device")]
    public DeviceInfo Device { get; set; } = new();
}

public class ActionInfo
{
    [JsonPropertyName("actionCode")]
    public string ActionCode { get; set; } = "00";

    [JsonPropertyName("actionMessage")]
    public string ActionMessage { get; set; } = "Cerro Pasarela";
}
