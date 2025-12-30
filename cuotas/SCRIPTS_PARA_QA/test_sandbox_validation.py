"""
Test de Validación SANDBOX - Merchant 4001834
Prueba el único BIN que funciona: 511578 (BBVA MC Platinum)
"""
import requests, json, time, sys
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CONFIG = {
    "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
    "merchant_code": "4001834",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}

def run_test():
    print("=" * 70)
    print("VALIDACIÓN SANDBOX - Merchant 4001834")
    print("BIN: 511578 (BBVA MC Platinum) - ÚNICO BIN CONFIRMADO")
    print("=" * 70)

    now = datetime.now()
    txn_id = f"SBX{now.strftime('%Y%m%d%H%M%S')}"
    order = f"ORDER{now.strftime('%Y%m%d%H%M%S')}"

    # PASO 1: Generate Token
    print(f"\n🆔 TransactionId: {txn_id}")
    print("📤 PASO 1: Generate Token")
    t1 = time.time()
    r1 = requests.post(CONFIG["token_url"],
                       headers={"Accept": "application/json", "Content-Type": "application/json", "transactionId": txn_id},
                       json={"requestSource": "ECOMMERCE", "merchantCode": CONFIG["merchant_code"], "orderNumber": order,
                             "publicKey": CONFIG["public_key"], "amount": "100.00"}, timeout=30)
    d1 = (time.time() - t1) * 1000
    print(f"⏱️  {d1:.0f}ms - Status: {r1.status_code}")

    if r1.status_code != 200 or r1.json().get("code") != "00":
        print(f"❌ FALLÓ Token Generation: {r1.json()}")
        return False

    token = r1.json()["response"]["token"]
    print(f"✅ Token: {token[:40]}...")

    # PASO 2: Search Installments con BIN 511578
    print("\n📤 PASO 2: Search Installments (BIN 511578)")
    time.sleep(1)  # Delay
    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"],
                       headers={"Accept": "application/json", "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}", "transactionId": txn_id},
                       json={"bin": "511578", "merchantCode": CONFIG["merchant_code"], "language": "ESP"}, timeout=30)
    d2 = (time.time() - t2) * 1000
    print(f"⏱️  {d2:.0f}ms - Status: {r2.status_code}")

    if r2.status_code == 200 and r2.json().get("code") == "00":
        cuotas = len(r2.json()["response"]["installments"])
        print(f"✅ Cuotas disponibles: {cuotas}")
        print(f"\n✅ PASÓ - Total: {d1+d2:.0f}ms")
        print(f"\n📊 Detalle de cuotas:")
        for inst in r2.json()["response"]["installments"][:5]:  # Mostrar primeras 5
            print(f"   - {inst['cuota']} cuota(s), Diferido: {inst['mes_diferido']} meses, TEA: {inst['tea']}%")
        return True
    else:
        print(f"❌ FALLÓ Search: {r2.json()}")
        return False

if __name__ == "__main__":
    passed = run_test()
    print("\n" + "=" * 70)
    if passed:
        print("✅ SANDBOX VALIDADO - BIN 511578 funciona correctamente")
    else:
        print("❌ SANDBOX FALLÓ - Revisar configuración del merchant")
    print("=" * 70)
    exit(0 if passed else 1)
