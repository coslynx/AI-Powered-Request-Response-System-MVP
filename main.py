from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import process, auth  # Import API routers
from .database import Base, engine  # Import database setup
from .config import settings  # Import configuration settings

app = FastAPI()

# Set up CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Allowed origins from .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
Base.metadata.create_all(bind=engine)

# Register API routers (process and auth)
app.include_router(process.router, prefix="/process", tags=["process"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    # Load environment variables from .env
    # This should already be handled in config.py
    # load_dotenv()
    # ... additional startup tasks ...

@app.on_event("shutdown")
async def shutdown_event():
    # ... shutdown tasks ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,  # Host from .env or default
        port=settings.PORT,  # Port from .env or default
        reload=settings.DEBUG,  # Reload on code changes if DEBUG is True
    )