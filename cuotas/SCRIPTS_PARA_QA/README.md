# Scripts de Pruebas API Installments - Izipay

## Descripción
Este paquete contiene 7 scripts de prueba para validar el API de Installments de Izipay en diferentes ambientes.

## Requisitos
- Python 3.7 o superior
- Librería `requests`

## Instalación
```bash
pip install requests
```

## Configuración

### 🔧 ANTES DE EJECUTAR - CONFIGURAR AMBIENTE Y COMERCIO

Cada script tiene una sección `CONFIG` al inicio del archivo que debe ser modificada según el ambiente a probar:

```python
# ============================================================================
# CONFIGURACIÓN - MODIFICAR ESTOS VALORES SEGÚN EL AMBIENTE A PROBAR
# ============================================================================
CONFIG = {
    # ⚠️ CAMBIAR: URL del ambiente (DEV, SANDBOX, QA, PROD)
    "token_url": "https://testapi-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://testapi-pw.izipay.pe/Installments/v1/Installments/Search",

    # ⚠️ CAMBIAR: Credenciales del comercio a probar
    "merchant_code": "4078370",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}
```

### URLs por Ambiente:

#### DEV (Desarrollo)
```python
"token_url": "https://testapi-pw.izipay.pe/security/v1/Token/Generate",
"installments_url": "https://testapi-pw.izipay.pe/Installments/v1/Installments/Search"
```

#### SANDBOX
```python
"token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
"installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search"
```

#### QA
```python
"token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
"installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search"
```

#### PRODUCCIÓN
```python
"token_url": "https://api-pw.izipay.pe/security/v1/Token/Generate",
"installments_url": "https://api-pw.izipay.pe/Installments/v1/Installments/Search"
```

## Scripts Disponibles

### CPI-001: Flujo completo exitoso
**Archivo:** `test_cpi_001.py`
**Descripción:** Genera un token y busca cuotas disponibles para un BIN
**Ejecución:**
```bash
python test_cpi_001.py
```

### CPI-002: Token Reutilizable
**Archivo:** `test_cpi_002.py`
**Descripción:** Verifica que un token puede reutilizarse en múltiples consultas
**Ejecución:**
```bash
python test_cpi_002.py
```

### CPI-003: TransactionId Consistente
**Archivo:** `test_cpi_003.py`
**Descripción:** Valida que el mismo TransactionId se mantiene en ambas llamadas
**Ejecución:**
```bash
python test_cpi_003.py
```

### CPI-004: Casos de Error
**Archivo:** `test_cpi_004.py`
**Descripción:** Valida el manejo correcto de errores (5 escenarios)
**Ejecución:**
```bash
python test_cpi_004.py
```

### CPI-005: Diferentes BINs
**Archivo:** `test_cpi_005.py`
**Descripción:** Prueba con 4 BINs de diferentes bancos
**Ejecución:**
```bash
python test_cpi_005.py
```

### CPI-006: Amount 0.00
**Archivo:** `test_cpi_006.py`
**Descripción:** Valida transacciones con monto 0.00
**Ejecución:**
```bash
python test_cpi_006.py
```

### CPI-007: Idioma Inglés
**Archivo:** `test_cpi_007.py`
**Descripción:** Valida respuestas en idioma inglés
**Ejecución:**
```bash
python test_cpi_007.py
```

## Resultados

Cada script genera automáticamente:

1. **test_result.json** - Resultado completo en formato JSON
2. **test_report.txt** - Reporte legible en texto plano
3. **step_X_[nombre].json** - Detalles de cada paso individual

Los archivos se guardan en la misma carpeta donde se ejecuta el script.

## Interpretación de Resultados

### ✅ Prueba Exitosa
- Exit code: 0
- Todos los pasos marcados con ✅
- Estado: "PASÓ"

### ❌ Prueba Fallida
- Exit code: 1
- Pasos fallidos marcados con ❌
- Estado: "FALLÓ"
- Mensaje de error incluido

## BINs Disponibles para Pruebas

Los siguientes BINs están configurados en el ambiente DEV/QA:

| BIN | Banco | Cuotas | Diferido |
|-----|-------|--------|----------|
| 545545 | SCOTIABANK | 12 | 3 meses |
| 400917 | SCOTIABANK VISA | 36 | 0 meses |
| 377893 | BCP | 36 | 3 meses |
| 553650 | BBVA MC Platinum | 36 | 3 meses |

## Ejemplo de Ejecución

```bash
# 1. Configurar el script (editar CONFIG en test_cpi_001.py)
# 2. Ejecutar
python test_cpi_001.py

# Salida esperada:
# ============================================================
# CASO DE PRUEBA CPI-001
# Flujo completo exitoso - Generar token y buscar cuotas
# ============================================================
# ...
# ✅ PRUEBA EXITOSA
```

## Soporte

Para más información, consultar la documentación completa en:
`DOCUMENTACION_PRUEBAS_DEV.md`

---

**Fecha de creación:** 2025-11-04
**Versión:** 1.0
**Ambiente de prueba original:** DEV (testapi-pw.izipay.pe)
**Comercio de prueba original:** 4078370
