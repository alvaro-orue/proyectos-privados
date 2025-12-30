# Documentación API: Generate Token (Generación de Token de Sesión)

## 1. Descripción General

El endpoint **Generate Token** (operación `generate_token`) permite generar un token de sesión que se utiliza como mecanismo de autenticación en las otras APIs de Izipay. Este token es:

- **De un solo uso**: Cada token solo puede utilizarse una vez
- **Tiempo de vida limitado**: Aproximadamente 15 minutos de vigencia
- **Esencial para**: Inicializar operaciones de ventas, tokenización, link de pago, anulaciones, depósitos y devoluciones

## 2. Endpoint

| Método | URL Sandbox | URL Producción |
| :--- | :--- | :--- |
| `POST` | `https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate` | `https://api-pw.izipay.pe/security/v1/Token/Generate` |

## 3. Autenticación y Headers

### 3.1. Headers Requeridos

| Parámetro | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transactionId` | `string` | Sí | Identificador único para cada transacción generada por el comercio. Debe coincidir con el valor utilizado en otros tokens. | Longitud: 5 a 40 caracteres | `16868479028040` |
| `Content-Type` | `string` | Sí | Tipo de contenido de la solicitud | Valor fijo | `application/json` |
| `Accept` | `string` | Sí | Tipo de respuesta esperada | Valor fijo | `application/json` |

## 4. Parámetros de Solicitud (Body JSON)

| Campo | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `requestSource` | `string` | Sí | Origen de la petición. **`ECOMMERCE`**: Para APIs de ventas, tokenización, link de pago, anulaciones y depósitos. **`REFUND`**: Para API de devoluciones. | Valores: `ECOMMERCE`, `REFUND`. Longitud: 6-10 caracteres | `ECOMMERCE` |
| `merchantCode` | `string` | Sí | Código del comercio o sub-merchant generado por Izipay durante la afiliación | Longitud: 1-15 caracteres | `4007701` |
| `orderNumber` | `string` | Sí | Número de pedido de la operación | Longitud: 5-15 caracteres | `R202211101518` |
| `publicKey` | `string` | Sí | Llave pública asociada a la generación del token (Clave API Nuevo Botón de Pagos). Se obtiene en Recursos/Credenciales de la plataforma Izipay | Longitud: 16-400 caracteres | `VErEthUtraQUxas57wUMuquprADrAHAb...` |
| `amount` | `string<decimal>` | Sí | Monto de la operación. Para operaciones sin depósito se puede enviar `0.00`. Usa punto (.) como separador decimal, sin delimitador de miles | Longitud: 4-13 caracteres | `15.00` |

## 5. Ejemplo de Solicitud

### 5.1. cURL

```bash
curl --request POST \
  --url https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
    "requestSource": "ECOMMERCE",
    "merchantCode": "4007701",
    "orderNumber": "R202211101518",
    "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
    "amount": "15.00"
  }'
```

### 5.2. JavaScript (Fetch)

```javascript
const url = 'https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate';
const options = {
  method: 'POST',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    transactionId: '16868479028040'
  },
  body: JSON.stringify({
    requestSource: 'ECOMMERCE',
    merchantCode: '4007701',
    orderNumber: 'R202211101518',
    publicKey: 'VErEthUtraQUxas57wUMuquprADrAHAb...',
    amount: '15.00'
  })
};

try {
  const response = await fetch(url, options);
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error(error);
}
```

### 5.3. Python (Requests)

```python
import requests

url = "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate"

