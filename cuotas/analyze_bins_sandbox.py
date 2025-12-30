"""
Analiza los BINs disponibles en SANDBOX y genera configuración
"""

import pandas as pd
import json
from pathlib import Path

def analyze_bins_sandbox():
    """
    Analiza los archivos Excel de SANDBOX y genera información de BINs
    """
    base_path = Path(__file__).parent / "CASOS_MULTI_AMBIENTE"
    bin_file = base_path / "Results_dbobinSandBox.xlsx"
    binecn_file = base_path / "Results_binEcnSandBox.xlsx"

    print(f"\n{'='*80}")
    print("ANALISIS DE BINS DISPONIBLES PARA SANDBOX")
    print(f"{'='*80}")

    # Leer archivo principal
    try:
        df_bin = pd.read_excel(bin_file)
        print(f"\n[OK] Archivo Results_dbobinSandBox.xlsx leido")
        print(f"Total registros: {len(df_bin)}")
        print(f"Columnas: {list(df_bin.columns)}")
    except Exception as e:
        print(f"[ERROR] No se pudo leer Results_dbobinSandBox.xlsx: {e}")
        df_bin = None

    # Leer archivo ECN
    try:
        df_binecn = pd.read_excel(binecn_file)
        print(f"\n[OK] Archivo Results_binEcnSandBox.xlsx leido")
        print(f"Total registros: {len(df_binecn)}")
        print(f"Columnas: {list(df_binecn.columns)}")
    except Exception as e:
        print(f"[ERROR] No se pudo leer Results_binEcnSandBox.xlsx: {e}")
        df_binecn = None

    if df_bin is None:
        print("\n[ERROR] No se pudo continuar sin datos")
        return

    # Filtrar BINs de 6 dígitos
    df_6_digits = df_bin[df_bin['bin'] < 1000000]

    print(f"\n{'='*80}")
    print("ESTADISTICAS")
    print(f"{'='*80}")
    print(f"Total de BINs en SANDBOX: {len(df_bin)}")
    print(f"BINs de 6 digitos: {len(df_6_digits)}")
    print(f"BINs de mas de 6 digitos: {len(df_bin) - len(df_6_digits)}")

    # Agrupar por banco
    print(f"\n{'='*80}")
    print("BINS POR BANCO (6 digitos)")
    print(f"{'='*80}")

    banco_groups = df_6_digits.groupby('Banco')
    bins_by_bank = {}

    for banco, group in banco_groups:
        bins_by_bank[banco] = sorted(group['bin'].tolist())
        print(f"\n{banco}:")
        print(f"  Total BINs: {len(group)}")
        bins_list = sorted(group['bin'].tolist())[:5]
        print(f"  BINs: {', '.join(map(str, bins_list))}")
        if len(group) > 5:
            print(f"  ... y {len(group) - 5} mas")

    # Verificar BINs de prueba anteriores
    print(f"\n{'='*80}")
    print("VERIFICACION DE BINS CONFIGURADOS ACTUALMENTE")
    print(f"{'='*80}")

    current_bins = {
        "545545": "SCOTIABANK (configurado en DEV/QA)",
        "400917": "SCOTIABANK VISA (configurado en DEV/QA)",
        "377893": "BCP (configurado en DEV/QA)",
        "553650": "BBVA MC Platinum (configurado en DEV/QA)"
    }

    valid_bins_sandbox = []

    for bin_num, description in current_bins.items():
        bin_int = int(bin_num)
        if bin_int in df_bin['bin'].values:
            bin_data = df_bin[df_bin['bin'] == bin_int].iloc[0]
            print(f"\n[OK] {bin_num} - {description}")
            print(f"   Banco: {bin_data['Banco']}")
            print(f"   Cuotas: {bin_data['cuotas']}")
            print(f"   Meses diferido: {bin_data['meses']}")
            valid_bins_sandbox.append({
                'bin': bin_num,
                'banco': bin_data['Banco'],
                'cuotas': int(bin_data['cuotas']),
                'meses': int(bin_data['meses'])
            })
        else:
            print(f"\n[NO] {bin_num} - {description}")
            print(f"   NO EXISTE en la base de datos de SANDBOX")

    # Sugerir BINs para SANDBOX
    print(f"\n{'='*80}")
    print("BINS RECOMENDADOS PARA SANDBOX")
    print(f"{'='*80}")

    suggested_bins = []

    # Si los BINs actuales no existen, buscar alternativas
    if len(valid_bins_sandbox) < 4:
        print("\n[INFO] Buscando BINs alternativos en SANDBOX...")

        # Buscar SCOTIABANK
        scotiabank = df_6_digits[df_6_digits['Banco'].str.contains('SCOTIA', na=False, case=False)]
        if len(scotiabank) > 0:
            for idx, row in scotiabank.head(2).iterrows():
                suggested_bins.append({
                    'bin': str(row['bin']),
                    'banco': row['Banco'],
                    'cuotas': int(row['cuotas']),
                    'meses': int(row['meses']),
                    'tipo': 'Scotiabank'
                })

        # Buscar BCP
        bcp = df_6_digits[df_6_digits['Banco'].str.contains('BCP', na=False, case=False)]
        if len(bcp) > 0:
            suggested_bins.append({
                'bin': str(bcp.iloc[0]['bin']),
                'banco': bcp.iloc[0]['Banco'],
                'cuotas': int(bcp.iloc[0]['cuotas']),
                'meses': int(bcp.iloc[0]['meses']),
                'tipo': 'BCP'
            })

        # Buscar BBVA
        bbva = df_6_digits[df_6_digits['Banco'].str.contains('BBVA', na=False, case=False)]
        if len(bbva) > 0:
            suggested_bins.append({
                'bin': str(bbva.iloc[0]['bin']),
                'banco': bbva.iloc[0]['Banco'],
                'cuotas': int(bbva.iloc[0]['cuotas']),
                'meses': int(bbva.iloc[0]['meses']),
                'tipo': 'BBVA'
            })

        # Buscar Interbank
        interbank = df_6_digits[df_6_digits['Banco'].str.contains('INTER', na=False, case=False)]
        if len(interbank) > 0:
            suggested_bins.append({
                'bin': str(interbank.iloc[0]['bin']),
                'banco': interbank.iloc[0]['Banco'],
                'cuotas': int(interbank.iloc[0]['cuotas']),
                'meses': int(interbank.iloc[0]['meses']),
                'tipo': 'Interbank'
            })

    # Si hay BINs válidos de la configuración actual, usarlos
    if len(valid_bins_sandbox) > 0:
        for bin_info in valid_bins_sandbox:
            if bin_info not in suggested_bins:
                suggested_bins.append({
                    'bin': bin_info['bin'],
                    'banco': bin_info['banco'],
                    'cuotas': bin_info['cuotas'],
                    'meses': bin_info['meses'],
                    'tipo': bin_info['banco'].strip()
                })

    # Asegurar que tenemos al menos 10 BINs
    if len(suggested_bins) < 10:
        # Agregar más BINs variados
        remaining_needed = 10 - len(suggested_bins)
        existing_bins = set(b['bin'] for b in suggested_bins)

        for idx, row in df_6_digits.iterrows():
            if len(suggested_bins) >= 10:
                break
            bin_str = str(row['bin'])
            if bin_str not in existing_bins:
                suggested_bins.append({
                    'bin': bin_str,
                    'banco': row['Banco'],
                    'cuotas': int(row['cuotas']),
                    'meses': int(row['meses']),
                    'tipo': row['Banco'].strip()
                })
                existing_bins.add(bin_str)

    print("\nBINs recomendados para config_environments.py (SANDBOX):\n")
    print("bins_disponibles = [")
    for bin_info in suggested_bins[:10]:
        print(f'    "{bin_info["bin"]}",  # {bin_info["banco"]} - {bin_info["cuotas"]} cuotas, {bin_info["meses"]} meses diferido')
    print("]")

    # Guardar configuración
    output_file = base_path / "SANDBOX" / "bins_recomendados.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    config_output = {
        "fecha_generacion": "2025-11-04",
        "ambiente": "SANDBOX",
        "total_bins_db": len(df_bin),
        "bins_recomendados": suggested_bins[:10],
        "bins_actuales_dev_qa": {
            "545545": "EXISTE" if 545545 in df_bin['bin'].values else "NO EXISTE",
            "400917": "EXISTE" if 400917 in df_bin['bin'].values else "NO EXISTE",
            "377893": "EXISTE" if 377893 in df_bin['bin'].values else "NO EXISTE",
            "553650": "EXISTE" if 553650 in df_bin['bin'].values else "NO EXISTE"
        },
        "bancos_disponibles": list(bins_by_bank.keys())
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config_output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Configuracion guardada en: {output_file}")

    # Mostrar lista completa de BINs
    print(f"\n{'='*80}")
    print("PRIMEROS 20 BINS DISPONIBLES EN SANDBOX")
    print(f"{'='*80}")

    for idx, row in df_6_digits.head(20).iterrows():
        print(f"{row['bin']}: {row['Banco']} - {row['cuotas']} cuotas, {row['meses']} meses diferido")

if __name__ == "__main__":
    analyze_bins_sandbox()
