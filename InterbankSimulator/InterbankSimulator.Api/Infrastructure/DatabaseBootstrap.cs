using Dapper;
using Microsoft.Data.Sqlite;
using System.Data;

namespace InterbankSimulator.Api.Infrastructure;

public class DatabaseBootstrap
{
    private const string DatabaseFile = "simulator.db";
    private const string ConnectionString = "Data Source=simulator.db";

    public static void Initialize()
    {
        // Crear el archivo de base de datos si no existe
        if (!File.Exists(DatabaseFile))
        {
            Console.WriteLine("📁 Base de datos no encontrada. Creando simulator.db...");
            SqliteConnection.ClearAllPools();
            File.Create(DatabaseFile).Dispose();
        }

        // Crear la tabla si no existe
        using var connection = new SqliteConnection(ConnectionString);
        connection.Open();

        // Eliminar tabla antigua si existe (para migrar a nuevo schema)
        var dropTableSql = "DROP TABLE IF EXISTS SimulatedTransactions;";
        connection.Execute(dropTableSql);

        var createTableSql = @"
            CREATE TABLE IF NOT EXISTS SimulatedTransactions (
                IdOrder TEXT NOT NULL,
                IdTransactionPasarela TEXT PRIMARY KEY,
                IdTransactionInterbank TEXT NOT NULL UNIQUE,
                CommerceCode TEXT NOT NULL,
                CommerceName TEXT NOT NULL,
                CellPhoneNumber TEXT NOT NULL,
                Amount REAL NOT NULL,
                Currency TEXT NOT NULL DEFAULT 'PEN',
                DeviceIp TEXT,
                DeviceType TEXT,
                Status TEXT NOT NULL DEFAULT 'PENDING',
                CreatedAt TEXT NOT NULL
            );
        ";

        connection.Execute(createTableSql);
        Console.WriteLine("✅ Base de datos SQLite inicializada correctamente.");
        Console.WriteLine($"📍 Ubicación: {Path.GetFullPath(DatabaseFile)}");
    }

    public static IDbConnection CreateConnection()
    {
        return new SqliteConnection(ConnectionString);
    }
}
