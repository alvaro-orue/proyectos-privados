using Microsoft.AspNetCore.Mvc;
using InterbankSimulator.Api.Models.Requests;
using InterbankSimulator.Api.Models.Responses;
using InterbankSimulator.Api.Models;
using Dapper;
using System.Data;
using System.Diagnostics;

namespace InterbankSimulator.Api.Controllers;

[ApiController]
[Route("pago-push/payment/v1")]
public class PaymentController : ControllerBase
{
    private readonly IDbConnection _dbConnection;
    private readonly ILogger<PaymentController> _logger;

    // ========== CONFIGURACIÓN DE SIMULACIÓN PLIN ==========

    /// <summary>
    /// Números que serán APROBADOS (usuario acepta el pago)
    /// </summary>
    private static readonly HashSet<string> ApprovedPhoneNumbers = new()
    {
        "931988302"
    };

    /// <summary>
    /// Números que serán DENEGADOS (usuario rechaza el pago)
    /// </summary>
    private static readonly HashSet<string> DeniedPhoneNumbers = new()
    {
        "984210587"
    };

    /// <summary>
    /// Números que simularán TIMEOUT (usuario no responde)
    /// </summary>
    private static readonly HashSet<string> TimeoutPhoneNumbers = new()
    {
        "999999999"
    };

    /// <summary>
    /// Números NO registrados en PLIN
    /// </summary>
    private static readonly HashSet<string> NotRegisteredPhoneNumbers = new()
    {
        "900000000",
        "911111111"
    };

    /// <summary>
    /// Dispositivos simulados por número de teléfono
    /// </summary>
    private static readonly Dictionary<string, string> SimulatedDevices = new()
    {
        { "931988302", "SAMSUNG-SM-G998B" },
        { "984210587", "IPHONE-14-PRO-MAX" },
        { "999999999", "XIAOMI-MI-11" }
    };

    public PaymentController(IDbConnection dbConnection, ILogger<PaymentController> logger)
    {
        _dbConnection = dbConnection;
        _logger = logger;
    }

    /// <summary>
    /// Normaliza el número de celular (quita espacios, +51, 51)
    /// </summary>
    private static string NormalizePhoneNumber(string phone)
    {
        if (string.IsNullOrWhiteSpace(phone))
            return string.Empty;

        var normalized = phone.Replace(" ", "").Replace("-", "");

        if (normalized.StartsWith("+51"))
            normalized = normalized.Substring(3);
        else if (normalized.StartsWith("51") && normalized.Length == 11)
            normalized = normalized.Substring(2);

        return normalized;
    }

    /// <summary>
    /// Verifica si el número está registrado en PLIN
    /// </summary>
    private static bool IsPhoneRegisteredInPlin(string phone)
    {
        var normalized = NormalizePhoneNumber(phone);

        if (NotRegisteredPhoneNumbers.Contains(normalized))
            return false;

        return true; // Por defecto, cualquier número está registrado
    }

    /// <summary>
    /// Determina el resultado simulado del pago
    /// </summary>
    private static string GetSimulatedPaymentResult(string phone)
    {
        var normalized = NormalizePhoneNumber(phone);

        if (ApprovedPhoneNumbers.Contains(normalized))
            return "APPROVED";

        if (DeniedPhoneNumbers.Contains(normalized))
            return "DENIED";

        if (TimeoutPhoneNumbers.Contains(normalized))
            return "EXPIRED";

        return "APPROVED"; // Por defecto, aprobar
    }

    /// <summary>
    /// Obtiene el dispositivo simulado del usuario PLIN
    /// </summary>
    private static string GetSimulatedDevice(string phone)
    {
        var normalized = NormalizePhoneNumber(phone);
        return SimulatedDevices.TryGetValue(normalized, out var device) ? device : "GENERIC-ANDROID";
    }

    /// <summary>
    /// Genera el header con tiempos de transacción
    /// </summary>
    private static HeaderResponseDto GenerateHeader(DateTime startTime)
    {
        var endTime = DateTime.Now;
        var millis = (endTime - startTime).TotalMilliseconds;

        return new HeaderResponseDto
        {
            TransactionStartDatetime = startTime.ToString("yyyy-MM-ddTHH:mm:ss.fff"),
            TransactionEndDatetime = endTime.ToString("yyyy-MM-ddTHH:mm:ss.fff"),
            Millis = millis.ToString("F0")
        };
    }

