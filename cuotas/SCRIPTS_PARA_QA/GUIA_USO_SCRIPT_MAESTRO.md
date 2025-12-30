# Guía de Uso - Script Maestro de Pruebas

## Descripción

El script `test_suite_completo.py` es un **script maestro interactivo** que ejecuta los 7 casos de prueba del API Installments de Izipay (CPI-001 a CPI-007) y genera un informe completo en formato Markdown y JSON.

## Requisitos

```bash
pip install requests
```

## Ejecución

### Opción 1: Ejecutar directamente
```bash
python test_suite_completo.py
```

### Opción 2: Con Python3 explícito
```bash
python3 test_suite_completo.py
```

## Flujo de Ejecución

### Paso 1: Selección de Ambiente

El script mostrará las opciones de ambiente:

```
📍 Selecciona el ambiente para las pruebas:
----------------------------------------------------------------------
   1. DEV (Desarrollo)
   2. SANDBOX
   3. QA (Quality Assurance)
   4. PRODUCCIÓN
----------------------------------------------------------------------
👉 Ingresa el número del ambiente (1-4):
```

**Recomendaciones por ambiente:**

| Ambiente | Estabilidad | Uso Recomendado | Observaciones |
|----------|-------------|-----------------|---------------|
| **DEV** | ✅ Alta | Desarrollo y pruebas funcionales | Todos los BINs funcionan correctamente |
| **QA** | ✅ Alta | Validación pre-producción | Todos los BINs funcionan correctamente |
| **SANDBOX** | ⚠️ Baja | Solo validación de conectividad | **INESTABLE** - Ver advertencias abajo |
| **PROD** | ✅ Alta | Validación en producción | **⚠️ Usar con precaución** |

### Advertencia Especial: SANDBOX

Si seleccionas SANDBOX (opción 2), verás esta advertencia:

```
⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
⚠️  ADVERTENCIA - AMBIENTE SANDBOX
⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
El ambiente SANDBOX es INESTABLE y puede presentar:
  • Error 500 (Internal Server Error) - Muy frecuente
  • Error TN (Token Null) - Incluso con tokens válidos
  • Timeouts de 20+ segundos
  • Solo 1 BIN validado como funcional: 511578

➡️  Se recomienda usar DEV o QA para pruebas confiables
➡️  SANDBOX debe usarse solo para validar conectividad básica
⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
```

**Problemas conocidos de SANDBOX:**
- Error 500 después de 20+ segundos (timeout interno del servidor)
- Error TN "El token no debe ser nulo o vacío" incluso con tokens válidos
- Solo 1 de 24,681 BINs funciona de manera confiable
- El script automáticamente usa solo BINs validados en SANDBOX

### Paso 2: Configuración del Comercio

Ingresa las credenciales del merchant:

```
🏪 Configuración del comercio
======================================================================

👉 Ingresa el Merchant Code: 4001834
👉 Ingresa el Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

**Credenciales por ambiente:**

#### DEV / QA
```
Merchant Code: 4078370
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

#### SANDBOX
```
Merchant Code: 4001834
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

### Paso 3: Confirmación y Ejecución

El script mostrará un resumen:

```
📋 Resumen de la configuración
======================================================================
   Ambiente: DEV (Desarrollo)
   Token URL: https://testapi-pw.izipay.pe/security/v1/Token/Generate
   Installments URL: https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
   Merchant Code: 4078370
   Public Key: VErethUtraQuxas57wu...
======================================================================

⏸️  Presiona ENTER para iniciar las pruebas...
```

### Paso 4: Ejecución de Pruebas

El script ejecutará los 7 casos de prueba secuencialmente:

```
🚀 INICIANDO EJECUCIÓN DE PRUEBAS
======================================================================

======================================================================
Ejecutando test 1/7
======================================================================
============================================================
Ejecutando CPI-001: Flujo completo exitoso
============================================================

🆔 Transaction ID: DEV20251107010000
🆔 Order Number: ORDER20251107010000

📝 Paso 1: Generar token...
✅ Token generado en 450.23ms

