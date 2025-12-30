# Evidencias de Prueba - Caso 08: Operación de Depósito

**Fecha de Ejecución:** 2025-11-28
**Hora de Ejecución:** 01:27 UTC
**Caso de Prueba:** CP-POS-008

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
transactionId: ONTE176431114
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176431114",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJPTlRFMTc2NDMxMTE0IiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NDMxMTE0IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiI4MDdmYmM5NC1jZTAyLTQxMmItYmU0NC0xZmIzNzRmZTg2NGMiLCJuYmYiOjE3NjQzMTEyMjEsImV4cCI6MTc2NDMxMjEyMSwiaWF0IjoxNzY0MzExMjIxfQ.YtpjHDmU48EvjxKXt7XjO61m1BuO6_z-vav20exE3Ns",
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
transactionId: ONTE176431114
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176431114",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S42032",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1546807",
    "transactionDatetime": "2025-11-28 01:26:07.000",
    "datetimeTerminalTransaction": "2025-11-28 01:26:07.000"
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
    "transactionStartDatetime": "2025-11-28 01:27:01.827",
    "transactionEndDatetime": "2025-11-28 01:27:01.994",
    "millis": "167"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176431114",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "card",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S42032",
      "uniqueId": "1546807",
      "batchNumber": "1248"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1248

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S42032",
    "referenceNumber": "0822156",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176431114",
    "dateTransaction": "20251128",
    "timeTransaction": "012607",
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
    "uniqueId": "1546807",
    "signature": "y4/1m1bbQ2Ah8HMl2mf4vv5qsolb24M+o+CKZzE7ZWc=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S42032\",\"referenceNumber\":\"0822156\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176431114\",\"dateTransaction\":\"20251128\",\"timeTransaction\":\"012607\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"AE\",\"pan\":\"377753*****0152\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1546807\"}}"
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
| **Authorization Code** | S42032 |
| **Unique ID** | 1546807 |
| **Batch Number** | 1248 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176431114)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S42032)
[OK] **UniqueId correcto** (1546807)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
