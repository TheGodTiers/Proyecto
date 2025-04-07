from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from database import conexion
from pymysql.cursors import DictCursor

app = FastAPI()

# Seguridad 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")  # Cambia el URL si es necesario
SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"

# Modelo de categoría
class Categoria(BaseModel):
    categoria: str

# Función para obtener el usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("rol")
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return {"username": username, "rol": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# Función para requerir rol de administrador
def admin_required(user: dict = Depends(get_current_user)):
    if user.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return user

# ----------------------------------------------------------------
# 🚀 Rutas públicas y protegidas:

# Mostrar todas las categorías con sus libros (público)
@app.get("/categorias")
def obtener_categorias():
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute("SELECT id, categoria FROM categorias")
            categorias = cursor.fetchall()

            resultado = []

            for cat in categorias:
                cursor.execute("""
                    SELECT l.titulo, l.descripcion, (l.precio + l.iva) AS precio_con_iva
                    FROM libro_categoria lc
                    INNER JOIN libros l ON lc.libro_id = l.id
                    WHERE lc.categoria_id = %s
                """, (cat["id"],))

                libros = cursor.fetchall()

                resultado.append({
                    "categoria": cat["categoria"],
                    "libros": libros
                })

            return resultado

    except Exception as e:
        return {"error": str(e)}

# Crear categoría (solo admin)
@app.post("/categorias")
def crear_categoria(categoria: Categoria, user: dict = Depends(admin_required)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM categorias WHERE categoria = %s", (categoria.categoria,))
            existe = cursor.fetchone()

            if existe:
                raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

            cursor.execute("INSERT INTO categorias (categoria) VALUES (%s)", (categoria.categoria,))
            conexion.commit()
            return {"mensaje": "Categoría creada correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}

# Editar categoría (solo admin)
@app.put("/categorias/{id_categoria}")
def editar_categoria(id_categoria: int, categoria: Categoria, user: dict = Depends(admin_required)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM categorias WHERE categoria = %s AND id != %s", (categoria.categoria, id_categoria))
            existe = cursor.fetchone()

            if existe:
                raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

            cursor.execute("UPDATE categorias SET categoria = %s WHERE id = %s", (categoria.categoria, id_categoria))
            conexion.commit()
            return {"mensaje": "Categoría actualizada correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}

# Eliminar categoría (solo admin)
@app.delete("/categorias/{id_categoria}")
def eliminar_categoria(id_categoria: int, user: dict = Depends(admin_required)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM libro_categoria WHERE categoria_id = %s", (id_categoria,))
            cursor.execute("DELETE FROM categorias WHERE id = %s", (id_categoria,))
            conexion.commit()
            return {"mensaje": "Categoría eliminada correctamente"}

    except Exception as e:
        return {"error": str(e)}
