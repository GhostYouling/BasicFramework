# backend/main.py
from fastapi import FastAPI
from .api.user import router as user_router
from config import PORT

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)