# 🏦 Guía de BINs por Ambiente - API Installments Izipay

## 📌 Propósito de este Documento

Este documento contiene información **CRÍTICA** sobre qué BINs (Bank Identification Numbers) funcionan en cada ambiente de Izipay. **DEBES consultar esta guía antes de ejecutar las pruebas** para evitar errores.

---

## ⚠️ IMPORTANTE - LEER PRIMERO

**Problema común**: No todos los BINs funcionan en todos los ambientes.

- ✅ **DEV y QA**: Comparten la misma base de datos de BINs (263 BINs disponibles)
- ⚠️ **SANDBOX**: Tiene BINs diferentes (261 BINs disponibles)
- ❓ **PRODUCCIÓN**: Los BINs dependen de la configuración real del merchant

**Consecuencia**: Si usas un BIN que no está configurado en el ambiente, obtendrás errores 400, 403 o 500.

---

## 🎯 BINs Recomendados para Pruebas

### ✅ AMBIENTE: DEV (Desarrollo)

**URL Base**: `https://testapi-pw.izipay.pe`
**Merchant Code por defecto**: `4078370`
**Total de BINs en DB**: 263

#### BINs Validados que SÍ Funcionan:

| BIN    | Banco/Emisor        | Tipo       | Cuotas Máx | Diferido | Estado |
|--------|---------------------|------------|------------|----------|--------|
| 545545 | SCOTIABANK          | Mastercard | 12         | 3 meses  | ✅ OK  |
| 400917 | SCOTIABANK VISA     | Visa       | 36         | 0 meses  | ✅ OK  |
| 510308 | SCOTIABANK MC       | Mastercard | 0          | 0 meses  | ✅ OK  |
| 377893 | BCP                 | Amex       | 36         | 3 meses  | ✅ OK  |
| 377755 | AMEX INTERBANK      | Amex       | 36         | 3 meses  | ✅ OK  |
| 553650 | BBVA MC Platinum    | Mastercard | 36         | 3 meses  | ✅ OK  |
| 511578 | BBVA                | Mastercard | 36         | 0 meses  | ✅ OK  |
| 362333 | Diners Club         | Diners     | 36         | 3 meses  | ✅ OK  |
| 602008 | WieseCash           | Privada    | 12         | 3 meses  | ✅ OK  |
| 456781 | Banco Financiero    | Visa       | 7          | 3 meses  | ✅ OK  |

#### 💡 BINs Recomendados para Tests Rápidos (DEV):

```python
# Usar estos BINs en los scripts de prueba para DEV:
BINS_RECOMENDADOS_DEV = {
    "545545": {"banco": "SCOTIABANK", "cuotas_esperadas": 12},
    "400917": {"banco": "SCOTIABANK VISA", "cuotas_esperadas": 36},
    "377893": {"banco": "BCP", "cuotas_esperadas": 36},
    "553650": {"banco": "BBVA MC Platinum", "cuotas_esperadas": 36}
}
```

**Nota**: Estos son los BINs configurados por defecto en `test_suite_completo.py`.

---

### ✅ AMBIENTE: QA (Quality Assurance)

**URL Base**: `https://qa-api-pw.izipay.pe`
**Merchant Code por defecto**: `4078370`
**Total de BINs en DB**: 263 (misma DB que DEV)

#### BINs Validados que SÍ Funcionan:

**IMPORTANTE**: QA usa la misma base de datos que DEV, por lo tanto **los mismos BINs funcionan**.

| BIN    | Banco/Emisor        | Tipo       | Cuotas Máx | Diferido | Estado |
|--------|---------------------|------------|------------|----------|--------|
| 545545 | SCOTIABANK          | Mastercard | 12         | 3 meses  | ✅ OK  |
| 400917 | SCOTIABANK VISA     | Visa       | 36         | 0 meses  | ✅ OK  |
| 510308 | SCOTIABANK MC       | Mastercard | 0          | 0 meses  | ✅ OK  |
| 377893 | BCP                 | Amex       | 36         | 3 meses  | ✅ OK  |
| 377755 | AMEX INTERBANK      | Amex       | 36         | 3 meses  | ✅ OK  |
| 553650 | BBVA MC Platinum    | Mastercard | 36         | 3 meses  | ✅ OK  |
| 511578 | BBVA                | Mastercard | 36         | 0 meses  | ✅ OK  |
| 362333 | Diners Club         | Diners     | 36         | 3 meses  | ✅ OK  |
| 602008 | WieseCash           | Privada    | 12         | 3 meses  | ✅ OK  |
| 456781 | Banco Financiero    | Visa       | 7          | 3 meses  | ✅ OK  |

