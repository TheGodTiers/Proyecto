# Usar una imagen base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del microservicio login
COPY login/main.py ./   
# Copiar database.py desde raíz
COPY ../../database.py ./database.py
# CORS
COPY ../../config.py ./config.py

EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
