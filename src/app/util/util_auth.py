import jwt

from config import settings


def gerar_token(email: str) -> str:
    token = jwt.encode(
        {"email": email}, settings.secret.get_secret_value(), algorithm="HS256"
    )
    return token


def verificar_jwt(token) -> None | dict[str, str]:

    try:
        pyload = jwt.decode(
            token, settings.secret.get_secret_value(), algorithms="HS256"
        )
        return pyload
    except Exception:
        return None
