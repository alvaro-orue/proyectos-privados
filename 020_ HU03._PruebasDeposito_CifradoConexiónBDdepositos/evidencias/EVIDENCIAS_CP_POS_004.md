# Evidencias de Prueba - Caso 04: Operación de Depósito

**Fecha de Ejecución:** 2025-11-28
**Hora de Ejecución:** 01:26 UTC
**Caso de Prueba:** CP-POS-004

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
transactionId: ONTE176431102
```

**Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ONTE176431102",
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAxODM0IiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJPTlRFMTc2NDMxMTAyIiwiT3JkZXJOdW1iZXIiOiJPTlRFMTc2NDMxMTAyIiwiQW1vdW50IjoiMS4wMCIsIlRva2VuSWQiOiIzMDU2MjM3Mi1hZGU3LTQyODctOWZmNS1kM2E4N2MwMDk3ZGQiLCJuYmYiOjE3NjQzMTEyMTcsImV4cCI6MTc2NDMxMjExNywiaWF0IjoxNzY0MzExMjE3fQ.gX_8Le47Nmm0NUeVADklvyZv-y4X-6HDkSpAoqgllLE",
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
transactionId: ONTE176431102
```

**Body:**
```json
{
  "merchantCode": "4001834",
  "order": {
    "orderNumber": "ONTE176431102",
    "currency": "PEN",
    "amount": "1.00",
    "authorizationCode": "S99091",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "1546803",
    "transactionDatetime": "2025-11-28 01:23:55.000",
    "datetimeTerminalTransaction": "2025-11-28 01:23:55.000"
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
    "transactionStartDatetime": "2025-11-28 01:26:57.990",
    "transactionEndDatetime": "2025-11-28 01:26:58.228",
    "millis": "238"
  },
  "code": "00",
  "message": "OperaciÃ³n satisfactoria",
  "response": {
    "merchantCode": "4001834",
    "order": {
      "orderNumber": "ONTE176431102",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "card",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "OperaciÃ³n satisfactoria",
      "authorizationCode": "S99091",
      "uniqueId": "1546803",
      "batchNumber": "1244"
    }
  }
}
```

**Resultado:** [OK] Deposito procesado exitosamente
**Batch Number:** 1244

---

## 4. Datos de la Transacción Original

```json
{
  "code": "00",
  "message": "OK",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "codeAuth": "S99091",
    "referenceNumber": "0328523",
    "merchantCode": "4001834",
    "currency": "PEN",
    "amount": "1.00",
    "orderNumber": "ONTE176431102",
    "dateTransaction": "20251128",
    "timeTransaction": "012355",
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
    "uniqueId": "1546803",
    "signature": "ohPokLl6p6+sLE+srtLGNseeEWQHzFy81oyJlpEzI7g=",
    "payloadHttp": "{\"code\":\"00\",\"message\":\"OK\",\"messageUser\":\"Operación exitosa\",\"messageUserEng\":\"Successful\",\"response\":{\"codeAuth\":\"S99091\",\"referenceNumber\":\"0328523\",\"merchantCode\":\"4001834\",\"currency\":\"PEN\",\"amount\":\"1.00\",\"orderNumber\":\"ONTE176431102\",\"dateTransaction\":\"20251128\",\"timeTransaction\":\"012355\",\"idLogMPI\":0,\"payMethod\":\"CARD\",\"card\":{\"brand\":\"AE\",\"pan\":\"377753*****0152\",\"save\":false},\"billing\":{\"firstName\":\"Juan\",\"lastName\":\"Wick quispe\",\"email\":\"jwick@gmail.com\",\"phoneNumber\":\"989339999\",\"street\":\"calle el demo\",\"city\":\"lima\",\"state\":\"lima\",\"country\":\"PE\",\"postalCode\":\"00001\",\"documentType\":\"DNI\",\"document\":\"10252022\",\"companyName\":\"\"},\"uniqueId\":\"1546803\"}}"
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
| **Authorization Code** | S99091 |
| **Unique ID** | 1546803 |
| **Batch Number** | 1244 |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones (ONTE176431102)
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** (PEN 1.00)
[OK] **Authorization Code válido** (S99091)
[OK] **UniqueId correcto** (1546803)
[OK] **Response Code 00** indica operación exitosa
[OK] **Batch Number asignado** confirma procesamiento

---

**Fin del Documento**
