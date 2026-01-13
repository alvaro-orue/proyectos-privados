-- Verificar si el esquema Push existe (usualmente ya existe)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Push')
BEGIN
    EXEC('CREATE SCHEMA [Push]')
END
GO

-- Eliminar tabla si existe (para migrar a nuevo schema)
IF OBJECT_ID('[Push].[SimulatedTransactions]', 'U') IS NOT NULL
    DROP TABLE [Push].[SimulatedTransactions];
GO

-- Crear la tabla con estructura real de Interbank Pago Push
CREATE TABLE [Push].[SimulatedTransactions] (
    -- Identificadores
    IdOrder NVARCHAR(100) NOT NULL,                      -- ID de orden del comercio
    IdTransactionPasarela NVARCHAR(100) PRIMARY KEY,     -- ID de transacción de la pasarela
    IdTransactionInterbank NVARCHAR(100) NOT NULL UNIQUE, -- ID generado por Interbank

    -- Comercio
    CommerceCode NVARCHAR(50) NOT NULL,                  -- Código del comercio
    CommerceName NVARCHAR(200) NOT NULL,                 -- Nombre del comercio

    -- Cliente
    CellPhoneNumber NVARCHAR(20) NOT NULL,               -- Teléfono del cliente

    -- Pago
    Amount DECIMAL(18, 2) NOT NULL,                      -- Monto
    Currency NVARCHAR(10) NOT NULL DEFAULT 'PEN',        -- Moneda (PEN, USD)

    -- Dispositivo
    DeviceIp NVARCHAR(50) NULL,                          -- IP del dispositivo
    DeviceType NVARCHAR(50) NULL,                        -- Tipo de dispositivo

    -- Estado
    Status NVARCHAR(20) NOT NULL DEFAULT 'PENDING',      -- PENDING, APPROVED, CANCELLED

    -- Metadata
    CreatedAt DATETIME DEFAULT GETDATE(),                -- Fecha creación
    UpdatedAt DATETIME NULL                              -- Fecha actualización
);
GO

-- Índices para búsquedas frecuentes
CREATE INDEX IX_SimulatedTransactions_IdOrder ON [Push].[SimulatedTransactions](IdOrder);
CREATE INDEX IX_SimulatedTransactions_Status ON [Push].[SimulatedTransactions](Status);
CREATE INDEX IX_SimulatedTransactions_CellPhoneNumber ON [Push].[SimulatedTransactions](CellPhoneNumber);
GO
