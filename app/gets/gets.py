from fastapi import Depends
from app.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from app.app import app


@app.get("/facultades")
def listar_facultades(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT id_facultad, nombre
        FROM facultad
        ORDER BY nombre
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


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


# --------------------------------
# TORNEOS
# Administrador y planillero
# --------------------------------

@app.get("/torneos")
def listar_torneos(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM torneo
        ORDER BY anio DESC, semestre DESC
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# --------------------------------
# EQUIPOS
# Administrador y planillero
# --------------------------------

@app.get("/equipos")
def listar_equipos(
    id_torneo: int = None,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    if id_torneo is None:
        sql = """
            SELECT *
            FROM equipo
            ORDER BY nombre
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql)

    else:
        sql = """
            SELECT *
            FROM equipo
            WHERE id_torneo = %s
            ORDER BY nombre
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, (id_torneo,))

    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# --------------------------------
# PARTIDOS
# Administrador y planillero
# --------------------------------

@app.get("/partidos")
def listar_partidos(
    id_torneo: int = None,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    if id_torneo is None:
        sql = """
            SELECT *
            FROM partido
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql)

    else:
        sql = """
            SELECT *
            FROM partido
            WHERE id_torneo = %s
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, (id_torneo,))

    resultado = cursor.fetchall()
    cursor.close()

    return resultado