# Casos de Prueba de Integración - Flujo Completo: Generate Token + Search Installments

## Información General
- **Flujo**: Generación de Token → Búsqueda de Cuotas
- **Ambiente**: QA
- **Fecha**: 2025-10-28
- **Versión**: 1.0

---

## DATOS DE CONFIGURACIÓN - AMBIENTE QA

### Endpoints
```
Generate Token: https://qa-api-pw.izipay.pe/security/v1/Token/Generate
Search Installments: https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search
```

### Credenciales
```
Merchant Code: 4078370
API Key (publicKey): VErethUtraQuxas57wuMuquprADrAHAb
```

### Variables de Entorno (Postman/Newman)
```json
{
  "qa_token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
  "qa_installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
  "merchant_code": "4078370",
  "public_key": "VErethUtraQuxas57wuMuquprADrAHAb"
}
```

---

## 1. CASOS DE PRUEBA DE INTEGRACIÓN - FLUJO COMPLETO

### CPI-001: Flujo completo exitoso - Generar token y buscar cuotas
**Objetivo**: Verificar el flujo completo desde la generación del token hasta la búsqueda de cuotas.

**Precondiciones**:
- Merchant activo en ambiente QA
- Credenciales válidas

**Pasos**:

**PASO 1: Generar Token**
```bash
curl --request POST \
  --url https://qa-api-pw.izipay.pe/security/v1/Token/Generate \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: TXN1730089200001' \
  --data '{
    "requestSource": "ECOMMERCE",
    "merchantCode": "4078370",
    "orderNumber": "ORDER20241028001",
    "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
    "amount": "100.00"
  }'
```

**Resultado esperado PASO 1**:
- Status Code: `200 OK`
- Response:
```json
{
  "code": "00",
  "message": "OK",
  "response": {
    "token": "{TOKEN_GENERADO}"
  }
}
```

**PASO 2: Buscar Cuotas usando el token generado**
```bash
curl --request POST \
  --url https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {TOKEN_DEL_PASO_1}' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: TXN1730089200001' \
  --data '{
    "bin": "545545",
    "merchantCode": "4078370",
    "language": "ESP"
  }'
```

**Resultado esperado PASO 2**:
- Status Code: `200 OK`
- Response:
```json
{
  "code": "00",
  "message": "Aprobado",
  "header": {
    "transactionStartDatetime": "2024-10-28 12:25:47.000",
    "transactionEndDatetime": "2024-10-28 12:25:47.000",
    "millis": "1201"
  },
  "response": {
    "merchantCode": "4078370",
    "bin": "545545",
    "issuerName": "SCOTIABANK",
    "installments": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    "deferred": "0",
    "result": {
      "messageFriendly": "Aprobado"
    }
  }
}
```

---

### CPI-002: Múltiples búsquedas de cuotas con diferentes BINs usando el mismo token
**Objetivo**: Verificar que un token puede usarse solo una vez.

**Pasos**:
1. Generar token con transactionId "TXN1730089200002"
2. Buscar cuotas para BIN "545545" (primera llamada)
3. Intentar buscar cuotas para BIN "411111" con el mismo token (segunda llamada)

**Resultado esperado**:
- Primera búsqueda: `200 OK`
- Segunda búsqueda: `401 Unauthorized` (token ya usado)

---

### CPI-003: Validar que el transactionId es consistente entre ambas llamadas
**Objetivo**: Verificar que se debe usar el mismo transactionId en ambas APIs.

**Pasos**:
1. Generar token con transactionId "TXN1730089200003"
2. Intentar buscar cuotas con transactionId diferente "TXN1730089200999"

**Resultado esperado**:
- Búsqueda de cuotas rechazada
- Error indicando transactionId inconsistente

---

### CPI-004: Flujo con token expirado
**Objetivo**: Verificar comportamiento cuando el token expira antes de ser usado.

**Pasos**:
1. Generar token
2. Esperar 16 minutos
3. Intentar buscar cuotas con el token expirado

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje: Token expirado o inválido

---

### CPI-005: Flujo con diferentes BINs de tarjetas
**Objetivo**: Verificar búsqueda de cuotas para diferentes emisores.

**Datos de prueba**:

