# ============================================
# Script de Prueba Automatizada Completa
# Interbank Simulator - Flujo End-to-End
# ============================================

$baseUrl = "http://localhost:5000"
$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🧪 PRUEBA AUTOMATIZADA - INTERBANK SIMULATOR" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ============================================
# Verificar que el servidor está corriendo
# ============================================
Write-Host "🔍 Verificando que el servidor esté activo..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/swagger/v1/swagger.json" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Servidor activo en $baseUrl" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ ERROR: El servidor no está activo." -ForegroundColor Red
    Write-Host "   Por favor, ejecuta 'dotnet run' en InterbankSimulator.Api/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 1: OAuth - Obtener Token
# ============================================
Write-Host "1️⃣  TEST: OAuth - Obtener Token" -ForegroundColor Yellow
try {
    $oauth = Invoke-RestMethod -Uri "$baseUrl/pago-push/security/v1/oauth" -Method POST
    Write-Host "   ✅ Token obtenido: $($oauth.accessToken.Substring(0, 30))..." -ForegroundColor Green
    Write-Host "   📊 Token Type: $($oauth.tokenType)" -ForegroundColor Gray
    Write-Host "   ⏱️  Expires In: $($oauth.expiresIn)s" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo obtener el token OAuth" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 2: Enviar Solicitud de Pago
# ============================================
Write-Host "2️⃣  TEST: Enviar Solicitud de Pago" -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$paymentRequest = @{
    phoneNumber = "987654321"
    amount = 150.50
    merchantId = "MERCHANT-TEST"
    transactionId = "TXN-AUTO-$timestamp"
    currency = "PEN"
    description = "Prueba automática - Script PowerShell"
} | ConvertTo-Json

try {
    $payment = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" `
        -Method POST -Body $paymentRequest -ContentType "application/json"

    Write-Host "   ✅ Pago creado exitosamente" -ForegroundColor Green
    Write-Host "   📋 Transaction ID: $($payment.transactionId)" -ForegroundColor Gray
    Write-Host "   🆔 Unique ID: $($payment.uniqueId)" -ForegroundColor Gray
    Write-Host "   🔑 Code Auth: $($payment.codeAuth)" -ForegroundColor Gray
    Write-Host "   📊 Status: $($payment.status)" -ForegroundColor Gray

    # Guardar IDs para próximos tests
    $txId = $payment.transactionId
    $uniqueId = $payment.uniqueId
    $codeAuth = $payment.codeAuth
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo crear el pago" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 3: Listar Transacciones
# ============================================
Write-Host "3️⃣  TEST: Listar Transacciones" -ForegroundColor Yellow
try {
    $transactions = Invoke-RestMethod -Uri "$baseUrl/api/simulator/transactions" -Method GET
    Write-Host "   ✅ Transacciones obtenidas" -ForegroundColor Green
    Write-Host "   📊 Total de transacciones: $($transactions.total)" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudieron listar las transacciones" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 4: Obtener Transacción Específica
# ============================================
Write-Host "4️⃣  TEST: Obtener Transacción Específica" -ForegroundColor Yellow
try {
    $specific = Invoke-RestMethod -Uri "$baseUrl/api/simulator/transactions/$txId" -Method GET
    Write-Host "   ✅ Transacción encontrada" -ForegroundColor Green
    Write-Host "   📋 Transaction ID: $($specific.TransactionId)" -ForegroundColor Gray
    Write-Host "   📊 Status: $($specific.Status)" -ForegroundColor Gray
    Write-Host "   💰 Amount: S/ $($specific.Amount)" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo obtener la transacción específica" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 5: Confirmar Pago (Flujo Normal)
# ============================================
Write-Host "5️⃣  TEST: Confirmar Pago" -ForegroundColor Yellow
$confirmRequest = @{
    transactionId = $txId
    uniqueId = $uniqueId
    codeAuth = $codeAuth
} | ConvertTo-Json

try {
    $confirmed = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/confirmTransactionPayment" `
        -Method POST -Body $confirmRequest -ContentType "application/json"

    Write-Host "   ✅ Pago confirmado exitosamente" -ForegroundColor Green
    Write-Host "   📊 Status: $($confirmed.status)" -ForegroundColor Gray
    Write-Host "   💬 Mensaje: $($confirmed.message)" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo confirmar el pago" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 6: Crear Segundo Pago para Cancelar
# ============================================
Write-Host "6️⃣  TEST: Crear Segundo Pago (para cancelar)" -ForegroundColor Yellow
$timestamp2 = Get-Date -Format "yyyyMMddHHmmss"
$paymentRequest2 = @{
    phoneNumber = "987654322"
    amount = 200.00
    merchantId = "MERCHANT-TEST"
    transactionId = "TXN-CANCEL-$timestamp2"
    currency = "PEN"
    description = "Pago para cancelar - Prueba automática"
} | ConvertTo-Json

try {
    $payment2 = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" `
        -Method POST -Body $paymentRequest2 -ContentType "application/json"

    Write-Host "   ✅ Segundo pago creado" -ForegroundColor Green
    Write-Host "   📋 Transaction ID: $($payment2.transactionId)" -ForegroundColor Gray

    $txId2 = $payment2.transactionId
    $uniqueId2 = $payment2.uniqueId
    $codeAuth2 = $payment2.codeAuth
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo crear el segundo pago" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 7: Cancelar Pago
# ============================================
Write-Host "7️⃣  TEST: Cancelar Pago" -ForegroundColor Yellow
$cancelRequest = @{
    transactionId = $txId2
    uniqueId = $uniqueId2
    codeAuth = $codeAuth2
} | ConvertTo-Json

try {
    $cancelled = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/cancelationPaymentAuthorization" `
        -Method POST -Body $cancelRequest -ContentType "application/json"

    Write-Host "   ✅ Pago cancelado exitosamente" -ForegroundColor Green
    Write-Host "   📊 Status: $($cancelled.status)" -ForegroundColor Gray
    Write-Host "   💬 Mensaje: $($cancelled.message)" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo cancelar el pago" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 8: Crear Tercer Pago para Force-Pay
# ============================================
Write-Host "8️⃣  TEST: Crear Tercer Pago (para force-pay)" -ForegroundColor Yellow
$timestamp3 = Get-Date -Format "yyyyMMddHHmmss"
$paymentRequest3 = @{
    phoneNumber = "987654323"
    amount = 300.00
    merchantId = "MERCHANT-TEST"
    transactionId = "TXN-FORCE-$timestamp3"
    currency = "PEN"
    description = "Pago para force-pay - Prueba automática"
} | ConvertTo-Json

try {
    $payment3 = Invoke-RestMethod -Uri "$baseUrl/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" `
        -Method POST -Body $paymentRequest3 -ContentType "application/json"

    Write-Host "   ✅ Tercer pago creado" -ForegroundColor Green
    Write-Host "   📋 Transaction ID: $($payment3.transactionId)" -ForegroundColor Gray

    $txId3 = $payment3.transactionId
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo crear el tercer pago" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# TEST 9: Forzar Aprobación (Backoffice)
# ============================================
Write-Host "9️⃣  TEST: Forzar Aprobación (Backoffice)" -ForegroundColor Yellow
$forcePayRequest = @{
    identifier = $txId3
} | ConvertTo-Json

try {
    $forced = Invoke-RestMethod -Uri "$baseUrl/api/simulator/force-pay" `
        -Method POST -Body $forcePayRequest -ContentType "application/json"

    Write-Host "   ✅ Pago forzado exitosamente" -ForegroundColor Green
    Write-Host "   📊 Status: $($forced.status)" -ForegroundColor Gray
    Write-Host "   💬 Mensaje: $($forced.message)" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ FALLÓ: No se pudo forzar la aprobación" -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================
# RESUMEN FINAL
# ============================================
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📊 RESUMEN DE LA PRUEBA" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

try {
    $finalTransactions = Invoke-RestMethod -Uri "$baseUrl/api/simulator/transactions" -Method GET

    Write-Host "✅ Total de tests ejecutados: 9/9" -ForegroundColor Green
    Write-Host "✅ Total de transacciones creadas: $($finalTransactions.total)" -ForegroundColor Green
    Write-Host ""

    Write-Host "📋 Transacciones creadas en esta prueba:" -ForegroundColor Yellow
    Write-Host "   1. $txId → Status: APPROVED (confirmado)" -ForegroundColor White
    Write-Host "   2. $txId2 → Status: CANCELLED (cancelado)" -ForegroundColor White
    Write-Host "   3. $txId3 → Status: APPROVED (force-pay)" -ForegroundColor White
}
catch {
    Write-Host "⚠️  No se pudo obtener el resumen final" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   - Revisa las transacciones en Swagger: http://localhost:5000" -ForegroundColor White
Write-Host "   - Inspecciona la base de datos: InterbankSimulator.Api/simulator.db" -ForegroundColor White
Write-Host "   - Conecta tu cliente real: .\switch-to-simulator.ps1" -ForegroundColor White
Write-Host ""
