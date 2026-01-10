# ============================================
# Script para restaurar las URLs del cliente
# a la API de producción de Interbank
# ============================================

$clientConfigPath = "C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json"

Write-Host "🔄 Restaurando configuración del cliente a PRODUCCIÓN (Interbank Real)..." -ForegroundColor Cyan

# Verificar si el archivo existe
if (-Not (Test-Path $clientConfigPath)) {
    Write-Host "❌ ERROR: No se encontró el archivo de configuración del cliente." -ForegroundColor Red
    Write-Host "   Ruta esperada: $clientConfigPath" -ForegroundColor Yellow
    exit 1
}

# Crear backup
$backupPath = "$clientConfigPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $clientConfigPath $backupPath
Write-Host "📦 Backup creado: $backupPath" -ForegroundColor Green

# Leer el archivo
try {
    $config = Get-Content $clientConfigPath -Raw | ConvertFrom-Json
}
catch {
    Write-Host "❌ ERROR: No se pudo leer el archivo JSON." -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    exit 1
}

# Verificar que la sección PagoPushEndPoints exista
if (-Not $config.PSObject.Properties.Name -contains "PagoPushEndPoints") {
    Write-Host "⚠️ ADVERTENCIA: No se encontró la sección 'PagoPushEndPoints' en el archivo." -ForegroundColor Yellow
    Write-Host "   Verifique manualmente el archivo de configuración." -ForegroundColor Yellow
    exit 1
}

# Modificar las URLs a producción
$config.PagoPushEndPoints.BaseUrl = "https://api.interbank.pe"
$config.PagoPushEndPoints.OAuthUrl = "https://api.interbank.pe/pago-push/security/v1/oauth"
$config.PagoPushEndPoints.SendPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification"
$config.PagoPushEndPoints.ConfirmPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/confirmTransactionPayment"
$config.PagoPushEndPoints.CancelPaymentUrl = "https://api.interbank.pe/pago-push/payment/v1/cancelationPaymentAuthorization"

# Guardar cambios
try {
    $config | ConvertTo-Json -Depth 10 | Set-Content $clientConfigPath -Encoding UTF8
    Write-Host "✅ Configuración restaurada exitosamente." -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 URLs configuradas:" -ForegroundColor Cyan
    Write-Host "   BaseUrl: https://api.interbank.pe" -ForegroundColor White
    Write-Host "   OAuth: https://api.interbank.pe/pago-push/security/v1/oauth" -ForegroundColor White
    Write-Host "   SendPayment: https://api.interbank.pe/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" -ForegroundColor White
    Write-Host "   ConfirmPayment: https://api.interbank.pe/pago-push/payment/v1/confirmTransactionPayment" -ForegroundColor White
    Write-Host "   CancelPayment: https://api.interbank.pe/pago-push/payment/v1/cancelationPaymentAuthorization" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️ El cliente ahora apunta a la API de PRODUCCIÓN REAL de Interbank." -ForegroundColor Yellow
    Write-Host "   ¡Ten cuidado! Las transacciones serán reales." -ForegroundColor Red
}
catch {
    Write-Host "❌ ERROR: No se pudo guardar el archivo." -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    Write-Host "   Restaurando backup..." -ForegroundColor Yellow
    Copy-Item $backupPath $clientConfigPath -Force
    Write-Host "✅ Backup restaurado." -ForegroundColor Green
    exit 1
}