| Test Case | BIN | Emisor Esperado | TransactionId |
|-----------|-----|----------------|---------------|
| A | 545545 | SCOTIABANK | TXN1730089200005A |
| B | 411111 | VISA | TXN1730089200005B |
| C | 424242 | VISA | TXN1730089200005C |
| D | 552277 | MASTERCARD | TXN1730089200005D |

**Pasos para cada caso**:
1. Generar token único
2. Buscar cuotas con el BIN correspondiente

**Resultado esperado**:
- Cada búsqueda retorna cuotas válidas para el emisor
- `response.issuerName` coincide con el emisor esperado

---

### CPI-006: Flujo con amount 0.00 (sin depósito)
**Objetivo**: Verificar flujo completo para operaciones sin depósito.

**PASO 1: Generar Token**
```json
{
  "requestSource": "ECOMMERCE",
  "merchantCode": "4078370",
  "orderNumber": "ORDER20241028006",
  "publicKey": "VErethUtraQuxas57wuMuquprADrAHAb",
  "amount": "0.00"
}
```

**PASO 2: Buscar Cuotas**
- Usar token generado
- Buscar cuotas normalmente

**Resultado esperado**:
- Ambos pasos exitosos
- Cuotas retornadas correctamente

---

### CPI-007: Flujo con idioma inglés
**Objetivo**: Verificar flujo con mensajes en inglés.

**PASO 2: Buscar Cuotas con language="ENG"**
```json
{
  "bin": "545545",
  "merchantCode": "4078370",
  "language": "ENG"
}
```

**Resultado esperado**:
- Mensajes en inglés (ej: "Approved" en lugar de "Aprobado")

---

### CPI-008: Flujo con merchantCode diferente en Search Installments
**Objetivo**: Verificar que el merchantCode debe ser consistente o autorizado.

**Pasos**:
1. Generar token con merchantCode "4078370"
2. Intentar buscar cuotas con merchantCode "9999999"

**Resultado esperado**:
- Error de autorización o validación de merchant

---

### CPI-009: Validar tiempo total del flujo completo
**Objetivo**: Medir el tiempo total de respuesta del flujo.

**Métricas a validar**:
- Tiempo generación token < 2 segundos
- Tiempo búsqueda cuotas < 2 segundos
- Tiempo total del flujo < 4 segundos

---

### CPI-010: Flujo con BIN no registrado o sin cuotas
**Objetivo**: Verificar comportamiento con BIN válido pero sin cuotas configuradas.

**PASO 2: Buscar Cuotas con BIN no configurado**
```json
{
  "bin": "999999",
  "merchantCode": "4078370",
  "language": "ESP"
}
```

**Resultado esperado**:
- Status Code: `200 OK` o `404 Not Found`
- Si 200, `code` diferente de "00" con mensaje apropiado
- Array de installments vacío o null

---

## 2. CASOS DE PRUEBA DE CONCURRENCIA

### CPI-C001: Múltiples transacciones simultáneas
**Objetivo**: Verificar que el sistema maneja correctamente múltiples transacciones concurrentes.

**Pasos**:
1. Ejecutar 10 flujos completos simultáneamente
2. Cada flujo con transactionId único
3. Diferentes BINs y orderNumbers

**Resultado esperado**:
- Todos los flujos se completan exitosamente
- Sin interferencia entre transacciones
- Tiempos de respuesta dentro de lo esperado

---

### CPI-C002: Rate limiting en flujo completo
**Objetivo**: Verificar límites de tasa en ambas APIs.

**Pasos**:
1. Enviar múltiples solicitudes rápidas de generación de token
2. Usar tokens generados para búsqueda de cuotas

**Resultado esperado**:
- `429 Too Many Requests` al exceder límites
- Headers con información de retry

---

## 3. CASOS DE PRUEBA DE ERRORES Y RECUPERACIÓN

### CPI-E001: Token inválido o malformado
**Objetivo**: Verificar validación de token en Search Installments.

**Pasos**:
1. NO generar token válido
2. Intentar buscar cuotas con token inventado

```bash
Authorization: Bearer INVALID_TOKEN_12345
```

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje indicando token inválido

---

