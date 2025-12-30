# 📁 Índice de Archivos - CPI-001

## 🗂️ Estructura del Directorio

```
CPI-001/
│
├── 📘 DOCUMENTACIÓN
│   ├── README.md                      (5.2 KB)  - Guía principal
│   ├── RESUMEN_EJECUTIVO.md           (8.2 KB)  - Resumen para gerencia
│   ├── ANALISIS_RESULTADOS.md        (11.0 KB)  - Análisis técnico detallado
│   └── INDEX.md                              - Este archivo
│
├── 🔧 SCRIPTS
│   ├── test_cpi_001.py               (13.0 KB)  - Script principal de prueba
│   └── diagnose_environment.py        (7.4 KB)  - Script de diagnóstico
│
├── 📊 RESULTADOS
│   ├── test_result.json               (2.4 KB)  - Resultado completo en JSON
│   ├── test_report.txt                (0.8 KB)  - Reporte resumido en texto
│   ├── step_1_Generate_Token.json     (1.3 KB)  - Detalle del Paso 1
│   └── step_2_Search_Installments.json (0.3 KB)  - Detalle del Paso 2
│
└── 📋 TOTAL: 9 archivos               (~50 KB)
```

---

## 📖 Guía de Lectura

### Para Ejecutivos / Gerencia
1. 📊 **[RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)** - Comienza aquí
   - Estado general del test
   - Problema identificado
   - Impacto y prioridad
   - Acciones recomendadas

### Para QA / Testers
2. 📘 **[README.md](./README.md)** - Guía de uso
   - Cómo ejecutar las pruebas
   - Requisitos previos
   - Configuración
   - Troubleshooting

3. 📊 **test_report.txt** - Reporte rápido
   - Resumen en texto plano
   - Estado de cada paso
   - Tiempos de ejecución

### Para Desarrolladores / DevOps
4. 🔍 **[ANALISIS_RESULTADOS.md](./ANALISIS_RESULTADOS.md)** - Análisis técnico
   - Detalles técnicos completos
   - Análisis del token JWT
   - Posibles causas del error
   - Recomendaciones técnicas

5. 📊 **test_result.json** - Datos estructurados
   - Resultado completo en JSON
   - Requests y responses completos
   - Ideal para análisis automatizado

6. 🔧 **diagnose_environment.py** - Diagnóstico
   - Script para verificar servicios
   - Validación de conectividad
   - Estado del ambiente

---

## 🚀 Inicio Rápido

### Ver Resumen
```bash
cat RESUMEN_EJECUTIVO.md
```

### Ver Reporte Corto
```bash
cat test_report.txt
```

### Ver Resultado JSON
```bash
cat test_result.json | python -m json.tool
```

### Ejecutar Prueba Nuevamente
```bash
python test_cpi_001.py
```

### Ejecutar Diagnóstico
```bash
python diagnose_environment.py
```

---

## 📝 Descripción de Archivos

### 📘 README.md
**Propósito**: Guía principal de uso del caso de prueba
**Audiencia**: QA, Testers
**Contenido**:
- Descripción del caso de prueba
- Instrucciones de ejecución
- Configuración
- Resultados obtenidos
- Próximos pasos

**Cuándo leer**: Antes de ejecutar las pruebas

---

### 📊 RESUMEN_EJECUTIVO.md
**Propósito**: Resumen ejecutivo del resultado
**Audiencia**: Gerencia, Product Owners, QA Leads
**Contenido**:
- Estado general (PASÓ/FALLÓ)
- Problema identificado
- Impacto y prioridad
- Acciones inmediatas
- Métricas clave

**Cuándo leer**: Para reporte rápido o escalación

---

### 🔍 ANALISIS_RESULTADOS.md
**Propósito**: Análisis técnico detallado
**Audiencia**: Desarrolladores, DevOps, Arquitectos
**Contenido**:
- Análisis de cada paso
- Decodificación del token JWT
- Análisis del error 500
- Posibles causas técnicas
- Recomendaciones detalladas
- Comandos de diagnóstico

**Cuándo leer**: Para investigación técnica profunda

---

### 🔧 test_cpi_001.py
**Propósito**: Script ejecutable de prueba
**Lenguaje**: Python 3
**Funcionalidad**:
- Genera token de sesión
- Busca cuotas con el token
- Captura requests/responses
- Genera reportes automáticos
- Maneja errores

**Cuándo usar**: Para ejecutar o re-ejecutar la prueba

**Uso**:
```bash
python test_cpi_001.py
```

---

