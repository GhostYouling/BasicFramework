# backend/main.py
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user import router as user_router
from api.candidate import router as candidate_router
from config import PORT

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(candidate_router, prefix="/api", tags=["candidates"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

@app.get("/")
async def root():
    return {"message": "Welcome to BasicFramework API"}
