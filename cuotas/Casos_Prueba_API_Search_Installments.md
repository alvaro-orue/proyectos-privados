# Casos de Prueba Funcionales - API Search Installments

## Información General
- **API**: Search Installments (Búsqueda de Cuotas)
- **Endpoint**: `POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search`
- **Versión**: v1
- **Fecha**: 2025-10-28

---

## 1. CASOS DE PRUEBA POSITIVOS

### CP-001: Búsqueda exitosa con todos los parámetros obligatorios
**Objetivo**: Verificar que el API retorna las cuotas disponibles cuando se envían todos los parámetros obligatorios correctamente.

**Precondiciones**:
- API Key válida
- Merchant Code activo en el sistema

**Datos de entrada**:
```json
Headers:
  Authorization: {API_KEY_VALIDA}
  transactionId: "16868479028040"
  Content-Type: "application/json"
  Accept: "application/json"

Body:
{
  "bin": "545545",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Response contiene:
  - `code`: "00"
  - `message`: "Aprobado"
  - `response.installments`: Array con cuotas disponibles
  - `response.issuerName`: Nombre del banco emisor
  - `response.bin`: "545545"
  - `response.merchantCode`: "4000011"

---

### CP-002: Búsqueda exitosa con parámetro opcional language="ESP"
**Objetivo**: Verificar que el API retorna mensajes en español cuando se especifica el idioma.

**Datos de entrada**:
```json
Headers:
  Authorization: {API_KEY_VALIDA}
  transactionId: "16868479028041"

Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": "ESP"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- `message`: "Aprobado" (en español)
- `response.result.messageFriendly`: "Aprobado"

---

### CP-003: Búsqueda exitosa con parámetro opcional language="ENG"
**Objetivo**: Verificar que el API retorna mensajes en inglés cuando se especifica el idioma.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": "ENG"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Mensajes en inglés (ej: "Approved")

---

### CP-004: Validar diferentes BINs válidos
**Objetivo**: Verificar que el API procesa correctamente diferentes BINs de tarjetas válidos.

**Datos de prueba**:
| BIN | Emisor Esperado | Observación |
|-----|----------------|-------------|
| 545545 | SCOTIABANK | Mastercard |
| 411111 | Visa Test | Visa |
| 424242 | Visa Test | Visa |
| 552277 | Mastercard | Mastercard |

**Resultado esperado**:
- Status Code: `200 OK` para cada BIN
- `response.issuerName` corresponde al emisor del BIN
- `response.installments` contiene array de cuotas

---

### CP-005: TransactionId con longitud mínima (5 caracteres)
**Objetivo**: Verificar que se acepta un transactionId de longitud mínima válida.

**Datos de entrada**:
```json
Headers:
  transactionId: "12345"
```

**Resultado esperado**:
- Status Code: `200 OK`
- Transacción procesada correctamente

---

### CP-006: TransactionId con longitud máxima (40 caracteres)
**Objetivo**: Verificar que se acepta un transactionId de longitud máxima válida.

**Datos de entrada**:
```json
Headers:
  transactionId: "1234567890123456789012345678901234567890"
```

**Resultado esperado**:
- Status Code: `200 OK`
- Transacción procesada correctamente

---

### CP-007: MerchantCode con longitud mínima (1 carácter)
**Objetivo**: Verificar que se acepta un merchantCode de longitud mínima válida.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "1"
}
```

**Resultado esperado**:
- Status Code: `200 OK` o error de negocio apropiado si el código no existe

---

### CP-008: MerchantCode con longitud máxima (15 caracteres)
**Objetivo**: Verificar que se acepta un merchantCode de longitud máxima válida.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "123456789012345"
}
```

**Resultado esperado**:
- Status Code: `200 OK` o error de negocio apropiado si el código no existe

---

## 2. CASOS DE PRUEBA NEGATIVOS

### CP-N001: Solicitud sin header Authorization
**Objetivo**: Verificar que el API rechaza solicitudes sin autenticación.

**Datos de entrada**:
```json
Headers:
  transactionId: "16868479028040"
  (Sin Authorization header)
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje indicando autenticación requerida

---

### CP-N002: Solicitud con API Key inválida
**Objetivo**: Verificar que el API rechaza solicitudes con credenciales incorrectas.

**Datos de entrada**:
```json
Headers:
  Authorization: "INVALID_API_KEY_12345"
