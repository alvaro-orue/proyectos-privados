namespace InterbankSimulator.Api.Models;

public class SimulatedTransaction
{
    // Identificadores
    public string IdOrder { get; set; } = string.Empty;
    public string IdTransactionPasarela { get; set; } = string.Empty;
    public string IdTransactionInterbank { get; set; } = string.Empty;

    // Comercio
    public string CommerceCode { get; set; } = string.Empty;
    public string CommerceName { get; set; } = string.Empty;

    // Cliente
    public string CellPhoneNumber { get; set; } = string.Empty;

    // Pago
    public decimal Amount { get; set; }
    public string Currency { get; set; } = "PEN";

    // Dispositivo
    public string DeviceIp { get; set; } = string.Empty;
    public string DeviceType { get; set; } = string.Empty;

    // Estado
    public string Status { get; set; } = "PENDING"; // PENDING, APPROVED, CANCELLED

    // Metadata
    public string CreatedAt { get; set; } = DateTime.UtcNow.ToString("o");
}
