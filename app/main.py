from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import views
from app.services.db_async_sqlalchemy import init_db, async_engine

app = FastAPI(title="AI-Powered Feedback Analysis Platform")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include routes from views.py
app.include_router(views.router)

@app.on_event("startup")
async def startup_event():
    # Initialize the database and create tables if they don't exist
    await init_db()
    # You can add additional startup logic here

@app.on_event("shutdown")
async def shutdown_event():
    # Dispose of the async engine to properly close all connections
    await async_engine.dispose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
