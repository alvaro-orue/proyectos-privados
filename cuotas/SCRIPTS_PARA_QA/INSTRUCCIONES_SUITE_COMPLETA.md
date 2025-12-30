# Suite Completa de Pruebas - API Installments

## 🎯 ¿Qué es este script?

`test_suite_completo.py` es un **script maestro unificado** que:

✅ Ejecuta **TODOS los 7 casos de prueba** en un solo comando
✅ Solicita al usuario el **ambiente** y **comercio** a probar
✅ Genera automáticamente un **informe completo en Markdown**
✅ **NO requiere** editar código ni archivos de configuración
✅ Es **interactivo** y fácil de usar

## 🚀 Inicio Rápido

### 0. ⚠️ ANTES DE EMPEZAR - MUY IMPORTANTE

**📖 Lee el archivo `BINS_POR_AMBIENTE.md` primero**

Este archivo contiene información crítica sobre qué BINs (números de tarjeta de prueba) funcionan en cada ambiente. Algunos BINs NO funcionan en ciertos ambientes:

- BIN `377893` funciona en DEV/QA pero **NO en SANDBOX**
- BIN `377750` funciona en SANDBOX pero **NO en DEV/QA**
- BIN `545545` funciona en todos los ambientes pero con **diferentes resultados** (12 cuotas en DEV/QA vs 36 cuotas en SANDBOX)

El script maestro ya tiene los BINs correctos pre-configurados para cada ambiente, pero debes conocer estas diferencias para interpretar los resultados correctamente.

### 1. Instalar dependencias

```bash
pip install requests
```

### 2. Ejecutar el script

```bash
python test_suite_completo.py
```

### 3. Responder las preguntas

El script te preguntará:

```
📍 Selecciona el ambiente para las pruebas:
   1. DEV (Desarrollo)
   2. SANDBOX
   3. QA (Quality Assurance)
   4. PRODUCCIÓN

👉 Ingresa el número del ambiente (1-4): 1

🏪 Configuración del comercio
👉 Ingresa el Merchant Code: 4078370
👉 Ingresa el Public Key: VErethUtraQuxas57wuMuquprADrAHAb

⏸️  Presiona ENTER para iniciar las pruebas...
```

### 4. ¡Listo!

El script ejecutará automáticamente:
- CPI-001: Flujo completo exitoso
- CPI-002: Token reutilizable
- CPI-003: TransactionId consistente
- CPI-004: Casos de error (5 escenarios)
- CPI-005: Diferentes BINs (4 bancos)
- CPI-006: Amount 0.00
- CPI-007: Idioma inglés

## 📊 Resultados Generados

Al finalizar, el script genera **automáticamente**:

### 1. Informe en Markdown
**Archivo:** `INFORME_PRUEBAS_[AMBIENTE]_[TIMESTAMP].md`

Similar al informe de documentación, incluye:
- Tabla de casos de prueba
- Resultados detallados de cada test
- Requests y responses
- Resumen ejecutivo
- Estadísticas completas
- Estado del ambiente

**Ejemplo:** `INFORME_PRUEBAS_DEV_20251104_183000.md`

### 2. Resultados en JSON
**Archivo:** `RESULTADOS_PRUEBAS_[AMBIENTE]_[TIMESTAMP].json`

Contiene todos los datos técnicos:
- Configuración utilizada
- Resultados de cada test
- Tiempos de ejecución
- Requests/responses completos
- Transaction IDs

**Ejemplo:** `RESULTADOS_PRUEBAS_DEV_20251104_183000.json`

## 💡 Ventajas sobre los Scripts Individuales

| Característica | Scripts Individuales | Suite Completa |
|----------------|---------------------|----------------|
| Número de archivos | 7 scripts Python | 1 script Python |
| Configuración | Editar código en cada script | Interactivo (sin editar código) |
| Ejecución | 7 comandos separados | 1 solo comando |
| Informe | Archivos individuales | Informe unificado automático |
| Facilidad de uso | Requiere conocimiento técnico | Muy fácil de usar |

## 🎨 Ejemplo de Uso Completo

