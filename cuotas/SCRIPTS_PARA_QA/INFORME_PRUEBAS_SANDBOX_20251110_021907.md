# Informe de Pruebas - API Installments Izipay

## Descripción
Validación completa del API de Installments en ambiente SANDBOX

## Ambiente de Pruebas
**Ambiente:** SANDBOX (SANDBOX)
**Fecha de Ejecución:** 2025-11-10
**Hora de Inicio:** 02:16:49
**Hora de Finalización:** 02:19:07
**Duración Total:** 137.32 segundos
**Merchant Code:** 4001834

---

## Endpoints Utilizados

### 1. Token Generation API
**URL:** `POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate`
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
  "merchantCode": "4001834",
  "orderNumber": "ORDER{TIMESTAMP}",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

---

### 2. Installments Search API
**URL:** `POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search`
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
  "merchantCode": "4001834",
  "language": "ESP"
}
```

---

## Casos de Prueba Ejecutados

### Tabla de Casos de Prueba

| Cód. CP | Descripción del CP | Tipo de CP | Estado | Duración |
|---------|-------------------|------------|--------|----------|
| CPI-001 | Flujo completo exitoso | FUNCIONAL | ✅ PASÓ | 6243ms |
| CPI-002 | Token reutilizable | FUNCIONAL | ❌ FALLÓ | 37477ms |
| CPI-003 | TransactionId consistente | FUNCIONAL | ❌ FALLÓ | 6108ms |
| CPI-004 | Casos de error | REGRESSION | ❌ FALLÓ | 62855ms |
| CPI-005 | Diferentes BINs | REGRESSION | ✅ PASÓ | 6390ms |
| CPI-006 | Amount 0.00 | FUNCIONAL | ❌ FALLÓ | 6156ms |
| CPI-007 | Idioma inglés | FUNCIONAL | ✅ PASÓ | 6090ms |

---

## Resultados Detallados

### CPI-001: Flujo completo exitoso
**Estado:** ✅ PASÓ
**Duración Total:** 6243ms
**Transaction IDs:** SBX20251110021649

**Pasos ejecutados:**
- ✅ Generate Token - 2170ms
- ✅ Search Installments - 2068ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 2170ms

#### Paso 2: Search Installments
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200
**Duración:** 2068ms


---

### CPI-002: Token reutilizable
**Estado:** ❌ FALLÓ
**Duración Total:** 37477ms
**Transaction IDs:** SBX20251110021656
**Error:** Token no pudo ser reutilizado

**Pasos ejecutados:**
- ✅ Generate Token - 2024ms
- ❌ First Search (Should Succeed) - 30905ms
- ❌ Second Search (Should Succeed - Reusable) - 2043ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 2024ms

#### Paso 2: First Search (Should Succeed)
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** N/A
**Duración:** 30905ms


---

### CPI-003: TransactionId consistente
**Estado:** ❌ FALLÓ
**Duración Total:** 6108ms
**Transaction IDs:** SBX20251110021735
**Error:** Installments search failed: El token no debe ser nulo o vacío

**Pasos ejecutados:**
- ✅ Generate Token - 1985ms
- ❌ Search Installments - 2119ms

---

### CPI-004: Casos de error
**Estado:** ❌ FALLÓ
**Duración Total:** 62855ms
**Error:** Solo 4 de 5 escenarios pasaron

**Pasos ejecutados:**
- ✅ Error 1: Token Inválido - 2062ms
- ✅ Error 2: Sin Header Authorization - 23860ms
- ❌ Error 3: BIN con Formato Inválido - 0ms
- ✅ Error 4: Merchant Code Inválido - 1812ms
- ✅ Error 5: Parámetro BIN Faltante - 1970ms

---

### CPI-005: Diferentes BINs
**Estado:** ✅ PASÓ
**Duración Total:** 6390ms
**Transaction IDs:** SBX20251110021846

**Pasos ejecutados:**
- ✅ BIN 511578 (BBVA MC Platinum) - 4386ms

---

### CPI-006: Amount 0.00
**Estado:** ❌ FALLÓ
**Duración Total:** 6156ms
**Transaction IDs:** SBX20251110021853
**Error:** Installments search failed: El token no debe ser nulo o vacío

**Pasos ejecutados:**
- ✅ Generate Token (amount=0.00) - 2072ms
- ❌ Search Installments - 2081ms

---

### CPI-007: Idioma inglés
**Estado:** ✅ PASÓ
**Duración Total:** 6090ms
**Transaction IDs:** SBX20251110021900

**Pasos ejecutados:**
- ✅ Generate Token - 2203ms
- ✅ Search Installments (language=ENG) - 1884ms

**Detalle del flujo:**

#### Paso 1: Generate Token
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 2203ms

#### Paso 2: Search Installments (language=ENG)
**Endpoint:** `POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search`
**Status:** 200
**Duración:** 1884ms


---

## Resumen Ejecutivo

### Estadísticas Generales
- **Total de Casos de Prueba:** 7
- **Casos Exitosos:** 3 (42.9%)
- **Casos Fallidos:** 4 (57.1%)
- **Ambiente:** SANDBOX
- **Fecha:** 2025-11-10
- **Duración Total de Ejecución:** 137.32 segundos

### Cobertura de Pruebas
- ✅ **Token Generation API:** Validado
- ✅ **Installments Search API:** Validado
- ❌ **Token Reutilizable:** No validado
- ❌ **TransactionId Consistency:** No validado
- ❌ **Error Handling:** No validado
- ✅ **Múltiples BINs:** Validado
- ❌ **Amount Especial (0.00):** No validado
- ✅ **Soporte Multi-idioma (ENG):** Validado

### Estado del Ambiente SANDBOX
⚠️ **PARCIALMENTE OPERATIVO (4 tests fallaron)**

Se encontraron 4 tests fallidos. Revisar los detalles de cada caso para más información.

### Observaciones
- **CPI-002:** Token no pudo ser reutilizado
- **CPI-003:** Installments search failed: El token no debe ser nulo o vacío
- **CPI-004:** Solo 4 de 5 escenarios pasaron
- **CPI-006:** Installments search failed: El token no debe ser nulo o vacío

---

**Documento generado:** 2025-11-10 02:19:07
**Ejecutado por:** Suite de Pruebas Automatizada
**Ambiente:** SANDBOX (sandbox-api-pw.izipay.pe)
**Merchant Code:** 4001834
**Estado Final:** ⚠️ 4 TESTS FALLARON
