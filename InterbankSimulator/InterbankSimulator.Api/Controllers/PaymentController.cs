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
        _logger.LogInformation("💳 Solicitud de pago recibida: {CellPhone} - {Currency} {Amount}",
            request.Customer.CellPhoneNumber, request.Pay.Money, request.Pay.Amount);

        // Generar ID de transacción Interbank simulado
        var idTransactionInterbank = Guid.NewGuid().ToString();

        var transaction = new SimulatedTransaction
        {
            IdOrder = request.IdOrder,
            IdTransactionPasarela = request.IdTransactionPasarela,
            IdTransactionInterbank = idTransactionInterbank,
            CommerceCode = request.Commerce.Code,
            CommerceName = request.Commerce.Name,
            CellPhoneNumber = request.Customer.CellPhoneNumber,
            Amount = request.Pay.Amount,
            Currency = request.Pay.Money,
            DeviceIp = request.Device.Ip,
            DeviceType = request.Device.Type,
            Status = "PENDING",
            CreatedAt = DateTime.UtcNow.ToString("o")
        };

        // Insertar en SQLite
        var sql = @"
            INSERT INTO SimulatedTransactions
            (IdOrder, IdTransactionPasarela, IdTransactionInterbank, CommerceCode, CommerceName,
             CellPhoneNumber, Amount, Currency, DeviceIp, DeviceType, Status, CreatedAt)
            VALUES
            (@IdOrder, @IdTransactionPasarela, @IdTransactionInterbank, @CommerceCode, @CommerceName,
             @CellPhoneNumber, @Amount, @Currency, @DeviceIp, @DeviceType, @Status, @CreatedAt)
        ";

        await _dbConnection.ExecuteAsync(sql, transaction);

        _logger.LogInformation("✅ Transacción guardada: IdTransactionInterbank={IdTransactionInterbank}",
            idTransactionInterbank);

        var response = new PaymentAuthorizationResponse
        {
            Code = "00",
            Message = "Solicitud de pago enviada correctamente",
            Response = new PaymentAuthorizationResponseData
            {
                Device = new { },
                IdTransactionInterbank = idTransactionInterbank
            }
        };

        return Ok(response);
    }

    /// <summary>
    /// Confirma una transacción de pago (simula aprobación del cliente)
    /// </summary>
    [HttpPost("confirmTransactionPayment")]
    public async Task<IActionResult> ConfirmTransaction([FromBody] ConfirmPaymentRequest request)
    {
        _logger.LogInformation("✅ Confirmando transacción: IdTransactionPasarela={IdTransactionPasarela}",
            request.IdTransactionPasarela);

        // Buscar la transacción por IdTransactionPasarela o IdOrder
        var findSql = @"
            SELECT IdTransactionInterbank FROM SimulatedTransactions
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
            LIMIT 1
        ";

        var idTransactionInterbank = await _dbConnection.QueryFirstOrDefaultAsync<string>(
            findSql, new { request.IdTransactionPasarela, request.IdOrder });

        if (string.IsNullOrEmpty(idTransactionInterbank))
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {IdTransactionPasarela}", request.IdTransactionPasarela);
            return NotFound(new {
                code = "01",
                message = "Transacción no encontrada"
            });
        }

        var updateSql = @"
            UPDATE SimulatedTransactions
            SET Status = 'APPROVED'
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
        ";

        await _dbConnection.ExecuteAsync(updateSql, new { request.IdTransactionPasarela, request.IdOrder });

        var response = new TransactionActionResponse
        {
            Code = "00",
            Message = "Transacción confirmada exitosamente",
            Response = new TransactionActionResponseData
            {
                IdTransactionInterbank = idTransactionInterbank
            }
        };

        return Ok(response);
    }

    /// <summary>
    /// Cancela una autorización de pago (simula rechazo del cliente)
    /// </summary>
    [HttpPost("cancelationPaymentAuthorization")]
    public async Task<IActionResult> CancelTransaction([FromBody] CancelPaymentRequest request)
    {
        _logger.LogInformation("❌ Cancelando transacción: IdTransactionPasarela={IdTransactionPasarela}",
            request.IdTransactionPasarela);

        // Buscar la transacción por IdTransactionPasarela o IdOrder
        var findSql = @"
            SELECT IdTransactionInterbank FROM SimulatedTransactions
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
            LIMIT 1
        ";

        var idTransactionInterbank = await _dbConnection.QueryFirstOrDefaultAsync<string>(
            findSql, new { request.IdTransactionPasarela, request.IdOrder });

        if (string.IsNullOrEmpty(idTransactionInterbank))
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {IdTransactionPasarela}", request.IdTransactionPasarela);
            return NotFound(new {
                code = "01",
                message = "Transacción no encontrada"
            });
        }

        var updateSql = @"
            UPDATE SimulatedTransactions
            SET Status = 'CANCELLED'
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
        ";

        await _dbConnection.ExecuteAsync(updateSql, new { request.IdTransactionPasarela, request.IdOrder });

        var response = new TransactionActionResponse
        {
            Code = "00",
            Message = "Transacción cancelada exitosamente",
            Response = new TransactionActionResponseData
            {
                IdTransactionInterbank = idTransactionInterbank
            }
        };

        return Ok(response);
    }
}
