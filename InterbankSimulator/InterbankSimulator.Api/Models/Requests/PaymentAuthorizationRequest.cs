using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Requests;

/// <summary>
/// Request para sendPaymentAuthorizationRequestNotification
/// Estructura real de Interbank Pago Push
/// </summary>
public class PaymentAuthorizationRequest
{
    [JsonPropertyName("typeTransaction")]
    public string TypeTransaction { get; set; } = "02";

    [JsonPropertyName("idPasarela")]
    public string IdPasarela { get; set; } = "01";

    [JsonPropertyName("idOrder")]
    public string IdOrder { get; set; } = string.Empty;

    [JsonPropertyName("idTransactionPasarela")]
    public string IdTransactionPasarela { get; set; } = string.Empty;

    [JsonPropertyName("commerce")]
    public CommerceInfo Commerce { get; set; } = new();

    [JsonPropertyName("customer")]
    public CustomerInfo Customer { get; set; } = new();

    [JsonPropertyName("pay")]
    public PayInfo Pay { get; set; } = new();

    [JsonPropertyName("device")]
    public DeviceInfo Device { get; set; } = new();
}

public class CommerceInfo
{
    [JsonPropertyName("code")]
    public string Code { get; set; } = string.Empty;

    [JsonPropertyName("name")]
    public string Name { get; set; } = string.Empty;
}

public class CustomerInfo
{
    [JsonPropertyName("cellPhoneNumber")]
    public string CellPhoneNumber { get; set; } = string.Empty;
}

public class PayInfo
{
    [JsonPropertyName("amount")]
    public decimal Amount { get; set; }

    [JsonPropertyName("money")]
    public string Money { get; set; } = "PEN";
}

public class DeviceInfo
{
    [JsonPropertyName("ip")]
    public string Ip { get; set; } = string.Empty;

    [JsonPropertyName("type")]
    public string Type { get; set; } = string.Empty;
}
