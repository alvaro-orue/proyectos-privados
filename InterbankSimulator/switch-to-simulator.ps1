# ============================================
# Script para cambiar las URLs del cliente
# al simulador local de Interbank
# ============================================

$clientConfigPath = "C:\Users\aaquispe\Desktop\REPOSITORIO2\izipay-digital-pw.0095.apibusiness.pagopush-81627d3ea858\ApiPaymentController\appsettings.json"

Write-Host "🔄 Cambiando configuración del cliente a SIMULADOR LOCAL..." -ForegroundColor Cyan

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

# Modificar las URLs al simulador
$config.PagoPushEndPoints.BaseUrl = "http://localhost:5000"
$config.PagoPushEndPoints.OAuthUrl = "http://localhost:5000/pago-push/security/v1/oauth"
$config.PagoPushEndPoints.SendPaymentUrl = "http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification"
$config.PagoPushEndPoints.ConfirmPaymentUrl = "http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment"
$config.PagoPushEndPoints.CancelPaymentUrl = "http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization"

# Guardar cambios
try {
    $config | ConvertTo-Json -Depth 10 | Set-Content $clientConfigPath -Encoding UTF8
    Write-Host "✅ Configuración actualizada exitosamente." -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 URLs configuradas:" -ForegroundColor Cyan
    Write-Host "   BaseUrl: http://localhost:5000" -ForegroundColor White
    Write-Host "   OAuth: http://localhost:5000/pago-push/security/v1/oauth" -ForegroundColor White
    Write-Host "   SendPayment: http://localhost:5000/pago-push/payment/v1/sendPaymentAuthorizationRequestNotification" -ForegroundColor White
    Write-Host "   ConfirmPayment: http://localhost:5000/pago-push/payment/v1/confirmTransactionPayment" -ForegroundColor White
    Write-Host "   CancelPayment: http://localhost:5000/pago-push/payment/v1/cancelationPaymentAuthorization" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 El cliente ahora apunta al SIMULADOR LOCAL." -ForegroundColor Green
    Write-Host "   Asegúrate de ejecutar el simulador con: dotnet run" -ForegroundColor Yellow
}
catch {
    Write-Host "❌ ERROR: No se pudo guardar el archivo." -ForegroundColor Red
    Write-Host "   Detalle: $_" -ForegroundColor Yellow
    Write-Host "   Restaurando backup..." -ForegroundColor Yellow
    Copy-Item $backupPath $clientConfigPath -Force
    Write-Host "✅ Backup restaurado." -ForegroundColor Green
    exit 1
}
