# CPI-005: Diferentes BINs

## Resultado: ⚠️ PARCIAL

**Fecha**: 2025-10-29 10:17
**TransactionId**: FVCL20251029101730

## Resultados

| BIN | Emisor | Estado | Cuotas |
|-----|--------|--------|--------|
| 545545 | SCOTIABANK | ✅ PASÓ | 12 |
| 411111 | VISA | ❌ FALLÓ | 0 |
| 424242 | VISA | ❌ FALLÓ | 0 |
| 552277 | MASTERCARD | ❌ FALLÓ | 0 |

**Exitosos**: 1/4 (25%)

## Hallazgo

Solo el BIN 545545 (SCOTIABANK) está configurado en QA. Los demás BINs no están asociados al merchant 4078370.

**Recomendación**: Configurar BINs adicionales para pruebas completas.
