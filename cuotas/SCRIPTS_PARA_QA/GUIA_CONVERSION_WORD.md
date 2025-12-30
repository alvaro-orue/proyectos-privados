# Guía de Conversión Automática a Word

## Descripción

El script maestro (`test_suite_completo.py`) ahora convierte automáticamente los informes Markdown (.md) a formato Word (.docx) usando Pandoc, eliminando la necesidad de ejecutar comandos manuales.

---

## ✅ Configuración Inicial (Una sola vez)

### Paso 1: Instalar Pandoc

#### Windows (Recomendado)
```bash
winget install JohnMacFarlane.Pandoc
```

#### Alternativa Windows (Chocolatey)
```bash
choco install pandoc
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install pandoc
```

#### macOS
```bash
brew install pandoc
```

### Paso 2: Verificar Instalación
```bash
pandoc --version
```

**Salida esperada:**
```
pandoc 3.x.x
Features: +server +lua
Scripting engine: Lua 5.4
...
```

### Paso 3: Reiniciar Terminal
Después de instalar Pandoc, **cierra y vuelve a abrir** tu terminal para que los cambios surtan efecto.

---

## 🚀 Uso del Script Maestro

### Ejecución Normal
```bash
cd SCRIPTS_PARA_QA
python test_suite_completo.py
```

El script automáticamente:
1. ✅ Ejecuta los 7 casos de prueba
2. ✅ Genera informe Markdown (.md)
3. ✅ **Convierte automáticamente a Word (.docx)**
4. ✅ Genera resultados JSON (.json)

### Archivos Generados

Después de ejecutar el script, encontrarás 3 archivos:

```
SCRIPTS_PARA_QA/
├── INFORME_PRUEBAS_DEV_20251110_123045.md     ← Informe Markdown
├── INFORME_PRUEBAS_DEV_20251110_123045.docx   ← Informe Word (NUEVO)
└── RESULTADOS_PRUEBAS_DEV_20251110_123045.json ← Datos JSON
```

---

## 📊 Escenarios y Salidas

### Escenario 1: Pandoc Instalado ✅

**Ejecución:**
```bash
python test_suite_completo.py
```

**Salida:**
```
📄 GENERANDO INFORME
======================================================================

✅ Informe Markdown generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.md

📄 Convirtiendo MD a DOCX usando pandoc...

✅ Informe Word generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.docx

   📁 C:\...\RESULTADOS_PRUEBAS_DEV_20251110_123045.json
```

**Resultado:** ✅ Tienes 3 archivos (MD, DOCX, JSON)

---

### Escenario 2: Pandoc NO Instalado ⚠️

**Ejecución:**
```bash
python test_suite_completo.py
```

**Salida:**
```
📄 GENERANDO INFORME
======================================================================

✅ Informe Markdown generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.md

📄 Convirtiendo MD a DOCX usando pandoc...

⚠️  No se pudo generar el archivo Word:
   ❌ Pandoc no está instalado.
   📥 Para instalarlo, ejecuta:
      winget install JohnMacFarlane.Pandoc
   Después, reinicia tu terminal y vuelve a ejecutar este script.
   💡 Puedes convertirlo manualmente con:
      pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o INFORME_PRUEBAS_DEV_20251110_123045.docx

   📁 C:\...\RESULTADOS_PRUEBAS_DEV_20251110_123045.json
```

**Resultado:** ⚠️ Tienes 2 archivos (MD, JSON). Para obtener el DOCX:
1. Instala Pandoc con el comando proporcionado
2. Reinicia tu terminal
3. Ejecuta el comando manual de conversión mostrado

---

### Escenario 3: Error de Conversión ❌

**Posibles causas:**
- Archivo MD corrupto
- Permisos insuficientes
- Disco lleno
- Pandoc instalado pero no en PATH

**Salida:**
```
📄 GENERANDO INFORME
======================================================================

✅ Informe Markdown generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.md

📄 Convirtiendo MD a DOCX usando pandoc...

⚠️  No se pudo generar el archivo Word:
   ❌ Error en conversión: [mensaje de error específico]
   💡 Puedes convertirlo manualmente con:
      pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o INFORME_PRUEBAS_DEV_20251110_123045.docx

   📁 C:\...\RESULTADOS_PRUEBAS_DEV_20251110_123045.json
```

**Solución:** Ejecuta el comando manual proporcionado para ver el error detallado de Pandoc.

---

## 🔧 Conversión Manual (Si es necesario)

Si la conversión automática falla o quieres convertir un informe antiguo:

### Comando Básico
```bash
pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o INFORME_PRUEBAS_DEV_20251110_123045.docx
```

