"""
Script de prueba CPI-001: Flujo completo exitoso - Generar token y buscar cuotas
Ambiente: QA
Fecha: 2025-10-28
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración
CONFIG = {
    "token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
    "merchant_code": "4078370",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}

# Crear carpeta para resultados si no existe
RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestResult:
    def __init__(self):
        self.test_id = "CPI-001"
        self.test_name = "Flujo completo exitoso - Generar token y buscar cuotas"
        self.start_time = None
        self.end_time = None
        self.results = []
        self.passed = False
        self.error_message = None

    def add_step(self, step_name, success, data, duration_ms):
        self.results.append({
            "step": step_name,
            "success": success,
            "data": data,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self):
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": (self.end_time - self.start_time) * 1000 if self.start_time and self.end_time else 0,
            "passed": self.passed,
            "error_message": self.error_message,
            "steps": self.results
        }


def generate_transaction_id():
    """Genera un transactionId único"""
    return f"TXN{int(time.time() * 1000)}"


def generate_order_number():
    """Genera un orderNumber único"""
    return f"ORDER{int(time.time())}"


def generate_token(transaction_id, order_number):
    """
    PASO 1: Generar token de sesión
    """
    print("=" * 60)
    print("PASO 1: GENERAR TOKEN DE SESIÓN")
    print("=" * 60)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "transactionId": transaction_id
    }

    payload = {
        "requestSource": "ECOMMERCE",
        "merchantCode": CONFIG["merchant_code"],
        "orderNumber": order_number,
        "publicKey": CONFIG["public_key"],
        "amount": "100.00"
    }

    print(f"\n📤 Request URL: {CONFIG['token_url']}")
    print(f"📤 Headers: {json.dumps(headers, indent=2)}")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")

    start_time = time.time()

    try:
        response = requests.post(
            CONFIG["token_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        duration_ms = (time.time() - start_time) * 1000

        print(f"\n📥 Response Status: {response.status_code}")
        print(f"⏱️  Response Time: {duration_ms:.2f}ms")

        response_data = response.json()
        print(f"📥 Response Body: {json.dumps(response_data, indent=2)}")

        if response.status_code == 200 and response_data.get("code") == "00":
            token = response_data.get("response", {}).get("token")
            print(f"\n✅ Token generado exitosamente")
            print(f"🔑 Token (primeros 50 caracteres): {token[:50]}...")

            return {
                "success": True,
                "token": token,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "headers": dict(response.headers)
            }
        else:
            print(f"\n❌ Error al generar token")
            print(f"Código: {response_data.get('code')}")
            print(f"Mensaje: {response_data.get('message')}")

            return {
                "success": False,
                "error": f"Token generation failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }

    except requests.exceptions.RequestException as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f"\n❌ Excepción durante la solicitud: {str(e)}")

        return {
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms
        }


def search_installments(token, transaction_id, bin_number="545545"):
    """
    PASO 2: Buscar cuotas disponibles
    """
    print("\n" + "=" * 60)
    print("PASO 2: BUSCAR CUOTAS DISPONIBLES")
    print("=" * 60)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "transactionId": transaction_id
    }

    payload = {
        "bin": bin_number,
        "merchantCode": CONFIG["merchant_code"],
        "language": "ESP"
    }

    print(f"\n📤 Request URL: {CONFIG['installments_url']}")
    print(f"📤 Headers (Authorization truncado): {json.dumps({**headers, 'Authorization': f'Bearer {token[:30]}...'}, indent=2)}")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")

    start_time = time.time()

    try:
        response = requests.post(
            CONFIG["installments_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        duration_ms = (time.time() - start_time) * 1000

        print(f"\n📥 Response Status: {response.status_code}")
        print(f"⏱️  Response Time: {duration_ms:.2f}ms")

        response_data = response.json()
        print(f"📥 Response Body: {json.dumps(response_data, indent=2, ensure_ascii=False)}")

        if response.status_code == 200 and response_data.get("code") == "00":
            installments = response_data.get("response", {}).get("installments", [])
            issuer_name = response_data.get("response", {}).get("issuerName")

            print(f"\n✅ Cuotas obtenidas exitosamente")
            print(f"🏦 Emisor: {issuer_name}")
            print(f"💳 BIN: {bin_number}")
            print(f"📊 Número de cuotas disponibles: {len(installments)}")
            print(f"📋 Cuotas: {', '.join(installments)}")

            return {
                "success": True,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "installments_count": len(installments),
                "issuer_name": issuer_name,
                "headers": dict(response.headers)
            }
        else:
            print(f"\n❌ Error al buscar cuotas")
            print(f"Código: {response_data.get('code')}")
            print(f"Mensaje: {response_data.get('message')}")

            return {
                "success": False,
                "error": f"Installments search failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }

    except requests.exceptions.RequestException as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f"\n❌ Excepción durante la solicitud: {str(e)}")

        return {
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms
        }


def run_test():
    """
    Ejecuta el caso de prueba completo CPI-001
    """
    print("\n" + "=" * 60)
    print("CASO DE PRUEBA CPI-001")
    print("Flujo completo exitoso - Generar token y buscar cuotas")
    print("=" * 60)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ambiente: QA")
    print("=" * 60)

    result = TestResult()
    result.start_time = time.time()

    # Generar identificadores únicos
    transaction_id = generate_transaction_id()
    order_number = generate_order_number()

    print(f"\n🆔 Transaction ID: {transaction_id}")
    print(f"🆔 Order Number: {order_number}")

    # PASO 1: Generar token
    token_result = generate_token(transaction_id, order_number)
    result.add_step(
        "Generate Token",
        token_result["success"],
        token_result,
        token_result["duration_ms"]
    )

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = token_result.get("error", "Token generation failed")
        return result

    # PASO 2: Buscar cuotas
    token = token_result["token"]
    installments_result = search_installments(token, transaction_id)
    result.add_step(
        "Search Installments",
        installments_result["success"],
        installments_result,
        installments_result["duration_ms"]
    )

    result.end_time = time.time()
    result.passed = token_result["success"] and installments_result["success"]

    if not installments_result["success"]:
        result.error_message = installments_result.get("error", "Installments search failed")

    return result


def save_results(result):
    """
    Guarda los resultados en archivos
    """
    print("\n" + "=" * 60)
    print("GUARDANDO RESULTADOS")
    print("=" * 60)

    # Guardar resultado completo en JSON
    json_file = os.path.join(RESULTS_DIR, "test_result.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    print(f"✅ Resultado JSON guardado: {json_file}")

    # Guardar reporte en texto
    txt_file = os.path.join(RESULTS_DIR, "test_report.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("REPORTE DE PRUEBA CPI-001\n")
        f.write("=" * 60 + "\n")
        f.write(f"Test ID: {result.test_id}\n")
        f.write(f"Test Name: {result.test_name}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Estado: {'✅ PASÓ' if result.passed else '❌ FALLÓ'}\n")
        f.write(f"Duración Total: {result.to_dict()['total_duration_ms']:.2f}ms\n")

        if result.error_message:
            f.write(f"Error: {result.error_message}\n")

        f.write("\n" + "-" * 60 + "\n")
        f.write("PASOS EJECUTADOS\n")
        f.write("-" * 60 + "\n")

        for step in result.results:
            f.write(f"\n{step['step']}:\n")
            f.write(f"  Estado: {'✅ Éxito' if step['success'] else '❌ Fallo'}\n")
            f.write(f"  Duración: {step['duration_ms']:.2f}ms\n")
            f.write(f"  Timestamp: {step['timestamp']}\n")

            if step['success']:
                if 'status_code' in step['data']:
                    f.write(f"  Status Code: {step['data']['status_code']}\n")
                if 'response' in step['data']:
                    f.write(f"  Response Code: {step['data']['response'].get('code')}\n")
                    f.write(f"  Response Message: {step['data']['response'].get('message')}\n")

    print(f"✅ Reporte TXT guardado: {txt_file}")

    # Guardar requests individuales
    for i, step in enumerate(result.results, 1):
        step_file = os.path.join(RESULTS_DIR, f"step_{i}_{step['step'].replace(' ', '_')}.json")
        with open(step_file, "w", encoding="utf-8") as f:
            json.dump(step['data'], f, indent=2, ensure_ascii=False)
        print(f"✅ Paso {i} guardado: {step_file}")


def print_summary(result):
    """
    Imprime resumen final
    """
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Test: {result.test_name}")
    print(f"Estado: {'✅ PASÓ' if result.passed else '❌ FALLÓ'}")
    print(f"Duración Total: {result.to_dict()['total_duration_ms']:.2f}ms")

    if result.error_message:
        print(f"Error: {result.error_message}")

    print("\nPasos ejecutados:")
    for step in result.results:
        status_icon = "✅" if step['success'] else "❌"
        print(f"  {status_icon} {step['step']} - {step['duration_ms']:.2f}ms")

    print("=" * 60)


if __name__ == "__main__":
    try:
        # Ejecutar prueba
        test_result = run_test()

        # Guardar resultados
        save_results(test_result)

        # Imprimir resumen
        print_summary(test_result)

        # Exit code
        exit(0 if test_result.passed else 1)

    except Exception as e:
        print(f"\n❌ Error crítico durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
