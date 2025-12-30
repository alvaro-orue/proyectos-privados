# Informe de Pruebas - API Installments Izipay

## Descripción
Validación completa del API de Installments en ambiente DEV (Desarrollo)

## Ambiente de Pruebas
**Ambiente:** DEV (Desarrollo) (DEV)
**Fecha de Ejecución:** 2025-11-06
**Hora de Inicio:** 18:53:41
**Hora de Finalización:** 18:54:20
**Duración Total:** 39.24 segundos
**Merchant Code:** 4078370

---

## Endpoints Utilizados

### 1. Token Generation API
**URL:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Descripción:** Genera un token JWT para autenticar las peticiones al servicio de Installments
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER{TIMESTAMP}",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

---

### 2. Installments Search API
**URL:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Descripción:** Busca las cuotas disponibles para un BIN específico
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `Authorization`: Bearer {token}
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

---

## Casos de Prueba Ejecutados

### Tabla de Casos de Prueba

| Cód. CP | Descripción del CP | Tipo de CP | Estado | Duración |
|---------|-------------------|------------|--------|----------|
| CPI-001 | Flujo completo exitoso | FUNCIONAL | ✅ PASÓ | 6026ms |
| CPI-002 | Token reutilizable | FUNCIONAL | ✅ PASÓ | 7346ms |
| CPI-003 | TransactionId consistente | FUNCIONAL | ✅ PASÓ | 1895ms |
| CPI-004 | Casos de error | REGRESSION | ✅ PASÓ | 6063ms |
| CPI-005 | Diferentes BINs | REGRESSION | ✅ PASÓ | 7898ms |
| CPI-006 | Amount 0.00 | FUNCIONAL | ✅ PASÓ | 1908ms |
| CPI-007 | Idioma inglés | FUNCIONAL | ✅ PASÓ | 2102ms |

---

## Resultados Detallados

### CPI-001: Flujo completo exitoso
**Estado:** ✅ PASÓ
**Duración Total:** 6026ms
**Transaction IDs:** DEV20251106185341

**Pasos ejecutados:**
- ✅ Generate Token - 1164ms
- ✅ Search Installments - 4857ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 1164ms

#### Paso 2: Search Installments
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200
**Duración:** 4857ms


---

### CPI-002: Token reutilizable
**Estado:** ✅ PASÓ
**Duración Total:** 7346ms
**Transaction IDs:** DEV20251106185348

**Pasos ejecutados:**
- ✅ Generate Token - 1045ms
- ✅ First Search (Should Succeed) - 4733ms
- ✅ Second Search (Should Succeed - Reusable) - 1062ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 1045ms

#### Paso 2: First Search (Should Succeed)
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200
**Duración:** 4733ms


---

### CPI-003: TransactionId consistente
**Estado:** ✅ PASÓ
**Duración Total:** 1895ms
**Transaction IDs:** DEV20251106185356

**Pasos ejecutados:**
- ✅ Generate Token - 941ms
- ✅ Search Installments - 948ms

---

### CPI-004: Casos de error
**Estado:** ✅ PASÓ
**Duración Total:** 6063ms

**Pasos ejecutados:**
- ✅ Error 1: Token Inválido - 990ms
- ✅ Error 2: Sin Header Authorization - 1108ms
- ✅ Error 3: BIN con Formato Inválido - 949ms
- ✅ Error 4: Merchant Code Inválido - 982ms
- ✅ Error 5: Parámetro BIN Faltante - 1027ms

---

### CPI-005: Diferentes BINs
**Estado:** ✅ PASÓ
**Duración Total:** 7898ms
**Transaction IDs:** DEV20251106185406, DEV20251106185408, DEV20251106185410, DEV20251106185412

**Pasos ejecutados:**
- ✅ BIN 545545 (SCOTIABANK) - 1881ms
- ✅ BIN 400917 (SCOTIABANK VISA) - 2006ms
- ✅ BIN 377893 (BCP) - 2016ms
- ✅ BIN 553650 (BBVA MC Platinum) - 1975ms

---

### CPI-006: Amount 0.00
**Estado:** ✅ PASÓ
**Duración Total:** 1908ms
**Transaction IDs:** DEV20251106185415

**Pasos ejecutados:**
- ✅ Generate Token (amount=0.00) - 923ms
- ✅ Search Installments - 980ms

---

### CPI-007: Idioma inglés
**Estado:** ✅ PASÓ
**Duración Total:** 2102ms
**Transaction IDs:** DEV20251106185418

**Pasos ejecutados:**
- ✅ Generate Token - 1126ms
- ✅ Search Installments (language=ENG) - 971ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 1126ms

#### Paso 2: Search Installments (language=ENG)
**Endpoint:** `POST https://testapi-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200
**Duración:** 971ms


---

## Resumen Ejecutivo

### Estadísticas Generales
- **Total de Casos de Prueba:** 7
- **Casos Exitosos:** 7 (100.0%)
- **Casos Fallidos:** 0 (0.0%)
- **Ambiente:** DEV (Desarrollo)
- **Fecha:** 2025-11-06
- **Duración Total de Ejecución:** 39.24 segundos

### Cobertura de Pruebas
- ✅ **Token Generation API:** Validado
- ✅ **Installments Search API:** Validado
- ✅ **Token Reutilizable:** Validado
- ✅ **TransactionId Consistency:** Validado
- ✅ **Error Handling:** Validado
- ✅ **Múltiples BINs:** Validado
- ✅ **Amount Especial (0.00):** Validado
- ✅ **Soporte Multi-idioma (ENG):** Validado

### Estado del Ambiente DEV
✅ **COMPLETAMENTE OPERATIVO**

El ambiente está funcionando correctamente. Todas las APIs (Token y Installments) están operativas y respondiendo dentro de los tiempos esperados.

### Conclusión
✅ **VALIDACIÓN API INSTALLMENTS EN AMBIENTE DEV: EXITOSA**

Todos los casos de prueba pasaron exitosamente, confirmando que:
- Las APIs están completamente funcionales
- El token es reutilizable como se esperaba
- Los diferentes BINs configurados funcionan correctamente
- El manejo de errores es apropiado
- El sistema soporta múltiples idiomas
- Los casos especiales (amount 0.00) funcionan correctamente

**El ambiente DEV está listo para su uso.**

---

**Documento generado:** 2025-11-06 18:54:20
**Ejecutado por:** Suite de Pruebas Automatizada
**Ambiente:** DEV (testapi-pw.izipay.pe)
**Merchant Code:** 4078370
**Estado Final:** ✅ TODOS LOS TESTS PASARON
