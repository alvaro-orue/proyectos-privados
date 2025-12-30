# Changelog - Actualizaciones del Script Maestro

## Versión 2.1 (2025-11-10)

### ✅ Nuevas Funcionalidades

#### 1. Conversión Automática a Word (DOCX)
**Descripción:** El script ahora convierte automáticamente los informes Markdown a formato Word (.docx) usando Pandoc.

**Características:**
- ✅ Conversión automática después de generar el informe MD
- ✅ Detección automática de Pandoc instalado
- ✅ Mensajes de error informativos si Pandoc no está instalado
- ✅ Ejecución silenciosa en Windows (sin ventana de consola)
- ✅ Fallback manual si la conversión falla
- ✅ No detiene el script si la conversión falla

**Uso:**
```bash
# Simplemente ejecuta el script como siempre
python test_suite_completo.py

# El script automáticamente generará:
# 1. INFORME_PRUEBAS_DEV_20251110_123045.md
# 2. INFORME_PRUEBAS_DEV_20251110_123045.docx  <- NUEVO
# 3. RESULTADOS_PRUEBAS_DEV_20251110_123045.json
```

**Salida cuando Pandoc está instalado:**
```
✅ Informe Markdown generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.md

📄 Convirtiendo MD a DOCX usando pandoc...

✅ Informe Word generado exitosamente:
   📁 C:\...\INFORME_PRUEBAS_DEV_20251110_123045.docx
```

**Salida cuando Pandoc NO está instalado:**
```
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
```

#### 2. Informes con Detalles Completos
**Descripción:** Los informes ahora incluyen todos los detalles de requests y responses como en la versión anterior.

**Contenido de los informes:**
- ✅ Objetivos de cada caso de prueba
- ✅ Request Headers completos
- ✅ Request Body completos
- ✅ Response Body completos
- ✅ Response Headers relevantes (Content-Type, Authorization)
- ✅ Transaction IDs utilizados
- ✅ Duración de cada paso en milisegundos
- ✅ Ejemplos de requests/responses en la sección de Endpoints

**Ejemplo de detalle por paso:**
```markdown
#### Paso 1 - Generar Token
**Endpoint:** `POST https://testapi-pw.izipay.pe/security/v1/Token/Generate`
**Status:** 200
**Duración:** 450ms

**Request Headers:**
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "transactionId": "DEV20251110120000"
}
```

**Request Body:**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20251110120000",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "100.00"
}
```

**Response Body:**
```json
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
```

### 🔧 Mejoras Técnicas

#### 1. Función `convertir_md_a_docx()`
**Ubicación:** Líneas 1136-1195 en `test_suite_completo.py`

**Características:**
- Verifica si Pandoc está instalado antes de intentar conversión
- Usa `subprocess.CREATE_NO_WINDOW` en Windows para ejecución silenciosa
- Captura y reporta errores detallados
- Retorna tupla: `(success: bool, archivo_docx: str, error_message: str)`

**Código:**
```python
def convertir_md_a_docx(archivo_md):
    """
    Convierte un archivo Markdown a Word (DOCX) usando pandoc

    Args:
        archivo_md (str): Ruta al archivo .md

    Returns:
        tuple: (success: bool, archivo_docx: str, error_message: str)
    """
    try:
        archivo_docx = archivo_md.replace('.md', '.docx')

        # Verificar si pandoc está instalado
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            subprocess.run(
                ['pandoc', '--version'],
                capture_output=True,
                check=True,
                creationflags=creationflags
            )
        except FileNotFoundError:
            error_msg = (
                "Pandoc no está instalado.\n"
                "   📥 Para instalarlo, ejecuta:\n"
                "      winget install JohnMacFarlane.Pandoc\n"
                "   Después, reinicia tu terminal y vuelve a ejecutar este script."
            )
            return (False, None, error_msg)

        # Ejecutar conversión
        print(f"\n📄 Convirtiendo MD a DOCX usando pandoc...")
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        result = subprocess.run(
            ['pandoc', archivo_md, '-o', archivo_docx],
            capture_output=True,
            text=True,
            creationflags=creationflags
        )

        if result.returncode == 0:
            return (True, archivo_docx, None)
        else:
            error_msg = result.stderr if result.stderr else "Error desconocido en la conversión"
            return (False, None, f"Error en conversión: {error_msg}")

    except Exception as e:
        return (False, None, f"Excepción durante conversión: {str(e)}")
```

#### 2. Integración en `main()`
**Ubicación:** Líneas 1365-1375 en `test_suite_completo.py`