📝 Paso 2: Buscar cuotas...
✅ Cuotas obtenidas en 523.45ms
📊 Cuotas disponibles: 12

✅ CPI-001 completado exitosamente
...
```

**Comportamiento en SANDBOX:**

Verás mensajes adicionales de delay:

```
✅ Token generado en 850.23ms
⏱️  Esperando 2 segundos (requerido por SANDBOX)...

📝 Paso 2: Buscar cuotas...
```

Este delay de 2 segundos es **CRÍTICO** para evitar el Error TN en SANDBOX.

### Paso 5: Resultados

Al finalizar, verás un resumen:

```
📊 RESUMEN DE RESULTADOS
======================================================================

Total de tests ejecutados: 7
✅ Tests exitosos: 7
❌ Tests fallidos: 0
⏱️  Duración total: 8.45 segundos

Detalle por test:
  ✅ PASÓ CPI-001: Flujo completo exitoso (1250ms)
  ✅ PASÓ CPI-002: Token reutilizable (1450ms)
  ✅ PASÓ CPI-003: TransactionId consistente (1180ms)
  ✅ PASÓ CPI-004: Casos de error (2300ms)
  ✅ PASÓ CPI-005: Diferentes BINs (3400ms)
  ✅ PASÓ CPI-006: Amount 0.00 (1100ms)
  ✅ PASÓ CPI-007: Idioma inglés (1150ms)
```

### Paso 6: Archivos Generados

El script genera 2 archivos:

```
📄 GENERANDO INFORME
======================================================================

✅ Informe generado exitosamente:
   📁 C:\path\INFORME_PRUEBAS_DEV_20251107_123045.md
   📁 C:\path\RESULTADOS_PRUEBAS_DEV_20251107_123045.json
```

**Archivos generados:**

1. **INFORME_PRUEBAS_{AMBIENTE}_{TIMESTAMP}.md**
   - Informe completo en Markdown
   - Tabla de resultados
   - Detalles de cada caso de prueba
   - Resumen ejecutivo con estadísticas

2. **RESULTADOS_PRUEBAS_{AMBIENTE}_{TIMESTAMP}.json**
   - Resultados completos en JSON
   - Incluye requests/responses de cada paso
   - Tiempos de ejecución detallados
   - Útil para análisis programático

## Casos de Prueba Ejecutados

### CPI-001: Flujo completo exitoso
- Genera token de sesión
- Busca cuotas disponibles para BIN por defecto
- Valida respuesta exitosa (código 00)

### CPI-002: Token reutilizable
- Genera token
- Realiza primera búsqueda de cuotas
- Reutiliza el mismo token para segunda búsqueda
- Valida que el token funcione en ambas llamadas

### CPI-003: TransactionId consistente
- Genera token con TransactionId específico
- Busca cuotas usando el MISMO TransactionId
- Valida consistencia del TransactionId

### CPI-004: Casos de error (5 escenarios)
1. Token inválido → Espera Error 401
2. Sin header Authorization → Espera Error 400
3. BIN con formato inválido → Espera Error 400
4. Merchant Code inválido → Espera Error 401
5. Parámetro BIN faltante → Espera Error 400

### CPI-005: Diferentes BINs
Prueba múltiples BINs de diferentes bancos:

**DEV/QA (4 BINs):**
- 545545 - SCOTIABANK (12 cuotas)
- 400917 - SCOTIABANK VISA (36 cuotas)
- 377893 - BCP (36 cuotas)
- 553650 - BBVA MC Platinum (36 cuotas)

**SANDBOX (1 BIN):**
- 511578 - BBVA MC Platinum (36 cuotas)

### CPI-006: Amount 0.00
- Genera token con amount="0.00"
- Busca cuotas
- Valida que el sistema acepte amount 0.00

### CPI-007: Idioma inglés
- Genera token
- Busca cuotas con language="ENG"
- Valida respuesta en inglés

## Exportar Informe a Word

Después de generar el informe en Markdown, puedes exportarlo a Word:

```bash
pip install python-docx
python markdown_to_word.py INFORME_PRUEBAS_DEV_20251107_123045.md
```

Esto generará: `INFORME_PRUEBAS_DEV_20251107_123045.docx`

## Solución de Problemas

### Error: ModuleNotFoundError: No module named 'requests'
```bash
pip install requests
```

### Error: Token generation failed
- Verifica el Merchant Code
- Verifica la Public Key
- Verifica conectividad al ambiente seleccionado

### Error TN en SANDBOX (Token Null)
**Causa:** El ambiente SANDBOX es inestable

**Solución:**
1. El script ya incluye delay de 2 segundos automáticamente
2. Si persiste, intenta ejecutar nuevamente
3. Considera usar DEV o QA para pruebas confiables

### Error 500 en SANDBOX
**Causa:** Timeout interno del servidor de SANDBOX (20+ segundos)

**Solución:**
1. Es un problema del ambiente SANDBOX de Izipay
2. No se puede resolver desde el cliente
3. Usa DEV o QA para pruebas funcionales

### Solo 1 BIN funciona en SANDBOX
**Causa:** De los 24,681 BINs en la base de datos de SANDBOX, solo 1 está configurado correctamente para el merchant 4001834

**Solución:**
1. El script automáticamente usa solo el BIN validado (511578)
2. Para probar múltiples BINs, usa DEV o QA

## Características Especiales del Script

### 1. Delay Automático para SANDBOX
El script detecta automáticamente si estás usando SANDBOX y aplica un delay de 2 segundos entre la generación de token y la búsqueda de cuotas.

```python
# Código interno del script
if config.get("transaction_prefix") == "SBX":
    print("⏱️  Esperando 2 segundos (requerido por SANDBOX)...")
    time.sleep(2)
