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
        "merchant_code": "4078370",  # Mismo que QA (ajustar si es diferente)
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",  # Mismo que QA (ajustar si es diferente)
        "bins_disponibles": [
            # BINs reales extraídos de la base de datos (2025-11-04)
            # Total de 263 BINs disponibles en DB
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
        "descripcion": "Ambiente de desarrollo - Pruebas tempranas e integración continua",
        "timeout": 30,
        "retry_count": 2,
        "transaction_prefix": "DEV"
    },

    "SANDBOX": {
        "name": "Sandbox",
        "token_url": "https://sandbox-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://sandbox-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "merchant_code": "4001834",  # Merchant Code de sandbox - ACTUALIZADO
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",  # Public Key de sandbox - ACTUALIZADO
        "bins_disponibles": [
            # BINs reales extraídos de la base de datos SANDBOX (2025-11-04)
            # Total de 261 BINs disponibles en DB SANDBOX
            "545545",  # SCOTIABANK MC - 36 cuotas, 0 meses diferido
            "400917",  # SCOTIABANK VISA - 36 cuotas, 0 meses diferido
            "510308",  # SCOTIABANK MC - 36 cuotas, 0 meses diferido
            "377750",  # AMEX INTERBANK - 36 cuotas, 3 meses diferido
            "553650",  # BBVA MC Black - 36 cuotas, 0 meses diferido
            "511578",  # BBVA MC Platinum - 36 cuotas, 0 meses diferido
            "512312",  # BBVA MC CLASICA - 36 cuotas, 0 meses diferido
            "362426",  # DINERS CLUB - 36 cuotas, 3 meses diferido
            "602008",  # WieseCash - 12 cuotas, 1 mes diferido
            "527556",  # Banco Financiero - 3 cuotas, 0 meses diferido
        ],
        "descripcion": "Ambiente sandbox - Pruebas de integración externas",
        "timeout": 30,
        "retry_count": 2,
        "transaction_prefix": "SBX"
    },

    "QA": {
        "name": "Quality Assurance",
        "token_url": "https://qa-api-pw.izipay.pe/security/v1/Token/Generate",
        "installments_url": "https://qa-api-pw.izipay.pe/Installments/v1/Installments/Search",
        "merchant_code": "4078370",
        "public_key": "VErethUtraQuxas57wuMuquprADrAHAb",
        "bins_disponibles": [
            # BINs reales extraídos de la base de datos (2025-11-04)
            # Total de 263 BINs disponibles en DB
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
        "descripcion": "Ambiente de QA - Pruebas de calidad",
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


def print_environment_info(env_name=None):
    """
    Imprime información de uno o todos los ambientes

    Args:
        env_name (str, optional): Nombre del ambiente específico
    """
    if env_name:
        env = get_environment(env_name)
        print(f"\n{'='*60}")
        print(f"AMBIENTE: {env['name']} ({env_name})")
        print(f"{'='*60}")
        print(f"Descripción: {env['descripcion']}")
        print(f"Token URL: {env['token_url']}")
        print(f"Installments URL: {env['installments_url']}")
        print(f"Merchant Code: {env['merchant_code']}")
        print(f"Public Key: {env['public_key'][:30]}...")
        print(f"BINs disponibles: {', '.join(env['bins_disponibles'])}")
        print(f"Timeout: {env['timeout']}s")
        print(f"Reintentos: {env['retry_count']}")
        print(f"Prefijo TransactionId: {env['transaction_prefix']}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("AMBIENTES DISPONIBLES")
        print(f"{'='*60}")
        for env_name in ENVIRONMENTS:
            env = ENVIRONMENTS[env_name]
            print(f"\n{env_name}:")
            print(f"  Nombre: {env['name']}")
            print(f"  URL Base: {env['token_url'].split('/security')[0]}")
            print(f"  Merchant: {env['merchant_code']}")
            print(f"  BINs: {len(env['bins_disponibles'])} configurados")


if __name__ == "__main__":
    # Ejemplo de uso
    import sys

    if len(sys.argv) > 1:
        env_name = sys.argv[1]
        print_environment_info(env_name)
    else:
        print_environment_info()
