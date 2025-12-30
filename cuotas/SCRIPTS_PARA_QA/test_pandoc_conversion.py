"""
Test de la función de conversión Pandoc
Verifica que la función convertir_md_a_docx() funciona correctamente
"""
import subprocess
import sys
import os

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


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
        except subprocess.CalledProcessError:
            error_msg = "Pandoc está instalado pero no responde correctamente."
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


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEST DE CONVERSIÓN PANDOC - MD a DOCX")
    print("=" * 70)

    # Crear un archivo MD de prueba
    test_md = "test_conversion_temp.md"

    print(f"\n📝 Creando archivo de prueba: {test_md}")
    with open(test_md, 'w', encoding='utf-8') as f:
        f.write("""# Informe de Prueba

## Sección 1
Este es un test de conversión de Markdown a Word.

### Subsección 1.1
- Item 1
- Item 2
- Item 3

## Sección 2
Texto con **negrita** y *cursiva*.

```json
{
  "test": "example",
  "number": 123
}
```

## Conclusión
✅ Test completado exitosamente.
""")

    print(f"✅ Archivo creado: {os.path.abspath(test_md)}")

    # Intentar conversión
    print("\n" + "=" * 70)
    print("EJECUTANDO CONVERSIÓN")
    print("=" * 70)

    success, docx_file, error_msg = convertir_md_a_docx(test_md)

    print("\n" + "=" * 70)
    print("RESULTADO")
    print("=" * 70)

    if success:
        print(f"\n✅ CONVERSIÓN EXITOSA")
        print(f"   📁 Archivo MD:   {os.path.abspath(test_md)}")
        print(f"   📁 Archivo DOCX: {os.path.abspath(docx_file)}")
        print(f"\n💡 Puedes abrir el archivo DOCX para verificar el resultado.")

        # Limpiar archivos de prueba
        print(f"\n🧹 Limpiando archivos de prueba...")
        try:
            os.remove(test_md)
            print(f"   ✅ {test_md} eliminado")
        except:
            pass

        try:
            os.remove(docx_file)
            print(f"   ✅ {docx_file} eliminado")
        except:
            pass

    else:
        print(f"\n❌ CONVERSIÓN FALLÓ")
        print(f"   Error: {error_msg}")
        print(f"\n💡 Si pandoc no está instalado:")
        print(f"   1. Ejecuta: winget install JohnMacFarlane.Pandoc")
        print(f"   2. Reinicia tu terminal")
        print(f"   3. Vuelve a ejecutar este test")

        # Limpiar archivo MD de prueba
        try:
            os.remove(test_md)
        except:
            pass

    print("\n" + "=" * 70)
