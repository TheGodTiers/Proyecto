from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from database import conexion

app = FastAPI()

# Configuración del token
SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"

# OAuth2: URL del login (microservicio de autenticación)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

# Modelo para crear un Libro
class Libro(BaseModel):
    titulo: str
    descripcion: str
    precio: float
    iva: float
    ventas: int
    categoria_id: int 

# Función para verificar el token y rol
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        rol: str = payload.get("rol")

        if username is None or rol is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        return {"username": username, "rol": rol}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

# Middleware de autorización para admin
def admin_required(user: dict = Depends(get_current_user)):
    if user["rol"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para esta acción")
    return user

# Endpoint protegido: Crear libro (solo admin)
@app.post("/libros")
def crear_libro(libro: Libro, user: dict = Depends(admin_required)):
    try:
        with conexion.cursor() as cursor:
            # Verificar que la categoría exista
            sql_categoria = "SELECT id FROM categorias WHERE id = %s"
            cursor.execute(sql_categoria, (libro.categoria_id,))
            categoria = cursor.fetchone()

            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")

            # Insertar el nuevo libro
            sql_libro = """
                INSERT INTO libros (titulo, descripcion, precio, iva, ventas)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores_libro = (
                libro.titulo,
                libro.descripcion,
                libro.precio,
                libro.iva,
                libro.ventas
            )
            cursor.execute(sql_libro, valores_libro)
            conexion.commit()

            # Obtener el ID del libro recién creado
            libro_id = cursor.lastrowid

            # Insertar en la tabla libro_categoria
            sql_libro_categoria = """
                INSERT INTO libro_categoria (libro_id, categoria_id)
                VALUES (%s, %s)
            """
            cursor.execute(sql_libro_categoria, (libro_id, libro.categoria_id))
            conexion.commit()

        return {"message": "Libro creado y asociado a la categoría exitosamente", "libro_id": libro_id}

    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))
