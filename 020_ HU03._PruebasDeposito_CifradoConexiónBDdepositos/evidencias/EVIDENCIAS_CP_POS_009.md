# Evidencias de Prueba - Caso 09: Operación de Depósito

**Fecha de Ejecución:** 2025-11-28
**Hora de Ejecución:** 01:27 UTC
**Caso de Prueba:** CP-POS-009

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
transactionId: ONTE176431118
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176431118",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJPTlRFMTc2NDMxMTE4IiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NDMxMTE4IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiIzZWEzM2Q5OC1kMDkxLTQzMjMtOThkYy0xM2I3YWMyODcyM2UiLCJuYmYiOjE3NjQzMTEyMjIsImV4cCI6MTc2NDMxMjEyMiwiaWF0IjoxNzY0MzExMjIyfQ.WDoCKzieNUmZOBXyUy68MXFqZjm1hcymkvkJ_D79OYU",
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
transactionId: ONTE176431118
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176431118",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S59279",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1546808",
    "transactionDatetime": "2025-11-28 01:26:36.000",
    "datetimeTerminalTransaction": "2025-11-28 01:26:36.000"
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
    "transactionStartDatetime": "2025-11-28 01:27:02.805",
    "transactionEndDatetime": "2025-11-28 01:27:02.988",
    "millis": "183"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176431118",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "card",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S59279",
      "uniqueId": "1546808",
      "batchNumber": "1249"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1249

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S59279",
    "referenceNumber": "0753334",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176431118",
    "dateTransaction": "20251128",
    "timeTransaction": "012636",
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
    "uniqueId": "1546808",
    "signature": "xeUB8TUJe92CUUn62oo4bQAlb2QW31f7buUrFFJ+UTE=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S59279\",\"referenceNumber\":\"0753334\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176431118\",\"dateTransaction\":\"20251128\",\"timeTransaction\":\"012636\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"AE\",\"pan\":\"377753*****0152\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1546808\"}}"
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
| **Authorization Code** | S59279 |
| **Unique ID** | 1546808 |
| **Batch Number** | 1249 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176431118)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S59279)
[OK] **UniqueId correcto** (1546808)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
