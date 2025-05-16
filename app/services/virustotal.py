import httpx, time, asyncio
from fastapi import HTTPException
from app.config import VT_API_KEY, MAX_WAIT_SECONDS, VT_BASE_URL
from app.utils import build_summary, generate_html_from_analysis

HTTP_TIMEOUT = httpx.Timeout(300.0, connect=30.0)

async def scan_with_virustotal(file, return_html=False):
    headers = {"x-apikey": VT_API_KEY}
    if not VT_API_KEY:
        raise RuntimeError("La variable VT_API_KEY no está definida")

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        files = {"file": (file.filename, file.file, file.content_type)}

        upload_resp = await client.post(f"{VT_BASE_URL}/files", headers=headers, files=files)
        upload_resp.raise_for_status()
        upload_result = upload_resp.json()
        analysis_id = upload_result.get("data", {}).get("id")

        if not analysis_id:
            raise HTTPException(status_code=500, detail="No se obtuvo el ID de análisis")

        start_time = time.time()

        while True:
            analysis_resp = await client.get(f"{VT_BASE_URL}/analyses/{analysis_id}", headers=headers)
            analysis_resp.raise_for_status()
            analysis_result = analysis_resp.json()

            if analysis_result["data"]["attributes"]["status"] == "completed":
                if return_html:
                    return generate_html_from_analysis(analysis_result, file.filename)
                else:
                    analysis_result["summary"] = build_summary(analysis_result)
                    return analysis_result

            if time.time() - start_time > MAX_WAIT_SECONDS:
                return {
                    "status": "in_progress",
                    "message": f"Análisis en progreso después de {MAX_WAIT_SECONDS} segundos.",
                    "analysis_id": analysis_id,
                    "link_virustotal": f"https://www.virustotal.com/gui/file/{analysis_id}/detection",
                }

            await asyncio.sleep(3)