#### 💡 BINs Recomendados para Tests Rápidos (QA):

```python
# Usar los mismos BINs que en DEV:
BINS_RECOMENDADOS_QA = {
    "545545": {"banco": "SCOTIABANK", "cuotas_esperadas": 12},
    "400917": {"banco": "SCOTIABANK VISA", "cuotas_esperadas": 36},
    "377893": {"banco": "BCP", "cuotas_esperadas": 36},
    "553650": {"banco": "BBVA MC Platinum", "cuotas_esperadas": 36}
}
```

---

### ⚠️ AMBIENTE: SANDBOX

**URL Base**: `https://sandbox-api-pw.izipay.pe`
**Merchant Code por defecto**: `4001834`
**Total de BINs en DB**: **24,681** (base de datos diferente a DEV/QA)

**📊 Fuente de Datos**: Archivos Excel `ResultsSandBoxBin.xlsx` y `ResultsSanBoxBinesEnc.xlsx` (actualizado 2025-11-06)

#### 🏦 Distribución de BINs por Banco en SANDBOX:

| Banco          | Total de BINs en DB | BINs Validados | Observaciones |
|----------------|---------------------|----------------|---------------|
| SCOTIABANK     | 64                  | 1 confirmado   | Solo 545545 validado para merchant 4001834 |
| BBVA           | 82                  | 1 confirmado   | Solo 553650 validado para merchant 4001834 |
| INTERBANK      | 52                  | 0 confirmados  | BIN 377750 existe pero no configurado para 4001834 |
| BCP            | 47                  | 0 confirmados  | BIN 377893 NO existe en SANDBOX |
| OTROS          | 24,436              | -              | Diversos bancos y emisores |

**🚨 IMPORTANTE - Diferencia entre "Existe en DB" vs "Configurado para Merchant":**

- ✅ **Existe en DB**: El BIN está en la base de datos de SANDBOX (24,681 BINs totales)
- ⚠️ **Configurado para Merchant**: El BIN está autorizado para el merchant específico (mucho menor cantidad)

**Conclusión**: De los 24,681 BINs en la base de datos de SANDBOX, solo un subconjunto está configurado para cada merchant. Para el merchant `4001834`, solo se han validado exitosamente 2 BINs en las pruebas.

#### BINs Validados que SÍ Funcionan (Confirmados con Pruebas Reales):

**⚠️ IMPORTANTE**: Estos BINs fueron probados y confirmados para el merchant `4001834` en SANDBOX.

| BIN    | Banco/Emisor        | Tipo       | Cuotas Máx | Diferido | Estado Pruebas | Observaciones |
|--------|---------------------|------------|------------|----------|----------------|---------------|
| 545545 | SCOTIABANK MC       | Mastercard | 36         | 0 meses  | ✅ CONFIRMADO  | Funciona correctamente |
| 553650 | BBVA MC Black       | Mastercard | 36         | 0 meses  | ✅ CONFIRMADO  | Funciona correctamente |

#### BINs que Existen en DB pero NO Funcionan para Merchant 4001834:

**⚠️ Estos BINs están en la base de datos de SANDBOX pero NO están configurados para el merchant 4001834:**

