from cryptography.fernet import Fernet

# Твой сгенерированный ключ шифрования
KEY = b'iC6leMkQy7kSh9KPpPLlEOpYc9Ig_TW6HzMyJmTLR4I='

fernet = Fernet(KEY)

def encrypt_password(password: str) -> str:
    """Шифрует пароль."""
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    """Расшифровывает пароль."""
    return fernet.decrypt(token.encode()).decode()
