# 🔧 Instrucciones para Pruebas en SANDBOX

**Última actualización**: 2025-11-07
**Estado**: ✅ BIN validado encontrado | ⚠️ Ambiente ALTAMENTE INESTABLE

---

## 📊 Estado Actual (Actualizado 2025-11-07)

### ✅ Lo que SÍ funciona en SANDBOX
- ✅ **Token Generation** (200 OK) - Funciona correctamente en ~800ms
- ✅ **Autenticación** - Merchant 4001834 es válido
- ✅ **BIN 511578** (BBVA MC Platinum) - **ÚNICO BIN VALIDADO** ⭐

### ⚠️ Problemas CRÍTICOS del Ambiente SANDBOX

#### 1. Inestabilidad Severa
- ❌ **Error 500** (Internal Server Error) - Muy frecuente (>80% de requests)
- ❌ **Error TN** "El token no debe ser nulo o vacío" - Incluso con tokens válidos
- ❌ **Timeouts** de 20-22 segundos antes de responder Error 500
- ⚠️ **Comportamiento errático** - Mismo request puede funcionar o fallar aleatoriamente

#### 2. Configuración Limitada de BINs
De **24,681 BINs** en la base de datos de SANDBOX:
- ✅ **Solo 1 BIN confirmado funcional**: 511578 (BBVA MC Platinum)
- ❌ BIN 545545 (SCOTIABANK) - Falla con Error 500 o TN
- ❌ BIN 553650 (BBVA MC) - Falla con Error TN
- ❌ Resto de BINs - No validados o fallan

#### 3. Delay Crítico Requerido
**IMPORTANTE**: SANDBOX requiere un **delay de 2 segundos** entre:
1. Generación de Token
2. Búsqueda de Cuotas

Sin este delay, se obtiene Error TN incluso con token válido.

---

## 🎯 Credenciales de SANDBOX

### Merchant Code y API Key
```
Ambiente: SANDBOX
URL Base: https://sandbox-api-pw.izipay.pe
Merchant Code: 4001834
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

### Endpoints
```
Token Generation:
POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate

Search Installments:
POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search
```

---

## 🚀 Cómo Probar en SANDBOX

### Opción 1: Usar Script Maestro (RECOMENDADO)

```bash
cd SCRIPTS_PARA_QA
python test_suite_completo.py
```

**Flujo interactivo:**
1. Seleccionar opción **2. SANDBOX**
2. Verás advertencia sobre inestabilidad del ambiente
3. Ingresar credenciales:
   - Merchant Code: `4001834`
   - Public Key: `VErethUtraQuxas57wuMuquprADrAHAb`
4. El script automáticamente:
   - ✅ Aplica delay de 2 segundos
   - ✅ Usa solo BIN validado (511578)
   - ✅ Maneja errores apropiadamente

### Opción 2: Script Individual

```bash
cd SCRIPTS_PARA_QA
python test_cpi_001.py
```

**Características:**
- ✅ Delay de 2 segundos incorporado
- ✅ Usa BIN 545545 (puede fallar por inestabilidad)
- ✅ Configuración pre-cargada para SANDBOX

### Opción 3: Prueba Manual (Para Debugging)

```python
import requests, time

# 1. Generate Token
token_response = requests.post(
    "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "transactionId": "SBX20251107120000"
    },
    json={
        "requestSource": "ECOMMERCE",
        "merchantCode": "4001834",
        "orderNumber": "ORDER20251107120000",
        "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
        "amount": "100.00"
    }
)

token = token_response.json()["response"]["token"]
print(f"Token: {token[:50]}...")

# 2. CRÍTICO: Esperar 2 segundos
time.sleep(2)

# 3. Search Installments
installments_response = requests.post(
    "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "transactionId": "SBX20251107120000"
    },
    json={
        "bin": "511578",  # ÚNICO BIN validado
        "merchantCode": "4001834",
        "language": "ESP"
    }
)

