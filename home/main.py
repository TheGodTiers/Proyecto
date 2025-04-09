from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import conexion
from config import setup_cors

app = FastAPI()

setup_cors(app)

#ruta para home

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