```

### 2. BINs Específicos por Ambiente
El script usa automáticamente BINs diferentes según el ambiente:

- **DEV/QA/PROD:** 4 BINs validados (545545, 400917, 377893, 553650)
- **SANDBOX:** 1 BIN validado (511578)

### 3. Advertencias Contextuales
El script muestra advertencias específicas para ambientes problemáticos.

### 4. Informes Profesionales
Genera informes en Markdown con:
- Tabla de resultados
- Detalles de endpoints
- Request/Response examples
- Resumen ejecutivo con estadísticas
- Recomendaciones

### 5. Codificación UTF-8
El script maneja correctamente caracteres especiales y emojis en Windows y Linux.

## Estructura de Archivos

```
SCRIPTS_PARA_QA/
├── test_suite_completo.py        ← Script maestro
├── test_cpi_001.py                ← Test individual CPI-001
├── test_cpi_002.py                ← Test individual CPI-002
├── test_cpi_003.py                ← Test individual CPI-003
├── test_cpi_004.py                ← Test individual CPI-004
├── test_cpi_005.py                ← Test individual CPI-005
├── test_cpi_006.py                ← Test individual CPI-006
├── test_cpi_007.py                ← Test individual CPI-007
├── markdown_to_word.py            ← Exportador a Word
├── GUIA_USO_SCRIPT_MAESTRO.md     ← Esta guía
├── BINS_POR_AMBIENTE.md           ← Documentación de BINs
└── README_ENTREGA.md              ← Guía de entrega
```

## Recomendaciones Finales

### Para Desarrollo y Pruebas
✅ **Usa DEV o QA** - Ambientes estables con todos los BINs funcionando

### Para Validación en SANDBOX
⚠️ **Expectativas realistas:**
- Solo para validar conectividad básica
- Espera errores 500 y TN frecuentes
- Solo 1 BIN funcional
- Timeouts de 20+ segundos

### Para Producción
🔴 **Usa con precaución:**
- Solo para validación final
- No ejecutar tests masivos
- Coordinar con equipo de producción

---

**Fecha de última actualización:** 2025-11-07
**Versión del script:** 2.0 (con soporte SANDBOX mejorado)
**Autor:** Automatización QA - Izipay
