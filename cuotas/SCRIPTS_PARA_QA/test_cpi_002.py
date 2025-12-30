"""
Script de prueba CPI-002: Token Reutilizable

Descripción:
    Este script valida que un token puede ser reutilizado en múltiples consultas:
    1. Generación de token de sesión
    2. Primera búsqueda de cuotas (debe funcionar)
    3. Segunda búsqueda con el mismo token (debe funcionar - token reutilizable)

Ambiente original: DEV (testapi-pw.izipay.pe)
Fecha: 2025-11-04
Formato TransactionId: DEV + YYYYMMDDHHMMSS
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

# ============================================================================
# CONFIGURACIÓN - MODIFICAR ESTOS VALORES SEGÚN EL AMBIENTE A PROBAR
# ============================================================================
CONFIG = {
    # ⚠️ CAMBIAR: URL del ambiente que deseas probar
    # Opciones:
    # - DEV: https://testapi-pw.izipay.pe
    # - SANDBOX: https://sandbox-api-pw.izipay.pe
    # - QA: https://qa-api-pw.izipay.pe
    # - PROD: https://api-pw.izipay.pe
    "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",

    # ⚠️ CAMBIAR: Credenciales del comercio a probar
    # Valores actuales corresponden al comercio 4001834 en SANDBOX
    "merchant_code": "4001834",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}
# ============================================================================

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestResult:
    def __init__(self):
        self.test_id = "CPI-002"
        self.test_name = "Token Reutilizable"
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
    """Genera un transactionId único con formato: DEV + YYYYMMDDHHMMSS"""
    now = datetime.now()
    return f"DEV{now.strftime('%Y%m%d%H%M%S')}"


def generate_order_number():
    """Genera un orderNumber único"""
    now = datetime.now()
    return f"ORDER{now.strftime('%Y%m%d%H%M%S')}"


def generate_token(transaction_id, order_number):
    """PASO 1: Generar token de sesión"""
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
    print(f"📤 TransactionId: {transaction_id}")

    start_time = time.time()

    try:
        response = requests.post(CONFIG["token_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        print(f"\n📥 Response Status: {response.status_code}")
        print(f"⏱️  Response Time: {duration_ms:.2f}ms")

        response_data = response.json()

        if response.status_code == 200 and response_data.get("code") == "00":
            token = response_data.get("response", {}).get("token")
            print(f"✅ Token generado exitosamente")
            print(f"🔑 Token (primeros 50 caracteres): {token[:50]}...")

            return {
                "success": True,
                "token": token,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }
        else:
            print(f"❌ Error al generar token: {response_data.get('message')}")
            return {
                "success": False,
                "error": f"Token generation failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f"❌ Excepción: {str(e)}")
        return {"success": False, "error": str(e), "duration_ms": duration_ms}


def search_installments(token, transaction_id, bin_number="545545", attempt_number=1):
    """Buscar cuotas con el token"""
    print("\n" + "=" * 60)
    print(f"PASO {attempt_number + 1}: BUSCAR CUOTAS (Intento #{attempt_number})")
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
    print(f"📤 Using token: {token[:30]}...")
    print(f"📤 Attempt: {attempt_number}")

    start_time = time.time()

    try:
        response = requests.post(CONFIG["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        print(f"\n📥 Response Status: {response.status_code}")
        print(f"⏱️  Response Time: {duration_ms:.2f}ms")

        response_data = response.json()
        print(f"📥 Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")

        if response.status_code == 200 and response_data.get("code") == "00":
            installments = response_data.get("response", {}).get("installments", [])
            print(f"\n✅ Cuotas obtenidas: {len(installments)} opciones")
            return {
                "success": True,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "installments_count": len(installments)
            }
        else:
            print(f"\n❌ Error al buscar cuotas: {response_data.get('message')}")
            return {
                "success": False,
                "error": f"Search failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f"❌ Excepción: {str(e)}")
        return {"success": False, "error": str(e), "duration_ms": duration_ms}


def run_test():
    """Ejecuta el caso de prueba CPI-002"""
    print("\n" + "=" * 60)
    print("CASO DE PRUEBA CPI-002")
    print("Token Reutilizable")
    print("=" * 60)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Objetivo: Verificar que un token puede reutilizarse en múltiples consultas")
    print("=" * 60)

    result = TestResult()
    result.start_time = time.time()

    # Generar identificadores
    transaction_id = generate_transaction_id()
    order_number = generate_order_number()

    print(f"\n🆔 Transaction ID: {transaction_id}")
    print(f"🆔 Order Number: {order_number}")

    # PASO 1: Generar token
    token_result = generate_token(transaction_id, order_number)
    result.add_step("Generate Token", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "Failed to generate token"
        return result

    token = token_result["token"]

    # PASO 2: Primera búsqueda (debe funcionar)
    print("\n" + "🔹" * 30)
    print("PRIMER USO DEL TOKEN (Debe funcionar)")
    print("🔹" * 30)

    first_search = search_installments(token, transaction_id, attempt_number=1)
    result.add_step("First Search (Should Succeed)", first_search["success"], first_search, first_search["duration_ms"])

    # PASO 3: Segunda búsqueda con el mismo token (debe funcionar - token reutilizable)
    print("\n" + "🔹" * 30)
    print("SEGUNDO USO DEL TOKEN (Debe funcionar - token reutilizable)")
    print("🔹" * 30)

    second_search = search_installments(token, transaction_id, attempt_number=2)
    result.add_step("Second Search (Should Succeed - Reusable)", second_search["success"], second_search, second_search["duration_ms"])

    result.end_time = time.time()

    # La prueba pasa si:
    # 1. El token se genera correctamente
    # 2. La primera búsqueda funciona
    # 3. La segunda búsqueda TAMBIÉN FUNCIONA (token reutilizable)

    if token_result["success"] and first_search["success"] and second_search["success"]:
        result.passed = True
        print("\n" + "=" * 60)
        print("✅ PRUEBA EXITOSA")
        print("=" * 60)
        print("✅ Token generado correctamente")
        print("✅ Primera búsqueda exitosa")
        print("✅ Segunda búsqueda exitosa (token reutilizado)")
        print("\n🎉 El token es reutilizable como se esperaba!")
    else:
        result.passed = False
        if not first_search["success"]:
            result.error_message = "Primera búsqueda falló inesperadamente"
        elif not second_search["success"]:
            result.error_message = "⚠️ FALLO: Segunda búsqueda rechazó el token (debería aceptarlo)"
        else:
            result.error_message = "Error en la generación del token"

    return result


def save_results(result):
    """Guarda los resultados en archivos"""
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
        f.write("REPORTE DE PRUEBA CPI-002\n")
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

    print(f"✅ Reporte TXT guardado: {txt_file}")

    # Guardar pasos individuales
    for i, step in enumerate(result.results, 1):
        step_file = os.path.join(RESULTS_DIR, f"step_{i}_{step['step'].replace(' ', '_').replace('(', '').replace(')', '')}.json")
        with open(step_file, "w", encoding="utf-8") as f:
            json.dump(step['data'], f, indent=2, ensure_ascii=False)
        print(f"✅ Paso {i} guardado: {step_file}")


def print_summary(result):
    """Imprime resumen final"""
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Test: {result.test_name}")
    print(f"Estado: {'✅ PASÓ' if result.passed else '❌ FALLÓ'}")
    print(f"Duración Total: {result.to_dict()['total_duration_ms']:.2f}ms")

    if result.error_message:
        print(f"\nObservación: {result.error_message}")

    print("\nPasos ejecutados:")
    for step in result.results:
        status_icon = "✅" if step['success'] else "❌"
        print(f"  {status_icon} {step['step']} - {step['duration_ms']:.2f}ms")

    print("=" * 60)


if __name__ == "__main__":
    try:
        test_result = run_test()
        save_results(test_result)
        print_summary(test_result)
        exit(0 if test_result.passed else 1)
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
