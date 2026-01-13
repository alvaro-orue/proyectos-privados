using System.Text.Json.Serialization;

namespace InterbankSimulator.Api.Models.Responses;

public class OAuthResponse
{
    [JsonPropertyName("token_type")]
    public string TokenType { get; set; } = "Bearer";

    [JsonPropertyName("access_token")]
    public string AccessToken { get; set; } = string.Empty;

    [JsonPropertyName("expires_in")]
    public string ExpiresIn { get; set; } = "3600";

    [JsonPropertyName("ext_expires_in")]
    public string ExtExpiresIn { get; set; } = "3600";
}
