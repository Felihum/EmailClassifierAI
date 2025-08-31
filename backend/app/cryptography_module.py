from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64

# ======================================================================================
#                               MÓDULO DE CRIPTOGRAFIA
# ======================================================================================


def generate_keys():
    # generate_keys.py
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization


    # Gerar chave privada
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Salvar chave privada
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Salvar chave pública
    with open("public_key.pem", "wb") as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("✅ Chaves RSA geradas: private_key.pem e public_key.pem")


# ------------------ Função de Descriptografia -------------------

def decrypt(password):
    # Carregar chave privada
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

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