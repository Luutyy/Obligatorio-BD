from fastapi import Depends, HTTPException
from app.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from app.app import app

# Solo admin
@app.get("/jugadores")
def listar_jugadores(
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT
            j.ci,
            j.nombre,
            j.apellido,
            j.email,
            j.fecha_nacimiento,
            f.nombre AS facultad,
            j.tipo
        FROM jugador j
        JOIN facultad f ON f.id_facultad = j.id_facultad
        ORDER BY j.apellido, j.nombre
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

# Solo admin
@app.get("/jugadores/{ci}")
def obtener_jugador(
    ci: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT j.ci, j.nombre, j.apellido, j.email,
               j.fecha_nacimiento, j.id_facultad,
               f.nombre AS facultad, j.tipo
        FROM jugador j
        JOIN facultad f ON f.id_facultad = j.id_facultad
        WHERE j.ci = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (ci,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return resultado[0]

# Admin y planillero
@app.get("/torneos/{id_torneo}/jugadores-disponibles")
def jugadores_disponibles(
    id_torneo: int,
    id_facultad: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT j.ci, j.nombre, j.apellido, j.tipo
        FROM jugador j
        WHERE j.id_facultad = %s
          AND NOT EXISTS (
              SELECT 1
              FROM equipo_jugador_torneo ej
              WHERE ej.ci_jugador = j.ci
                AND ej.id_torneo = %s
          )
        ORDER BY j.apellido, j.nombre
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_facultad, id_torneo))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado