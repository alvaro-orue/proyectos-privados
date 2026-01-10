# 📁 Estructura del Proyecto - Interbank Simulator

## 🗂️ Vista General

```
InterbankSimulator/
│
├── 📄 InterbankSimulator.sln                      # Solución principal
├── 📄 README.md                                   # Documentación completa
├── 📄 QUICK_START.md                              # Guía de inicio rápido
├── 📄 INSTRUCCIONES_CONEXION_CLIENTE.md           # Cómo conectar el cliente real
├── 📄 TESTING_EXAMPLES.md                         # Ejemplos de pruebas
├── 📄 ESTRUCTURA_PROYECTO.md                      # Este archivo
├── 📄 .gitignore                                  # Archivos ignorados por Git
│
├── 📜 switch-to-simulator.ps1                     # Script: Cambiar a simulador
├── 📜 switch-to-production.ps1                    # Script: Cambiar a producción
│
└── 📂 InterbankSimulator.Api/                     # Proyecto Web API
    │
    ├── 📄 InterbankSimulator.Api.csproj           # Archivo de proyecto
    ├── 📄 Program.cs                              # Punto de entrada principal
    ├── 📄 appsettings.json                        # Configuración (puerto 5000)
    ├── 🗄️ simulator.db                            # Base de datos SQLite (generada al ejecutar)
    │
    ├── 📂 Properties/
    │   └── launchSettings.json                    # Configuración de ejecución
    │
    ├── 📂 Controllers/                            # Controladores de la API
    │   ├── SecurityController.cs                  # OAuth (token simulado)
    │   ├── PaymentController.cs                   # Pagos (Send, Confirm, Cancel)
    │   └── SimulatorBackofficeController.cs       # Backoffice (Force-Pay, List, etc.)
    │
    ├── 📂 Infrastructure/
    │   └── DatabaseBootstrap.cs                   # Inicialización de SQLite
    │
    └── 📂 Models/
        ├── SimulatedTransaction.cs                # Modelo principal
        │
        ├── 📂 Requests/
        │   ├── PaymentAuthorizationRequest.cs     # Request de autorización
        │   └── TransactionActionRequest.cs        # Request de confirmación/cancelación
        │
        └── 📂 Responses/
            ├── OAuthResponse.cs                   # Response de OAuth
            ├── PaymentAuthorizationResponse.cs    # Response de autorización
            └── TransactionActionResponse.cs       # Response de acción (confirm/cancel)
```

---

## 🔍 Descripción de Componentes

### 📂 Controllers (Controladores)

| Archivo | Ruta | Descripción |
|---------|------|-------------|
| `SecurityController.cs` | `/pago-push/security/v1` | Simula la autenticación OAuth de Interbank |
| `PaymentController.cs` | `/pago-push/payment/v1` | Maneja solicitudes de pago, confirmación y cancelación |
| `SimulatorBackofficeController.cs` | `/api/simulator` | Endpoints de administración (force-pay, listar, etc.) |

#### Endpoints Principales

**SecurityController:**
- `POST /pago-push/security/v1/oauth` → Retorna token simulado

**PaymentController:**
- `POST /pago-push/payment/v1/sendPaymentAuthorizationRequestNotification` → Crea pago PENDING
- `POST /pago-push/payment/v1/confirmTransactionPayment` → Cambia a APPROVED
- `POST /pago-push/payment/v1/cancelationPaymentAuthorization` → Cambia a CANCELLED

**SimulatorBackofficeController:**
- `POST /api/simulator/force-pay` → Fuerza aprobación
- `GET /api/simulator/transactions` → Lista todas las TX
- `GET /api/simulator/transactions/{id}` → Obtiene TX específica
- `DELETE /api/simulator/transactions/clear` → Limpia todas las TX

---

### 📂 Infrastructure

| Archivo | Propósito |
|---------|-----------|
| `DatabaseBootstrap.cs` | Crea y inicializa la base de datos SQLite al arrancar |

**Funciones:**
- `Initialize()`: Crea el archivo `simulator.db` y la tabla `SimulatedTransactions`
- `CreateConnection()`: Retorna una conexión SQLite lista para usar con Dapper

---

### 📂 Models

#### Modelo Principal

| Archivo | Descripción |
|---------|-------------|
| `SimulatedTransaction.cs` | Representa una transacción en la base de datos |

**Propiedades:**
```csharp
- TransactionId (TEXT, PRIMARY KEY)
- PhoneNumber (TEXT)
- Amount (REAL)
- Status (TEXT) → "PENDING", "APPROVED", "CANCELLED"
- CodeAuth (TEXT) → Código de 6 dígitos
- UniqueId (TEXT, UNIQUE) → GUID
- CreatedAt (TEXT) → Timestamp ISO 8601
```

#### Requests

| Archivo | Uso |
|---------|-----|
| `PaymentAuthorizationRequest.cs` | Body del endpoint `sendPaymentAuthorizationRequestNotification` |
| `TransactionActionRequest.cs` | Body de `confirmTransactionPayment` y `cancelationPaymentAuthorization` |

#### Responses

| Archivo | Uso |
|---------|-----|
| `OAuthResponse.cs` | Response del endpoint `oauth` |
| `PaymentAuthorizationResponse.cs` | Response de `sendPaymentAuthorizationRequestNotification` |
| `TransactionActionResponse.cs` | Response de confirmación/cancelación |

---

## 🗄️ Base de Datos SQLite

### Tabla: SimulatedTransactions

```sql
CREATE TABLE SimulatedTransactions (
    TransactionId TEXT PRIMARY KEY,
    PhoneNumber TEXT NOT NULL,
    Amount REAL NOT NULL,
    Status TEXT NOT NULL DEFAULT 'PENDING',
    CodeAuth TEXT NOT NULL,
    UniqueId TEXT NOT NULL UNIQUE,
    CreatedAt TEXT NOT NULL
);
```