    /// <summary>
    /// Envía una solicitud de autorización de pago (simula envío al móvil del cliente)
    /// </summary>
    [HttpPost("sendPaymentAuthorizationRequestNotification")]
    public async Task<IActionResult> SendPaymentAuthorizationRequest([FromBody] PaymentAuthorizationRequest request)
    {
        var startTime = DateTime.Now;
        var cellPhone = request.Customer.CellPhoneNumber;
        var normalizedPhone = NormalizePhoneNumber(cellPhone);

        _logger.LogInformation("💳 Solicitud de pago recibida: {CellPhone} - {Currency} {Amount}",
            cellPhone, request.Pay.Money, request.Pay.Amount);

        // ========== VALIDACIÓN DEL CELULAR ==========

        // Validar formato (9 dígitos, empieza con 9)
        if (string.IsNullOrEmpty(normalizedPhone) || normalizedPhone.Length != 9 || !normalizedPhone.StartsWith("9"))
        {
            _logger.LogWarning("❌ Formato de celular inválido: {CellPhone}", cellPhone);
            return Ok(new ErrorResponseDto
            {
                ErrorCode = "P03",
                ErrorMessage = "Formato de número de celular inválido. Debe ser 9 dígitos comenzando con 9."
            });
        }

        // Verificar si está registrado en PLIN
        if (!IsPhoneRegisteredInPlin(cellPhone))
        {
            _logger.LogWarning("❌ Celular NO registrado en PLIN: {CellPhone}", cellPhone);
            return Ok(new ErrorResponseDto
            {
                ErrorCode = "P01",
                ErrorMessage = "El número de celular no está registrado en PLIN"
            });
        }

        // ========== CREAR TRANSACCIÓN ==========

        var idTransactionInterbank = $"IBK-TRX-{Guid.NewGuid():N}".Substring(0, 24).ToUpper();
        var simulatedResult = GetSimulatedPaymentResult(cellPhone);
        var simulatedDevice = GetSimulatedDevice(cellPhone);

        var transaction = new SimulatedTransaction
        {
            IdOrder = request.IdOrder,
            IdTransactionPasarela = request.IdTransactionPasarela,
            IdTransactionInterbank = idTransactionInterbank,
            CommerceCode = request.Commerce.Code,
            CommerceName = request.Commerce.Name,
            CellPhoneNumber = normalizedPhone,
            Amount = request.Pay.Amount,
            Currency = request.Pay.Money,
            DeviceIp = request.Device.Ip,
            DeviceType = request.Device.Type,
            Status = "PENDING",
            CreatedAt = DateTime.UtcNow.ToString("o")
        };

        var sql = @"
            INSERT INTO SimulatedTransactions
            (IdOrder, IdTransactionPasarela, IdTransactionInterbank, CommerceCode, CommerceName,
             CellPhoneNumber, Amount, Currency, DeviceIp, DeviceType, Status, CreatedAt)
            VALUES
            (@IdOrder, @IdTransactionPasarela, @IdTransactionInterbank, @CommerceCode, @CommerceName,
             @CellPhoneNumber, @Amount, @Currency, @DeviceIp, @DeviceType, @Status, @CreatedAt)
        ";

        await _dbConnection.ExecuteAsync(sql, transaction);

        _logger.LogInformation("✅ Transacción creada: {IdTransactionInterbank} | Dispositivo: {Device} | Resultado simulado: {Result}",
            idTransactionInterbank, simulatedDevice, simulatedResult);

        var response = new PaymentAuthorizationResponse
        {
            Code = "00",
            Message = "Notificación enviada exitosamente",
            Response = new PaymentAuthorizationResponseData
            {
                Device = simulatedDevice,
                IdTransactionInterbank = idTransactionInterbank
            },
            Header = GenerateHeader(startTime)
        };

        return Ok(response);
    }

    /// <summary>
    /// Confirma una transacción de pago (simula aprobación del cliente)
    /// </summary>
    [HttpPost("confirmTransactionPayment")]
    public async Task<IActionResult> ConfirmTransaction([FromBody] ConfirmPaymentRequest request)
    {
        var startTime = DateTime.Now;

        _logger.LogInformation("✅ Confirmando transacción: {IdTransactionPasarela}", request.IdTransactionPasarela);

        // Buscar la transacción
        var findSql = @"
            SELECT IdTransactionInterbank, CellPhoneNumber, Status
            FROM SimulatedTransactions
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
            LIMIT 1
        ";

        var transaction = await _dbConnection.QueryFirstOrDefaultAsync<dynamic>(
            findSql, new { request.IdTransactionPasarela, request.IdOrder });

        if (transaction == null)
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {IdTransactionPasarela}", request.IdTransactionPasarela);
            return Ok(new ErrorResponseDto
            {
                ErrorCode = "404",
                ErrorMessage = "Transacción no encontrada"
            });
        }

