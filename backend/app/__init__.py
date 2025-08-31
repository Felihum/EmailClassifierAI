from flask import Flask
import os

# ---------------- Criação da Instância da Aplicação --------------
def create_app():
    app = Flask(__name__)

    # Configurações de variáveis do serviço de envio de email -----

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    # -------------------------------------------------------------

    # Registro dos endpoints --------------------------------------

    from .routes import bp_email
    app.register_blueprint(bp_email)

    # -------------------------------------------------------------

    return app

# -----------------------------------------------------------------
