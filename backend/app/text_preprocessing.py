import re
from dotenv import load_dotenv

load_dotenv()

# ======================================================================================
#                        MÓDULO DE PRÉ-PROCESSAMENTO DE EMAILS
# ======================================================================================

class EmailPreprocessor:

    def __init__(self):
        pass

    # ------------ Função de Limpeza do email ------------------------------------
    def clean_text(self, text: str, type: str) -> tuple[str, str]:
        # Ordem de processamento:

        # 1. Remover URLs e endereços de email
        text = self._remove_urls_emails(text)

        # 2. Remover cabecalhos de email
        [sender, text] = self._remove_headers_refined(text, type)

        # 3. Remover assinaturas
        text = self._remove_signatures_refined(text)

        # 4. Converter para minúsculas
        text = self._to_lowercase(text)

        # 5. Remover espaços extras
        text = self._remove_extra_whitespace(text)

        return sender, text
    # ----------------------------------------------------------------------------

    # --- EXTRAI CADA EMAIL DO CONJUNTO ------------------------------------------

    def extract_emails_from_set(self, text: str, file_type: str) -> [str]:
        emails: [str] = []

        # No caso de ser um arquivo txt
        if file_type == "txt":
            emails = text.split("\r\n\r\n")

        # No caso de ser um arquivo pdf
        elif file_type == "pdf":

            emails = text.split("\n \n \n")

            for i in range(len(emails)):
                emails[i] = emails[i].replace("\n \n", " ")

        # No caso de ser um texto digitado no textarea
        elif file_type == "default":
            emails = text.split("\n\n")

        print(f"Email: {emails}")
        return emails
    # ----------------------------------------------------------------------------

    # Função de remoção de cabeçalhos do email -----------------------------------
    def _remove_headers_refined(self, email: str, type: str) -> tuple[str, str]:

        # Extrai o remetente e a mensagem da string de email
        sender = ""
        message = ""
        # ---------------------------------------------------


        # No caso de ser arquivo TXT ou digitado no textarea
        if type == "txt" or type == "default":
            for line in email.splitlines():
                if line.startswith("De:"):
                    sender = line.replace("De:", "").strip()
                elif line.startswith("From:"):
                    sender = line.replace("From:", "").strip()
                elif line.startswith("Mensagem:"):
                    message = line.split("Mensagem:", 1)[1].strip()
                elif line.startswith("Message:"):
                    message = line.split("Message:", 1)[1].strip()

        # No caso de ser arquivo PDF
        elif type == "pdf":
            sender = email.split("De:")[1].split("Assunto:")[0].strip()

            message = email.split("Mensagem:")[1].strip()

        return sender, message
    # --------------------------------------------------------------------------------

    # Função de remoção de assinaturas comuns e avisos legais do final do email ------
    def _remove_signatures_refined(self, email_text: str) -> str:
        if not isinstance(email_text, str):
            return ""

        patterns = [
            r'-----Original Message-----', r'From:.*', r'Sent:.*', r'To:.*',
            r'Subject:.*', r'[\s]*_{3,}[\s]*', r'[\s]*-{3,}[\s]*',
            r'Assunto:.*',
            r'Regards,', r'Sincerely,', r'Thank you,', r'V/R,',
            r'Atenciosamente,', r'Obrigado,', r'Abraços,', r'Att,',
            r'Best regards,', r'Sent from my BlackBerry', r'Confidentiality Notice:',
            r'This email and any files transmitted with it are confidential',
            r'This message is intended only for the use of the individual or entity to which it is addressed and may contain information that is confidential and privileged.'
        ]

        # Percorre os padrões de assinatura, removendo do final do texto
        for pattern in patterns:
            match = re.search(pattern, email_text, re.IGNORECASE | re.DOTALL)
            if match:
                email_text = email_text[:match.start()].strip()
                break

        # ---------------------------------------------------------------------------

        return email_text
    # --------------------------------------------------------------------------------

    # ----------- Função de remoção de URLs do email ---------------------------------
    def _remove_urls_emails(self, text: str) -> str:

        if not isinstance(text, str):
            return ""
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        return text

    # ----------- Função para deixar o email em lowercase ---------------------------
    def _to_lowercase(self, text: str) -> str:

        if not isinstance(text, str):
            return ""
        return text.lower()

    # -------------------------------------------------------------------------------

    # ----------- Função de remoção de espaços em branco do email -------------------
    def _remove_extra_whitespace(self, text: str) -> str:

        if not isinstance(text, str):
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # -------------------------------------------------------------------------------