### Ubicación del Archivo

```
InterbankSimulator.Api/simulator.db
```

Se crea automáticamente al ejecutar `dotnet run` por primera vez.

---

## ⚙️ Archivos de Configuración

### appsettings.json

```json
{
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
        "Url": "http://localhost:5000"  ← Puerto configurado aquí
      }
    }
  }
}
```

### launchSettings.json

Perfil de ejecución:
- Nombre: `InterbankSimulator`
- Puerto: `5000`
- Abre navegador automáticamente: `true`
- URL de inicio: Swagger UI (raíz)

---

## 📦 Paquetes NuGet Instalados

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `Dapper` | 2.1.66 | Micro-ORM para SQL |
| `Microsoft.Data.Sqlite` | 10.0.1 | Driver SQLite para .NET |
| `Swashbuckle.AspNetCore` | 10.1.0 | Generación de Swagger/OpenAPI |
| `Microsoft.AspNetCore.OpenApi` | 10.0.0 | Soporte OpenAPI nativo de .NET |

---

## 🔄 Flujo de Datos

### 1. Inicio de la Aplicación

```
Program.cs
  ↓
DatabaseBootstrap.Initialize()
  ↓
Crea simulator.db si no existe
  ↓
Crea tabla SimulatedTransactions
  ↓
Configura inyección de dependencias (IDbConnection)
  ↓
Inicia Kestrel en puerto 5000
  ↓
Swagger UI disponible en http://localhost:5000
```

### 2. Creación de Pago

```
Cliente → POST /sendPaymentAuthorizationRequestNotification
  ↓
PaymentController recibe PaymentAuthorizationRequest
  ↓
Genera UniqueId (GUID) y CodeAuth (aleatorio 6 dígitos)
  ↓
INSERT en SQLite con Status = 'PENDING'
  ↓
Retorna PaymentAuthorizationResponse con IDs generados
```

### 3. Confirmación de Pago

```
Cliente → POST /confirmTransactionPayment
  ↓
PaymentController recibe TransactionActionRequest
  ↓
UPDATE en SQLite: Status = 'APPROVED' WHERE UniqueId = @id
  ↓
Retorna TransactionActionResponse
```

### 4. Forzar Aprobación (Backoffice)

```
Usuario → POST /api/simulator/force-pay
  ↓
SimulatorBackofficeController recibe identifier
  ↓
UPDATE Status = 'APPROVED' WHERE TransactionId = @id OR UniqueId = @id
  ↓
Retorna confirmación
```

---

## 🧩 Inyección de Dependencias

```csharp
// Program.cs
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connection = new SqliteConnection("Data Source=simulator.db");
    connection.Open();
    return connection;
});
```

Cada controlador recibe `IDbConnection` en su constructor:

```csharp
public PaymentController(IDbConnection dbConnection, ILogger<PaymentController> logger)
{
    _dbConnection = dbConnection;
    _logger = logger;
}
```

Esto permite usar Dapper directamente:

```csharp
await _dbConnection.ExecuteAsync(sql, parameters);
var results = await _dbConnection.QueryAsync<T>(sql, parameters);
```

---

## 🎨 Características Destacadas

### ✅ Logging Integrado

Todos los controladores usan `ILogger<T>` para escribir logs en consola:

```csharp
_logger.LogInformation("💳 Solicitud de pago recibida: {PhoneNumber} - S/ {Amount}",
    request.PhoneNumber, request.Amount);
```

### ✅ Swagger Automático

Todos los endpoints se documentan automáticamente en Swagger sin anotaciones adicionales.

### ✅ Base de Datos Portátil

SQLite es un archivo único (`simulator.db`). Fácil de:
- Copiar
- Respaldar
- Inspeccionar
- Eliminar

### ✅ Scripts PowerShell

Automatización para cambiar entre simulador y producción sin editar manualmente archivos.

---

## 🔧 Modificaciones Comunes

### Cambiar el Puerto

Edita `appsettings.json`:

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5001"  ← Cambia aquí
      }
    }
  }
}
```

### Agregar HTTPS

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      },
      "Https": {
        "Url": "https://localhost:5001"
      }
    }
  }
}
```

Necesitarás un certificado de desarrollo:

```bash
dotnet dev-certs https --trust
```

### Personalizar la Base de Datos

Edita `DatabaseBootstrap.cs` para agregar más tablas o columnas.

### Agregar Más Endpoints

1. Crea un nuevo controlador en `Controllers/`
2. Usa `[Route(...)]` y `[HttpPost/Get/etc]`
3. Inyecta `IDbConnection` si necesitas acceso a la BD
4. Reinicia el servidor

Swagger se actualizará automáticamente.

---

## 📚 Referencias

- [Documentación de Dapper](https://github.com/DapperLib/Dapper)
- [Microsoft.Data.Sqlite](https://learn.microsoft.com/en-us/dotnet/standard/data/sqlite/)
- [Swashbuckle.AspNetCore](https://github.com/domaindrivendev/Swashbuckle.AspNetCore)
- [ASP.NET Core 10](https://learn.microsoft.com/en-us/aspnet/core/)

---

## 🎯 Próximos Pasos

1. ✅ Ejecutar el simulador: `dotnet run`
2. ✅ Probar en Swagger: [http://localhost:5000](http://localhost:5000)
3. ✅ Conectar el cliente: `.\switch-to-simulator.ps1`
4. ✅ Validar el flujo completo
5. ⏭️ (Opcional) Agregar endpoints adicionales según necesidades
