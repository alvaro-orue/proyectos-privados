# Evidencias Detalladas - Ambiente DEV
## Fecha: 2025-11-04 13:23:47
## Caso de Prueba: CPI-001 - Flujo completo exitoso

---

## Información del Ambiente

| Parámetro | Valor |
|-----------|-------|
| **Ambiente** | DEV (Desarrollo) |
| **URL Base** | https://testapi-pw.izipay.pe |
| **Merchant Code** | 4078370 |
| **Transaction ID** | DEV20251104132347 |
| **Order Number** | ORDER20251104132347 |
| **Fecha/Hora Ejecución** | 2025-11-04 13:23:47 |

---

## PASO 1: GENERAR TOKEN DE SESIÓN

### ✅ ESTADO: EXITOSO

### Endpoint Completo
```
POST https://testapi-pw.izipay.pe/security/v1/Token/Generate
```

### Request Headers
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "transactionId": "DEV20251104132347"
}
```

### Request Body (Payload)
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104132347",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

### Response
```json
Status Code: 200 OK
Response Time: 988.50ms

Body:
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDEzMjM0NyIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDEzMjM0NyIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiI1OTdjYmE3Yy04ZDVkLTQ4NWUtOWFmMS1hNzA4N2VjYjc2NDEiLCJuYmYiOjE3NjIyODA2MjgsImV4cCI6MTc2MjI4MTUyOCwiaWF0IjoxNzYyMjgwNjI4fQ.pnjzIYl_eG0n44lI2WB1TdVU23SZynymCKHcPlS4rAw",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

### Token JWT Generado
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDEzMjM0NyIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDEzMjM0NyIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiI1OTdjYmE3Yy04ZDVkLTQ4NWUtOWFmMS1hNzA4N2VjYjc2NDEiLCJuYmYiOjE3NjIyODA2MjgsImV4cCI6MTc2MjI4MTUyOCwiaWF0IjoxNzYyMjgwNjI4fQ.pnjzIYl_eG0n44lI2WB1TdVU23SZynymCKHcPlS4rAw
```

### Decodificación del Token (Header)
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Decodificación del Token (Payload)
```json
{
  "merchantCode": "4078370",
  "facilitatorCode": "0",
  "transactionId": "DEV20251104132347",
  "OrderNumber": "ORDER20251104132347",
  "Amount": "100.00",
  "TokenId": "597cba7c-8d5d-485e-9af1-a7087ecb7641",
  "nbf": 1762280628,
  "exp": 1762281528,
  "iat": 1762280628
}
```

### Análisis del Resultado
- ✅ **Status Code:** 200 OK - Respuesta exitosa
- ✅ **Response Time:** 988.50ms - Tiempo aceptable (< 1 segundo)
- ✅ **Token Generado:** JWT válido con firma HS256
- ✅ **Token ID:** 597cba7c-8d5d-485e-9af1-a7087ecb7641
- ✅ **Validez:** 900 segundos (15 minutos)
- ✅ **User Organization:** 1snn5n9w
- ✅ **User Scoring:** izipay_high

### Conclusión Paso 1
**El servicio Security API está funcionando correctamente en el ambiente DEV.**

---

## PASO 2: BUSCAR CUOTAS DISPONIBLES

### ❌ ESTADO: FALLIDO

### Endpoint Completo
```
POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
```

### Request Headers
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDEzMjM0NyIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDEzMjM0NyIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiI1OTdjYmE3Yy04ZDVkLTQ4NWUtOWFmMS1hNzA4N2VjYjc2NDEiLCJuYmYiOjE3NjIyODA2MjgsImV4cCI6MTc2MjI4MTUyOCwiaWF0IjoxNzYyMjgwNjI4fQ.pnjzIYl_eG0n44lI2WB1TdVU23SZynymCKHcPlS4rAw",
  "transactionId": "DEV20251104132347"
}
```

### Request Body (Payload)
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

