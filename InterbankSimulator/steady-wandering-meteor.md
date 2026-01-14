# Plan de Implementacion: Validacion de Afiliacion PLIN desde SQL Server

## Objetivo
Modificar el endpoint `sendPaymentAuthorizationRequestNotification` para consultar la tabla `[Push].[SimulatedTransactions]` en SQL Server y determinar si un numero de celular esta afiliado a PLIN basandose en la columna `State`.

## Logica de Negocio
- `State = 1` → El CellPhoneNumber **esta afiliado** a PLIN
- `State != 1` o no existe → El CellPhoneNumber **NO esta afiliado** a PLIN

---

## Respuestas del Endpoint

### Caso 1: Celular AFILIADO (State = 1)

Cuando el registro existe en la BD y `State = 1`, retorna exito con el `device` de la BD:

```json
{
  "code": "00",
  "message": "Notificación enviada exitosamente",
  "response": {
    "device": "SAMSUNG-SM-G998B",
    "idTransactionInterbank": "IBK-TRX-9F434A3877DF4EF8"
  },
  "header": {
    "transactionStartDatetime": "2026-01-13T12:51:57.022",
    "transactionEndDatetime": "2026-01-13T12:51:57.037",
    "millis": "15"
  }
}
```

**Nota:** El valor de `response.device` viene directamente de la columna `[Device]` de la tabla `[Push].[SimulatedTransactions]`.

### Caso 2: Celular NO AFILIADO (State != 1 o no existe)

Cuando el registro NO existe en la BD o `State != 1`, retorna error P01:

```json
{
  "ErrorCode": "P01",
  "ErrorMessage": "El número de celular no está registrado en PLIN"
}
```

**Condiciones para retornar este error:**
- El `CellPhoneNumber` no existe en la tabla
- El `CellPhoneNumber` existe pero `State = 0` (u otro valor distinto de 1)

---

## Estructura de la Tabla SQL Server

### Tabla: `[Push].[SimulatedTransactions]`

| Columna | Tipo de Dato | Nullable | Descripcion |
|---------|--------------|----------|-------------|
| `Id` | INT IDENTITY(1,1) | NOT NULL | PK - Identificador unico |
| `CellPhoneNumber` | NVARCHAR(20) | NOT NULL | Telefono del cliente |
| `Device` | NVARCHAR(50) | NOT NULL | Dispositivo del cliente |
| `State` | TINYINT | NOT NULL | **1 = Afiliado, 0 = No afiliado** |
| `CreateUser` | NVARCHAR(50) | NOT NULL | Usuario que creo el registro |
| `UpdateUser` | NVARCHAR(50) | NULL | Usuario que actualizo el registro |
| `CreatedAt` | DATETIME | DEFAULT GETDATE() | Fecha de creacion |
| `UpdatedAt` | DATETIME | NULL | Fecha de actualizacion |

### Script de Creacion

```sql
-- Crear esquema si no existe
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Push')
BEGIN
    EXEC('CREATE SCHEMA [Push]')
END
GO

-- Crear tabla
CREATE TABLE [Push].[SimulatedTransactions] (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CellPhoneNumber NVARCHAR(20) NOT NULL,
    Device NVARCHAR(50) NOT NULL,
    [State] TINYINT NOT NULL,
    CreateUser NVARCHAR(50) NOT NULL,
    UpdateUser NVARCHAR(50) NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME NULL
);
GO
```

### Data Actual en la Tabla

| Id | CellPhoneNumber | Device | State | CreateUser | Afiliacion |
|----|-----------------|--------|-------|------------|------------|
| 1 | 911111111 | Samsung Galaxy S23 | 1 | TR11439 | Afiliado |
| 2 | 922222222 | Google Pixel 8 | 0 | TR11439 | **NO Afiliado** |
| 3 | 933333333 | Huawei P40 | 1 | TR11439 | Afiliado |

---

## Estado Actual del Proyecto

| Componente | Estado |
|------------|--------|
| Dapper | Ya instalado (v2.1.66) |
| IDbConnection | Ya inyectado en PaymentController |
| Microsoft.Data.SqlClient | Falta agregar |
| SQLite | Actualmente en uso (a reemplazar) |

---

## Archivos a Modificar

| Archivo | Accion |
|---------|--------|
| `InterbankSimulator.Api/InterbankSimulator.Api.csproj` | Agregar paquete Microsoft.Data.SqlClient |
| `InterbankSimulator.Api/appsettings.json` | Agregar ConnectionStrings |
| `InterbankSimulator.Api/Program.cs` | Cambiar SqliteConnection por SqlConnection |
| `InterbankSimulator.Api/Controllers/PaymentController.cs` | Modificar `IsPhoneRegisteredInPlin()` |

---

## Paso 1: Agregar Paquete NuGet

**Archivo:** `InterbankSimulator.Api/InterbankSimulator.Api.csproj`

