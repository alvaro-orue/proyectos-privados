@echo off
echo ========================================
echo Instalador de Exportador a Word
echo ========================================
echo.
echo Instalando python-docx...
pip install python-docx
echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo Instalacion completada con exito!
    echo ========================================
    echo.
    echo Ahora puedes convertir Markdown a Word con:
    echo   python markdown_to_word.py archivo.md
    echo.
    echo O convertir todos los archivos .md:
    echo   python markdown_to_word.py -d .
    echo.
) else (
    echo ========================================
    echo Error en la instalacion
    echo ========================================
    echo Verifica tu conexion a internet e intenta nuevamente
)
echo.
pause
