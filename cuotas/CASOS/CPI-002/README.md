# Caso de Prueba CPI-002: Token de Un Solo Uso

## 📋 Información del Caso

**ID**: CPI-002
**Nombre**: Token de un solo uso
**Objetivo**: Verificar que un token no puede ser reutilizado después de ser usado
**Prioridad**: ALTA
**Ambiente**: QA

---

## ⚠️ Resultado: HALLAZGO IMPORTANTE

**Fecha/Hora**: 2025-10-29 08:54:16
**Estado**: ❌ FALLÓ (Comportamiento inesperado)
**Duración Total**: 9.49 segundos

### 🔍 Hallazgo

**El token puede ser reutilizado en el ambiente QA**, lo cual difiere del comportamiento esperado donde un token debería ser de un solo uso.

---

## 📊 Resultados Detallados

| Paso | Resultado | Duración | Observación |
|------|-----------|----------|-------------|
| 1. Generate Token | ✅ OK | 606 ms | Token generado correctamente |
| 2. Primera Búsqueda | ✅ OK | 4,928 ms | 12 cuotas retornadas |
| 3. Segunda Búsqueda | ⚠️ **OK** | 3,958 ms | **Token reutilizado exitosamente** |

### TransactionId
```
FVCL20251029085416
```

---

## 🎯 Análisis

### Comportamiento Esperado
1. ✅ Token se genera correctamente
2. ✅ Primera búsqueda funciona
3. ❌ Segunda búsqueda debería **FALLAR** (token ya usado)

### Comportamiento Observado
1. ✅ Token se genera correctamente
2. ✅ Primera búsqueda funciona
3. ⚠️ Segunda búsqueda **FUNCIONA** (token puede reutilizarse)

---

## ⚠️ Implicaciones

### Seguridad
- El token puede ser interceptado y reutilizado
- No hay protección contra replay attacks con el mismo token
- Posible vulnerabilidad de seguridad

### Posibles Causas
1. **Configuración de QA**: El ambiente de pruebas permite reutilización para facilitar testing
2. **Característica**: El token puede usarse múltiples veces dentro de su ventana de 15 minutos
3. **Bug**: Comportamiento no intencionado que debe corregirse

---

## 📋 Recomendaciones

### Acción Inmediata
1. **Verificar documentación**: Confirmar si el comportamiento es intencional
2. **Consultar con Desarrollo**: Validar si es comportamiento esperado en QA
3. **Probar en Producción**: Verificar si el comportamiento es diferente

### Si es un Bug
- Implementar validación de token de un solo uso
- Marcar token como usado después de la primera petición
- Retornar error 401 en intentos subsecuentes

### Si es Característica
- Documentar claramente el comportamiento
- Actualizar criterios de prueba
- Considerar implicaciones de seguridad

---

## 📁 Archivos Generados

```
CASOS/CPI-002/
├── test_cpi_002.py                              # Script de prueba
├── test_result.json                             # Resultado completo
├── test_report.txt                              # Reporte resumido
├── step_1_Generate_Token.json                   # Paso 1: Token
├── step_2_First_Search_Should_Succeed.json      # Paso 2: Primera búsqueda
├── step_3_Second_Search_Should_Fail.json        # Paso 3: Segunda búsqueda
└── README.md                                    # Este archivo
```

---

## 🔍 Datos de la Prueba

**Primera Búsqueda**:
- Status: 200 OK
- Code: "00"
- Cuotas: 12 opciones
- Duración: 4,928 ms

**Segunda Búsqueda** (con mismo token):
- Status: 200 OK
- Code: "00"
- Cuotas: 12 opciones
- Duración: 3,958 ms

**Conclusión**: Ambas búsquedas exitosas con el mismo token.

---

**Última actualización**: 2025-10-29 08:54:16
**Estado**: ⚠️ HALLAZGO - Requiere validación con equipo de desarrollo
