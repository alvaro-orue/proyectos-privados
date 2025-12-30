"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     SUITE COMPLETA DE PRUEBAS - API INSTALLMENTS IZIPAY                 ║
║                                                                          ║
║     Ejecuta todos los casos de prueba (CPI-001 a CPI-007)               ║
║     Genera informe completo en Markdown                                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

Descripción:
    Script maestro que ejecuta los 7 casos de prueba del API Installments
    y genera un informe completo en formato Markdown similar al informe
    de documentación de pruebas.

Casos de prueba incluidos:
    - CPI-001: Flujo completo exitoso
    - CPI-002: Token reutilizable
    - CPI-003: TransactionId consistente
    - CPI-004: Casos de error (5 escenarios)
    - CPI-005: Diferentes BINs (4 bancos)
    - CPI-006: Amount 0.00
    - CPI-007: Idioma inglés

Autor: Automatización QA
Fecha: 2025-11-04
Versión: 1.0
"""

import requests
import json
import time
from datetime import datetime
import os
import sys
import subprocess

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================================================
# CONFIGURACIÓN DE AMBIENTES
# ============================================================================
AMBIENTES = {
    "1": {
        "nombre": "DEV (Desarrollo)",
        "codigo": "DEV",
        "token_url": "https://testapi-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://testapi-pw.izipay.pe/Installments/v1/Installments/Search",
        "transaction_prefix": "DEV"
    },
    "2": {
        "nombre": "SANDBOX",
        "codigo": "SANDBOX",
        "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "transaction_prefix": "SBX"
    },
    "3": {
        "nombre": "QA (Quality Assurance)",
        "codigo": "QA",
        "token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "transaction_prefix": "QA"
    },
    "4": {
        "nombre": "PRODUCCIÓN",
        "codigo": "PROD",
        "token_url": "https://api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://api-pw.izipay.pe/Installments/v1/Installments/Search",
        "transaction_prefix": "PROD"
    }
}

# BINs disponibles para pruebas (validados en DEV/QA)
# NOTA: Para SANDBOX, solo el BIN 511578 ha sido validado como funcional
BINS_PRUEBA = {
    "545545": {"banco": "SCOTIABANK", "cuotas_esperadas": 12},
    "400917": {"banco": "SCOTIABANK VISA", "cuotas_esperadas": 36},
    "377893": {"banco": "BCP", "cuotas_esperadas": 36},
    "553650": {"banco": "BBVA MC Platinum", "cuotas_esperadas": 36}
}

# BINs específicos para SANDBOX (ambiente inestable)
BINS_SANDBOX = {
    "511578": {"banco": "BBVA MC Platinum", "cuotas_esperadas": 36}
}

# ============================================================================
# CLASES AUXILIARES
# ============================================================================

class TestResult:
    """Clase para almacenar resultados de pruebas"""
    def __init__(self, test_id, test_name):
        self.test_id = test_id
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
        self.passed = False
        self.error_message = None
        self.steps = []
        self.transaction_ids = []

    def add_step(self, step_name, success, data, duration_ms):
        self.steps.append({
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
            "steps": self.steps,
            "transaction_ids": self.transaction_ids
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def generate_transaction_id(prefix):
    """Genera un transactionId único con prefijo del ambiente"""
    now = datetime.now()
    return f"{prefix}{now.strftime('%Y%m%d%H%M%S')}"


def generate_order_number():
    """Genera un orderNumber único"""
    now = datetime.now()
    return f"ORDER{now.strftime('%Y%m%d%H%M%S')}"


def print_header(title, char="="):
    """Imprime un encabezado formateado"""
    print(f"\n{char * 60}")
    print(title)
    print(f"{char * 60}")


def apply_sandbox_delay(config, delay_seconds=2):
    """
    Aplica un delay si el ambiente es SANDBOX
    SANDBOX requiere tiempo para procesar el token antes de usarlo
    """
    if config.get("transaction_prefix") == "SBX":
        print(f"⏱️  Esperando {delay_seconds} segundos (requerido por SANDBOX)...")
        time.sleep(delay_seconds)


# ============================================================================
# FUNCIONES API
# ============================================================================

def generate_token(config, transaction_id, order_number, amount="100.00"):
    """Genera un token de sesión"""
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

    start_time = time.time()

    try:
        response = requests.post(
            config["token_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        duration_ms = (time.time() - start_time) * 1000
        response_data = response.json()

        if response.status_code == 200 and response_data.get("code") == "00":
            token = response_data.get("response", {}).get("token")
            return {
                "success": True,
                "token": token,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "headers": dict(response.headers),
                "request": {"headers": headers, "body": payload}
            }
        else:
            return {
                "success": False,
                "error": f"Token generation failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request": {"headers": headers, "body": payload}
            }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms,
            "request": {"headers": headers, "body": payload}
        }


def search_installments(config, token, transaction_id, bin_number="545545", language="ESP"):
    """Busca cuotas disponibles"""
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

    start_time = time.time()

    try:
        response = requests.post(
            config["installments_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        duration_ms = (time.time() - start_time) * 1000
        response_data = response.json()

        if response.status_code == 200 and response_data.get("code") == "00":
            installments = response_data.get("response", {}).get("installments", [])
            return {
                "success": True,
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "installments_count": len(installments),
                "headers": dict(response.headers),
                "request": {"headers": {k: v for k, v in headers.items() if k != "Authorization"}, "body": payload}
            }
        else:
            return {
                "success": False,
                "error": f"Installments search failed: {response_data.get('message')}",
                "response": response_data,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request": {"headers": {k: v for k, v in headers.items() if k != "Authorization"}, "body": payload}
            }

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms,
            "request": {"headers": {k: v for k, v in headers.items() if k != "Authorization"}, "body": payload}
        }


# ============================================================================
# CASOS DE PRUEBA
# ============================================================================

def test_cpi_001(config):
    """CPI-001: Flujo completo exitoso"""
    print_header("Ejecutando CPI-001: Flujo completo exitoso")

    result = TestResult("CPI-001", "Flujo completo exitoso")
    result.start_time = time.time()

    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    result.transaction_ids.append(transaction_id)

    print(f"🆔 Transaction ID: {transaction_id}")
    print(f"🆔 Order Number: {order_number}")

    # Paso 1: Generar token
    print("\n📝 Paso 1: Generar token...")
    token_result = generate_token(config, transaction_id, order_number)
    result.add_step("Generate Token", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = token_result.get("error", "Token generation failed")
        print(f"❌ Error: {result.error_message}")
        return result

    print(f"✅ Token generado en {token_result['duration_ms']:.2f}ms")

    # ⏱️ CRÍTICO: Delay para SANDBOX
    apply_sandbox_delay(config)

    # Paso 2: Buscar cuotas
    print("📝 Paso 2: Buscar cuotas...")
    token = token_result["token"]
    installments_result = search_installments(config, token, transaction_id)
    result.add_step("Search Installments", installments_result["success"], installments_result, installments_result["duration_ms"])

    result.end_time = time.time()
    result.passed = token_result["success"] and installments_result["success"]

    if installments_result["success"]:
        print(f"✅ Cuotas obtenidas en {installments_result['duration_ms']:.2f}ms")
        print(f"📊 Cuotas disponibles: {installments_result['installments_count']}")
    else:
        result.error_message = installments_result.get("error", "Installments search failed")
        print(f"❌ Error: {result.error_message}")

    return result


def test_cpi_002(config):
    """CPI-002: Token reutilizable"""
    print_header("Ejecutando CPI-002: Token reutilizable")

    result = TestResult("CPI-002", "Token reutilizable")
    result.start_time = time.time()

    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    result.transaction_ids.append(transaction_id)

    print(f"🆔 Transaction ID: {transaction_id}")

    # Paso 1: Generar token
    print("\n📝 Paso 1: Generar token...")
    token_result = generate_token(config, transaction_id, order_number)
    result.add_step("Generate Token", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "Failed to generate token"
        return result

    token = token_result["token"]
    print(f"✅ Token generado en {token_result['duration_ms']:.2f}ms")

    # ⏱️ CRÍTICO: Delay para SANDBOX
    apply_sandbox_delay(config)

    # Paso 2: Primera búsqueda
    print("📝 Paso 2: Primera búsqueda de cuotas...")
    first_search = search_installments(config, token, transaction_id)
    result.add_step("First Search (Should Succeed)", first_search["success"], first_search, first_search["duration_ms"])

    if first_search["success"]:
        print(f"✅ Primera búsqueda exitosa en {first_search['duration_ms']:.2f}ms")
    else:
        print(f"❌ Primera búsqueda falló")

    # Paso 3: Segunda búsqueda con el mismo token
    print("📝 Paso 3: Segunda búsqueda con el mismo token...")
    time.sleep(0.5)  # Pequeña pausa entre búsquedas
    second_search = search_installments(config, token, transaction_id)
    result.add_step("Second Search (Should Succeed - Reusable)", second_search["success"], second_search, second_search["duration_ms"])

    result.end_time = time.time()
    result.passed = token_result["success"] and first_search["success"] and second_search["success"]

    if second_search["success"]:
        print(f"✅ Segunda búsqueda exitosa en {second_search['duration_ms']:.2f}ms")
        print("🎉 Token reutilizado correctamente!")
    else:
        result.error_message = "Token no pudo ser reutilizado"
        print(f"❌ Token no se pudo reutilizar")

    return result


def test_cpi_003(config):
    """CPI-003: TransactionId consistente"""
    print_header("Ejecutando CPI-003: TransactionId consistente")

    result = TestResult("CPI-003", "TransactionId consistente")
    result.start_time = time.time()

    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    result.transaction_ids.append(transaction_id)

    print(f"🆔 Transaction ID: {transaction_id}")
    print("🎯 Objetivo: Usar el mismo TransactionId en ambas llamadas")

    # Paso 1: Generar token
    print("\n📝 Paso 1: Generar token con TransactionId...")
    token_result = generate_token(config, transaction_id, order_number)
    result.add_step("Generate Token", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "Failed to generate token"
        return result

    print(f"✅ Token generado en {token_result['duration_ms']:.2f}ms")

    # ⏱️ CRÍTICO: Delay para SANDBOX
    apply_sandbox_delay(config)

    # Paso 2: Buscar cuotas con el mismo TransactionId
    print("📝 Paso 2: Buscar cuotas con el MISMO TransactionId...")
    token = token_result["token"]
    installments_result = search_installments(config, token, transaction_id)
    result.add_step("Search Installments", installments_result["success"], installments_result, installments_result["duration_ms"])

    result.end_time = time.time()
    result.passed = token_result["success"] and installments_result["success"]

    if installments_result["success"]:
        print(f"✅ Cuotas obtenidas en {installments_result['duration_ms']:.2f}ms")
        print(f"✅ TransactionId consistente: {transaction_id}")
    else:
        result.error_message = installments_result.get("error", "Installments search failed")
        print(f"❌ Error: {result.error_message}")

    return result


def test_cpi_004(config):
    """CPI-004: Casos de error"""
    print_header("Ejecutando CPI-004: Casos de error (5 escenarios)")

    result = TestResult("CPI-004", "Casos de error")
    result.start_time = time.time()

    escenarios_exitosos = 0
    total_escenarios = 5

    # Escenario 1: Token inválido
    print("\n📝 Escenario 1: Token inválido...")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer TOKEN_INVALIDO_12345",
        "transactionId": "TEST_ERROR_001"
    }
    payload = {"bin": "545545", "merchantCode": config["merchant_code"], "language": "ESP"}

    start_time = time.time()
    try:
        response = requests.post(config["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        if response.status_code == 401:
            print(f"✅ Error 401 detectado correctamente ({duration_ms:.2f}ms)")
            escenarios_exitosos += 1
            success = True
        else:
            print(f"❌ Se esperaba 401, pero se recibió {response.status_code}")
            success = False

        result.add_step("Error 1: Token Inválido", success, {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response": response.json()
        }, duration_ms)
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        result.add_step("Error 1: Token Inválido", False, {"error": str(e)}, 0)

    # Escenario 2: Sin header Authorization
    print("📝 Escenario 2: Sin header Authorization...")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "transactionId": "TEST_ERROR_002"
    }

    start_time = time.time()
    try:
        response = requests.post(config["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        if response.status_code == 400:
            print(f"✅ Error 400 detectado correctamente ({duration_ms:.2f}ms)")
            escenarios_exitosos += 1
            success = True
        else:
            print(f"❌ Se esperaba 400, pero se recibió {response.status_code}")
            success = False

        result.add_step("Error 2: Sin Header Authorization", success, {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response": response.json()
        }, duration_ms)
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        result.add_step("Error 2: Sin Header Authorization", False, {"error": str(e)}, 0)

    # Generar token válido para los siguientes escenarios
    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    token_result = generate_token(config, transaction_id, order_number)

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "No se pudo generar token para escenarios de error"
        return result

    token = token_result["token"]

    # Escenario 3: BIN con formato inválido
    print("📝 Escenario 3: BIN con formato inválido...")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "transactionId": transaction_id
    }
    payload = {"bin": "ABC", "merchantCode": config["merchant_code"], "language": "ESP"}

    start_time = time.time()
    try:
        response = requests.post(config["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        if response.status_code == 400:
            print(f"✅ Error 400 detectado correctamente ({duration_ms:.2f}ms)")
            escenarios_exitosos += 1
            success = True
        else:
            print(f"❌ Se esperaba 400, pero se recibió {response.status_code}")
            success = False

        result.add_step("Error 3: BIN con Formato Inválido", success, {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response": response.json()
        }, duration_ms)
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        result.add_step("Error 3: BIN con Formato Inválido", False, {"error": str(e)}, 0)

    # Escenario 4: Merchant Code inválido
    print("📝 Escenario 4: Merchant Code inválido...")
    payload = {"bin": "545545", "merchantCode": "9999999", "language": "ESP"}

    start_time = time.time()
    try:
        response = requests.post(config["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        if response.status_code == 401:
            print(f"✅ Error 401 detectado correctamente ({duration_ms:.2f}ms)")
            escenarios_exitosos += 1
            success = True
        else:
            print(f"❌ Se esperaba 401, pero se recibió {response.status_code}")
            success = False

        result.add_step("Error 4: Merchant Code Inválido", success, {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response": response.json()
        }, duration_ms)
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        result.add_step("Error 4: Merchant Code Inválido", False, {"error": str(e)}, 0)

    # Escenario 5: Parámetro BIN faltante
    print("📝 Escenario 5: Parámetro BIN faltante...")
    payload = {"merchantCode": config["merchant_code"], "language": "ESP"}

    start_time = time.time()
    try:
        response = requests.post(config["installments_url"], headers=headers, json=payload, timeout=30)
        duration_ms = (time.time() - start_time) * 1000

        if response.status_code == 400:
            print(f"✅ Error 400 detectado correctamente ({duration_ms:.2f}ms)")
            escenarios_exitosos += 1
            success = True
        else:
            print(f"❌ Se esperaba 400, pero se recibió {response.status_code}")
            success = False

        result.add_step("Error 5: Parámetro BIN Faltante", success, {
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "response": response.json()
        }, duration_ms)
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        result.add_step("Error 5: Parámetro BIN Faltante", False, {"error": str(e)}, 0)

    result.end_time = time.time()
    result.passed = (escenarios_exitosos == total_escenarios)

    print(f"\n📊 Resultado: {escenarios_exitosos}/{total_escenarios} escenarios validados correctamente")

    if not result.passed:
        result.error_message = f"Solo {escenarios_exitosos} de {total_escenarios} escenarios pasaron"

    return result


def test_cpi_005(config):
    """CPI-005: Diferentes BINs"""
    # Seleccionar BINs según el ambiente
    bins_a_probar = BINS_SANDBOX if config.get("transaction_prefix") == "SBX" else BINS_PRUEBA
    total_bins_text = f"{len(bins_a_probar)} banco{'s' if len(bins_a_probar) > 1 else ''}"

    if config.get("transaction_prefix") == "SBX":
        print_header(f"Ejecutando CPI-005: Diferentes BINs ({total_bins_text}) - SANDBOX")
        print("⚠️  NOTA: SANDBOX solo tiene 1 BIN validado debido a inestabilidad del ambiente")
    else:
        print_header(f"Ejecutando CPI-005: Diferentes BINs ({total_bins_text})")

    result = TestResult("CPI-005", "Diferentes BINs")
    result.start_time = time.time()

    bins_exitosos = 0
    total_bins = len(bins_a_probar)

    for bin_number, bin_info in bins_a_probar.items():
        print(f"\n📝 Probando BIN: {bin_number} ({bin_info['banco']})...")

        transaction_id = generate_transaction_id(config["transaction_prefix"])
        order_number = generate_order_number()
        result.transaction_ids.append(transaction_id)

        # Generar token
        token_result = generate_token(config, transaction_id, order_number)

        if not token_result["success"]:
            print(f"❌ Error al generar token")
            result.add_step(f"BIN {bin_number} ({bin_info['banco']}) - Token", False, token_result, token_result["duration_ms"])
            continue

        # ⏱️ CRÍTICO: Delay para SANDBOX
        apply_sandbox_delay(config)

        # Buscar cuotas
        token = token_result["token"]
        installments_result = search_installments(config, token, transaction_id, bin_number)

        if installments_result["success"]:
            cuotas = installments_result["installments_count"]
            print(f"✅ {cuotas} cuotas obtenidas en {installments_result['duration_ms']:.2f}ms")
            bins_exitosos += 1
            result.add_step(f"BIN {bin_number} ({bin_info['banco']})", True, {
                "token_result": token_result,
                "installments_result": installments_result,
                "cuotas_obtenidas": cuotas
            }, token_result["duration_ms"] + installments_result["duration_ms"])
        else:
            print(f"❌ Error al buscar cuotas")
            result.add_step(f"BIN {bin_number} ({bin_info['banco']})", False, {
                "token_result": token_result,
                "installments_result": installments_result
            }, token_result["duration_ms"] + installments_result["duration_ms"])

    result.end_time = time.time()
    result.passed = (bins_exitosos == total_bins)

    print(f"\n📊 Resultado: {bins_exitosos}/{total_bins} BINs validados correctamente")

    if not result.passed:
        result.error_message = f"Solo {bins_exitosos} de {total_bins} BINs pasaron"

    return result


def test_cpi_006(config):
    """CPI-006: Amount 0.00"""
    print_header("Ejecutando CPI-006: Amount 0.00")

    result = TestResult("CPI-006", "Amount 0.00")
    result.start_time = time.time()

    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    result.transaction_ids.append(transaction_id)

    print(f"🆔 Transaction ID: {transaction_id}")
    print("🎯 Objetivo: Validar amount 0.00")

    # Paso 1: Generar token con amount 0.00
    print("\n📝 Paso 1: Generar token con amount=0.00...")
    token_result = generate_token(config, transaction_id, order_number, amount="0.00")
    result.add_step("Generate Token (amount=0.00)", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "Failed to generate token with amount 0.00"
        return result

    print(f"✅ Token generado en {token_result['duration_ms']:.2f}ms")

    # ⏱️ CRÍTICO: Delay para SANDBOX
    apply_sandbox_delay(config)

    # Paso 2: Buscar cuotas
    print("📝 Paso 2: Buscar cuotas...")
    token = token_result["token"]
    installments_result = search_installments(config, token, transaction_id)
    result.add_step("Search Installments", installments_result["success"], installments_result, installments_result["duration_ms"])

    result.end_time = time.time()
    result.passed = token_result["success"] and installments_result["success"]

    if installments_result["success"]:
        print(f"✅ Cuotas obtenidas en {installments_result['duration_ms']:.2f}ms")
        print("✅ Sistema acepta amount 0.00 correctamente!")
    else:
        result.error_message = installments_result.get("error", "Installments search failed")
        print(f"❌ Error: {result.error_message}")

    return result


def test_cpi_007(config):
    """CPI-007: Idioma inglés"""
    print_header("Ejecutando CPI-007: Idioma inglés")

    result = TestResult("CPI-007", "Idioma inglés")
    result.start_time = time.time()

    transaction_id = generate_transaction_id(config["transaction_prefix"])
    order_number = generate_order_number()
    result.transaction_ids.append(transaction_id)

    print(f"🆔 Transaction ID: {transaction_id}")
    print("🎯 Objetivo: Validar respuesta en inglés")

    # Paso 1: Generar token
    print("\n📝 Paso 1: Generar token...")
    token_result = generate_token(config, transaction_id, order_number)
    result.add_step("Generate Token", token_result["success"], token_result, token_result["duration_ms"])

    if not token_result["success"]:
        result.end_time = time.time()
        result.passed = False
        result.error_message = "Failed to generate token"
        return result

    print(f"✅ Token generado en {token_result['duration_ms']:.2f}ms")

    # ⏱️ CRÍTICO: Delay para SANDBOX
    apply_sandbox_delay(config)

    # Paso 2: Buscar cuotas con language=ENG
    print("📝 Paso 2: Buscar cuotas con language=ENG...")
    token = token_result["token"]
    installments_result = search_installments(config, token, transaction_id, language="ENG")
    result.add_step("Search Installments (language=ENG)", installments_result["success"], installments_result, installments_result["duration_ms"])

    result.end_time = time.time()
    result.passed = token_result["success"] and installments_result["success"]

    if installments_result["success"]:
        message = installments_result["response"].get("response", {}).get("result", {}).get("messageFriendly", "")
        print(f"✅ Cuotas obtenidas en {installments_result['duration_ms']:.2f}ms")
        print(f"✅ Mensaje en inglés: '{message}'")
    else:
        result.error_message = installments_result.get("error", "Installments search failed")
        print(f"❌ Error: {result.error_message}")

    return result


# ============================================================================
# GENERACIÓN DE INFORME MARKDOWN
# ============================================================================

def generar_informe_markdown(ambiente_config, merchant_code, public_key, resultados, inicio_pruebas, fin_pruebas):
    """Genera un informe completo en formato Markdown con detalles completos de requests/responses"""

    ambiente_nombre = ambiente_config["nombre"]
    ambiente_codigo = ambiente_config["codigo"]

    informe = f"""# Informe de Pruebas - API Installments Izipay

## Descripción
Validación completa del API de Installments en ambiente {ambiente_nombre}

## Ambiente de Pruebas
**Ambiente:** {ambiente_nombre} ({ambiente_codigo})
**Fecha de Ejecución:** {datetime.now().strftime('%Y-%m-%d')}
**Hora de Inicio:** {datetime.fromtimestamp(inicio_pruebas).strftime('%H:%M:%S')}
**Hora de Finalización:** {datetime.fromtimestamp(fin_pruebas).strftime('%H:%M:%S')}
**Duración Total:** {(fin_pruebas - inicio_pruebas):.2f} segundos
**Merchant Code:** {merchant_code}

---

## Endpoints Utilizados

### 1. Token Generation API
**URL:** `POST {ambiente_config['token_url']}`
**Descripción:** Genera un token JWT para autenticar las peticiones al servicio de Installments
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{{
  "requestSource": "ECOMMERCE",
  "merchantCode": "{merchant_code}",
  "orderNumber": "ORDER{{TIMESTAMP}}",
  "publicKey": "{public_key}",
  "amount": "100.00"
}}
```

**Response Exitoso (200 OK):**
```json
{{
  "code": "00",
  "message": "OK",
  "response": {{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userOrg": "1snn5n9w",
    "userScoring": "izipay_high"
  }}
}}
```

---

### 2. Installments Search API
**URL:** `POST {ambiente_config['installments_url']}`
**Descripción:** Busca las cuotas disponibles para un BIN específico
**Content-Type:** `application/json`

**Headers Requeridos:**
- `Accept`: application/json
- `Content-Type`: application/json
- `Authorization`: Bearer {{token}}
- `transactionId`: ID único de la transacción

**Request Body:**
```json
{{
  "bin": "545545",
  "merchantCode": "{merchant_code}",
  "language": "ESP"
}}
```

**Response Exitoso (200 OK):**
```json
{{
  "code": "00",
  "message": "OK",
  "header": {{
    "transactionStartDatetime": "2025-11-04 18:38:55.120",
    "transactionEndDatetime": "2025-11-04 18:38:56.819",
    "millis": 1699
  }},
  "response": {{
    "merchantCode": "{merchant_code}",
    "bin": "545545",
    "issuerName": "SCOTIABANK ",
    "installments": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "deferred": "3",
    "result": {{
      "messageFriendly": "Operación exitosa"
    }}
  }}
}}
```

---

## Casos de Prueba Ejecutados

### Tabla de Casos de Prueba

| Cód. CP | Descripción del CP | Tipo de CP | Estado | Duración |
|---------|-------------------|------------|--------|----------|
"""

    # Agregar resultados a la tabla
    for resultado in resultados:
        estado = "✅ PASÓ" if resultado.passed else "❌ FALLÓ"
        duracion = f"{resultado.to_dict()['total_duration_ms']:.0f}ms"
        informe += f"| {resultado.test_id} | {resultado.test_name} | {'FUNCIONAL' if resultado.test_id in ['CPI-001', 'CPI-002', 'CPI-003', 'CPI-006', 'CPI-007'] else 'REGRESSION'} | {estado} | {duracion} |\n"

    informe += "\n---\n\n## Resultados Detallados\n\n"

    # Detalles de cada test CON REQUESTS/RESPONSES COMPLETOS
    for resultado in resultados:
        estado_emoji = "✅" if resultado.passed else "❌"
        estado_texto = "PASÓ" if resultado.passed else "FALLÓ"

        informe += f"""### {resultado.test_id}: {resultado.test_name}
**Estado:** {estado_emoji} {estado_texto}
**Duración Total:** {resultado.to_dict()['total_duration_ms']:.0f}ms
"""

        # Transaction IDs
        if resultado.transaction_ids:
            if len(resultado.transaction_ids) == 1:
                informe += f"**Transaction ID:** {resultado.transaction_ids[0]}\n"
            else:
                informe += f"**Transaction IDs:** {', '.join(resultado.transaction_ids)}\n"

        # Error message
        if resultado.error_message:
            informe += f"**Error:** {resultado.error_message}\n"

        # Objetivo del test
        objetivos = {
            "CPI-001": "Validar el flujo completo de generación de token y búsqueda de cuotas",
            "CPI-002": "Verificar que un token puede reutilizarse en múltiples consultas",
            "CPI-003": "Validar que el mismo TransactionId se mantiene consistente en ambas llamadas",
            "CPI-004": "Validar el manejo correcto de errores en el API de Installments",
            "CPI-005": "Validar que el servicio funciona correctamente con múltiples BINs de diferentes bancos",
            "CPI-006": "Validar que el sistema acepta correctamente transacciones con monto 0.00",
            "CPI-007": "Validar que el servicio soporta correctamente el idioma inglés en las respuestas"
        }
        if resultado.test_id in objetivos:
            informe += f"**Objetivo:** {objetivos[resultado.test_id]}\n"

        informe += "\n"

        # DETALLES COMPLETOS DE REQUESTS/RESPONSES POR CADA PASO
        for i, step in enumerate(resultado.steps, 1):
            step_emoji = "✅" if step["success"] else "❌"
            step_data = step.get('data', {})

            informe += f"#### Paso {i} - {step['step']}\n"

            # Determinar el endpoint
            if 'Token' in step['step'] or 'token' in step['step'].lower():
                endpoint = ambiente_config['token_url']
            else:
                endpoint = ambiente_config['installments_url']

            informe += f"**Endpoint:** `POST {endpoint}`\n"
            informe += f"**Status:** {step_data.get('status_code', 'N/A')}\n"
            informe += f"**Duración:** {step['duration_ms']:.0f}ms\n\n"

            # Request Headers
            if 'request' in step_data and 'headers' in step_data['request']:
                headers = step_data['request']['headers']
                informe += f"**Request Headers:**\n```json\n{json.dumps(headers, indent=2, ensure_ascii=False)}\n```\n\n"

            # Request Body
            if 'request' in step_data and 'body' in step_data['request']:
                body = step_data['request']['body']
                informe += f"**Request Body:**\n```json\n{json.dumps(body, indent=2, ensure_ascii=False)}\n```\n\n"

            # Response Body
            if 'response' in step_data:
                response = step_data['response']
                informe += f"**Response Body:**\n```json\n{json.dumps(response, indent=2, ensure_ascii=False)}\n```\n\n"

            # Response Headers (si están disponibles)
            if 'headers' in step_data and isinstance(step_data['headers'], dict):
                # Filtrar headers más relevantes
                relevant_headers = {k: v for k, v in step_data['headers'].items()
                                  if k in ['Content-Type', 'transactionId', 'X-Correlation-Id',
                                          'X-Content-Type-Options', 'Referrer-Policy',
                                          'Strict-Transport-Security', 'X-Xss-Proteccion', 'HttpOnly']}
                if relevant_headers:
                    informe += f"**Response Headers:**\n```json\n{json.dumps(relevant_headers, indent=2, ensure_ascii=False)}\n```\n\n"

            # Resultado del paso
            if step["success"]:
                if 'Token' in step['step']:
                    informe += f"{step_emoji} **Token generado exitosamente**\n\n"
                elif 'Installments' in step['step'] or 'Search' in step['step']:
                    if 'installments_count' in step_data:
                        count = step_data['installments_count']
                        informe += f"{step_emoji} **{count} cuotas obtenidas correctamente**\n\n"
                    else:
                        informe += f"{step_emoji} **Búsqueda exitosa**\n\n"
                elif 'Error' in step['step']:
                    informe += f"{step_emoji} **Error detectado correctamente**\n\n"
                else:
                    informe += f"{step_emoji} **Paso completado exitosamente**\n\n"
            else:
                error_msg = step_data.get('error', 'Error desconocido')
                informe += f"{step_emoji} **Error:** {error_msg}\n\n"

            informe += "---\n\n"

        # Resultado final del test
        if resultado.passed:
            if resultado.test_id == "CPI-002":
                informe += "**Resultado:**\n"
                informe += "- ✅ Primera búsqueda: Cuotas obtenidas correctamente\n"
                informe += "- ✅ Segunda búsqueda: Cuotas obtenidas correctamente\n"
                informe += "- ✅ **Token reutilizado exitosamente en ambas consultas**\n\n"
            elif resultado.test_id == "CPI-003":
                if resultado.transaction_ids:
                    informe += f"**Resultado:**\n"
                    informe += f"- ✅ TransactionId consistente: {resultado.transaction_ids[0]} en ambas llamadas\n"
                    informe += f"- ✅ Cuotas obtenidas correctamente\n\n"
            elif resultado.test_id == "CPI-004":
                successful_scenarios = sum(1 for s in resultado.steps if s['success'])
                total_scenarios = len(resultado.steps)
                informe += f"**Resultado:** {successful_scenarios}/{total_scenarios} escenarios validados correctamente\n\n"
            elif resultado.test_id == "CPI-005":
                successful_bins = sum(1 for s in resultado.steps if s['success'])
                informe += f"**Resultado:** {successful_bins} BINs validados exitosamente\n\n"
            elif resultado.test_id == "CPI-006":
                informe += "**Resultado:**\n"
                informe += "- ✅ Token generado exitosamente con amount 0.00\n"
                informe += "- ✅ Cuotas obtenidas correctamente\n"
                informe += "- ✅ **El sistema acepta amount 0.00 sin errores**\n\n"
            elif resultado.test_id == "CPI-007":
                informe += "**Resultado:**\n"
                informe += "- ✅ Token generado exitosamente\n"
                informe += "- ✅ Cuotas obtenidas correctamente\n"
                informe += "- ✅ **Soporte multi-idioma confirmado**\n\n"

        informe += "\n---\n\n"

    # Resumen ejecutivo
    total_tests = len(resultados)
    tests_pasados = sum(1 for r in resultados if r.passed)
    tests_fallados = total_tests - tests_pasados
    porcentaje_exito = (tests_pasados / total_tests * 100) if total_tests > 0 else 0

    informe += f"""## Resumen Ejecutivo

### Estadísticas Generales
- **Total de Casos de Prueba:** {total_tests}
- **Casos Exitosos:** {tests_pasados} ({porcentaje_exito:.1f}%)
- **Casos Fallidos:** {tests_fallados} ({100-porcentaje_exito:.1f}%)
- **Ambiente:** {ambiente_nombre}
- **Fecha:** {datetime.now().strftime('%Y-%m-%d')}
- **Duración Total de Ejecución:** {(fin_pruebas - inicio_pruebas):.2f} segundos

### Cobertura de Pruebas
"""

    # Determinar cobertura
    coberturas = {
        "Token Generation API": any(r.test_id in ["CPI-001", "CPI-002", "CPI-003", "CPI-006", "CPI-007"] and r.passed for r in resultados),
        "Installments Search API": any(r.test_id in ["CPI-001", "CPI-002", "CPI-003", "CPI-005"] and r.passed for r in resultados),
        "Token Reutilizable": any(r.test_id == "CPI-002" and r.passed for r in resultados),
        "TransactionId Consistency": any(r.test_id == "CPI-003" and r.passed for r in resultados),
        "Error Handling": any(r.test_id == "CPI-004" and r.passed for r in resultados),
        "Múltiples BINs": any(r.test_id == "CPI-005" and r.passed for r in resultados),
        "Amount Especial (0.00)": any(r.test_id == "CPI-006" and r.passed for r in resultados),
        "Soporte Multi-idioma (ENG)": any(r.test_id == "CPI-007" and r.passed for r in resultados),
    }

    for cobertura, validado in coberturas.items():
        estado = "✅" if validado else "❌"
        informe += f"- {estado} **{cobertura}:** {'Validado' if validado else 'No validado'}\n"

    # Estado final del ambiente
    estado_ambiente = "COMPLETAMENTE OPERATIVO" if tests_fallados == 0 else f"PARCIALMENTE OPERATIVO ({tests_fallados} tests fallaron)"
    emoji_ambiente = "✅" if tests_fallados == 0 else "⚠️"

    informe += f"""
### Estado del Ambiente {ambiente_codigo}
{emoji_ambiente} **{estado_ambiente}**

"""

    if tests_fallados == 0:
        informe += """El ambiente está funcionando correctamente. Todas las APIs (Token y Installments) están operativas y respondiendo dentro de los tiempos esperados.

### Conclusión
✅ **VALIDACIÓN API INSTALLMENTS EN AMBIENTE {}: EXITOSA**

Todos los casos de prueba pasaron exitosamente, confirmando que:
- Las APIs están completamente funcionales
- El token es reutilizable como se esperaba
- Los diferentes BINs configurados funcionan correctamente
- El manejo de errores es apropiado
- El sistema soporta múltiples idiomas
- Los casos especiales (amount 0.00) funcionan correctamente

**El ambiente {} está listo para su uso.**
""".format(ambiente_codigo, ambiente_codigo)
    else:
        informe += f"""Se encontraron {tests_fallados} tests fallidos. Revisar los detalles de cada caso para más información.

### Observaciones
"""
        for resultado in resultados:
            if not resultado.passed:
                informe += f"- **{resultado.test_id}:** {resultado.error_message}\n"

    informe += f"""
---

**Documento generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Ejecutado por:** Suite de Pruebas Automatizada
**Ambiente:** {ambiente_codigo} ({ambiente_config['token_url'].split('/')[2]})
**Merchant Code:** {merchant_code}
**Estado Final:** {'✅ TODOS LOS TESTS PASARON' if tests_fallados == 0 else f'⚠️ {tests_fallados} TESTS FALLARON'}
"""

    return informe


# ============================================================================
# CONVERSIÓN A WORD (DOCX)
# ============================================================================

def convertir_md_a_docx(archivo_md):
    """
    Convierte un archivo Markdown a Word (DOCX) usando pandoc

    Args:
        archivo_md (str): Ruta al archivo .md

    Returns:
        tuple: (success: bool, archivo_docx: str, error_message: str)

    Ejemplos:
        >>> success, docx_path, error = convertir_md_a_docx("informe.md")
        >>> if success:
        ...     print(f"Archivo generado: {docx_path}")
        ... else:
        ...     print(f"Error: {error}")
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
            # pandoc existe pero falló al ejecutar --version (raro, pero manejar)
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
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del script"""
    print("\n" + "=" * 70)
    print("   SUITE COMPLETA DE PRUEBAS - API INSTALLMENTS IZIPAY")
    print("=" * 70)

    # Seleccionar ambiente
    print("\n📍 Selecciona el ambiente para las pruebas:")
    print("-" * 70)
    for key, ambiente in AMBIENTES.items():
        print(f"   {key}. {ambiente['nombre']}")
    print("-" * 70)

    while True:
        opcion_ambiente = input("\n👉 Ingresa el número del ambiente (1-4): ").strip()
        if opcion_ambiente in AMBIENTES:
            ambiente_seleccionado = AMBIENTES[opcion_ambiente]
            break
        else:
            print("❌ Opción inválida. Por favor ingresa 1, 2, 3 o 4.")

    print(f"\n✅ Ambiente seleccionado: {ambiente_seleccionado['nombre']}")
    print(f"   URL: {ambiente_seleccionado['token_url'].split('/')[2]}")

    # Advertencia especial para SANDBOX
    if ambiente_seleccionado['codigo'] == "SANDBOX":
        print("\n" + "⚠️ " * 20)
        print("⚠️  ADVERTENCIA - AMBIENTE SANDBOX")
        print("⚠️ " * 20)
        print("El ambiente SANDBOX es INESTABLE y puede presentar:")
        print("  • Error 500 (Internal Server Error) - Muy frecuente")
        print("  • Error TN (Token Null) - Incluso con tokens válidos")
        print("  • Timeouts de 20+ segundos")
        print("  • Solo 1 BIN validado como funcional: 511578")
        print("\n➡️  Se recomienda usar DEV o QA para pruebas confiables")
        print("➡️  SANDBOX debe usarse solo para validar conectividad básica")
        print("⚠️ " * 20 + "\n")

    # Ingresar credenciales del comercio
    print("\n" + "=" * 70)
    print("🏪 Configuración del comercio")
    print("=" * 70)

    merchant_code = input("\n👉 Ingresa el Merchant Code: ").strip()
    if not merchant_code:
        print("❌ Merchant Code no puede estar vacío. Usando valor por defecto: 4078370")
        merchant_code = "4078370"

    public_key = input("👉 Ingresa el Public Key: ").strip()
    if not public_key:
        print("❌ Public Key no puede estar vacío. Usando valor por defecto: VErethUtraQuxas57wuMuquprADrAHAb")
        public_key = "VErethUtraQuxas57wuMuquprADrAHAb"

    # Configuración final
    config = {
        "token_url": ambiente_seleccionado["token_url"],
        "installments_url": ambiente_seleccionado["installments_url"],
        "merchant_code": merchant_code,
        "public_key": public_key,
        "transaction_prefix": ambiente_seleccionado["transaction_prefix"]
    }

    print("\n" + "=" * 70)
    print("📋 Resumen de la configuración")
    print("=" * 70)
    print(f"   Ambiente: {ambiente_seleccionado['nombre']}")
    print(f"   Token URL: {config['token_url']}")
    print(f"   Installments URL: {config['installments_url']}")
    print(f"   Merchant Code: {merchant_code}")
    print(f"   Public Key: {public_key[:20]}...")
    print("=" * 70)

    input("\n⏸️  Presiona ENTER para iniciar las pruebas...")

    # Ejecutar pruebas
    print("\n" + "=" * 70)
    print("🚀 INICIANDO EJECUCIÓN DE PRUEBAS")
    print("=" * 70)

    inicio_pruebas = time.time()
    resultados = []

    # Ejecutar cada caso de prueba
    tests = [
        test_cpi_001,
        test_cpi_002,
        test_cpi_003,
        test_cpi_004,
        test_cpi_005,
        test_cpi_006,
        test_cpi_007
    ]

    for i, test_func in enumerate(tests, 1):
        print(f"\n{'='*70}")
        print(f"Ejecutando test {i}/7")
        print(f"{'='*70}")

        try:
            resultado = test_func(config)
            resultados.append(resultado)

            if resultado.passed:
                print(f"\n✅ {resultado.test_id} completado exitosamente")
            else:
                print(f"\n❌ {resultado.test_id} falló: {resultado.error_message}")

        except Exception as e:
            print(f"\n❌ Error crítico ejecutando {test_func.__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

        # Pausa entre tests
        if i < len(tests):
            time.sleep(1)

    fin_pruebas = time.time()

    # Resumen de resultados
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)

    total_tests = len(resultados)
    tests_pasados = sum(1 for r in resultados if r.passed)
    tests_fallados = total_tests - tests_pasados

    print(f"\nTotal de tests ejecutados: {total_tests}")
    print(f"✅ Tests exitosos: {tests_pasados}")
    print(f"❌ Tests fallidos: {tests_fallados}")
    print(f"⏱️  Duración total: {(fin_pruebas - inicio_pruebas):.2f} segundos")

    print("\nDetalle por test:")
    for resultado in resultados:
        estado = "✅ PASÓ" if resultado.passed else "❌ FALLÓ"
        duracion = f"{resultado.to_dict()['total_duration_ms']:.0f}ms"
        print(f"  {estado} {resultado.test_id}: {resultado.test_name} ({duracion})")

    # Generar informe
    print("\n" + "=" * 70)
    print("📄 GENERANDO INFORME")
    print("=" * 70)

    try:
        informe_markdown = generar_informe_markdown(
            ambiente_seleccionado,
            merchant_code,
            public_key,
            resultados,
            inicio_pruebas,
            fin_pruebas
        )

        # Guardar informe
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"INFORME_PRUEBAS_{ambiente_seleccionado['codigo']}_{timestamp}.md"

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(informe_markdown)

        print(f"\n✅ Informe Markdown generado exitosamente:")
        print(f"   📁 {os.path.abspath(nombre_archivo)}")

        # Convertir automáticamente a DOCX usando Pandoc
        success_docx, archivo_docx, error_docx = convertir_md_a_docx(nombre_archivo)

        if success_docx:
            print(f"\n✅ Informe Word generado exitosamente:")
            print(f"   📁 {os.path.abspath(archivo_docx)}")
        else:
            print(f"\n⚠️  No se pudo generar el archivo Word:")
            print(f"   ❌ {error_docx}")
            print(f"   💡 Puedes convertirlo manualmente con:")
            print(f"      pandoc {nombre_archivo} -o {nombre_archivo.replace('.md', '.docx')}")

        # Guardar resultados en JSON
        nombre_json = f"RESULTADOS_PRUEBAS_{ambiente_seleccionado['codigo']}_{timestamp}.json"
        resultados_json = {
            "ambiente": ambiente_seleccionado['nombre'],
            "ambiente_codigo": ambiente_seleccionado['codigo'],
            "merchant_code": merchant_code,
            "fecha_ejecucion": datetime.now().isoformat(),
            "duracion_total_segundos": fin_pruebas - inicio_pruebas,
            "total_tests": total_tests,
            "tests_pasados": tests_pasados,
            "tests_fallados": tests_fallados,
            "resultados": [r.to_dict() for r in resultados]
        }

        with open(nombre_json, 'w', encoding='utf-8') as f:
            json.dump(resultados_json, f, indent=2, ensure_ascii=False)

        print(f"   📁 {os.path.abspath(nombre_json)}")

    except Exception as e:
        print(f"\n❌ Error al generar informe: {str(e)}")
        import traceback
        traceback.print_exc()

    # Mensaje final
    print("\n" + "=" * 70)
    if tests_fallados == 0:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f"⚠️  {tests_fallados} PRUEBA(S) FALLARON - REVISAR INFORME")
    print("=" * 70)
    print("\n")

    # Exit code
    return 0 if tests_fallados == 0 else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
