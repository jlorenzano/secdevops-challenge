from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from app.config import MAX_UPLOAD_SIZE
from app.services.virustotal import scan_with_virustotal
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(template_path, "r") as f:
        return f.read()

@router.post("/scan-file/")
async def scan_file_json(file: UploadFile = File(...)):
    file.file.seek(0, 2)
    if file.file.tell() > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande")
    file.file.seek(0)
    return await scan_with_virustotal(file, return_html=False)

@router.post("/upload/")
async def scan_file_html(file: UploadFile = File(...)):
    file.file.seek(0, 2)
    if file.file.tell() > MAX_UPLOAD_SIZE:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(BASE_DIR, "templates", "size.html")
        with open(template_path, "r") as f:
            return HTMLResponse(content=f.read(), status_code=413)
    file.file.seek(0)
    html_result = await scan_with_virustotal(file, return_html=True)
    return HTMLResponse(content=html_result)