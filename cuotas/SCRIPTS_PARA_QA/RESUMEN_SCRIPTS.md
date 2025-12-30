# Resumen de Scripts de Prueba - API Installments

## Paquete Completo para Analista de Calidad

Este paquete contiene **7 scripts de prueba** listos para ejecutar en cualquier ambiente de Izipay.

---

## 📋 Lista de Scripts

### 1. test_cpi_001.py - Flujo completo exitoso
**Descripción:** Genera un token y busca cuotas disponibles para un BIN
**Pasos:**
1. Generar token de sesión
2. Buscar cuotas disponibles con BIN 545545 (SCOTIABANK)

**Resultado esperado:** Token generado + 12 cuotas disponibles
**Duración aproximada:** 2-7 segundos

---

### 2. test_cpi_002.py - Token Reutilizable
**Descripción:** Verifica que un token puede reutilizarse en múltiples consultas
**Pasos:**
1. Generar token de sesión
2. Primera búsqueda de cuotas
3. Segunda búsqueda con el mismo token

**Resultado esperado:** Ambas búsquedas exitosas usando el mismo token
**Duración aproximada:** 3-4 segundos

---

### 3. test_cpi_003.py - TransactionId Consistente
**Descripción:** Valida que el mismo TransactionId se mantiene en ambas llamadas
**Pasos:**
1. Generar token con TransactionId específico
2. Buscar cuotas con el mismo TransactionId

**Resultado esperado:** TransactionId consistente en ambas llamadas
**Duración aproximada:** 2 segundos

---

### 4. test_cpi_004.py - Casos de Error
**Descripción:** Valida el manejo correcto de errores del API
**Escenarios probados:**
1. Token inválido → Debe retornar 401
2. Sin header Authorization → Debe retornar 400
3. BIN con formato inválido → Debe retornar 400
4. Merchant Code inválido → Debe retornar 401
5. Parámetro BIN faltante → Debe retornar 400

**Resultado esperado:** Todos los errores detectados correctamente
**Duración aproximada:** 6 segundos

---

### 5. test_cpi_005.py - Diferentes BINs
**Descripción:** Prueba con 4 BINs de diferentes bancos
**BINs probados:**
1. **545545** (SCOTIABANK) → 12 cuotas
2. **400917** (SCOTIABANK VISA) → 36 cuotas
3. **377893** (BCP) → 36 cuotas
4. **553650** (BBVA MC Platinum) → 36 cuotas

**Resultado esperado:** Los 4 BINs retornan cuotas correctamente
**Duración aproximada:** 7-8 segundos

---

### 6. test_cpi_006.py - Amount 0.00
**Descripción:** Valida transacciones con monto 0.00
**Pasos:**
1. Generar token con amount="0.00"
2. Buscar cuotas disponibles

**Resultado esperado:** Sistema acepta amount 0.00 sin errores
**Duración aproximada:** 3 segundos

---

### 7. test_cpi_007.py - Idioma Inglés
**Descripción:** Valida respuestas en idioma inglés
**Pasos:**
1. Generar token de sesión
2. Buscar cuotas con language="ENG"

**Resultado esperado:** Mensaje en inglés "Approved" (en lugar de "Operación exitosa")
**Duración aproximada:** 2-3 segundos

---

## 🔧 Configuración Requerida

**IMPORTANTE:** Antes de ejecutar cualquier script, debes modificar la sección `CONFIG` en cada archivo.

### Valores a Cambiar:

1. **URLs del Ambiente**
   - DEV: `https://testapi-pw.izipay.pe`
   - SANDBOX: `https://sandbox-api-pw.izipay.pe`
   - QA: `https://qa-api-pw.izipay.pe`
   - PROD: `https://api-pw.izipay.pe`

2. **Credenciales del Comercio**
   - `merchant_code`: Código del comercio a probar
   - `public_key`: Llave pública del comercio

