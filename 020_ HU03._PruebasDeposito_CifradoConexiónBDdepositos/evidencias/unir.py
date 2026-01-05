import os
from pypdf import PdfWriter

def unir_pdfs():
    escritor = PdfWriter()
    archivos_encontrados = []

    # 1. Buscar todos los PDFs en la carpeta actual
    for archivo in os.listdir('.'):
        if archivo.endswith('.pdf') and archivo != "Completo.pdf":
            archivos_encontrados.append(archivo)

    # 2. Ordenar alfabéticamente (importante para que el 001 vaya antes del 002)
    archivos_encontrados.sort()

    if not archivos_encontrados:
        print("No encontré archivos PDF en esta carpeta.")
        return

    print(f"Uniendo {len(archivos_encontrados)} archivos: {archivos_encontrados}")

    # 3. Unir
    for pdf in archivos_encontrados:
        escritor.append(pdf)

    # 4. Guardar
    with open("Completo.pdf", "wb") as salida:
        escritor.write(salida)

    print("¡Éxito! Se ha creado el archivo: Completo.pdf")

if __name__ == "__main__":
    unir_pdfs()