| BIN    | Banco/Emisor        | Tipo       | Estado en DB | Error Obtenido | Razón |
|--------|---------------------|------------|--------------|----------------|-------|
| 400917 | SCOTIABANK VISA     | Visa       | ✅ Existe    | Error 500      | No configurado para este merchant |
| 510308 | SCOTIABANK MC       | Mastercard | ✅ Existe    | Error 500      | No configurado para este merchant |
| 377750 | AMEX INTERBANK      | Amex       | ✅ Existe    | Error TN       | No configurado para este merchant |
| 511578 | BBVA MC Platinum    | Mastercard | ✅ Existe    | Error TN       | No configurado para este merchant |
| 512312 | BBVA MC CLASICA     | Mastercard | ✅ Existe    | ⚠️ No probado  | Probablemente no configurado |
| 362426 | DINERS CLUB         | Diners     | ✅ Existe    | ⚠️ No probado  | Probablemente no configurado |
| 602008 | WieseCash           | Privada    | ✅ Existe    | ⚠️ No probado  | Probablemente no configurado |
| 527556 | Banco Financiero    | Mastercard | ✅ Existe    | ⚠️ No probado  | Probablemente no configurado |

#### 💡 BINs Recomendados para Tests Rápidos (SANDBOX - Merchant 4001834):

```python
# 🚨 USAR SOLO ESTOS BINs para merchant 4001834 en SANDBOX:
BINS_RECOMENDADOS_SANDBOX = {
    "545545": {"banco": "SCOTIABANK MC", "cuotas_esperadas": 36},  # ✅ Validado
    "553650": {"banco": "BBVA MC Black", "cuotas_esperadas": 36}   # ✅ Validado
}

# ⚠️ EVITAR ESTOS BINs (existen pero no configurados para merchant 4001834):
BINS_NO_CONFIGURADOS = ["400917", "510308", "377750", "511578", "512312", "362426", "602008", "527556"]
```

#### 📋 Lista Completa de BINs Disponibles en SANDBOX (Primeros 50 BINs de Excel):

**Nota**: Esta es una muestra de los 24,681 BINs totales. Consulta los archivos Excel para la lista completa.

<details>
<summary>Ver lista de BINs SCOTIABANK (64 total)</summary>

```
545545, 545544, 545543, 510308, 400917, 545542, 545541, 545540,
545539, 545538, 545537, 545536, 545535, 545534, 545533, 545532,
... (y 48 más - ver Excel para lista completa)
```
</details>

<details>
<summary>Ver lista de BINs BBVA (82 total)</summary>

```
553650, 511578, 512312, 426702, 426703, 426704, 426705, 426706,
426707, 426708, 426709, 426710, 426711, 426712, 426713, 426714,
... (y 66 más - ver Excel para lista completa)
```
</details>

<details>
<summary>Ver lista de BINs INTERBANK (52 total)</summary>

```
377750, 377751, 377752, 377753, 377754, 377755, 377756, 377757,
377758, 377759, 377760, 377761, 377762, 377763, 377764, 377765,
... (y 36 más - ver Excel para lista completa)
```
</details>

<details>
<summary>Ver lista de BINs BCP (47 total)</summary>

```
⚠️ NOTA: BIN 377893 (usado en DEV/QA) NO existe en SANDBOX
BCP tiene otros 47 BINs en SANDBOX, pero ninguno validado para merchant 4001834
```
</details>

#### 🚨 Diferencias Importantes SANDBOX vs DEV/QA:

| Característica | DEV/QA | SANDBOX (Merchant 4001834) | Impacto |
|----------------|--------|---------------------------|---------|
| Total BINs en DB | 263 | **24,681** | ⚠️ DB completamente diferente |
| BIN 545545 cuotas | 12 | 36 | ⚠️ Resultado diferente |
| BIN 545545 estado | ✅ Funciona | ✅ Funciona (VALIDADO) | ✅ Compatible |
| BIN 553650 estado | ✅ Funciona | ✅ Funciona (VALIDADO) | ✅ Compatible |
| BIN 400917 (SCOTIABANK VISA) | ✅ Funciona | ❌ Existe pero NO configurado | ⚠️ Fallará en SANDBOX |
| BIN 510308 (SCOTIABANK MC) | ✅ Funciona | ❌ Existe pero NO configurado | ⚠️ Fallará en SANDBOX |
| BIN 377893 (BCP) | ✅ Existe | ❌ NO existe en DB | ⚠️ Fallará en SANDBOX |
| BIN 377750 (AMEX INTERBANK) | ❌ NO validado | ⚠️ Existe pero NO configurado | ⚠️ Probablemente fallará |
| BIN 511578 (BBVA MC Platinum) | ✅ Funciona | ❌ Existe pero NO configurado | ⚠️ Fallará en SANDBOX |
| BIN 362333 (Diners) | ✅ Existe | ❌ NO existe en DB | ⚠️ Fallará en SANDBOX |
| BIN 362426 (Diners) | ❌ NO validado | ⚠️ Existe (no probado) | ⚠️ Estado desconocido |
| BIN 456781 (Financiero) | ✅ Existe (7 cuotas) | ❌ NO existe en DB | ⚠️ Fallará en SANDBOX |
| BIN 527556 (Financiero) | ❌ NO validado | ⚠️ Existe (no probado) | ⚠️ Estado desconocido |