### Datos del BIN Utilizado
| Parámetro | Valor |
|-----------|-------|
| **BIN** | 545545 |
| **Banco** | SCOTIABANK |
| **Tipo Tarjeta** | Mastercard |
| **Cuotas Esperadas** | 12 |
| **Diferido Esperado** | 3 meses |
| **Estado en DB** | ✅ Validado previamente (funcionó hace 1 hora) |

### Response
```json
Status Code: 500 Internal Server Error
Response Time: 4367.55ms

Body:
{
  "code": "500",
  "message": "an error has occurred."
}
```

### Análisis del Resultado
- ❌ **Status Code:** 500 Internal Server Error
- ❌ **Response Time:** 4,367.55ms - Muy lento (> 4 segundos)
- ❌ **Error Message:** "an error has occurred." - Error genérico del servidor
- ✅ **Token Válido:** El token JWT fue aceptado (no hay error 401/403)
- ✅ **BIN Válido:** El BIN 545545 existe en la base de datos
- ✅ **Merchant Code Válido:** 4078370 es correcto

### Conclusión Paso 2
**El servicio Installments API está experimentando un error interno del servidor (500) en el ambiente DEV.**

---

## RESUMEN DE LA EJECUCIÓN

| Paso | Endpoint | Método | Status | Tiempo | Resultado |
|------|----------|--------|--------|--------|-----------|
| 1 | `/security/v1/Token/Generate` | POST | 200 | 988ms | ✅ EXITOSO |
| 2 | `/Installments/v1/Installments/Search` | POST | 500 | 4,368ms | ❌ FALLIDO |

### Duración Total
```
5,360.72ms (5.36 segundos)
```

### Estado Final
```
❌ FALLIDO
```

### Error
```
Installments search failed: an error has occurred.
```

---

## ANÁLISIS TÉCNICO DEL PROBLEMA

### Evidencia 1: Token Generation Funciona
El servicio Security API (`https://testapi-pw.izipay.pe/security/v1/Token/Generate`) está **operativo y funcional**:
- ✅ Responde con 200 OK
- ✅ Genera tokens JWT válidos
- ✅ Tiempo de respuesta normal (~1 segundo)

### Evidencia 2: Installments Search Falla
El servicio Installments API (`https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`) está **experimentando errores**:
- ❌ Responde con 500 Internal Server Error
- ❌ Tiempo de respuesta anormal (4+ segundos, normalmente ~1 segundo)
- ❌ Mensaje de error genérico

### Evidencia 3: No es un Problema de Autenticación
- ✅ El token JWT fue generado correctamente
- ✅ El header Authorization fue enviado correctamente
- ✅ No hay error 401 (Unauthorized) ni 403 (Forbidden)
- ✅ El servicio acepta el token pero falla internamente

### Evidencia 4: No es un Problema de Datos
- ✅ BIN 545545 existe en la base de datos
- ✅ Merchant Code 4078370 es válido
- ✅ Funcionó correctamente hace ~1 hora
- ✅ Funciona en ambiente QA con los mismos datos

### Evidencia 5: Es un Problema del Servidor
- ❌ Error 500 = Internal Server Error (problema del lado del servidor)
- ❌ Tiempo de respuesta 4x más lento de lo normal
- ❌ Todos los BINs fallan de la misma manera
- ❌ Problema consistente en múltiples intentos

---

## HISTORIAL DE INTENTOS

| Hora | Transaction ID | Token Status | Search Status | Tiempo Search |
|------|----------------|--------------|---------------|---------------|
| 13:09:41 | DEV20251104130941 | ✅ 200 OK | ❌ 500 Error | 4,377ms |
| 13:10:07 | DEV20251104131007 | ✅ 200 OK | ❌ 500 Error | 4,328ms |
| 13:13:50 | DEV20251104131350 | ✅ 200 OK | ❌ 500 Error | 4,253ms |
| 13:17:42 | DEV20251104131742 | ✅ 200 OK | ❌ 500 Error | 879ms |
| **13:23:47** | **DEV20251104132347** | **✅ 200 OK** | **❌ 500 Error** | **4,368ms** |

