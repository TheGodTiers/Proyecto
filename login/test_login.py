from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

# Datos simulados del usuario
fake_user = {
    "id": 1,
    "username": "admin",
    "password": "admin123",
    "rol": "admin"
}

@patch("main.conexion")
def test_login_exitoso(mock_conexion):
    # Mock del cursor y su retorno
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fake_user
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.cursor.return_value = mock_cursor

    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["message"] == "inicio de sesion exitoso"
    assert json_data["token_type"] == "bearer"

@patch("main.conexion")
def test_login_usuario_no_encontrado(mock_conexion):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conexion.cursor.return_value = mock_cursor

    response = client.post(
        "/token",
        data={"username": "noexiste", "password": "algo"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario no encontrado"

@patch("main.conexion")
def test_login_password_incorrecta(mock_conexion):
    mock_cursor = MagicMock()
    user = fake_user.copy()
    user["password"] = "otra"
    mock_cursor.fetchone_
