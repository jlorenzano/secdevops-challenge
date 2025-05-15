from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from config import VT_API_KEY, MAX_UPLOAD_SIZE, MAX_WAIT_SECONDS, VT_BASE_URL
from utils import build_summary, generate_html_from_analysis

import httpx
import os
import uvicorn
import asyncio
import time

app = FastAPI()


HTTP_TIMEOUT = httpx.Timeout(300.0, connect=30.0)

if not VT_API_KEY:
    raise RuntimeError("La variable VT_API_KEY no está definida")

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r") as f:
        return f.read()
    

@app.post("/scan-file/")
async def upload_file(file: UploadFile = File(...)):
    file.file.seek(0,2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_UPLOAD_SIZE:    
        raise HTTPException(
            status_code=413,
            detail="El archivo excede el tamaño máximo permitido de {MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
        )
        
    headers = {"x-apikey": VT_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            files = {"file": (file.filename, file.file, file.content_type)}

            upload_resp = await client.post(
                f"{VT_BASE_URL}/files",
                headers=headers,
                files=files,
            )

            upload_resp.raise_for_status()
            upload_result = upload_resp.json()

            analysis_id = upload_result.get("data", {}).get("id")

            if not analysis_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"No se obtuvo el ID de análisis. Respuesta: {upload_result}"
                )

            start_time = time.time()

            while True:
                analysis_resp = await client.get(
                    f"{VT_BASE_URL}/analyses/{analysis_id}",
                    headers=headers,
                )

                analysis_resp.raise_for_status()
                analysis_result = analysis_resp.json()

                status = analysis_result.get("data", {}).get("attributes", {}).get("status")

                if status == "completed":
                    summary = build_summary(analysis_result)
                    analysis_result["summary"] = summary
                    return analysis_result

                if time.time() - start_time > MAX_WAIT_SECONDS:
                    return {
                        "status": status,
                        "message": f"Análisis en progreso después de {MAX_WAIT_SECONDS} segundos.",
                        "analysis_id": analysis_id,
                        "link_virustotal": f"https://www.virustotal.com/gui/file/{analysis_id}/detection",
                    }

                await asyncio.sleep(3)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout al subir el archivo o esperar respuesta.")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    
    except Exception as e:
        print("Error de HTTP:", e.response.text)
        raise HTTPException(status_code=500, detail="Exception - " + str(e))


@app.post("/upload/")
async def scan_file(file: UploadFile = File(...)):
    file.file.seek(0, 2) 
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_UPLOAD_SIZE:
        with open("templates/size.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(
            content=html_content,
            status_code=413
        )

    headers = {"x-apikey": VT_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            files = {"file": (file.filename, file.file, file.content_type)}

            print("Archivo recibido, subiendo a VirusTotal...")

            upload_resp = await client.post(
                f"{VT_BASE_URL}/files",
                headers=headers,
                files=files,
            )

            upload_resp.raise_for_status()
            upload_result = upload_resp.json()

            analysis_id = upload_result.get("data", {}).get("id")

            if not analysis_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"No se obtuvo el ID de análisis. Respuesta: {upload_result}"
                )

            start_time = time.time()

            while True:
                analysis_resp = await client.get(
                    f"{VT_BASE_URL}/analyses/{analysis_id}",
                    headers=headers,
                )

                analysis_resp.raise_for_status()
                analysis_result = analysis_resp.json()

                status = analysis_result.get("data", {}).get("attributes", {}).get("status")

                if status == "completed":
                    html_content = generate_html_from_analysis(analysis_result, file.filename)
                    return HTMLResponse(content=html_content, status_code=200)

                if time.time() - start_time > MAX_WAIT_SECONDS:
                    return {
                        "status": status,
                        "message": f"Análisis en progreso después de {MAX_WAIT_SECONDS} segundos.",
                        "analysis_id": analysis_id,
                        "link_virustotal": f"https://www.virustotal.com/gui/file/{analysis_id}/detection",
                    }

                await asyncio.sleep(3)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout al subir el archivo o esperar respuesta.")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    
    except Exception as e:
        print("Error de HTTP:", e.response.text)
        raise HTTPException(status_code=500, detail="Exception - " + str(e))