Agregar la referencia a `Microsoft.Data.SqlClient`:

```xml
<ItemGroup>
  <PackageReference Include="Dapper" Version="2.1.66" />
  <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="10.0.0" />
  <PackageReference Include="Microsoft.Data.SqlClient" Version="5.2.2" />  <!-- AGREGAR -->
  <PackageReference Include="Microsoft.Data.Sqlite" Version="10.0.1" />    <!-- Opcional: eliminar si no se usara -->
  <PackageReference Include="Swashbuckle.AspNetCore" Version="10.1.0" />
</ItemGroup>
```

**Comando alternativo:**
```bash
cd InterbankSimulator.Api && dotnet add package Microsoft.Data.SqlClient
```

---

## Paso 2: Configurar Connection String

**Archivo:** `InterbankSimulator.Api/appsettings.json`

Agregar seccion `ConnectionStrings`:

```json
{
  "ConnectionStrings": {
    "SqlServerConnection": "Server=MC0780;Database=PUNTOWEB;User Id=PUNTOUSER;Password=!908@N61@D0#;TrustServerCertificate=True;Min Pool Size=10;Max Pool Size=100;"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      }
    }
  }
}
```

---

## Paso 3: Actualizar Program.cs

**Archivo:** `InterbankSimulator.Api/Program.cs`

### 3.1 Cambiar el using statement

```csharp
// ANTES
using Microsoft.Data.Sqlite;

// DESPUES
using Microsoft.Data.SqlClient;
```

### 3.2 Cambiar la inyeccion de IDbConnection

```csharp
// ANTES (SQLite) - lineas 17-22
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connection = new SqliteConnection("Data Source=simulator.db");
    connection.Open();
    return connection;
});

// DESPUES (SQL Server)
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connectionString = builder.Configuration.GetConnectionString("SqlServerConnection");
    var connection = new SqlConnection(connectionString);
    connection.Open();
    return connection;
});
```

### 3.3 (Opcional) Eliminar inicializacion de DatabaseBootstrap

Si ya no se usara SQLite, comentar o eliminar la linea 26:

```csharp
// DatabaseBootstrap.Initialize();  // Ya no es necesario con SQL Server
```

---

## Paso 4: Modificar PaymentController.cs

**Archivo:** `InterbankSimulator.Api/Controllers/PaymentController.cs`

### 4.1 Eliminar HashSets y Diccionarios estaticos

Eliminar estas lineas ya que la validacion y el Device vendran de la BD:

```csharp
// ELIMINAR - HashSet NotRegisteredPhoneNumbers (lineas 44-51)
private static readonly HashSet<string> NotRegisteredPhoneNumbers = new()
{
    "900000000",
    "911111111"
};

// ELIMINAR - Dictionary SimulatedDevices (lineas 56-61)
private static readonly Dictionary<string, string> SimulatedDevices = new()
{
    { "931988302", "SAMSUNG-SM-G998B" },
    { "984210587", "IPHONE-14-PRO-MAX" },
    { "999999999", "XIAOMI-MI-11" }
};
```

### 4.2 Eliminar metodo `GetSimulatedDevice()`

Ya no sera necesario (lineas 119-126):

```csharp
// ELIMINAR
private static string GetSimulatedDevice(string phone)
{
    var normalized = NormalizePhoneNumber(phone);
    return SimulatedDevices.TryGetValue(normalized, out var device) ? device : "GENERIC-ANDROID";
}
```

### 4.3 Crear DTO para resultado de afiliacion

Agregar clase interna o record para el resultado de la consulta:

```csharp
// AGREGAR - Record para resultado de consulta PLIN
private record PlinAffiliationResult(byte State, string Device);
```

### 4.4 Cambiar metodo `IsPhoneRegisteredInPlin()` por `GetPlinAffiliationAsync()`

Convertir de metodo estatico a metodo de instancia que retorne State y Device:

```csharp
// ANTES (estatico con HashSet) - lineas 90-98
private static bool IsPhoneRegisteredInPlin(string phone)
{
    var normalized = NormalizePhoneNumber(phone);

    if (NotRegisteredPhoneNumbers.Contains(normalized))
        return false;

    return true;
}

// DESPUES (consulta a SQL Server con Dapper - retorna State y Device)
private async Task<PlinAffiliationResult?> GetPlinAffiliationAsync(string phone)
{
    var normalized = NormalizePhoneNumber(phone);

    var sql = @"
        SELECT [State], [Device]
        FROM [Push].[SimulatedTransactions]
        WHERE CellPhoneNumber = @CellPhoneNumber
    ";

    var result = await _dbConnection.QueryFirstOrDefaultAsync<PlinAffiliationResult>(
        sql,
        new { CellPhoneNumber = normalized }
    );

    return result;
}
```

### 4.5 Actualizar logica en `SendPaymentAuthorizationRequest()`

