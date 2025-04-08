import logging
import io
import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from schemas.feedback import FeedbackCreate, FeedbackResponse
from services.cognitive import analyze_feedback
from services.db_async_sqlalchemy import init_db, save_feedback, get_all_feedbacks
from services.storage import upload_file_to_blob
import uvicorn

logger = logging.getLogger(__name__)
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    with open("templates/dashboard.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/feedbacks", response_class=JSONResponse)
async def api_get_all_feedbacks():
    feedbacks = await get_all_feedbacks()
    # Convert ORM objects to dicts; in a real app, use a serializer or Pydantic conversion.
    result = []
    for fb in feedbacks:
        result.append({
            "id": fb.id,
            "name": fb.name,
            "email": fb.email,
            "feedback_text": fb.feedback_text,
            "sentiment": fb.sentiment,
            "confidence_scores": fb.confidence_scores,
            "key_phrases": fb.key_phrases,
            "attachment_url": fb.attachment_url,
            "created_at": fb.created_at.isoformat() if fb.created_at else None
        })
    return JSONResponse(content=result)

@app.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(
    name: str = Form(...),
    email: str = Form(...),
    feedback_text: str = Form(...),
    attachment: UploadFile = File(None)
):
    try:
        cognitive_results = analyze_feedback(feedback_text)
    except Exception as e:
        logger.error(f"Cognitive analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Cognitive analysis error.")

    attachment_url = None
    if attachment:
        content = await attachment.read()
        attachment_url = upload_file_to_blob(io.BytesIO(content), attachment.filename)

    feedback_data = {
        "name": name,
        "email": email,
        "feedback_text": feedback_text,
        "sentiment": cognitive_results.get("sentiment"),
        "confidence_scores": str(cognitive_results.get("confidence_scores")),
        "key_phrases": ", ".join(cognitive_results.get("key_phrases")),
        "attachment_url": attachment_url,
        "created_at": datetime.datetime.utcnow()
    }
    try:
        feedback_id = await save_feedback(feedback_data)
        feedback_data["id"] = feedback_id
        feedback_data["created_at"] = feedback_data["created_at"].isoformat()
        return feedback_data
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        raise HTTPException(status_code=500, detail="Error saving feedback.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
