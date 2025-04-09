from fastapi.testclient import TestClient
from pedido.main import app
import pytest
from jose import jwt

client = TestClient(app)

SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"

@pytest.fixture
def admin_token():
    payload = {
        "username": "admin_user",
        "rol": "admin"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def test_listar_pedidos(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/pedidos", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data: 
        assert "pedido_id" in data[0]
        assert "usuario_id" in data[0]
        assert "fecha" in data[0]
        assert "total" in data[0]
        assert "detalles" in data[0]
