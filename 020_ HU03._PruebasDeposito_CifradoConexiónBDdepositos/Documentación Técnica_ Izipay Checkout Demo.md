# Documentación Técnica: Izipay Checkout Demo

Este documento presenta un resumen técnico de la integración de Izipay Checkout, basado en la URL de demostración proporcionada (`https://testcheckout.izipay.pe/demo/`) y la documentación oficial de Izipay para su SDK Web Core.

La página de demostración es una implementación del **Izipay Web Core SDK (JavaScript)**, que permite a los desarrolladores integrar un formulario de pago directamente en sus aplicaciones web.

## 1. Componentes Clave de la Integración

La integración del Checkout de Izipay se centra en el uso de su SDK web para manejar la captura segura de datos de la tarjeta y la comunicación con la pasarela de pago.

### 1.1. SDK Web (JavaScript)

El SDK es el componente principal para la integración en el lado del cliente.

| Característica | Descripción |
| :--- | :--- |
| **Propósito** | Permite la integración de un formulario de pago seguro y la gestión de eventos de la transacción. |
| **Modalidad** | Principalmente en modo **Embebido** (Embedded), donde el formulario de pago se muestra dentro de un `iframe` en la página del comercio. |
| **Funcionalidad** | Tokenización de tarjetas, validaciones de SDK, y manejo de la autorización de pago. |
| **Recurso Oficial** | [Introducción | izipay developers](https://developers.izipay.pe/web-core/) |

### 1.2. Proceso de Pago (Flujo de Alto Nivel)

El flujo de pago típico con el SDK Web Core de Izipay sigue los siguientes pasos:

1.  **Creación del Objeto de Configuración**: El comercio debe generar un objeto de configuración en el *backend* con los detalles de la orden (monto, moneda, número de orden, etc.) y las credenciales de autenticación.
2.  **Inicialización del Formulario**: En el *frontend*, se utiliza el SDK de JavaScript para inicializar el formulario de pago, generalmente en un contenedor HTML.
3.  **Captura de Datos y Tokenización**: El cliente ingresa los datos de su tarjeta en el formulario seguro. El SDK se encarga de la **tokenización**, reemplazando los datos sensibles de la tarjeta por un *token* único.
4.  **Autorización de Pago**: El *token* se envía al *backend* del comercio, que a su vez lo utiliza para realizar la solicitud de autorización de pago a la API de Izipay.
5.  **Respuesta de la Transacción**: El *backend* recibe la respuesta de la transacción (éxito, rechazo, pendiente) y la procesa.

## 2. Estructura de la Respuesta de Transacción (Ejemplo)

La documentación de Izipay proporciona un ejemplo de la estructura de la respuesta de una transacción exitosa. Esta estructura es crucial para el procesamiento posterior en el *backend* del comercio.

```json
{
  "code": "00",
  "message": "Operación exitosa",
  "messageUser": "Operación exitosa",
  "messageUserEng": "Successful",
  "response": {
    "payMethod": "CARD",
    "order": [
      {
        "payMethodAuthorization": "CARD",
        "codeAuth": "831000",
        "currency": "PEN",
        "amount": "149.00",
        "installment": "00",
        "deferred": "0",
        "orderNumber": "1737067728",
        "stateMessage": "Autorizado",
        "dateTransaction": "20250116",
        "timeTransaction": "174837",
        "uniqueId": "1429383",
        "referenceNumber": "6330602"
      }
    ],
    "card": {
      "brand": "MC",
      "pan": "511842******6017",
      "save": "false"
    },
    "billing": {
      "firstName": "Lucho",
      "lastName": "Torres",
      "email": "luchotorres@gmail.com",
      "phoneNumber": "989897960",
      "street": "Av. Jorge Chávez 275",
      "city": "Lima",
      "state": "Lima",
      "country": "PE",
      "postalCode": "15000",
      "documentType": "DNI",
      "document": "12345678",
      "companyName": ""
    },
    "merchant": {
      "merchantCode": "4001061",
      "facilitatorCode": ""
    },
    "token": {
      "merchantBuyerId": "MC20250101",
      "cardToken": "",
      "alias": ""
    },
    "authentication": {
      "result": ""
    },
    "customFields": [
      // ... 10 campos personalizados
    ]
  },
  "payloadHttp": "{...}", // Payload completo de la respuesta HTTP
  "signature": "ddAlW9dl2/t5D3LwG3DpiWZPLmnowunw2XLo5MkxV9s=", // Firma de seguridad
  "transactionId": "17370677285350"
}
```

### 2.1. Campos Clave de la Respuesta

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `code` | String | Código de respuesta de la transacción. **`"00"`** indica éxito. |
| `message` | String | Mensaje de la transacción. |
| `transactionId` | String | Identificador único de la transacción. |
| `response.order[0].amount` | String | Monto de la transacción. |
| `response.order[0].currency` | String | Moneda de la transacción (ej. PEN). |
| `response.order[0].codeAuth` | String | Código de autorización del banco. |
| `response.card.pan` | String | Número de tarjeta ofuscado (ej. `511842******6017`). |
| `response.billing` | Objeto | Información de facturación del cliente. |
| `signature` | String | Firma digital para verificar la integridad de la respuesta. |

## 3. Consideraciones Técnicas Adicionales

*   **Seguridad (PCI DSS)**: Al utilizar el SDK Web Core, Izipay maneja la información sensible de la tarjeta en un entorno seguro (iframe), lo que ayuda al comercio a reducir su alcance de cumplimiento con PCI DSS.
*   **Modo de Prueba**: La URL `https://testcheckout.izipay.pe/demo/` indica un entorno de prueba (`testcheckout`), lo que significa que las transacciones realizadas allí no son reales y se utilizan para la integración y pruebas.
*   **Integración de SDKs Nativos**: Izipay también ofrece SDKs nativos para plataformas móviles (Android/iOS), lo que sugiere una solución de pago multiplataforma.
*   **Uso de Tokens**: La respuesta de la transacción incluye un objeto `token`, lo que confirma la capacidad de Izipay para almacenar de forma segura los datos de la tarjeta para pagos recurrentes o futuros (tokenización).
*   **Otros Casos de Uso**: La documentación oficial menciona otros casos de uso como **Pagar con Yape** y **Registro de Tarjeta**, lo que amplía las capacidades de la pasarela más allá del pago simple con tarjeta.

---
*Este documento fue generado a partir del análisis de la URL de demostración y la documentación pública de Izipay Developers.*
