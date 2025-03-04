# backend/config.py
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/mydb"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
PORT = 8000
DEBUG = True