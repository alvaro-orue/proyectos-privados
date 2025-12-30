#!/usr/bin/env python3
"""
Script de Automatización Interactiva - Casos de Prueba Depósito Izipay

Este script guía al usuario paso a paso para:
1. Ingresar credenciales de comercio
2. Generar 9 pagos en el checkout demo de Izipay
3. Copiar y pegar los Payment Responses
4. Ejecutar automáticamente los 9 depósitos
5. Generar informe consolidado

Casos de prueba: CP-POS-001 a CP-POS-009 de CASOS_PRUEBA_POSITIVOS.md

Autor: Claude Code
Fecha: 2025-11-18
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime


class AutomatizacionInteractiva:
    def __init__(self):
        self.merchant_code = None
        self.api_key = None
        self.payment_dir = Path("payment_responses")
        self.payment_dir.mkdir(exist_ok=True)

        # Casos de prueba a ejecutar (solo 9 primeros)
        self.test_cases = [
            {
                "id": "CP-POS-001",
                "descripcion": "Depósito CARD en PEN",
                "metodo_pago": "CARD",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "ecommerce"
            },
            {
                "id": "CP-POS-002",
                "descripcion": "Depósito CARD en USD",
                "metodo_pago": "CARD",
                "moneda": "USD",
                "monto": "1.00",
                "canal": "ecommerce"
            },
            {
                "id": "CP-POS-003",
                "descripcion": "Depósito con Yape",
                "metodo_pago": "YAPE_CODE",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "mobile"
            },
            {
                "id": "CP-POS-004",
                "descripcion": "Depósito con QR",
                "metodo_pago": "QR",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "web"
            },
            {
                "id": "CP-POS-005",
                "descripcion": "Depósito con Apple Pay",
                "metodo_pago": "APPLE_PAY",
                "moneda": "USD",
                "monto": "1.00",
                "canal": "mobile"
            },
            {
                "id": "CP-POS-006",
                "descripcion": "Depósito con Pago Push",
                "metodo_pago": "PAGO_PUSH",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "ecommerce"
            },
            {
                "id": "CP-POS-007",
                "descripcion": "Depósito canal MOTO",
                "metodo_pago": "CARD",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "moto"
            },
            {
                "id": "CP-POS-008",
                "descripcion": "Depósito recurrente",
                "metodo_pago": "CARD",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "reccurrence"
            },
            {
                "id": "CP-POS-009",
                "descripcion": "Depósito Izivirtual",
                "metodo_pago": "CARD",
                "moneda": "PEN",
                "monto": "1.00",
                "canal": "izivirtual"
            }
        ]

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        """Imprime un encabezado"""
        print("\n" + "="*70)
        print(title.center(70))
        print("="*70 + "\n")

    def solicitar_credenciales(self):
        """Solicita al usuario las credenciales de Izipay"""
        self.print_header("PASO 1: CREDENCIALES DE IZIPAY")

        print("Ingresa las credenciales de tu comercio Izipay:\n")

        self.merchant_code = input("Codigo de Comercio (merchantCode): ").strip()

        if not self.merchant_code:
            print("\n[ERROR] El codigo de comercio es obligatorio")
            return False

        self.api_key = input("Public Key (API Key): ").strip()

        if not self.api_key:
            print("\n[ERROR] El API Key es obligatorio")
            return False

        print("\n[OK] Credenciales guardadas:")
        print(f"  - Merchant Code: {self.merchant_code}")
        print(f"  - API Key: {self.api_key[:20]}...")

        confirmar = input("\n¿Son correctas las credenciales? (s/n): ").lower()

        return confirmar == 's'

    def mostrar_instrucciones_checkout(self):
        """Muestra instrucciones para usar el checkout demo"""
        self.print_header("PASO 2: GENERAR PAGOS EN CHECKOUT DEMO")

        print("""
INSTRUCCIONES PARA GENERAR PAGOS:

1. Abre tu navegador y accede a:
   https://testcheckout.izipay.pe/demo/

2. IMPORTANTE: Usa las mismas credenciales que acabas de ingresar:
   - Merchant Code: {}
   - API Key: {}