**💡 Conclusión Clave**: De todos los BINs probados, solo **2 BINs funcionan** para merchant 4001834 en SANDBOX: `545545` y `553650`.

---

## 🔬 Análisis Detallado de BINs en SANDBOX (Desde Archivos Excel)

### 📊 Datos Estadísticos Completos:

**Total de BINs en SANDBOX**: 24,681

**Distribución por Marca/Tipo de Tarjeta**:
- Marca 1 (Mastercard): Mayor cantidad de BINs
- Marca 14 (Visa): Segunda mayor cantidad
- Marca 11 (Amex): INTERBANK y BCP principalmente
- Otras marcas: Diners Club, Privadas (WieseCash), etc.

**Top 10 Bancos por Cantidad de BINs**:
1. OTROS/DIVERSOS: 24,436 BINs
2. BBVA: 82 BINs
3. SCOTIABANK: 64 BINs
4. INTERBANK: 52 BINs
5. BCP: 47 BINs
6. (Otros bancos menores)

### 🎯 Implicaciones para Pruebas:

**Realidad del Merchant 4001834**:
- ✅ **Existe en DB**: 24,681 BINs totales
- ⚠️ **Configurados para merchant**: Solo 2 validados (545545, 553650)
- ❌ **Tasa de configuración**: 0.008% (2 de 24,681)

**¿Por qué tan pocos BINs configurados?**
1. Los merchants tienen contratos específicos con bancos/emisores
2. No todos los bancos tienen acuerdos con todos los merchants
3. Algunos BINs requieren configuración especial (fees, comisiones, etc.)
4. SANDBOX es un ambiente de pruebas con configuración limitada

**Recomendación para QA**:
- NO asumir que todos los BINs en Excel funcionarán
- Probar primero con BINs validados (545545, 553650)
- Si necesitas más BINs, solicitar configuración explícita a Izipay
- Documentar claramente qué BINs funcionan para cada merchant

### 📋 Estructura de Datos en Excel:

**Columnas disponibles**:
- `Bin`: Número de 6 dígitos (ej: 545545)
- `Descripcion`: Nombre del banco/emisor (ej: SCOTIABANK)
- `Banco`: Código o nombre del banco
- `BinEncriptado`: Versión encriptada del BIN
- `Marca`: Código numérico (1=MC, 14=Visa, 11=Amex, etc.)
- `Tipo`: Tipo de tarjeta (Débito, Crédito, etc.)

**Ejemplo de registros**:
```
Bin     | Descripcion      | Marca | Banco      | Tipo
--------|------------------|-------|------------|-------
545545  | SCOTIABANK       | 1     | SCOTIABANK | Crédito
400917  | SCOTIABANK       | 14    | SCOTIABANK | Crédito
553650  | BBVA             | 1     | BBVA       | Crédito
377750  | INTERBANK        | 11    | INTERBANK  | Crédito
```

---

### ❓ AMBIENTE: PRODUCCIÓN

**URL Base**: `https://api-pw.izipay.pe`
**Merchant Code**: Depende del comercio real
**Total de BINs en DB**: Depende de la configuración del merchant

#### ⚠️ ADVERTENCIAS PARA PRODUCCIÓN:

1. **NO ejecutar tests de error (CPI-004)** en producción sin autorización
2. **Verificar BINs con el equipo de Izipay** antes de probar
3. **Los BINs disponibles dependen del contrato del merchant**
4. **Usar BINs reales de prueba** proporcionados por el banco/emisor
5. **Solicitar sandbox de producción** si está disponible

