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

        var createTableSql = @"
            CREATE TABLE IF NOT EXISTS SimulatedTransactions (
                TransactionId TEXT PRIMARY KEY,
                PhoneNumber TEXT NOT NULL,
                Amount REAL NOT NULL,
                Status TEXT NOT NULL DEFAULT 'PENDING',
                CodeAuth TEXT NOT NULL,
                UniqueId TEXT NOT NULL UNIQUE,
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
