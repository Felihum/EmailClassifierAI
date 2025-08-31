import json
from flask import Blueprint, jsonify, request
import google.generativeai as genai
import PyPDF2
from werkzeug.datastructures import FileStorage
from app.text_preprocessing import EmailPreprocessor
from app.email import Email
from app.ai_answer_model import AIAnswerModel
import os

bp_email = Blueprint("main", __name__, url_prefix="/email")

# ------------- Configurações do modelo de IA --------------

genai.configure(api_key=os.getenv('GENAI_KEY'))

generation_config = genai.GenerationConfig(
    response_mime_type="application/json",
    response_schema=list[AIAnswerModel]
)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config=generation_config
)

# ----------------------------------------------------------

text_preprocessor = EmailPreprocessor()

# =================================================================
#          ENDPOINT DE CLASSIFICAÇÂO DE EMAIL POR TEXTO
# =================================================================

@bp_email.route("/", methods=["POST"])
def classify_text_email():

    email_set: str = request.get_json()["email"]
    file_type = "default"

    # Pré-processa o conjunto de emails
    cleaned_emails = _clean_emails(email_set, file_type)

    # IA classifica os emails pré-processados
    ai_answer: str = _classify_emails(cleaned_emails)

    # Extrai o conteúdo JSON da string retornada pela IA
    ai_answer_json = json.loads(ai_answer)

    # Extrai os dados do JSON
    classifications, suggestions = _organize_ai_response(ai_answer_json)

    cleaned_emails_dicts = [{"sender": e.sender, "message": e.message, "classification": c, "suggestion": s} for e, c, s
                            in zip(cleaned_emails, classifications, suggestions)]

    return jsonify({"emails": cleaned_emails_dicts}), 200

# =================================================================


# =================================================================
#        ENDPOINT DE CLASSIFICAÇÂO DE EMAIL POR ARQUIVO
# =================================================================

@bp_email.route("/upload", methods=["POST"])
def update_file():

    # Verifica se foi enviado algum arquivo
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    # Extrai o conteúdo do arquivo enviado
    email_set, file_type = _extract_content_from_file(file)

    # Pré-processa o conjunto de emails
    cleaned_emails = _clean_emails(email_set, file_type)

    # IA classifica os emails pré-processados
    ai_answer: str = _classify_emails(cleaned_emails)

    # Extrai o conteúdo JSON da string retornada pela IA
    ai_answer_json = json.loads(ai_answer)

    # Extrai os dados do JSON
    classifications, suggestions = _organize_ai_response(ai_answer_json)

    cleaned_emails_dicts = [{"sender": e.sender, "message": e.message, "classification": c, "suggestion": s} for e, c, s
                            in zip(cleaned_emails, classifications, suggestions)]

    return jsonify({"emails": cleaned_emails_dicts}), 200

# =================================================================


# ---------------------- Funções Privadas --------------------------

def _classify_emails(emails: [Email]):

    # ------------------- Monta a estrutura de prompt dos emails -------------------------

    emails_prepared_for_ai : str = ""
    for email in emails:
        emails_prepared_for_ai += f"\nEmails a serem analisados: {email.message}"

    # ------------------------------------------------------------------------------------

    # Gera a resposta do modelo de IA
    classification_response_json = model.generate_content(
        'Tendo em mente as seguintes classificações possíveis: - Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema). - Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos). Irei lhe mandar alguns emails e você deve classificá-los apenas entre essas duas possibilidades. Além de classificá-los, você deve dar uma sugestão de resposta ao email. Tenha em mente que você não pode ter relações pessoais com ninguém, afinal você responde em nome de uma empresa. Os emails são os seguintes: ' + emails_prepared_for_ai
    )

    return classification_response_json.text

def _extract_content_from_file(file: FileStorage):
    content: str = ""

    # ---------------Extrai conteúdo do arquivo -------------------------------

    if file.filename == '':
        return jsonify({"error": "Arquivo sem nome"}), 400

    # No caso de ser um arquivo txt
    if file.filename.endswith('.txt'):
        file_type = "txt"
        content = file.read().decode("utf-8")
        return content, file_type

    # No caso de ser um arquivo pdf
    elif file.filename.endswith('.pdf'):
        file_type = "pdf"
        try:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() or ""

            return content, file_type
        except Exception as e:
            return jsonify({"error": f"Erro ao ler PDF: {str(e)}"}), 500

    else:
        return jsonify({"error": "Formato inválido. Envie .txt ou .pdf"}), 400

def _clean_emails(email_set: str, file_type: str):

    # Extrai os emails do conjunto
    emails: [str] = text_preprocessor.extract_emails_from_set(email_set.strip(), file_type)
    cleaned_emails: [Email] = list()

    for email in emails:
        # Extrai os dados do Remetente e da Mensagem de cada email
        sender, message = text_preprocessor.clean_text(email, file_type)

        cleaned_emails.append(Email(sender, message))

    return cleaned_emails

def _organize_ai_response(ai_answer_json):
    classifications = []
    suggestions = []

    if isinstance(ai_answer_json, list):

        # Extrai os dados de Classificação e da Sugestão de Resposta de cada email
        for item in ai_answer_json:
            classifications.append(item.get("classification"))
            suggestions.append(item.get("suggestion"))

    return classifications, suggestions

# ------------------------------------------------------------------
