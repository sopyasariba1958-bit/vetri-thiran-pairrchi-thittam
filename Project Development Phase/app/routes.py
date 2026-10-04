from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import traceback

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        full_prompt = (
            f"{prompt}. The main character is {character_name}. "
            f"The setting is {setting}. The tone is {tone}. The art style is {style}."
        )
        
        outline = generate_outline(full_prompt)
        full_story = generate_story(outline)
        images = [generate_image(panel["image_prompt"]) for panel in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)
        
        web_pdf_path = "/" + pdf_path.replace("\\", "/") 
        
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={
            "layout": layout,
            "pdf_path": web_pdf_path
        })
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str):
    return templates.TemplateResponse(request=request, name="export_success.html", context={
        "pdf_path": pdf_path
    })