# Usar una imagen base
FROM python:3.13-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del microservicio carrito
COPY carrito/main.py ./   
# Copiar database.py desde raíz
COPY ../../database.py ./database.py
# CORS
COPY ../../config.py ./config.py

EXPOSE 8004

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
