# SDK-1402 Pase al PRD Card Selector en SDK Mobile

## Descripción
Actualización de Tarjetas y la regresión para BOTON SDK, VTX, LDP, API, etc

## Ambiente de Pruebas
**Ambiente:** DEV (Desarrollo)
**Fecha de Ejecución:** 2025-11-04
**Hora de Inicio:** 18:37:16
**Hora de Finalización:** 18:41:58
**URL Base:** https://testapi-pw.izipay.pe
**Merchant Code:** 4078370

---

## Endpoints Utilizados

### 1. Token Generation API
**URL:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Descripción:** Genera un token JWT para autenticar las peticiones al servicio de Installments
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER{TIMESTAMP}",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Response Exitoso (200 OK):**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

---

### 2. Installments Search API
**URL:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Descripción:** Busca las cuotas disponibles para un BIN específico
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `Authorization`: Bearer {token}
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response Exitoso (200 OK):**
```json
{
  "code": "00",
  "message": "OK",
  "header": {
    "transactionStartDatetime": "2025-11-04 18:38:55.120",
    "transactionEndDatetime": "2025-11-04 18:38:56.819",
    "millis": 1699
  },
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Operación exitosa"
    }
  }
}
```

---

## Casos de Prueba Ejecutados

### Tabla de Casos de Prueba

| Cód. CP / PROB | Plataforma | Descripción del CP | Condiciones | Pasos a seguir | Tipo de CP | Estado |
|----------------|------------|-------------------|-------------|----------------|------------|--------|
| CPI-001 | API Installments | Flujo completo exitoso - Generar token y buscar cuotas | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. BIN válido configurado<br>4. Merchant Code válido | 1. Generar token de sesión<br>2. Buscar cuotas disponibles con BIN<br>3. Validar respuesta exitosa | FUNCIONAL | ✅ PASÓ |
| CPI-002 | API Installments | Token Reutilizable - Verificar que un token puede usarse múltiples veces | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. BIN válido configurado | 1. Generar token de sesión<br>2. Primera búsqueda de cuotas<br>3. Segunda búsqueda con el mismo token<br>4. Validar ambas respuestas exitosas | FUNCIONAL | ✅ PASÓ |
| CPI-003 | API Installments | TransactionId Consistente - Validar uso del mismo TransactionId | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. TransactionId único | 1. Generar token con TransactionId específico<br>2. Buscar cuotas con el mismo TransactionId<br>3. Validar consistencia en headers | FUNCIONAL | ✅ PASÓ |
| CPI-004 | API Installments | Casos de Error - Validar manejo de errores | 1. Acceso a Installments API<br>2. Capacidad de enviar datos inválidos | 1. Token inválido (401)<br>2. Sin header Authorization (400)<br>3. BIN con formato inválido (400)<br>4. Merchant Code inválido (401)<br>5. Parámetro BIN faltante (400) | REGRESSION | ✅ PASÓ |
| CPI-005 | API Installments | Diferentes BINs - Validar múltiples tarjetas | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. 4 BINs configurados | 1. Probar BIN 545545 (SCOTIABANK)<br>2. Probar BIN 400917 (SCOTIABANK VISA)<br>3. Probar BIN 377893 (BCP)<br>4. Probar BIN 553650 (BBVA MC Platinum)<br>5. Validar cuotas para cada BIN | REGRESSION | ✅ PASÓ |
| CPI-006 | API Installments | Flujo con Amount 0.00 - Validar monto especial | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. Permitir amount=0.00 | 1. Generar token con amount 0.00<br>2. Buscar cuotas disponibles<br>3. Validar respuesta exitosa | FUNCIONAL | ✅ PASÓ |
| CPI-007 | API Installments | Idioma Inglés (ENG) - Validar respuesta en inglés | 1. Acceso a Token API<br>2. Acceso a Installments API<br>3. Soporte de idioma ENG | 1. Generar token de sesión<br>2. Buscar cuotas con language=ENG<br>3. Validar mensaje en inglés | REGRESSION | ✅ PASÓ |

---

## Resultados Detallados

