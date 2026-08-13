import bcrypt


def gerar_hash(senha_pura: str)-> str:
    return bcrypt.hashpw(senha_pura.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha_pura:str, senha_hash:str)-> str:
    return bcrypt.checkpw(senha_pura.encode(), senha_hash.encode())