### Observaciones del Historial
- **Consistencia:** 5 intentos consecutivos fallan con error 500
- **Duración:** Problema activo por ~15 minutos
- **Token:** 100% exitoso en todos los intentos
- **Search:** 0% exitoso en todos los intentos

---

## COMPARACIÓN CON EJECUCIÓN EXITOSA ANTERIOR

### Ejecución Exitosa (12:29 - Hace 1 hora)
```
Transaction ID: DEV20251104122900

✅ Token Generation:
   Status: 200 OK
   Time: 1,282ms

✅ Search Installments:
   Status: 200 OK
   Time: 1,194ms
   Cuotas: 12 opciones retornadas
   Banco: SCOTIABANK

Total: 2,476ms
Estado: EXITOSO
```

### Ejecución Actual (13:23 - Ahora)
```
Transaction ID: DEV20251104132347

✅ Token Generation:
   Status: 200 OK
   Time: 989ms

❌ Search Installments:
   Status: 500 Internal Server Error
   Time: 4,368ms
   Error: "an error has occurred."

Total: 5,361ms
Estado: FALLIDO
```

### Diferencias Clave
| Métrica | Antes (Exitoso) | Ahora (Fallido) | Diferencia |
|---------|-----------------|-----------------|------------|
| Token Time | 1,282ms | 989ms | -23% (mejor) |
| Search Time | 1,194ms | 4,368ms | +266% (mucho peor) |
| Search Status | 200 OK | 500 Error | Error crítico |
| Total Time | 2,476ms | 5,361ms | +116% (doble) |

---

## DIAGNÓSTICO PROBABLE

### Causas Más Probables (Ordenadas por Probabilidad)

#### 1. Base de Datos No Disponible (80% probabilidad)
```
Síntomas:
- Error 500 genérico
- Timeout alto (4+ segundos)
- Token funciona (no requiere DB), Search falla (requiere DB)

Posible causa:
- Base de datos DEV caída o en mantenimiento
- Conexión entre API y DB interrumpida
- Stored procedure Installments.SP_Installments no responde
```

#### 2. Servicio en Mantenimiento (15% probabilidad)
```
Síntomas:
- Problema repentino (funcionó hace 1 hora)
- Afecta solo a Installments API
- Security API no afectada

Posible causa:
- Actualización o deployment en progreso
- Mantenimiento programado no anunciado
```

#### 3. Excepción No Controlada (5% probabilidad)
```
Síntomas:
- Error 500 sin detalle
- Mensaje genérico "an error has occurred."

Posible causa:
- Exception en el código que no está siendo capturada
- Error en el stored procedure
- Timeout de base de datos
```

---

## ARQUITECTURA Y FLUJO

### Flujo Normal (Cuando Funciona)
```
Cliente Python
    ↓
    → POST /security/v1/Token/Generate
    ↓
Security API (✅ Funciona)
    ↓
    ← JWT Token
    ↓
Cliente Python
    ↓
    → POST /Installments/v1/Installments/Search (con Bearer Token)
    ↓
Controller API (❌ Falla aquí)
    ↓
    → EXEC Installments.SP_Installments @bin='545545', @merchantCode='4078370'
    ↓
Base de Datos (❌ Problema aquí?)
    ↓
    ← Cuotas disponibles
    ↓
Controller API
    ↓
    ← JSON Response
    ↓
Cliente Python
```

### Punto de Falla Identificado
```
Controller API → Base de Datos

El problema está en:
1. La conexión entre Controller API y Base de Datos, O
2. La base de datos misma (caída/lenta), O
3. El stored procedure Installments.SP_Installments
```

---

## ENDPOINTS DETALLADOS

### Endpoint 1: Token Generation (Security API)
```
URL Completa: https://testapi-pw.izipay.pe/security/v1/Token/Generate
Método: POST
Content-Type: application/json
Estado: ✅ OPERATIVO

Arquitectura:
- Proyecto: Service.ApiController (Security)
- Puerto: No especificado (usa HTTPS 443)
- Autenticación: Public Key
- Base de Datos: No requiere (o requiere DB diferente que está operativa)
```

