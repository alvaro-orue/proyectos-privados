# 🧪 Ejemplos de Testing - Interbank Simulator

## 📋 Colección de Requests para Testing

### 1. OAuth - Obtener Token

**Endpoint:** `POST http://localhost:5000/pago-push/security/v1/oauth`

**cURL:**
```bash
curl -X POST http://localhost:5000/pago-push/security/v1/oauth \
  -H "Content-Type: application/json"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/pago-push/security/v1/oauth" `
  -Method POST `
  -ContentType "application/json"
```

**Respuesta Esperada:**
```json
{
  "accessToken": "MOCK-TOKEN-abc123...",
  "tokenType": "Bearer",
  "expiresIn": 3600
}
```

---

### 2. Enviar Solicitud de Pago

**Endpoint:** `POST http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification`

**cURL:**
```bash
curl -X POST http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumber": "987654321",
    "amount": 150.50,
    "merchantId": "MERCHANT123",
    "transactionId": "TXN-20260109-001",
    "currency": "PEN",
    "description": "Compra en tienda online"
  }'
```

**PowerShell:**
```powershell
$body = @{
    phoneNumber = "987654321"
    amount = 150.50
    merchantId = "MERCHANT123"
    transactionId = "TXN-20260109-001"
    currency = "PEN"
    description = "Compra en tienda online"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

**Respuesta Esperada:**
```json
{
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456",
  "status": "PENDING",
  "message": "Solicitud de pago enviada correctamente",
  "transactionId": "TXN-20260109-001"
}
```

**IMPORTANTE:** Guarda el `uniqueId` y `codeAuth` para los siguientes pasos.

---

### 3. Confirmar Transacción

**Endpoint:** `POST http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment`

**cURL:**
```bash
curl -X POST http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment \
  -H "Content-Type: application/json" \
  -d '{
    "transactionId": "TXN-20260109-001",
    "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "codeAuth": "123456"
  }'
```

**PowerShell:**
```powershell
$body = @{
    transactionId = "TXN-20260109-001"
    uniqueId = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    codeAuth = "123456"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

**Respuesta Esperada:**
```json
{
  "status": "APPROVED",
  "message": "Transacción aprobada exitosamente",
  "transactionId": "TXN-20260109-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

### 4. Cancelar Transacción

**Endpoint:** `POST http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization`

**cURL:**
```bash
curl -X POST http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization \
  -H "Content-Type: application/json" \
  -d '{
    "transactionId": "TXN-20260109-002",
    "uniqueId": "abc-123-def-456",
    "codeAuth": "654321"
  }'
```

**PowerShell:**
```powershell
$body = @{
    transactionId = "TXN-20260109-002"
    uniqueId = "abc-123-def-456"
    codeAuth = "654321"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

**Respuesta Esperada:**
```json
{
  "status": "CANCELLED",
  "message": "Transacción cancelada exitosamente",
  "transactionId": "TXN-20260109-002",
  "uniqueId": "abc-123-def-456"
}
```

---

## 🔧 Endpoints de Backoffice

### 5. Forzar Aprobación de Pago

**Endpoint:** `POST http://localhost:5000/api/simulator/force-pay`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/simulator/force-pay \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "TXN-20260109-001"
  }'
