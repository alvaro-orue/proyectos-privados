# Archivos para Compartir - Suite de Pruebas Izipay API Installments

## Descripción General

Este paquete contiene scripts de prueba automatizados para validar el API de Installments de Izipay en múltiples ambientes (DEV, SANDBOX, QA, PROD).

## Versión Actual

**Versión:** 2.1
**Fecha:** 2025-11-10
**Mejoras principales:**
- ✅ Soporte mejorado para ambiente SANDBOX
- ✅ Delay automático de 2 segundos para SANDBOX (evita Error TN)
- ✅ BINs específicos por ambiente
- ✅ Advertencias contextuales para ambientes inestables
- ✅ **Conversión automática a Word (DOCX) usando Pandoc** ⭐ **NUEVO**
- ✅ **Informes con detalles completos de requests/responses** ⭐ **NUEVO**

---

## Opción 1: Paquete Mínimo (Para Comenzar) - 13 archivos

### Scripts de Prueba (8 archivos)
1. **test_suite_completo.py** ⭐ **PRINCIPAL** - Script maestro interactivo
2. **test_cpi_001.py** - Test individual: Flujo completo exitoso
3. **test_cpi_002.py** - Test individual: Token reutilizable
4. **test_cpi_003.py** - Test individual: TransactionId consistente
5. **test_cpi_004.py** - Test individual: Casos de error (5 escenarios)
6. **test_cpi_005.py** - Test individual: Diferentes BINs
7. **test_cpi_006.py** - Test individual: Amount 0.00
8. **test_cpi_007.py** - Test individual: Idioma inglés

### Documentación (4 archivos)
9. **GUIA_USO_SCRIPT_MAESTRO.md** ⭐ **LEER PRIMERO** - Guía completa de uso
10. **BINS_POR_AMBIENTE.md** - Documentación de BINs por ambiente
11. **README_ENTREGA.md** - Guía de entrega y setup
12. **RESUMEN_SCRIPTS.md** - Resumen de casos de prueba

### Utilidades (2 archivos)
13. **markdown_to_word.py** - Exportador de informes a Word (opcional - legacy)
14. **test_pandoc_conversion.py** - Test de verificación de Pandoc ⭐ **NUEVO**

---

## Opción 2: Paquete Completo (Recomendado) - 20 archivos

**Incluye todo el Paquete Mínimo (14 archivos) +**

### Documentación Adicional (6 archivos)
15. **00_LEEME_PRIMERO.txt** - Instrucciones iniciales rápidas
16. **INSTRUCCIONES_CONFIGURACION.txt** - Configuración detallada
17. **INSTRUCCIONES_SUITE_COMPLETA.md** - Guía de suite completa
18. **GUIA_CONVERSION_WORD.md** - Guía de conversión automática a Word ⭐ **NUEVO**
19. **CHANGELOG_ACTUALIZACIONES.md** - Registro de cambios versión 2.1 ⭐ **NUEVO**
20. **EXPORTAR_A_WORD.md** - Guía de exportación a Word (legacy)

---

## Opción 3: Paquete con Referencias (Para QA Avanzado) - 22 archivos

**Incluye todo el Paquete Completo (20 archivos) +**

### Archivos de Referencia (2 archivos)
21. **ResultsSandBoxBin.xlsx** - 24,681 BINs de SANDBOX (referencia)
22. **ResultsSanBoxBinesEnc.xlsx** - 24,681 BINs de SANDBOX (referencia alternativa)

⚠️ **Nota:** Estos Excel son solo de referencia. El script ya tiene los BINs validados incorporados.

---

## Instalación y Uso Rápido

### 1️⃣ Instalar Dependencias
```bash
# Dependencia obligatoria
pip install requests

# Dependencia opcional (para conversión automática a Word)
winget install JohnMacFarlane.Pandoc
```

### 2️⃣ Ejecutar Script Maestro
```bash
python test_suite_completo.py
```

### 3️⃣ Seguir las Instrucciones Interactivas
El script te pedirá:
1. Seleccionar ambiente (DEV/SANDBOX/QA/PROD)
2. Ingresar Merchant Code
3. Ingresar Public Key
4. Confirmar y ejecutar

