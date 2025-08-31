from app import create_app
from flask_mail import Mail, Message
import traceback
from flask import jsonify, request
from app.cryptography_module import decrypt
from flask_cors import CORS

# Instancía a aplicação
app = create_app()

# Configurações de CORS -------------------------------------------------------------

origins = [
    "https://email-classifier-frontend-three.vercel.app",
    "http://localhost:3000"
]

CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True,
     allow_headers="*", methods=["GET","POST","OPTIONS"])

# -----------------------------------------------------------------------------------

# --- Carrega a chave de criptografia pública ---
with open("public_key.pem", "rb") as f:
    public_key_pem = f.read().decode("utf-8")
# -----------------------------------------------

# ===========================================================
#  ENDPOINT PARA OBTENÇÂO DA CHAVE PÚBLICA DE CRIPTOGRAFIA
# ===========================================================

@app.route("/public-key", methods=["GET"])
def get_public_key():
    """Retorna a chave pública para o frontend"""
    return jsonify({"publicKey": public_key_pem})

# ===========================================================



# =======================================================================================
#                              ENDPOINT PARA ENVIO DE EMAIL
# =======================================================================================

@app.route("/submit", methods=["POST"])
def send_email():
    # Verificando se os dados foram enviados no formato JSON ----------------------------
    if not request.is_json:
        return jsonify({"error": "Formato inválido. É necessário enviar um JSON."}), 400
    # -----------------------------------------------------------------------------------

    data = request.get_json()  # Obtendo os dados da requisição JSON

    # --- Extrai os dados do corpo da requisição ---
    recipient = data.get("recipient")
    sender = data.get("sender")
    password = decrypt(data.get("password"))
    message = data.get("message")
    # ----------------------------------------------

    # --- Configura o app para que cada usuário tenha configurações diferentes ---
    app.config['MAIL_USERNAME'] = sender
    app.config['MAIL_PASSWORD'] = password
    # ----------------------------------------------------------------------------

    mail = Mail(app)

    # Valida se o "recipient" não foi informado ------------------------------
    if not recipient:
        return jsonify({"error": "O campo 'recipient' é obrigatório."}), 400
    # ------------------------------------------------------------------------

    # Define o valor padrão para "subject" ---------------------
    subject = data.get("subject", "Resposta ao seu comunicado")
    # ----------------------------------------------------------

    # Configurando o email ---------------------------------------
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = message
    # ------------------------------------------------------------

    try:

        # Tenta enviar o email ----------------------------------------------------------------------------
        mail.send(msg)
        return jsonify({
            "message": "Caso o email exista, o link de recuperação será enviado para o e-mail informado."
        }), 200
        # -------------------------------------------------------------------------------------------------

    except Exception as e:
        traceback.print_exc()

        # Retornando erro genérico sem expor detalhes sensíveis -------------------------------------------------
        return jsonify({"error": "Ocorreu um erro ao tentar enviar o e-mail. Tente novamente mais tarde."}), 500
        # -------------------------------------------------------------------------------------------------------

# =======================================================================================


# ---------- Roda a aplicação ------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# ----------------------------------------------------