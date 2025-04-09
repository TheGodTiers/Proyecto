from fastapi.testclient import TestClient
from categorias.main import app

client = TestClient(app)

def test_obtener_categorias():
    response = client.get("/categorias")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for categoria in data:
        assert "categoria" in categoria
        assert "libros" in categoria
        assert isinstance(categoria["libros"], list)
