# Evidencias de Prueba - Caso 01: Operación de Depósito

**Fecha de Ejecución:** 2026-01-05
**Hora de Ejecución:** 01:19 UTC
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
transactionId: ONTE176758768
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176758768",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiIxNzY3NTkzOTQwMjMzIiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NzU4NzY4IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiI1MGU0MjdlNS1lOGE5LTRkZjEtOTY1Mi03YmJjNTQwYTk4ZjUiLCJuYmYiOjE3Njc1OTM5NDAsImV4cCI6MTc2NzU5NDg0MCwiaWF0IjoxNzY3NTkzOTQwfQ.vEkfIThXk_CcY7Dmi2SC_FTprtQMMiJB1wT8b9eyvYo",
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
transactionId: ONTE176758768
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176758768",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S14939",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1548091",
    "transactionDatetime": "2026-01-04 23:37:14.000",
    "datetimeTerminalTransaction": "2026-01-04 23:37:14.000"
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
    "transactionStartDatetime": "2026-01-05 01:19:01.058",
    "transactionEndDatetime": "2026-01-05 01:19:06.207",
    "millis": "5149"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176758768",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "CARD",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S14939",
      "uniqueId": "1548091",
      "batchNumber": "1269"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1269

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S14939",
    "referenceNumber": "0775524",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176758768",
    "dateTransaction": "20260104",
    "timeTransaction": "233714",
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
    "uniqueId": "1548091",
    "signature": "U/Ta2FsC2BM4Xd8/loZHF4mYq2moQsLpxiKNAOp2vlE=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S14939\",\"referenceNumber\":\"0775524\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176758768\",\"dateTransaction\":\"20260104\",\"timeTransaction\":\"233714\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"MC\",\"pan\":\"520474******1127\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1548091\"}}"
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
| **Authorization Code** | S14939 |
| **Unique ID** | 1548091 |
| **Batch Number** | 1269 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176758768)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S14939)
[OK] **UniqueId correcto** (1548091)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