3. Configura cada pago con estos datos:

   TARJETA DE PRUEBA:
   - Numero: 377753000000152 (American Express)
   - Expira: 12/2025
   - CVC: 1234

   DATOS DEL CLIENTE:
   - Nombre: Juan
   - Apellido: Wick Quispe
   - Email: jwick@gmail.com
   - Telefono: 989339999
   - DNI: 10252022
   - Direccion: calle el demo, lima, PE

4. Parametros de cada transaccion:
   - Monto: {} PEN (o la moneda correspondiente)
   - Tipo: Autorizacion/Pago

5. Despues de cada pago EXITOSO:
   - Copia el JSON COMPLETO del Payment Response
   - Pega en este script cuando se te solicite

6. Repite el proceso 9 veces (una por cada caso de prueba)

IMPORTANTE:
- Los Payment Responses deben tener code: "00" (exitosos)
- Deben contener: codeAuth, uniqueId, orderNumber
- Deben ser transacciones NUEVAS (no reutilizadas)

        """.format(self.merchant_code, self.api_key, "1.00"))

        input("\nPresiona ENTER cuando estes listo para comenzar...")

    def capturar_payment_response(self, case_num, test_case):
        """Captura un payment response del usuario"""
        self.print_header(f"PAYMENT RESPONSE {case_num}/9")

        print(f"Caso de Prueba: {test_case['id']}")
        print(f"Descripcion: {test_case['descripcion']}")
        print(f"Metodo: {test_case['metodo_pago']}")
        print(f"Moneda: {test_case['moneda']}")
        print(f"Monto: {test_case['monto']}")
        print(f"Canal: {test_case['canal']}")
        print("\n" + "-"*70)

        print("\nGenera el pago #{} en el checkout demo y copia el Payment Response\n".format(case_num))
        print("Pega el JSON completo aqui (termina con una linea vacia):")
        print("(Ctrl+Z y Enter en Windows, o Ctrl+D en Linux/Mac para terminar)\n")

        # Capturar múltiples líneas
        lines = []
        try:
            while True:
                line = input()
                if not line and lines:  # Línea vacía después de contenido
                    break
                lines.append(line)
        except EOFError:
            pass

        json_text = '\n'.join(lines)

        if not json_text.strip():
            print("\n[ERROR] No se ingreso ningun JSON")
            return False

        # Validar JSON
        try:
            payment_data = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"\n[ERROR] JSON invalido: {e}")
            return False

        # Validar estructura
        if payment_data.get('code') != '00':
            print(f"\n[WARNING] El codigo de respuesta no es 00: {payment_data.get('code')}")
            print(f"[WARNING] Mensaje: {payment_data.get('message')}")
            continuar = input("\n¿Deseas usar este payment response de todos modos? (s/n): ").lower()
            if continuar != 's':
                return False

        response = payment_data.get('response', {})

        if not response.get('codeAuth'):
            print("\n[ERROR] El payment response no contiene 'codeAuth'")
            return False

        if not response.get('uniqueId'):
            print("\n[ERROR] El payment response no contiene 'uniqueId'")
            return False

        if not response.get('orderNumber'):
            print("\n[ERROR] El payment response no contiene 'orderNumber'")
            return False

        # Mostrar resumen
        print("\n[OK] Payment Response valido:")
        print(f"  - Order Number: {response.get('orderNumber')}")
        print(f"  - Auth Code: {response.get('codeAuth')}")
        print(f"  - Unique ID: {response.get('uniqueId')}")
        print(f"  - Monto: {response.get('currency')} {response.get('amount')}")

        # Guardar en archivo
        filename = f"Untitled-{case_num}.json"
        filepath = self.payment_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(payment_data, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Guardado en: {filename}")

        return True

    def capturar_todos_los_pagos(self):
        """Captura los 9 payment responses"""
        self.print_header("CAPTURA DE PAYMENT RESPONSES")

        print("A continuacion capturaras 9 Payment Responses\n")

        for i, test_case in enumerate(self.test_cases, 1):
            while True:
                success = self.capturar_payment_response(i, test_case)

                if success:
                    if i < len(self.test_cases):
                        input(f"\n[OK] Payment {i}/9 capturado. Presiona ENTER para continuar...")
                    break
                else:
                    reintentar = input("\n¿Deseas intentar nuevamente? (s/n): ").lower()
                    if reintentar != 's':
                        return False

        self.print_header("TODOS LOS PAGOS CAPTURADOS")
        print("\n[OK] Se capturaron exitosamente 9 Payment Responses")
        print("\nArchivos guardados en: payment_responses/")

        return True

    def ejecutar_depositos(self):
        """Ejecuta el script de depósitos"""
        self.print_header("PASO 3: EJECUTAR DEPOSITOS")

        print("\nEjecutando depositos automaticamente...\n")
        print(f"Usando credenciales ingresadas:")
        print(f"  - Merchant Code: {self.merchant_code}")
        print(f"  - Public Key: {self.api_key[:20]}...\n")

        result = subprocess.run(
            ['python', 'ejecutar_depositos.py',
             '--merchant-code', self.merchant_code,
             '--public-key', self.api_key],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Mostrar output
        try:
            print(result.stdout, flush=True)
        except:
            for line in result.stdout.split('\n'):
                try:
                    print(line)
                except:
                    print(line.encode('ascii', 'replace').decode('ascii'))

        if result.returncode != 0:
            print("\n[ERROR] Hubo errores en la ejecucion de depositos")
            return False

        return True

    def mostrar_resumen_final(self):
        """Muestra el resumen final"""
        self.print_header("RESUMEN FINAL")

        print("\n[OK] Automatizacion completada exitosamente!\n")

        print("Archivos generados:")
        print("  - INFORME_CONSOLIDADO_DEPOSITOS.md")
        print("  - evidencias/EVIDENCIAS_CP_POS_*.md (9 archivos)\n")

        informe = Path("INFORME_CONSOLIDADO_DEPOSITOS.md")
        if informe.exists():
            print("Abre el informe consolidado para ver los resultados:\n")
            print(f"  {informe.absolute()}\n")

        print("="*70)

    def run(self):
        """Ejecuta el flujo completo"""
        self.clear_screen()

        self.print_header("AUTOMATIZACION INTERACTIVA - IZIPAY")

        print("""