### Valores Actuales (Comercio 4078370 en DEV):
```python
CONFIG = {
    "token_url": "https://testapi-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://testapi-pw.izipay.pe/Installments/v1/Installments/Search",
    "merchant_code": "4078370",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}
```

---

## 📁 Archivos del Paquete

```
SCRIPTS_PARA_QA/
├── README.md                           # Documentación principal
├── INSTRUCCIONES_CONFIGURACION.txt     # Instrucciones detalladas
├── RESUMEN_SCRIPTS.md                  # Este archivo
├── test_cpi_001.py                     # Script CPI-001
├── test_cpi_002.py                     # Script CPI-002
├── test_cpi_003.py                     # Script CPI-003
├── test_cpi_004.py                     # Script CPI-004
├── test_cpi_005.py                     # Script CPI-006
├── test_cpi_006.py                     # Script CPI-006
└── test_cpi_007.py                     # Script CPI-007
```

---

## ⚡ Ejecución Rápida

```bash
# 1. Instalar dependencias (solo una vez)
pip install requests

# 2. Configurar el script (editar CONFIG)
# Abrir test_cpi_001.py y modificar URLs + credenciales

# 3. Ejecutar
python test_cpi_001.py

# 4. Ver resultados
# Los archivos se generan en la misma carpeta:
# - test_result.json
# - test_report.txt
# - step_X_*.json
```

---

## ✅ Criterios de Éxito

### Test Exitoso:
- Exit code: `0`
- Todos los pasos marcados con ✅
- Archivo `test_result.json` con `"passed": true`

### Test Fallido:
- Exit code: `1`
- Pasos fallidos marcados con ❌
- Archivo `test_result.json` con `"passed": false`
- Campo `error_message` con descripción del error

---

## 📊 Resultados Generados

Cada script genera automáticamente:

1. **test_result.json** - Resultado completo en JSON con:
   - Test ID y nombre
   - Estado (passed/failed)
   - Duración total
   - Detalles de cada paso (request/response)
   - Timestamps

2. **test_report.txt** - Reporte legible con:
   - Resumen del test
   - Estado de cada paso
   - Duraciones
   - Errores (si aplica)

3. **step_X_[nombre].json** - Detalles de cada paso individual:
   - Request completo (headers + body)
   - Response completo
   - Status code
   - Duración en ms

---

## 🎯 Casos de Uso

### Caso 1: Validar Ambiente DEV
```bash
# Configurar scripts con URLs de DEV
# Ejecutar todos los tests
python test_cpi_001.py
python test_cpi_002.py
python test_cpi_003.py
python test_cpi_004.py
python test_cpi_005.py
python test_cpi_006.py
python test_cpi_007.py
```

### Caso 2: Probar Nuevo Comercio en QA
```bash
# 1. Editar CONFIG en todos los scripts
# 2. Cambiar URLs a QA
# 3. Cambiar merchant_code y public_key
# 4. Ejecutar tests
python test_cpi_001.py  # Test básico primero
```

### Caso 3: Validación Pre-Producción
```bash
# 1. Configurar con URLs de PROD
# 2. Ejecutar test de lectura solamente (CPI-001, CPI-005)
# 3. NO ejecutar tests de error en PROD
```

---

## ⚠️ Advertencias

1. **NO ejecutar tests de error (CPI-004) en PRODUCCIÓN** sin autorización
2. **Verificar credenciales** antes de ejecutar en cualquier ambiente
3. **Validar BINs disponibles** en cada ambiente (pueden variar)
4. **Respetar rate limits** del API (no ejecutar tests masivos)

---

## 📞 Soporte

Para dudas o problemas:
1. Revisar `README.md` en esta carpeta
2. Revisar `INSTRUCCIONES_CONFIGURACION.txt`
3. Consultar `DOCUMENTACION_PRUEBAS_DEV.md` (documentación completa de resultados)

---

**Fecha de creación:** 2025-11-04
**Ambiente de prueba original:** DEV (testapi-pw.izipay.pe)
**Comercio de prueba original:** 4078370
**Versión:** 1.0
