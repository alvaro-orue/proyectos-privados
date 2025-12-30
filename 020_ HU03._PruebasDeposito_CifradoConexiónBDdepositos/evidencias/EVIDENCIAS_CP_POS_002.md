# Evidencias de Prueba - Caso 02: Operación de Depósito

**Fecha de Ejecución:** 2025-11-28
**Hora de Ejecución:** 01:26 UTC
**Caso de Prueba:** CP-POS-002

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
transactionId: ONTE176431096
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176431096",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJPTlRFMTc2NDMxMDk2IiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NDMxMDk2IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiI1NDZjYTU3ZS04NzY5LTQyNDgtOTk0MS01YTRiZTkzODRlODQiLCJuYmYiOjE3NjQzMTEyMTUsImV4cCI6MTc2NDMxMjExNSwiaWF0IjoxNzY0MzExMjE1fQ.j6HovV1WDiiaZL2Dvp6lUd9haSH2xnAN1Kp2Ns5O358",
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
transactionId: ONTE176431096
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176431096",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S41305",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1546801",
    "transactionDatetime": "2025-11-28 01:22:58.000",
    "datetimeTerminalTransaction": "2025-11-28 01:22:58.000"
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
    "transactionStartDatetime": "2025-11-28 01:26:56.103",
    "transactionEndDatetime": "2025-11-28 01:26:56.336",
    "millis": "233"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176431096",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "card",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S41305",
      "uniqueId": "1546801",
      "batchNumber": "1242"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1242

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S41305",
    "referenceNumber": "0497539",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176431096",
    "dateTransaction": "20251128",
    "timeTransaction": "012258",
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
    "uniqueId": "1546801",
    "signature": "ZfSZ10fVLyNZX3fUUSa/VeoZ8eLv3JUHg7+b0kDtiUo=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S41305\",\"referenceNumber\":\"0497539\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176431096\",\"dateTransaction\":\"20251128\",\"timeTransaction\":\"012258\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"AE\",\"pan\":\"377753*****0152\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1546801\"}}"
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
| **Authorization Code** | S41305 |
| **Unique ID** | 1546801 |
| **Batch Number** | 1242 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176431096)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S41305)
[OK] **UniqueId correcto** (1546801)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