### 🔧 diagnose_environment.py
**Propósito**: Script de diagnóstico del ambiente
**Lenguaje**: Python 3
**Funcionalidad**:
- Verifica resolución DNS
- Prueba conectividad con endpoints
- Valida estado de servicios
- Genera reporte de diagnóstico

**Cuándo usar**: Para troubleshooting de ambiente

**Uso**:
```bash
python diagnose_environment.py
```

---

### 📊 test_result.json
**Propósito**: Resultado completo estructurado
**Formato**: JSON
**Contenido**:
- Test ID y nombre
- Timestamps de inicio/fin
- Duración total
- Estado final (passed/failed)
- Detalles de cada paso:
  - Request completo (headers, body)
  - Response completo
  - Status codes
  - Duraciones
  - Errores

**Cuándo usar**:
- Para análisis automatizado
- Para integración con herramientas de CI/CD
- Para procesamiento programático

**Ejemplo de uso**:
```python
import json
with open('test_result.json') as f:
    result = json.load(f)
    print(f"Test: {result['test_name']}")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
```

---

### 📊 test_report.txt
**Propósito**: Reporte resumido legible
**Formato**: Texto plano
**Contenido**:
- Información básica del test
- Estado general
- Resumen de cada paso
- Tiempos de ejecución

**Cuándo usar**: Para revisión rápida en terminal

---

### 📊 step_1_Generate_Token.json
**Propósito**: Detalle completo del Paso 1
**Formato**: JSON
**Contenido**:
- Request enviado
- Response recibida
- Token JWT generado
- Headers
- Duración
- Status codes

**Cuándo usar**: Para análisis específico del paso de generación de token

---

### 📊 step_2_Search_Installments.json
**Propósito**: Detalle completo del Paso 2
**Formato**: JSON
**Contenido**:
- Request enviado (con token)
- Response recibida
- Error 500 capturado
- Headers
- Duración
- Status codes

**Cuándo usar**: Para análisis del error en búsqueda de cuotas

---

## 🎯 Flujos de Trabajo

### Flujo 1: Primera Revisión
```
1. Leer RESUMEN_EJECUTIVO.md
2. Revisar test_report.txt
3. Si necesita más detalles → ANALISIS_RESULTADOS.md
```

### Flujo 2: Troubleshooting Técnico
```
1. Leer ANALISIS_RESULTADOS.md
2. Ejecutar diagnose_environment.py
3. Revisar step_2_Search_Installments.json
4. Revisar logs del servidor
```

### Flujo 3: Re-ejecución de Prueba
```
1. Leer README.md (sección "Cómo Ejecutar")
2. Verificar ambiente con diagnose_environment.py
3. Ejecutar test_cpi_001.py
4. Revisar nuevos resultados
```

### Flujo 4: Reporte a Stakeholders
```
1. Usar RESUMEN_EJECUTIVO.md como base
2. Adjuntar test_report.txt
3. Si es técnico → adjuntar ANALISIS_RESULTADOS.md
4. Incluir TransactionId y TokenId para tracking
```

---

## 🔗 Enlaces Relacionados

### Documentación de APIs
- [Documentación Generate Token](../Documentación_API_Generate_Token.md)
- [Documentación Search Installments](../Documentación%20API_%20Búsqueda%20de%20Cuotas%20(Search%20Installments).md)

### Casos de Prueba
- [Casos de Prueba Generate Token](../Casos_Prueba_API_Generate_Token.md)
- [Casos de Prueba Search Installments](../Casos_Prueba_API_Search_Installments.md)
- [Casos de Integración Completa](../Casos_Prueba_Integracion_Completa.md)

---

## 📞 Información de Soporte

### Para Reportar Problemas

**Incluir**:
- TransactionId: `TXN1761677772192`
- TokenId: `0ab78e53-1a49-4f81-9604-b6c1b9d6075f`
- Timestamp: `2025-10-28 13:56:12 - 13:56:23`
- Archivo: `test_result.json`
- Archivo: `ANALISIS_RESULTADOS.md`

**Contactos**:
- DevOps/Infraestructura (servicio caído)
- Desarrollo Backend (error de aplicación)
- QA Team Lead (ambiente de pruebas)

---

## 🔄 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2025-10-28 | Ejecución inicial - Error 500 identificado |

---

## 📊 Estadísticas

```
Total de archivos:     9
Tamaño total:         ~50 KB
Scripts ejecutables:   2
Documentos:           4
Resultados:           3

Tiempo de ejecución:  10.85 segundos
Pasos exitosos:       1/2 (50%)
Errores encontrados:  1 (Error 500)
```

---

**Última actualización**: 2025-10-28 14:00
**Preparado por**: Sistema automatizado de pruebas
