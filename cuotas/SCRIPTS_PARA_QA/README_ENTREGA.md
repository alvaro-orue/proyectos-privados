# 📦 Paquete de Scripts de Prueba - API Installments Izipay

## 🎯 Contenido del Paquete

Este paquete contiene scripts automatizados para probar el API de Installments de Izipay en diferentes ambientes (DEV, SANDBOX, QA, PRODUCCIÓN).

---

## 📁 Archivos Incluidos

### 📄 DOCUMENTACIÓN (COMENZAR AQUÍ):
1. **00_LEEME_PRIMERO.txt** - ⭐ Guía de inicio rápido
2. **BINS_POR_AMBIENTE.md** - 🏦 CRÍTICO: Qué BINs usar en cada ambiente
3. **INSTRUCCIONES_SUITE_COMPLETA.md** - Cómo usar el script maestro
4. **SOLUCION_ERRORES_BINS.txt** - Solución rápida de errores
5. **EXPORTAR_A_WORD.md** - 📄 Cómo exportar informes a Word
6. **README.md** - Documentación técnica completa
7. **RESUMEN_SCRIPTS.md** - Descripción detallada de cada test

### 🐍 SCRIPTS:
8. **test_suite_completo.py** - ⭐ Script maestro (ejecuta todos los tests)
9. **markdown_to_word.py** - 📄 Conversor Markdown → Word
10. **config_environments.py** - Configuración de ambientes
11. **test_cpi_001.py** a **test_cpi_007.py** - Scripts individuales (7 archivos)

### 🛠️ INSTALADORES:
12. **instalar_exportador.bat** - Instalador automático para Windows

### 📊 ARCHIVOS DE REFERENCIA (Opcional):
10. **ResultsSandBoxBin.xlsx** - Lista de 24,681 BINs en SANDBOX
11. **ResultsSanBoxBinesEnc.xlsx** - BINs encriptados

---

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Instalar Dependencias
```bash
pip install requests
```

### 2️⃣ Leer Documentación Crítica
**IMPORTANTE**: Lee estos archivos ANTES de ejecutar:
- `00_LEEME_PRIMERO.txt` (5 minutos)
- `BINS_POR_AMBIENTE.md` (10 minutos) - Explica por qué algunos tests pueden fallar

### 3️⃣ Ejecutar Tests
```bash
# OPCIÓN A: Script maestro (RECOMENDADO)
python test_suite_completo.py
# Seleccionar ambiente y seguir instrucciones en pantalla

# OPCIÓN B: Scripts individuales
python test_cpi_001.py  # Flujo completo
python test_cpi_002.py  # Token reutilizable
python test_cpi_003.py  # TransactionId consistente
python test_cpi_004.py  # Casos de error
python test_cpi_005.py  # Diferentes BINs
python test_cpi_006.py  # Amount 0.00
python test_cpi_007.py  # Idioma inglés
```

### 4️⃣ (OPCIONAL) Exportar Informe a Word

**Para mayor comodidad, puedes convertir el informe Markdown a Word:**

```bash
# Instalar exportador (solo una vez)
pip install python-docx

# Convertir el informe generado a Word
python markdown_to_word.py INFORME_PRUEBAS_DEV_20251107.md

# O convertir todos los archivos .md a .docx
python markdown_to_word.py -d .
```

**Resultado**: Se genera un archivo `.docx` con formato profesional listo para compartir.

📖 **Guía completa**: Ver `EXPORTAR_A_WORD.md` para más opciones

---

## ⚠️ ADVERTENCIAS IMPORTANTES

### 🚨 Para SANDBOX (Merchant 4001834):

**PROBLEMA CONOCIDO**: SANDBOX presenta inestabilidad actualmente (2025-11-07):
- ✅ Token Generation funciona correctamente
- ❌ Installments Search tiene errores intermitentes:
  - Error 500: "The API Public service threw an error"
  - Error TN: "El token no debe ser nulo o vacío"
  - Timeouts de 21-22 segundos

**RECOMENDACIÓN**:
1. ✅ Usar **DEV** o **QA** para pruebas funcionales (ambientes estables)
2. ⚠️ SANDBOX solo para pruebas de integración (cuando esté estable)
3. Si encuentran errores en SANDBOX, contactar a Izipay

**BINs en SANDBOX**:
- Total en DB: 24,681 BINs
- Configurados para merchant 4001834: Estado inestable (verificar con Izipay)
- BINs documentados: 545545, 553650, 511578 (pero con fallos intermitentes)

### 🏦 Diferencias entre Ambientes:

**BINs que funcionan DIFERENTE por ambiente**:
| BIN | DEV/QA | SANDBOX |
|-----|--------|---------|
| 545545 | 12 cuotas | 36 cuotas |
| 377893 | ✅ Existe | ❌ NO existe |
| 377750 | ❌ NO existe | ✅ Existe |

**Consultar `BINS_POR_AMBIENTE.md` para lista completa**

---

## 📊 Casos de Prueba Incluidos