### CPI-E002: Sin header Authorization
**Objetivo**: Verificar que Authorization es obligatorio.

**Pasos**:
1. Generar token válido
2. Buscar cuotas sin incluir header Authorization

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje indicando autenticación requerida

---

### CPI-E003: Formato incorrecto del header Authorization
**Objetivo**: Verificar validación del formato Bearer.

**Pasos**:
1. Generar token válido
2. Usar formato incorrecto: `Authorization: {TOKEN}` (sin "Bearer")

**Resultado esperado**:
- Status Code: `401 Unauthorized`
- Mensaje indicando formato inválido

---

### CPI-E004: Reintentar con nuevo token después de error
**Objetivo**: Verificar recuperación después de token expirado.

**Pasos**:
1. Generar primer token
2. Esperar expiración o usarlo
3. Generar nuevo token con nuevo transactionId
4. Buscar cuotas con el nuevo token

**Resultado esperado**:
- Nueva generación exitosa
- Búsqueda exitosa con nuevo token

---

## 4. CASOS DE PRUEBA DE SEGURIDAD INTEGRADA

### CPI-S001: Verificar que tokens no son reutilizables
**Objetivo**: Confirmar que cada token es de un solo uso.

**Pasos**:
1. Generar token
2. Buscar cuotas (primera vez) - Éxito
3. Buscar cuotas con mismo token (segunda vez) - Fallo

**Resultado esperado**:
- Primera búsqueda: `200 OK`
- Segunda búsqueda: `401 Unauthorized`

---

### CPI-S002: Verificar aislamiento entre comercios
**Objetivo**: Confirmar que no hay acceso cruzado entre merchants.

**Pasos**:
1. Generar token para merchant "4078370"
2. Intentar buscar cuotas especificando otro merchantCode

**Resultado esperado**:
- Error de autorización
- Sin acceso a datos de otro comercio

---

### CPI-S003: Protección de credenciales en logs
**Objetivo**: Verificar que publicKey y tokens no se registran en logs.

**Pasos**:
1. Ejecutar flujo completo
2. Revisar logs del sistema

**Resultado esperado**:
- PublicKey y tokens ofuscados en logs
- Solo se muestran últimos 4 caracteres o hash

---

## 5. COLECCIÓN POSTMAN PARA PRUEBAS

### Pre-request Script Global
```javascript
// Generar transactionId único
pm.environment.set("transactionId", "TXN" + Date.now() + Math.floor(Math.random() * 1000));

// Generar orderNumber único
pm.environment.set("orderNumber", "ORDER" + Date.now());
```

### Test Script para Generate Token
```javascript
// Validar respuesta exitosa
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.code).to.eql("00");
    pm.expect(jsonData.response.token).to.be.a('string');
    pm.expect(jsonData.response.token.length).to.be.above(100);

    // Guardar token para usar en siguiente request
    pm.environment.set("session_token", jsonData.response.token);
});

pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});
```

### Test Script para Search Installments
```javascript
// Validar respuesta exitosa
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Installments found", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.code).to.eql("00");
    pm.expect(jsonData.message).to.include("Aprobado");
    pm.expect(jsonData.response.installments).to.be.an('array');
    pm.expect(jsonData.response.installments.length).to.be.above(0);
});

pm.test("Merchant code matches", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.response.merchantCode).to.eql(pm.environment.get("merchant_code"));
});

pm.test("BIN matches", function () {
    var jsonData = pm.response.json();
    var requestBody = JSON.parse(pm.request.body.raw);
    pm.expect(jsonData.response.bin).to.eql(requestBody.bin);
});

pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});
```

---

## 6. SCRIPT DE AUTOMATIZACIÓN COMPLETO