#### 💡 Recomendaciones:

- Solicitar a Izipay la lista de BINs configurados para tu merchant en producción
- Usar BINs de prueba oficiales de cada banco (si existen)
- NO usar BINs de tarjetas reales de clientes
- Validar primero en SANDBOX antes de probar en producción

---

## 🔍 ¿Cómo Saber Si un BIN Funciona?

### Respuesta Exitosa (200 OK):
```json
{
  "code": "00",
  "message": "Operación exitosa",
  "response": {
    "merchantCode": "4078370",
    "issuerName": "SCOTIABANK",
    "bin": "545545",
    "installments": [
      {
        "cuota": 1,
        "mes_diferido": 0,
        "tea": 0.00
      },
      ...
    ]
  }
}
```

### Errores Comunes:

#### Error 400 (Bad Request):
```json
{
  "code": "400",
  "errorMessage": "TN"
}
```
**Causa**: BIN no tiene formato válido o no cumple validaciones básicas.

#### Error 403 (Forbidden):
```json
{
  "code": "403",
  "errorMessage": "IB0"
}
```
**Causa**: BIN no está autorizado para este merchant.

#### Error 500 (Internal Server Error):
```json
{
  "code": "500",
  "errorMessage": "The API Public service threw an error..."
}
```
**Causa**: BIN no existe en la base de datos del ambiente o hay un error de configuración.

---

## 🛠️ Solución de Problemas

### Problema 1: BIN Falla en SANDBOX pero Funciona en DEV

**Solución**:
1. Consulta la tabla de "Diferencias Importantes SANDBOX vs DEV/QA" arriba
2. Usa los BINs alternativos recomendados para SANDBOX
3. Ejemplo: En lugar de `377893` (BCP), usa `377750` (AMEX INTERBANK)

### Problema 2: Necesito Probar Más BINs

**Solución**:
1. Consulta el archivo `config_environments.py` en el repositorio
2. Allí están listados los 10 BINs validados por ambiente
3. Si necesitas más BINs, contacta a Izipay para solicitar la lista completa

### Problema 3: Error 500 en SANDBOX con Todos los BINs

**Solución**:
1. Verifica que estés usando el `merchant_code` correcto: `4001834` para SANDBOX
2. Revisa el archivo `INSTRUCCIONES_SANDBOX.md` para más detalles
3. Si el problema persiste, puede que necesites solicitar configuración de BINs a Izipay

### Problema 4: ¿Puedo Usar Cualquier BIN en Producción?

**NO**. En producción:
1. Solo funcionan los BINs configurados específicamente para tu merchant
2. Debes solicitar a Izipay la lista de BINs disponibles
3. Algunos merchants tienen restricciones por contrato (ej: solo Visa, solo ciertos bancos)

---

## 📊 Resumen Rápido - Qué BINs Usar

### Para Pruebas Básicas (1 BIN):
```
DEV/QA:     545545 (SCOTIABANK - 12 cuotas)
SANDBOX:    545545 (SCOTIABANK - 36 cuotas) ⚠️ Nota: Diferente resultado
```

### Para Pruebas Completas (Merchant 4001834):
```
DEV/QA:     545545, 400917, 377893, 553650 (4 BINs validados)
SANDBOX:    545545, 553650 (🚨 SOLO 2 BINs confirmados para merchant 4001834)
```

**⚠️ IMPORTANTE PARA SANDBOX**:
- Merchant 4001834 tiene configuración limitada de BINs
- Solo 2 BINs han sido validados exitosamente: 545545 y 553650
- Otros BINs (400917, 510308, 377750, 511578) existen en la DB pero NO funcionan para este merchant

### Para Pruebas Extensivas (10 BINs):
```
DEV/QA:     Ver tabla completa arriba (10 BINs validados)
SANDBOX:    ⚠️ Solo 2 BINs validados para merchant 4001834
            Para más BINs, solicitar configuración a Izipay
```

---

## 📞 ¿Necesitas Más BINs?

Si necesitas BINs adicionales o específicos:

