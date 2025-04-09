from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from database import conexion
import pymysql.cursors
from datetime import datetime
from config import setup_cors

app = FastAPI()

setup_cors(app)

# Configuración del token
SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

# Función para verificar token y extraer usuario
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"usuario_id": int(usuario_id)}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# Modelos
class CarritoItem(BaseModel):
    libro_id: int
    cantidad: int

class CarritoUpdate(BaseModel):
    libro_id: int
    nueva_cantidad: int

class CarritoDelete(BaseModel):
    libro_id: int

# Endpoints

@app.post("/carrito/agregar")
def agregar_producto(item: CarritoItem, user=Depends(get_current_user)):
    usuario_id = user["usuario_id"]
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM carrito WHERE usuario_id=%s AND libro_id=%s"
        cursor.execute(sql, (usuario_id, item.libro_id))
        existing_item = cursor.fetchone()

        if existing_item:
            nueva_cantidad = existing_item['cantidad'] + item.cantidad
            sql = "UPDATE carrito SET cantidad=%s WHERE usuario_id=%s AND libro_id=%s"
            cursor.execute(sql, (nueva_cantidad, usuario_id, item.libro_id))
        else:
            sql = "INSERT INTO carrito (usuario_id, libro_id, cantidad) VALUES (%s, %s, %s)"
            cursor.execute(sql, (usuario_id, item.libro_id, item.cantidad))

        conexion.commit()

    return {"message": "Producto agregado al carrito"}

@app.put("/carrito/editar")
def editar_cantidad(update: CarritoUpdate, user=Depends(get_current_user)):
    usuario_id = user["usuario_id"]
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM carrito WHERE usuario_id=%s AND libro_id=%s"
        cursor.execute(sql, (usuario_id, update.libro_id))
        existing_item = cursor.fetchone()

        if not existing_item:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

        sql = "UPDATE carrito SET cantidad=%s WHERE usuario_id=%s AND libro_id=%s"
        cursor.execute(sql, (update.nueva_cantidad, usuario_id, update.libro_id))
        conexion.commit()

    return {"message": "Cantidad actualizada"}

@app.delete("/carrito/eliminar")
def eliminar_producto(delete: CarritoDelete, user=Depends(get_current_user)):
    usuario_id = user["usuario_id"]
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM carrito WHERE usuario_id=%s AND libro_id=%s"
        cursor.execute(sql, (usuario_id, delete.libro_id))
        existing_item = cursor.fetchone()

        if not existing_item:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

        sql = "DELETE FROM carrito WHERE usuario_id=%s AND libro_id=%s"
        cursor.execute(sql, (usuario_id, delete.libro_id))
        conexion.commit()

    return {"message": "Producto eliminado del carrito"}

@app.get("/carrito")
def ver_carrito(user=Depends(get_current_user)):
    usuario_id = user["usuario_id"]
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = """
            SELECT c.libro_id, l.titulo, ((l.precio + l.iva) * c.cantidad) as precio_total, l.imagen, c.cantidad 
            FROM carrito c
            JOIN libros l ON c.libro_id = l.id
            WHERE c.usuario_id = %s
        """
        cursor.execute(sql, (usuario_id,))
        carrito = cursor.fetchall()

        precio_final = sum(item['precio_total'] for item in carrito)

    return {"carrito": carrito, "precio_final": round(precio_final)}

@app.post("/carrito/realizar_compra")
def realizar_compra(user=Depends(get_current_user)):
    usuario_id = user["usuario_id"]
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = """
            SELECT 
                c.libro_id, 
                l.precio, 
                IFNULL(l.iva, 0) AS iva, 
                c.cantidad,
                ((l.precio + IFNULL(l.iva, 0)) * c.cantidad) AS precio_total
            FROM carrito c
            JOIN libros l ON c.libro_id = l.id
            WHERE c.usuario_id = %s
        """
        cursor.execute(sql, (usuario_id,))
        carrito = cursor.fetchall()

        if not carrito:
            raise HTTPException(status_code=400, detail="El carrito está vacío")
        
        total = sum(item["precio_total"] for item in carrito)

        sql = "INSERT INTO pedidos (usuario_id, fecha, total) VALUES (%s, %s, %s)"
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (usuario_id, fecha_actual, total))
        pedido_id = cursor.lastrowid  

        for item in carrito:
            sql = """
                INSERT INTO pedido_detalle (pedido_id, libro_id, cantidad, precio_unitario, iva)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                pedido_id,
                item['libro_id'],
                item['cantidad'],
                item['precio'],
                item['iva']
            ))
            
            sql = """
                UPDATE libros 
                SET ventas = ventas + %s 
                WHERE id = %s
            """
            cursor.execute(sql, (item['cantidad'], item['libro_id']))

        sql = "DELETE FROM carrito WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))

        conexion.commit()

    return {
        "message": "Compra realizada con éxito",
        "pedido_id": pedido_id,
        "total": round(total, 2)
    }


