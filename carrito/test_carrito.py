from fastapi.testclient import TestClient
from carrito.main import app
import pytest
from jose import jwt

client = TestClient(app)

SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"

@pytest.fixture
def token():
    payload = {
        "sub": "1", 
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def test_ver_carrito(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/carrito", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "carrito" in data
    assert "precio_final" in data
    assert isinstance(data["carrito"], list)
