# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Test automation framework for Izipay payment gateway deposits (HU03). Executes deposit operations against the Izipay test API and generates evidence documentation for test cases CP-POS-001 through CP-POS-009.

## Commands

Run all deposit test cases:
```bash
python ejecutar_depositos.py
```

Run with custom merchant credentials:
```bash
python ejecutar_depositos.py --merchant-code CODE --public-key KEY
```

Interactive guided automation (collects payment responses from user):
```bash
python automatizacion_interactiva.py
```

## Dependencies

- Python 3
- curl (for API calls via subprocess)
- pandoc (optional, for Word export)

## Architecture

Two main execution modes:

1. **ejecutar_depositos.py** - Batch executor (`DepositExecutor` class) that:
   - Reads payment response JSON files from `payment_responses/`
   - Generates session tokens via `/security/v1/Token/Generate`
   - Executes deposits via `/capture/v1/Transaction/Deposit`
   - Creates markdown evidence files in `evidencias/`
   - Generates consolidated report `INFORME_CONSOLIDADO_DEPOSITOS.md`
   - Optionally exports to Word via pandoc

2. **automatizacion_interactiva.py** - Interactive wrapper (`AutomatizacionInteractiva` class) that guides users to:
   - Input merchant credentials
   - Generate 9 payments in Izipay checkout demo
   - Paste payment responses which are saved to `payment_responses/Untitled-{1-9}.json`
   - Execute the deposit batch process

## API Integration

- **Test Environment**: `https://testapi-pw.izipay.pe`
- **Checkout Demo**: `https://testcheckout.izipay.pe/demo/`
- **Token Endpoint**: `/security/v1/Token/Generate`
- **Deposit Endpoint**: `/capture/v1/Transaction/Deposit`
- API calls use curl via subprocess

## Test Cases

9 test cases covering different payment methods and channels:

| Case | Pay Method | Currency | Channel |
|------|-----------|----------|---------|
| CP-POS-001 | CARD | PEN | ecommerce |
| CP-POS-002 | CARD | USD | ecommerce |
| CP-POS-003 | YAPE_CODE | PEN | mobile |
| CP-POS-004 | QR | PEN | web |
| CP-POS-005 | APPLE_PAY | USD | mobile |
| CP-POS-006 | PAGO_PUSH | PEN | ecommerce |
| CP-POS-007 | CARD | PEN | moto |
| CP-POS-008 | CARD | PEN | reccurrence |
| CP-POS-009 | CARD | PEN | izivirtual |

## Test Data

Test card for checkout demo:
- Number: 377753000000152 (American Express)
- Expiry: 12/2025
- CVC: 1234

## File Structure

- `payment_responses/Untitled-{1-9}.json` - Input payment response data
- `evidencias/EVIDENCIAS_CP_POS_{001-009}.md` - Per-case evidence files
- `INFORME_CONSOLIDADO_DEPOSITOS.md` - Summary report with traceability matrix
- `word_exports/` - Word document exports (requires pandoc)
