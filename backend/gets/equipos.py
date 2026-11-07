from fastapi import Depends, HTTPException
from backend.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from backend.app import app


# Admin y planillero
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

# Admnin
@app.get("/equipos/{id_equipo}")
def obtener_equipo(
    id_equipo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT e.id_equipo, e.nombre, e.id_torneo, e.id_facultad,
               f.nombre AS facultad, e.ci_capitan,
               CONCAT(j.nombre, ' ', j.apellido) AS capitan
        FROM equipo e
        JOIN facultad f ON f.id_facultad = e.id_facultad
        JOIN jugador j ON j.ci = e.ci_capitan
        WHERE e.id_equipo = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_equipo,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return resultado[0]

# Admin y planillero
@app.get("/equipos/{id_equipo}/plantel")
def plantel_de_equipo(
    id_equipo: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT j.ci, j.nombre, j.apellido, j.tipo,
               ej.numero_camiseta,
               (e.ci_capitan = j.ci) AS es_capitan
        FROM equipo_jugador_torneo ej
        JOIN jugador j ON j.ci = ej.ci_jugador
        JOIN equipo e ON e.id_equipo = ej.id_equipo
        WHERE ej.id_equipo = %s
        ORDER BY ej.numero_camiseta
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_equipo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado