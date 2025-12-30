# Casos de Prueba Funcionales - API Generate Token

## Información General
- **API**: Generate Token (Generación de Token de Sesión)
- **Endpoint**: `POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate`
- **Versión**: v1
- **Fecha**: 2025-10-28

---

## 1. CASOS DE PRUEBA POSITIVOS

### CPT-001: Generación exitosa de token para ECOMMERCE
**Objetivo**: Verificar que el API genera correctamente un token de sesión para operaciones de ecommerce.

**Precondiciones**:
- Merchant Code válido y activo
- Public Key válida

**Datos de entrada**:
```json
Headers:
  transactionId: "TXN1698447028040"
  Content-Type: "application/json"
  Accept: "application/json"

Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "ORDER12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Response contiene:
  - `code`: "00"
  - `message`: "OK"
  - `response.token`: String alfanumérico (>255 caracteres)
- Token válido y utilizable en otras APIs

---

### CPT-002: Generación exitosa de token para REFUND
**Objetivo**: Verificar que el API genera correctamente un token para operaciones de devolución.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "REFUND",
  "merchantCode": "4007701",
  "orderNumber": "REFUND12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "50.00"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- `code`: "00"
- Token generado correctamente

---

### CPT-003: Generación de token con amount 0.00
**Objetivo**: Verificar que se puede generar token para operaciones sin depósito.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "ORDER12346",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "0.00"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Token generado correctamente

---

### CPT-004: TransactionId con longitud mínima (5 caracteres)
**Objetivo**: Verificar que se acepta transactionId de longitud mínima válida.

**Datos de entrada**:
```json
Headers:
  transactionId: "12345"
```

**Resultado esperado**:
- Status Code: `200 OK`
- Token generado correctamente

---

### CPT-005: TransactionId con longitud máxima (40 caracteres)
**Objetivo**: Verificar que se acepta transactionId de longitud máxima válida.

**Datos de entrada**:
```json
Headers:
  transactionId: "1234567890123456789012345678901234567890"
```

**Resultado esperado**:
- Status Code: `200 OK`
- Token generado correctamente

---

### CPT-006: MerchantCode con longitud mínima (1 carácter)
**Objetivo**: Verificar que se acepta merchantCode de longitud mínima.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "1",
  "requestSource": "ECOMMERCE",
  "orderNumber": "ORDER12347",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `200 OK` o error de negocio si el código no existe

---

### CPT-007: MerchantCode con longitud máxima (15 caracteres)
**Objetivo**: Verificar que se acepta merchantCode de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "123456789012345",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK` o error de negocio si el código no existe

---

### CPT-008: OrderNumber con longitud mínima (5 caracteres)
**Objetivo**: Verificar validación de longitud mínima de orderNumber.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "ORD12",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK`

---

### CPT-009: OrderNumber con longitud máxima (15 caracteres)
**Objetivo**: Verificar validación de longitud máxima de orderNumber.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "ORDER1234567890",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK`

---

### CPT-010: Amount con decimales
**Objetivo**: Verificar que se acepta correctamente valores con decimales.

**Datos de prueba**:
| Amount | Descripción |
|--------|-------------|
| "0.01" | Valor mínimo con decimales |
| "10.50" | Valor con 50 centavos |
| "999.99" | Valor alto con decimales |
| "1000.00" | Valor redondo con decimales explícitos |

**Resultado esperado**:
- Status Code: `200 OK` para todos los casos

---

### CPT-011: PublicKey con longitud mínima (16 caracteres)
**Objetivo**: Verificar longitud mínima de publicKey.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "1234567890123456",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK` o `401` si la clave no es válida

---

### CPT-012: PublicKey con longitud máxima (400 caracteres)
**Objetivo**: Verificar longitud máxima de publicKey.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "{STRING_DE_400_CARACTERES}",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK` o `401` si la clave no es válida

---

## 2. CASOS DE PRUEBA NEGATIVOS

### CPT-N001: Solicitud sin header transactionId
**Objetivo**: Verificar que transactionId es obligatorio.

**Datos de entrada**:
```json
Headers:
  Content-Type: "application/json"
  Accept: "application/json"
  (Sin transactionId)
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando que transactionId es requerido

---

### CPT-N002: TransactionId con longitud menor a 5 caracteres
**Objetivo**: Verificar validación de longitud mínima.

**Datos de entrada**:
```json
Headers:
  transactionId: "1234"
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación de longitud

---

### CPT-N003: TransactionId con longitud mayor a 40 caracteres
**Objetivo**: Verificar validación de longitud máxima.

**Datos de entrada**:
```json
Headers:
  transactionId: "12345678901234567890123456789012345678901"
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N004: Solicitud sin campo requestSource
**Objetivo**: Verificar que requestSource es obligatorio.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "4007701",
  "orderNumber": "ORDER12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando que requestSource es requerido

---

### CPT-N005: RequestSource con valor inválido
**Objetivo**: Verificar validación de valores permitidos.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "INVALID_SOURCE",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando valores válidos: ECOMMERCE, REFUND

---

### CPT-N006: RequestSource con longitud menor a 6 caracteres
**Objetivo**: Verificar restricción de longitud mínima.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMM",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N007: RequestSource con longitud mayor a 10 caracteres
**Objetivo**: Verificar restricción de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE123",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N008: Solicitud sin campo merchantCode
**Objetivo**: Verificar que merchantCode es obligatorio.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "orderNumber": "ORDER12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N009: MerchantCode vacío
**Objetivo**: Verificar que no se acepta merchantCode vacío.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N010: MerchantCode con longitud mayor a 15 caracteres
**Objetivo**: Verificar restricción de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "1234567890123456",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N011: MerchantCode no registrado o inválido
**Objetivo**: Verificar validación de merchant existente.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "9999999",
  ...
}
```

**Resultado esperado**:
- Status Code: `401 Unauthorized` o `400 Bad Request`
- Mensaje indicando merchant no válido

---

### CPT-N012: Solicitud sin campo orderNumber
**Objetivo**: Verificar que orderNumber es obligatorio.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N013: OrderNumber con longitud menor a 5 caracteres
**Objetivo**: Verificar restricción de longitud mínima.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "ORD1",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N014: OrderNumber con longitud mayor a 15 caracteres
**Objetivo**: Verificar restricción de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "ORDER12345678901",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N015: Solicitud sin campo publicKey
**Objetivo**: Verificar que publicKey es obligatoria.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "ORDER12345",
  "amount": "100.00"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N016: PublicKey inválida
**Objetivo**: Verificar validación de publicKey.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "INVALID_PUBLIC_KEY_123",
  ...
}
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje indicando publicKey inválida

---

### CPT-N017: PublicKey con longitud menor a 16 caracteres
**Objetivo**: Verificar restricción de longitud mínima.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "SHORT_KEY",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N018: PublicKey con longitud mayor a 400 caracteres
**Objetivo**: Verificar restricción de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "{STRING_DE_MAS_DE_400_CARACTERES}",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N019: Solicitud sin campo amount
**Objetivo**: Verificar que amount es obligatorio.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "ORDER12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb..."
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N020: Amount con formato inválido (sin decimales)
**Objetivo**: Verificar validación de formato decimal.

**Datos de entrada**:
```json
Body:
{
  "amount": "100",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request` o el sistema acepta y normaliza

---

### CPT-N021: Amount con coma como separador decimal
**Objetivo**: Verificar que solo se acepta punto como separador.

**Datos de entrada**:
```json
Body:
{
  "amount": "100,50",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando formato inválido

---

### CPT-N022: Amount con delimitador de miles
**Objetivo**: Verificar que no se permiten delimitadores de miles.

**Datos de entrada**:
```json
Body:
{
  "amount": "1,000.00",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N023: Amount negativo
**Objetivo**: Verificar que no se aceptan montos negativos.

**Datos de entrada**:
```json
Body:
{
  "amount": "-100.00",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N024: Amount con más de 2 decimales
**Objetivo**: Verificar precisión de decimales.

**Datos de entrada**:
```json
Body:
{
  "amount": "100.999",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request` o redondeo a 2 decimales

---

### CPT-N025: Amount con longitud menor a 4 caracteres
**Objetivo**: Verificar restricción de longitud mínima.

**Datos de entrada**:
```json
Body:
{
  "amount": "1.0",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request` o el sistema acepta y normaliza

---

### CPT-N026: Amount con longitud mayor a 13 caracteres
**Objetivo**: Verificar restricción de longitud máxima.

**Datos de entrada**:
```json
Body:
{
  "amount": "99999999999.99",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`

---

### CPT-N027: Body con formato JSON inválido
**Objetivo**: Verificar manejo de JSON malformado.

**Datos de entrada**:
```
Body (texto plano):
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701"
  (falta coma o cierre de llave)
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de error de parseo JSON

---

### CPT-N028: Content-Type incorrecto
**Objetivo**: Verificar validación de Content-Type.

**Datos de entrada**:
```json
Headers:
  Content-Type: "text/plain"
```

**Resultado esperado**:
- Status Code: `415 Unsupported Media Type`

---

### CPT-N029: Solicitud completamente vacía
**Objetivo**: Verificar manejo de body vacío.

**Datos de entrada**:
```json
Body: {}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensajes indicando todos los campos requeridos faltantes

---

## 3. CASOS DE PRUEBA DE SEGURIDAD

### CPT-S001: SQL Injection en requestSource
**Objetivo**: Verificar protección contra inyección SQL.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE' OR '1'='1",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Sin acceso no autorizado

---

### CPT-S002: SQL Injection en merchantCode
**Objetivo**: Verificar protección contra inyección SQL.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "4007701'; DROP TABLE tokens;--",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Sin ejecución de comandos SQL

---

### CPT-S003: XSS en orderNumber
**Objetivo**: Verificar protección contra scripts maliciosos.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "<script>alert('XSS')</script>",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Caracteres especiales sanitizados o rechazados

---

### CPT-S004: Inyección de comandos en publicKey
**Objetivo**: Verificar protección contra command injection.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "key; rm -rf /",
  ...
}
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Sin ejecución de comandos

---

### CPT-S005: PublicKey de otro comercio
**Objetivo**: Verificar aislamiento entre comercios.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "4007701",
  "publicKey": "{PUBLIC_KEY_DE_OTRO_MERCHANT}",
  ...
}
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje de autenticación fallida

---

### CPT-S006: Token reutilizado
**Objetivo**: Verificar que tokens son de un solo uso.

**Pasos**:
1. Generar token con transactionId "TXN001"
2. Usar token en Search Installments
3. Intentar usar el mismo token nuevamente

**Resultado esperado**:
- Segunda llamada rechazada con `401 Unauthorized`
- Mensaje indicando token inválido o expirado

---

### CPT-S007: Solicitudes concurrentes con mismo transactionId
**Objetivo**: Verificar manejo de idempotencia.

**Pasos**:
- Enviar 2+ solicitudes simultáneas con mismo transactionId

**Resultado esperado**:
- Una de las solicitudes se procesa
- Otras reciben error de duplicación o se procesan idempotentemente

---

### CPT-S008: Overflow en amount
**Objetivo**: Verificar protección contra overflow numérico.

**Datos de entrada**:
```json
Body:
{
  "amount": "999999999999999999999999.99",
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Validación de rango de valores

---

## 4. CASOS DE PRUEBA DE TIEMPO Y EXPIRACIÓN

### CPT-T001: Validar vigencia del token (15 minutos)
**Objetivo**: Verificar que el token expira después de ~15 minutos.

**Pasos**:
1. Generar token
2. Esperar 16 minutos
3. Intentar usar el token en Search Installments

**Resultado esperado**:
- Token rechazado con `401 Unauthorized`
- Mensaje indicando token expirado

---

### CPT-T002: Usar token dentro del período de vigencia
**Objetivo**: Verificar que el token es válido dentro de los 15 minutos.

**Pasos**:
1. Generar token
2. Esperar 5 minutos
3. Usar el token en Search Installments

**Resultado esperado**:
- Token aceptado
- Operación exitosa

---

### CPT-T003: Tiempo de respuesta para generación de token
**Objetivo**: Verificar que la generación es rápida.

**Resultado esperado**:
- Tiempo de respuesta < 2 segundos
- 95% de solicitudes < 3 segundos

---

## 5. CASOS DE PRUEBA DE BORDE

### CPT-B001: TransactionId con caracteres especiales
**Objetivo**: Verificar qué caracteres se permiten.

**Datos de entrada**:
```json
Headers:
  transactionId: "TXN-2024_10_28@12:30"
```

**Resultado esperado**:
- Sistema acepta o rechaza según política
- Comportamiento consistente

---

### CPT-B002: OrderNumber con caracteres alfanuméricos
**Objetivo**: Verificar tipos de caracteres aceptados.

**Datos de entrada**:
```json
Body:
{
  "orderNumber": "ORD-2024-ABC",
  ...
}
```

**Resultado esperado**:
- Sistema acepta o rechaza según política

---

### CPT-B003: Amount con valor muy pequeño
**Objetivo**: Verificar valores mínimos.

**Datos de entrada**:
```json
Body:
{
  "amount": "0.01",
  ...
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Token generado correctamente

---

### CPT-B004: Campos con espacios en blanco
**Objetivo**: Verificar sanitización de entrada.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": " 4007701 ",
  "orderNumber": " ORDER123 ",
  ...
}
```

**Resultado esperado**:
- Sistema hace trim de espacios o rechaza

---

### CPT-B005: Body con campos adicionales no documentados
**Objetivo**: Verificar que campos extra no causan errores.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4007701",
  "orderNumber": "ORDER12345",
  "publicKey": "VErEthUtraQUxas57wUMuquprADrAHAb...",
  "amount": "100.00",
  "extraField": "valor_no_esperado",
  "customData": {"key": "value"}
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Campos extra ignorados

---

### CPT-B006: RequestSource en minúsculas
**Objetivo**: Verificar sensibilidad a mayúsculas/minúsculas.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ecommerce",
  ...
}
```

**Resultado esperado**:
- Sistema acepta y normaliza, o rechaza con error claro

---

### CPT-B007: Valores null en campos obligatorios
**Objetivo**: Verificar manejo de valores null.

**Datos de entrada**:
```json
Body:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": null,
  ...
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando campo requerido

---

### CPT-B008: PublicKey con espacios internos
**Objetivo**: Verificar formato de publicKey.

**Datos de entrada**:
```json
Body:
{
  "publicKey": "VErEthUtra QUxas57wUMuqupr ADrAHAb",
  ...
}
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- PublicKey rechazada

---

## 6. CASOS DE PRUEBA DE RENDIMIENTO

### CPT-P001: Carga normal - 10 usuarios concurrentes
**Objetivo**: Verificar rendimiento bajo carga normal.

**Parámetros**:
- Usuarios concurrentes: 10
- Duración: 5 minutos
- Transacciones por segundo: 5-10

**Resultado esperado**:
- Tiempo promedio respuesta < 2 seg
- 0% de errores
- CPU y memoria en rangos normales

---

### CPT-P002: Carga alta - 100 usuarios concurrentes
**Objetivo**: Verificar estabilidad bajo carga alta.

**Parámetros**:
- Usuarios concurrentes: 100
- Duración: 10 minutos

**Resultado esperado**:
- Tiempo promedio respuesta < 3 seg
- Tasa de error < 1%
- Sistema mantiene estabilidad

---

### CPT-P003: Límite de rate limiting
**Objetivo**: Verificar límites de tasa.

**Pasos**:
- Enviar múltiples solicitudes rápidamente desde mismo cliente

**Resultado esperado**:
- Status Code: `429 Too Many Requests` al exceder límite
- Headers con información de retry

---

## 7. MATRIZ DE TRAZABILIDAD

| ID Caso | Tipo | Prioridad | Automatizable | Dependencias |
|---------|------|-----------|---------------|--------------|
| CPT-001 | Positivo | Crítica | Sí | - |
| CPT-002 | Positivo | Alta | Sí | - |
| CPT-003 | Positivo | Media | Sí | - |
| CPT-N001 | Negativo | Alta | Sí | - |
| CPT-N004 | Negativo | Alta | Sí | - |
| CPT-N008 | Negativo | Alta | Sí | - |
| CPT-N015 | Negativo | Crítica | Sí | - |
| CPT-S006 | Seguridad | Crítica | Sí | Search Installments API |
| CPT-T001 | Temporal | Alta | Parcial | - |
| CPT-P001 | Rendimiento | Media | Sí | - |

---

## 8. DATOS DE PRUEBA

### Credenciales de Sandbox
```
Merchant Code: 4007701
Public Key: {SOLICITAR_EN_PORTAL_IZIPAY}
Base URL: https://sandbox-api-pw.izipay.pe
```

### TransactionIds de Ejemplo
```
TXN1698447028040
TXN1698447028041
TXN1698447028042
ORDER-2024-10-28-001
```

### OrderNumbers de Ejemplo
```
ORDER12345
ORD202410280001
R202211101518
REFUND12345
```

---

## 9. CRITERIOS DE ACEPTACIÓN

- ✓ Todos los casos positivos críticos pasan (CPT-001, CPT-002)
- ✓ Validaciones de campos obligatorios funcionan (CPT-N001, N004, N008, N015, N019)
- ✓ Tokens generados son válidos y utilizables
- ✓ Tokens expiran después de ~15 minutos
- ✓ Protección contra inyecciones SQL/XSS
- ✓ Tiempo de respuesta < 2 segundos (p95)
- ✓ Sin fugas de tokens o credenciales en logs

---

## 10. AMBIENTE DE PRUEBAS

### Variables de Entorno
```bash
TOKEN_API_URL=https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate
MERCHANT_CODE=4007701
PUBLIC_KEY={{YOUR_PUBLIC_KEY}}
INSTALLMENTS_API_URL=https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search
```

### Herramientas Recomendadas
- **API Testing**: Postman, Insomnia
- **Automatización**: Newman, Jest, Pytest
- **Performance**: JMeter, Artillery
- **Monitoreo**: Tiempo de respuesta, logs de errores

---

**Preparado por**: Claude
**Última actualización**: 2025-10-28
**Versión del documento**: 1.0
