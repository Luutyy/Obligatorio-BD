from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import obtener_conexion
from datetime import date
from typing import Optional

app = FastAPI()

class Partido(BaseModel):
    id_toneo: int
    numero_fecha: int
    id_equipo_local: int
    id_equipo_visitante: int
    dia: str
    id_turno: int
    nombre_cancha: str
    id_complejo: int
    estado: str

#POST PARA DAR DE ALTA UN PARTIDOS
@app.post("/partido")
def registrar_partido( id_toneo: int, numero_fecha: int,id_equipo_local: int,id_equipo_visitante: int, dia: str, id_turno: int, nombre_cancha: str, id_complejo: int, estado: str, user=Depends(requiere_rol("administrador"))):

     sql = """
        INSERT INTO jugador
        (id_partido, id_torneo, numero_fecha, id_equipo_local, id_equipo_visitante, dia, id_turno, nombre_cancha, id_complejo, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (partido.id_partido, partido.id_torneo, partido.numero_fecha, partido.id_equipo_local, partido.id_equipo_visitante, partido.dia, partido.id_turno, partido.nombre_cancha, partido.id_complejo, partido.estado)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Partido registrado correctamente",
        }
    except mysql.connector.IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El documento ya existe o el equipo no es válido"
        )
    finally:
        cursor.close()
        conexion.close()

#DELETE PARA DAR DE BAJA PARTIDOS
@app.delete("/partidos/{id_partido}")
def eliminar_partido(id_partido: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            DELETE FROM partido
            WHERE ci = %s
        """
        cursor.execute(sql, (ci,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Partido no encontrado"
            )
        return {
            "mensaje": "Partido eliminado correctamente"
        }

    finally:
        cursor.close()
        conexion.close()

#PUT PARA MODIFICAR PARTIDOS
@app.delete("/Partido/{id_partido}")
def modificar_partido(id_partido: int,partido: Partido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            UPDATE partido
            SET nombre = %s,
                apellido = %s,
                ci = %s,
                email = %s,
                fecha_nacimiento= %s,
                id_facultad = %s,
                tipo = %s,
            WHERE ci = %s
        """
        cursor.execute(sql, (id_jugador,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Jugador no encontrado"
            )
        return {
            "mensaje": "Jugador eliminado correctamente"
        }

    finally:
        cursor.close()
        conexion.close()