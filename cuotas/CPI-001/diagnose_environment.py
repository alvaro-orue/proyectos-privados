"""
Script de diagnóstico del ambiente QA de Izipay
Verifica conectividad y estado de los servicios
"""

import requests
import json
import socket
from datetime import datetime
import sys

# Configurar codificación UTF-8 para la salida
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración
ENDPOINTS = {
    "Generate Token": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
    "Search Installments": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search"
}

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_dns_resolution(hostname):
    """Verifica resolución DNS"""
    print(f"\n🔍 Verificando resolución DNS para {hostname}...")
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS resuelto: {hostname} -> {ip_address}")
        return True, ip_address
    except socket.gaierror as e:
        print(f"❌ Error de DNS: {e}")
        return False, None

def check_connectivity(url, name):
    """Verifica conectividad con un endpoint"""
    print(f"\n🔌 Verificando conectividad con {name}...")
    print(f"   URL: {url}")

    try:
        # Intentar HEAD request
        response = requests.head(url, timeout=10, allow_redirects=True)
        print(f"✅ Conexión establecida")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers:")
        for key, value in response.headers.items():
            print(f"     {key}: {value}")
        return True, response.status_code
    except requests.exceptions.Timeout:
        print(f"❌ Timeout al conectar (>10 segundos)")
        return False, "TIMEOUT"
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        return False, "CONNECTION_ERROR"
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en request: {e}")
        return False, "REQUEST_ERROR"

def test_endpoint_without_auth(url, name):
    """Prueba endpoint sin autenticación para verificar respuesta"""
    print(f"\n🧪 Probando {name} sin autenticación...")
    print(f"   (Esperamos un error de autenticación, no un 500)")

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={},
            timeout=10
        )
        print(f"   Status Code: {response.status_code}")

        try:
            body = response.json()
            print(f"   Response: {json.dumps(body, indent=2)}")
        except:
            print(f"   Response Body: {response.text[:200]}")

        # Si recibimos 401/403, el servicio está funcionando
        if response.status_code in [401, 403, 400]:
            print(f"✅ Servicio responde correctamente (error de auth esperado)")
            return True
        elif response.status_code == 500:
            print(f"⚠️  Servicio retorna 500 - Posible problema del servidor")
            return False
        else:
            print(f"ℹ️  Respuesta inesperada: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print(f"❌ Timeout al probar endpoint (>10 segundos)")
        return False
    except Exception as e:
        print(f"❌ Error al probar endpoint: {e}")
        return False

def run_diagnostics():
    """Ejecuta diagnóstico completo"""
    print_header("DIAGNÓSTICO DEL AMBIENTE QA - IZIPAY")
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "timestamp": datetime.now().isoformat(),
        "checks": []
    }

    # Extraer hostname
    hostname = "qa-api-pw.izipay.pe"

    # 1. Verificar DNS
    print_header("1. VERIFICACIÓN DNS")
    dns_ok, ip = check_dns_resolution(hostname)
    results["checks"].append({
        "test": "DNS Resolution",
        "passed": dns_ok,
        "details": {"hostname": hostname, "ip": ip}
    })

    if not dns_ok:
        print("\n⚠️  No se puede resolver DNS. Verificar conectividad de red.")
        return results

    # 2. Verificar conectividad con cada endpoint
    print_header("2. VERIFICACIÓN DE CONECTIVIDAD")

    connectivity_ok = True
    for name, url in ENDPOINTS.items():
        conn_ok, status = check_connectivity(url, name)
        results["checks"].append({
            "test": f"Connectivity - {name}",
            "passed": conn_ok,
            "details": {"url": url, "status": status}
        })
        if not conn_ok:
            connectivity_ok = False

    # 3. Probar endpoints sin autenticación
    print_header("3. PRUEBA DE ENDPOINTS")

    for name, url in ENDPOINTS.items():
        test_ok = test_endpoint_without_auth(url, name)
        results["checks"].append({
            "test": f"Endpoint Test - {name}",
            "passed": test_ok,
            "details": {"url": url}
        })

    # Resumen
    print_header("RESUMEN DE DIAGNÓSTICO")

    passed = sum(1 for check in results["checks"] if check["passed"] is True)
    failed = sum(1 for check in results["checks"] if check["passed"] is False)
    unknown = sum(1 for check in results["checks"] if check["passed"] is None)
    total = len(results["checks"])

    print(f"\n📊 Resultados:")
    print(f"   Total de pruebas: {total}")
    print(f"   ✅ Exitosas: {passed}")
    print(f"   ❌ Fallidas: {failed}")
    print(f"   ⚠️  Indeterminadas: {unknown}")

    if failed == 0 and unknown == 0:
        print(f"\n✅ Todos los servicios están operativos")
        overall_status = "HEALTHY"
    elif failed > 0:
        print(f"\n⚠️  Se detectaron problemas en los servicios")
        overall_status = "UNHEALTHY"
    else:
        print(f"\n⚠️  Estado indeterminado")
        overall_status = "UNKNOWN"

    results["overall_status"] = overall_status

    # Guardar resultados
    print_header("GUARDANDO RESULTADOS")

    with open("diagnostic_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Resultados guardados en: diagnostic_results.json")

    # Recomendaciones
    print_header("RECOMENDACIONES")

    if overall_status == "UNHEALTHY":
        print("\n📋 Acciones recomendadas:")
        print("   1. Verificar que los servicios de QA estén levantados")
        print("   2. Contactar al equipo de DevOps/Infraestructura")
        print("   3. Revisar logs del servidor para el timestamp actual")
        print("   4. Considerar probar en ambiente Sandbox como alternativa")
    elif overall_status == "HEALTHY":
        print("\n📋 Los servicios están operativos:")
        print("   1. El error 500 puede ser específico del caso de prueba")
        print("   2. Verificar configuración del merchant en QA")
        print("   3. Validar que el BIN esté registrado en QA")
        print("   4. Revisar logs de aplicación para más detalles")

    print("\n" + "=" * 70)

    return results

if __name__ == "__main__":
    try:
        results = run_diagnostics()

        # Exit code basado en el estado
        if results.get("overall_status") == "HEALTHY":
            exit(0)
        else:
            exit(1)

    except Exception as e:
        print(f"\n❌ Error crítico durante diagnóstico: {e}")
        import traceback
        traceback.print_exc()
        exit(2)
