# CPI-001: Flujo Completo - Generate Token + Search Installments

## Descripción
Este directorio contiene el caso de prueba CPI-001 que valida el flujo completo de integración entre los APIs de Generate Token y Search Installments de Izipay.

## Contenido del Directorio

```
CPI-001/
├── test_cpi_001.py                    # Script de prueba en Python
├── test_result.json                   # Resultado completo en JSON
├── test_report.txt                    # Reporte en formato texto
├── step_1_Generate_Token.json         # Detalle del Paso 1
├── step_2_Search_Installments.json    # Detalle del Paso 2
├── ANALISIS_RESULTADOS.md            # Análisis detallado de resultados
├── diagnose_environment.py            # Script de diagnóstico
└── README.md                          # Este archivo
```

## Resultado de la Ejecución

**Fecha:** 2025-10-28 13:56:12
**Estado:** ❌ FALLÓ
**Duración Total:** 10.85 segundos

### Resumen por Pasos

| Paso | Estado | Duración | Observación |
|------|--------|----------|-------------|
| 1. Generate Token | ✅ EXITOSO | 478 ms | Token JWT generado correctamente |
| 2. Search Installments | ❌ FALLÓ | 10,374 ms | Error 500 del servidor |

## Problema Identificado

El API de **Search Installments** está retornando un error HTTP 500:

```json
{
  "code": "500",
  "errorMessage": "The API Controller service threw an error. Check the errors field to view possible details."
}
```

### Posibles Causas

1. Servicio de Installments caído o con problemas en QA
2. URL del endpoint incorrecta para ambiente QA
3. MerchantCode sin configuración de cuotas en QA
4. BIN no registrado en el ambiente QA
5. Problemas de infraestructura o red

## Cómo Ejecutar

### Requisitos Previos

```bash
# Instalar Python 3.7+
python --version

# Instalar dependencias
pip install requests
```

### Ejecutar la Prueba

```bash
# Navegar al directorio
cd c:\IZIPAY\cuotas\CPI-001

# Ejecutar el script
python test_cpi_001.py

# Ver resultados
cat test_report.txt
```

### Parámetros del Script

El script usa la siguiente configuración (editable en el archivo):

```python
CONFIG = {
    "token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
    "merchant_code": "4078370",
    "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}
```

## Archivos Generados

### test_result.json
Resultado completo en formato JSON con:
- Información de cada paso
- Requests y responses completos
- Duración de cada operación
- Timestamps detallados

### test_report.txt
Reporte resumido en texto plano con:
- Estado general de la prueba
- Resumen de cada paso
- Tiempos de ejecución

### step_X_*.json
Archivos individuales con detalles de cada paso:
- Request completo (headers, body)
- Response completo
- Códigos de estado
- Duración

## Próximos Pasos

### 1. Verificar Estado del Servicio

```bash
# Ejecutar script de diagnóstico
python diagnose_environment.py

# O manualmente
curl -I https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search
```

### 2. Contactar Soporte

Si el problema persiste, contactar al equipo de DevOps/Infraestructura con:
- TransactionId: `TXN1761677772192`
- TokenId: `0ab78e53-1a49-4f81-9604-b6c1b9d6075f`
- Timestamp: `2025-10-28 13:56:12 - 13:56:23`
- Archivos de evidencia en este directorio

### 3. Probar en Sandbox

Como alternativa, probar el mismo flujo en ambiente Sandbox:

```python
# Modificar CONFIG en test_cpi_001.py
CONFIG = {
    "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
    "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
    "merchant_code": "4007701",  # Merchant de sandbox
    "public_key": "VErEthUtraQUxas57wUMuquprADrAHAb..."  # Public key de sandbox
}
```

## Token Generado

El token JWT generado exitosamente contiene:

```json
{
  "merchantCode": "4078370",
  "facilitatorCode": "0",
  "transactionId": "TXN1761677772192",
  "OrderNumber": "ORDER1761677772",
  "Amount": "100.00",
  "TokenId": "0ab78e53-1a49-4f81-9604-b6c1b9d6075f",
  "nbf": 1761677772,
  "exp": 1761678672,  // Expira en 15 minutos
  "iat": 1761677772
}
```

**Observaciones:**
- ✅ Token válido con formato JWT
- ✅ Incluye todos los datos esperados
- ✅ Configurado con expiración de 15 minutos
- ✅ TokenId único generado

## Documentación Relacionada

- [Documentación API Generate Token](../Documentación_API_Generate_Token.md)
- [Documentación API Search Installments](../Documentación%20API_%20Búsqueda%20de%20Cuotas%20(Search%20Installments).md)
- [Casos de Prueba Completos](../Casos_Prueba_Integracion_Completa.md)
- [Análisis de Resultados](./ANALISIS_RESULTADOS.md)

## Contacto y Soporte

Para reportar problemas o solicitar soporte:

1. **Revisar el análisis detallado**: [ANALISIS_RESULTADOS.md](./ANALISIS_RESULTADOS.md)
2. **Recopilar evidencias**: Adjuntar archivos JSON generados
3. **Contactar al equipo técnico**: Con TransactionId y timestamp

---

**Última ejecución:** 2025-10-28 13:56:12
**Estado del ambiente QA:** ⚠️ API Search Installments con problemas
**Recomendación:** Esperar resolución del error 500 o probar en Sandbox
