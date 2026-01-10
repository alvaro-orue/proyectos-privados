using Microsoft.AspNetCore.Mvc;
using Dapper;
using System.Data;

namespace InterbankSimulator.Api.Controllers;

[ApiController]
[Route("api/simulator")]
public class SimulatorBackofficeController : ControllerBase
{
    private readonly IDbConnection _dbConnection;
    private readonly ILogger<SimulatorBackofficeController> _logger;

    public SimulatorBackofficeController(IDbConnection dbConnection, ILogger<SimulatorBackofficeController> logger)
    {
        _dbConnection = dbConnection;
        _logger = logger;
    }

    /// <summary>
    /// Fuerza la aprobación de un pago manualmente (Backoffice)
    /// </summary>
    [HttpPost("force-pay")]
    public async Task<IActionResult> ForcePay([FromBody] ForcePayRequest request)
    {
        _logger.LogInformation("🔧 Forzando aprobación de pago: {Identifier}", request.Identifier);

        // Buscar por TransactionId o UniqueId
        var sql = @"
            UPDATE SimulatedTransactions
            SET Status = 'APPROVED'
            WHERE TransactionId = @Identifier OR UniqueId = @Identifier
        ";

        var rowsAffected = await _dbConnection.ExecuteAsync(sql, new { request.Identifier });

        if (rowsAffected == 0)
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {Identifier}", request.Identifier);
            return NotFound(new
            {
                Success = false,
                Message = $"No se encontró ninguna transacción con ID: {request.Identifier}"
            });
        }

        _logger.LogInformation("✅ Pago forzado exitosamente para: {Identifier}", request.Identifier);

        return Ok(new
        {
            Success = true,
            Message = $"Transacción {request.Identifier} aprobada forzadamente",
            Status = "APPROVED"
        });
    }

    /// <summary>
    /// Lista todas las transacciones simuladas (para debugging)
    /// </summary>
    [HttpGet("transactions")]
    public async Task<IActionResult> GetAllTransactions()
    {
        var sql = "SELECT * FROM SimulatedTransactions ORDER BY CreatedAt DESC";
        var transactions = await _dbConnection.QueryAsync<dynamic>(sql);

        return Ok(new
        {
            Total = transactions.Count(),
            Transactions = transactions
        });
    }

    /// <summary>
    /// Obtiene una transacción específica por ID
    /// </summary>
    [HttpGet("transactions/{identifier}")]
    public async Task<IActionResult> GetTransaction(string identifier)
    {
        var sql = @"
            SELECT * FROM SimulatedTransactions
            WHERE TransactionId = @Identifier OR UniqueId = @Identifier
            LIMIT 1
        ";

        var transaction = await _dbConnection.QueryFirstOrDefaultAsync<dynamic>(sql, new { Identifier = identifier });

        if (transaction == null)
        {
            return NotFound(new { Message = "Transacción no encontrada" });
        }

        return Ok(transaction);
    }

    /// <summary>
    /// Limpia todas las transacciones (útil para testing)
    /// </summary>
    [HttpDelete("transactions/clear")]
    public async Task<IActionResult> ClearAllTransactions()
    {
        _logger.LogWarning("🗑️ Eliminando TODAS las transacciones de la base de datos...");

        var sql = "DELETE FROM SimulatedTransactions";
        await _dbConnection.ExecuteAsync(sql);

        return Ok(new
        {
            Success = true,
            Message = "Todas las transacciones han sido eliminadas"
        });
    }
}

public class ForcePayRequest
{
    public string Identifier { get; set; } = string.Empty; // Puede ser TransactionId o UniqueId
}
