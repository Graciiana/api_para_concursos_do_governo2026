import bcrypt


def gerar_hash(senha_pura: str)-> str:
    return bcrypt.hashpw(senha_pura.encode(), bcrypt.gensalt()).decode()


def verifica_senha(passe_pura: str, senha_hash: str):
    return bcrypt.checkpw(passe_pura.encode(), senha_hash.encode())


