from fastapi.testclient import TestClient
from home.main import app

client = TestClient(app)

def test_libros_mas_vendidos():
    response = client.get("/home")
    assert response.status_code == 200
    data = response.json()
    assert "libros_mas_vendidos" in data
    assert isinstance(data["libros_mas_vendidos"], list)
