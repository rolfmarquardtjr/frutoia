import hashlib
import secrets

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

def verify_password(stored_password, provided_password, salt):
    return stored_password == hash_password(provided_password, salt)

def generate_session_token():
    return secrets.token_urlsafe(32)

def sanitize_input(input_string):
    # Implementar lógica de sanitização de entrada
    # Por exemplo, remover caracteres especiais, limitar comprimento, etc.
    return input_string[:1000]  # Limita a 1000 caracteres como exemplo