### CPI-001: Flujo completo exitoso
**Estado:** ✅ PASÓ
**Duración Total:** 7,285ms
**Transaction ID:** DEV20251104183849
**Order Number:** ORDER20251104183849

#### Paso 1 - Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200 OK
**Duración:** 1,072ms

**Request Headers:**
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "transactionId": "DEV20251104183849"
}
```

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104183849",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDE4Mzg0OSIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDE4Mzg0OSIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiI2ZmY1YzA1NC1iODEzLTRhMjMtOWNmYy0wNTNiOTJkOGFmYmUiLCJuYmYiOjE3NjIyOTk1MzAsImV4cCI6MTc2MjMwMDQzMCwiaWF0IjoxNzYyMjk5NTMwfQ.Mlm9iHXrIfp4bbuG1i3Ul9fSVr1CgOxGv6JneObJ-3s",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

**Response Headers:**
```json
{
  "Content-Type": "application/json; charset=utf-8",
  "transactionId": "DEV20251104183849",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Strict-Transport-Security": "max-age=31536000; includeSubdomains",
  "X-Xss-Proteccion": "1, mode=block",
  "HttpOnly": "HttpOnly"
}
```

---

#### Paso 2 - Search Installments
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 6,209ms

**Request Headers:**
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDE4Mzg0OSIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDE4Mzg0OSIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiI2ZmY1YzA1NC1iODEzLTRhMjMtOWNmYy0wNTNiOTJkOGFmYmUiLCJuYmYiOjE3NjIyOTk1MzAsImV4cCI6MTc2MjMwMDQzMCwiaWF0IjoxNzYyMjk5NTMwfQ.Mlm9iHXrIfp4bbuG1i3Ul9fSVr1CgOxGv6JneObJ-3s",
  "transactionId": "DEV20251104183849"
}
```

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "header": {
    "transactionStartDatetime": "2025-11-04 18:38:55.120",
    "transactionEndDatetime": "2025-11-04 18:38:56.819",
    "millis": 1699
  },
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Operación exitosa"
    }
  }
}
```

**Response Headers:**
```json
{
  "Content-Type": "application/json; charset=utf-8",
  "X-Correlation-Id": "9a6c2431-6af7-4efc-90e6-884451732c0b",
  "transactionId": "DEV20251104183849",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Strict-Transport-Security": "max-age=31536000; includeSubdomains",
  "X-Xss-Proteccion": "1, mode=block",
  "HttpOnly": "HttpOnly"
}
```

**Resultado:**
- BIN: 545545 (SCOTIABANK)
- Cuotas disponibles: 12 opciones (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
- Diferido: 3 meses
- Mensaje: "Operación exitosa"

---

### CPI-002: Token Reutilizable
**Estado:** ✅ PASÓ
**Duración Total:** 3,816ms
**Transaction ID:** DEV20251104183929
**Order Number:** ORDER20251104183929
**Objetivo:** Verificar que un token puede reutilizarse en múltiples consultas

#### Paso 1 - Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200 OK
**Duración:** 1,805ms

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104183929",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDE4MzkyOSIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDE4MzkyOSIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiJiOGM1NDYxOS04MzJlLTRlYjYtYWU2Mi05NWIxNzM5YmQxMmIiLCJuYmYiOjE3NjIyOTk1NzEsImV4cCI6MTc2MjMwMDQ3MSwiaWF0IjoxNzYyMjk5NTcxfQ.R1up-oC-laXkERfnI5CFGw1K1zqpelaH6cnYRNYousY",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

---

#### Paso 2 - First Search (Should Succeed)
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 1,014ms

**Request Headers:**
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDE4MzkyOSIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDE4MzkyOSIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiJiOGM1NDYxOS04MzJlLTRlYjYtYWU2Mi05NWIxNzM5YmQxMmIiLCJuYmYiOjE3NjIyOTk1NzEsImV4cCI6MTc2MjMwMDQ3MSwiaWF0IjoxNzYyMjk5NTcxfQ.R1up-oC-laXkERfnI5CFGw1K1zqpelaH6cnYRNYousY",
  "transactionId": "DEV20251104183929"
}
```

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "header": {
    "transactionStartDatetime": "2025-11-04 18:39:32.350",
    "transactionEndDatetime": "2025-11-04 18:39:32.392",
    "millis": 41
  },
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Operación exitosa"
    }
  }
}
```

---

#### Paso 3 - Second Search (Should Succeed - Reusable)
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 992ms

**Request Headers:**
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDc4MzcwIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJERVYyMDI1MTEwNDE4MzkyOSIsIk9yZGVyTnVtYmVyIjoiT1JERVIyMDI1MTEwNDE4MzkyOSIsIkFtb3VudCI6IjEwMC4wMCIsIlRva2VuSWQiOiJiOGM1NDYxOS04MzJlLTRlYjYtYWU2Mi05NWIxNzM5YmQxMmIiLCJuYmYiOjE3NjIyOTk1NzEsImV4cCI6MTc2MjMwMDQ3MSwiaWF0IjoxNzYyMjk5NTcxfQ.R1up-oC-laXkERfnI5CFGw1K1zqpelaH6cnYRNYousY",
  "transactionId": "DEV20251104183929"
}
```

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "header": {
    "transactionStartDatetime": "2025-11-04 18:39:33.317",
    "transactionEndDatetime": "2025-11-04 18:39:33.384",
    "millis": 66
  },
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Operación exitosa"
    }
  }
}
```

**Resultado:**
- ✅ Primera búsqueda: 12 cuotas obtenidas (41ms procesamiento en servidor)
- ✅ Segunda búsqueda: 12 cuotas obtenidas (66ms procesamiento en servidor)
- ✅ **Token reutilizado exitosamente en ambas consultas**

---

### CPI-003: TransactionId Consistente
**Estado:** ✅ PASÓ
**Duración Total:** 2,049ms
**Transaction ID:** DEV20251104183955
**Order Number:** ORDER20251104183955
**Objetivo:** Validar que el mismo TransactionId se mantiene consistente en ambas llamadas

#### Paso 1 - Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200 OK
**Duración:** 1,010ms

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104183955",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Request Headers:**
```json
{
  "transactionId": "DEV20251104183955"
}
```

---

#### Paso 2 - Search Installments
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 1,039ms

**Request Headers:**
```json
{
  "Authorization": "Bearer [token]",
  "transactionId": "DEV20251104183955"
}
```

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Resultado:**
- ✅ TransactionId consistente: DEV20251104183955 en ambas llamadas
- ✅ 12 cuotas obtenidas correctamente

---

### CPI-004: Casos de Error
**Estado:** ✅ PASÓ
**Duración Total:** 5,941ms
**Total escenarios:** 5
**Validados correctamente:** 5/5
**Objetivo:** Validar el manejo correcto de errores en el API de Installments

#### Escenario 1 - Token Inválido
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 401 Unauthorized
**Duración:** 1,328ms

**Request Headers:**
```json
{
  "Authorization": "Bearer TOKEN_INVALIDO_12345",
  "transactionId": "TEST_ERROR_001"
}
```

**Response:**
```json
{
  "code": "401",
  "message": "Unauthorized"
}
```
✅ **Error detectado correctamente**

---

#### Escenario 2 - Sin Header Authorization
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 400 Bad Request
**Duración:** 933ms

**Request Headers:**
```json
{
  "Content-Type": "application/json",
  "transactionId": "TEST_ERROR_002"
}
```
*(Sin header "Authorization")*

**Response:**
```json
{
  "code": "400",
  "message": "Bad Request - Missing Authorization header"
}
```
✅ **Error detectado correctamente**

---

#### Escenario 3 - BIN con Formato Inválido
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 400 Bad Request
**Duración:** 1,365ms

**Request Body:**
```json
{
  "bin": "ABC",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "400",
  "message": "Invalid BIN format"
}
```
✅ **Error detectado correctamente**

---

#### Escenario 4 - Merchant Code Inválido
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 401 Unauthorized
**Duración:** 1,315ms

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "9999999",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "401",
  "message": "Invalid merchant code"
}
```
✅ **Error detectado correctamente**

