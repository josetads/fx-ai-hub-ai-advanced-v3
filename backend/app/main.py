from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db
from app.api.routes import router

app = FastAPI(title=settings.APP_NAME, version="3.0.0", description="FX AI Hub AI Advanced V3")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"app": settings.APP_NAME, "docs": "/docs"}

app.include_router(router, prefix="/api/v1")
