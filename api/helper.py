def get_instrument_code(crypto: str, fiat: str):
    return f'{crypto.upper()}_{fiat.upper()}'