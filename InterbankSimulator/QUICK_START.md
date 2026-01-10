# ⚡ Inicio Rápido - Interbank Simulator

## 🚀 Paso 1: Ejecutar el Simulador

Abre una terminal en el directorio del proyecto y ejecuta:

```bash
cd InterbankSimulator.Api
dotnet run
```

Deberías ver:

```
🚀 Iniciando Interbank Simulator...
📁 Base de datos no encontrada. Creando simulator.db...
✅ Base de datos SQLite inicializada correctamente.
📍 Ubicación: C:\...\simulator.db
✅ Simulador listo. Accede a Swagger en: http://localhost:5000
📋 Endpoints disponibles:
   - POST /pago-push/security/v1/oauth
   - POST /pago-push/payment/v1/sendPaymentAuthorizationRequestNotification
   - POST /pago-push/payment/v1/confirmTransactionPayment
   - POST /pago-push/payment/v1/cancelationPaymentAuthorization
   - POST /api/simulator/force-pay (Backoffice)
   - GET  /api/simulator/transactions (Backoffice)
```

---

## 🌐 Paso 2: Abrir Swagger UI

Abre tu navegador en: [http://localhost:5000](http://localhost:5000)

Verás la interfaz de Swagger con todos los endpoints documentados.

---

## 🔗 Paso 3: Conectar el Cliente Real (Opcional)

Para que tu cliente consuma este simulador en vez de Interbank real:

### Opción A: Script Automático (Recomendado)

```powershell
.\switch-to-simulator.ps1
```

Este script:
- Crea un backup automático del `appsettings.json` del cliente
- Reemplaza las URLs de Interbank por `http://localhost:5000`
- Muestra confirmación de los cambios

### Opción B: Manual

Edita el archivo:
```
C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json
```

Busca la sección `PagoPushEndPoints` y cambia todas las URLs a `http://localhost:5000/...`

---

## 🧪 Paso 4: Probar el Flujo Completo

### 1. Enviar Solicitud de Pago

```bash
POST http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification
```

**Body (JSON):**
```json
{
  "phoneNumber": "987654321",
  "amount": 150.50,
  "merchantId": "MERCHANT123",
  "transactionId": "TXN-001",
  "currency": "PEN",
  "description": "Test payment"
}
```

**Response:**
```json
{
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456",
  "status": "PENDING",
  "message": "Solicitud de pago enviada correctamente",
  "transactionId": "TXN-001"
}
```

---

### 2. Opción A: Confirmar Pago (Flujo Normal)

```bash
POST http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment
```

**Body:**
```json
{
  "transactionId": "TXN-001",
  "uniqueId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "codeAuth": "123456"
}
```

---

### 2. Opción B: Forzar Aprobación (Backoffice)

```bash
POST http://localhost:5000/api/simulator/force-pay
```

**Body:**
```json
{
  "identifier": "TXN-001"
}
```

---

### 3. Ver Todas las Transacciones

```bash
GET http://localhost:5000/api/simulator/transactions
```

---

## 🗂️ Base de Datos

El archivo `simulator.db` se crea automáticamente en:
```
InterbankSimulator.Api/simulator.db
```

Puedes abrirlo con cualquier visor de SQLite (DB Browser, DBeaver, etc.).

---

## 🔁 Volver a Producción

Cuando quieras que el cliente vuelva a apuntar a Interbank real:

```powershell
.\switch-to-production.ps1
```

---

## 📝 Comandos Útiles

| Comando | Descripción |
|---------|-------------|
| `dotnet run` | Ejecutar el simulador |
| `dotnet build` | Compilar el proyecto |
| `dotnet clean` | Limpiar archivos compilados |
| `.\switch-to-simulator.ps1` | Apuntar cliente al simulador |
| `.\switch-to-production.ps1` | Apuntar cliente a producción |

---

## 🛠️ Solución de Problemas

### El puerto 5000 está ocupado

Edita [appsettings.json](InterbankSimulator.Api/appsettings.json) y cambia el puerto:

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5001"
      }
    }
  }
}
```

También actualiza el script `switch-to-simulator.ps1` con el nuevo puerto.

### Error al conectar desde el cliente

Verifica:
1. El simulador está corriendo (`dotnet run`)
2. El puerto 5000 está accesible
3. Las URLs en el cliente están correctamente configuradas
4. No hay firewall bloqueando la conexión

---

## 📚 Más Información

- [README.md](README.md) - Documentación completa
- [INSTRUCCIONES_CONEXION_CLIENTE.md](INSTRUCCIONES_CONEXION_CLIENTE.md) - Guía detallada de conexión
- Swagger UI: [http://localhost:5000](http://localhost:5000)