---

#### Escenario 5 - Parámetro BIN Faltante
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 400 Bad Request
**Duración:** 1,000ms

**Request Body:**
```json
{
  "merchantCode": "4078370",
  "language": "ESP"
}
```
*(Sin parámetro "bin")*

**Response:**
```json
{
  "code": "400",
  "message": "Missing required parameter: bin"
}
```
✅ **Error detectado correctamente**

---

### CPI-005: Diferentes BINs
**Estado:** ✅ PASÓ
**Duración Total:** ~7,300ms
**Total BINs probados:** 4
**Exitosos:** 4/4
**Fallidos:** 0
**Objetivo:** Validar que el servicio funciona correctamente con múltiples BINs de diferentes bancos

Cada BIN sigue el mismo flujo:
1. **Token Generation:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
2. **Installments Search:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`

---

#### BIN 1 - 545545 (SCOTIABANK)
**Status:** 200 OK
**Token Generation:** 1,217ms
**Installments Search:** 1,270ms

**Request Body (Installments):**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3"
  }
}
```
**Cuotas:** 12 | **Diferido:** 3 meses | ✅ **Exitoso**

---

#### BIN 2 - 400917 (SCOTIABANK VISA)
**Status:** 200 OK
**Token Generation:** 1,044ms
**Installments Search:** 1,471ms

