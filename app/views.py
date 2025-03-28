from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import io

from app.services import cognitive, storage, db
from app.models.feedback import Feedback

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Render the user feedback form."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/submit", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    feedback_text: str = Form(...),
    attachment: UploadFile = File(None)
):
    """Handle user feedback submission."""
    # Analyze the feedback text using Azure Cognitive Services
    analysis = cognitive.analyze_feedback(feedback_text)

    # If a file was uploaded, read it and store it in Blob Storage
    attachment_url = None
    if attachment:
        file_bytes = await attachment.read()
        file_stream = io.BytesIO(file_bytes)
        attachment_url = storage.upload_file_to_blob(file_stream, attachment.filename)

    # Create a feedback record
    feedback_record = Feedback(
        name=name,
        email=email,
        feedback_text=feedback_text,
        sentiment=analysis["sentiment"],
        confidence_scores=str(analysis["confidence_scores"]),
        key_phrases=", ".join(analysis["key_phrases"]),
        attachment_url=attachment_url,
        created_at=datetime.utcnow()
    )

    # Save the feedback to the database
    db.save_feedback(feedback_record)

    # Redirect back to the form with a success message
    response = RedirectResponse(url="/", status_code=302)
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render admin dashboard with analytics."""
    # Fetch feedback entries (this is a simple example; you might want to add pagination, filtering, etc.)
    feedbacks = db.get_all_feedbacks()
    # For a real chart, you might pass JSON data to be used with Chart.js on the frontend.
    return templates.TemplateResponse("dashboard.html", {"request": request, "feedbacks": feedbacks})
