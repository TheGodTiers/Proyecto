from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import conexion
from config import setup_cors

app = FastAPI()

setup_cors(app)

@app.get("/home")
def home():
    try:
        with conexion.cursor() as cursor:
            query = """
                SELECT 
                    id,
                    titulo, 
                    descripcion, 
                    (precio + iva) AS precio_total,
                    imagen
                FROM libros
                ORDER BY ventas DESC
                LIMIT 3;
            """
            cursor.execute(query)
            libros = cursor.fetchall()
            
            return {"libros_mas_vendidos": libros}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