print(f"Status: {installments_response.status_code}")
print(f"Response: {installments_response.json()}")
```

---

## 📋 BINs Disponibles en SANDBOX

### BINs Validados ✅
| BIN | Banco | Tipo | Cuotas | Estado |
|-----|-------|------|--------|--------|
| **511578** | BBVA | MC Platinum | 36 | ✅ **FUNCIONAL** (con errores esporádicos) |

### BINs en Base de Datos (No Validados) ⚠️
Total en DB: **24,681 BINs**

**Distribución por banco:**
- SCOTIABANK: 64 BINs
- BBVA: 82 BINs
- INTERBANK: 52 BINs
- BCP: 47 BINs
- OTROS: 24,436 BINs

**NOTA**: La mayoría de estos BINs NO están configurados para merchant 4001834 o no funcionan confiablemente.

### BINs Probados que FALLAN ❌
| BIN | Banco | Error Observado |
|-----|-------|-----------------|
| 545545 | SCOTIABANK | Error 500 / Error TN |
| 553650 | BBVA MC | Error TN |
| 411111 | VISA TEST | Error TN |
| 424242 | VISA TEST | Error 500 |

---

## ⚠️ Recomendaciones Importantes

### 🔴 NO Uses SANDBOX Para:
- ❌ Pruebas funcionales completas
- ❌ Validación de múltiples BINs
- ❌ Pruebas de performance
- ❌ Demostraciones a clientes
- ❌ Validación pre-producción

### ✅ USA SANDBOX Solo Para:
- ✅ Validar conectividad básica
- ✅ Verificar credenciales del merchant
- ✅ Confirmar estructura de requests/responses
- ✅ Testing de integración inicial (con expectativas bajas)

### 🟢 MEJOR OPCIÓN: Usa DEV o QA
Para pruebas confiables y completas:

**DEV / QA:**
```
Merchant Code: 4078370
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
URL DEV: https://testapi-pw.izipay.pe
URL QA: https://qa-api-pw.izipay.pe
```

**Ventajas:**
- ✅ Estabilidad >95%
- ✅ 4 BINs validados funcionando
- ✅ Respuestas <1 segundo
- ✅ Sin errores 500 o TN
- ✅ Comportamiento predecible

---

## 🔍 Troubleshooting SANDBOX

### Error TN: "El token no debe ser nulo o vacío"

**Causa**: SANDBOX requiere tiempo para procesar el token antes de usarlo.

**Solución**:
```python
# Generar token
token = generate_token()

# ⏱️ CRÍTICO: Esperar 2 segundos
time.sleep(2)

# Ahora buscar cuotas
search_installments(token)
```

**Notas:**
- ✅ Scripts actualizados YA incluyen este delay
- ⚠️ Incluso con delay, puede fallar esporádicamente

### Error 500: Internal Server Error

**Causa**: Timeout interno del servidor SANDBOX (20+ segundos).

**Síntomas**:
- Respuesta demora 20-22 segundos
- Luego retorna Error 500
- No hay detalles adicionales en `errorMessage`

**Solución**:
❌ **No hay solución del lado del cliente**

**Opciones:**
1. Reintentar el request (puede funcionar la 2da o 3ra vez)
2. Esperar unos minutos y volver a intentar
3. **MEJOR**: Usar DEV o QA en su lugar

### Solo 1 BIN funciona

**Causa**: Solo el BIN 511578 está correctamente configurado para merchant 4001834.

**Solución**:
1. ✅ Scripts automáticamente usan solo BINs validados en SANDBOX
2. Para probar más BINs, usa DEV/QA (4 BINs validados)
3. Contactar a Izipay para solicitar más BINs configurados (ver abajo)

---

## 📞 Contactar a Izipay (Si Necesitas Más BINs)

### Paso 1: Enviar Solicitud

**Email a**: soporte@izipay.pe o developers@izipay.pe

**Asunto**: Solicitud de configuración de BINs adicionales en SANDBOX - Merchant 4001834

**Mensaje Sugerido**:
```
Estimado equipo de Izipay,

Estoy trabajando con el API de Installments en el ambiente SANDBOX
(merchant 4001834) y he observado las siguientes limitaciones:

ESTADO ACTUAL:
- Merchant Code: 4001834
- Ambiente: SANDBOX (https://sandbox-api-pw.izipay.pe)
- BINs validados funcionando: Solo 1 (511578 - BBVA)
- BINs en base de datos: 24,681 total

SOLICITUD:
Por favor, configurar BINs adicionales para testing de Installments API:
1. 545545 (SCOTIABANK) - Actualmente falla con Error 500/TN
2. 553650 (BBVA MC) - Actualmente falla con Error TN
3. 400917 (SCOTIABANK VISA)
4. 377893 (BCP)

O indicar qué BINs están disponibles y configurados para merchant 4001834.

PROBLEMAS OBSERVADOS:
- Error 500 después de 20+ segundos (timeout interno)
- Error TN incluso con tokens válidos y delay de 2 segundos
- Solo 1 de 24,681 BINs funciona confiablemente

EVIDENCIAS:
Puedo proporcionar logs detallados y resultados de pruebas si lo requieren.

Agradezco su pronta atención.

Saludos,
[Tu Nombre]
[Tu Empresa]
```

### Paso 2: Información Técnica (Si te la solicitan)

**Request Exitoso - Token Generation:**
```json
POST https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate

Request:
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4001834",
  "orderNumber": "ORDER20251107010000",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}

Response: 200 OK ✅
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "eyJhbGci...",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }
}
```

**Request Fallido - Search Installments (Error 500):**
```json
POST https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search

Request:
{
  "bin": "545545",
  "merchantCode": "4001834",
  "language": "ESP"
}

