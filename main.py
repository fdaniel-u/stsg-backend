from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.projects_routes import router as projects_router
from routes.content_routes import router as content_router
from init_db import init_database

app = FastAPI(title="STSG Calidad Total API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "https://*.replit.dev", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(content_router)


@app.on_event("startup")
async def startup_event():
    init_database()


@app.get("/")
def root():
    return {"message": "STSG API funcionando", "version": "1.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
