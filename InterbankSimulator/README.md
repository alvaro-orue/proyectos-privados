# 🏦 Interbank Simulator - Mock Server para Pago Push

Mock Server completo para simular los servicios de Interbank (Pago Push) utilizando .NET 10, SQLite y Dapper.

## 🎯 Stack Tecnológico

- **Framework**: .NET 10 (net10.0)
- **ORM**: Dapper (Micro-ORM)
- **Base de Datos**: SQLite (ligera y portable)
- **Documentación**: Swagger/OpenAPI

## 🚀 Inicio Rápido

### 1. Ejecutar el Simulador

```bash
cd InterbankSimulator.Api
dotnet run
```

El servidor estará disponible en: **http://localhost:5000**

### 2. Acceder a Swagger UI

Abre tu navegador en: **http://localhost:5000**

## 📡 Endpoints Disponibles

### A. Seguridad (OAuth)

**POST** `/pago-push/security/v1/oauth`

Retorna un token de acceso simulado.

**Respuesta:**
```json
{
  "accessToken": "MOCK-TOKEN-123abc...",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```

---

### B. Pagos

#### 1. Enviar Solicitud de Pago

**POST** `/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification`

**Request:**
```json
{
  "phoneNumber": "987654321",
  "amount": 150.00,
  "merchantId": "MERCHANT123",
  "transactionId": "TXN-20260109-001",
  "currency": "PEN",
  "description": "Compra en tienda online"
}
```

**Response:**
```json
{
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456",
  "status": "PENDING",
  "message": "Solicitud de pago enviada correctamente",
  "transactionId": "TXN-20260109-001"
}
```

---

#### 2. Confirmar Transacción

**POST** `/pago-push/payment/v1/confirmTransactionPayment`

**Request:**
```json
{
  "transactionId": "TXN-20260109-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456"
}
```

**Response:**
```json
{
  "status": "APPROVED",
  "message": "Transacción aprobada exitosamente",
  "transactionId": "TXN-20260109-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

#### 3. Cancelar Transacción

**POST** `/pago-push/payment/v1/cancelationPaymentAuthorization`

**Request:**
```json
{
  "transactionId": "TXN-20260109-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456"
}
```

**Response:**
```json
{
  "status": "CANCELLED",
  "message": "Transacción cancelada exitosamente",
  "transactionId": "TXN-20260109-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

### C. Backoffice (Endpoints de Administración)

#### 1. Forzar Aprobación de Pago

**POST** `/api/simulator/force-pay`

**Request:**
```json
{
  "identifier": "TXN-20260109-001"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Transacción TXN-20260109-001 aprobada forzadamente",
  "status": "APPROVED"
}
```

---

#### 2. Listar Todas las Transacciones

**GET** `/api/simulator/transactions`

**Response:**
```json
{
  "total": 5,
  "transactions": [...]
}
```

---

#### 3. Obtener Transacción Específica

**GET** `/api/simulator/transactions/{identifier}`

---

#### 4. Limpiar Todas las Transacciones

**DELETE** `/api/simulator/transactions/clear`

---

## 🗄️ Base de Datos

El simulador crea automáticamente un archivo `simulator.db` (SQLite) en el directorio raíz del proyecto.

### Estructura de la Tabla

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

**Estados posibles:**
- `PENDING`: Pago pendiente de aprobación
- `APPROVED`: Pago aprobado
- `CANCELLED`: Pago cancelado

---

## 🔗 Conexión con el Cliente Real

### Configurar el Cliente (Repo 0095)

Edita el archivo de configuración del cliente ubicado en:

```
C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json
```

Busca la sección `PagoPushEndPoints` y reemplaza las URLs de producción por las URLs del simulador:

**ANTES (Producción):**
```json
{
  "PagoPushEndPoints": {
    "BaseUrl": "https://api.interbank.pe",
    "OAuthUrl": "https://api.interbank.pe/pago-push/security/v1/oauth",
    "SendPaymentUrl": "https://api.interbank.pe/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification",
    "ConfirmPaymentUrl": "https://api.interbank.pe/pago-push/payment/v1/confirmTransactionPayment",
    "CancelPaymentUrl": "https://api.interbank.pe/pago-push/payment/v1/cancelationPaymentAuthorization"
  }
}
```

**DESPUÉS (Simulador Local):**
```json
{
  "PagoPushEndPoints": {
    "BaseUrl": "http://localhost:5000",
    "OAuthUrl": "http://localhost:5000/pago-push/security/v1/oauth",
    "SendPaymentUrl": "http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification",
    "ConfirmPaymentUrl": "http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment",
    "CancelPaymentUrl": "http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization"
  }
}
```

---

## 🧪 Flujo de Prueba Completo

1. **Iniciar el simulador:**
   ```bash
   dotnet run
   ```

2. **Enviar solicitud de pago** (desde tu cliente o Postman):
   ```bash
   POST http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification
   ```

3. **Verificar en SQLite** que la transacción está en estado `PENDING`.

4. **Opción A - Confirmar manualmente:**
   ```bash
   POST http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment
   ```

5. **Opción B - Forzar aprobación (Backoffice):**
   ```bash
   POST http://localhost:5000/api/simulator/force-pay
   {
     "identifier": "TXN-20260109-001"
   }
   ```

---

## 📂 Estructura del Proyecto

```
InterbankSimulator/
├── InterbankSimulator.Api/
│   ├── Controllers/
│   │   ├── SecurityController.cs         # OAuth
│   │   ├── PaymentController.cs          # Pagos (Send, Confirm, Cancel)
│   │   └── SimulatorBackofficeController.cs  # Backoffice (Force-Pay)
│   ├── Infrastructure/
│   │   └── DatabaseBootstrap.cs          # Inicialización SQLite
│   ├── Models/
│   │   ├── SimulatedTransaction.cs
│   │   ├── Requests/
│   │   │   ├── PaymentAuthorizationRequest.cs
│   │   │   └── TransactionActionRequest.cs
│   │   └── Responses/
│   │       ├── OAuthResponse.cs
│   │       ├── PaymentAuthorizationResponse.cs
│   │       └── TransactionActionResponse.cs
│   ├── Program.cs
│   ├── appsettings.json
│   └── simulator.db                      # Base de datos SQLite (generada al inicio)
└── InterbankSimulator.sln
```

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología |
|------------|------------|
| Framework | .NET 10 |
| Lenguaje | C# 13 |
| ORM | Dapper 2.1.66 |
| Base de Datos | SQLite 10.0.1 |
| API Doc | Swagger/OpenAPI |

---

## 📝 Notas Importantes

- El archivo `simulator.db` se crea automáticamente al iniciar la aplicación.
- Todos los endpoints están documentados en Swagger UI.
- Los tokens OAuth son simulados y no tienen validación real.
- Los códigos de autorización son números aleatorios de 6 dígitos.
- Los `UniqueId` son GUIDs generados automáticamente.

---

## 🎓 Autor

Proyecto creado como **Mock Server** para desarrollo y testing de integraciones con Interbank Pago Push.

---

## 📄 Licencia

Este proyecto es un simulador de desarrollo. No usar en producción.
