# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mock server simulating Interbank's "Pago Push" payment API for development and testing. Written in Spanish (Peru).

## Build & Run Commands

```bash
# Run the simulator (from project root)
cd InterbankSimulator.Api && dotnet run

# Build only
dotnet build InterbankSimulator.Api

# Clean build artifacts
dotnet clean InterbankSimulator.Api
```

The API runs on http://localhost:5000 with Swagger UI at the root path.

## Architecture

**Stack**: .NET 10, SQLite (local) / SQL Server (production), Dapper (micro-ORM), Swagger/OpenAPI

**Single-project structure** (`InterbankSimulator.Api/`):
- `Controllers/` - Two API controllers matching Interbank's API surface
- `Infrastructure/DatabaseBootstrap.cs` - SQLite initialization (creates `simulator.db` on startup)
- `Models/` - Request/Response DTOs with nested structures matching real Interbank API

**API Routes** (match real Interbank endpoints):
- `POST /pago-push/security/v1/oauth` - Mock OAuth token generation
- `POST /pago-push/payment/v1/sendPaymentAuthorizationRequestNotification` - Send payment request
- `POST /pago-push/payment/v1/confirmTransactionPayment` - Confirm transaction
- `POST /pago-push/payment/v1/cancelationPaymentAuthorization` - Cancel transaction

**Transaction States**: PENDING → APPROVED or CANCELLED

## Database

**Local (SQLite)**: File `simulator.db` auto-created in `InterbankSimulator.Api/`.

**Production (SQL Server)**: Schema `[Push].[SimulatedTransactions]` - see `[Push].[Sp_SimulatedTransactions].sql`.

**Table structure**:
- `IdTransactionPasarela` (PK) - Gateway transaction ID
- `IdOrder` - Commerce order ID
- `IdTransactionInterbank` - Interbank-generated ID (UNIQUE)
- `CommerceCode`, `CommerceName` - Commerce info
- `CellPhoneNumber` - Customer phone
- `Amount`, `Currency` - Payment details
- `DeviceIp`, `DeviceType` - Device info
- `Status` - PENDING, APPROVED, CANCELLED

## Key Patterns

- Dependency injection for `IDbConnection` (scoped per request)
- Dapper for all SQL operations (no EF Core)
- Controllers use `ILogger<T>` for console logging
- Transactions identified by `IdTransactionPasarela`, `IdOrder`, or `IdTransactionInterbank`
- Request/Response models use `[JsonPropertyName]` to match Interbank's camelCase API
