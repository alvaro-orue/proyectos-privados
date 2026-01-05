# Documentación Técnica: Generar Token de Sesión (Izipay API)

Este documento describe la operación para generar un token de sesión, el cual es un mecanismo de autenticación requerido para invocar otras APIs de Izipay.

## 1. Endpoint

| Método | URL | Descripción |
| :--- | :--- | :--- |
| `POST` | `https://testapi-pw.izipay.pe/security/v1/Token/Generate` | Genera un token de sesión válido por 15 minutos. |

**Nota Importante:** La autenticación en la API se realiza con tokens Bearer en las solicitudes HTTP. Asegúrese de proteger sus claves API.

## 2. Parámetros de la Solicitud (Request)

La solicitud requiere un encabezado (`transactionId`) y un cuerpo JSON con los siguientes campos:

### 2.1. Encabezados (Headers)

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transactionId` | `string` | Sí | ID único por cada transacción generada por el comercio. Debe ser el mismo que se envía al generar el token. | `>= 5` caracteres, `<= 40` caracteres | `16868479028040` |

### 2.2. Cuerpo de la Solicitud (Body - JSON)

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `requestSource` | `string` | Sí | Origen de la petición. Valores permitidos: `ECOMMERCE` (para ventas, tokenización, etc.) o `REFUND` (para devoluciones). | `>= 6` caracteres, `<= 10` caracteres | `ECOMMERCE` |
| `merchantCode` | `string` | Sí | Código del comercio o submerchant, generado por Izipay. | `>= 1` caracteres, `<= 15` caracteres | `4007701` |
| `orderNumber` | `string` | Sí | Número de Pedido de la operación. | `>= 5` caracteres, `<= 15` caracteres | `R202211101518` |
| `publicKey` | `string` | Sí | Llave pública utilizada en la generación del token (**Clave API Nuevo Botón de Pagos**). Se puede obtener en la sección de Recursos/Credenciales. | `>= 16` caracteres, `<= 400` caracteres | `VErethUtraQuxas57wuMuquprADrAHAb` |
| `amount` | `string<double>` | Sí | Monto de la operación. Valor por defecto `0.00` para operaciones que no sean de pago. Enteros con 2 decimales, sin delimitador de miles. | `>= 4` caracteres, `<= 13` caracteres | `15.00` |

## 3. Respuesta Exitosa (200 Success)

Indica que la solicitud se ha procesado correctamente y se ha generado un token válido.

### 3.1. Estructura de la Respuesta

| Campo | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- |
| `code` | `string` | Sí | Código de respuesta de la autorización. |
| `message` | `string` | Sí | Mensaje de respuesta de la autorización. |
| `response` | `object` | Sí | Objeto de respuesta que contiene el token generado. |
| `response.token` | `string` | Sí | **Token generado**, válido para un solo uso. |

### 3.2. Ejemplo de Respuesta

```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudENvZGUiOiI0MDAwOTAxIiwiZmFjaWxpdGF0b3JDb2RlIjoiMCIsInRyYW5zYWN0aW9uSWQiOiJSMjAyMjExMTAxNTE4IiwiT3JkZXJOdW1iZXIiOiJSMjAyMjExMTAxNTE4IiwiQW1vdW50IjoiMC4wMCIsIlRva2VuSWQiOiJkOGVkNmM2NS05OGQ4LTQ3OWEtOGQ1MC05NWM0MmI0ZjhmNjAiLCJuYmYiOjE2NjU2MTYzMzYsImV4cCI6MTY2NTcwMjczNiwiaWF0IjoxNjY1NjE2MzM2fQ.pPe3HGxZwmxn9M90jSX_PWb5QeUhwDj_DeOJX59Q2Pk"
  }
}
```

## 4. Ejemplo de Solicitud cURL

```bash
curl --request POST \
  --url https://testapi-pw.izipay.pe/security/v1/Token/Generate \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "R202211101518",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "15.00"
}'
```
