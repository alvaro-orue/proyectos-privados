# 🚀 Suite de Pruebas Multi-Ambiente - APIs Izipay

Documentación completa para ejecutar pruebas en múltiples ambientes (DEV, SANDBOX, QA).

---

## 📋 Tabla de Contenidos

1. [Ambientes Disponibles](#ambientes-disponibles)
2. [Requisitos](#requisitos)
3. [Configuración](#configuración)
4. [Uso Básico](#uso-básico)
5. [Casos de Prueba](#casos-de-prueba)
6. [Ejemplos de Ejecución](#ejemplos-de-ejecución)
7. [Estructura de Archivos](#estructura-de-archivos)
8. [Interpretación de Resultados](#interpretación-de-resultados)
9. [Troubleshooting](#troubleshooting)

---

## 🌐 Ambientes Disponibles

### **DEV (Desarrollo)**
```
URL Base:        https://testapi-pw.izipay.pe
Merchant Code:   4078370
Descripción:     Ambiente de desarrollo - Pruebas tempranas e integración continua
Transaction ID:  DEV + YYYYMMDDHHMMSS
```

### **SANDBOX**
```
URL Base:        https://sandbox-api-pw.izipay.pe
Merchant Code:   4000011
Descripción:     Ambiente sandbox - Pruebas de integración externas
Transaction ID:  SBX + YYYYMMDDHHMMSS
```

### **QA (Quality Assurance)**
```
URL Base:        https://qa-api-pw.izipay.pe
Merchant Code:   4078370
Descripción:     Ambiente de QA - Pruebas de calidad
Transaction ID:  QA + YYYYMMDDHHMMSS
```

---

## 📦 Requisitos

### Software Requerido
- Python 3.7+
- pip (gestor de paquetes)

### Dependencias Python
```bash
pip install requests
```

### Estructura de Archivos
```
cuotas/
├── config_environments.py          ← Configuración de ambientes
├── test_runner_multi_env.py        ← Script principal de ejecución
├── README_MULTI_AMBIENTE.md        ← Este archivo
├── CASOS_MULTI_AMBIENTE/           ← Resultados de pruebas
│   ├── DEV/
│   │   └── results/
│   ├── SANDBOX/
│   │   └── results/
│   └── QA/
│       └── results/
```

---

## ⚙️ Configuración

### 1. Verificar Configuración de Ambientes

```bash
# Listar todos los ambientes
python config_environments.py

# Ver detalles de un ambiente específico
python config_environments.py DEV
python config_environments.py SANDBOX
python config_environments.py QA
```

### 2. Ajustar Credenciales (si es necesario)

Editar [config_environments.py](config_environments.py:1) y modificar:

```python
"DEV": {
    "merchant_code": "TU_MERCHANT_CODE",
    "public_key": "TU_PUBLIC_KEY",
    "bins_disponibles": ["545545", "411111"],  # BINs a probar
}
```

---

## 🎯 Uso Básico

### Comando Principal

```bash
python test_runner_multi_env.py --env <AMBIENTE> --test <CASO>
```

### Opciones Disponibles

| Opción | Valores | Descripción |
|--------|---------|-------------|
| `--env` | DEV, SANDBOX, QA | Ambiente de ejecución |
| `--test` | CPI-001, ALL | Caso de prueba a ejecutar |
| `--list-envs` | - | Lista todos los ambientes |
| `--list-bins` | - | Lista BINs del ambiente |
| `--env-info` | - | Muestra info del ambiente |

---

## 📝 Casos de Prueba

### CPI-001: Flujo Completo Exitoso

**Descripción**: Genera token JWT y busca cuotas disponibles para un BIN

**Pasos**:
1. Genera TransactionId único con prefijo del ambiente
2. Genera OrderNumber único
3. Llama a `/Token/Generate` con credenciales del ambiente
4. Obtiene token JWT
5. Llama a `/Installments/Search` con el token y primer BIN configurado
6. Valida respuesta y cuotas disponibles

**Validaciones**:
- ✅ Token generado exitosamente (status 200, code "00")
- ✅ Cuotas retornadas (status 200, code "00")
- ✅ Tiempo de respuesta < 5 segundos
- ✅ Issuer name presente
- ✅ Array de installments no vacío

---

## 🚀 Ejemplos de Ejecución

### 1. Ver Ambientes Disponibles

```bash
python test_runner_multi_env.py --list-envs
```

**Salida esperada**:
```
============================================================
AMBIENTES DISPONIBLES
============================================================

DEV:
  Nombre: Desarrollo
  URL Base: https://testapi-pw.izipay.pe
  Merchant: 4078370
  BINs: 4 configurados

SANDBOX:
  Nombre: Sandbox
  URL Base: https://sandbox-api-pw.izipay.pe
  Merchant: 4000011
  BINs: 4 configurados
```

---

### 2. Ver Información de un Ambiente

```bash
python test_runner_multi_env.py --env DEV --env-info
```

**Salida esperada**:
```
============================================================
AMBIENTE: Desarrollo (DEV)
============================================================
Descripción: Ambiente de desarrollo - Pruebas tempranas e integración continua
Token URL: https://testapi-pw.izipay.pe/security/v1/Token/Generate
Installments URL: https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
Merchant Code: 4078370
Public Key: VErethUtraQuxas57wuMuquprADrAH...
BINs disponibles: 545545, 411111, 424242, 552277
Timeout: 30s
Reintentos: 2
Prefijo TransactionId: DEV
============================================================
```

---

### 3. Listar BINs de un Ambiente

```bash
python test_runner_multi_env.py --env SANDBOX --list-bins
```

**Salida esperada**:
```
============================================================
BINs DISPONIBLES - AMBIENTE: SANDBOX
============================================================
Ambiente: Sandbox
Merchant Code: 4000011

BINs configurados:
  • 545545
  • 411111
  • 424242
  • 552277

Total: 4 BINs
============================================================
```

---

### 4. Ejecutar Prueba en DEV

```bash
python test_runner_multi_env.py --env DEV --test CPI-001
```

**Salida esperada**:
```
============================================================
CASO DE PRUEBA CPI-001 - AMBIENTE: DEV
Flujo completo exitoso - Generar token y buscar cuotas
============================================================
Fecha/Hora: 2025-10-29 14:30:15
Ambiente: Desarrollo
URL Base: https://testapi-pw.izipay.pe
Merchant Code: 4078370
============================================================

🆔 Transaction ID: DEV20251029143015
🆔 Order Number: ORDER20251029143015

============================================================
PASO 1: GENERAR TOKEN DE SESIÓN
============================================================

📤 Request URL: https://testapi-pw.izipay.pe/security/v1/Token/Generate
...
✅ Token generado exitosamente
🔑 Token (primeros 50 caracteres): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiO...

============================================================
PASO 2: BUSCAR CUOTAS DISPONIBLES
============================================================

📤 Request URL: https://testapi-pw.izipay.pe/Installments/v1/Installments/Search
...
✅ Cuotas obtenidas exitosamente
🏦 Emisor: SCOTIABANK
💳 BIN: 545545
📊 Número de cuotas disponibles: 12
📋 Cuotas: 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

============================================================
RESUMEN FINAL
============================================================
Test: Flujo completo exitoso
Ambiente: DEV
Estado: ✅ PASÓ
Duración Total: 627.45ms

Pasos ejecutados:
  ✅ Generate Token - 329.12ms
  ✅ Search Installments - 298.33ms
============================================================
```

---

### 5. Ejecutar Prueba en SANDBOX

```bash
python test_runner_multi_env.py --env SANDBOX --test CPI-001
```

---

### 6. Ejecutar Todas las Pruebas en un Ambiente

```bash
python test_runner_multi_env.py --env DEV --test ALL
```

**Nota**: Por ahora solo está implementado CPI-001, pero la estructura soporta múltiples casos.

---

## 📁 Estructura de Archivos

Después de ejecutar las pruebas, se generan los siguientes archivos:

```
CASOS_MULTI_AMBIENTE/
├── DEV/
│   └── results/
│       ├── test_result_CPI-001_DEV.json       ← Resultado completo en JSON
│       └── test_report_CPI-001_DEV.txt        ← Reporte legible
├── SANDBOX/
│   └── results/
│       ├── test_result_CPI-001_SANDBOX.json
│       └── test_report_CPI-001_SANDBOX.txt
└── QA/
    └── results/
        ├── test_result_CPI-001_QA.json
        └── test_report_CPI-001_QA.txt
```

---

## 📊 Interpretación de Resultados

### Archivo JSON (`test_result_*.json`)

```json
{
  "test_id": "CPI-001",
  "test_name": "Flujo completo exitoso",
  "environment": "DEV",
  "start_time": 1698567890.123,
  "end_time": 1698567890.750,
  "total_duration_ms": 627.45,
  "passed": true,
  "error_message": null,
  "steps": [
    {
      "step": "Generate Token",
      "success": true,
      "duration_ms": 329.12,
      "timestamp": "2025-10-29T14:30:15.123456",
      "data": {
        "success": true,
        "token": "eyJhbGci...",
        "status_code": 200,
        "response": { ... }
      }
    },
    {
      "step": "Search Installments",
      "success": true,
      "duration_ms": 298.33,
      "timestamp": "2025-10-29T14:30:15.452568",
      "data": {
        "success": true,
        "status_code": 200,
        "installments_count": 12,
        "issuer_name": "SCOTIABANK",
        "response": { ... }
      }
    }
  ]
}
```

### Archivo TXT (`test_report_*.txt`)

```
============================================================
REPORTE DE PRUEBA CPI-001 - DEV
============================================================
Test ID: CPI-001
Test Name: Flujo completo exitoso
Ambiente: DEV
Fecha: 2025-10-29 14:30:15
Estado: ✅ PASÓ
Duración Total: 627.45ms

------------------------------------------------------------
PASOS EJECUTADOS
------------------------------------------------------------

Generate Token:
  Estado: ✅ Éxito
  Duración: 329.12ms
  Timestamp: 2025-10-29T14:30:15.123456
  Status Code: 200
  Response Code: 00
  Response Message: Aprobado

Search Installments:
  Estado: ✅ Éxito
  Duración: 298.33ms
  Timestamp: 2025-10-29T14:30:15.452568
  Status Code: 200
  Response Code: 00
  Response Message: Aprobado
```

---

## 🔍 Interpretación de Estados

### Estados de Prueba

| Estado | Icono | Significado |
|--------|-------|-------------|
| PASÓ | ✅ | Todos los pasos exitosos |
| FALLÓ | ❌ | Al menos un paso falló |

### Códigos de Respuesta API

| Código | Significado | Acción |
|--------|-------------|--------|
| 00 | Aprobado | ✅ Éxito |
| IT0 | Invalid transactionId | ❌ Verificar formato |
| IB3 | Invalid BIN | ❌ Verificar BIN configurado |
| TV | Token validation failed | ❌ Token inválido o expirado |
| IMC | Invalid merchant code | ❌ Verificar credenciales |

---

## 🛠️ Troubleshooting

### Error: "Ambiente no encontrado"

```bash
ValueError: Ambiente 'PROD' no encontrado. Disponibles: DEV, SANDBOX, QA
```

**Solución**: Usar uno de los ambientes válidos: `DEV`, `SANDBOX`, `QA`

---

### Error: "Token generation failed"

**Posibles causas**:
1. **Credenciales incorrectas**: Verificar `merchant_code` y `public_key` en [config_environments.py](config_environments.py:1)
2. **URL incorrecta**: Verificar que la URL del ambiente sea accesible
3. **Ambiente no disponible**: El ambiente puede estar caído

**Verificación**:
```bash
# Verificar configuración
python test_runner_multi_env.py --env DEV --env-info

# Probar conectividad (curl o navegador)
curl https://testapi-pw.izipay.pe/security/v1/Token/Generate
```

---

### Error: "BIN no configurado"

```json
{
  "code": "IB3",
  "message": "BIN no válido o no configurado para este comercio"
}
```

**Solución**:
1. Verificar BINs disponibles: `python test_runner_multi_env.py --env DEV --list-bins`
2. Usar un BIN válido para el ambiente
3. Solicitar configuración de BINs adicionales al equipo de infraestructura

---

### Error: Timeout

```
requests.exceptions.Timeout: HTTPSConnectionPool(...): Read timed out. (read timeout=30)
```

**Solución**:
1. Verificar conectividad de red
2. Aumentar timeout en [config_environments.py](config_environments.py:1):
   ```python
   "timeout": 60  # Aumentar a 60 segundos
   ```

---

### Diferencias entre Ambientes

| Aspecto | DEV | SANDBOX | QA |
|---------|-----|---------|-----|
| Estabilidad | 🟡 Media | 🟢 Alta | 🟢 Alta |
| Velocidad | 🟢 Rápido | 🟡 Medio | 🟢 Rápido |
| BINs Configurados | Varios | Varios | Solo 545545 |
| Propósito | Desarrollo | Integración | Calidad |

---

## 📈 Próximos Pasos

### Casos de Prueba a Implementar

- [ ] **CPI-002**: Token de un solo uso
- [ ] **CPI-003**: TransactionId consistente
- [ ] **CPI-004**: Casos de error (401, 400, etc.)
- [ ] **CPI-005**: Diferentes BINs
- [ ] **CPI-006**: Amount 0.00
- [ ] **CPI-007**: Idioma inglés

### Mejoras Sugeridas

1. **Paralelización**: Ejecutar pruebas en múltiples ambientes simultáneamente
2. **Comparación**: Generar reporte comparativo entre ambientes
3. **CI/CD**: Integrar con pipeline de integración continua
4. **Alertas**: Notificaciones automáticas en caso de fallos
5. **Dashboard**: Visualización web de resultados

---

## 📞 Soporte

### Contacto
- **Repositorio**: pw.0009.api.installments
- **Branch**: DEV-GSTI-5752-VulnerabilidadesAltas

### Documentación Adicional
- [Casos_Prueba_API_Search_Installments.md](Casos_Prueba_API_Search_Installments.md:1) - Plan completo de casos de prueba
- [CASOS/RESUMEN_EJECUTIVO_CONSOLIDADO.md](CASOS/RESUMEN_EJECUTIVO_CONSOLIDADO.md:1) - Resultados de QA

---

**Última actualización**: 2025-10-29
**Versión**: 1.0
**Estado**: ✅ Listo para uso
