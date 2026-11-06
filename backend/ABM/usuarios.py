
from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from typing import Literal
import bcrypt
from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario


class Usuario(BaseModel):
    correo: str
    contrasena: str
    rol: Literal["administrador", "planillero"]


# FUNCION PARA HASHEAR CONTRASEÑAS
def hashear_contrasena(contrasena: str):
    return bcrypt.hashpw(
        contrasena.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# POST: REGISTRAR USUARIO
@app.post("/usuarios", status_code=201)
def registrar_usuario(
    usuario: Usuario,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO login (correo, contrasena, rol)
        VALUES (%s, %s, %s)
    """

    hash_contrasena = hashear_contrasena(usuario.contrasena)
    valores = (
        usuario.correo,
        hash_contrasena,
        usuario.rol
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Usuario registrado correctamente",
            "correo": usuario.correo,
            "rol": usuario.rol
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese correo"
        )
    finally:
        cursor.close()


# GET: LISTAR USUARIOS
@app.get("/usuarios")
def listar_usuarios(
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT correo, rol
        FROM login
        ORDER BY correo
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado
