"""Script CPI-004: Casos de Error - DEV Format"""
import requests, json, time, os, sys
from datetime import datetime
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CONFIG = {"token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
          "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
          "merchant_code": "4001834", "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"}

def generate_transaction_id():
    """Genera transactionId: DEV + YYYYMMDDHHMMSS"""
    return f"DEV{datetime.now().strftime('%Y%m%d%H%M%S')}"

def test_error_scenario(name, test_func):
    """Ejecuta un escenario de error y valida que falle correctamente"""
    print(f"\n{'='*60}")
    print(f"Escenario: {name}")
    print('='*60)

    try:
        should_fail, status_code, response, duration = test_func()

        if should_fail and status_code != 200:
            print(f"✅ Error detectado correctamente")
            print(f"   Status Code: {status_code}")
            print(f"   Duración: {duration:.0f} ms")
            return True, status_code, response, duration
        elif should_fail and status_code == 200:
            print(f"⚠️ Debería haber fallado pero respondió OK")
            return False, status_code, response, duration
        else:
            print(f"✅ Respuesta exitosa")
            return True, status_code, response, duration
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        return False, 0, {"error": str(e)}, 0

# ESCENARIO 1: Token inválido
def test_invalid_token():
    txn_id = generate_transaction_id()
    print(f"📤 Intentando Search con token INVÁLIDO")

    t1 = time.time()
    r = requests.post(CONFIG["installments_url"],
                      headers={"Accept": "application/json",
                              "Content-Type": "application/json",
                              "Authorization": "Bearer INVALID_TOKEN_12345",
                              "transactionId": txn_id},
                      json={"bin": "545545",
                            "merchantCode": CONFIG["merchant_code"],
                            "language": "ESP"},
                      timeout=30)
    d = (time.time() - t1) * 1000

    return True, r.status_code, r.json() if r.status_code == 200 else r.text, d

# ESCENARIO 2: Sin header Authorization
def test_missing_auth_header():
    txn_id = generate_transaction_id()
    print(f"📤 Intentando Search SIN header Authorization")

    t1 = time.time()
    r = requests.post(CONFIG["installments_url"],
                      headers={"Accept": "application/json",
                              "Content-Type": "application/json",
                              "transactionId": txn_id},
                      json={"bin": "545545",
                            "merchantCode": CONFIG["merchant_code"],
                            "language": "ESP"},
                      timeout=30)
    d = (time.time() - t1) * 1000

    return True, r.status_code, r.json() if r.status_code == 200 else r.text, d

# ESCENARIO 3: BIN con formato inválido
def test_invalid_bin_format():
    # Primero generar token válido
    txn_id = generate_transaction_id()
    order = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"

    r1 = requests.post(CONFIG["token_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "transactionId": txn_id},
                       json={"requestSource": "ECOMMERCE",
                             "merchantCode": CONFIG["merchant_code"],
                             "orderNumber": order,
                             "publicKey": CONFIG["public_key"],
                             "amount": "100.00"},
                       timeout=30)

    if r1.status_code != 200:
        return False, r1.status_code, r1.text, 0

    token = r1.json()["response"]["token"]

    print(f"📤 Intentando Search con BIN inválido (ABC)")

    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}",
                               "transactionId": txn_id},
                       json={"bin": "ABC",  # BIN inválido
                             "merchantCode": CONFIG["merchant_code"],
                             "language": "ESP"},
                       timeout=30)
    d = (time.time() - t2) * 1000

    return True, r2.status_code, r2.json() if r2.status_code == 200 else r2.text, d

# ESCENARIO 4: Merchant Code inválido
def test_invalid_merchant():
    txn_id = generate_transaction_id()
    order = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"

    r1 = requests.post(CONFIG["token_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "transactionId": txn_id},
                       json={"requestSource": "ECOMMERCE",
                             "merchantCode": CONFIG["merchant_code"],
                             "orderNumber": order,
                             "publicKey": CONFIG["public_key"],
                             "amount": "100.00"},
                       timeout=30)

    if r1.status_code != 200:
        return False, r1.status_code, r1.text, 0

    token = r1.json()["response"]["token"]

    print(f"📤 Intentando Search con merchantCode INVÁLIDO (9999999)")

    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}",
                               "transactionId": txn_id},
                       json={"bin": "545545",
                             "merchantCode": "9999999",  # Merchant inválido
                             "language": "ESP"},
                       timeout=30)
    d = (time.time() - t2) * 1000

    return True, r2.status_code, r2.json() if r2.status_code == 200 else r2.text, d

# ESCENARIO 5: Parámetro BIN faltante
def test_missing_bin():
    txn_id = generate_transaction_id()
    order = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"

    r1 = requests.post(CONFIG["token_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "transactionId": txn_id},
                       json={"requestSource": "ECOMMERCE",
                             "merchantCode": CONFIG["merchant_code"],
                             "orderNumber": order,
                             "publicKey": CONFIG["public_key"],
                             "amount": "100.00"},
                       timeout=30)

    if r1.status_code != 200:
        return False, r1.status_code, r1.text, 0

    token = r1.json()["response"]["token"]

    print(f"📤 Intentando Search SIN parámetro BIN")

    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}",
                               "transactionId": txn_id},
                       json={"merchantCode": CONFIG["merchant_code"],  # Sin BIN
                             "language": "ESP"},
                       timeout=30)
    d = (time.time() - t2) * 1000

    return True, r2.status_code, r2.json() if r2.status_code == 200 else r2.text, d

def run_test():
    print("=" * 60)
    print("CPI-004: Casos de Error")
    print("=" * 60)

    results = []

    # Ejecutar todos los escenarios
    scenarios = [
        ("Error 1: Token Inválido", test_invalid_token),
        ("Error 2: Sin Header Authorization", test_missing_auth_header),
        ("Error 3: BIN con Formato Inválido", test_invalid_bin_format),
        ("Error 4: Merchant Code Inválido", test_invalid_merchant),
        ("Error 5: Parámetro BIN Faltante", test_missing_bin)
    ]

    for name, test_func in scenarios:
        success, status_code, response, duration = test_error_scenario(name, test_func)
        results.append({
            "name": name,
            "success": success,
            "status_code": status_code,
            "response": response,
            "duration_ms": round(duration, 2)
        })
        time.sleep(1)  # Pausa entre tests

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    passed = sum(1 for r in results if r["success"])
    total = len(results)

    print(f"Total escenarios: {total}")
    print(f"✅ Validados correctamente: {passed}")
    print(f"❌ Con problemas: {total - passed}")

    # Guardar resultados
    with open(os.path.join(os.path.dirname(__file__), "test_result.json"), "w", encoding="utf-8") as f:
        json.dump({
            "test_id": "CPI-004",
            "test_name": "Casos de Error",
            "total_scenarios": total,
            "passed": passed,
            "failed": total - passed,
            "scenarios": results
        }, f, indent=2, ensure_ascii=False)

    with open(os.path.join(os.path.dirname(__file__), "test_report.txt"), "w", encoding="utf-8") as f:
        f.write("CPI-004: Casos de Error\n")
        f.write(f"Total: {total} | Validados: {passed} | Con problemas: {total - passed}\n\n")
        for r in results:
            status = "✅" if r["success"] else "❌"
            f.write(f"{status} {r['name']}\n")
            f.write(f"   Status Code: {r['status_code']}\n")
            f.write(f"   Duración: {r['duration_ms']} ms\n\n")

    return passed == total

if __name__ == "__main__":
    all_passed = run_test()
    exit(0 if all_passed else 1)
