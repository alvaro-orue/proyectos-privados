"""
Test Runner Multi-Ambiente
Ejecuta casos de prueba en diferentes ambientes (DEV, SANDBOX, QA)

Uso:
    python test_runner_multi_env.py --env DEV --test CPI-001
    python test_runner_multi_env.py --env SANDBOX --test CPI-001
    python test_runner_multi_env.py --env DEV --test ALL
    python test_runner_multi_env.py --env SANDBOX --list-bins
"""

import requests
import json
import time
from datetime import datetime
import os
import sys
import argparse

# Importar configuración de ambientes
from config_environments import get_environment, list_environments, print_environment_info

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class TestResult:
    def __init__(self, test_id, test_name, environment):
        self.test_id = test_id
        self.test_name = test_name
        self.environment = environment
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
            "environment": self.environment,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": (self.end_time - self.start_time) * 1000 if self.start_time and self.end_time else 0,
            "passed": self.passed,
            "error_message": self.error_message,
            "steps": self.results
        }


def generate_transaction_id(env_prefix="TEST"):
    """
    Genera un transactionId único con formato: PREFIX + YYYYMMDDHHMMSS
    Ejemplo: DEV20251029075105, SBX20251029075105
    """
    now = datetime.now()
    return f"{env_prefix}{now.strftime('%Y%m%d%H%M%S')}"


def generate_order_number():
    """Genera un orderNumber único"""
    now = datetime.now()
    return f"ORDER{now.strftime('%Y%m%d%H%M%S')}"


def generate_token(config, transaction_id, order_number, amount="100.00"):
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
        "merchantCode": config["merchant_code"],
        "orderNumber": order_number,
        "publicKey": config["public_key"],
        "amount": amount
    }

    print(f"\n📤 Request URL: {config['token_url']}")
    print(f"📤 Headers: {json.dumps(headers, indent=2)}")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")

    start_time = time.time()

    try:
        response = requests.post(
            config["token_url"],
            headers=headers,
            json=payload,
            timeout=config.get("timeout", 30)
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


def search_installments(config, token, transaction_id, bin_number="545545", language="ESP"):
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
        "merchantCode": config["merchant_code"],
        "language": language
    }

    print(f"\n📤 Request URL: {config['installments_url']}")
    print(f"📤 Headers (Authorization truncado): {json.dumps({**headers, 'Authorization': f'Bearer {token[:30]}...'}, indent=2)}")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")

    start_time = time.time()

    try:
        response = requests.post(
            config["installments_url"],
            headers=headers,
            json=payload,
            timeout=config.get("timeout", 30)
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


def run_cpi_001(environment):
    """
    Ejecuta CPI-001: Flujo completo exitoso
    """
    config = get_environment(environment)

    print("\n" + "=" * 60)
    print(f"CASO DE PRUEBA CPI-001 - AMBIENTE: {environment}")
    print("Flujo completo exitoso - Generar token y buscar cuotas")
    print("=" * 60)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ambiente: {config['name']}")
    print(f"URL Base: {config['token_url'].split('/security')[0]}")
    print(f"Merchant Code: {config['merchant_code']}")
    print("=" * 60)

    result = TestResult("CPI-001", "Flujo completo exitoso", environment)
    result.start_time = time.time()

    # Generar identificadores únicos
    transaction_id = generate_transaction_id(config.get("transaction_prefix", "TEST"))
    order_number = generate_order_number()

    print(f"\n🆔 Transaction ID: {transaction_id}")
    print(f"🆔 Order Number: {order_number}")

    # PASO 1: Generar token
    token_result = generate_token(config, transaction_id, order_number)
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

    # PASO 2: Buscar cuotas con el primer BIN disponible
    token = token_result["token"]
    bin_number = config["bins_disponibles"][0]
    installments_result = search_installments(config, token, transaction_id, bin_number)
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


def save_results(result, output_dir):
    """
    Guarda los resultados en archivos
    """
    print("\n" + "=" * 60)
    print("GUARDANDO RESULTADOS")
    print("=" * 60)

    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Guardar resultado completo en JSON
    json_file = os.path.join(output_dir, f"test_result_{result.test_id}_{result.environment}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    print(f"✅ Resultado JSON guardado: {json_file}")

    # Guardar reporte en texto
    txt_file = os.path.join(output_dir, f"test_report_{result.test_id}_{result.environment}.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"REPORTE DE PRUEBA {result.test_id} - {result.environment}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Test ID: {result.test_id}\n")
        f.write(f"Test Name: {result.test_name}\n")
        f.write(f"Ambiente: {result.environment}\n")
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


def print_summary(result):
    """
    Imprime resumen final
    """
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Test: {result.test_name}")
    print(f"Ambiente: {result.environment}")
    print(f"Estado: {'✅ PASÓ' if result.passed else '❌ FALLÓ'}")
    print(f"Duración Total: {result.to_dict()['total_duration_ms']:.2f}ms")

    if result.error_message:
        print(f"Error: {result.error_message}")

    print("\nPasos ejecutados:")
    for step in result.results:
        status_icon = "✅" if step['success'] else "❌"
        print(f"  {status_icon} {step['step']} - {step['duration_ms']:.2f}ms")

    print("=" * 60)


def list_bins(environment):
    """
    Lista los BINs disponibles para un ambiente
    """
    config = get_environment(environment)

    print(f"\n{'='*60}")
    print(f"BINs DISPONIBLES - AMBIENTE: {environment}")
    print(f"{'='*60}")
    print(f"Ambiente: {config['name']}")
    print(f"Merchant Code: {config['merchant_code']}")
    print(f"\nBINs configurados:")

    for bin_num in config['bins_disponibles']:
        print(f"  • {bin_num}")

    print(f"\nTotal: {len(config['bins_disponibles'])} BINs")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Test Runner Multi-Ambiente para APIs Izipay")

    parser.add_argument(
        "--env",
        choices=list_environments(),
        required=False,
        help="Ambiente de ejecución (DEV, SANDBOX, QA)"
    )

    parser.add_argument(
        "--test",
        choices=["CPI-001", "ALL"],
        help="Caso de prueba a ejecutar"
    )

    parser.add_argument(
        "--list-envs",
        action="store_true",
        help="Lista todos los ambientes disponibles"
    )

    parser.add_argument(
        "--list-bins",
        action="store_true",
        help="Lista los BINs disponibles para el ambiente especificado"
    )

    parser.add_argument(
        "--env-info",
        action="store_true",
        help="Muestra información del ambiente especificado"
    )

    args = parser.parse_args()

    # Listar ambientes
    if args.list_envs:
        print_environment_info()
        return 0

    # Validar que se especificó ambiente para otras operaciones
    if not args.env and (args.test or args.list_bins or args.env_info):
        print("❌ Error: Debe especificar --env para esta operación")
        return 1

    # Mostrar info del ambiente
    if args.env_info:
        print_environment_info(args.env)
        return 0

    # Listar BINs
    if args.list_bins:
        list_bins(args.env)
        return 0

    # Ejecutar pruebas
    if args.test:
        output_dir = os.path.join("CASOS_MULTI_AMBIENTE", args.env, "results")

        if args.test == "CPI-001":
            result = run_cpi_001(args.env)
            save_results(result, output_dir)
            print_summary(result)
            return 0 if result.passed else 1

        elif args.test == "ALL":
            print(f"\n🚀 Ejecutando TODOS los casos de prueba en ambiente: {args.env}\n")
            results = []

            # CPI-001
            result = run_cpi_001(args.env)
            save_results(result, output_dir)
            results.append(result)

            # Resumen consolidado
            print("\n" + "=" * 60)
            print("RESUMEN CONSOLIDADO")
            print("=" * 60)
            passed = sum(1 for r in results if r.passed)
            failed = len(results) - passed
            print(f"Total: {len(results)} casos")
            print(f"✅ Pasados: {passed}")
            print(f"❌ Fallados: {failed}")
            print("=" * 60)

            return 0 if failed == 0 else 1

    # Si no se especificó ninguna acción, mostrar ayuda
    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error crítico durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
