from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64

# ======================================================================================
#                               MÓDULO DE CRIPTOGRAFIA
# ======================================================================================


# Carregar chave privada
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# ------------------ Função de Descriptografia -------------------

def decrypt(password):
    """Recebe mensagem criptografada e retorna descriptografada"""
    ciphertext_b64 = password

    ciphertext = base64.b64decode(ciphertext_b64)
    decrypted = private_key.decrypt(
        ciphertext,
        padding.PKCS1v15()
    )
    decrypted_text = decrypted.decode("utf-8")
    print(f"This is the password: {decrypted_text}")
    return decrypted_text

# ----------------------------------------------------------------