-- Verificar si el esquema Push existe (usualmente ya existe)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Push')
BEGIN
    EXEC('CREATE SCHEMA [Push]')
END
GO

-- Crear la tabla dentro del esquema Push
CREATE TABLE [Push].[SimulatedTransactions] (
    TransactionId NVARCHAR(50) PRIMARY KEY, -- ID único (GUID)
    PhoneNumber NVARCHAR(20) NOT NULL,      -- Teléfono simulado
    Amount DECIMAL(18, 2) NOT NULL,         -- Monto
    Status NVARCHAR(20) NOT NULL,           -- PENDING, APPROVED, CANCELLED
    CodeAuth NVARCHAR(10),                  -- Código simulado (ej: 123456)
    UniqueId NVARCHAR(50),                  -- ID interno simulado
    CreatedAt DATETIME DEFAULT GETDATE(),   -- Fecha creación
    UpdatedAt DATETIME NULL                 -- Fecha actualización
);
GO