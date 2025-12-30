# 📄 Cómo Exportar Informes de Markdown a Word

## 🎯 Funcionalidad

Los scripts generan informes en formato Markdown (`.md`). Esta guía te muestra cómo **convertirlos automáticamente a Word** (`.docx`) para facilitar su distribución y edición.

---

## ⚡ Opción 1: Conversión Automática (RECOMENDADO)

### Paso 1: Instalar Dependencia

```bash
pip install python-docx
```

### Paso 2: Convertir Markdown a Word

#### 2A. Convertir UN archivo específico:
```bash
python markdown_to_word.py INFORME_PRUEBAS_DEV_20251107.md
```

**Resultado**: Se generará `INFORME_PRUEBAS_DEV_20251107.docx` en la misma carpeta

#### 2B. Convertir TODOS los archivos .md en la carpeta:
```bash
python markdown_to_word.py -d .
```

**Resultado**: Todos los `.md` en la carpeta actual se convertirán a `.docx`

#### 2C. Especificar nombre de salida:
```bash
python markdown_to_word.py informe.md -o mi_informe_personalizado.docx
```

---

## 🔧 Opción 2: Usar Pandoc (Alternativa)

Si prefieres usar Pandoc (herramienta externa muy potente):

### Paso 1: Instalar Pandoc
Descargar de: https://pandoc.org/installing.html

### Paso 2: Convertir
```bash
pandoc informe.md -o informe.docx
```

---

## 📝 Ejemplos de Uso Práctico

### Ejemplo 1: Después de ejecutar el script maestro
```bash
# 1. Ejecutar tests
python test_suite_completo.py

# 2. Convertir el informe generado a Word
python markdown_to_word.py INFORME_PRUEBAS_SANDBOX_20251107_001234.md

# 3. Abrir el archivo Word
# El archivo .docx estará en la misma carpeta
```

### Ejemplo 2: Convertir toda la documentación
```bash
# Convertir todos los archivos .md del proyecto
python markdown_to_word.py -d . -r

# Resultado: Todos los .md se convierten a .docx:
# - README.md → README.docx
# - BINS_POR_AMBIENTE.md → BINS_POR_AMBIENTE.docx
# - INSTRUCCIONES_SUITE_COMPLETA.md → INSTRUCCIONES_SUITE_COMPLETA.docx
# - etc.
```

### Ejemplo 3: Integrar en el script maestro

Si quieres que el script maestro convierta automáticamente a Word, agrega al final del `test_suite_completo.py`:

```python
# Al final del script, después de generar el .md
try:
    from markdown_to_word import markdown_to_word
    docx_file = markdown_to_word(informe_md_path)
    print(f"✅ Informe Word generado: {docx_file}")
except ImportError:
    print("⚠️  Para exportar a Word, instalar: pip install python-docx")
except Exception as e:
    print(f"⚠️  No se pudo generar Word: {e}")
```

---

## 🎨 Formato del Documento Word Generado

El documento Word incluirá:

✅ **Títulos con jerarquía**
- # Título → Heading 1 (azul, centrado)
- ## Título → Heading 2 (azul medio)
- ### Título → Heading 3 (azul claro)

✅ **Tablas formateadas**
- Encabezados con fondo azul
- Bordes automáticos
- Estilos profesionales

✅ **Listas**
- Viñetas (bullet points)
- Numeradas

✅ **Bloques de código**
- Fondo gris
- Fuente monoespaciada
- Texto azul

✅ **Emojis y símbolos**
- Se mantienen en el documento

---

## ❓ Problemas Comunes

### Error: "Module 'docx' not found"
```bash
pip install python-docx
```

### Error: "Permission denied" al guardar
Cerrar el archivo Word si está abierto antes de convertir

### Las tablas no se ven bien
La conversión es automática pero puede requerir ajustes manuales en Word para tablas muy complejas

### Los emojis no se ven
Depende de la fuente usada en Word. Usar fuentes con soporte Unicode (Segoe UI, Arial)

---

## 🚀 Automatización Completa

### Script Bash/PowerShell para automatizar todo:

**Windows (PowerShell)**:
```powershell
# ejecutar_y_exportar.ps1
python test_suite_completo.py
$ultimo_md = Get-ChildItem -Filter "INFORME_PRUEBAS_*.md" | Sort-Object LastWriteTime | Select-Object -Last 1
python markdown_to_word.py $ultimo_md.Name
Write-Host "✅ Informe Word generado"
```

**Linux/Mac (Bash)**:
```bash
# ejecutar_y_exportar.sh
python test_suite_completo.py
ultimo_md=$(ls -t INFORME_PRUEBAS_*.md | head -1)
python markdown_to_word.py "$ultimo_md"
echo "✅ Informe Word generado"
```

---

## 📊 Comparación de Opciones

| Característica | python-docx | pandoc |
|----------------|-------------|--------|
| Instalación | `pip install` | Instalador externo |
| Velocidad | Rápida | Muy rápida |
| Calidad tablas | Buena | Excelente |
| Control formato | Alto | Medio |
| Dependencias | Solo Python | Requiere Haskell |
| Tamaño | ~500KB | ~100MB |
| **Recomendado** | ✅ Sí | Para casos avanzados |

---

## 💡 Consejos

1. **Generar Word automáticamente**: Agregar la conversión al final del script maestro
2. **Revisar el Word**: Algunos formatos pueden requerir ajuste manual
3. **Mantener el Markdown**: Siempre guardar el `.md` original como respaldo
4. **Compartir ambos**: Enviar tanto `.md` como `.docx` al cliente

---

## 📞 Ayuda Adicional

### Documentación python-docx:
https://python-docx.readthedocs.io/

### Documentación pandoc:
https://pandoc.org/MANUAL.html

### Soporte:
Consultar con el equipo de desarrollo

---

## ✅ Checklist

- [ ] `pip install python-docx` ejecutado
- [ ] Script `markdown_to_word.py` en la carpeta
- [ ] Ejecutar tests y generar `.md`
- [ ] Convertir a Word con el comando
- [ ] Verificar que el `.docx` se abrió correctamente
- [ ] Compartir informe en Word con el equipo

---

**Última actualización**: 2025-11-07
**Versión**: 1.0
**Creado por**: Equipo de Automatización QA