### JavaScript/Node.js
```javascript
const fetch = require('node-fetch');

class IzipayTestSuite {
  constructor() {
    this.config = {
      tokenUrl: 'https://qa-api-pw.izipay.pe/security/v1/Token/Generate',
      installmentsUrl: 'https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search',
      merchantCode: '4078370',
      publicKey: 'VErethUtraQuxas57wuMuquprADrAHAb'
    };
  }

  generateTransactionId() {
    return `TXN${Date.now()}${Math.floor(Math.random() * 10000)}`;
  }

  generateOrderNumber() {
    return `ORDER${Date.now()}`;
  }

  async generateToken(amount = '100.00') {
    const transactionId = this.generateTransactionId();
    const orderNumber = this.generateOrderNumber();

    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'transactionId': transactionId
      },
      body: JSON.stringify({
        requestSource: 'ECOMMERCE',
        merchantCode: this.config.merchantCode,
        orderNumber: orderNumber,
        publicKey: this.config.publicKey,
        amount: amount
      })
    });

    const data = await response.json();

    if (response.status !== 200 || data.code !== '00') {
      throw new Error(`Token generation failed: ${data.message}`);
    }

    return {
      token: data.response.token,
      transactionId: transactionId
    };
  }

  async searchInstallments(bin, token, transactionId, language = 'ESP') {
    const response = await fetch(this.config.installmentsUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'transactionId': transactionId
      },
      body: JSON.stringify({
        bin: bin,
        merchantCode: this.config.merchantCode,
        language: language
      })
    });

    const data = await response.json();

    if (response.status !== 200 || data.code !== '00') {
      throw new Error(`Installments search failed: ${data.message}`);
    }

    return data;
  }

  async runTest(testName, testFn) {
    try {
      console.log(`\n🧪 Running: ${testName}`);
      const startTime = Date.now();
      await testFn();
      const duration = Date.now() - startTime;
      console.log(`✅ PASSED (${duration}ms): ${testName}`);
      return { test: testName, status: 'PASSED', duration };
    } catch (error) {
      console.log(`❌ FAILED: ${testName}`);
      console.log(`   Error: ${error.message}`);
      return { test: testName, status: 'FAILED', error: error.message };
    }
  }

  async runAllTests() {
    console.log('='.repeat(60));
    console.log('IZIPAY API INTEGRATION TEST SUITE');
    console.log('='.repeat(60));

    const results = [];

    // Test 1: Flujo completo exitoso
    results.push(await this.runTest('CPI-001: Flujo completo exitoso', async () => {
      const { token, transactionId } = await this.generateToken('100.00');
      const installments = await this.searchInstallments('545545', token, transactionId);

      if (!installments.response.installments || installments.response.installments.length === 0) {
        throw new Error('No installments returned');
      }
    }));

    // Test 2: Token de un solo uso
    results.push(await this.runTest('CPI-002: Token de un solo uso', async () => {
      const { token, transactionId } = await this.generateToken('100.00');

      // Primera llamada - debe funcionar
      await this.searchInstallments('545545', token, transactionId);

      // Segunda llamada - debe fallar
      try {
        await this.searchInstallments('411111', token, transactionId);
        throw new Error('Token should not be reusable');
      } catch (error) {
        if (!error.message.includes('failed')) {
          throw error;
        }
        // Error esperado
      }
    }));

    // Test 3: Diferentes BINs
    results.push(await this.runTest('CPI-005: Diferentes BINs', async () => {
      const bins = ['545545', '411111', '424242'];

      for (const bin of bins) {
        const { token, transactionId } = await this.generateToken('100.00');
        const installments = await this.searchInstallments(bin, token, transactionId);

        if (installments.response.bin !== bin) {
          throw new Error(`BIN mismatch: expected ${bin}, got ${installments.response.bin}`);
        }
      }
    }));

    // Test 4: Amount 0.00
    results.push(await this.runTest('CPI-006: Amount 0.00', async () => {
      const { token, transactionId } = await this.generateToken('0.00');
      await this.searchInstallments('545545', token, transactionId);
    }));

    // Test 5: Idioma inglés
    results.push(await this.runTest('CPI-007: Idioma inglés', async () => {
      const { token, transactionId } = await this.generateToken('100.00');
      const installments = await this.searchInstallments('545545', token, transactionId, 'ENG');
      // Verificar que los mensajes están en inglés
    }));

    // Test 6: Token inválido
    results.push(await this.runTest('CPI-E001: Token inválido', async () => {
      const transactionId = this.generateTransactionId();

      try {
        await this.searchInstallments('545545', 'INVALID_TOKEN_123', transactionId);
        throw new Error('Invalid token should be rejected');
      } catch (error) {
        if (!error.message.includes('failed')) {
          throw error;
        }
        // Error esperado
      }
    }));

    // Resumen
    console.log('\n' + '='.repeat(60));
    console.log('TEST SUMMARY');
    console.log('='.repeat(60));

    const passed = results.filter(r => r.status === 'PASSED').length;
    const failed = results.filter(r => r.status === 'FAILED').length;

    console.log(`Total Tests: ${results.length}`);
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`Success Rate: ${((passed / results.length) * 100).toFixed(2)}%`);

    if (failed > 0) {
      console.log('\nFailed Tests:');
      results.filter(r => r.status === 'FAILED').forEach(r => {
        console.log(`  - ${r.test}`);
        console.log(`    ${r.error}`);
      });
    }

    return results;
  }
}

// Ejecutar tests
(async () => {
  const suite = new IzipayTestSuite();
  await suite.runAllTests();
})();
```

