using Microsoft.AspNetCore.Mvc;
using InterbankSimulator.Api.Models.Requests;
using InterbankSimulator.Api.Models.Responses;
using InterbankSimulator.Api.Models;
using Dapper;
using System.Data;

namespace InterbankSimulator.Api.Controllers;

[ApiController]
[Route("pago-push/payment/v1")]
public class PaymentController : ControllerBase
{
    private readonly IDbConnection _dbConnection;
    private readonly ILogger<PaymentController> _logger;

    public PaymentController(IDbConnection dbConnection, ILogger<PaymentController> logger)
    {
        _dbConnection = dbConnection;
        _logger = logger;
    }

    /// <summary>
    /// Envía una solicitud de autorización de pago (simula envío al móvil del cliente)
    /// </summary>
    [HttpPost("sendPaymentAuthorizationRequestNotification")]
    public async Task<IActionResult> SendPaymentAuthorizationRequest([FromBody] PaymentAuthorizationRequest request)
    {
        _logger.LogInformation("💳 Solicitud de pago recibida: {PhoneNumber} - S/ {Amount}",
            request.PhoneNumber, request.Amount);

        // Generar datos simulados
        var uniqueId = Guid.NewGuid().ToString();
        var codeAuth = new Random().Next(100000, 999999).ToString();

        var transaction = new SimulatedTransaction
        {
            TransactionId = request.TransactionId,
            PhoneNumber = request.PhoneNumber,
            Amount = request.Amount,
            Status = "PENDING",
            CodeAuth = codeAuth,
            UniqueId = uniqueId,
            CreatedAt = DateTime.UtcNow.ToString("o")
        };

        // Insertar en SQLite
        var sql = @"
            INSERT INTO SimulatedTransactions
            (TransactionId, PhoneNumber, Amount, Status, CodeAuth, UniqueId, CreatedAt)
            VALUES
            (@TransactionId, @PhoneNumber, @Amount, @Status, @CodeAuth, @UniqueId, @CreatedAt)
        ";

        await _dbConnection.ExecuteAsync(sql, transaction);

        _logger.LogInformation("✅ Transacción guardada: UniqueId={UniqueId}, CodeAuth={CodeAuth}",
            uniqueId, codeAuth);

        var response = new PaymentAuthorizationResponse
        {
            UniqueId = uniqueId,
            CodeAuth = codeAuth,
            Status = "PENDING",
            Message = "Solicitud de pago enviada correctamente",
            TransactionId = request.TransactionId
        };

        return Ok(response);
    }

    /// <summary>
    /// Confirma una transacción de pago (simula aprobación del cliente)
    /// </summary>
    [HttpPost("confirmTransactionPayment")]
    public async Task<IActionResult> ConfirmTransaction([FromBody] TransactionActionRequest request)
    {
        _logger.LogInformation("✅ Confirmando transacción: UniqueId={UniqueId}", request.UniqueId);

        var sql = @"
            UPDATE SimulatedTransactions
            SET Status = 'APPROVED'
            WHERE UniqueId = @UniqueId
        ";

        var rowsAffected = await _dbConnection.ExecuteAsync(sql, new { request.UniqueId });

        if (rowsAffected == 0)
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {UniqueId}", request.UniqueId);
            return NotFound(new { Message = "Transacción no encontrada" });
        }

        var response = new TransactionActionResponse
        {
            Status = "APPROVED",
            Message = "Transacción aprobada exitosamente",
            TransactionId = request.TransactionId,
            UniqueId = request.UniqueId
        };

        return Ok(response);
    }

    /// <summary>
    /// Cancela una autorización de pago (simula rechazo del cliente)
    /// </summary>
    [HttpPost("cancelationPaymentAuthorization")]
    public async Task<IActionResult> CancelTransaction([FromBody] TransactionActionRequest request)
    {
        _logger.LogInformation("❌ Cancelando transacción: UniqueId={UniqueId}", request.UniqueId);

        var sql = @"
            UPDATE SimulatedTransactions
            SET Status = 'CANCELLED'
            WHERE UniqueId = @UniqueId
        ";

        var rowsAffected = await _dbConnection.ExecuteAsync(sql, new { request.UniqueId });

        if (rowsAffected == 0)
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {UniqueId}", request.UniqueId);
            return NotFound(new { Message = "Transacción no encontrada" });
        }

        var response = new TransactionActionResponse
        {
            Status = "CANCELLED",
            Message = "Transacción cancelada exitosamente",
            TransactionId = request.TransactionId,
            UniqueId = request.UniqueId
        };

        return Ok(response);
    }
}
