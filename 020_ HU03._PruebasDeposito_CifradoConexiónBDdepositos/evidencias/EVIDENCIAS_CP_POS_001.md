# Evidencias de Prueba - Caso 01: Operación de Depósito

**Fecha de Ejecución:** 2025-11-28
**Hora de Ejecución:** 01:26 UTC
**Caso de Prueba:** CP-POS-001

---

## 1. Datos del Comercio

```
Merchant Code: 4001834
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
Ambiente: Test (https://testapi-pw.izipay.pe)
```

---

## 2. Paso 1: Generación de Token de Sesión

### 2.1. Request - Generar Token

**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`

**Headers:**
```
Accept: application/json
Content-Type: application/json
transactionId: ONTE176431091
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176431091",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "1.00"
}
```

### 2.2. Response - Token Generado

**HTTP Status:** 200 OK

**Response Body:**
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJPTlRFMTc2NDMxMDkxIiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NDMxMDkxIiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiIyZjZhMTIzNy1iMmY2LTQ1MGYtYTNlNS00Y2U5MjRhNjBjOGEiLCJuYmYiOjE3NjQzMTEyMTQsImV4cCI6MTc2NDMxMjExNCwiaWF0IjoxNzY0MzExMjE0fQ.RC8nXoZa9XcKJ6FVzaOfxxu6z4EiB49cw1V0hRYkm1M",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_low"
  }
}
```

**Resultado:** [OK] Token generado exitosamente

---

## 3. Paso 2: Operación de Depósito

### 3.1. Request - Realizar Depósito

**Endpoint:** `POST https://testapi-pw.izipay.pe/capture/v1/Transaction/Deposit`

**Headers:**
```
Accept: application/json
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFud...
transactionId: ONTE176431091
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176431091",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S16270",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1546800",
    "transactionDatetime": "2025-11-28 01:22:29.000",
    "datetimeTerminalTransaction": "2025-11-28 01:22:29.000"
  },
  "language": "ESP"
}
```

### 3.2. Response - Depósito Exitoso

**HTTP Status:** 200 OK

**Response Body:**
```json
{
  "header": {
    "transactionStartDatetime": "2025-11-28 01:26:55.204",
    "transactionEndDatetime": "2025-11-28 01:26:55.454",
    "millis": "250"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176431091",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "card",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S16270",
      "uniqueId": "1546800",
      "batchNumber": "1241"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1241

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S16270",
    "referenceNumber": "0185200",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176431091",
    "dateTransaction": "20251128",
    "timeTransaction": "012229",
    "payMethod": "CARD",
    "card": {
      "brand": "AE",
      "pan": "377753*****0152",
      "save": false
    },
    "billing": {
      "firstName": "Juan",
      "lastName": "Wick quispe",
      "email": "jwick@gmail.com",
      "phoneNumber": "989339999",
      "street": "calle el demo",
      "city": "lima",
      "state": "lima",
      "country": "PE",
      "postalCode": "00001",
      "documentType": "DNI",
      "document": "10252022",
      "companyName": ""
    },
    "uniqueId": "1546800",
    "signature": "JjfEEH+t8F3RzkNBUQpuBIc9lg7G8IXvUVOIgc2qJBU=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S16270\",\"referenceNumber\":\"0185200\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176431091\",\"dateTransaction\":\"20251128\",\"timeTransaction\":\"012229\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"AE\",\"pan\":\"377753*****0152\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1546800\"}}"
  }
}
```

---

## 5. Resumen de Resultados

| Aspecto | Detalle |
|---------|---------|
| **Estado General** | [OK] EXITOSO |
| **Generación de Token** | [OK] Exitosa (Code: 00) |
| **Operación de Depósito** | [OK] Exitosa (Code: 00) |
| **Monto Depositado** | PEN 1.00 |
| **Método de Pago** | CARD (AE 377753*****0152) |
| **Canal** | ecommerce |
| **Authorization Code** | S16270 |
| **Unique ID** | 1546800 |
| **Batch Number** | 1241 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176431091)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S16270)
[OK] **UniqueId correcto** (1546800)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
