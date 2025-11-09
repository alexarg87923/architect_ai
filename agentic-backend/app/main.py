from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import agent, auth, projects, admin, simulation, feedback
from app.core.config import settings
from app.core.database import engine, Base
import logging

# RUN APP --> uvicorn app.main:app --reload
# API DOCS --> http://127.0.0.1:8000/docs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Roadmap API",
    description="AI-powered project roadmap generator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - make this more specific for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # From config
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Checking database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified successfully")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(simulation.router, prefix="/api", tags=["simulation"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic Roadmap API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}