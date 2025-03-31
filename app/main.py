from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import logging

from app import views
from app.services.db_async_sqlalchemy import init_db, async_engine
from app.cache import init_cache, close_cache

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI-Powered Feedback Analysis Platform")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include routes from views.py
app.include_router(views.router)

# Global exception handler for HTTPExceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.on_event("startup")
async def startup_event():
    # Initialize the database and create tables if they don't exist
    await init_db()
    # Initialize the cache (using Redis in this example)
    await init_cache("redis://localhost")
    logger.info("Startup complete: Database and cache initialized.")

@app.on_event("shutdown")
async def shutdown_event():
    # Close the cache and dispose of the async engine to properly close all connections
    await close_cache()
    await async_engine.dispose()
    logger.info("Shutdown complete: Cache closed and database engine disposed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