payload = {
    "requestSource": "ECOMMERCE",
    "merchantCode": "4007701",
    "orderNumber": "R202211101518",
    "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
    "amount": "15.00"
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "transactionId": "16868479028040"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## 6. Estructura de la Respuesta

### 6.1. Respuesta Exitosa (HTTP 200)

```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c..."
  }
}
```

### 6.2. Campos de Respuesta

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `code` | `string` | Código de respuesta de la autorización. **`00`** indica aprobación exitosa |
| `message` | `string` | Mensaje asociado al código de autorización (ejemplo: "OK") |
| `response` | `object` | Objeto que contiene el token generado |
| `response.token` | `string` | Token de sesión generado. Cadena alfanumérica larga (>255 caracteres), válida para un único uso |

### 6.3. Respuestas de Error

#### Error 400 - Bad Request
```json
{
  "code": "400",
  "message": "Parámetro requerido faltante: merchantCode",
  "response": null
}
```

#### Error 401 - Unauthorized
```json
{
  "code": "401",
  "message": "transactionId o publicKey inválidos",
  "response": null
}
```

#### Error 500 - Internal Server Error
```json
{
  "code": "500",
  "message": "Error interno al procesar la solicitud",
  "response": null
}
```

## 7. Códigos de Respuesta HTTP

| Código HTTP | Significado | Descripción |
| :--- | :--- | :--- |
| `200` | Éxito | La solicitud se ha procesado correctamente y se devuelve un token válido |
| `400` | Bad Request | Falta un parámetro requerido o los datos enviados son inválidos |
| `401` | Unauthorized | El transactionId o la publicKey no son válidos |
| `500` | Internal Server Error | Indica un problema interno al procesar la solicitud |

## 8. Uso del Token Generado

El token obtenido debe incluirse en el header `Authorization` al invocar otros endpoints de Izipay:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Ejemplo de uso en Search Installments:

```bash
curl --request POST \
  --url https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {TOKEN_GENERADO}' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
    "bin": "545545",
    "merchantCode": "4000011",
    "language": "ESP"
  }'
```

## 9. Buenas Prácticas

### 9.1. Generar transactionId único
- Genere un `transactionId` único para cada solicitud
- Facilita el seguimiento y auditoría de las llamadas
- Use el mismo `transactionId` para el token y las operaciones relacionadas

### 9.2. Proteger las credenciales
- La autenticación utiliza tokens Bearer
- Mantenga en secreto la `publicKey` y el token generado
- **NO publique estas claves en repositorios públicos**
- Use variables de entorno para almacenar credenciales

### 9.3. Definir el requestSource apropiado
- Use `ECOMMERCE` para: ventas, tokenización, link de pago, anulaciones, depósitos
- Use `REFUND` para: API de devoluciones

### 9.4. Manejo de errores
- Implemente lógica para interpretar códigos de error HTTP
- Interprete los mensajes de respuesta
- Informe de manera clara al usuario final
- Implemente reintentos con backoff exponencial

### 9.5. Rotación de tokens
- El token tiene vigencia limitada (~15 minutos)
- Genere un nuevo token cuando sea necesario
- **NO reutilice tokens caducados**
- Implemente lógica de renovación automática

### 9.6. Validación de amount
- Use punto (.) como separador decimal
- No use delimitador de miles
- Para operaciones sin depósito, envíe `0.00`
- Formato válido: `15.00`, `100.50`, `0.00`

## 10. Flujo de Integración Completo

```mermaid
sequenceDiagram
    participant Cliente
    participant API_Token
    participant API_Installments

    Cliente->>API_Token: POST /Token/Generate
    Note right of Cliente: Envía credenciales y datos
    API_Token-->>Cliente: Token de sesión
    Note left of API_Token: Token válido 15 min

    Cliente->>API_Installments: POST /Installments/Search
    Note right of Cliente: Incluye token en Authorization
    API_Installments-->>Cliente: Cuotas disponibles
```

## 11. Ejemplo de Implementación Completa

### 11.1. Flujo Completo con Manejo de Errores

```javascript
class IzipayClient {
  constructor(config) {
    this.baseUrl = config.baseUrl || 'https://sandbox-api-pw.izipay.pe';
    this.merchantCode = config.merchantCode;
    this.publicKey = config.publicKey;
  }

  generateTransactionId() {
    return `TXN${Date.now()}${Math.random().toString(36).substr(2, 9)}`;
  }

  async generateToken(orderNumber, amount) {
    const transactionId = this.generateTransactionId();
    const url = `${this.baseUrl}/security/v1/Token/Generate`;

    const payload = {
      requestSource: 'ECOMMERCE',
      merchantCode: this.merchantCode,
      orderNumber: orderNumber,
      publicKey: this.publicKey,
      amount: amount.toFixed(2)
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'transactionId': transactionId
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.code !== '00') {
        throw new Error(`Error: ${data.message}`);
      }

      return {
        token: data.response.token,
        transactionId: transactionId
      };
    } catch (error) {
      console.error('Error generating token:', error);
      throw error;
    }
  }

  async searchInstallments(bin, token, transactionId) {
    const url = `${this.baseUrl}/Installments/v1/Installments/Search`;

    const payload = {
      bin: bin,
      merchantCode: this.merchantCode,
      language: 'ESP'
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'transactionId': transactionId
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error searching installments:', error);
      throw error;
    }
  }

  async getInstallmentsForBin(bin, orderNumber, amount) {
    // 1. Generar token
    const { token, transactionId } = await this.generateToken(orderNumber, amount);

    // 2. Buscar cuotas
    const installments = await this.searchInstallments(bin, token, transactionId);

    return installments;
  }
}

// Uso
const client = new IzipayClient({
  baseUrl: 'https://sandbox-api-pw.izipay.pe',
  merchantCode: '4007701',
  publicKey: 'VErEthUtraQUxas57wUMuquprADrAHAb...'
});

// Obtener cuotas para un BIN
client.getInstallmentsForBin('545545', 'ORDER123', 100.00)
  .then(data => console.log('Cuotas disponibles:', data))
  .catch(error => console.error('Error:', error));
```

## 12. Seguridad

### 12.1. Almacenamiento Seguro de Credenciales

**Variables de Entorno (Recomendado)**
```bash
# .env
IZIPAY_MERCHANT_CODE=4007701
IZIPAY_PUBLIC_KEY=VErEthUtraQUxas57wUMuquprADrAHAb...
IZIPAY_BASE_URL=https://sandbox-api-pw.izipay.pe
```

```javascript
// Uso en la aplicación
require('dotenv').config();

const client = new IzipayClient({
  baseUrl: process.env.IZIPAY_BASE_URL,
  merchantCode: process.env.IZIPAY_MERCHANT_CODE,
  publicKey: process.env.IZIPAY_PUBLIC_KEY
});
```

### 12.2. Validaciones de Seguridad

- Validar formato de datos antes de enviar
- Implementar rate limiting en el cliente
- Usar HTTPS exclusivamente
- No registrar tokens en logs
- Implementar timeout en las solicitudes

## 13. Troubleshooting

### Problema: Token expirado
**Síntoma**: Error 401 al usar el token
**Solución**: Generar un nuevo token, los tokens tienen vigencia de ~15 minutos

### Problema: transactionId duplicado
**Síntoma**: Error de transacción ya procesada
**Solución**: Generar un nuevo transactionId único para cada solicitud

### Problema: publicKey inválida
**Síntoma**: Error 401 al generar token
**Solución**: Verificar las credenciales en el portal de Izipay

### Problema: Formato de amount incorrecto
**Síntoma**: Error 400 Bad Request
**Solución**: Usar punto como separador decimal (ejemplo: "15.00")

## 14. Referencias

- **Portal de Desarrolladores**: [https://developers.izipay.pe](https://developers.izipay.pe)
- **API Reference**: [https://developers.izipay.pe/api/#/operations/generate_token](https://developers.izipay.pe/api/#/operations/generate_token)
- **Obtención de Credenciales**: Recursos/Credenciales en la plataforma Izipay

---

**Versión del documento**: 1.0
**Última actualización**: 2025-10-28
**Preparado por**: Equipo de Documentación