        string cellPhone = transaction.CellPhoneNumber;
        string currentStatus = transaction.Status;

        // Verificar si ya fue procesada
        if (currentStatus != "PENDING")
        {
            return Ok(new TransactionActionResponse
            {
                Code = currentStatus == "APPROVED" ? "00" : "403",
                Message = $"Transacción ya fue procesada con estado: {currentStatus}",
                Response = null,
                Header = GenerateHeader(startTime)
            });
        }

        // ========== SIMULAR RESPUESTA DEL USUARIO ==========
        var simulatedResult = GetSimulatedPaymentResult(cellPhone);

        if (simulatedResult == "DENIED")
        {
            await _dbConnection.ExecuteAsync(
                "UPDATE SimulatedTransactions SET Status = 'DENIED' WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder",
                new { request.IdTransactionPasarela, request.IdOrder });

            _logger.LogInformation("❌ Usuario RECHAZÓ el pago: {CellPhone}", cellPhone);

            return Ok(new ErrorResponseDto
            {
                ErrorCode = "DN",
                ErrorMessage = "El usuario rechazó la solicitud de pago"
            });
        }

        if (simulatedResult == "EXPIRED")
        {
            await _dbConnection.ExecuteAsync(
                "UPDATE SimulatedTransactions SET Status = 'EXPIRED' WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder",
                new { request.IdTransactionPasarela, request.IdOrder });

            _logger.LogInformation("⏰ TIMEOUT - Usuario no respondió: {CellPhone}", cellPhone);

            return Ok(new ErrorResponseDto
            {
                ErrorCode = "EX",
                ErrorMessage = "Tiempo de espera agotado. El usuario no respondió."
            });
        }

        // ========== APROBAR TRANSACCIÓN ==========
        await _dbConnection.ExecuteAsync(
            "UPDATE SimulatedTransactions SET Status = 'APPROVED' WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder",
            new { request.IdTransactionPasarela, request.IdOrder });

        _logger.LogInformation("✅ Transacción APROBADA: {CellPhone}", cellPhone);

        return Ok(new TransactionActionResponse
        {
            Code = "00",
            Message = "Transacción confirmada exitosamente",
            Response = null,
            Header = GenerateHeader(startTime)
        });
    }

    /// <summary>
    /// Cancela una autorización de pago
    /// </summary>
    [HttpPost("cancelationPaymentAuthorization")]
    public async Task<IActionResult> CancelTransaction([FromBody] CancelPaymentRequest request)
    {
        var startTime = DateTime.Now;

        _logger.LogInformation("❌ Cancelando transacción: {IdTransactionPasarela}", request.IdTransactionPasarela);

        // Buscar la transacción
        var findSql = @"
            SELECT IdTransactionInterbank, CellPhoneNumber, Status
            FROM SimulatedTransactions
            WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder
            LIMIT 1
        ";

        var transaction = await _dbConnection.QueryFirstOrDefaultAsync<dynamic>(
            findSql, new { request.IdTransactionPasarela, request.IdOrder });

        if (transaction == null)
        {
            _logger.LogWarning("⚠️ Transacción no encontrada: {IdTransactionPasarela}", request.IdTransactionPasarela);
            return Ok(new ErrorResponseDto
            {
                ErrorCode = "404",
                ErrorMessage = "Transacción no encontrada"
            });
        }

        string currentStatus = transaction.Status;

        // Si ya fue procesada, retornar info
        if (currentStatus != "PENDING")
        {
            return Ok(new TransactionActionResponse
            {
                Code = currentStatus == "CANCELLED" ? "00" : "403",
                Message = $"Transacción ya fue procesada con estado: {currentStatus}",
                Response = null,
                Header = GenerateHeader(startTime)
            });
        }

        // ========== CANCELAR TRANSACCIÓN ==========
        await _dbConnection.ExecuteAsync(
            "UPDATE SimulatedTransactions SET Status = 'CANCELLED' WHERE IdTransactionPasarela = @IdTransactionPasarela OR IdOrder = @IdOrder",
            new { request.IdTransactionPasarela, request.IdOrder });

        _logger.LogInformation("🚫 Transacción CANCELADA");

        return Ok(new TransactionActionResponse
        {
            Code = "00",
            Message = "Transacción cancelada exitosamente",
            Response = null,
            Header = GenerateHeader(startTime)
        });
    }
}
