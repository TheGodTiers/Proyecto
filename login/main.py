from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone
from database import conexion 
from config import setup_cors

app = FastAPI()

setup_cors(app)

# Configuración del token
SECRET_KEY = "Robin#707+"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Ruta para login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios WHERE username = %s"
    cursor.execute(query, (form_data.username,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    if user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "username": user["username"], "rol": user["rol"]},
        expires_delta=access_token_expires
    )

    return {"message": "inicio de sesion exitoso" ,"access_token": access_token, "token_type": "bearer"}

