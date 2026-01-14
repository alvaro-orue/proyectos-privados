using System.Data;

namespace InterbankSimulator.Api.Infrastructure;

/// <summary>
/// Clase de inicialización de base de datos (deshabilitada - ahora se usa SQL Server)
/// </summary>
public class DatabaseBootstrap
{
    public static void Initialize()
    {
        // Ya no es necesario con SQL Server
        // La tabla [Push].[SimulatedTransactions] ya existe en la BD
        Console.WriteLine("ℹ️ Usando SQL Server - No se requiere inicialización local.");
    }
}
