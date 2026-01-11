# app/main.py

from fastapi import FastAPI
from app.db.session import init_db
from app.api.v1.endpoints import router as api_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khoi tao co so du lieu khi ung dung bat dau
    init_db()
    yield
    print('Hệ thống: Đang dừng ứng dụng...')

app = FastAPI(
    title='Agentic Molecule Discovery Platform',
    description="Hệ thống thiết kế phân tử tự động dựa trên AI và RDKit.",
    version="1.0.0",
    lifespan=lifespan
)

# Dang ky cac Endpoint API
app.include_router(api_router, prefix='/api/v1', tags=['Molecule Runs'])

@app.get('/')
def root():
    return {"message": "Chào mừng bạn đến với AI Molecule Discovery Platform. Hãy truy cập /docs để xem tài liệu API."}