### 4️⃣ Revisar Resultados
El script generará automáticamente:
- **INFORME_PRUEBAS_{AMBIENTE}_{TIMESTAMP}.md** - Informe en Markdown
- **INFORME_PRUEBAS_{AMBIENTE}_{TIMESTAMP}.docx** - Informe en Word ⭐ **AUTOMÁTICO** (si Pandoc está instalado)
- **RESULTADOS_PRUEBAS_{AMBIENTE}_{TIMESTAMP}.json** - Datos completos en JSON

---

## Credenciales por Ambiente

### DEV y QA
```
Merchant Code: 4078370
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

### SANDBOX
```
Merchant Code: 4001834
Public Key: VErethUtraQuxas57wuMuquprADrAHAb
```

---

## Ambientes Soportados

| Ambiente | URL Base | Estabilidad | BINs Disponibles | Recomendación |
|----------|----------|-------------|------------------|---------------|
| **DEV** | testapi-pw.izipay.pe | ✅ Alta | 4 BINs validados | ✅ **RECOMENDADO** para pruebas |
| **QA** | qa-api-pw.izipay.pe | ✅ Alta | 4 BINs validados | ✅ **RECOMENDADO** para validación |
| **SANDBOX** | sandbox-api-pw.izipay.pe | ⚠️ Baja | 1 BIN validado | ⚠️ Solo validación de conectividad |
| **PROD** | api-pw.izipay.pe | ✅ Alta | Variable | 🔴 Usar con precaución |

---

## Casos de Prueba Incluidos

| ID | Descripción | Valida |
|----|-------------|--------|
| **CPI-001** | Flujo completo exitoso | Token + Búsqueda de cuotas |
| **CPI-002** | Token reutilizable | Reutilización de token en múltiples llamadas |
| **CPI-003** | TransactionId consistente | Uso del mismo TransactionId |
| **CPI-004** | Casos de error | 5 escenarios de error (401, 400, etc.) |
| **CPI-005** | Diferentes BINs | Múltiples bancos (SCOTIABANK, BBVA, BCP) |
| **CPI-006** | Amount 0.00 | Validación de amount especial |
| **CPI-007** | Idioma inglés | Soporte multi-idioma (ESP/ENG) |

**Total:** 7 casos de prueba automatizados

---

## Características Destacadas

### ✅ Automatización Completa
- Ejecución automática de 7 casos de prueba
- Generación automática de informes
- Validación automática de respuestas

### ✅ Multi-Ambiente
- Soporte para DEV, SANDBOX, QA, PROD
- Configuración dinámica por ambiente
- URLs y credenciales específicas por ambiente

### ✅ Manejo Inteligente de SANDBOX
- **Delay automático de 2 segundos** (crítico para evitar Error TN)
- BINs específicos validados para SANDBOX
- Advertencias sobre inestabilidad del ambiente

### ✅ Informes Profesionales
- Formato Markdown con tablas y estadísticas
- **Conversión automática a Word (.docx) usando Pandoc** ⭐ **NUEVO**
- Detalles completos de requests/responses en cada paso ⭐ **NUEVO**
- JSON estructurado para análisis programático
- Headers, bodies y Transaction IDs completos

### ✅ Manejo de Errores
- Validación de 5 escenarios de error
- Mensajes claros y descriptivos
- Captura de timeouts y excepciones

---

## Problemas Conocidos y Soluciones

### SANDBOX: Error 500 (Internal Server Error)
**Causa:** Timeout interno del servidor de SANDBOX (20+ segundos)
**Solución:** Usar DEV o QA para pruebas confiables

### SANDBOX: Error TN (Token Null)
**Causa:** SANDBOX requiere tiempo para procesar el token
**Solución:** ✅ El script ya incluye delay de 2 segundos automáticamente

### SANDBOX: Solo 1 BIN funciona
**Causa:** Solo 1 de 24,681 BINs está configurado para merchant 4001834
**Solución:** ✅ El script usa automáticamente solo BINs validados

---

## Estructura de Entrega

### Carpeta: SCRIPTS_PARA_QA/

```
SCRIPTS_PARA_QA/
│
├── 📄 00_LEEME_PRIMERO.txt                    ← Inicio rápido
├── 📘 GUIA_USO_SCRIPT_MAESTRO.md              ← ⭐ Guía principal
├── 📘 README_ENTREGA.md                       ← Guía de entrega
├── 📘 BINS_POR_AMBIENTE.md                    ← BINs por ambiente
├── 📘 RESUMEN_SCRIPTS.md                      ← Resumen de tests
├── 📘 INSTRUCCIONES_CONFIGURACION.txt         ← Configuración
├── 📘 INSTRUCCIONES_SUITE_COMPLETA.md         ← Suite completa
├── 📘 EXPORTAR_A_WORD.md                      ← Exportación Word
│
├── 🐍 test_suite_completo.py                  ← ⭐ SCRIPT MAESTRO
├── 🐍 test_cpi_001.py                         ← Test CPI-001
├── 🐍 test_cpi_002.py                         ← Test CPI-002
├── 🐍 test_cpi_003.py                         ← Test CPI-003
├── 🐍 test_cpi_004.py                         ← Test CPI-004
├── 🐍 test_cpi_005.py                         ← Test CPI-005
├── 🐍 test_cpi_006.py                         ← Test CPI-006
├── 🐍 test_cpi_007.py                         ← Test CPI-007
│
├── 🐍 markdown_to_word.py                     ← Exportador Word
├── 📦 instalar_exportador.bat                 ← Instalador (Windows)
│
├── 📊 ResultsSandBoxBin.xlsx                  ← Referencia BINs
└── 📊 ResultsSanBoxBinesEnc.xlsx              ← Referencia BINs
```

---

## Soporte y Contacto

### Documentación
- Guía principal: `GUIA_USO_SCRIPT_MAESTRO.md`
- BINs por ambiente: `BINS_POR_AMBIENTE.md`
- Troubleshooting: Ver sección "Solución de Problemas" en guía principal

### Ejecución de Pruebas
1. Leer `GUIA_USO_SCRIPT_MAESTRO.md`
2. Ejecutar `python test_suite_completo.py`
3. Seguir instrucciones interactivas

### Problemas Comunes
- **Error TN en SANDBOX:** Normal, ambiente inestable - usar DEV/QA
- **Error 500 en SANDBOX:** Normal, timeout del servidor - usar DEV/QA
- **ModuleNotFoundError:** Ejecutar `pip install requests`

---

## Changelog

### Versión 2.1 (2025-11-10) ⭐ **ACTUAL**
- ✅ **Conversión automática a Word (DOCX) usando Pandoc**
- ✅ **Informes con detalles completos de requests/responses**
- ✅ Detección automática de Pandoc instalado
- ✅ Mensajes de error informativos si Pandoc falta
- ✅ Headers completos en informes (request y response)
- ✅ Bodies completos en informes
- ✅ Transaction IDs documentados
- ✅ Objetivos por cada test
- ✅ Script de test de Pandoc (test_pandoc_conversion.py)
- ✅ Guía completa de conversión a Word

### Versión 2.0 (2025-11-07)
- ✅ Agregado delay automático de 2 segundos para SANDBOX
- ✅ BINs específicos por ambiente
- ✅ Advertencias para SANDBOX
- ✅ Documentación actualizada con hallazgos de SANDBOX
- ✅ Guía de uso completa

### Versión 1.0 (2025-11-04)
- ✅ Script maestro inicial
- ✅ 7 casos de prueba automatizados
- ✅ Soporte multi-ambiente
- ✅ Generación de informes Markdown/JSON
- ✅ Exportación manual a Word

---

## Resumen: ¿Qué Archivos Compartir?

### Para Desarrollo/QA (Recomendado)
📦 **Paquete Completo (20 archivos)**

### Para Usuario Final (Mínimo)
📦 **Paquete Mínimo (14 archivos)**

### Para QA Avanzado con Referencias
📦 **Paquete con Referencias (22 archivos)**

---

**Fecha de entrega:** 2025-11-10
**Versión:** 2.1
**Estado:** ✅ LISTO PARA COMPARTIR

---

## Inicio Rápido (3 Pasos)

```bash
# 1. Instalar dependencias
pip install requests

# 2. Ejecutar script maestro
python test_suite_completo.py

# 3. Seguir instrucciones en pantalla
# - Seleccionar ambiente
# - Ingresar credenciales
# - Revisar informe generado
```

**¡Listo para usar!** 🚀