| Script | Descripción | Duración aprox. |
|--------|-------------|-----------------|
| CPI-001 | Flujo completo exitoso | 3-5 seg |
| CPI-002 | Token reutilizable | 3-5 seg |
| CPI-003 | TransactionId consistente | 3-5 seg |
| CPI-004 | Casos de error (5 escenarios) | 5-10 seg |
| CPI-005 | Diferentes BINs (4 bancos) | 8-12 seg |
| CPI-006 | Amount 0.00 | 3-5 seg |
| CPI-007 | Idioma inglés | 3-5 seg |

**Total (suite completa)**: ~30-45 segundos

---

## 🔧 Configuración de Ambientes

El archivo `config_environments.py` contiene las configuraciones para:

### DEV (Desarrollo):
- URL: `https://testapi-pw.izipay.pe`
- Merchant: 4078370
- BINs validados: 10

### SANDBOX:
- URL: `https://sandbox-api-pw.izipay.pe`
- Merchant: 4001834
- ⚠️ Estado: Inestable (2025-11-07)

### QA:
- URL: `https://qa-api-pw.izipay.pe`
- Merchant: 4078370
- BINs validados: 10 (mismos que DEV)

### PRODUCCIÓN:
- URL: `https://api-pw.izipay.pe`
- Merchant: Variable
- ⚠️ NO ejecutar test CPI-004 (errores) sin autorización

---

## 📝 Resultados Generados

Cada ejecución genera automáticamente:

### Script Maestro:
- `INFORME_PRUEBAS_[AMBIENTE]_[TIMESTAMP].md` - Informe en Markdown
- `RESULTADOS_PRUEBAS_[AMBIENTE]_[TIMESTAMP].json` - Datos técnicos

### Scripts Individuales:
- `test_result.json` - Resultado completo
- `test_report.txt` - Reporte legible
- `step_X_[nombre].json` - Detalles de cada paso

---

## 🐛 Solución de Problemas

### Error: "Module 'requests' not found"
```bash
pip install requests
```

### Error: BIN falla con 400/500/TN
1. Consultar `BINS_POR_AMBIENTE.md`
2. Verificar que el BIN esté disponible para ese ambiente
3. Si persiste, contactar a Izipay

### Error: Timeout al ejecutar tests
- Verificar conectividad de red
- Verificar que el ambiente esté activo
- SANDBOX puede tener timeouts (problema conocido)

### Tests fallan en SANDBOX pero funcionan en DEV/QA
- ✅ Esto es ESPERADO actualmente
- SANDBOX tiene problemas de estabilidad (2025-11-07)
- Usar DEV o QA para validaciones

---

## 📞 Soporte

### Contacto Izipay:
- Email: soporte@izipay.pe
- Portal: https://developers.izipay.pe

### Solicitudes Comunes:
1. **Lista de BINs disponibles**: "Solicito lista de BINs configurados para merchant [CÓDIGO] en ambiente [AMBIENTE]"
2. **Configurar más BINs**: "Solicito configuración de BINs adicionales para merchant [CÓDIGO]"
3. **Problemas en SANDBOX**: "Reporto errores en SANDBOX - Timeouts de 21-22 segundos y errores 500/TN"

---

## ✅ Checklist Antes de Ejecutar

- [ ] Python 3.7+ instalado
- [ ] Librería `requests` instalada
- [ ] Leí `00_LEEME_PRIMERO.txt`
- [ ] Leí `BINS_POR_AMBIENTE.md` (CRÍTICO)
- [ ] Identifiqué el ambiente a probar (DEV/SANDBOX/QA/PROD)
- [ ] Tengo las credenciales del merchant (Merchant Code + Public Key)
- [ ] El ambiente está activo y accesible

---

## 📈 Recomendaciones de Uso

### Para Desarrollo:
✅ Usar **DEV** - Ambiente estable, 10 BINs validados

### Para QA/Testing:
✅ Usar **QA** - Ambiente estable, mismos BINs que DEV

### Para Pruebas de Integración:
⚠️ Usar **SANDBOX** - Verificar estabilidad primero

### Para Producción:
⚠️ Usar **PRODUCCIÓN** - NO ejecutar test CPI-004 sin autorización

---

## 🎉 ¡Listo para Empezar!

1. Lee `00_LEEME_PRIMERO.txt`
2. Lee `BINS_POR_AMBIENTE.md`
3. Ejecuta `python test_suite_completo.py`
4. Revisa el informe generado

---

## 📌 Información del Paquete

- **Versión**: 1.0
- **Fecha**: 2025-11-07
- **Ambientes validados**: DEV ✅, QA ✅, SANDBOX ⚠️
- **Total de tests**: 7 casos de prueba
- **Última actualización**: 2025-11-07

---

**NOTA FINAL**: Si encuentras errores en SANDBOX, revisa primero `BINS_POR_AMBIENTE.md` y `SOLUCION_ERRORES_BINS.txt`. El ambiente SANDBOX actualmente presenta inestabilidad. Para pruebas confiables, usa DEV o QA.

---

Creado por: Equipo de Automatización QA - Izipay
Contacto: [Tu contacto aquí]