```

**PowerShell:**
```powershell
$body = @{
    identifier = "TXN-20260109-001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/simulator/force-pay" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

**Nota:** El `identifier` puede ser el `transactionId` o el `uniqueId`.

**Respuesta Esperada:**
```json
{
  "success": true,
  "message": "Transacción TXN-20260109-001 aprobada forzadamente",
  "status": "APPROVED"
}
```

---

### 6. Listar Todas las Transacciones

**Endpoint:** `GET http://localhost:5000/api/simulator/transactions`

**cURL:**
```bash
curl http://localhost:5000/api/simulator/transactions
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/simulator/transactions" -Method GET
```

**Respuesta Esperada:**
```json
{
  "total": 3,
  "transactions": [
    {
      "TransactionId": "TXN-20260109-001",
      "PhoneNumber": "987654321",
      "Amount": 150.50,
      "Status": "APPROVED",
      "CodeAuth": "123456",
      "UniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "CreatedAt": "2026-01-09T15:30:00.123Z"
    },
    ...
  ]
}
```

---

### 7. Obtener Transacción Específica

**Endpoint:** `GET http://localhost:5000/api/simulator/transactions/{identifier}`

**cURL:**
```bash
curl http://localhost:5000/api/simulator/transactions/TXN-20260109-001
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/simulator/transactions/TXN-20260109-001" -Method GET
```

**Respuesta Esperada:**
```json
{
  "TransactionId": "TXN-20260109-001",
  "PhoneNumber": "987654321",
  "Amount": 150.50,
  "Status": "APPROVED",
  "CodeAuth": "123456",
  "UniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "CreatedAt": "2026-01-09T15:30:00.123Z"
}
```

---

### 8. Limpiar Todas las Transacciones

**Endpoint:** `DELETE http://localhost:5000/api/simulator/transactions/clear`

**cURL:**
```bash
curl -X DELETE http://localhost:5000/api/simulator/transactions/clear
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/simulator/transactions/clear" -Method DELETE
```

**Respuesta Esperada:**
```json
{
  "success": true,
  "message": "Todas las transacciones han sido eliminadas"
}
```

---

## 🔄 Flujo Completo de Prueba (Script PowerShell)

```powershell
# ============================================
# Script de prueba completo del simulador
# ============================================

$baseUrl = "http://localhost:5000"

Write-Host "🧪 Iniciando prueba completa del simulador..." -ForegroundColor Cyan

# 1. OAuth
Write-Host "`n1️⃣ Obteniendo token OAuth..." -ForegroundColor Yellow
$oauth = Invoke-RestMethod -Uri "$baseUrl/pago-push/security/v1/oauth" -Method POST
Write-Host "   Token: $($oauth.accessToken)" -ForegroundColor Green

# 2. Enviar solicitud de pago
Write-Host "`n2️⃣ Enviando solicitud de pago..." -ForegroundColor Yellow
$paymentRequest = @{
    phoneNumber = "987654321"
    amount = 150.50
    merchantId = "MERCHANT123"
    transactionId = "TXN-TEST-$(Get-Date -Format 'yyyyMMddHHmmss')"
    currency = "PEN"
    description = "Prueba automática"
} | ConvertTo-Json

$payment = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" `
    -Method POST -Body $paymentRequest -ContentType "application/json"

Write-Host "   UniqueId: $($payment.uniqueId)" -ForegroundColor Green
Write-Host "   CodeAuth: $($payment.codeAuth)" -ForegroundColor Green
Write-Host "   Status: $($payment.status)" -ForegroundColor Green

# 3. Listar transacciones
Write-Host "`n3️⃣ Listando transacciones..." -ForegroundColor Yellow
$transactions = Invoke-RestMethod -Uri "$baseUrl/api/simulator/transactions" -Method GET
Write-Host "   Total de transacciones: $($transactions.total)" -ForegroundColor Green

# 4. Forzar aprobación
Write-Host "`n4️⃣ Forzando aprobación del pago..." -ForegroundColor Yellow
$forceBody = @{
    identifier = $payment.transactionId
} | ConvertTo-Json

$forced = Invoke-RestMethod -Uri "$baseUrl/api/simulator/force-pay" `
    -Method POST -Body $forceBody -ContentType "application/json"

Write-Host "   $($forced.message)" -ForegroundColor Green

# 5. Verificar estado
Write-Host "`n5️⃣ Verificando estado final..." -ForegroundColor Yellow
$final = Invoke-RestMethod -Uri "$baseUrl/api/simulator/transactions/$($payment.transactionId)" -Method GET
Write-Host "   Status: $($final.Status)" -ForegroundColor Green

Write-Host "`n✅ Prueba completa finalizada exitosamente!" -ForegroundColor Cyan
```

Guarda este script como `test-simulator.ps1` y ejecútalo para probar todo el flujo.

---

## 📊 Verificar en la Base de Datos

Si quieres verificar directamente en la base de datos SQLite:

### Opción 1: SQLite Browser

1. Descarga [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Abre el archivo `InterbankSimulator.Api/simulator.db`
3. Ve a la pestaña "Browse Data" → Tabla "SimulatedTransactions"

### Opción 2: Comando SQL (SQLite CLI)

```bash
sqlite3 InterbankSimulator.Api/simulator.db "SELECT * FROM SimulatedTransactions;"
```

---

## 🎯 Casos de Prueba Sugeridos

| Caso | Descripción | Endpoint | Resultado Esperado |
|------|-------------|----------|-------------------|
| TC-01 | Crear pago válido | sendPaymentAuthorizationRequestNotification | Status: PENDING |
| TC-02 | Confirmar pago existente | confirmTransactionPayment | Status: APPROVED |
| TC-03 | Cancelar pago existente | cancelationPaymentAuthorization | Status: CANCELLED |
| TC-04 | Forzar aprobación | force-pay | Status: APPROVED |
| TC-05 | Listar todas las transacciones | GET /transactions | Lista con todas las TX |
| TC-06 | Buscar TX inexistente | GET /transactions/FAKE-ID | 404 Not Found |
| TC-07 | Confirmar TX inexistente | confirmTransactionPayment | 404 Not Found |
| TC-08 | Limpiar todas las TX | DELETE /transactions/clear | Base de datos vacía |

---

## 💡 Tips para Testing

1. **Usa Swagger UI**: La forma más fácil de probar es usar [http://localhost:5000](http://localhost:5000)
2. **Guarda los IDs**: Siempre guarda el `uniqueId` y `codeAuth` después de crear un pago
3. **Monitorea los logs**: La consola del simulador muestra logs detallados de cada operación
4. **Verifica en la DB**: Usa SQLite Browser para ver directamente los datos
5. **Limpia entre pruebas**: Usa el endpoint `DELETE /transactions/clear` para empezar limpio

---

## 🐛 Debugging

Si algo no funciona:

1. **Verifica el servidor**: ¿Está corriendo? Deberías ver el mensaje "✅ Simulador listo..."
2. **Revisa los logs**: La consola muestra todos los requests y errores
3. **Valida el JSON**: Asegúrate de que el body está bien formado
4. **Prueba con Swagger**: Si curl/PowerShell fallan, prueba con Swagger UI primero
5. **Revisa la base de datos**: Verifica que los datos se estén guardando correctamente