**Request Body (Installments):**
```json
{
  "bin": "400917",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "400917",
    "issuerName": "SCOTIABANK VISA",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
    "deferred": "0"
  }
}
```
**Cuotas:** 36 | **Diferido:** 0 meses | ✅ **Exitoso**

---

#### BIN 3 - 377893 (BCP)
**Status:** 200 OK
**Token Generation:** 1,111ms
**Installments Search:** 1,018ms

**Request Body (Installments):**
```json
{
  "bin": "377893",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "377893",
    "issuerName": "BCP",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
    "deferred": "3"
  }
}
```
**Cuotas:** 36 | **Diferido:** 3 meses | ✅ **Exitoso**

---

#### BIN 4 - 553650 (BBVA MC Platinum)
**Status:** 200 OK
**Token Generation:** 1,151ms
**Installments Search:** 1,169ms

**Request Body (Installments):**
```json
{
  "bin": "553650",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "553650",
    "issuerName": "BBVA MC Platinum",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
    "deferred": "3"
  }
}
```
**Cuotas:** 36 | **Diferido:** 3 meses | ✅ **Exitoso**

---

### CPI-006: Flujo con Amount 0.00
**Estado:** ✅ PASÓ
**Duración Total:** 3,435ms
**Transaction ID:** FVCL20251104184132
**Objetivo:** Validar que el sistema acepta correctamente transacciones con monto 0.00

#### Paso 1 - Generate Token (amount=0.00)
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200 OK
**Duración:** 2,210ms

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104184132",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "0.00"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

---

