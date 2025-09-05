import os

class Config:
    # Ajuste seu usuário e senha do PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:qweqwe@localhost:5432/registro_ponto"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("CHAVESEGURA", "chave_secreta_temporaria")