**Código:**
```python
# Convertir automáticamente a DOCX usando Pandoc
success_docx, archivo_docx, error_docx = convertir_md_a_docx(nombre_archivo)

if success_docx:
    print(f"\n✅ Informe Word generado exitosamente:")
    print(f"   📁 {os.path.abspath(archivo_docx)}")
else:
    print(f"\n⚠️  No se pudo generar el archivo Word:")
    print(f"   ❌ {error_docx}")
    print(f"   💡 Puedes convertirlo manualmente con:")
    print(f"      pandoc {nombre_archivo} -o {nombre_archivo.replace('.md', '.docx')}")
```

### 📦 Nuevos Archivos

#### 1. `test_pandoc_conversion.py`
**Descripción:** Script de prueba para verificar que la conversión Pandoc funciona correctamente.

**Uso:**
```bash
python test_pandoc_conversion.py
```

**Propósito:**
- Verificar que Pandoc está instalado
- Probar la función de conversión con un archivo MD de ejemplo
- Validar que la conversión genera un archivo DOCX válido
- Limpiar archivos de prueba automáticamente

### 🛠️ Instalación de Pandoc

#### Windows (Recomendado - usando winget)
```bash
winget install JohnMacFarlane.Pandoc
```

#### Windows (Alternativo - usando Chocolatey)
```bash
choco install pandoc
```

#### Windows (Alternativo - Descarga manual)
1. Visita: https://pandoc.org/installing.html
2. Descarga el instalador para Windows
3. Ejecuta el instalador
4. Reinicia tu terminal

#### Linux (Ubuntu/Debian)
```bash
sudo apt install pandoc
```

#### macOS
```bash
brew install pandoc
```

#### Verificar instalación
```bash
pandoc --version
```

### 📊 Comparación de Versiones

| Característica | v2.0 | v2.1 (NUEVA) |
|----------------|------|--------------|
| **Generación de informe MD** | ✅ | ✅ |
| **Generación de informe JSON** | ✅ | ✅ |
| **Conversión a DOCX** | ❌ Manual | ✅ **Automática** |
| **Detección de Pandoc** | ❌ | ✅ |
| **Mensajes de error informativos** | ❌ | ✅ |
| **Fallback manual** | ❌ | ✅ |
| **Ejecución silenciosa (Windows)** | ❌ | ✅ |
| **Detalles completos en informe** | ⚠️ Parcial | ✅ **Completo** |
| **Request Headers** | ❌ | ✅ |
| **Request Body** | ✅ | ✅ |
| **Response Body** | ✅ | ✅ |
| **Response Headers** | ❌ | ✅ |
| **Objetivos por test** | ❌ | ✅ |
| **Transaction IDs** | ⚠️ Parcial | ✅ **Completo** |

### 🚀 Flujo de Ejecución Actualizado

```
1. Usuario ejecuta: python test_suite_completo.py
   ↓
2. Selecciona ambiente (DEV/SANDBOX/QA/PROD)
   ↓
3. Ingresa credenciales (Merchant Code, Public Key)
   ↓
4. Ejecuta 7 casos de prueba (CPI-001 a CPI-007)
   ↓
5. Genera informe Markdown
   ↓
6. [NUEVO] Verifica si Pandoc está instalado
   ↓
7a. Si Pandoc está instalado:
    - Convierte MD a DOCX automáticamente
    - Muestra ruta del archivo DOCX
   ↓
7b. Si Pandoc NO está instalado:
    - Muestra mensaje informativo
    - Proporciona comando de instalación
    - Proporciona comando manual de conversión
   ↓
8. Genera resultados JSON
   ↓
9. Muestra resumen final
```

### ✅ Tests Realizados

#### Test 1: Conversión Pandoc
```bash
python test_pandoc_conversion.py
```
**Resultado:** ✅ EXITOSO - Conversión funciona correctamente

#### Test 2: Script Maestro
```bash
python test_suite_completo.py --help
```
**Resultado:** ✅ EXITOSO - Script carga sin errores

### 📝 Notas de Compatibilidad

- ✅ Compatible con Windows, Linux, macOS
- ✅ Requiere Python 3.6+
- ✅ Requiere módulo `requests`
- ✅ Pandoc es **opcional** (el script funciona sin él, solo no genera DOCX)
- ✅ Si Pandoc no está instalado, el script continúa normalmente y solo genera MD + JSON

### 🔜 Próximas Mejoras (Futuras)

- [ ] Soporte para exportar a PDF
- [ ] Configuración de estilos personalizados en DOCX
- [ ] Gráficos de estadísticas en el informe
- [ ] Comparación entre ejecuciones

---

**Fecha:** 2025-11-10
**Versión:** 2.1
**Autor:** Automatización QA - Izipay
**Estado:** ✅ LISTO PARA PRODUCCIÓN
