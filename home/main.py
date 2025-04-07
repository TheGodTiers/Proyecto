from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import conexion

app = FastAPI()

@app.get("/home")
def home():
    try:
        with conexion.cursor() as cursor:
            query = """
                SELECT 
                    titulo, 
                    descripcion, 
                    (precio + iva) AS precio_total
                FROM libros
                ORDER BY ventas DESC
                LIMIT 3;
            """
            cursor.execute(query)
            libros = cursor.fetchall()
            return {"libros_mas_vendidos": libros}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
