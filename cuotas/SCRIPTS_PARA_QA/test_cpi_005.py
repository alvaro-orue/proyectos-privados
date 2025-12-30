"""Script CPI-005: Diferentes BINs - FVCL Format"""
import requests, json, time, os, sys
from datetime import datetime
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Importar configuración de ambientes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config_environments import get_environment

# Obtener configuración del ambiente (DEV por defecto, o desde argumento)
env_name = sys.argv[1] if len(sys.argv) > 1 else "DEV"
env_config = get_environment(env_name)
CONFIG = {"token_url": env_config["token_url"],
          "installments_url": env_config["installments_url"],
          "merchant_code": env_config["merchant_code"],
          "public_key": env_config["public_key"]}

# BINs según el ambiente - Verificados en Excel de SANDBOX
# DEV/QA: 545545, 400917, 377893, 553650
# SANDBOX: Todos los BINs validados que existen en ResultsSandBoxBin.xlsx
if env_name == "SANDBOX":
    BINS = [
        ("545545", "SCOTIABANK MC"),        # Verificado en Excel SANDBOX
        ("510308", "SCOTIABANK MC"),        # Verificado en Excel SANDBOX
        ("553650", "BBVA MC"),              # Verificado en Excel SANDBOX
        ("511578", "BBVA MC"),              # Verificado en Excel SANDBOX
    ]
else:  # DEV/QA
    BINS = [
        ("545545", "SCOTIABANK"),           # 12 cuotas, 3 meses diferido (DEV/QA)
        ("400917", "SCOTIABANK VISA"),      # 36 cuotas, 0 meses diferido
        ("377893", "BCP"),                  # 36 cuotas, 3 meses diferido (solo DEV/QA)
        ("553650", "BBVA MC Platinum"),     # 36 cuotas, 3 meses diferido
    ]

def test_bin(bin_num, expected):
    now = datetime.now()
    txn_id = f"{env_config['transaction_prefix']}{now.strftime('%Y%m%d%H%M%S')}"
    order = f"ORDER{now.strftime('%Y%m%d%H%M%S')}"

    try:
        # Generate Token
        t1 = time.time()
        r1 = requests.post(CONFIG["token_url"], headers={"Accept": "application/json", "Content-Type": "application/json", "transactionId": txn_id},
                           json={"requestSource": "ECOMMERCE", "merchantCode": CONFIG["merchant_code"], "orderNumber": order,
                                 "publicKey": CONFIG["public_key"], "amount": "100.00"}, timeout=60)
        d1 = (time.time() - t1) * 1000

        if r1.status_code != 200 or r1.json().get("code") != "00":
            print(f"   ❌ Error en token: {r1.status_code} - {r1.json()}")
            return False, 0, d1, 0

        token = r1.json()["response"]["token"]

        # Pequeño delay para evitar problemas de timing
        time.sleep(1)

        # Search Installments
        t2 = time.time()
        r2 = requests.post(CONFIG["installments_url"], headers={"Accept": "application/json", "Content-Type": "application/json",
                           "Authorization": f"Bearer {token}", "transactionId": txn_id},
                           json={"bin": bin_num, "merchantCode": CONFIG["merchant_code"], "language": "ESP"}, timeout=60)
        d2 = (time.time() - t2) * 1000

        if r2.status_code == 200 and r2.json().get("code") == "00":
            cuotas = len(r2.json()["response"]["installments"])
            issuer = r2.json()["response"].get("issuerName", "").strip()
            return True, cuotas, d1, d2
        else:
            print(f"   ❌ Error en search: {r2.status_code} - {r2.json().get('code', 'N/A')}")
            return False, 0, d1, d2
    except Exception as e:
        print(f"   ❌ Excepción: {str(e)[:80]}")
        return False, 0, 0, 0

def run_test():
    print("=" * 60)
    print("CPI-005: Diferentes BINs")
    print("=" * 60)

    results = []
    for bin_num, expected in BINS:
        print(f"\n📤 Probando BIN: {bin_num} ({expected})")
        passed, cuotas, t1, t2 = test_bin(bin_num, expected)
        results.append((bin_num, expected, passed, cuotas, t1, t2))
        if passed:
            print(f"✅ {cuotas} cuotas - Token:{t1:.0f}ms Search:{t2:.0f}ms")
        else:
            print(f"❌ FALLÓ")
        time.sleep(1)  # Evitar sobrecarga

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    passed_count = sum(1 for r in results if r[2])
    print(f"Total: {len(results)} | Exitosos: {passed_count} | Fallidos: {len(results)-passed_count}")

    with open(os.path.join(os.path.dirname(__file__), "test_report.txt"), "w", encoding="utf-8") as f:
        f.write("CPI-005: Diferentes BINs\n")
        f.write(f"Exitosos: {passed_count}/{len(results)}\n\n")
        for bin_num, exp, passed, cuotas, t1, t2 in results:
            f.write(f"{bin_num} ({exp}): {'PASO' if passed else 'FALLO'} - {cuotas} cuotas\n")

    return passed_count == len(results)

if __name__ == "__main__":
    all_passed = run_test()
    exit(0 if all_passed else 1)
