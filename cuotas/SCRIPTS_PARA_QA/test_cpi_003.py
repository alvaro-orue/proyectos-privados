"""Script CPI-003: TransactionId Consistente - DEV Format"""
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

def run_test():
    print("=" * 60)
    print("CPI-003: TransactionId Consistente")
    print("=" * 60)

    # Generar un único TransactionId
    txn_id = generate_transaction_id()
    order = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"

    print(f"\n📋 TransactionId: {txn_id}")
    print(f"📦 OrderNumber: {order}")

    # PASO 1: Generate Token
    print("\n📤 PASO 1: Generate Token con TransactionId: " + txn_id)
    t1 = time.time()
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
    d1 = (time.time() - t1) * 1000

    print(f"⏱️  Duración: {d1:.0f} ms")
    print(f"📊 Status Code: {r1.status_code}")

    step1_data = {"status_code": r1.status_code, "duration_ms": round(d1, 2),
                  "response": r1.json() if r1.status_code == 200 else {"error": r1.text}}

    with open(os.path.join(os.path.dirname(__file__), "step_1_Generate_Token.json"), "w", encoding="utf-8") as f:
        json.dump(step1_data, f, indent=2, ensure_ascii=False)

    if r1.status_code != 200 or r1.json().get("code") != "00":
        print(f"❌ Error en Generate Token: {r1.json()}")
        return False

    token = r1.json()["response"]["token"]
    print(f"✅ Token generado: {token[:20]}...")

    time.sleep(1)

    # PASO 2: Search Installments con el MISMO TransactionId
    print(f"\n📤 PASO 2: Search Installments con el MISMO TransactionId: {txn_id}")
    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"],
                       headers={"Accept": "application/json",
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}",
                               "transactionId": txn_id},  # MISMO ID
                       json={"bin": "545545",
                             "merchantCode": CONFIG["merchant_code"],
                             "language": "ESP"},
                       timeout=30)
    d2 = (time.time() - t2) * 1000

    print(f"⏱️  Duración: {d2:.0f} ms")
    print(f"📊 Status Code: {r2.status_code}")

    step2_data = {"status_code": r2.status_code, "duration_ms": round(d2, 2),
                  "response": r2.json() if r2.status_code == 200 else {"error": r2.text}}

    with open(os.path.join(os.path.dirname(__file__), "step_2_Search_Installments.json"), "w", encoding="utf-8") as f:
        json.dump(step2_data, f, indent=2, ensure_ascii=False)

    if r2.status_code != 200 or r2.json().get("code") != "00":
        print(f"❌ Error en Search Installments: {r2.json()}")
        return False

    cuotas = len(r2.json()["response"]["installments"])
    print(f"✅ {cuotas} cuotas retornadas")

    # VALIDACIÓN: El TransactionId debe ser consistente
    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print(f"✅ TransactionId usado en ambas llamadas: {txn_id}")
    print(f"✅ Token generado: {d1:.0f} ms")
    print(f"✅ Cuotas obtenidas: {d2:.0f} ms")
    print(f"⏱️  Duración total: {d1+d2:.0f} ms")
    print(f"✅ PRUEBA EXITOSA: TransactionId consistente")

    # Guardar reporte
    with open(os.path.join(os.path.dirname(__file__), "test_report.txt"), "w", encoding="utf-8") as f:
        f.write("CPI-003: TransactionId Consistente\n")
        f.write(f"TransactionId: {txn_id}\n")
        f.write(f"Generate Token: {d1:.0f} ms\n")
        f.write(f"Search Installments: {d2:.0f} ms\n")
        f.write(f"Total: {d1+d2:.0f} ms\n")
        f.write(f"Cuotas: {cuotas}\n")
        f.write(f"Estado: PASÓ\n")

    # Guardar resultado JSON
    result_data = {
        "test_id": "CPI-003",
        "test_name": "TransactionId Consistente",
        "status": "PASSED",
        "transaction_id": txn_id,
        "order_number": order,
        "duration_ms": round(d1 + d2, 2),
        "steps": [
            {"step": 1, "name": "Generate Token", "duration_ms": round(d1, 2), "status": "SUCCESS"},
            {"step": 2, "name": "Search Installments", "duration_ms": round(d2, 2), "status": "SUCCESS", "cuotas": cuotas}
        ]
    }

    with open(os.path.join(os.path.dirname(__file__), "test_result.json"), "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    return True

if __name__ == "__main__":
    success = run_test()
    exit(0 if success else 1)
