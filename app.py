from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r") as f:
        return f.read()
    
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_location, "wb") as f: 
            f.write(await file.read())
        
        return {"message": f"Archivo '{file.filename}' subido exitosamente"}
    
    except Exception as e:
        return {"error": f"Hubo un error al subir el archivo: {str(e)}"}

#@app.post("/")
