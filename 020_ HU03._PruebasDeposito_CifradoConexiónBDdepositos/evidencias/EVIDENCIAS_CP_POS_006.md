# Evidencias de Prueba - Caso 06: Operación de Depósito

**Fecha de Ejecución:** 2026-01-05
**Hora de Ejecución:** 01:19 UTC
**Caso de Prueba:** CP-POS-006

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
transactionId: ONTE176758866
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176758866",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiIxNzY3NTkzOTUyNzQ0IiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NzU4ODY2IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiI5ZmI5YzI2MS05YmI1LTQzZTUtOGIzZi01MzEyNTI5ODhmYjIiLCJuYmYiOjE3Njc1OTM5NTMsImV4cCI6MTc2NzU5NDg1MywiaWF0IjoxNzY3NTkzOTUzfQ.hlYVKBhS1LLY0V4va-r0M6Ncp6MA7kG3T5eM2WzvmTI",
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
transactionId: ONTE176758866
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176758866",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S76362",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1548096",
    "transactionDatetime": "2026-01-04 23:51:09.000",
    "datetimeTerminalTransaction": "2026-01-04 23:51:09.000"
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
    "transactionStartDatetime": "2026-01-05 01:19:13.333",
    "transactionEndDatetime": "2026-01-05 01:19:13.672",
    "millis": "339"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176758866",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "CARD",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S76362",
      "uniqueId": "1548096",
      "batchNumber": "1274"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1274

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S76362",
    "referenceNumber": "0967424",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176758866",
    "dateTransaction": "20260104",
    "timeTransaction": "235109",
    "payMethod": "CARD",
    "card": {
      "brand": "MC",
      "pan": "520474******1127",
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
    "uniqueId": "1548096",
    "signature": "LPss8pn8hQRGJDGO6abtlaeCoGoE7tvjolSSyp81OvE=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S76362\",\"referenceNumber\":\"0967424\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176758866\",\"dateTransaction\":\"20260104\",\"timeTransaction\":\"235109\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"MC\",\"pan\":\"520474******1127\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1548096\"}}"
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
| **Método de Pago** | CARD (MC 520474******1127) |
| **Canal** | ecommerce |
| **Authorization Code** | S76362 |
| **Unique ID** | 1548096 |
| **Batch Number** | 1274 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176758866)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S76362)
[OK] **UniqueId correcto** (1548096)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