### Con Opciones Adicionales

#### Agregar tabla de contenidos
```bash
pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o output.docx --toc
```

#### Especificar plantilla
```bash
pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o output.docx --reference-doc=plantilla.docx
```

#### Ajustar nivel de encabezados
```bash
pandoc INFORME_PRUEBAS_DEV_20251110_123045.md -o output.docx --shift-heading-level-by=1
```

---

## 🛠️ Troubleshooting

### Problema 1: "pandoc: command not found"

**Causa:** Pandoc no está instalado o no está en PATH.

**Solución:**
```bash
# 1. Instalar Pandoc
winget install JohnMacFarlane.Pandoc

# 2. Reiniciar terminal

# 3. Verificar instalación
pandoc --version
```

---

### Problema 2: Conversión exitosa pero DOCX no se abre

**Causa:** Posible corrupción durante la conversión.

**Solución:**
```bash
# Intentar con configuración específica
pandoc archivo.md -o archivo.docx -f markdown -t docx
```

---

### Problema 3: El script se demora mucho en convertir

**Causa:** Archivo MD muy grande (>5MB) o muchas imágenes.

**Solución:**
- ✅ Es normal, Pandoc puede demorar 5-10 segundos con archivos grandes
- ✅ El script muestra "Convirtiendo MD a DOCX usando pandoc..." mientras trabaja
- ✅ Espera pacientemente hasta que complete

---

### Problema 4: Caracteres especiales no aparecen correctamente en DOCX

**Causa:** Codificación incorrecta.

**Solución:**
```bash
# Especificar codificación UTF-8 explícitamente
pandoc archivo.md -o archivo.docx --metadata charset=UTF-8
```

---

## 📝 Preguntas Frecuentes

### ¿Es obligatorio instalar Pandoc?
**No.** El script funciona perfectamente sin Pandoc. Si Pandoc no está instalado:
- ✅ Se generará el informe Markdown (.md)
- ✅ Se generarán los resultados JSON (.json)
- ❌ No se generará el archivo Word (.docx)
- ✅ El script te indicará cómo instalarlo

### ¿Puedo usar el script sin internet?
**Sí.** Una vez que Pandoc está instalado, la conversión se realiza completamente offline. No requiere conexión a internet.

### ¿Puedo personalizar el formato del DOCX?
**Sí.** Puedes crear una plantilla de Word con los estilos que prefieras y usarla con Pandoc:
```bash
pandoc archivo.md -o archivo.docx --reference-doc=mi_plantilla.docx
```

### ¿El script se detiene si la conversión falla?
**No.** El script continúa normalmente y genera los otros archivos (MD y JSON). Solo muestra un mensaje informativo sobre el error de conversión.

### ¿Puedo convertir informes antiguos que se generaron antes?
**Sí.** Usa el comando manual:
```bash
pandoc INFORME_ANTIGUO.md -o INFORME_ANTIGUO.docx
```

---

## 🎯 Ventajas de la Conversión Automática

| Antes (Manual) | Ahora (Automático) |
|----------------|-------------------|
| 1. Ejecutar script | 1. Ejecutar script |
| 2. **Copiar ruta del MD** | 2. ✅ ¡Listo! |
| 3. **Ejecutar comando pandoc** | |
| 4. **Verificar archivo generado** | |
| **Total: 4 pasos** | **Total: 1 paso** |

**Tiempo ahorrado:** ~30 segundos por ejecución

**Errores eliminados:**
- ❌ Olvidar ejecutar la conversión
- ❌ Error en la ruta del archivo
- ❌ Error de sintaxis en el comando pandoc
- ❌ Perder la ruta del archivo MD generado

---

## 📦 Archivos Relacionados

| Archivo | Propósito |
|---------|-----------|
| `test_suite_completo.py` | Script maestro con conversión automática |
| `test_pandoc_conversion.py` | Test de verificación de Pandoc |
| `CHANGELOG_ACTUALIZACIONES.md` | Registro de cambios versión 2.1 |
| `GUIA_CONVERSION_WORD.md` | Esta guía |

---

## 🚀 Inicio Rápido (3 Pasos)

```bash
# 1. Instalar Pandoc (solo una vez)
winget install JohnMacFarlane.Pandoc

# 2. Reiniciar terminal
# (Cerrar y volver a abrir)

# 3. Ejecutar script
cd SCRIPTS_PARA_QA
python test_suite_completo.py
```

**¡Listo!** Ahora tienes informes en MD, DOCX y JSON automáticamente.

---

**Fecha:** 2025-11-10
**Versión del script:** 2.1
**Estado:** ✅ DOCUMENTACIÓN COMPLETA
