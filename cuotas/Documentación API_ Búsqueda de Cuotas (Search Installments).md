# Documentación API: Búsqueda de Cuotas (Search Installments)

## 1. Descripción General

El servicio de **Búsqueda de Cuotas** (`Search Installments`) permite obtener información detallada sobre los planes de pago y cuotas asociados a un BIN (Número de Identificación Bancaria) específico. Esto incluye el número de cuotas disponibles, plazos de pago y otros datos relevantes. Es una herramienta esencial para ofrecer opciones de financiamiento flexibles y convenientes a los usuarios.

## 2. Endpoint

| Método | URL |
| :--- | :--- |
| `POST` | `https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search` |

> **Nota:** La URL proporcionada es para el entorno de **Sandbox**. Para el entorno de producción, la URL base puede variar.

## 3. Seguridad

Este endpoint requiere autenticación mediante **API Key**.

| Parámetro | Tipo | Descripción |
| :--- | :--- | :--- |
| `Authorization` | Header | La clave API para autenticar la solicitud. |

## 4. Parámetros de Solicitud

La solicitud utiliza una combinación de **Headers** y un **Body** en formato JSON.

### 4.1. Headers

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transactionId` | `string` | Sí | ID único por cada transacción generada por el comercio. Debe ser el mismo que se envió al generar el token. | Longitud: 5 a 40 caracteres | `16868479028040` |

### 4.2. Body (JSON)

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `bin` | `string` | Sí | Bin de la tarjeta, compuesto por los 6 primeros dígitos de la tarjeta. | Longitud: 6 caracteres | `545545` |
| `merchantCode` | `string` | Sí | Código del comercio generado por Izipay. | Longitud: 1 a 15 caracteres | `4000011` |
| `language` | `string` | No | Idioma del mensaje de respuesta. | Valores permitidos: `ESP`, `ENG` | `ESP` |

## 5. Ejemplo de Solicitud (cURL)

```bash
curl --request POST \
  --url https://sandbox-api-pw.izipay.pe/gateway/api/v1/proxy-cors/https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search \
  --header 'Accept: application/json' \
  --header 'Authorization: YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": "ESP"
}'
```

## 6. Estructura de la Respuesta Exitosa (HTTP 200)

Una respuesta exitosa indica que la solicitud se ha procesado correctamente y se ha devuelto una respuesta válida del servidor.

### 6.1. Ejemplo de Respuesta JSON

```json
{
  "code": "00",
  "message": "Aprobado",
  "header": {
    "transactionStartDatetime": "2024-01-01 12:25:47.000",
    "transactionEndDatetime": "2024-01-01 12:25:47.000",
    "millis": "1201"
  },
  "response": {
    "merchantCode": "4000011",
    "bin": "545545",
    "issuerName": "SCOTIABANK",
    "installments": [ 
      "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", 
      "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", 
      "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36" 
    ],
    "deferred": "0",
    "result": {
      "messageFriendly": "Aprobado"
    }
  }
}
```

### 6.2. Campos de Respuesta

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `code` | `string` o `null` | Código de respuesta de la autorización. **`00`** indica éxito. |
| `message` | `string` o `null` | Mensaje de respuesta de la autorización. |
| `header` | `object` | Objeto que contiene información de la transacción. |
| `header.transactionStartDatetime` | `string` o `null` | Fecha y hora de inicio de la transacción. |
| `header.transactionEndDatetime` | `string` o `null` | Fecha y hora de fin de la transacción. |
| `header.millis` | `integer` | Tiempo de ejecución de la operación expresado en milisegundos. |
| `response` | `object` | Objeto principal de la respuesta con los datos de las cuotas. |
| `response.merchantCode` | `string` o `null` | Código del comercio. |
| `response.bin` | `string` o `null` | Bin de la tarjeta. |
| `response.issuerName` | `string` o `null` | Nombre del Emisor del Bin de la tarjeta. |
| `response.installments` | `array[string]` o `null` | Lista de números de cuotas disponibles para la compra. |
| `response.deferred` | `string` o `null` | Número Diferido que afectará a la compra. |
| `response.result` | `object` | Objeto que contiene el resultado amigable de la operación. |
| `response.result.messageFriendly` | `string` | Mensaje amigable del resultado. |
