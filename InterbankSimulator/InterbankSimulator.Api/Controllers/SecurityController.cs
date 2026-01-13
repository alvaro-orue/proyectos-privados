using Microsoft.AspNetCore.Mvc;
using InterbankSimulator.Api.Models.Responses;

namespace InterbankSimulator.Api.Controllers;

[ApiController]
[Route("pago-push/security/v1")]
public class SecurityController : ControllerBase
{
    private readonly ILogger<SecurityController> _logger;

    public SecurityController(ILogger<SecurityController> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Simula la autenticación OAuth de Interbank
    /// </summary>
    [HttpPost("oauth")]
    public IActionResult GetOAuthToken()
    {
        _logger.LogInformation("🔐 Generando token de autenticación simulado...");

        var response = new OAuthResponse
        {
            AccessToken = $"MOCK-TOKEN-{Guid.NewGuid():N}",
            TokenType = "Bearer",
            ExpiresIn = "3600",
            ExtExpiresIn = "3600"
        };

        return Ok(response);
    }
}
