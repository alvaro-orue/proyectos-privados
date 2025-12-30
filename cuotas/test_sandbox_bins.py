"""
Script para probar diferentes BINs en SANDBOX
Identifica cuáles BINs están configurados
"""

import requests
import json
import time
import sys
import io
from datetime import datetime
from config_environments import get_environment

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# BINs de prueba comunes
TEST_BINS = [
    "545545",  # SCOTIABANK - Mastercard
    "411111",  # VISA TEST
    "424242",  # VISA TEST
    "552277",  # MASTERCARD TEST
    "450799",  # Otro VISA
    "542118",  # Otro Mastercard
]

def generate_transaction_id():
    now = datetime.now()
    return f"TESTBIN{now.strftime('%Y%m%d%H%M%S')}"

def generate_order_number():
    now = datetime.now()
    return f"ORDER{now.strftime('%Y%m%d%H%M%S')}"

def generate_token(config, transaction_id, order_number):
    """Genera token de sesión"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "transactionId": transaction_id
    }

    payload = {
        "requestSource": "ECOMMERCE",
        "merchantCode": config["merchant_code"],
        "orderNumber": order_number,
        "publicKey": config["public_key"],
        "amount": "100.00"
    }

    try:
        response = requests.post(
            config["token_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00":
                return data.get("response", {}).get("token")
    except:
        pass

    return None

def test_bin(config, token, transaction_id, bin_number):
    """Prueba un BIN específico"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "transactionId": transaction_id
    }

    payload = {
        "bin": bin_number,
        "merchantCode": config["merchant_code"],
        "language": "ESP"
    }

    start_time = time.time()

    try:
        response = requests.post(
            config["installments_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        duration_ms = (time.time() - start_time) * 1000

        data = response.json()

        return {
            "bin": bin_number,
            "status_code": response.status_code,
            "response_code": data.get("code"),
            "message": data.get("message"),
            "duration_ms": duration_ms,
            "success": response.status_code == 200 and data.get("code") == "00",
            "issuer": data.get("response", {}).get("issuerName") if data.get("code") == "00" else None,
            "installments_count": len(data.get("response", {}).get("installments", [])) if data.get("code") == "00" else 0,
            "error_message": data.get("errorMessage")
        }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        return {
            "bin": bin_number,
            "status_code": 0,
            "response_code": None,
            "message": str(e),
            "duration_ms": duration_ms,
            "success": False,
            "issuer": None,
            "installments_count": 0,
            "error_message": str(e)
        }

def main():
    print("=" * 80)
    print("PRUEBA DE BINs EN SANDBOX")
    print("=" * 80)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Obtener configuración de SANDBOX
    config = get_environment("SANDBOX")

    print(f"Ambiente: {config['name']}")
    print(f"Merchant Code: {config['merchant_code']}")
    print(f"URL: {config['installments_url'].split('/Installments')[0]}")
    print()

    # Generar token
    print("Generando token de sesión...")
    transaction_id = generate_transaction_id()
    order_number = generate_order_number()

    token = generate_token(config, transaction_id, order_number)

    if not token:
        print("❌ Error: No se pudo generar el token")
        return

    print(f"✅ Token generado: {token[:50]}...")
    print()

    # Probar cada BIN
    results = []
    print("=" * 80)
    print("PROBANDO BINs")
    print("=" * 80)
    print()

    for bin_number in TEST_BINS:
        print(f"Probando BIN: {bin_number}...", end=" ")

        result = test_bin(config, token, transaction_id, bin_number)
        results.append(result)

        if result["success"]:
            print(f"✅ {result['issuer']} - {result['installments_count']} cuotas ({result['duration_ms']:.0f}ms)")
        else:
            print(f"❌ Error {result['status_code']} - {result['response_code']} ({result['duration_ms']:.0f}ms)")

    # Resumen
    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print()

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"Total BINs probados: {len(results)}")
    print(f"✅ Exitosos: {len(successful)}")
    print(f"❌ Fallidos: {len(failed)}")
    print()

    if successful:
        print("BINs FUNCIONALES:")
        for r in successful:
            print(f"  • {r['bin']} - {r['issuer']} - {r['installments_count']} cuotas")
        print()

    if failed:
        print("BINs NO CONFIGURADOS:")
        for r in failed:
            error_msg = r.get('error_message', r.get('message', 'Unknown'))
            print(f"  • {r['bin']} - {error_msg}")

    # Guardar resultados
    output_file = "CASOS_MULTI_AMBIENTE/SANDBOX/results/bin_test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "test_date": datetime.now().isoformat(),
            "environment": "SANDBOX",
            "merchant_code": config["merchant_code"],
            "results": results,
            "summary": {
                "total": len(results),
                "successful": len(successful),
                "failed": len(failed)
            }
        }, f, indent=2, ensure_ascii=False)

    print()
    print(f"✅ Resultados guardados en: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
