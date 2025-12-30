"""
Configuración de ambientes para pruebas de APIs Izipay
Soporta: DEV, SANDBOX, QA

Uso:
    from config_environments import get_environment

    config = get_environment("DEV")  # o "SANDBOX" o "QA"
    print(config["token_url"])
"""

ENVIRONMENTS = {
    "DEV": {
        "name": "Desarrollo",
        "token_url": "https://testapi-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://testapi-pw.izipay.pe/Installments/v1/Installments/Search",
        "merchant_code": "4078370",
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",
        "bins_disponibles": [
            "545545",  # SCOTIABANK - 12 cuotas, 3 meses diferido
            "400917",  # SCOTIABANK VISA - 36 cuotas, 0 meses diferido
            "510308",  # SCOTIABANK MC - 0 cuotas, 0 meses diferido
            "377893",  # BCP - 36 cuotas, 3 meses diferido
            "377755",  # AMEX INTERBANK - 36 cuotas, 3 meses diferido
            "553650",  # BBVA MC Platinum - 36 cuotas, 3 meses diferido
            "511578",  # BBVV - 36 cuotas, 0 meses diferido
            "362333",  # Diners - 36 cuotas, 3 meses diferido
            "602008",  # WieseCash - 12 cuotas, 3 meses diferido
            "456781",  # Banco Financiero - 7 cuotas, 3 meses diferido
        ],
        "descripcion": "Ambiente de desarrollo",
        "timeout": 30,
        "retry_count": 2,
        "transaction_prefix": "DEV"
    },

    "SANDBOX": {
        "name": "Sandbox",
        "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "merchant_code": "4001834",
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",
        "bins_disponibles": [
            # 🚨 IMPORTANTE: Solo estos BINs están VALIDADOS para merchant 4001834
            # Base de datos tiene 24,681 BINs pero solo estos 2 están configurados para este merchant
            "545545",  # SCOTIABANK MC - 36 cuotas, 0 meses diferido ✅ VALIDADO
            "553650",  # BBVA MC Black - 36 cuotas, 0 meses diferido ✅ VALIDADO

            # ⚠️ ESTOS BINES EXISTEN EN DB PERO NO ESTÁN CONFIGURADOS PARA MERCHANT 4001834:
            # "400917",  # SCOTIABANK VISA - Error 500 - NO configurado
            # "510308",  # SCOTIABANK MC - Error 500 - NO configurado
            # "377750",  # AMEX INTERBANK - Error TN - NO configurado
            # "511578",  # BBVA MC Platinum - Error TN - NO configurado
            # "512312",  # BBVA MC CLASICA - No probado
            # "362426",  # DINERS CLUB - No probado
            # "602008",  # WieseCash - No probado
            # "527556",  # Banco Financiero - No probado
        ],
        "descripcion": "Ambiente sandbox - Solo 2 BINs validados de 24,681 en DB (actualizado 2025-11-06)",
        "timeout": 60,  # Aumentado por timeouts frecuentes en SANDBOX
        "retry_count": 2,
        "transaction_prefix": "SBX",
        "notas_importantes": [
            "SANDBOX tiene 24,681 BINs en base de datos (ver ResultsSandBoxBin.xlsx)",
            "Solo 2 BINs validados para merchant 4001834: 545545, 553650",
            "Otros BINs existen pero NO están configurados para este merchant",
            "Para más BINs, solicitar configuración a Izipay",
            "BIN 545545 retorna 36 cuotas (vs 12 en DEV/QA)"
        ]
    },

    "QA": {
        "name": "Quality Assurance",
        "token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "merchant_code": "4078370",
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",
        "bins_disponibles": [
            "545545",  # SCOTIABANK - 12 cuotas, 3 meses diferido
            "400917",  # SCOTIABANK VISA - 36 cuotas, 0 meses diferido
            "510308",  # SCOTIABANK MC - 0 cuotas, 0 meses diferido
            "377893",  # BCP - 36 cuotas, 3 meses diferido
            "377755",  # AMEX INTERBANK - 36 cuotas, 3 meses diferido
            "553650",  # BBVA MC Platinum - 36 cuotas, 3 meses diferido
            "511578",  # BBVV - 36 cuotas, 0 meses diferido
            "362333",  # Diners - 36 cuotas, 3 meses diferido
            "602008",  # WieseCash - 12 cuotas, 3 meses diferido
            "456781",  # Banco Financiero - 7 cuotas, 3 meses diferido
        ],
        "descripcion": "Ambiente de QA",
        "timeout": 30,
        "retry_count": 2,
        "transaction_prefix": "QA"
    }
}


def get_environment(env_name):
    """
    Obtiene la configuración de un ambiente específico

    Args:
        env_name (str): Nombre del ambiente ("DEV", "SANDBOX", "QA")

    Returns:
        dict: Configuración del ambiente

    Raises:
        ValueError: Si el ambiente no existe
    """
    env_name = env_name.upper()

    if env_name not in ENVIRONMENTS:
        available = ", ".join(ENVIRONMENTS.keys())
        raise ValueError(f"Ambiente '{env_name}' no encontrado. Disponibles: {available}")

    return ENVIRONMENTS[env_name]


def list_environments():
    """
    Lista todos los ambientes disponibles

    Returns:
        list: Lista de nombres de ambientes
    """
    return list(ENVIRONMENTS.keys())
