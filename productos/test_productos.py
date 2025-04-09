from fastapi.testclient import TestClient
from productos.main import app
import pytest
from productos.main import admin_required
from database import conexion

@pytest.fixture
def client():
    return TestClient(app)

app.dependency_overrides[admin_required] = lambda: {"username": "admin_user", "rol": "admin"}

def test_crear_libro_sin_afectar_db(client):
    payload = {
        "titulo": "Libro Temporal",
        "descripcion": "Test",
        "precio": 10.0,
        "iva": 2.0,
        "ventas": 0,
        "categoria_id": 1,
        "imagen": "dummy.jpg"
    }

    response = client.post("/libros", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "libro_id" in json_data

    libro_id = json_data["libro_id"]
    
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM libro_categoria WHERE libro_id = %s", (libro_id,))
        cursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))
        conexion.commit()