Response: 500 Internal Server Error ❌ (después de 21 segundos)
{
  "code": "500",
  "errorMessage": "The API Public service threw an error. Check the errors field to view possible details."
}
```

**Request Fallido - Search Installments (Error TN):**
```json
Response: 400 Bad Request ❌
{
  "code": "TN",
  "message": "El token no debe ser nulo o vacío",
  "header": {
    "transactionStartDatetime": "2025-11-07 01:05:27.273",
    "transactionEndDatetime": "2025-11-07 01:05:27.335",
    "millis": 62
  }
}
```

---

## 📊 Archivos de Referencia

### Archivos Excel con BINs de SANDBOX
Ubicación: `SCRIPTS_PARA_QA/`

1. **ResultsSandBoxBin.xlsx** - 24,681 BINs en base de datos SANDBOX
2. **ResultsSanBoxBinesEnc.xlsx** - 24,681 BINs (versión alternativa)

**Distribución de BINs por banco:**
```
SCOTIABANK:  64 BINs
BBVA:        82 BINs
INTERBANK:   52 BINs
BCP:         47 BINs
OTROS:   24,436 BINs
--------------------------
TOTAL:   24,681 BINs
```

**NOTA**: Estos archivos son solo de referencia. La mayoría de estos BINs NO están configurados para funcionar con merchant 4001834.

---

## 📈 Comparación de Ambientes

| Característica | DEV/QA | SANDBOX | PROD |
|----------------|--------|---------|------|
| **Estabilidad** | ✅ Alta (>95%) | ❌ Baja (<20%) | ✅ Alta |
| **BINs Validados** | 4 BINs | 1 BIN | Variable |
| **Tiempo Respuesta** | <1s | 1-22s | <2s |
| **Error 500** | Raro | Muy frecuente | Raro |
| **Error TN** | No | Frecuente | No |
| **Requiere Delay** | No | Sí (2s) | No |
| **Uso Recomendado** | ✅ Desarrollo | ⚠️ Solo conectividad | 🔴 Validación final |

---

## ✅ Checklist de Validación SANDBOX

Antes de reportar problemas, verifica:

```
[ ] ✅ Credenciales correctas (Merchant 4001834, Public Key VErethUtraQuxas57wuMuquprADrAHAb)
[ ] ✅ URL correcta (https://sandbox-api-pw.izipay.pe)
[ ] ✅ Delay de 2 segundos entre token y search
[ ] ✅ Usando BIN validado (511578)
[ ] ✅ Token generado correctamente (200 OK, code "00")
[ ] ⚠️ Expectativas realistas (esperar errores 500/TN frecuentes)
[ ] ✅ Considerar usar DEV/QA para pruebas confiables
```

---

## 🎯 Resultado Esperado (Cuando Funciona)

```bash
$ python test_suite_completo.py

Seleccionar ambiente: 2 (SANDBOX)

⚠️ ⚠️ ⚠️ ADVERTENCIA - AMBIENTE SANDBOX ⚠️ ⚠️ ⚠️
El ambiente SANDBOX es INESTABLE...
[Ver advertencia completa]

Merchant Code: 4001834
Public Key: VErethUtraQuxas57wuMuquprADrAHAb

============================================================
CASO DE PRUEBA CPI-001 - AMBIENTE: SANDBOX
============================================================

PASO 1: GENERAR TOKEN
✅ Token generado exitosamente (850ms)

⏱️  Esperando 2 segundos (requerido por SANDBOX)...

PASO 2: BUSCAR CUOTAS
✅ Cuotas obtenidas exitosamente (1200ms)
🏦 Emisor: BBVA
💳 BIN: 511578
📊 Número de cuotas disponibles: 36

============================================================
RESUMEN FINAL
============================================================
Estado: ✅ PASÓ
Duración Total: 4,050ms (incluyendo delay de 2s)
```

**NOTA**: Incluso con configuración correcta, espera que falle ~50-80% de las veces debido a la inestabilidad del ambiente.

---

## 📚 Recursos Adicionales

### Documentación Relacionada
- [GUIA_USO_SCRIPT_MAESTRO.md](SCRIPTS_PARA_QA/GUIA_USO_SCRIPT_MAESTRO.md) - Guía completa del script maestro
- [BINS_POR_AMBIENTE.md](SCRIPTS_PARA_QA/BINS_POR_AMBIENTE.md) - BINs validados por ambiente
- [ARCHIVOS_PARA_COMPARTIR.md](SCRIPTS_PARA_QA/ARCHIVOS_PARA_COMPARTIR.md) - Archivos para distribuir

### Scripts Relevantes
- `test_suite_completo.py` - Script maestro con soporte SANDBOX
- `test_cpi_001.py` - Test individual con delay SANDBOX
- `test_sandbox_validation.py` - Validación específica SANDBOX

### Contactos
- **Portal Developers**: https://developers.izipay.pe
- **Soporte Técnico**: soporte@izipay.pe
- **Developers**: developers@izipay.pe

---

**Última actualización**: 2025-11-07
**Validado por**: Automatización QA
**Estado**: ⚠️ SANDBOX ALTAMENTE INESTABLE - Usar DEV/QA para pruebas confiables