Modificar la validacion y uso del Device (lineas 170-185):

```csharp
// ANTES
if (!IsPhoneRegisteredInPlin(cellPhone))
{
    _logger.LogWarning("❌ Celular NO registrado en PLIN: {CellPhone}", cellPhone);
    return Ok(new ErrorResponseDto
    {
        ErrorCode = "P01",
        ErrorMessage = "El número de celular no está registrado en PLIN"
    });
}

// ... mas codigo ...

var simulatedDevice = GetSimulatedDevice(cellPhone);

// DESPUES
var plinAffiliation = await GetPlinAffiliationAsync(cellPhone);

// Validar: no existe en BD o State != 1
if (plinAffiliation == null || plinAffiliation.State != 1)
{
    _logger.LogWarning("❌ Celular NO registrado en PLIN: {CellPhone}", cellPhone);
    return Ok(new ErrorResponseDto
    {
        ErrorCode = "P01",
        ErrorMessage = "El número de celular no está registrado en PLIN"
    });
}

// Usar Device de la BD para el response
var simulatedDevice = plinAffiliation.Device;
```

### 4.6 Actualizar construccion del Response

El response ya usara el `simulatedDevice` que ahora viene de la BD:

```csharp
var response = new PaymentAuthorizationResponse
{
    Code = "00",
    Message = "Notificación enviada exitosamente",
    Response = new PaymentAuthorizationResponseData
    {
        Device = simulatedDevice,  // <-- Ahora viene de [Push].[SimulatedTransactions].Device
        IdTransactionInterbank = idTransactionInterbank
    },
    Header = GenerateHeader(startTime)
};
```

---

## Resumen de Cambios

```
InterbankSimulator.Api/
├── InterbankSimulator.Api.csproj  [MODIFICAR] - Agregar Microsoft.Data.SqlClient
├── appsettings.json               [MODIFICAR] - Agregar ConnectionStrings
├── Program.cs                     [MODIFICAR] - SqliteConnection -> SqlConnection
└── Controllers/
    └── PaymentController.cs       [MODIFICAR]
        - ELIMINAR: HashSet NotRegisteredPhoneNumbers
        - ELIMINAR: Dictionary SimulatedDevices
        - ELIMINAR: Metodo GetSimulatedDevice()
        - AGREGAR:  Record PlinAffiliationResult
        - AGREGAR:  Metodo GetPlinAffiliationAsync() (retorna State + Device)
        - MODIFICAR: Logica en SendPaymentAuthorizationRequest()
```

---

## Verificacion

1. **Restaurar paquetes:**
   ```bash
   cd InterbankSimulator.Api && dotnet restore
   ```

2. **Compilar el proyecto:**
   ```bash
   dotnet build InterbankSimulator.Api
   ```

3. **Ejecutar el proyecto:**
   ```bash
   cd InterbankSimulator.Api && dotnet run
   ```

4. **Probar con Swagger (http://localhost:5000):**

   | CellPhoneNumber | State | Device en BD | Resultado Esperado |
   |-----------------|-------|--------------|-------------------|
   | 911111111 | 1 | Samsung Galaxy S23 | Exito - Response.Device = "Samsung Galaxy S23" |
   | 922222222 | 0 | Google Pixel 8 | Error P01 (no afiliado) |
   | 933333333 | 1 | Huawei P40 | Exito - Response.Device = "Huawei P40" |
   | 999999999 | - | No existe | Error P01 (no existe en BD) |

---

## Notas Importantes

### Prerrequisitos SQL Server
- La tabla `[Push].[SimulatedTransactions]` debe existir en SQL Server
- El usuario de la cadena de conexion debe tener permisos SELECT sobre la tabla
- El campo `State` es `TINYINT`: 1 = afiliado, 0 = no afiliado

### Sobre Dapper (Ya Configurado)
- **Ya esta instalado** en el proyecto (v2.1.66)
- El controlador ya usa `IDbConnection` inyectado
- Los metodos Dapper disponibles:
  - `QueryFirstOrDefaultAsync<T>` - Para consultas que retornan un solo valor o null
  - `QueryAsync<T>` - Para consultas que retornan multiples registros
  - `ExecuteAsync` - Para INSERT/UPDATE/DELETE (ya usado en el controller)

### Consideraciones de Produccion
- Usar variables de entorno o User Secrets para credenciales
- Considerar connection pooling (SqlConnection lo maneja automaticamente)
- Agregar manejo de excepciones para errores de conexion a BD

---

## Datos de Prueba Adicionales

```sql
-- Insertar nuevos numeros de prueba
INSERT INTO [Push].[SimulatedTransactions]
    (CellPhoneNumber, Device, [State], CreateUser)
VALUES
    ('944444444', 'iPhone 15 Pro', 1, 'TR11439'),      -- Afiliado
    ('955555555', 'Xiaomi 14', 0, 'TR11439');          -- No afiliado
```
