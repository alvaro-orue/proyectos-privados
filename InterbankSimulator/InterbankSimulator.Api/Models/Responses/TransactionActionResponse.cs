using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Responses;

/// <summary>
/// Response para confirmTransactionPayment y cancelationPaymentAuthorization
/// Estructura real de Interbank Pago Push según ENDPOINTS_CONSUMED_REPORT.md
/// NOTA: ResponseConfirmDto y ResponseCancelDto son clases vacías, por lo que response será null
/// </summary>
public class TransactionActionResponse
{
    [JsonPropertyName("code")]
    public string Code { get; set; } = "00";

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;

    /// <summary>
    /// Response es null para Confirm y Cancel (las clases DTO están vacías)
    /// </summary>
    [JsonPropertyName("response")]
    public object? Response { get; set; } = null;

    [JsonPropertyName("header")]
    public HeaderResponseDto? Header { get; set; }
}

/// <summary>
/// Response de error de Interbank
/// </summary>
public class ErrorResponseDto
{
    [JsonPropertyName("ErrorCode")]
    public string ErrorCode { get; set; } = string.Empty;

    [JsonPropertyName("ErrorMessage")]
    public string ErrorMessage { get; set; } = string.Empty;
}
