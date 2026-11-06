import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.conexion import get_conexion
from dotenv import load_dotenv
import bcrypt

load_dotenv()
router = APIRouter()
SECRET = os.environ["JWT_SECRET"]
 
 
class LoginIn(BaseModel):
    correo: str
    contrasena: str
 

@router.post("/login")
def login(datos: LoginIn):
    conexion = get_conexion(None)
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT contrasena, rol FROM login WHERE correo = %s", (datos.correo,))
        filas = cursor.fetchall()
        cursor.close()
    finally:
        conexion.close()
 
    credenciales_ok = False
    if filas:
        try:
            credenciales_ok = bcrypt.checkpw(datos.contrasena.encode(), filas[0]["contrasena"].encode())
        except ValueError:  # la contraseña guardada no es un hash bcrypt
            credenciales_ok = False
    if not credenciales_ok:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
 
    token = jwt.encode(
        {"sub": datos.correo, "rol": filas[0]["rol"],
         "exp": datetime.now(timezone.utc) + timedelta(hours=8)},
        SECRET, algorithm="HS256")
    return {"token": token, "rol": filas[0]["rol"]}
 
 
security = HTTPBearer()

def usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return jwt.decode(
            credentials.credentials,
            SECRET,
            algorithms=["HS256"]
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o vencido"
        )
 
 
def requiere_rol(*roles):
    def verificar(user=Depends(usuario_actual)):
        if user["rol"] not in roles:
            raise HTTPException(status_code=403, detail="No tenés permiso para esta acción")
        return user
    return verificar
 
 
SOLO_ADMIN = requiere_rol("administrador")
ADMIN_Y_PLANILLERO = requiere_rol("administrador", "planillero")
 
 
def db_para_usuario(user=Depends(usuario_actual)):
    """Abre la conexión con el usuario de MySQL que corresponde al rol y la cierra al terminar."""
    conexion = get_conexion(user["rol"])
    try:
        yield conexion
    finally:
        conexion.close()