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
    Id INT IDENTITY(1,1) PRIMARY KEY,                  -- Identificador único de la tabla

    -- Cliente
    CellPhoneNumber NVARCHAR(20) NOT NULL,               -- Teléfono del cliente
    Device NVARCHAR(50) NOT NULL,                     -- Dispositivo del cliente
    [State] tinyint NOT NULL,
    
    -- Metadata
    CreateUser NVARCHAR(50) NOT NULL,                     -- Usuario que creó el registro
    UpdateUser NVARCHAR(50) NULL,                         -- Usuario que actualizó el registro
    CreatedAt DATETIME DEFAULT GETDATE(),                -- Fecha creación
    UpdatedAt DATETIME NULL                              -- Fecha actualización

);
GO
