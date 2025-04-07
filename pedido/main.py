from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from database import conexion  # Asegúrate de que este archivo tenga la conexión MySQL
import pymysql.cursors

app = FastAPI()

SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("rol") != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido solo para administradores")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@app.get("/pedidos")
def listar_pedidos(admin=Depends(get_current_admin)):
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        # Obtener todos los pedidos
        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()

        resultados = []

        for pedido in pedidos:
            cursor.execute("""
                SELECT pd.libro_id, l.titulo, pd.cantidad, pd.precio_unitario, pd.iva
                FROM pedido_detalle pd
                JOIN libros l ON pd.libro_id = l.id
                WHERE pd.pedido_id = %s
            """, (pedido["id"],))
            detalles = cursor.fetchall()

            resultados.append({
                "pedido_id": pedido["id"],
                "usuario_id": pedido["usuario_id"],
                "fecha": pedido["fecha"],
                "total": float(pedido["total"]),
                "detalles": detalles
            })

    return resultados
