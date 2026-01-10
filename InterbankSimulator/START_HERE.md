# 🚀 START HERE - Interbank Simulator

## ¡Bienvenido! Este es tu punto de partida.

---

## ⚡ Inicio Ultra Rápido (2 minutos)

### 1. Ejecutar el Simulador

```bash
cd InterbankSimulator.Api
dotnet run
```

Verás:
```
🚀 Iniciando Interbank Simulator...
✅ Base de datos SQLite inicializada correctamente.
✅ Simulador listo. Accede a Swagger en: http://localhost:5000
```

### 2. Abrir Swagger UI

Abre tu navegador: [http://localhost:5000](http://localhost:5000)

### 3. Probar un Endpoint

En Swagger UI:
1. Expande `POST /pago-push/payment/v1/sendPaymentAuthorizationRequestNotification`
2. Click en "Try it out"
3. Edita el JSON de ejemplo
4. Click en "Execute"
5. ¡Listo! Verás la respuesta.

---

## 📚 Documentación Disponible

| Documento | Cuándo Leerlo |
|-----------|---------------|
| **[QUICK_START.md](QUICK_START.md)** | 👈 **Empieza aquí** - Tutorial paso a paso |
| **[README.md](README.md)** | Documentación técnica completa |
| **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** | Vista ejecutiva del proyecto |
| **[TESTING_EXAMPLES.md](TESTING_EXAMPLES.md)** | Ejemplos de pruebas (cURL, PowerShell) |
| **[INSTRUCCIONES_CONEXION_CLIENTE.md](INSTRUCCIONES_CONEXION_CLIENTE.md)** | Conectar tu cliente real al simulador |
| **[ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)** | Arquitectura y componentes |

---

## 🎯 Flujos Comunes

### Flujo 1: Solo quiero probar rápido
1. `cd InterbankSimulator.Api && dotnet run`
2. Abre [http://localhost:5000](http://localhost:5000)
3. Usa Swagger UI para probar endpoints

### Flujo 2: Quiero hacer pruebas automatizadas
1. `cd InterbankSimulator.Api && dotnet run` (en una terminal)
2. `.\test-simulator.ps1` (en otra terminal)
3. Observa todas las pruebas ejecutándose automáticamente

### Flujo 3: Quiero conectar mi cliente real
1. `cd InterbankSimulator.Api && dotnet run`
2. `.\switch-to-simulator.ps1`
3. Ejecuta tu cliente normalmente

### Flujo 4: Quiero inspeccionar la base de datos
1. Descarga [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Abre `InterbankSimulator.Api/simulator.db`
3. Explora la tabla `SimulatedTransactions`

---

## 🛠️ Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `test-simulator.ps1` | Ejecuta 9 pruebas automatizadas end-to-end |
| `switch-to-simulator.ps1` | Conecta el cliente real al simulador |
| `switch-to-production.ps1` | Restaura el cliente a producción |

---

## 📋 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/pago-push/security/v1/oauth` | POST | Obtener token OAuth |
| `/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification` | POST | Crear pago |
| `/pago-push/payment/v1/confirmTransactionPayment` | POST | Confirmar pago |
| `/pago-push/payment/v1/cancelationPaymentAuthorization` | POST | Cancelar pago |
| `/api/simulator/force-pay` | POST | **Backoffice:** Forzar aprobación |
| `/api/simulator/transactions` | GET | **Backoffice:** Listar transacciones |

Todos documentados en: [http://localhost:5000](http://localhost:5000)

---

## 🔧 Solución Rápida de Problemas

### "El puerto 5000 está ocupado"
Edita `InterbankSimulator.Api/appsettings.json`:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5001"  ← Cambia aquí
      }
    }
  }
}
```

### "No se puede conectar al simulador"
1. Verifica que el simulador esté corriendo (`dotnet run`)
2. Revisa que el puerto sea el correcto
3. Verifica que no haya firewall bloqueando

### "La base de datos no se crea"
1. Verifica permisos de escritura en la carpeta
2. Ejecuta `dotnet clean && dotnet build && dotnet run`

---

## 🎓 Conceptos Clave

### ¿Qué es este proyecto?
Un **Mock Server** que simula los servicios de Interbank (Pago Push). Permite desarrollar y probar sin depender del servicio real.

### ¿Qué tecnologías usa?
- .NET 10
- Dapper (ORM)
- SQLite (base de datos)
- Swagger (documentación)

### ¿Para qué sirve?
- Desarrollo local sin conexión a Interbank
- Testing automático
- Debugging de flujos de pago
- Demos sin credenciales reales

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa la documentación**: Cada archivo `.md` tiene información detallada
2. **Consulta los ejemplos**: `TESTING_EXAMPLES.md` tiene casos completos
3. **Verifica los logs**: La consola muestra errores detallados
4. **Inspecciona la base de datos**: Usa SQLite Browser

---

## ✅ Checklist Antes de Empezar

- [ ] Tengo .NET 10 instalado (`dotnet --version` → debe mostrar 10.x.x)
- [ ] Estoy en el directorio correcto (`InterbankSimulator/`)
- [ ] El puerto 5000 está disponible
- [ ] Tengo permisos de escritura en la carpeta

**Si todos los checks están ✅, ejecuta:**

```bash
cd InterbankSimulator.Api
dotnet run
```

---

## 🎉 ¡Listo!

El simulador está completamente funcional. Todos los archivos, endpoints y documentación están listos.

**Próximo paso:** Lee [QUICK_START.md](QUICK_START.md) para un tutorial completo.

---

**Creado:** 2026-01-09
**Framework:** .NET 10
**Estado:** ✅ Completado y Probado
