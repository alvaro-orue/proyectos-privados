# 🔗 Instrucciones para Conectar el Cliente Real al Simulador

## Objetivo

Hacer que el sistema cliente (Repo 0095) deje de consumir los servicios de Interbank en producción y consuma el **Mock Server local** (InterbankSimulator).

---

## 📍 Ubicación del Archivo de Configuración del Cliente

```
C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json
```

---

## ✏️ Modificaciones Requeridas

Busca la sección `PagoPushEndPoints` en el archivo `appsettings.json` del cliente y reemplaza las URLs de producción por las URLs del simulador local.

### ANTES (Producción - Interbank Real)

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

### DESPUÉS (Simulador Local)

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

## 🔄 Script PowerShell Automatizado (Opcional)

Si prefieres automatizar el cambio, crea un archivo `switch-to-simulator.ps1`:

```powershell
# Script para cambiar las URLs del cliente al simulador local

$clientConfigPath = "C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json"

# Leer el archivo
$config = Get-Content $clientConfigPath -Raw | ConvertFrom-Json

# Modificar las URLs
$config.PagoPushEndPoints.BaseUrl = "http://localhost:5000"
$config.PagoPushEndPoints.OAuthUrl = "http://localhost:5000/pago-push/security/v1/oauth"
$config.PagoPushEndPoints.SendPaymentUrl = "http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification"
$config.PagoPushEndPoints.ConfirmPaymentUrl = "http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment"
$config.PagoPushEndPoints.CancelPaymentUrl = "http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization"

# Guardar cambios
$config | ConvertTo-Json -Depth 10 | Set-Content $clientConfigPath

Write-Host "✅ Configuración actualizada. El cliente ahora apunta al simulador local." -ForegroundColor Green
```

**Ejecutar:**
```powershell
.\switch-to-simulator.ps1
```

---

## 🔄 Script para Volver a Producción (Opcional)

Crea un archivo `switch-to-production.ps1`:

```powershell
# Script para restaurar las URLs de producción

$clientConfigPath = "C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json"

# Leer el archivo
$config = Get-Content $clientConfigPath -Raw | ConvertFrom-Json

# Modificar las URLs a producción
$config.PagoPushEndPoints.BaseUrl = "https://api.interbank.pe"
$config.PagoPushEndPoints.OAuthUrl = "https://api.interbank.pe/pago-push/security/v1/oauth"
$config.PagoPushEndPoints.SendPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification"
$config.PagoPushEndPoints.ConfirmPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/confirmTransactionPayment"
$config.PagoPushEndPoints.CancelPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/cancelationPaymentAuthorization"

# Guardar cambios
$config | ConvertTo-Json -Depth 10 | Set-Content $clientConfigPath

Write-Host "✅ Configuración restaurada. El cliente ahora apunta a Interbank REAL." -ForegroundColor Yellow
```

---

## 🧪 Verificación

### 1. Iniciar el Simulador

```bash
cd InterbankSimulator.Api
dotnet run
```

Deberías ver:
```
🚀 Iniciando Interbank Simulator...
📁 Base de datos no encontrada. Creando simulator.db...
✅ Base de datos SQLite inicializada correctamente.
✅ Simulador listo. Accede a Swagger en: http://localhost:5000
```

### 2. Ejecutar el Cliente

Inicia tu aplicación cliente (Repo 0095) normalmente. Ahora todas las llamadas a Interbank irán al simulador local.

### 3. Monitorear las Llamadas

Verás logs en la consola del simulador cada vez que el cliente haga una petición:

```
💳 Solicitud de pago recibida: 987654321 - S/ 150.00
✅ Transacción guardada: UniqueId=f47ac10b..., CodeAuth=123456
```

---

## 📊 Endpoints de Backoffice para Testing

Una vez conectado, puedes usar los endpoints de backoffice para manipular transacciones:

### Ver todas las transacciones

```bash
GET http://localhost:5000/api/simulator/transactions
```

### Forzar aprobación de un pago

```bash
POST http://localhost:5000/api/simulator/force-pay
{
  "identifier": "TXN-20260109-001"
}
```

### Limpiar todas las transacciones

```bash
DELETE http://localhost:5000/api/simulator/transactions/clear
```

---

## ⚠️ Advertencias

1. **NO usar en producción**: Este simulador es solo para desarrollo.
2. **Backup**: Antes de modificar el `appsettings.json` del cliente, haz una copia de seguridad.
3. **HTTPS**: El simulador usa HTTP por simplicidad. Si tu cliente requiere HTTPS, necesitarás configurar certificados.

---

## 🎯 Beneficios de Usar el Simulador

- ✅ **Testing sin límites**: No dependes de Interbank real.
- ✅ **Control total**: Fuerza aprobaciones/cancelaciones a voluntad.
- ✅ **Debugging fácil**: Logs en consola y base de datos SQLite visible.
- ✅ **Sin costos**: No consume créditos/transacciones reales.
- ✅ **Portabilidad**: Todo local, sin conectividad externa.

---

## 📞 Soporte

Si tienes problemas, revisa:

1. El simulador está corriendo (`dotnet run` en InterbankSimulator.Api).
2. El puerto 5000 está disponible.
3. Las URLs en `appsettings.json` del cliente están correctamente configuradas.
4. Los logs del simulador y del cliente para identificar errores.