### Uso del script
```bash
# Instalar dependencias
npm install node-fetch

# Ejecutar tests
node integration_tests.js
```

---

## 7. CHECKLIST DE VALIDACIÓN

### Antes de Ejecutar Pruebas
- [ ] Verificar conectividad con ambiente QA
- [ ] Confirmar credenciales vigentes
- [ ] Validar que merchant está activo
- [ ] Preparar datos de prueba (BINs, amounts, etc.)

### Durante Ejecución
- [ ] Monitorear tiempos de respuesta
- [ ] Verificar logs de aplicación
- [ ] Capturar evidencias (screenshots, responses)
- [ ] Documentar cualquier comportamiento inesperado

### Después de Ejecutar
- [ ] Revisar todos los tokens generados fueron de un solo uso
- [ ] Confirmar que no hay tokens activos sin usar
- [ ] Validar que no hay fugas de credenciales en logs
- [ ] Actualizar documentación con hallazgos

---

## 8. CRITERIOS DE ACEPTACIÓN DEL FLUJO COMPLETO

### Funcionales
- ✓ Generación de token exitosa en <2 segundos
- ✓ Token válido para búsqueda de cuotas
- ✓ Búsqueda retorna cuotas correctas para BIN
- ✓ Token es de un solo uso
- ✓ Token expira en ~15 minutos
- ✓ TransactionId se mantiene consistente

### No Funcionales
- ✓ Tiempo total del flujo <4 segundos
- ✓ Sin memory leaks en pruebas de carga
- ✓ Rate limiting funciona correctamente
- ✓ Logs no exponen credenciales

### Seguridad
- ✓ Tokens no reutilizables
- ✓ Aislamiento entre merchants
- ✓ Protección contra inyecciones
- ✓ HTTPS obligatorio

---

## 9. MATRIZ DE CASOS VS PRIORIDAD

| ID | Descripción | Prioridad | Frecuencia | Impacto |
|----|-------------|-----------|------------|---------|
| CPI-001 | Flujo completo exitoso | CRÍTICA | Siempre | ALTO |
| CPI-002 | Token de un solo uso | CRÍTICA | Siempre | ALTO |
| CPI-003 | TransactionId consistente | ALTA | Siempre | ALTO |
| CPI-004 | Token expirado | ALTA | Regresión | MEDIO |
| CPI-005 | Diferentes BINs | ALTA | Siempre | ALTO |
| CPI-S001 | Tokens no reutilizables | CRÍTICA | Regresión | ALTO |
| CPI-E001 | Token inválido | MEDIA | Regresión | MEDIO |

---

## 10. TROUBLESHOOTING COMÚN

### Error: "Token generation failed"
**Causa**: PublicKey inválida o merchant inactivo
**Solución**: Verificar credenciales en portal QA

### Error: "Installments search failed - 401"
**Causa**: Token expirado o ya usado
**Solución**: Generar nuevo token

### Error: "TransactionId mismatch"
**Causa**: Usando diferentes transactionIds
**Solución**: Usar mismo transactionId en ambas llamadas

### Error: Timeout en requests
**Causa**: Problemas de red o ambiente QA caído
**Solución**: Verificar conectividad y estado del servicio

---

**Preparado por**: Claude
**Última actualización**: 2025-10-28
**Versión**: 1.0
**Ambiente**: QA
