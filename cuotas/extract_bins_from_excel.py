"""
Script para extraer datos de BINs desde los archivos Excel
que contienen la información real de la base de datos
"""

import pandas as pd
import json
from pathlib import Path

def read_bin_file(file_path):
    """
    Lee el archivo Results_dbo.bin
    Asumiendo que es un archivo Excel renombrado a .bin
    """
    try:
        # Intentar leer como Excel
        df = pd.read_excel(file_path)
        print(f"\n{'='*60}")
        print(f"Archivo: {Path(file_path).name}")
        print(f"{'='*60}")
        print(f"Columnas: {list(df.columns)}")
        print(f"Total registros: {len(df)}")
        print(f"\nPrimeras 10 filas:")
        print(df.head(10))
        return df
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None

def read_binecn_file(file_path):
    """
    Lee el archivo Results_binEcn.xlsx
    """
    try:
        df = pd.read_excel(file_path)
        print(f"\n{'='*60}")
        print(f"Archivo: {Path(file_path).name}")
        print(f"{'='*60}")
        print(f"Columnas: {list(df.columns)}")
        print(f"Total registros: {len(df)}")
        print(f"\nPrimeras 10 filas:")
        print(df.head(10))
        return df
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None

def extract_bins_for_dev(df_bin, df_binecn):
    """
    Extrae los BINs disponibles para el ambiente DEV
    """
    bins_info = []

    # Analizar estructura de datos
    if df_bin is not None:
        print(f"\n{'='*60}")
        print("ANÁLISIS DE DATOS - Results_dbo.bin")
        print(f"{'='*60}")
        print("\nEstructura de datos:")
        print(df_bin.info())

        # Buscar columna que contenga BIN
        bin_columns = [col for col in df_bin.columns if 'bin' in col.lower()]
        print(f"\nColumnas con 'bin': {bin_columns}")

        if bin_columns:
            # Obtener BINs únicos
            bin_col = bin_columns[0]
            unique_bins = df_bin[bin_col].unique()
            print(f"\nBINs únicos encontrados ({len(unique_bins)}):")
            for bin_value in sorted(unique_bins):
                print(f"  - {bin_value}")

    if df_binecn is not None:
        print(f"\n{'='*60}")
        print("ANÁLISIS DE DATOS - Results_binEcn.xlsx")
        print(f"{'='*60}")
        print("\nEstructura de datos:")
        print(df_binecn.info())

        # Buscar columna que contenga BIN
        bin_columns = [col for col in df_binecn.columns if 'bin' in col.lower()]
        print(f"\nColumnas con 'bin': {bin_columns}")

        if bin_columns:
            # Obtener BINs únicos
            bin_col = bin_columns[0]
            unique_bins = df_binecn[bin_col].unique()
            print(f"\nBINs únicos encontrados ({len(unique_bins)}):")
            for bin_value in sorted(unique_bins):
                print(f"  - {bin_value}")

    return bins_info

def main():
    # Rutas a los archivos
    base_path = Path(__file__).parent / "CASOS_MULTI_AMBIENTE"
    bin_file = base_path / "Results_dbo.bin"
    binecn_file = base_path / "Results_binEcn.xlsx"

    print(f"\n{'='*60}")
    print("EXTRACCIÓN DE DATOS DE BINS DESDE EXCEL")
    print(f"{'='*60}")

    # Leer archivos
    df_bin = read_bin_file(bin_file)
    df_binecn = read_binecn_file(binecn_file)

    # Extraer información de BINs
    bins_info = extract_bins_for_dev(df_bin, df_binecn)

    print(f"\n{'='*60}")
    print("EXTRACCIÓN COMPLETADA")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
