from pydantic import BaseModel

# ----------------- Modelo de Resposta da IA -------------------

class AIAnswerModel(BaseModel):
    classification: str
    suggestion: str

# --------------------------------------------------------------