```

**Resultado esperado**:
- Status Code: `401 Unauthorized` o `403 Forbidden`

---

### CP-N003: Solicitud sin header transactionId
**Objetivo**: Verificar validación del header obligatorio transactionId.

**Datos de entrada**:
```json
Headers:
  Authorization: {API_KEY_VALIDA}
  (Sin transactionId)
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando que transactionId es requerido

---

### CP-N004: TransactionId con longitud menor a 5 caracteres
**Objetivo**: Verificar validación de longitud mínima de transactionId.

**Datos de entrada**:
```json
Headers:
  transactionId: "1234"
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación indicando longitud mínima

---

### CP-N005: TransactionId con longitud mayor a 40 caracteres
**Objetivo**: Verificar validación de longitud máxima de transactionId.

**Datos de entrada**:
```json
Headers:
  transactionId: "12345678901234567890123456789012345678901"
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación indicando longitud máxima

---

### CP-N006: Solicitud sin parámetro bin en el body
**Objetivo**: Verificar validación del parámetro obligatorio bin.

**Datos de entrada**:
```json
Body:
{
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando que bin es requerido

---

### CP-N007: BIN con longitud menor a 6 caracteres
**Objetivo**: Verificar validación de longitud del BIN.

**Datos de entrada**:
```json
Body:
{
  "bin": "54554",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación de longitud de bin

---

### CP-N008: BIN con longitud mayor a 6 caracteres
**Objetivo**: Verificar validación de longitud del BIN.

**Datos de entrada**:
```json
Body:
{
  "bin": "5455456",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación de longitud de bin

---

### CP-N009: BIN con caracteres no numéricos
**Objetivo**: Verificar validación del formato del BIN.

**Datos de entrada**:
```json
Body:
{
  "bin": "54ABC5",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando formato inválido

---

### CP-N010: Solicitud sin parámetro merchantCode en el body
**Objetivo**: Verificar validación del parámetro obligatorio merchantCode.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando que merchantCode es requerido

---

### CP-N011: MerchantCode vacío
**Objetivo**: Verificar que no se acepta merchantCode vacío.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": ""
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación

---

### CP-N012: MerchantCode con longitud mayor a 15 caracteres
**Objetivo**: Verificar validación de longitud máxima de merchantCode.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "1234567890123456"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje de validación de longitud

---

### CP-N013: Language con valor no permitido
**Objetivo**: Verificar validación de valores permitidos para language.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": "FRA"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando valores permitidos: ESP, ENG

---

### CP-N014: Body con formato JSON inválido
**Objetivo**: Verificar manejo de JSON malformado.

**Datos de entrada**:
```
Body (texto plano):
{
  "bin": "545545",
  "merchantCode": "4000011"
  (falta coma o hay error de sintaxis)
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Mensaje indicando error de formato JSON

---

### CP-N015: Solicitud con Content-Type incorrecto
**Objetivo**: Verificar validación del Content-Type header.

**Datos de entrada**:
```json
Headers:
  Content-Type: "text/plain"
```

**Resultado esperado**:
- Status Code: `415 Unsupported Media Type`

---

### CP-N016: BIN no registrado en el sistema
**Objetivo**: Verificar comportamiento con BIN válido pero no registrado.

**Datos de entrada**:
```json
Body:
{
  "bin": "999999",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `200 OK` o `404 Not Found`
- Si 200, verificar `code` diferente de "00" con mensaje apropiado

---

### CP-N017: MerchantCode no registrado
**Objetivo**: Verificar comportamiento con merchantCode válido pero no registrado.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "9999999"
}
```

**Resultado esperado**:
- Status Code: `200 OK` con código de error
- Mensaje indicando comercio no encontrado

---

### CP-N018: MerchantCode inactivo o suspendido
**Objetivo**: Verificar comportamiento con merchantCode inactivo.

**Precondiciones**: Merchant code debe estar en estado inactivo

**Resultado esperado**:
- Status Code: `403 Forbidden` o `200 OK` con código de error
- Mensaje indicando estado del comercio

---

## 3. CASOS DE PRUEBA DE SEGURIDAD

### CP-S001: SQL Injection en campo bin
**Objetivo**: Verificar protección contra inyección SQL.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545' OR '1'='1",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Sin acceso no autorizado a datos

---

### CP-S002: XSS en campo merchantCode
**Objetivo**: Verificar protección contra scripts maliciosos.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "<script>alert('XSS')</script>"
}
```

**Resultado esperado**:
- Status Code: `400 Bad Request`
- Caracteres especiales sanitizados o rechazados

---

### CP-S003: Solicitudes concurrentes con mismo transactionId
**Objetivo**: Verificar manejo de transacciones duplicadas.

**Datos de entrada**:
- Enviar 2+ solicitudes simultáneas con mismo transactionId

**Resultado esperado**:
- Manejo apropiado de idempotencia
- Sin duplicación de transacciones

---

### CP-S004: API Key de otro comercio
**Objetivo**: Verificar aislamiento entre comercios.

**Datos de entrada**:
```json
Headers:
  Authorization: {API_KEY_COMERCIO_A}

Body:
{
  "bin": "545545",
  "merchantCode": "COMERCIO_B"
}
```

**Resultado esperado**:
- Status Code: `403 Forbidden`
- Sin acceso a datos de otro comercio

---

## 4. CASOS DE PRUEBA DE RENDIMIENTO

### CP-P001: Tiempo de respuesta bajo carga normal
**Objetivo**: Verificar que el tiempo de respuesta es aceptable.

**Parámetros**:
- Usuarios concurrentes: 10
- Duración: 5 minutos

**Resultado esperado**:
- Tiempo promedio de respuesta < 2 segundos
- 95% de respuestas < 3 segundos
- `header.millis` dentro de rangos aceptables

---

### CP-P002: Límite de rate limiting
**Objetivo**: Verificar límites de tasa de solicitudes.

**Datos de entrada**:
- Enviar múltiples solicitudes rápidamente desde mismo cliente

**Resultado esperado**:
- Status Code: `429 Too Many Requests` al exceder límite
- Headers con información de rate limiting (Retry-After, etc.)

---

## 5. CASOS DE PRUEBA DE BORDE

### CP-B001: BIN con ceros a la izquierda
**Objetivo**: Verificar manejo de BINs con ceros iniciales.

**Datos de entrada**:
```json
Body:
{
  "bin": "000123",
  "merchantCode": "4000011"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- BIN procesado correctamente manteniendo formato

---

### CP-B002: MerchantCode con caracteres alfanuméricos
**Objetivo**: Verificar si merchantCode acepta letras.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "ABC123"
}
```

**Resultado esperado**:
- Según especificación del sistema (validar documentación)

---

### CP-B003: TransactionId duplicado en diferente sesión
**Objetivo**: Verificar unicidad de transactionId.

**Datos de entrada**:
- Enviar solicitud con transactionId ya usado previamente

**Resultado esperado**:
- Comportamiento según política de idempotencia del sistema

---

### CP-B004: Parámetros con espacios en blanco
**Objetivo**: Verificar sanitización de entrada.

**Datos de entrada**:
```json
Body:
{
  "bin": " 545545 ",
  "merchantCode": " 4000011 "
}
```

**Resultado esperado**:
- Sistema debe hacer trim de espacios o rechazar entrada

---

### CP-B005: Body con parámetros adicionales no documentados
**Objetivo**: Verificar que parámetros extra no causan errores.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "extraParam": "valor no esperado"
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Parámetros extra ignorados

---

### CP-B006: Language con minúsculas
**Objetivo**: Verificar sensibilidad a mayúsculas/minúsculas.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": "esp"
}
```

**Resultado esperado**:
- Sistema acepta o normaliza, o rechaza con error claro

---

### CP-B007: Valores null en campos opcionales
**Objetivo**: Verificar manejo de valores null.

**Datos de entrada**:
```json
Body:
{
  "bin": "545545",
  "merchantCode": "4000011",
  "language": null
}
```

**Resultado esperado**:
- Status Code: `200 OK`
- Campo tratado como no enviado

---

## 6. CASOS DE PRUEBA DE INTEGRACIÓN

### CP-I001: Verificar coherencia de datos con otros endpoints
**Objetivo**: Validar que las cuotas retornadas son consistentes con el sistema de pagos.

**Pasos**:
1. Obtener cuotas con Search Installments
2. Intentar crear transacción con cuota obtenida
3. Validar que la cuota es aceptada

**Resultado esperado**:
- Cuotas retornadas son válidas para transacciones

---

### CP-I002: Validar header.transactionStartDatetime y transactionEndDatetime
**Objetivo**: Verificar que las fechas sean coherentes.

**Resultado esperado**:
- `transactionEndDatetime` >= `transactionStartDatetime`
- Diferencia de tiempo razonable
- `header.millis` aproximadamente igual a diferencia entre fechas

---

## 7. MATRIZ DE TRAZABILIDAD

| ID Caso | Tipo | Prioridad | Requerimiento | Automatizable |
|---------|------|-----------|---------------|---------------|
| CP-001 | Positivo | Alta | REQ-001 | Sí |
| CP-002 | Positivo | Media | REQ-002 | Sí |
| CP-003 | Positivo | Media | REQ-002 | Sí |
| CP-004 | Positivo | Alta | REQ-003 | Sí |
| CP-005 | Positivo | Media | REQ-004 | Sí |
| CP-006 | Positivo | Media | REQ-004 | Sí |
| CP-N001 | Negativo | Alta | REQ-SEC-001 | Sí |
| CP-N002 | Negativo | Alta | REQ-SEC-002 | Sí |
| CP-N003 | Negativo | Alta | REQ-VAL-001 | Sí |
| CP-N004 | Negativo | Media | REQ-VAL-002 | Sí |
| CP-N005 | Negativo | Media | REQ-VAL-002 | Sí |
| CP-S001 | Seguridad | Crítica | REQ-SEC-003 | Sí |
| CP-P001 | Rendimiento | Alta | REQ-PERF-001 | Sí |

---

## 8. DATOS DE PRUEBA RECOMENDADOS

### BINs de Prueba (Sandbox)
```
545545 - SCOTIABANK - Mastercard - Cuotas múltiples disponibles
411111 - VISA TEST - Visa - Cuotas estándar
424242 - VISA TEST - Visa - Sin cuotas
552277 - MASTERCARD TEST - Mastercard - Cuotas premium
```

### Merchant Codes de Prueba
```
4000011 - Comercio activo estándar
4000022 - Comercio con configuración especial
4000033 - Comercio inactivo (para pruebas negativas)
```

---

## 9. CRITERIOS DE ACEPTACIÓN

### Criterios Funcionales
- ✓ Todos los casos positivos (CP-001 a CP-008) deben pasar
- ✓ Al menos 90% de casos negativos deben comportarse según esperado
- ✓ Validaciones de entrada funcionan correctamente

### Criterios de Seguridad
- ✓ No se permite acceso sin autenticación
- ✓ No hay inyección SQL/XSS posible
- ✓ Aislamiento entre comercios funciona

### Criterios de Rendimiento
- ✓ Tiempo de respuesta < 2 segundos (p95)
- ✓ Disponibilidad > 99.5%
- ✓ Sin memory leaks en pruebas de carga

---

## 10. AMBIENTE DE PRUEBAS

### Configuración Requerida
- **URL Base**: `https://sandbox-api-pw.izipay.pe`
- **API Keys**: Solicitar credenciales de sandbox
- **Headers Requeridos**: Content-Type, Authorization, transactionId
- **Herramientas**: Postman, cURL, JMeter (para performance)

### Variables de Entorno
```
BASE_URL=https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search
API_KEY={{YOUR_SANDBOX_API_KEY}}
MERCHANT_CODE=4000011
```

---

## 11. NOTAS ADICIONALES

1. **Idempotencia**: Validar si el API es idempotente con mismo transactionId
2. **Logs**: Verificar que todas las transacciones se registren correctamente
3. **Monitoreo**: Configurar alertas para errores 5xx
4. **Documentación**: Actualizar con cualquier discrepancia encontrada
5. **Versionado**: Considerar compatibilidad con versiones futuras del API

---

## 12. REGISTRO DE EJECUCIÓN

| Fecha | Versión API | Ejecutor | Casos Pasados | Casos Fallados | Observaciones |
|-------|-------------|----------|---------------|----------------|---------------|
| | | | | | |

---

**Preparado por**: Claude
**Última actualización**: 2025-10-28
**Versión del documento**: 1.0