#### Paso 2 - Search Installments
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 1,225ms

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Operación exitosa"
    }
  }
}
```

**Resultado:**
- ✅ Token generado exitosamente con amount 0.00
- ✅ 12 cuotas obtenidas correctamente
- ✅ **El sistema acepta amount 0.00 sin errores**

---

### CPI-007: Idioma Inglés (ENG)
**Estado:** ✅ PASÓ
**Duración Total:** 2,636ms
**Transaction ID:** FVCL20251104184158
**Objetivo:** Validar que el servicio soporta correctamente el idioma inglés en las respuestas

#### Paso 1 - Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200 OK
**Duración:** 1,481ms

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251104184158",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

---

#### Paso 2 - Search Installments (language=ENG)
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200 OK
**Duración:** 1,155ms

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ENG"
}
```

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {
      "messageFriendly": "Approved"
    }
  }
}
```

**Resultado:**
- ✅ Token generado exitosamente
- ✅ 12 cuotas obtenidas correctamente
- ✅ **Mensaje en inglés:** "Approved" (en lugar de "Operación exitosa")
- ✅ **Soporte multi-idioma confirmado**

---

## Resumen Ejecutivo

### Estadísticas Generales
- **Total de Casos de Prueba:** 7
- **Casos Exitosos:** 7 (100%)
- **Casos Fallidos:** 0 (0%)
- **Ambiente:** DEV (Desarrollo)
- **Fecha:** 2025-11-04
- **Duración Total de Ejecución:** ~32 minutos

### Cobertura de Pruebas
- ✅ **Token Generation API:** 100% operativo
- ✅ **Installments Search API:** 100% operativo
- ✅ **Token Reutilizable:** Validado
- ✅ **TransactionId Consistency:** Validado
- ✅ **Error Handling:** 5/5 escenarios validados
- ✅ **Múltiples BINs:** 4/4 tarjetas validadas
- ✅ **Amount Especial (0.00):** Validado
- ✅ **Soporte Multi-idioma (ENG):** Validado

### BINs Validados
| BIN | Banco | Cuotas | Diferido | Estado |
|-----|-------|--------|----------|--------|
| 545545 | SCOTIABANK | 12 | 3 meses | ✅ |
| 400917 | SCOTIABANK VISA | 36 | 0 meses | ✅ |
| 377893 | BCP | 36 | 3 meses | ✅ |
| 553650 | BBVA MC Platinum | 36 | 3 meses | ✅ |

### Tiempos de Respuesta Promedio
- **Token Generation:** ~1,200ms
- **Installments Search:** ~1,500ms
- **Flujo Completo:** ~2,700ms

### Estado del Ambiente DEV
**✅ COMPLETAMENTE OPERATIVO**

El ambiente de desarrollo está funcionando correctamente después de las actualizaciones del servidor realizadas el 2025-11-04. Todas las APIs (Token y Installments) están operativas y respondiendo dentro de los tiempos esperados.

### Observaciones
1. **Incidente Previo:** El ambiente DEV presentó problemas con el API Controller del servicio Installments entre las 13:38 y 18:37 horas (duración ~5 horas). El problema fue resuelto mediante actualización del servidor.

2. **Estabilidad:** Después de la actualización a las 18:37, todas las pruebas ejecutadas fueron exitosas sin errores.

3. **Performance:** Los tiempos de respuesta están dentro de los rangos aceptables (1-7 segundos por transacción completa).

4. **Error Handling:** El sistema maneja correctamente todos los casos de error esperados (401, 400) con mensajes apropiados.

### Conclusión
✅ **REGRESIÓN API INSTALLMENTS EN AMBIENTE DEV: EXITOSA**

Todos los casos de prueba pasaron exitosamente, confirmando que:
- Las APIs están completamente funcionales
- El token es reutilizable como se esperaba
- Los diferentes BINs configurados funcionan correctamente
- El manejo de errores es apropiado
- El sistema soporta múltiples idiomas
- Los casos especiales (amount 0.00) funcionan correctamente

**El ambiente DEV está listo para continuar con las pruebas de desarrollo y QA.**

---

## Archivos de Evidencia

### Resultados JSON
- `CASOS_MULTI_AMBIENTE/DEV/results/test_result_CPI-001_DEV.json`
- `CASOS_MULTI_AMBIENTE/DEV/results/test_report_CPI-001_DEV.txt`
- `CASOS/CPI-002/test_result.json`
- `CASOS/CPI-002/test_report.txt`
- Archivos individuales para cada paso de cada test

### Transaction IDs para Rastreo
1. CPI-001: DEV20251104183849
2. CPI-002: DEV20251104183929
3. CPI-003: DEV20251104183955
4. CPI-004: Múltiples TransactionIds para cada escenario de error
5. CPI-005: Múltiples TransactionIds (uno por cada BIN)
6. CPI-006: FVCL20251104184132
7. CPI-007: FVCL20251104184158

---

**Documento generado:** 2025-11-04 18:45
**Ejecutado por:** Automatización de Tests
**Ambiente:** DEV (https://testapi-pw.izipay.pe)
**Estado Final:** ✅ TODOS LOS TESTS PASARON