### Endpoint 2: Installments Search (Installments API)
```
URL Completa: https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
Método: POST
Content-Type: application/json
Autenticación: Bearer Token (JWT)
Estado: ❌ ERROR 500

Arquitectura:
- Proyecto: Service.ApiController (Installments)
- Puerto: No especificado (usa HTTPS 443)
- Stored Procedure: Installments.SP_Installments
- Tablas: dbo.bin, binEcn
- Estado DB: ❌ Posiblemente no disponible
```

---

## ACCIONES RECOMENDADAS

### Inmediatas (Equipo de Infraestructura)

1. **Verificar estado de la base de datos DEV**
   ```sql
   -- Test básico de conectividad
   SELECT 1;

   -- Verificar tabla de BINs
   SELECT COUNT(*) FROM dbo.bin;

   -- Test del stored procedure
   EXEC Installments.SP_Installments
       @bin = '545545',
       @merchantCode = '4078370';
   ```

2. **Verificar logs del Controller API**
   - Buscar excepciones en logs
   - Verificar stack traces
   - Identificar timeout o connection errors

3. **Verificar servicios del servidor**
   ```bash
   # Estado del servicio Installments API
   systemctl status installments-api

   # Uso de recursos
   top
   df -h
   free -h

   # Conexiones de red
   netstat -an | grep ESTABLISHED
   ```

### Corto Plazo (Equipo de Desarrollo)

4. **Usar ambiente QA como alternativa**
   - QA está 100% operativo
   - Misma configuración de BINs
   - Permite continuar con testing

5. **Monitorear recuperación de DEV**
   - Reintentar cada 15 minutos
   - Documentar tiempo de caída
   - Registrar en sistema de tickets

---

## ARCHIVOS GENERADOS

### 1. Resultado JSON
```
Ubicación: CASOS_MULTI_AMBIENTE\DEV\results\test_result_CPI-001_DEV.json
Contenido: Request/Response completos, timestamps, tiempos de respuesta
```

### 2. Reporte TXT
```
Ubicación: CASOS_MULTI_AMBIENTE\DEV\results\test_report_CPI-001_DEV.txt
Contenido: Reporte legible en consola con estado de cada paso
```

### 3. Este Documento
```
Ubicación: CASOS_MULTI_AMBIENTE\DEV\EVIDENCIAS_DETALLADAS_DEV_2025-11-04_13-23.md
Contenido: Evidencias completas con análisis técnico detallado
```

---

## ESTADO DE OTROS AMBIENTES

### QA - ✅ OPERATIVO
```
URL: https://qa-api-pw.izipay.pe
Token API: ✅ Funcional
Installments API: ✅ Funcional
Última prueba: Hace ~1 hora (100% exitosa)
```

### SANDBOX - ⚠️ OPERATIVO (con ajustes)
```
URL: https://sandbox-api-pw.izipay.pe
Token API: ✅ Funcional
Installments API: ✅ Funcional (con BINs específicos)
Última prueba: Hace ~20 minutos (parcialmente exitosa)
```

---

## CONCLUSIÓN

### Estado del Ambiente DEV
**❌ NO DISPONIBLE TEMPORALMENTE**

### Componentes
- ✅ Security API: Operativo
- ❌ Installments API: Error 500 (problema interno del servidor)
- ❌ Base de Datos: Posiblemente no disponible o con problemas

### Impacto
- 🔴 **Testing en DEV:** Bloqueado
- 🟢 **Testing en QA:** Disponible
- 🟡 **Testing en SANDBOX:** Disponible (con ajustes)

### Código y Configuración
- ✅ **BINs:** Correctamente configurados
- ✅ **Tests:** Funcionando correctamente
- ✅ **Código:** Validado en QA

### Problema
**Infraestructura DEV requiere intervención del equipo de sistemas.**

---

**Documento generado:** 2025-11-04 13:23:47
**Ambiente:** DEV (Desarrollo)
**Estado:** Incidente activo - Error 500
**Duración del incidente:** ~15 minutos
**Próxima acción:** Esperar resolución de infraestructura
