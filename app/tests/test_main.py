import pytest
import sys
import os

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers["content-type"]

def test_scan_file_too_large(monkeypatch):
    # Simulacion un archivo mayor al límite
    class DummyFile:
        def seek(self, offset, whence=0): pass
        def tell(self): return 40 * 1024 * 1024  # 40MB
        def read(self): return b"x" * 10

    dummy_upload = {
        "file": ("dummy.exe", DummyFile(), "application/octet-stream")
    }

    response = client.post("/scan-file/", files=dummy_upload)
    assert response.status_code == 413

def test_env_variable_missing(monkeypatch):
    monkeypatch.setenv("VT_API_KEY", "")
    with pytest.raises(RuntimeError):
        from app.main import VT_API_KEY
        if not VT_API_KEY:
            raise RuntimeError("La variable VT_API_KEY no está definida")
        
