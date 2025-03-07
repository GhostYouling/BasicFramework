# backend/main.py
from fastapi import APIRouter, FastAPI
from .api.user import router as user_router
from backend.config import PORT

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)



@app.get("/")
async def lunch_app():
    return "Welcome to here!"