```bash
$ python test_suite_completo.py

======================================================================
   SUITE COMPLETA DE PRUEBAS - API INSTALLMENTS IZIPAY
======================================================================

📍 Selecciona el ambiente para las pruebas:
----------------------------------------------------------------------
   1. DEV (Desarrollo)
   2. SANDBOX
   3. QA (Quality Assurance)
   4. PRODUCCIÓN
----------------------------------------------------------------------

👉 Ingresa el número del ambiente (1-4): 1

✅ Ambiente seleccionado: DEV (Desarrollo)
   URL: testapi-pw.izipay.pe

======================================================================
🏪 Configuración del comercio
======================================================================

👉 Ingresa el Merchant Code: 4078370
👉 Ingresa el Public Key: VErethUtraQuxas57wuMuquprADrAHAb

======================================================================
📋 Resumen de la configuración
======================================================================
   Ambiente: DEV (Desarrollo)
   Token URL: https://testapi-pw.izipay.pe/security/v1/Token/Generate
   Installments URL: https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
   Merchant Code: 4078370
   Public Key: VErethUtraQuxas57wuMuqup...
======================================================================

⏸️  Presiona ENTER para iniciar las pruebas...

======================================================================
🚀 INICIANDO EJECUCIÓN DE PRUEBAS
======================================================================

======================================================================
Ejecutando test 1/7
======================================================================

============================================================
Ejecutando CPI-001: Flujo completo exitoso
============================================================
🆔 Transaction ID: DEV20251104183000
🆔 Order Number: ORDER20251104183000

📝 Paso 1: Generar token...
✅ Token generado en 1234.56ms

📝 Paso 2: Buscar cuotas...
✅ Cuotas obtenidas en 2345.67ms
📊 Cuotas disponibles: 12

✅ CPI-001 completado exitosamente

[... continúa con los demás tests ...]

======================================================================
📊 RESUMEN DE RESULTADOS
======================================================================

Total de tests ejecutados: 7
✅ Tests exitosos: 7
❌ Tests fallidos: 0
⏱️  Duración total: 35.42 segundos

Detalle por test:
  ✅ PASÓ CPI-001: Flujo completo exitoso (3580ms)
  ✅ PASÓ CPI-002: Token reutilizable (4123ms)
  ✅ PASÓ CPI-003: TransactionId consistente (2049ms)
  ✅ PASÓ CPI-004: Casos de error (6124ms)
  ✅ PASÓ CPI-005: Diferentes BINs (8345ms)
  ✅ PASÓ CPI-006: Amount 0.00 (3435ms)
  ✅ PASÓ CPI-007: Idioma inglés (2636ms)

======================================================================
📄 GENERANDO INFORME
======================================================================

✅ Informe generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251104_183000.md
   📁 C:\...\RESULTADOS_PRUEBAS_DEV_20251104_183000.json

======================================================================
🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!
======================================================================
```

## 📁 Estructura del Informe Generado

El informe Markdown incluye:

```markdown
# Informe de Pruebas - API Installments Izipay

## Descripción
Validación completa del API de Installments en ambiente DEV

## Ambiente de Pruebas
- Ambiente: DEV (Desarrollo)
- Fecha: 2025-11-04
- Merchant Code: 4078370

## Endpoints Utilizados
- Token Generation API (con ejemplos)
- Installments Search API (con ejemplos)

## Casos de Prueba Ejecutados
- Tabla con todos los resultados

## Resultados Detallados
- Detalle de cada test
- Pasos ejecutados
- Requests/responses (para tests principales)

## Resumen Ejecutivo
- Estadísticas generales
- Cobertura de pruebas
- Estado del ambiente
- Conclusión
```

## 🎯 Casos de Uso

### Caso 1: Validar Ambiente DEV
```bash
python test_suite_completo.py
# Seleccionar: 1 (DEV)
# Ingresar merchant y public key
# ¡Listo! Informe generado automáticamente
```

### Caso 2: Probar Nuevo Comercio en QA
```bash
python test_suite_completo.py
# Seleccionar: 3 (QA)
# Ingresar credenciales del nuevo comercio
# Revisar informe generado
```

### Caso 3: Validación Pre-Producción
```bash
python test_suite_completo.py
# Seleccionar: 4 (PRODUCCIÓN)
# ⚠️ CUIDADO: No ejecutar tests de error en PROD
```

## ⚠️ Consideraciones Importantes

### 1. Tests de Error en Producción
El test CPI-004 incluye 5 escenarios de error. En **PRODUCCIÓN**, considera:
- Coordinar con el equipo antes de ejecutar
- Revisar si hay límites de rate limiting
- Validar que no afecte métricas de monitoreo

### 2. BINs Disponibles
El script usa estos BINs por defecto:
- 545545 (SCOTIABANK)
- 400917 (SCOTIABANK VISA)
- 377893 (BCP)
- 553650 (BBVA MC Platinum)

Si algún BIN no está configurado en el ambiente, el test CPI-005 podría fallar parcialmente.

### 3. Tiempos de Ejecución
- Duración normal: 30-45 segundos
- Si toma más de 2 minutos: Verificar conectividad del ambiente

### 4. Archivos Generados
Los archivos se crean en el mismo directorio donde ejecutas el script.

## 🔍 Troubleshooting

### Error: "Module 'requests' not found"
```bash
pip install requests
```

### Error: Timeout al ejecutar tests
- Verificar que el ambiente esté activo
- Verificar conectividad de red
- Verificar que las URLs del ambiente sean correctas

### Tests fallan con error 401/400
- Verificar que el Merchant Code sea correcto
- Verificar que el Public Key sea correcto
- Verificar que las credenciales correspondan al ambiente seleccionado

### El informe no se genera
- Verificar permisos de escritura en el directorio
- Verificar que no haya errores críticos durante la ejecución

## 📞 Soporte

Para más información:
- `README.md` - Documentación general
- `RESUMEN_SCRIPTS.md` - Descripción de cada caso de prueba
- Archivos de resultados JSON para debugging

## 🎉 Ventajas del Script Unificado

✅ **Fácil de usar** - No requiere editar código
✅ **Rápido** - Ejecuta todas las pruebas en ~40 segundos
✅ **Completo** - Genera informe profesional automáticamente
✅ **Flexible** - Funciona con cualquier ambiente y comercio
✅ **Profesional** - Resultados listos para compartir con el equipo

---

**Fecha de creación:** 2025-11-04
**Versión:** 1.0
**Autor:** Automatización QA
