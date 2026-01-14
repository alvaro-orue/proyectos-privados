using InterbankSimulator.Api.Infrastructure;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.Data.SqlClient;
using System.Data;

var builder = WebApplication.CreateBuilder(args);

// ===== CONFIGURACIÓN DE SERVICIOS =====

// Controladores
builder.Services.AddControllers();

// Configuración de Swagger/OpenAPI
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Inyección de dependencia: SQL Server Connection con Dapper
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connectionString = builder.Configuration.GetConnectionString("SqlServerConnection");
    var connection = new SqlConnection(connectionString);
    connection.Open();
    return connection;
});

// ===== INICIALIZACIÓN DE LA BASE DE DATOS =====
Console.WriteLine("🚀 Iniciando Interbank Simulator...");
// DatabaseBootstrap.Initialize();  // Ya no es necesario con SQL Server

var app = builder.Build();

// ===== CONFIGURACIÓN DEL PIPELINE HTTP =====

// IMPORTANTE: Configuración para IIS y proxies inversos
app.UseForwardedHeaders(new ForwardedHeadersOptions
{
    ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto
});

// Configuración del PathBase para aplicaciones en rutas virtuales de IIS
app.UsePathBase("/InterbankSimulator");

// Swagger habilitado en todos los entornos (desarrollo y producción)
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/InterbankSimulator/swagger/v1/swagger.json", "Interbank Simulator v1");
    options.RoutePrefix = string.Empty; // Swagger UI en la raíz relativa
});

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

// ===== INICIO DE LA APLICACIÓN =====
Console.WriteLine("✅ Simulador listo. Accede a Swagger en la ruta configurada");
Console.WriteLine("📋 Endpoints disponibles:");
Console.WriteLine("   - POST /pago-push/security/v1/oauth");
Console.WriteLine("   - POST /pago-push/payment/v1/sendPaymentAuthorizationRequestNotification");
Console.WriteLine("   - POST /pago-push/payment/v1/confirmTransactionPayment");
Console.WriteLine("   - POST /pago-push/payment/v1/cancelationPaymentAuthorization");

app.Run();
