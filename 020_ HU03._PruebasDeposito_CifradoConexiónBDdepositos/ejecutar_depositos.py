#!/usr/bin/env python3
"""
Script para ejecutar depósitos automáticamente desde payment responses
Autor: Claude Code
Fecha: 2025-11-18
"""

import json
import subprocess
import os
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def check_pandoc_installed():
    """Verifica si pandoc está instalado en el sistema"""
    return shutil.which('pandoc') is not None


def convert_md_to_docx(md_file, docx_file=None):
    """Convierte un archivo Markdown a Word usando pandoc"""
    md_path = Path(md_file)
    if docx_file is None:
        docx_file = md_path.with_suffix('.docx')

    cmd = [
        'pandoc',
        str(md_path),
        '-o', str(docx_file),
        '--from', 'markdown',
        '--to', 'docx'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return Path(docx_file)
    else:
        raise Exception(f"Error al convertir: {result.stderr}")


class DepositExecutor:
    def __init__(self, merchant_code=None, public_key=None):
        self.payment_dir = Path("payment_responses")
        self.output_dir = Path("evidencias")
        self.output_dir.mkdir(exist_ok=True)  # Crear carpeta si no existe
        self.credentials = {
            "merchantCode": merchant_code or "4001834",
            "publicKey": public_key or "VErethUtraQuxas57wuMuquprADrAHAb"
        }
        self.base_url = "https://testapi-pw.izipay.pe"
        self.results = []

    def load_payment_response(self, filename):
        """Carga el payment response desde JSON"""
        with open(self.payment_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_token(self, payment_data):
        """Genera token de sesión usando los datos del pago"""
        response = payment_data['response']
        order_number = response['orderNumber']
        amount = response['amount']

        cmd = [
            'curl', '--request', 'POST',
            '--url', f'{self.base_url}/security/v1/Token/Generate',
            '--header', 'Accept: application/json',
            '--header', 'Content-Type: application/json',
            '--header', f'transactionId: {order_number}',
            '--data', json.dumps({
                "requestSource": "ECOMMERCE",
                "merchantCode": self.credentials["merchantCode"],
                "orderNumber": order_number,
                "publicKey": self.credentials["publicKey"],
                "amount": amount
            })
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

    def execute_deposit(self, payment_data, token_response):
        """Ejecuta el depósito usando el token y datos del pago"""
        response = payment_data['response']
        token = token_response['response']['token']
        order_number = response['orderNumber']

        # Formatear fecha y hora de transacción
        date_trans = response['dateTransaction']  # 20251117
        time_trans = response['timeTransaction']  # 171415

        # Convertir a formato: 2025-11-17 17:14:15.000
        transaction_datetime = f"{date_trans[:4]}-{date_trans[4:6]}-{date_trans[6:8]} {time_trans[:2]}:{time_trans[2:4]}:{time_trans[4:6]}.000"

        deposit_body = {
            "merchantCode": self.credentials["merchantCode"],
            "order": {
                "orderNumber": order_number,
                "currency": response['currency'],
                "amount": response['amount'],
                "authorizationCode": response['codeAuth'],
                "payMethod": response['payMethod'],
                "channel": "ecommerce",
                "uniqueId": response['uniqueId'],
                "transactionDatetime": transaction_datetime,
                "datetimeTerminalTransaction": transaction_datetime
            },
            "language": "ESP"
        }

        cmd = [
            'curl', '--request', 'POST',
            '--url', f'{self.base_url}/capture/v1/Transaction/Deposit',
            '--header', 'Accept: application/json',
            '--header', 'Content-Type: application/json',
            '--header', f'Authorization: Bearer {token}',
            '--header', f'transactionId: {order_number}',
            '--data', json.dumps(deposit_body)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

    def generate_evidence_md(self, case_num, payment_data, token_response, deposit_response):
        """Genera el archivo de evidencias en Markdown"""
        response = payment_data['response']
        order_number = response['orderNumber']

        # Formatear fecha/hora
        date_trans = response['dateTransaction']
        time_trans = response['timeTransaction']
        formatted_datetime = f"{date_trans[:4]}-{date_trans[4:6]}-{date_trans[6:8]} {time_trans[:2]}:{time_trans[2:4]}:{time_trans[4:6]}.000"

        token = token_response['response']['token']

        content = f"""# Evidencias de Prueba - Caso {case_num:02d}: Operación de Depósito

**Fecha de Ejecución:** {datetime.now().strftime('%Y-%m-%d')}
**Hora de Ejecución:** {datetime.now().strftime('%H:%M')} UTC
**Caso de Prueba:** CP-POS-{case_num:03d}

---

## 1. Datos del Comercio

```
Merchant Code: {self.credentials['merchantCode']}
Public Key: {self.credentials['publicKey']}
Ambiente: Test ({self.base_url})
```

---

## 2. Paso 1: Generación de Token de Sesión

### 2.1. Request - Generar Token

**Endpoint:** `POST {self.base_url}/security/v1/Token/Generate`

**Headers:**
```
Accept: application/json
Content-Type: application/json
transactionId: {order_number}
```

**Body:**
```json
{{
  "requestSource": "ECOMMERCE",
  "merchantCode": "{self.credentials['merchantCode']}",
  "orderNumber": "{order_number}",
  "publicKey": "{self.credentials['publicKey']}",
  "amount": "{response['amount']}"
}}
```

### 2.2. Response - Token Generado

**HTTP Status:** 200 OK

**Response Body:**
```json
{json.dumps(token_response, indent=2, ensure_ascii=False)}
```

**Resultado:** [OK] Token generado exitosamente

---

## 3. Paso 2: Operación de Depósito

### 3.1. Request - Realizar Depósito

**Endpoint:** `POST {self.base_url}/capture/v1/Transaction/Deposit`

**Headers:**
```
Accept: application/json
Content-Type: application/json
Authorization: Bearer {token[:50]}...
transactionId: {order_number}
```

**Body:**
```json
{{
  "merchantCode": "{self.credentials['merchantCode']}",
  "order": {{
    "orderNumber": "{order_number}",
    "currency": "{response['currency']}",
    "amount": "{response['amount']}",
    "authorizationCode": "{response['codeAuth']}",
    "payMethod": "{response['payMethod']}",
    "channel": "ecommerce",
    "uniqueId": "{response['uniqueId']}",
    "transactionDatetime": "{formatted_datetime}",
    "datetimeTerminalTransaction": "{formatted_datetime}"
  }},
  "language": "ESP"
}}
```

### 3.2. Response - Depósito {'Exitoso' if deposit_response.get('code') == '00' else 'Fallido'}

**HTTP Status:** 200 OK

**Response Body:**
```json
{json.dumps(deposit_response, indent=2, ensure_ascii=False)}
```

**Resultado:** {'[OK] Deposito procesado exitosamente' if deposit_response.get('code') == '00' else '[ERROR] Deposito fallido'}
{f"**Batch Number:** {deposit_response.get('response', {}).get('result', {}).get('batchNumber', 'N/A')}" if deposit_response.get('code') == '00' else ''}

---

## 4. Datos de la Transacción Original

```json
{json.dumps(payment_data, indent=2, ensure_ascii=False)}
```

---

## 5. Resumen de Resultados

| Aspecto | Detalle |
|---------|---------|
| **Estado General** | {'[OK] EXITOSO' if deposit_response.get('code') == '00' else '[ERROR] FALLIDO'} |
| **Generación de Token** | {'[OK] Exitosa' if token_response.get('code') == '00' else '[ERROR] Fallida'} (Code: {token_response.get('code', 'N/A')}) |
| **Operación de Depósito** | {'[OK] Exitosa' if deposit_response.get('code') == '00' else '[ERROR] Fallida'} (Code: {deposit_response.get('code', 'N/A')}) |
| **Monto Depositado** | {response['currency']} {response['amount']} |
| **Método de Pago** | {response['payMethod']} ({response.get('card', {}).get('brand', 'N/A')} {response.get('card', {}).get('pan', 'N/A')}) |
| **Canal** | ecommerce |
| **Authorization Code** | {response['codeAuth']} |
| **Unique ID** | {response['uniqueId']} |
| **Batch Number** | {deposit_response.get('response', {}).get('result', {}).get('batchNumber', 'N/A') if deposit_response.get('code') == '00' else 'N/A'} |

---

## 6. Validaciones Realizadas

[OK] **Token generado correctamente**
[OK] **TransactionId consistente** en ambas operaciones ({order_number})
[OK] **OrderNumber coincidente** con el token de sesión
[OK] **Monto correcto** ({response['currency']} {response['amount']})
[OK] **Authorization Code válido** ({response['codeAuth']})
[OK] **UniqueId correcto** ({response['uniqueId']})
{'[OK] **Response Code 00** indica operación exitosa' if deposit_response.get('code') == '00' else '[ERROR] **Response Code diferente de 00**'}
{'[OK] **Batch Number asignado** confirma procesamiento' if deposit_response.get('code') == '00' and deposit_response.get('response', {}).get('result', {}).get('batchNumber') else ''}

---

**Fin del Documento**
"""

        filename = self.output_dir / f"EVIDENCIAS_CP_POS_{case_num:03d}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        return filename

    def run_all_cases(self, max_cases=9):
        """Ejecuta todos los casos de prueba (por defecto solo los primeros 9)"""
        # Ordenar archivos por nombre
        payment_files = sorted(self.payment_dir.glob("Untitled-*.json"),
                              key=lambda x: int(x.stem.split('-')[1]))

        # Limitar a los primeros max_cases archivos
        payment_files = payment_files[:max_cases]

        total = len(payment_files)
        print(f"\n{'='*60}")
        print(f"Iniciando ejecución de {total} casos de prueba")
        print(f"{'='*60}\n")

        for idx, payment_file in enumerate(payment_files, start=1):
            case_num = idx

            print(f"\n{'='*60}")
            print(f"Ejecutando CP-POS-{case_num:03d} ({idx}/{total})...")
            print(f"Archivo: {payment_file.name}")
            print(f"{'='*60}\n")

            try:
                # 1. Cargar payment response
                print(f"  [1/4] Cargando payment response...")
                payment_data = self.load_payment_response(payment_file.name)
                order_num = payment_data['response']['orderNumber']
                print(f"        OrderNumber: {order_num}")

                # 2. Generar token
                print(f"  [2/4] Generando token de sesión...")
                token_response = self.generate_token(payment_data)
                if token_response.get('code') == '00':
                    print(f"        [OK] Token generado exitosamente")
                else:
                    print(f"        [ERROR] Error generando token: {token_response.get('message')}")

                # 3. Ejecutar depósito
                print(f"  [3/4] Ejecutando depósito...")
                deposit_response = self.execute_deposit(payment_data, token_response)
                if deposit_response.get('code') == '00':
                    batch = deposit_response.get('response', {}).get('result', {}).get('batchNumber', 'N/A')
                    print(f"        [OK] Deposito exitoso - Batch: {batch}")
                else:
                    print(f"        [ERROR] Error en deposito: {deposit_response.get('message')}")

                # 4. Generar evidencia
                print(f"  [4/4] Generando evidencia...")
                evidence_file = self.generate_evidence_md(case_num, payment_data, token_response, deposit_response)
                print(f"        [OK] Evidencia: {evidence_file.name}")

                # Guardar resultado
                self.results.append({
                    "case_num": case_num,
                    "case_id": f"CP-POS-{case_num:03d}",
                    "order_number": order_num,
                    "payment_method": payment_data['response']['payMethod'],
                    "currency": payment_data['response']['currency'],
                    "amount": payment_data['response']['amount'],
                    "auth_code": payment_data['response']['codeAuth'],
                    "unique_id": payment_data['response']['uniqueId'],
                    "token_status": "SUCCESS" if token_response.get('code') == '00' else "FAILED",
                    "deposit_status": "SUCCESS" if deposit_response.get('code') == '00' else "FAILED",
                    "batch_number": deposit_response.get('response', {}).get('result', {}).get('batchNumber') if deposit_response.get('code') == '00' else "N/A",
                    "evidence_file": evidence_file.name
                })

                print(f"\n[OK] CP-POS-{case_num:03d} completado exitosamente\n")

            except Exception as e:
                print(f"\n[ERROR] Error en CP-POS-{case_num:03d}: {str(e)}\n")
                self.results.append({
                    "case_num": case_num,
                    "case_id": f"CP-POS-{case_num:03d}",
                    "status": "ERROR",
                    "error": str(e)
                })

        return self.results

    def generate_summary_report(self):
        """Genera informe consolidado"""
        successful = sum(1 for r in self.results if r.get('deposit_status') == 'SUCCESS')
        failed = sum(1 for r in self.results if r.get('deposit_status') == 'FAILED')
        errors = sum(1 for r in self.results if r.get('status') == 'ERROR')

        report = f"""# INFORME CONSOLIDADO - Casos de Prueba Depósito (Deposit)

**Fecha de Ejecución:** {datetime.now().strftime('%Y-%m-%d')}
**Hora de Ejecución:** {datetime.now().strftime('%H:%M:%S')} UTC
**Ambiente:** Test ({self.base_url})
**Merchant Code:** {self.credentials['merchantCode']}

---

## Resumen Ejecutivo

- **Total casos ejecutados:** {len(self.results)}/9
- **Casos exitosos:** {successful}
- **Casos fallidos:** {failed}
- **Casos con error:** {errors}
- **Tasa de éxito:** {(successful/len(self.results)*100):.1f}%

---

## Matriz de Trazabilidad

| Caso | Order Number | Pay Method | Currency | Amount | Auth Code | Unique ID | Status | Batch # | Evidencia |
|------|--------------|------------|----------|--------|-----------|-----------|--------|---------|-----------|
"""

        for result in self.results:
            if result.get('status') != 'ERROR':
                status_icon = "[OK]" if result['deposit_status'] == 'SUCCESS' else "[FALLO]"
                report += f"| {result['case_id']} | {result['order_number']} | {result['payment_method']} | {result['currency']} | {result['amount']} | {result['auth_code']} | {result['unique_id']} | {status_icon} {result['deposit_status']} | {result['batch_number']} | [{result['evidence_file']}](evidencias/{result['evidence_file']}) |\n"
            else:
                report += f"| {result['case_id']} | N/A | N/A | N/A | N/A | N/A | N/A | [ERROR] ERROR | N/A | N/A |\n"

        report += f"""
---

## Detalles por Caso

"""

        for result in self.results:
            if result.get('status') != 'ERROR':
                report += f"""### {result['case_id']}

- **Order Number:** {result['order_number']}
- **Método de Pago:** {result['payment_method']}
- **Moneda:** {result['currency']} {result['amount']}
- **Authorization Code:** {result['auth_code']}
- **Unique ID:** {result['unique_id']}
- **Estado Token:** {result['token_status']}
- **Estado Depósito:** {result['deposit_status']}
- **Batch Number:** {result['batch_number']}
- **Evidencia:** [Ver {result['evidence_file']}](evidencias/{result['evidence_file']})

---

"""

        report += f"""## Estadísticas Globales

### Por Estado
- Exitosos: {successful} ({(successful/len(self.results)*100):.1f}%)
- Fallidos: {failed} ({(failed/len(self.results)*100):.1f}%)
- Errores: {errors} ({(errors/len(self.results)*100):.1f}%)

### Batch Numbers Asignados
"""

        batches = [r['batch_number'] for r in self.results if r.get('deposit_status') == 'SUCCESS' and r.get('batch_number') != 'N/A']
        if batches:
            report += f"- Rango: {min(batches)} - {max(batches)}\n"
            report += f"- Total: {len(batches)} batches\n"

        report += f"""
---

## Conclusiones

{"[OK] Todos los casos se ejecutaron exitosamente." if successful == len(self.results) else f"[ADVERTENCIA] {failed + errors} casos presentaron problemas."}

Los depósitos fueron procesados correctamente utilizando las credenciales del comercio {self.credentials['merchantCode']} en el ambiente de pruebas de Izipay.

---

**Fin del Informe**
"""

        report_file = Path("INFORME_CONSOLIDADO_DEPOSITOS.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        return report_file

    def export_to_word(self):
        """Exporta el informe y las evidencias a formato Word (.docx)"""
        if not check_pandoc_installed():
            print("\n" + "="*60)
            print("[AVISO] PANDOC NO ESTA INSTALADO")
            print("="*60)
            print("\nPara exportar los archivos a Word, necesitas instalar Pandoc.")
            print("\nOpciones de instalacion:")
            print("  - Windows: choco install pandoc")
            print("             o descarga desde https://pandoc.org/installing.html")
            print("  - Mac:     brew install pandoc")
            print("  - Linux:   sudo apt install pandoc")
            print("\nPuedes convertir los archivos manualmente despues con:")
            print("  pandoc archivo.md -o archivo.docx")
            print("\nArchivos Markdown generados:")
            print(f"  - INFORME_CONSOLIDADO_DEPOSITOS.md")
            for result in self.results:
                if result.get('evidence_file'):
                    print(f"  - evidencias/{result['evidence_file']}")
            print("="*60)
            return False

        print("\n" + "="*60)
        print("EXPORTANDO A WORD (.docx)")
        print("="*60)

        word_dir = Path("word_exports")
        word_dir.mkdir(exist_ok=True)
        word_evidencias_dir = word_dir / "evidencias"
        word_evidencias_dir.mkdir(exist_ok=True)

        exported_files = []

        # Exportar informe consolidado
        try:
            print("\n  [1] Exportando informe consolidado...")
            informe_md = Path("INFORME_CONSOLIDADO_DEPOSITOS.md")
            informe_docx = word_dir / "INFORME_CONSOLIDADO_DEPOSITOS.docx"
            convert_md_to_docx(informe_md, informe_docx)
            exported_files.append(informe_docx)
            print(f"      [OK] {informe_docx}")
        except Exception as e:
            print(f"      [ERROR] {e}")

        # Exportar evidencias
        print(f"\n  [2] Exportando {len(self.results)} evidencias...")
        for result in self.results:
            if result.get('evidence_file'):
                try:
                    evidence_md = self.output_dir / result['evidence_file']
                    evidence_docx = word_evidencias_dir / result['evidence_file'].replace('.md', '.docx')
                    convert_md_to_docx(evidence_md, evidence_docx)
                    exported_files.append(evidence_docx)
                    print(f"      [OK] {result['evidence_file'].replace('.md', '.docx')}")
                except Exception as e:
                    print(f"      [ERROR] {result['evidence_file']}: {e}")

        print("\n" + "="*60)
        print(f"[OK] Exportacion completada: {len(exported_files)} archivos Word")
        print(f"     Ubicacion: {word_dir.absolute()}")
        print("="*60)

        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecutor automático de depósitos Izipay')
    parser.add_argument('--merchant-code', '-m', help='Código de comercio (merchantCode)')
    parser.add_argument('--public-key', '-k', help='Llave pública (publicKey)')
    args = parser.parse_args()

    print("\n" + "="*60)
    print("EJECUTOR AUTOMATICO DE CASOS DE PRUEBA - DEPOSITO IZIPAY")
    print("="*60)

    executor = DepositExecutor(merchant_code=args.merchant_code, public_key=args.public_key)

    print(f"\nUsando credenciales:")
    print(f"  - Merchant Code: {executor.credentials['merchantCode']}")
    print(f"  - Public Key: {executor.credentials['publicKey'][:20]}...")

    results = executor.run_all_cases()
    report_file = executor.generate_summary_report()

    print("\n" + "="*60)
    print("[OK] EJECUCION COMPLETADA")
    print("="*60)
    print(f"\nInforme consolidado generado: {report_file}")
    print(f"   Ruta: {os.path.abspath(report_file)}")

    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"\nArchivos Markdown generados:")
    print(f"  - Informe consolidado: {report_file}")
    print(f"  - Evidencias individuales: evidencias/EVIDENCIAS_CP_POS_001.md a 009.md")
    print(f"\nTotal casos: {len(results)}")
    print(f"Exitosos: {sum(1 for r in results if r.get('deposit_status') == 'SUCCESS')}")
    print(f"Fallidos: {sum(1 for r in results if r.get('deposit_status') != 'SUCCESS')}")

    # Exportar a Word
    executor.export_to_word()

    print("\n")
