# backend/config.py
DATABASE_URL = "postgresql+asyncpg://postgres:ZAQ!xsw2cde3@localhost:5432/mydb"
SECRET_KEY = "51331b12719e4c9308b7c23b1684e175227199d775ad4f87bd84c842075825a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
PORT = 8000
DEBUG = True