Este script te guiara paso a paso para:

1. Ingresar credenciales de tu comercio Izipay
2. Generar 9 pagos en el checkout demo
3. Capturar los Payment Responses
4. Ejecutar depositos automaticamente
5. Generar informe consolidado

Casos de prueba: CP-POS-001 a CP-POS-009

IMPORTANTE:
- Tendras que generar pagos manualmente en el checkout demo
- Deberas copiar y pegar cada Payment Response en este script
- El proceso tomara aproximadamente 15-20 minutos

        """)

        continuar = input("¿Deseas continuar? (s/n): ").lower()

        if continuar != 's':
            print("\n[INFO] Automatizacion cancelada")
            return False

        # Paso 1: Credenciales
        while True:
            if self.solicitar_credenciales():
                break

            reintentar = input("\n¿Deseas reintentar? (s/n): ").lower()
            if reintentar != 's':
                return False

        # Paso 2: Instrucciones
        self.mostrar_instrucciones_checkout()

        # Paso 3: Capturar pagos
        if not self.capturar_todos_los_pagos():
            print("\n[ERROR] No se completaron todos los pagos")
            return False

        # Paso 4: Ejecutar depósitos
        if not self.ejecutar_depositos():
            return False

        # Paso 5: Resumen
        self.mostrar_resumen_final()

        return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("AUTOMATIZACION INTERACTIVA - CASOS DE PRUEBA DEPOSITO")
    print("="*70)
    print("\nIzipay - Test Automation Script")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Casos: CP-POS-001 a CP-POS-009")
    print("="*70)

    automation = AutomatizacionInteractiva()
    success = automation.run()

    if success:
        print("\n[OK] Proceso completado exitosamente!")
    else:
        print("\n[INFO] Proceso terminado")

    input("\nPresiona ENTER para salir...")
    exit(0 if success else 1)
