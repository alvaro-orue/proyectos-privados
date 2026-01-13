using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Responses;

/// <summary>
/// Response de sendPaymentAuthorizationRequestNotification
/// Estructura real de Interbank Pago Push según ENDPOINTS_CONSUMED_REPORT.md
/// </summary>
public class PaymentAuthorizationResponse
{
    [JsonPropertyName("code")]
    public string Code { get; set; } = "00";

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;

    [JsonPropertyName("response")]
    public PaymentAuthorizationResponseData? Response { get; set; }

    [JsonPropertyName("header")]
    public HeaderResponseDto? Header { get; set; }
}

public class PaymentAuthorizationResponseData
{
    /// <summary>
    /// Identificador del dispositivo del usuario PLIN (ej: "SAMSUNG-SM-G998B")
    /// NOTA: Es un STRING, no un objeto
    /// </summary>
    [JsonPropertyName("device")]
    public string Device { get; set; } = string.Empty;

    [JsonPropertyName("idTransactionInterbank")]
    public string IdTransactionInterbank { get; set; } = string.Empty;
}

/// <summary>
/// Header con metadata de tiempos de transacción
/// </summary>
public class HeaderResponseDto
{
    [JsonPropertyName("transactionStartDatetime")]
    public string TransactionStartDatetime { get; set; } = string.Empty;

    [JsonPropertyName("transactionEndDatetime")]
    public string TransactionEndDatetime { get; set; } = string.Empty;

    [JsonPropertyName("millis")]
    public string Millis { get; set; } = string.Empty;
}
