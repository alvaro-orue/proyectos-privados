# Documentación Técnica: Operación Depósito (Deposit)

**API de Izipay**

---

## 1. Descripción General

La operación **Depósito** (`/capture/v1/Transaction/Deposit`) es una funcionalidad de la API de Izipay que permite realizar transacciones de depósito en una cuenta específica. Esta característica está diseñada para agregar fondos a una cuenta de forma **segura y eficiente**, facilitando la gestión y el flujo de dinero en la aplicación del comercio.

## 2. Endpoint

| Método | URL | Entorno |
| :--- | :--- | :--- |
| `POST` | `/capture/v1/Transaction/Deposit` | `https://testapi-pw.izipay.pe` |

## 3. Seguridad

La solicitud requiere autenticación mediante una **API Key**.

| Tipo | Parámetro | Ubicación |
| :--- | :--- | :--- |
| API Key | `Authorization` | Header |

## 4. Parámetros de la Solicitud (Request)

La solicitud se compone de un **Header** y un **Body** en formato JSON.

### 4.1. Header

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transactionId` | `string` | Sí | ID único por cada transacción generada por el comercio. Debe ser el mismo que se envió al generar el token. | 5 a 40 caracteres | `16868479028040` |

### 4.2. Body (JSON)

El cuerpo de la solicitud contiene los siguientes campos principales:

| Campo | Tipo | Requerido | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| `merchantCode` | `string` | Sí | Código del comercio generado por Izipay. | `4007701` |
| `order` | `object` | Sí | Objeto que contiene los detalles de la compra. | Ver tabla 4.3 |
| `language` | `string` | No | Idioma del mensaje de respuesta. | `ESP` |

### 4.3. Objeto `order`

Este objeto anidado contiene todos los detalles transaccionales:

| Campo | Tipo | Requerido | Descripción | Restricciones | Valores Permitidos | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `orderNumber` | `string` | Sí | Número de Pedido de la transacción. Debe ser el mismo que fue enviado al generar el token de sesión. | 5 a 15 caracteres | N/A | `ONSAND171105514` |
| `currency` | `string` | Sí | Moneda de la Transacción. | 3 caracteres | `PEN`, `USD` | `PEN` |
| `amount` | `string<double>` | Sí | Monto de la Transacción. Entero con 2 decimales, usando separador decimal sin delimitador de miles. | 4 a 13 caracteres | N/A | `15.00` |
| `authorizationCode` | `string` | Sí | Código de Autorización de la compra, generado por el emisor de la tarjeta. | 0 a 10 caracteres | N/A | `S40961` |
| `payMethod` | `string` | Sí | Indicador del método de pago de la compra. | 2 a 50 caracteres | `CARD`, `QR`, `APPLE_PAY`, `YAPE_CODE`, `PAGO_PUSH` | `CARD` |
| `channel` | `string` | Sí | Canal donde se originó la operación. | 2 a 50 caracteres | `ecommerce`, `web`, `moto`, `mobile`, `reccurrence`, `izivirtual` | `ecommerce` |
| `uniqueId` | `string` | Sí | ID Único de la transacción de compra original de Pre-Autorización. | 0 a 40 caracteres | N/A | `449858741` |
| `transactionDatetime` | `string` | Sí | Fecha y Hora de la transacción enviado por el comercio o terminal. | 10 a 40 caracteres | N/A | `2024-02-22 14:30:45.123` |
| `datetimeTerminalTransaction` | `string` | Sí | Fecha y Hora de la transacción enviado por el comercio o terminal. | 10 a 40 caracteres | N/A | `2024-02-22 14:30:45.123` |
| `mile` | `object` | No | Objeto de millas (opcional). | N/A | N/A | N/A |

## 5. Ejemplo de Solicitud (cURL)

```bash
curl --request POST \
  --url https://testapi-pw.izipay.pe/capture/v1/Transaction/Deposit \
  --header 'Accept: application/json' \
  --header 'Authorization: 123' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
  "merchantCode": "4007701",
  "order": {
    "orderNumber": "ONSAND171105514",
    "currency": "PEN",
    "amount": "15.00",
    "authorizationCode": "S40961",
    "payMethod": "CARD",
    "channel": "ecommerce",
    "uniqueId": "449858741",
    "transactionDatetime": "2024-02-22 14:30:45.123",
    "datetimeTerminalTransaction": "2024-02-22 14:30:45.123",
    "mile": {
      "netMiles": "",
      "uniqueId": "1011173920740022",
      "authorizationCode": "VA00000",
      "referenceNumber": "PV10111"
    }
  },
  "language": "ESP"
}'
```

## 6. Estructura de la Respuesta (Response)

Una respuesta exitosa (`200 Success`) indica que la solicitud se ha procesado correctamente.

### 6.1. Objeto de Respuesta Exitoso (HTTP 200)

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `header` | `object` | Objeto que contiene metadatos de la transacción. |
| `code` | `string` | Código de respuesta de la autorización. `00` indica éxito. |
| `message` | `string` | Mensaje de respuesta de la autorización, según el idioma solicitado. |
| `response` | `object` | Objeto principal de la respuesta. |

### 6.2. Objeto `header`

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `transactionStartDatetime` | `string or null` | Fecha y hora de inicio de la transacción. | `2024-02-22 14:30:45.123` |
| `transactionEndDatetime` | `string or null` | Fecha y hora fin de la transacción. | `2024-02-22 14:30:46.123` |
| `millis` | `string or null` | Tiempo de ejecución de la operación expresado en milisegundos. | `1000` |

### 6.3. Objeto `response`

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `merchantCode` | `string or null` | Código del comercio. |
| `order` | `object` | Objeto con los detalles de la orden (número, moneda, monto, método, canal). |
| `result` | `object` | Objeto con el resultado final de la operación. |

### 6.4. Objeto `result`

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `messageFriendly` | `string` | Mensaje amigable del resultado de la operación. | `aprobado` |
| `authorizationCode` | `string` | Código de autorización. | `VA00000` |
| `uniqueId` | `string` | ID único de la transacción. | `1011173920740022` |
| `batchNumber` | `string` | Número de lote. | `string` |

## 7. Ejemplo de Respuesta (JSON)

```json
{
  "header": {
    "transactionStartDatetime": "2024-02-22 14:30:45.123",
    "transactionEndDatetime": "2024-02-22 14:30:46.123",
    "millis": "1000"
  },
  "code": "00",
  "message": "OK",
  "response": {
    "merchantCode": "4007701",
    "order": {
      "orderNumber": "R202211101518",
      "currency": "PEN",
      "amount": "1.00",
      "payMethod": "CARD",
      "channel": "ecommerce"
    },
    "result": {
      "messageFriendly": "aprobado",
      "authorizationCode": "VA00000",
      "uniqueId": "1011173920740022",
      "batchNumber": "string"
    }
  }
}
```
