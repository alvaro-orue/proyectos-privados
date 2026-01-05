# Evidencias de Prueba - Caso 03: Operación de Depósito

**Fecha de Ejecución:** 2026-01-05
**Hora de Ejecución:** 01:19 UTC
**Caso de Prueba:** CP-POS-003

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
transactionId: ONTE176758858
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176758858",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiIxNzY3NTkzOTQ4OTMxIiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NzU4ODU4IiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiI3MTMyMmY3ZS0wNWJmLTRmMjUtYTEyNy0xOWM5Y2M2ZjNhNDIiLCJuYmYiOjE3Njc1OTM5NDksImV4cCI6MTc2NzU5NDg0OSwiaWF0IjoxNzY3NTkzOTQ5fQ.QgxElaAXjETc4-_hYAbj0xcYgYDLVJmNVLE-HsllGiM",
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
transactionId: ONTE176758858
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176758858",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S16082",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1548093",
    "transactionDatetime": "2026-01-04 23:49:52.000",
    "datetimeTerminalTransaction": "2026-01-04 23:49:52.000"
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
    "transactionStartDatetime": "2026-01-05 01:19:09.501",
    "transactionEndDatetime": "2026-01-05 01:19:09.824",
    "millis": "323"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176758858",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "CARD",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S16082",
      "uniqueId": "1548093",
      "batchNumber": "1271"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1271

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S16082",
    "referenceNumber": "0861755",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176758858",
    "dateTransaction": "20260104",
    "timeTransaction": "234952",
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
    "uniqueId": "1548093",
    "signature": "pUUhF+5KrGfioTXa6YiJ7HIGn1zlQBXwM/iLrIYaFfw=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S16082\",\"referenceNumber\":\"0861755\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176758858\",\"dateTransaction\":\"20260104\",\"timeTransaction\":\"234952\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"MC\",\"pan\":\"520474******1127\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1548093\"}}"
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
| **Authorization Code** | S16082 |
| **Unique ID** | 1548093 |
| **Batch Number** | 1271 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176758858)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S16082)
[OK] **UniqueId correcto** (1548093)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