1. **Consultar Base de Datos**:
   - DEV/QA: 263 BINs disponibles en total
   - SANDBOX: **24,681 BINs** disponibles en base de datos
   - **⚠️ IMPORTANTE**: No todos los BINs están configurados para todos los merchants

2. **Archivos Excel con BINs de SANDBOX**:
   - `ResultsSandBoxBin.xlsx`: Lista completa de 24,681 BINs con información detallada
   - `ResultsSanBoxBinesEnc.xlsx`: Lista completa con BINs encriptados
   - Columnas disponibles: Bin, Descripcion, Banco, BinEncriptado, Marca, Tipo

3. **Contactar a Izipay para Configuración**:
   - Email: soporte@izipay.pe
   - Portal: https://developers.izipay.pe
   - **Solicitar específicamente**: "Configuración de BINs adicionales para merchant [CÓDIGO] en ambiente [AMBIENTE]"
   - **Nota**: Aunque existan 24,681 BINs en SANDBOX, solo algunos están configurados por merchant

4. **Verificar Documentación**:
   - Archivo: `config_environments.py` (en el repositorio)
   - Archivo: `ACTUALIZACION_BINS_REALES_2025-11-04.md` (para DEV/QA)
   - Archivo: `INSTRUCCIONES_SANDBOX.md` (para SANDBOX)
   - Archivos Excel: `ResultsSandBoxBin.xlsx` y `ResultsSanBoxBinesEnc.xlsx` (para ver todos los BINs disponibles)

---

## ✅ Checklist Antes de Ejecutar Pruebas

Antes de ejecutar `test_suite_completo.py` o cualquier script individual:

- [ ] Identifiqué el ambiente donde voy a probar (DEV, SANDBOX, QA, PROD)
- [ ] Consulté la tabla de BINs para ese ambiente específico
- [ ] Verifiqué que los BINs que voy a usar están en la lista de "BINs Validados"
- [ ] Si voy a SANDBOX, verifiqué las diferencias con DEV/QA
- [ ] Tengo el `merchant_code` correcto para el ambiente
- [ ] Tengo el `public_key` correcto para el ambiente

---

## 📝 Historial de Actualizaciones

| Fecha | Ambiente | Cambio |
|-------|----------|--------|
| 2025-11-04 | DEV/QA | Documentados 10 BINs validados (de 263 disponibles) |
| 2025-11-04 | SANDBOX | Documentados 10 BINs validados (de 261 disponibles - dato inicial incorrecto) |
| 2025-11-04 | SANDBOX | Identificadas diferencias clave con DEV/QA |
| 2025-11-06 | SANDBOX | **ACTUALIZACIÓN MAYOR**: Análisis de archivos Excel completos |
| 2025-11-06 | SANDBOX | Corregido total de BINs: 24,681 (no 261 como se documentó inicialmente) |
| 2025-11-06 | SANDBOX | Agregada distribución por banco: SCOTIABANK (64), BBVA (82), INTERBANK (52), BCP (47), OTROS (24,436) |
| 2025-11-06 | SANDBOX | Validados mediante pruebas reales: Solo 2 BINs funcionan para merchant 4001834 (545545, 553650) |
| 2025-11-06 | SANDBOX | Documentados 6 BINs que existen en DB pero NO están configurados para merchant 4001834 |
| 2025-11-06 | SANDBOX | Agregada sección explicando diferencia entre "Existe en DB" vs "Configurado para Merchant" |

---

## 🎯 Uso en Scripts Automatizados

El script maestro `test_suite_completo.py` ya incluye los BINs recomendados para cada ambiente. Sin embargo, es importante que entiendas estas diferencias por si necesitas:

1. Ejecutar scripts individuales (test_cpi_001.py hasta test_cpi_007.py)
2. Crear nuevos casos de prueba
3. Diagnosticar fallos en pruebas existentes
4. Documentar resultados de pruebas

---

**Última actualización**: 2025-11-06
**Versión del documento**: 1.0
**Autor**: Equipo de Automatización de Pruebas Izipay

---

**📌 RECUERDA**: Cuando una prueba falle con un error 400, 403 o 500 relacionado con el BIN, **consulta este documento PRIMERO** antes de reportar un bug. Es muy probable que el BIN simplemente no esté configurado en ese ambiente.
