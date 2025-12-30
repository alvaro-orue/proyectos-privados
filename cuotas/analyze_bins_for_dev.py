"""
Analiza los BINs disponibles y genera configuración para ambiente DEV
"""

import pandas as pd
import json
from pathlib import Path

def analyze_bins():
    """
    Analiza los archivos Excel y genera información de BINs para DEV
    """
    base_path = Path(__file__).parent / "CASOS_MULTI_AMBIENTE"
    bin_file = base_path / "Results_dbo.bin"

    # Leer archivo
    df = pd.read_excel(bin_file)

    print(f"\n{'='*80}")
    print("ANÁLISIS DE BINS DISPONIBLES PARA AMBIENTE DEV")
    print(f"{'='*80}")

    # Obtener BINs de 6 dígitos (los más comunes)
    df_6_digits = df[df['bin'] < 1000000]

    print(f"\nTotal de BINs en base de datos: {len(df)}")
    print(f"BINs de 6 dígitos: {len(df_6_digits)}")
    print(f"BINs de más de 6 dígitos: {len(df) - len(df_6_digits)}")

    # Agrupar por banco
    print(f"\n{'='*80}")
    print("BINS POR BANCO (6 dígitos)")
    print(f"{'='*80}")

    banco_groups = df_6_digits.groupby('Banco')

    bins_by_bank = {}
    for banco, group in banco_groups:
        bins_by_bank[banco] = sorted(group['bin'].tolist())
        print(f"\n{banco}:")
        print(f"  Total BINs: {len(group)}")
        print(f"  BINs: {', '.join(map(str, sorted(group['bin'].tolist())[:10]))}")
        if len(group) > 10:
            print(f"  ... y {len(group) - 10} más")

    # Analizar BINs específicos que estaban en las pruebas
    print(f"\n{'='*80}")
    print("VERIFICACIÓN DE BINS DE PRUEBA")
    print(f"{'='*80}")

    test_bins = {
        "545545": "SCOTIABANK (en pruebas actuales)",
        "411111": "VISA TEST (en pruebas actuales)",
        "424242": "VISA TEST (en pruebas actuales)",
        "552277": "MASTERCARD TEST (en pruebas actuales)"
    }

    for bin_num, description in test_bins.items():
        bin_int = int(bin_num)
        if bin_int in df['bin'].values:
            bin_data = df[df['bin'] == bin_int].iloc[0]
            print(f"\n[OK] {bin_num} - {description}")
            print(f"   Banco: {bin_data['Banco']}")
            print(f"   Cuotas: {bin_data['cuotas']}")
            print(f"   Meses diferido: {bin_data['meses']}")
        else:
            print(f"\n[NO] {bin_num} - {description}")
            print(f"   NO EXISTE en la base de datos")

    # Sugerir BINs para pruebas por tipo de tarjeta
    print(f"\n{'='*80}")
    print("BINS SUGERIDOS PARA PRUEBAS DEV")
    print(f"{'='*80}")

    # BINs de diferentes bancos para tener variedad
    suggested_bins = []

    # SCOTIABANK (ya funciona)
    scotiabank = df_6_digits[df_6_digits['Banco'].str.contains('SCOTIA', na=False)]
    if len(scotiabank) > 0:
        bin_545545 = scotiabank[scotiabank['bin'] == 545545]
        if len(bin_545545) > 0:
            suggested_bins.append({
                'bin': '545545',
                'banco': bin_545545.iloc[0]['Banco'],
                'cuotas': int(bin_545545.iloc[0]['cuotas']),
                'meses': int(bin_545545.iloc[0]['meses']),
                'tipo': 'Mastercard'
            })

    # BCP (Banco de Crédito del Perú)
    bcp = df_6_digits[df_6_digits['Banco'].str.contains('BCP|CREDITO', na=False)]
    if len(bcp) > 0:
        bcp_sample = bcp.iloc[0]
        suggested_bins.append({
            'bin': str(bcp_sample['bin']),
            'banco': bcp_sample['Banco'],
            'cuotas': int(bcp_sample['cuotas']),
            'meses': int(bcp_sample['meses']),
            'tipo': 'Visa/Mastercard'
        })

    # INTERBANK
    interbank = df_6_digits[df_6_digits['Banco'].str.contains('INTER', na=False)]
    if len(interbank) > 0:
        inter_sample = interbank.iloc[0]
        suggested_bins.append({
            'bin': str(inter_sample['bin']),
            'banco': inter_sample['Banco'],
            'cuotas': int(inter_sample['cuotas']),
            'meses': int(inter_sample['meses']),
            'tipo': 'Visa/Mastercard'
        })

    # BBVA
    bbva = df_6_digits[df_6_digits['Banco'].str.contains('BBVA', na=False)]
    if len(bbva) > 0:
        bbva_sample = bbva.iloc[0]
        suggested_bins.append({
            'bin': str(bbva_sample['bin']),
            'banco': bbva_sample['Banco'],
            'cuotas': int(bbva_sample['cuotas']),
            'meses': int(bbva_sample['meses']),
            'tipo': 'Visa/Mastercard'
        })

    # American Express
    amex = df_6_digits[df_6_digits['Banco'].str.contains('AMERICAN|AMEX', na=False)]
    if len(amex) > 0:
        amex_sample = amex.iloc[0]
        suggested_bins.append({
            'bin': str(amex_sample['bin']),
            'banco': amex_sample['Banco'],
            'cuotas': int(amex_sample['cuotas']),
            'meses': int(amex_sample['meses']),
            'tipo': 'American Express'
        })

    print("\nBINs recomendados para config_environments.py:\n")
    print("bins_disponibles = [")
    for bin_info in suggested_bins:
        print(f'    "{bin_info["bin"]}",  # {bin_info["banco"]} - {bin_info["cuotas"]} cuotas, {bin_info["meses"]} meses diferido')
    print("]")

    # Guardar configuración en JSON
    output_file = base_path / "DEV" / "bins_recomendados.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    config_output = {
        "fecha_generacion": "2025-11-04",
        "total_bins_db": len(df),
        "bins_recomendados": suggested_bins,
        "bins_prueba_anteriores": {
            "545545": "EXISTE - SCOTIABANK",
            "411111": "NO EXISTE",
            "424242": "NO EXISTE",
            "552277": "NO EXISTE"
        },
        "bancos_disponibles": list(bins_by_bank.keys())
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config_output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Configuracion guardada en: {output_file}")

    # Mostrar todos los BINs disponibles por banco
    print(f"\n{'='*80}")
    print("LISTADO COMPLETO DE BINS POR BANCO (primeros 5 de cada uno)")
    print(f"{'='*80}")

    for banco in sorted(bins_by_bank.keys()):
        bins = bins_by_bank[banco]
        print(f"\n{banco} ({len(bins)} BINs):")
        for bin_num in bins[:5]:
            bin_data = df_6_digits[df_6_digits['bin'] == bin_num].iloc[0]
            print(f"  {bin_num}: {bin_data['cuotas']} cuotas, diferido {bin_data['meses']} meses")

if __name__ == "__main__":
    analyze_bins()
