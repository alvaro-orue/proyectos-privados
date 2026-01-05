# Evidencias de Prueba - Caso 09: Operación de Depósito

**Fecha de Ejecución:** 2026-01-05
**Hora de Ejecución:** 01:19 UTC
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
transactionId: ONTE176758874
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176758874",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiIxNzY3NTkzOTU1Mjg4IiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NzU4ODc0IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiIxMTk5MDBiNS00N2YzLTRkOWYtODZhNC0yNGQ3ZGM0YzVmYjQiLCJuYmYiOjE3Njc1OTM5NTUsImV4cCI6MTc2NzU5NDg1NSwiaWF0IjoxNzY3NTkzOTU1fQ.Nd1zo4Btulc0_z6VibCwn0-tIozrMfe8LEyAeKLh9cY",
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
transactionId: ONTE176758874
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176758874",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S91012",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1548099",
    "transactionDatetime": "2026-01-04 23:52:32.000",
    "datetimeTerminalTransaction": "2026-01-04 23:52:32.000"
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
    "transactionStartDatetime": "2026-01-05 01:19:15.896",
    "transactionEndDatetime": "2026-01-05 01:19:16.118",
    "millis": "222"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176758874",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "CARD",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S91012",
      "uniqueId": "1548099",
      "batchNumber": "1277"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1277

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S91012",
    "referenceNumber": "0716537",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176758874",
    "dateTransaction": "20260104",
    "timeTransaction": "235232",
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
    "uniqueId": "1548099",
    "signature": "xtS92YiYN3odnjBmaA+1OY3yQlPXcN95fojsgBOGYm8=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S91012\",\"referenceNumber\":\"0716537\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176758874\",\"dateTransaction\":\"20260104\",\"timeTransaction\":\"235232\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"MC\",\"pan\":\"520474******1127\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1548099\"}}"
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
| **Authorization Code** | S91012 |
| **Unique ID** | 1548099 |
| **Batch Number** | 1277 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176758874)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S91012)
[OK] **UniqueId correcto** (1548099)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
