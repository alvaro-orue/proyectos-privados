"""Script CPI-006: Amount 0.00 - FVCL Format"""
import requests, json, time, os, sys
from datetime import datetime
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CONFIG = {"token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
          "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
          "merchant_code": "4078370", "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"}

def run_test():
    print("=" * 60)
    print("CPI-006: Flujo con Amount 0.00")
    print("=" * 60)
    now = datetime.now()
    txn_id = f"FVCL{now.strftime('%Y%m%d%H%M%S')}"
    order = f"ORDER{now.strftime('%Y%m%d%H%M%S')}"

    # Paso 1: Generate Token con amount 0.00
    print(f"\n🆔 TransactionId: {txn_id}")
    print("📤 PASO 1: Generate Token (amount=0.00)")
    t1 = time.time()
    r1 = requests.post(CONFIG["token_url"], headers={"Accept": "application/json", "Content-Type": "application/json", "transactionId": txn_id},
                       json={"requestSource": "ECOMMERCE", "merchantCode": CONFIG["merchant_code"], "orderNumber": order,
                             "publicKey": CONFIG["public_key"], "amount": "0.00"}, timeout=30)
    d1 = (time.time() - t1) * 1000
    print(f"⏱️  {d1:.0f}ms - Status: {r1.status_code}")

    if r1.status_code != 200 or r1.json().get("code") != "00":
        print(f"❌ FALLÓ: {r1.json()}")
        return False, d1, 0

    token = r1.json()["response"]["token"]
    print(f"✅ Token: {token[:40]}...")

    # Paso 2: Search Installments
    print("\n📤 PASO 2: Search Installments")
    t2 = time.time()
    r2 = requests.post(CONFIG["installments_url"], headers={"Accept": "application/json", "Content-Type": "application/json",
                       "Authorization": f"Bearer {token}", "transactionId": txn_id},
                       json={"bin": "545545", "merchantCode": CONFIG["merchant_code"], "language": "ESP"}, timeout=30)
    d2 = (time.time() - t2) * 1000
    print(f"⏱️  {d2:.0f}ms - Status: {r2.status_code}")

    if r2.status_code == 200 and r2.json().get("code") == "00":
        cuotas = len(r2.json()["response"]["installments"])
        print(f"✅ Cuotas: {cuotas}")
        print(f"\n✅ PASÓ - Total: {d1+d2:.0f}ms")
        return True, d1, d2
    else:
        print(f"❌ FALLÓ: {r2.json()}")
        return False, d1, d2

if __name__ == "__main__":
    passed, t1, t2 = run_test()
    with open(os.path.join(os.path.dirname(__file__), "test_report.txt"), "w") as f:
        f.write(f"CPI-006: Amount 0.00\n")
        f.write(f"Estado: {'✅ PASÓ' if passed else '❌ FALLÓ'}\n")
        f.write(f"Generate Token: {t1:.0f}ms\n")
        f.write(f"Search Install: {t2:.0f}ms\n")
        f.write(f"Total: {t1+t2:.0f}ms\n")
    exit(0 if passed else 1)
